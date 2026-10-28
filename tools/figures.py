"""The figures of the two papers (author 2026-10-28: figures in the design of the Series 00 figures — the covers' ground
and AURORA, black-glass hexagons, the covers' type, no glow, 600 ppi — drawn only from published content).

  python tools/figures.py                  every figure: data → render → figures/fig-<id>.pdf, fig-<id>.tex, checks
  python tools/figures.py rose triangle    only these figures
  python tools/figures.py --data           only the data files and pages
  python tools/figures.py --check          checks only        → out/FIGURE-GATE.md (exit 1 on failure)

Design: the Series 00 figure library (master/figures/web: lib.js — the light layer of ground, aurora and black glass in
Three.js and the vector HUD; style.css; the TGP faces; three.js r186), copied unchanged into figures/web/ and checked
by hash against Series 00 on every run. Each figure is one module figures/web/fig-<id>.js (geometry and words) and one
data file written here. Every figure is drawn at its printed size: 132 mm, the measure of the papers.

Single source: every word and number a figure prints comes from programme.yaml, src/theses.yaml,
src/thesis-instances.yaml, the cards src/problems/*.yaml, src/changes.yaml, the hand-written paper text, the
candidate pool and the literature-check queries; each phrase is checked here to occur in its source (src_has), and the
check below finds every drawn line in the figure's PDF text.

Render (as Series 00): local HTTP server + headless Chrome with software WebGL. ?layer=gl → the light layer as a
lossless PNG at 605 ppi; ?layer=print → that PNG under the HUD, printed to PDF, the page set to the light layer's box.
The HUD reports lines that do not fit (data-fit), the smallest type (data-minpt), every line it drew (data-lines) and
the link areas (data-links: a cell that names a problem or a thesis), from which figures/fig-<id>.tex places links to
the cards and theses of the paper over the figure.
Checks: page 132 mm wide; one image ≥ 600 ppi, lossless; no Type 3 font; only Segoe UI and the TGP faces; type
≥ 6.5 pt, nothing condensed or overflowing; every drawn line searchable in the PDF; the number printed as FIGURE n
equals the figure's place in its paper; the accent colours that carry categories stay apart under simulated
protanopia, deuteranopia and tritanopia, and every category also has a non-colour mark (group, position or label).
"""
import hashlib
import http.server
import json
import re
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
import unicodedata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parents[1]
SERIES = HERE.parent
DESIGN = SERIES / "master" / "figures" / "web"
WEB = HERE / "figures" / "web"
FIGDIR = HERE / "figures"
OUT = HERE / "out"
LOCAL = json.loads((HERE / "local.json").read_text(encoding="utf-8")) if (HERE / "local.json").exists() else {}
CHROME = LOCAL.get("chrome", "")
MEASURE = 132.0
PPI, RENDER_PPI = 600, 605
CSS_PX_PER_MM = 96 / 25.4
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))

# figure id → (paper, height in mm)
FIGS = {"programme": ("overview", 132.0), "method": ("overview", 138.0), "series": ("overview", 124.0),
        "works": ("paper-I", 132.0), "theses": ("paper-I", 150.0), "chain": ("paper-I", 152.0),
        "relations": ("paper-I", 156.0), "triangle": ("paper-I", 114.0),
        "rose": ("paper-II", 160.0), "selection": ("paper-II", 106.0), "card": ("paper-II", 144.0),
        "credit": ("paper-II", 88.0), "matrix": ("paper-II", 150.0)}
FOOT = {"overview": "The Grothendieckian Programme: An Overview", "paper-I": "The Rising-Sea Theses",
        "paper-II": "The 57 Grothendieckian Problems"}
PAPERS = ("overview", "paper-I", "paper-II")          # the order of the three papers (author, 2026-10-28)
WORKS = ("S01", "S02", "S03", "S04", "S05", "S06", "S07")
# the sources, in the Series 00 folder or, in the published repository, the copies beside the papers' sources
_first = lambda *ps: next((p for p in ps if p.exists()), ps[-1])
PROGRAMME = _first(SERIES / "programme.yaml", HERE / "src" / "programme.yaml")
S00FIG = _first(DESIGN / "data-programme.json", HERE / "figures" / "web" / "s00-data-programme.json")
POOL = _first(HERE / "candidates" / "pool.json", HERE / "data" / "candidates.json")


# ------------------------------------------------------------------------------------------------ sources ------------
def read(p):
    return Path(p).read_text(encoding="utf-8")


def norm(s):
    s = unicodedata.normalize("NFKC", str(s)).replace("’", "'").replace("‘", "'")
    s = re.sub(r"\[@[^\]]*\]", " ", s)                        # citations are not part of a phrase
    s = re.sub(r"[*_`]", "", s)
    return " ".join(s.split()).lower()


