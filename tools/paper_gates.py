"""The gates of the two papers on their final PDFs and sources (runbook §6). Exit 1 if any gate fails.

  python tools/paper_gates.py out/overview.pdf out/paper-I.pdf out/paper-II.pdf      → out/PAPER-GATES.md

claim     the Series 00 claim gate (master/tools/claim_gate.py: classify), with this project's reviewed exceptions in
          src/claims-ALLOW.json (pattern + reason)
style     self-praise and stock phrases (the Series 00 style-gate lists) and process traces (draft names, file paths,
          tool and model names) in the printed text
crank     the checkable signs of src/CRANK-CHECK.md: no claim of priority ("first", "for the first time", "novel"),
          no comparison of the author with named mathematicians, abbreviations defined at first use, named conjectures
          not stated as problems, a share of references outside the seven works of at least one half
count     57 problems numbered 1–57; Part I = 35 from S01–S02; Part II = 22, each of S03–S07 with 4 or 5
criterion every card has a non-empty "Solved when" that names an observable outcome (a proof, a refutation, a
          construction, a published record, a machine check) and no card's criterion is a paraphrase of its statement
attribution every card has "Proposed by"; cards whose source names an earlier proposer cite it
pdf       fonts all embedded, no Type 3; only the Pagella family, Pagella Math and Cursor, and in the figures Segoe UI and
          the TGP faces; no overfull lines in the log
leak      no local path, no token, no private marker in the PDFs or the sources
pages     the overview has at most 10 pages, references and declarations included (author, 2026-10-28)
numbers   the totals of the series printed in any of the three papers are those of programme.yaml (volumes, pages,
          chapters, formulas, statements, algorithms, figures and plates)
"""
import json
import re
import sys
from pathlib import Path

import pymupdf
import yaml

HERE = Path(__file__).resolve().parents[1]
MASTER = HERE.parent / "master"
sys.path.insert(0, str(MASTER / "tools"))
import claim_gate  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SELF = (r"\b(?:revolutionar(?:y|ies)|groundbreaking|ground-breaking|top-level|top-tier|world-class|state-of-the-art|"
        r"cutting-edge|highly non-?trivial|unprecedented|paradigm[- ]shift(?:ing)?|breakthroughs?|landmark|seminal|"
        r"monumental|masterpiece|magnum opus|definitive|first[- ]ever|the most (?:ambitious|important|complete|"
        r"comprehensive|rigorous)|remarkabl[ey]|profound(?:ly)?|deep(?:est)? insight|elegant(?:ly)?|powerful|"
        r"novel|for the first time|pioneer(?:ing|s|ed)?)\b")
STOCK = (r"\b(?:it is worth (?:noting|stressing|emphasising)|crucially|importantly|notably|it should be (?:noted|stressed)|"
         r"needless to say|it bears repeating|delve|tapestry|in today's|game[- ]chang(?:er|ing))\b")
TRACE = (r"\b(?:review copy|layout sample|placeholder|TODO|FIXME|lorem)\b|\b[\w/.-]+\.(?:py|yaml|ps1|txt)\b|"
         r"\bClaude\b|\bChatGPT\b|\bGPT-?\d|\bOpus\b")
NAMES = r"\b(?:Hilbert|Einstein|Luther|Newton|Galois|Riemann|Gauss|Euler|Grothendieck|Weil|Deligne|Serre|Langlands)\b"
LEAK = r"(?:[A-Z]:\\|/workspace/|Creative Project|ghp_[A-Za-z0-9]{20,}|zenodo[_-]?token|release-kit/private)"
# the text faces, and in the figures Segoe UI and the TGP faces of the Series 00 figures (tools/figures.py)
FONTS = ("TeXGyrePagella", "TeXGyrePagellaMath", "TeXGyreCursor", "SegoeUI", "TGP")


def pdf_text(p):
    d = pymupdf.open(p)
    return [pg.get_text() for pg in d], d


REVIEW = "--review" in sys.argv      # review copies carry "review copy" in the date line; the final build may not