class Sources:
    def __init__(self):
        self.prog = yaml.safe_load(read(PROGRAMME))
        self.theses = yaml.safe_load(read(HERE / "src" / "theses.yaml"))
        self.inst = yaml.safe_load(read(HERE / "src" / "thesis-instances.yaml"))
        self.cards = []
        for f in sorted((HERE / "src" / "problems").glob("*.yaml")):
            self.cards += yaml.safe_load(read(f))
        self.cards.sort(key=lambda c: c["num"])
        self.changes = yaml.safe_load(read(HERE / "src" / "changes.yaml"))
        self.text = {
            "paper-I": "\n".join(read(HERE / "src" / "paper-I" / f) for f in
                                 ("01-introduction.md", "45-together.md", "50-limits.md")),
            "paper-II": read(HERE / "src" / "paper-II" / "01-introduction.md"),
            "overview": read(HERE / "src" / "overview" / "01-overview.md"),
            "theses": read(HERE / "src" / "theses.yaml"), "instances": read(HERE / "src" / "thesis-instances.yaml"),
            "cards": "\n".join(read(f) for f in sorted((HERE / "src" / "problems").glob("*.yaml"))),
            "programme": read(PROGRAMME),
            "s00-figure-1": read(S00FIG),
        }
        self.normed = {k: norm(v) for k, v in self.text.items()}
        self.checked = []
        self.release = {"s00": json.loads(read(SERIES / "release-kit" / "state.json")),
                        "s00-release": yaml.safe_load(read(SERIES / "release-kit" / "release.yaml"))} \
            if (SERIES / "release-kit").exists() else json.loads(read(HERE / "figures" / "web" / "s00-release.json"))

    def on_page(self, phrase, work, page):
        """phrase occurs on a printed page of a sealed work (quote_gate's matching); returns the phrase as given"""
        import quote_gate
        labels, keys = quote_gate.pages_of(work)
        ok = page in labels and quote_gate.key(phrase) in keys[labels.index(page)].split("|")[0]
        self.checked.append((phrase, (f"{work} p. {page}",), ok))
        return phrase

    def has(self, phrase, *where):
        """phrase occurs (normalised) in one of the named sources; returns the phrase as given"""
        p = norm(phrase)
        ok = any(p in self.normed[w] for w in where)
        self.checked.append((phrase, where, ok))
        return phrase


# ------------------------------------------------------------------------------------------------ data ----------------
def kind_level(c):
    return {"num": c["num"], "kind": c["kind"], "level": c["level"], "work": c["work"]}


def data_works(S):
    P, facts = S.prog, {w["series"]: w for w in S.prog["facts"]["works"]}
    cells = []
    for c in P["cells"]:
        f, w = P["figure_cells"][c["series"]], facts[c["series"]]
        cells.append({"series": c["series"], "position": c["position"], "colour": c["colour"], "name": f["name"],
                      "role": f["role"], "formula": w["cover_centre"]["formula"],
                      "size": f"{w['volumes']} volumes · {w['pages']:,} pages"})
    tot = P["facts"]["totals"]
    assert sum(w["pages"] for w in facts.values()) == tot["pages"], "pages do not add up"
    legend = json.loads(S.text["s00-figure-1"])["legend"]
    return {"title": "THE SEVEN WORKS", "right": f"{tot['works']} WORKS · {tot['volumes']} VOLUMES · {tot['pages']:,} PAGES",
            "cells": cells, "shared_edge": S.has(P["shared_edge"]["label"], "programme").upper(),
            "legend": [S.has(legend[0], "s00-figure-1"), S.has(legend[1], "s00-figure-1"),
                       S.has(legend[2], "s00-figure-1").replace(" | ", " "), S.has(legend[3], "s00-figure-1")]}


GROUPS = [("REPRESENTATION", "cyan", (1, 2, 3)), ("OPERATION", "blue", (4, 5, 6, 7)),
          ("METHOD", "gold", (8, 9, 10, 11, 12))]


def data_theses(S):
    groups = []
    for name, colour, nums in GROUPS:
        items = []
        for t in S.theses:
            if t["num"] in nums:
                probs = [c["num"] for c in S.cards if c["thesis"] == t["num"]]
                items.append({"num": t["num"], "title": S.has(t["title"], "theses"), "problems": probs})
        groups.append({"name": name, "colour": colour, "range": f"THESES {nums[0]}–{nums[-1]}", "items": items})
    return {"title": "THE TWELVE THESES", "right": f"THE {len(S.cards)} GROTHENDIECKIAN PROBLEMS BY THESIS",
            "groups": groups, "note": "number of problems at which the thesis can be tested"}


def data_chain(S):
    t6 = next(t for t in S.theses if t["num"] == 6)
    stages = [S.has(s, "theses") for s in ("operational completion", "mathematical validity", "epistemic promotion",
                                            "publication")]
    rule = S.has("Every implication requires a separately named input, judgment, and authority.", "theses")
    needs = [[S.has("a check of the mathematics", "theses"), S.has("a check of fidelity to the intended statement", "theses")],
             [S.has("a decision on status", "theses")], [S.has("an act of authorisation", "theses")]]
    fails = [[S.has("a distributed computation can finish without error while producing no mathematical object", "theses"),
              S.has("a kernel can accept a proof of a statement that is not the statement intended", "theses")],
             [S.has("a valid result can rest on a premise whose status does not permit promotion", "theses")],
             [S.has("a promoted result can still lack the authority to be published", "theses")]]
    who = [S.has("Retrieval may supply candidate evidence but cannot change truth status.", "theses"),
           S.has("Humans authorize publication.", "theses")]
    broken = [S.has(s, "instances") for s in (
        "a worker can write directly to the status store",
        "an evaluator shares mutable code or keys with the candidate",
        "a signature is detached from the artifact hash",
        "a promotion service accepts a producer's boolean assertion instead of replayable receipts")]
    verdict = S.has("the proposition does not apply and the system has failed its constitution", "instances")
    assert t6["title"] == "A chain of non-implications"
    return {"title": "THESES 6 AND 7", "right": "SERIES 01 · VOLUMES III AND V", "stages": stages, "rule": rule,
            "needs": needs, "fails": fails, "who": who, "broken": broken, "verdict": verdict,
            "heads": ["THESIS 6 · A CHAIN OF NON-IMPLICATIONS", "REQUIRES", "FAILS WHEN",
                      "THESIS 7 · MACHINES PROPOSE; HUMANS AUTHORIZE", "THE SEPARATION FAILS IF"],
            "src": ["S01 · VOL. III · CH. 3 · P. 8004", "S01 · P. 7966",
                    "S01 · VOL. V · PROPOSITION 1.3 · PP. 11913–11914"]}


def data_relations(S):
    T = {t["num"]: t["title"] for t in S.theses}
    nodes = [{"num": n, "title": T[n], "group": next(g[1] for g in GROUPS if n in g[2])} for n in range(1, 13)]
    p = "paper-I"
    edges = {
        "artefact": S.has("together say what an artefact is", p),
        "depends": S.has("Thesis 6 depends on both", p),
        "outside": S.has("locates the last of these passages outside the producing system", p),
        "step": S.has("the reasoning step that the others constrain", p),
        "method": S.has("the method of discovery that the architecture is meant to support", p),
        "idle": S.has("would be idle without Thesis 11", p),
        "ledger": S.has("makes the ledger of Thesis 12 checkable entry by entry", p),
        "conditions": S.has("held to the conditions", p),
    }
    return {"title": "HOW THE THESES FIT TOGETHER", "right": "SECTION 5", "nodes": nodes, "edges": edges,
            "s01": "S01, Vol. III, §5.1", "s01_line": S.has("an extension which deletes the predicate expressing a "
                                                           "contradiction", p),
            "s01_end": S.has("has not resolved the obstruction", p)}


def data_triangle(S):
    p = "paper-I"
    keeps = [S.has(s, p) for s in ("the hashes of the three sections", "the three local receipts", "the oriented face",
                                   "the transition digests", "the two composite results", "the normalisation rule",
                                   "the equality predicate", "the checker and its environment", "the counterexample")]
    acts = [(1, S.has("make the failure locatable", p)), (2, S.has("keep the pairwise receipts valid while the triangle fails", p)),
            (5, S.has("an obstruction with a location rather than a score", p)),
            (6, S.has("the refusal to read three successful comparisons as a successful gluing", p)),
            (10, S.has("the failure becomes the input of a proposal", p))]
    return {"title": "A WORKED EXAMPLE", "right": "SERIES 01 · VOL. III · §61.18 · P. 9227",
            "pass": S.has("All three edge predicates pass.", p), "excluded": S.has("an unrelated fourth chart", p),
            "keeps": keeps, "acts": [{"num": n, "text": t} for n, t in acts],
            "quote": S.has("The three pairwise receipts remain historically valid; they simply do not establish the failed "
                           "triangular law.", p),
            "heads": ["THREE CHARTS · THREE PASSING COMPARISONS", "THE RECORD KEEPS", "EXCLUDED", "WHERE THE THESES ACT"]}


def data_rose(S):
    P, facts = S.prog, {w["series"]: w for w in S.prog["facts"]["works"]}
    cells = []
    order = {"math": 0, "machine": 1, "formal": 2}
    for c in P["cells"]:
        w = "S" + c["series"]
        cs = sorted((x for x in S.cards if x["work"] == w), key=lambda x: (order[x["kind"]], x["num"]))
        f = P["figure_cells"][c["series"]]
        cells.append({"series": c["series"], "position": c["position"], "colour": c["colour"], "name": f["name"],
                      "role": f["role"], "problems": [kind_level(x) for x in cs],
                      "range": f"PROBLEMS {min(x['num'] for x in cs)}–{max(x['num'] for x in cs)}"})
    k, lv = Counter(c["kind"] for c in S.cards), Counter(c["level"] for c in S.cards)
    return {"title": "THE 57 GROTHENDIECKIAN PROBLEMS", "right": "57 = 35 + 22", "cells": cells,
            "kinds": [["math", f"{k['math']} MATHEMATICAL"], ["machine", f"{k['machine']} MACHINE"],
                      ["formal", f"{k['formal']} FORMALIZATION"]],
            "levels": [["entry", f"{lv['entry']} ENTRY LEVEL"], ["research", f"{lv['research']} RESEARCH LEVEL"],
                       ["programme", f"{lv['programme']} PROGRAMME LEVEL"]],
            "parts": ["PART I · THE MACHINE · PROBLEMS 1–35", "PART II · THE FIVE RESEARCH SUBJECTS · PROBLEMS 36–57"]}


def data_selection(S):
    pool = json.loads(read(POOL))
    per = Counter(p["work"] for p in pool)
    queries = yaml.safe_load(read(HERE / "src" / "litcheck-queries.yaml"))
    nq = sum(len(v) for k, v in queries.items() if str(k).isdigit() and 1 <= int(k) <= 57)
    kinds = Counter(c["kind"] for c in S.cards)
    rep = [c["num"] for c in S.changes if c["why"].startswith("Replaced")]
    nar = [c["num"] for c in S.changes if c["why"].startswith("Narrowed")]
    assert len(rep) + len(nar) == len(S.changes)
    p = "paper-II"
    rules = [S.has(s, p) for s in ("The problem is stated in the source.", "The problem is not a named conjecture.",
                                   "The problem is open as far as we can determine.", "The problem has a decision criterion.")]
    return {"title": "HOW THE PROBLEMS WERE CHOSEN", "right": "SECTIONS 1.1 AND 1.3",
            "works": [{"work": w, "n": per[w]} for w in WORKS], "total": len(pool), "rules": rules,
            "searched": [S.has("arXiv, OpenAlex, zbMATH Open and Crossref", p).replace(" and ", " · ").replace(", ", " · "),
                         "the Lean 4 repository, Mathlib and Formal Conjectures"],
            "queries": nq, "replaced": rep, "narrowed": nar,
            "final": {"n": len(S.cards), "p1": sum(1 for c in S.cards if c["num"] <= 35),
                      "p2": sum(1 for c in S.cards if c["num"] >= 36),
                      "kinds": [kinds["math"], kinds["machine"], kinds["formal"]]},
            "heads": ["ITEMS STATED AS OPEN, CONDITIONAL, CONJECTURAL OR OWED", "FOUR RULES", "LITERATURE CHECK · 28 OCTOBER 2026",
                      "PROBLEMS"]}