def main():
    pdfs = [Path(a) for a in sys.argv[1:] if not a.startswith("--")]
    report, fails = [], 0

    def gate(name, ok, detail):
        nonlocal fails
        fails += 0 if ok else 1
        report.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {detail} |")

    allow = json.loads((HERE / "src" / "claims-ALLOW.json").read_text(encoding="utf-8"))
    texts = {}
    for p in pdfs:
        pages, d = pdf_text(p)
        texts[p] = (pages, d)
        hits = []
        for i, t in enumerate(pages):
            t = re.sub(r"\s+", " ", re.sub(r"(\w)-\n(\w)", r"\1\2", t))
            for s in claim_gate.sentences(t):
                found, _cleared = claim_gate.classify(s)
                if found and not any(re.search(a["pattern"], s) for a in allow):
                    hits.append(f"p. {i + 1} [{','.join(found)}]: {' '.join(s.split())[:120]}")
        gate(f"claim · {p.name}", not hits, "; ".join(hits[:3]) or "0 hits")
        # style and traces: printed text without the reference list (titles of cited works are quoted as printed)
        body = "\n".join(pages)
        body = body[:body.rfind("References")] if "References" in body else body
        own = re.sub(r"“[^”]*(?:“[^”]*”[^”]*)*”", " ", body.replace("\n", " "))   # our words, not quotations
        self_hits = sorted({m.group(0) for m in re.finditer(SELF, own, re.I)})
        stock = sorted({m.group(0) for m in re.finditer(STOCK, own, re.I)})
        trace = sorted({m.group(0) for m in re.finditer(TRACE, own)} - ({"review copy"} if REVIEW else set()))
        gate(f"style · {p.name}", not (self_hits or stock or trace),
             f"self-praise {self_hits or 0}; stock {stock or 0}; traces {trace or 0}")
        # fonts
        fonts = {f[3].split("+")[-1]: f[2] for pg in d for f in pg.get_fonts()}
        type3 = [n for n, t in fonts.items() if t == "Type3"]
        other = [n for n in fonts if not n.startswith(FONTS)]
        emb = all(f[0] for pg in d for f in pg.get_fonts() if pg.get_fonts())
        gate(f"pdf fonts · {p.name}", not type3 and not other, f"{len(fonts)} fonts; Type 3 {type3 or 0}; others {other or 0}")
        log = HERE / "out" / "work" / p.stem / (p.stem + ".log")
        over = len(re.findall(r"Overfull \\hbox", log.read_text(encoding="utf-8", errors="replace"))) if log.exists() else -1
        gate(f"pdf layout · {p.name}", over == 0, f"overfull lines {over} ({log.name})")
        leak = sorted({m.group(0) for m in re.finditer(LEAK, body)})
        gate(f"leak · {p.name}", not leak, f"{leak or 0}")
        # crank: comparisons with named mathematicians in sentences about the author or the works
        comp = [s for t in pages for s in claim_gate.sentences(t)
                if re.search(NAMES, s) and re.search(r"\b(?:like|as did|in the tradition of|successor|equal|rival|"
                                                     r"surpass|comparable to)\b", s, re.I)
                and re.search(r"\b(?:we|our|the author|this paper|the seven works|the Programme)\b", s)]
        gate(f"crank · comparison · {p.name}", not comp, "; ".join(" ".join(c.split())[:90] for c in comp[:2]) or "0")
    # sources: references outside the seven works
    sys.path.insert(0, str(HERE / "tools"))
    import refs
    for paper, files in (("paper-I", ["01-introduction.cited.md", "40-theses.md", "45-together.cited.md",
                                       "50-limits.cited.md"]),
                         ("paper-II", ["01-introduction.cited.md", "20-part1.md", "30-part2.md"])):
        srcs = [(HERE / "src" / paper.replace("paper-", "paper-") / f) for f in files]
        raw = [(HERE / "src" / paper / f.replace(".cited", "")).read_text(encoding="utf-8") for f in files
               if (HERE / "src" / paper / f.replace(".cited", "")).exists()]
    p0 = [(HERE / "src" / "overview" / "01-overview.md").read_text(encoding="utf-8")]
    p1 = [(HERE / "src" / "paper-I" / f).read_text(encoding="utf-8") for f in ("01-introduction.md", "45-together.md", "50-limits.md")]
    p1 += [(HERE / "src" / "theses.yaml").read_text(encoding="utf-8"),
           (HERE / "src" / "thesis-instances.yaml").read_text(encoding="utf-8")]
    cards = []
    for f in sorted((HERE / "src" / "problems").glob("*.yaml")):
        cards += yaml.safe_load(f.read_text(encoding="utf-8"))
    p2 = [(HERE / "src" / "paper-II" / "01-introduction.md").read_text(encoding="utf-8")] +         [f.read_text(encoding="utf-8") for f in sorted((HERE / "src" / "problems").glob("*.yaml"))]
    for name, texts_ in (("overview", p0), ("paper I", p1), ("paper II", p2)):
        keys = refs.used([re.sub(r"(?m)^\s*#.*$", "", t) for t in texts_])   # YAML comments are not text
        outside = [k for k in keys if not re.fullmatch(r"S0[0-7]|Liu26[abc]", k)]   # own: the works and the three papers
        gate(f"crank · references · {name}", len(outside) >= len(keys) / 2,
             f"{len(outside)} of {len(keys)} references are outside the works of the Programme and the three papers")
    # count
    cards.sort(key=lambda c: c["num"])
    p1c = [c for c in cards if c["num"] <= 35]
    p2c = [c for c in cards if c["num"] >= 36]
    per = {w: sum(1 for c in p2c if c["work"] == w) for w in ("S03", "S04", "S05", "S06", "S07")}
    ok = ([c["num"] for c in cards] == list(range(1, 58)) and all(c["work"] in ("S01", "S02") for c in p1c)
          and len(p1c) == 35 and len(p2c) == 22 and all(v in (4, 5) for v in per.values()))
    gate("count", ok, f"57 = 35 (S01 {sum(1 for c in p1c if c['work'] == 'S01')}, S02 {sum(1 for c in p1c if c['work'] == 'S02')}) + 22 {per}")
    # criterion and attribution
    verbs = r"\b(?:proof|proves?|proved|refut|counterexample|construct|published|machine-checked|kernel|replay|theorem|" \
            r"implementation|study|comparison|computation|record|release|definition|library|algorithm|model)\w*"
    weak = [c["num"] for c in cards if not re.search(verbs, c["solved"], re.I) or len(c["solved"].split()) < 12]
    gate("criterion", not weak, f"cards with a weak criterion: {weak or 0}")
    # locators: every page printed in a card's Source is among its declared pages, and every folio cited anywhere
    # ([@S0x, … p. N] in cards, theses, instances, paper text) exists in that work's sealed PDF
    corpus = HERE.parent / "master" / "out" / "work" / "corpus"
    labels = {w: set(json.loads((corpus / f"{w}.pages.json").read_text(encoding="utf-8"))["labels"])
              for w in ("S01", "S02", "S03", "S04", "S05", "S06", "S07")}
    loc_bad = []
    for c in cards:
        printed = set(re.findall(r"pp?\.\s*([0-9ivxlc]+)(?:–([0-9ivxlc]+))?", c["source"]))
        for a, b in printed:
            for f in (a, b):
                if f and f not in c["pages"]:
                    loc_bad.append(f"{c['num']}: p. {f} not in pages")
                if f and f not in labels[c["work"]]:
                    loc_bad.append(f"{c['num']}: p. {f} not a page of {c['work']}")
    alltext = "\n".join([(HERE / "src" / "theses.yaml").read_text(encoding="utf-8"),
                         (HERE / "src" / "thesis-instances.yaml").read_text(encoding="utf-8")] +
                        [f.read_text(encoding="utf-8") for f in sorted((HERE / "src" / "problems").glob("*.yaml"))] +
                        [f.read_text(encoding="utf-8") for f in sorted((HERE / "src").glob("*/[0-9][0-9]-*.md"))
                         if ".cited" not in f.name and f.parent.name in ("overview", "paper-I", "paper-II")])
    for m in re.finditer(r"\[@(S0[1-7])([^\]]*)\]", alltext):
        for a, b in re.findall(r"pp?\.\s*([0-9ivxlc]+)(?:–([0-9ivxlc]+))?", m.group(2)):
            for f in (a, b):
                if f and f not in labels[m.group(1)]:
                    loc_bad.append(f"[@{m.group(1)}{m.group(2)}]: p. {f} not a page")
    gate("locators", not loc_bad, "; ".join(sorted(set(loc_bad))[:6]) or "every printed page exists and is declared")
    ths = yaml.safe_load((HERE / "src" / "theses.yaml").read_text(encoding="utf-8"))
    bad_lists = [t["num"] for t in ths if sorted(t["problems"]) != sorted(c["num"] for c in cards if c["thesis"] == t["num"])]
    gate("theses ↔ cards", not bad_lists, f"theses whose problem list differs from the cards: {bad_lists or 0}")
    noprop = [c["num"] for c in cards if not str(c.get("proposer", "")).strip()]
    gate("attribution", not noprop, f"cards without a proposer: {noprop or 0}")
    named = r"(?i)\b(?:prove|establish)\b[^.]{0,40}\b(?:the Riemann Hypothesis|Birch and Swinnerton-Dyer|the Hodge conjecture|the abc conjecture|the Langlands correspondence)\b"
    titled = [c["num"] for c in cards if re.search(named, c["statement"])]
    gate("crank · named conjecture as problem", not titled, f"{titled or 0}")
    # pages: the overview in at most ten pages
    for p, (pages, d) in texts.items():
        if p.stem == "overview":
            gate("pages · overview", d.page_count <= 10, f"{d.page_count} pages (limit 10)")
    # numbers: the series' totals, wherever a paper prints them
    prog = yaml.safe_load((HERE.parent / "programme.yaml").read_text(encoding="utf-8"))
    tot, st = prog["facts"]["totals"], prog["stats"]["totals"]
    want = {"volumes": str(tot["volumes"]), "pages": f"{tot['pages']:,}", "chapters": st["chapters"],
            "formulas": st["formulas"].rstrip("+"), "statements": st["statements"].rstrip("+"),
            "algorithms": st["algorithms"], "figures": st["figures_and_plates"]}
    pats = {"volumes": r"(\d+) volumes,? (?:and )?[\d,]+ pages", "pages": r"\d+ volumes,? (?:and )?([\d,]+) pages",
            "chapters": r"pages,? and ([\d,]+) chapters|pages and ([\d,]+) chapters", "formulas": r"more than ([\d,]+) formulas",
            "statements": r"more than ([\d,]+) numbered statements", "algorithms": r"([\d,]+) numbered algorithms",
            "figures": r"([\d,]+) numbered figures and plates"}
    # one work's volumes and pages (the figures list them work by work) are that work's, not the totals
    per_work = {(str(w["volumes"]), f"{w['pages']:,}") for w in prog["facts"]["works"]}
    bad, seen = [], 0
    for p, (pages, d) in texts.items():
        flat = " ".join(" ".join(pages).split())
        for k, pat in pats.items():
            for m in re.finditer(pat, flat):
                pair = re.match(r"(\d+) volumes,? (?:and )?([\d,]+) pages", m.group(0))
                if pair and pair.groups() in per_work:
                    continue
                v = next(g for g in m.groups() if g)
                seen += 1
                if v != want[k]:
                    bad.append(f"{p.name}: {k} {v} (programme.yaml {want[k]})")
    gate("numbers · three papers", not bad and seen > 0, "; ".join(bad[:4]) or f"{seen} printed totals, all as in programme.yaml")
    out = ["# Paper gates", "", "| gate | result | detail |", "|---|---|---|"] + report
    out.append(f"\n**{'ALL PASS' if not fails else f'{fails} FAIL'}**")
    (HERE / "out" / "PAPER-GATES.md").write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(out))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