def data_card(S):
    md = read(HERE / "src" / "paper-II" / "30-part2.md")
    m = re.search(r"::: \{\.problem #problem-49 .*?\n(.*?)\n::: *\n::: *\n", md, re.S)
    assert m, "card 49 not found in 30-part2.md"
    fields = re.findall(r'::: \{\.field label="([^"]+)"\}\n(.*?)\n:::', m.group(0), re.S)

    def plain(s):
        s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
        s = re.sub(r"[*`]", "", s).replace("\\", "")
        return " ".join(s.split())
    p = "paper-II"
    what = {
        "Thesis": S.has("names the thesis of The Rising-Sea Theses to which the problem belongs", p),
        "Source": S.has("names the work, the place in it and the page of the sealed PDF", p),
        "Status in the source": S.has("is the status that the source assigns, in its own notation", p),
        "Statement": S.has("states the problem", p),
        "What the source establishes": S.has("records what has been proved or specified", p),
        "Proposed by": S.has("names the source of the problem", p),
        "Background": S.has("cites the standard literature on which the problem rests", p),
        "Solved when": S.has("states the decision criterion", p),
        "Literature check (28 October 2026)": S.has("records what the check of 28 October 2026 found", p),
        "Discussion": S.has("Each problem has its own discussion thread", p)[0].lower() + "ach problem has its own discussion thread",
    }
    rows = [{"label": lab, "text": plain(txt), "what": what[lab]} for lab, txt in fields]
    assert [r["label"] for r in rows] == list(what), [r["label"] for r in rows]
    c49 = next(c for c in S.cards if c["num"] == 49)
    return {"title": "WHAT A CARD CONTAINS", "right": "PROBLEM 49 AS AN EXAMPLE", "rows": rows,
            "heading": {"num": 49, "title": c49["title"], "tags": "FORMALIZATION · ENTRY LEVEL"},
            "checks": [S.has("The words between quotation marks in a card are those of the source, on the pages named; this has "
                             "been checked by machine for every quotation.", p),
                       S.has("The searches, their dates and their first results are published with the paper.", p)],
            "lean": S.has("The repository gives the statements in Lean", "cards") + " (P49.lean)"}


def data_credit(S):
    p = "paper-II"
    kinds = [S.has(s, p) for s in ("A solution", "a partial result", "a counterexample to a problem as stated",
                                   "a report that a problem is already solved", "a correction to a card")]
    return {"title": "PARTICIPATION AND CREDIT", "right": "NO PRIZE IS ATTACHED TO ANY PROBLEM",
            "kinds": [kinds[0].capitalize()] + kinds[1:],
            "via": S.has("is submitted through the repository of the paper", p),
            "thread": S.has("Each problem has its own discussion thread, named in its card", p),
            "check": S.has("checked by someone other than its author and other than us", p),
            "records": [S.has("in the next version of this paper", p),
                        S.has("in the next edition of the work from which the problem comes, under the solver's name", p),
                        S.has("in a list of solutions kept with the repository", p)],
            "errata": S.has("recorded in the errata of the repository", p),
            "heads": ["WHAT CAN BE SUBMITTED", "WHERE", "HOW IT IS CHECKED", "A SOLUTION THAT MEETS THE CRITERION IS RECORDED",
                      "A CORRECTION"]}


def data_matrix(S):
    T = {t["num"]: t["title"] for t in S.theses}
    rows = []
    for n in range(1, 13):
        cells = {w: [kind_level(c) for c in S.cards if c["thesis"] == n and c["work"] == w] for w in WORKS}
        rows.append({"num": n, "title": T[n], "cells": cells, "n": sum(len(v) for v in cells.values())})
    cols = {w: sum(1 for c in S.cards if c["work"] == w) for w in WORKS}
    k = Counter(c["kind"] for c in S.cards)
    return {"title": "THE PROBLEMS BY THESIS AND BY WORK", "right": "APPENDIX A", "rows": rows, "cols": cols,
            "total": len(S.cards), "kinds": [["math", f"{k['math']} MATHEMATICAL"], ["machine", f"{k['machine']} MACHINE"],
                                             ["formal", f"{k['formal']} FORMALIZATION"]]}


def data_programme(S):
    d = data_works(S)
    t = S.prog["facts"]["totals"]
    return dict(d, title="THE GROTHENDIECKIAN PROGRAMME", right=f"{t['works']} WORKS · {t['pages']:,} PAGES")


def data_method(S):
    cyc = S.prog["figures"]["cycle"]
    for st in cyc["steps"]:
        S.has(st["code"], "programme")
        for l in st["lines"]:
            S.has(l, "programme")
    tests = []
    for g in cyc["tests"]["groups"]:
        body = g.get("text") or " · ".join(g["items"])
        tests.append({"head": S.has(g["head"], "programme"), "text": S.has(body, "programme") if "text" in g else body})
        for it in g.get("items", []):
            S.has(it, "programme")
    o = "overview"
    kept = [["SERIES 03", S.on_page("A mechanism that failed for a structural reason became a no-go theorem", "S03", "iv")],
            ["SERIES 04 · 05", S.on_page("what fails is recorded as an obstruction", "S04", "v")],
            ["SERIES 06", S.on_page("What fails is recorded as a proof obligation.", "S06", "v")],
            ["SERIES 07", S.on_page("What fails is recorded where it fails.", "S07", "v")]]
    labels = [["SERIES 01", "E · S · D · R · C · O · Q", S.has("E/S/D/R/C/O/Q", "theses")],
              ["SERIES 02", "LICENCE GRADE · FALSIFICATION CONDITION", S.has("licence grade and a falsification condition", o)],
              ["SERIES 03", "[T] · [C] · [O] · [E] · [N] · [K]", S.on_page("Every substantive mathematical claim is marked [T], [C], [O], [E], [N], or [K].", "S03", "v")],
              ["SERIES 04 · 05", "KNOWN · CONDITIONAL · NEW · OPEN", S.on_page("[ KNOWN ], [ CONDITIONAL ], [ NEW ], [ OPEN ]", "S04", "v")],
              ["SERIES 06", "+ REPROVED · DISPUTED", S.on_page("this work adds [ REPROVED ]", "S06", "vi")],
              ["SERIES 07", "ESTABLISHED · THEOREM · CONJECTURE · DESIGN · FORMAL TARGET",
               S.on_page("[ ESTABLISHED ], [ THEOREM ], [ CONJECTURE ], [ DESIGN ] or [ FORMAL TARGET ]", "S07", "vi")]]
    return {"title": "RECURSIVE MATHEMATICAL DISCOVERY", "right": "SERIES 03–07",
            "steps": cyc["steps"], "tests": tests, "kept": kept,
            "labels": [[a, b] for a, b, _ in labels],
            "rule": S.on_page("No result is presented at a strength greater than its proof.", "S03", "iv"),
            "heads": ["TESTED AGAINST WHAT IS KNOWN", "WHAT DOES NOT SURVIVE IS KEPT", "THE STATUS OF EVERY STATEMENT"],
            "source": "THE SERIES NOTE OF THE FIVE WORKS"}


def data_series(S):
    P = S.prog
    rel = S.release
    st, r0 = rel["s00"], rel["s00-release"]
    rows = [{"series": "00", "name": "The Grothendieckian Programme", "role": "the overview volume", "date": st["publication_date"],
             "size": f"{len(r0['volumes'])} volume · {r0['volumes'][0]['pages']} pages", "doi": st["zenodo_concept_doi"],
             "repo": st["github_repo"]}]
    for w in sorted(P["facts"]["works"], key=lambda w: (w["publication_date"], w["series"])):
        f = P["figure_cells"][w["series"]]
        rows.append({"series": w["series"], "name": " ".join(f["name"]), "role": f["role"], "date": w["publication_date"],
                     "size": f"{w['volumes']} volumes · {w['pages']:,} pages", "doi": w["concept_doi"],
                     "repo": w["repository"]})
    rows.sort(key=lambda r: (r["date"], r["series"]))
    o = "overview"
    return {"title": "THE SERIES AND ITS RECORDS", "right": f"EDITION 1 · v{P['facts']['works'][0]['version']}",
            "rows": rows, "colour": {c["series"]: c["colour"] for c in P["cells"]} | {"00": "cyan"},
            "heads": ["RELEASED", "WORK", "SIZE", "ZENODO · GITHUB", "THE THREE PAPERS", "REVIEW AND CONTINUATION · GITHUB"],
            "papers": [["1", "The Grothendieckian Programme: An Overview"], ["2", "The Rising-Sea Theses"],
                       ["3", "The 57 Grothendieckian Problems"]],
            "repo": "AlienMuse/grothendieckian-problems",
            "repo_lines": ["57 problems: " + S.has("Each has its own thread", o).lower(),
                           S.has("A solution that meets its criterion is recorded under the solver’s name", o),
                           S.has("corrections are listed with the version in which they are made", o).capitalize()],
            "every": [S.has("a signed list of the checksums of its files", o), S.has("BY-NC-ND 4.0", o),
                      S.has("Zenodo community", o)]}


BUILD = {"programme": data_programme, "method": data_method, "series": data_series, "works": data_works, "theses": data_theses, "chain": data_chain, "relations": data_relations,
         "triangle": data_triangle, "rose": data_rose, "selection": data_selection, "card": data_card,
         "credit": data_credit, "matrix": data_matrix}


# ------------------------------------------------------------------------------------------------ numbering -----------
def numbers():
    """{figure id: number}: the order of ::: {.figure #fig:<id> …} in each paper's ORDER.txt files"""
    out = {}
    for paper in PAPERS:
        src = HERE / "src" / paper
        order = [l.strip() for l in read(src / "ORDER.txt").splitlines() if l.strip() and not l.startswith("#")]
        ids = []
        for f in order:
            ids += re.findall(r"::: \{\.figure #fig:([a-z]+)", read(src / f))
        assert len(ids) == len(set(ids)), f"a figure is placed twice in {paper}: {ids}"
        for k, fid in enumerate(ids):
            assert FIGS[fid][0] == paper, f"figure {fid} placed in {paper}"
            out[fid] = k + 1
    return out


# ------------------------------------------------------------------------------------------------ design copy ---------
def sync_design():
    """lib.js, style.css, the TGP faces and three.js from Series 00, unchanged (hash-checked). Outside the Series 00
    folder (the published repository) the copies in figures/web are checked against DESIGN-SOURCE.json instead."""
    WEB.mkdir(parents=True, exist_ok=True)
    if not DESIGN.exists():
        rec = json.loads((WEB / "DESIGN-SOURCE.json").read_text(encoding="utf-8"))["sha256"]
        bad = [k for k, h in rec.items() if hashlib.sha256((WEB / k).read_bytes()).hexdigest() != h]
        if bad:
            sys.exit(f"the design files differ from DESIGN-SOURCE.json: {bad}")
        return len(rec)
    rec = {}
    for rel in ["lib.js", "style.css"] + [str(p.relative_to(DESIGN)).replace("\\", "/") for p in
                                         list((DESIGN / "fonts").glob("*")) + list((DESIGN / "vendor").rglob("*")) if p.is_file()]:
        src, dst = DESIGN / rel, WEB / rel
        h = hashlib.sha256(src.read_bytes()).hexdigest()
        if not dst.exists() or hashlib.sha256(dst.read_bytes()).hexdigest() != h:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
        rec[rel] = h
    (WEB / "DESIGN-SOURCE.json").write_text(json.dumps({"from": "Series 00, master/figures/web (unchanged)",
                                                       "sha256": rec}, indent=1) + "\n", encoding="utf-8")
    return len(rec)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Figure {num} — {title}</title>
<!-- written by tools/figures.py; the figure is fig-{fid}.js, the design lib.js (Series 00) -->
<link rel="stylesheet" href="style.css">
<style>@page {{ size: {w}mm {h}mm; margin: 0; }}
#figure, #gl, #glimg, #hud {{ width: {w}mm; height: {h}mm; }}</style>
<script type="importmap">
{{ "imports": {{ "three": "./vendor/three/build/three.module.js" }} }}
</script>
</head>
<body>
<main id="figure">
  <canvas id="gl"></canvas>
  <img id="glimg" alt="" src="gl-{fid}.png" decoding="sync">
  <svg id="hud" xmlns="http://www.w3.org/2000/svg" aria-label="Figure {num}: {title}"></svg>
</main>
<script type="module">
import {{ run }} from './lib.js';
import * as F from './fig-{fid}.js';
await run(F, 'data-{fid}.json');
</script>
</body>
</html>
"""


def write_data(fids, nums, S):
    meta = {p: yaml.safe_load(read(HERE / "src" / p / "metadata.yaml")) for p in PAPERS}
    for fid in fids:
        paper, h = FIGS[fid]
        data = BUILD[fid](S)
        doi = (meta[paper].get("doi") or "").strip()
        foot = f"{FOOT[paper]} · Vincent Liu · {('doi:' + doi) if doi else 'preprint, 2026'} · CC BY 4.0"
        data = {"id": fid, "number": nums[fid], "size_mm": [MEASURE, h], "footer": foot, **data}
        (WEB / f"data-{fid}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        (WEB / f"{fid}.html").write_text(PAGE.format(num=nums[fid], title=data["title"].title(), fid=fid, w=MEASURE, h=h),
                                         encoding="utf-8")


# ------------------------------------------------------------------------------------------------ render --------------
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def serve():
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), partial(Quiet, directory=str(WEB)))
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def chrome(args, timeout=900):
    prof = tempfile.mkdtemp(prefix="rs-fig-chrome-")
    base = [CHROME, "--headless=new", f"--user-data-dir={prof}", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
            "--ignore-gpu-blocklist", "--hide-scrollbars", "--disable-gpu-sandbox", "--no-first-run",
            "--no-default-browser-check", "--run-all-compositor-stages-before-draw"]
    r = subprocess.run(base + args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    shutil.rmtree(prof, ignore_errors=True)
    return r


def unescape(s):
    return s.replace("&quot;", '"').replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")


def render_one(fid, port):
    from PIL import Image, ImageStat
    import pikepdf
    import pymupdf
    out = []
    w_mm, h_mm = MEASURE, FIGS[fid][1]
    url = f"http://127.0.0.1:{port}/{fid}.html"
    gl = WEB / f"gl-{fid}.png"
    for attempt, budget in ((1, 60000), (2, 180000)):       # an empty light layer is rendered again (Series 00)
        gl.unlink(missing_ok=True)
        r = chrome([f"--window-size={round(w_mm * CSS_PX_PER_MM)},{round(h_mm * CSS_PX_PER_MM)}",
                    f"--force-device-scale-factor={RENDER_PPI / 96}", f"--virtual-time-budget={budget}",
                    "--enable-logging=stderr", "--v=0", f"--screenshot={gl}", f"{url}?layer=gl"])
        errs = [l for l in r.stderr.splitlines() if "CONSOLE" in l and ("Error" in l or "error" in l)]
        if errs or not gl.exists():
            return [f"!! {fid}: light layer not rendered: " + " | ".join(errs[:5] or [r.stderr[-400:]])]
        st = ImageStat.Stat(Image.open(gl).convert("L").reduce(8))
        mean, sd = st.mean[0], st.stddev[0]
        if 8 <= mean <= 120 and sd >= 8:
            break
        out.append(f"{fid}: light layer empty on attempt {attempt} (mean {mean:.0f}, spread {sd:.0f})")
    else:
        return out + [f"!! {fid}: the light layer is empty"]
    im = Image.open(gl)
    out.append(f"{fid}: light layer {im.size[0]} × {im.size[1]} px = {im.size[0] / (w_mm / 25.4):.0f} ppi, "
               f"{gl.stat().st_size / 2**20:.1f} MiB")
    for budget in (20000, 60000):                   # the HUD's report, read from the DOM (again if it was not yet drawn)
        r = chrome([f"--virtual-time-budget={budget}", "--dump-dom", f"{url}?layer=print"])
        m = re.search(r'data-fit="([^"]*)"', r.stdout)
        if m:
            break
    if not m:
        return out + [f"!! {fid}: the HUD did not draw: {r.stderr[-300:]}"]
    fit = json.loads(unescape(m.group(1)))
    mp = re.search(r'data-minpt="([^"]*)"', r.stdout)
    ml = re.search(r'data-lines="([^"]*)"', r.stdout)
    mk = re.search(r'data-links="([^"]*)"', r.stdout)
    mo = re.search(r'data-overlap="([^"]*)"', r.stdout)
    lines = json.loads(unescape(ml.group(1))) if ml else []
    links = json.loads(unescape(mk.group(1))) if mk else []
    overlap = json.loads(unescape(mo.group(1))) if mo else ["no collision report (data-overlap missing)"]
    (WEB / f"hud-{fid}.json").write_text(json.dumps({"lines": lines, "links": links, "fit": fit, "overlap": overlap,
                                                    "minpt": float(mp.group(1)) if mp else 0}, ensure_ascii=False,
                                                   indent=0), encoding="utf-8")
    out.append(f"{fid}: HUD {len(lines)} lines, {len(links)} links, smallest type {float(mp.group(1)) if mp else 0:.2f} pt, "
               f"{len(overlap)} colliding lines")
    for f in fit:
        out.append(f"!! {fid}: text does not fit: {f}")
    for f in overlap:
        out.append(f"!! {fid}: lines collide: {f}")
    tmp = WEB / f"{fid}.tmp.pdf"
    tmp.unlink(missing_ok=True)
    # Three prints at once can print before the light layer's PNG or the faces have loaded (2026-10-28: a page of
    # 12 × 12 pt, and a page without text): a print must carry the full image and text, or it is printed again.
    ok = False
    for budget in (20000, 60000, 120000):
        tmp.unlink(missing_ok=True)
        r = chrome(["--no-pdf-header-footer", f"--virtual-time-budget={budget}", f"--print-to-pdf={tmp}", f"{url}?layer=print"])
        if not tmp.exists():
            continue
        with pymupdf.open(tmp) as chk:
            imgs = chk[0].get_image_info()
            ok = (imgs and pymupdf.Rect(imgs[0]["bbox"]).width > 300 and len(chk[0].get_text().strip()) > 20)
        if ok:
            break
        out.append(f"{fid}: print incomplete at a budget of {budget} ms; printed again")
    if not tmp.exists() or not ok:
        return out + [f"!! {fid}: PDF not printed completely: {r.stderr[-300:]}"]
    with pymupdf.open(tmp) as src:
        ib = pymupdf.Rect(src[0].get_image_info()[0]["bbox"])
    with pikepdf.open(tmp) as pdf:                    # the page = the light layer's box (Series 00, figures_web.py)
        mb = [float(v) for v in pdf.pages[0].obj.MediaBox]
        left, top = mb[0], mb[3]
        pdf.pages[0].obj.MediaBox = pikepdf.Array([round(v, 4) for v in [left + ib.x0, top - ib.y1, left + ib.x1, top - ib.y0]])
        for k in ("/CropBox", "/TrimBox", "/BleedBox", "/ArtBox"):
            if k in pdf.pages[0].obj:
                del pdf.pages[0].obj[k]
        pdf.save(FIGDIR / f"fig-{fid}.pdf", compress_streams=True)
    tmp.unlink()
    write_tex(fid, links)
    return out


def write_tex(fid, links):
    """figures/fig-<id>.tex: the figure at its natural size, and a link over every cell that names a problem or thesis"""
    import pymupdf
    with pymupdf.open(FIGDIR / f"fig-{fid}.pdf") as d:
        wpt, hpt = d[0].rect.width, d[0].rect.height
    W, H = MEASURE, FIGS[fid][1]
    sx, sy = wpt / 72 * 25.4 / W, hpt / 72 * 25.4 / H
    L = [f"% written by tools/figures.py: Figure \"{fid}\" and its links (data-links of the HUD)",
         "\\begingroup\\setlength{\\unitlength}{1mm}%",
         f"\\begin{{picture}}({wpt / 72 * 25.4:.3f},{hpt / 72 * 25.4:.3f})%",
         f"\\put(0,0){{\\includegraphics{{fig-{fid}.pdf}}}}%"]
    for k in links:
        x0, y0, w, h = k["x"] * sx, (H - k["y"] - k["h"]) * sy, k["w"] * sx, k["h"] * sy
        L.append(f"\\put({x0:.3f},{y0:.3f}){{\\hyperref[{k['to']}]{{\\makebox({w:.3f},{h:.3f}){{}}}}}}%")
    L += ["\\end{picture}\\endgroup", ""]
    (FIGDIR / f"fig-{fid}.tex").write_text("\n".join(L), encoding="utf-8", newline="\n")


# ------------------------------------------------------------------------------------------------ checks --------------
def simulate(hexcol, kind):
    """Machado, Oliveira & Fernandes (2009), severity 1.0, on linear RGB; returns CIE L*a*b*"""
    M = {"protan": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
         "deutan": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
         "tritan": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
         "none": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]}[kind]
    lin = [((c / 255 + .055) / 1.055) ** 2.4 if c / 255 > .04045 else c / 255 / 12.92
           for c in (int(hexcol[i:i + 2], 16) for i in (1, 3, 5))]
    r, g, b = (min(1, max(0, sum(M[i][j] * lin[j] for j in range(3)))) for i in range(3))
    X, Y, Z = (.4124 * r + .3576 * g + .1805 * b) / .95047, .2126 * r + .7152 * g + .0722 * b, (.0193 * r + .1192 * g + .9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > .008856 else 7.787 * t + 16 / 116
    return 116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z))


ACCENTS = {"cyan": "#58ded4", "blue": "#82a4ff", "violet": "#cf8df6", "gold": "#dfc174"}
# the categories each figure encodes by accent colour, and the second, non-colour mark of each
# (the colours of the seven cells are those of the series covers and name no category: each cell prints its series)
CATEGORIES = {"works": ([], "none: the series number is printed in each cell"),
              "theses": (["cyan", "blue", "gold"], "group heading over each band"),
              "relations": (["cyan", "blue", "gold"], "thesis number in each node"),
              "rose": (["blue", "cyan", "gold"], "kinds grouped in order within each cell; level by 1–3 dots"),
              "matrix": (["blue", "cyan", "gold"], "problem number in each chip, whose card gives the kind"),
              "chain": (["cyan", "gold"], "headings THESIS 6 and THESIS 7"),
              "triangle": (["cyan", "gold"], "labels in each panel"),
              "selection": (["cyan", "gold"], "headings"), "card": (["cyan", "gold"], "headings"),
              "credit": (["cyan", "gold"], "headings"),
              "programme": ([], "none: the series number is printed in each cell"),
              "method": (["cyan", "gold"], "headings"), "series": ([], "none: the series number is printed in each row")}


def check_one(fid, num):
    import pymupdf
    pdf = FIGDIR / f"fig-{fid}.pdf"
    out, problems = [], []
    if not pdf.exists():
        return [f"!! {fid}: {pdf.name} missing"]
    d = pymupdf.open(pdf)
    p = d[0]
    w_mm, h_mm = p.rect.width / 72 * 25.4, p.rect.height / 72 * 25.4
    if d.page_count != 1 or abs(w_mm - MEASURE) > .6 or abs(h_mm - FIGS[fid][1]) > .6:
        problems.append(f"page {w_mm:.1f} × {h_mm:.1f} mm, expected {MEASURE} × {FIGS[fid][1]}")
    infos = p.get_image_info(xrefs=True)
    if len(infos) != 1:
        problems.append(f"{len(infos)} images on the page (the light layer only is expected)")
    for info in infos:
        bbox = pymupdf.Rect(info["bbox"])
        ppi = info["width"] / (bbox.width / 72) if bbox.width else 0
        filt = d.xref_get_key(info["xref"], "Filter")[1] if info["xref"] else "?"
        out.append(f"{fid}: light layer {info['width']} × {info['height']} px, {ppi:.0f} ppi, {filt}")
        if ppi < PPI - 1:
            problems.append(f"light layer at {ppi:.0f} ppi")
        if "DCT" in filt or "JPX" in filt:
            problems.append(f"lossy image filter {filt}")
    fonts = p.get_fonts()
    if "Type3" in {f[2] for f in fonts}:
        problems.append("Type 3 fonts")
    stray = sorted({f[3] for f in fonts if not re.match(r"^[A-Z]{6}\+(SegoeUI|TGP)", f[3])})
    if stray:
        problems.append(f"faces other than Segoe UI and TGP: {stray}")
    flat = " ".join(p.get_text().split())
    hud = json.loads(read(WEB / f"hud-{fid}.json")) if (WEB / f"hud-{fid}.json").exists() else {"lines": [], "fit": [1]}
    # compared without spaces: the extraction splits tracked capitals ("A WORKED E XAMPLE")
    bare = "".join(flat.split())
    missing = [l for l in hud["lines"] if "".join(l.split()) not in bare]
    if missing:
        problems.append(f"{len(missing)} drawn lines not searchable, e.g. {missing[:3]}")
    if f"FIGURE {num}" not in flat:
        problems.append(f"'FIGURE {num}' is not printed")
    if hud.get("overlap"):
        problems.append(f"lines that collide: {hud['overlap'][:3]}")
    if hud.get("fit"):
        problems.append(f"lines that do not fit: {hud['fit'][:3]}")
    if hud.get("minpt", 0) < 6.5:
        problems.append(f"type below 6.5 pt ({hud.get('minpt')})")
    cats, second = CATEGORIES[fid]
    worst = 1e9 if cats else float("nan")
    for kind in ("none", "protan", "deutan", "tritan"):
        labs = {c: simulate(ACCENTS[c], kind) for c in cats}
        for i, a in enumerate(cats):
            for b in cats[i + 1:]:
                worst = min(worst, sum((x - y) ** 2 for x, y in zip(labs[a], labs[b])) ** .5)
    out.append(f"{fid}: {w_mm:.1f} × {h_mm:.1f} mm, {pdf.stat().st_size / 2**20:.1f} MiB, faces "
               f"{sorted({f[3].split('+')[-1] for f in fonts})}; {len(hud['lines'])} lines searchable; categories "
               f"{cats}: least ΔE*ab under simulated colour-vision deficiency {worst:.0f}; second mark: {second}")
    if cats and worst < 8:
        problems.append(f"category colours too close under simulated colour-vision deficiency (ΔE {worst:.0f})")
    return out + [f"!! {fid}: {x}" for x in problems]


def check_links(nums):
    """every link target is a label of the paper (the .aux of the last build)"""
    bad = []
    for fid in nums:
        hud = WEB / f"hud-{fid}.json"
        if not hud.exists():
            continue
        paper = FIGS[fid][0]
        aux = OUT / "work" / paper / f"{paper}.aux"
        labels = set(re.findall(r"\\newlabel\{([^}]+)\}", read(aux))) if aux.exists() else set()
        for k in json.loads(read(hud))["links"]:
            if labels and k["to"] not in labels:
                bad.append(f"{fid} → {k['to']}")
    return bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    nums = numbers()
    fids = args or list(nums)
    unknown = [f for f in fids if f not in nums]
    if unknown:
        sys.exit(f"not placed in a paper: {unknown}")
    n = sync_design()
    S = Sources()
    write_data(list(nums), nums, S)
    bad_src = [f"“{p}” not in {w}" for p, w, ok in S.checked if not ok]
    print(f"design: {n} files from Series 00 (hash-checked); data: {len(nums)} figures; "
          f"phrases checked against their sources: {len(S.checked)}, not found: {len(bad_src)}")
    for b in bad_src:
        print("!!", b)
    if "--data" in sys.argv:
        return
    report = [f"!! source: {b}" for b in bad_src]
    if "--check" not in sys.argv:
        if not CHROME or not Path(CHROME).exists():
            sys.exit("Chrome not found: set \"chrome\" in local.json")
        httpd, port = serve()
        try:
            with ThreadPoolExecutor(max_workers=3) as ex:
                for lines in ex.map(lambda f: render_one(f, port), fids):
                    report += lines
        finally:
            httpd.shutdown()
    for fid in nums:
        report += check_one(fid, nums[fid])
    report += [f"!! link target not in the paper: {b}" for b in check_links(nums)]
    fails = [l for l in report if l.startswith("!!")]
    head = [f"# Figure gate: {len(nums)} figures, {'ALL PASS' if not fails else f'{len(fails)} FAIL'}", "",
            f"Phrases checked against their sources: {len(S.checked)}; not found: {len(bad_src)}.", ""]
    (OUT / "FIGURE-GATE.md").write_text("\n".join(head + [f"- {l}" for l in report]) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(head[0])
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
