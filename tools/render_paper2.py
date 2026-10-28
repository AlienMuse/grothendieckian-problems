"""Generate the problem cards, appendices and reference list of paper II from src/problems/*.yaml (single source).

  python tools/render_paper2.py      → src/paper-II/20-part1.md, 30-part2.md, 80-appendices.md, 90-references.md

Hand-written: 01-introduction.md. Citations [@key] are resolved by tools/refs.py; every printed reference must have
passed tools/verify_refs.py.
"""
import sys
from collections import Counter
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "tools"))
import refs  # noqa: E402

SRC = HERE / "src"
OUT = SRC / "paper-II"
WORKS = {"S01": "*GAI-MUA: The Grothendieckian Machine* [@S01]", "S02": "*GM-Omega-Infinity: Topos-Native Intelligence* [@S02]",
         "S03": "*Arithmetic Spectral Descent* [@S03]", "S04": "*Fractured Adelic Geometry* [@S04]",
         "S05": "*The Archimedean Prism* [@S05]", "S06": "*Strained Prismatic Geometry* [@S06]",
         "S07": "*The Arithmetic Topos* [@S07]"}
SUBJECT = {"S03": "the Riemann Hypothesis", "S04": "the conjecture of Birch and Swinnerton-Dyer",
           "S05": "the Hodge conjecture", "S06": "the $abc$ conjecture", "S07": "the Langlands programme"}
KIND = {"math": "Mathematical problem", "machine": "Machine problem", "formal": "Formalization problem"}
LEVEL = {"entry": "entry level", "research": "research level", "programme": "programme level"}
THESES = {t["num"]: t for t in yaml.safe_load((SRC / "theses.yaml").read_text(encoding="utf-8"))}
REPO = "https://github.com/AlienMuse/grothendieckian-problems"


def load():
    cards = []
    for f in sorted((SRC / "problems").glob("*.yaml")):
        cards += yaml.safe_load(f.read_text(encoding="utf-8"))
    cards.sort(key=lambda c: c["num"])
    assert [c["num"] for c in cards] == list(range(1, 58)), "problem numbers must be 1–57"
    return cards


def para(s):
    return " ".join(str(s).split())


def card(c):
    t = THESES[c["thesis"]]
    # the heading carries the kind and the level (second layout, 2026-10-28); the first field names the thesis
    tags = f"{KIND[c['kind']].split()[0].lower()} · {LEVEL[c['level']]}"
    L = [f"::: {{.problem #problem-{c['num']} title=\"{c['title']}\" tags=\"{tags}\"}}",
         "::: {.field label=\"Thesis\"}",
         f"Thesis {c['thesis']} ({t['title']}).", ":::", "",
         "::: {.field label=\"Source\"}", f"{WORKS[c['work']]}, {c['source']}.", ":::", "",
         "::: {.field label=\"Status in the source\"}", f"{para(c['status'])}.", ":::", "",
         "::: {.field label=\"Statement\"}", para(c["statement"]), ":::", "",
         "::: {.field label=\"What the source establishes\"}", para(c["established"]), ":::", "",
         "::: {.field label=\"Proposed by\"}", para(c["proposer"]), ":::", "",
         "::: {.field label=\"Background\"}", para(c["background"]), ":::", "",
         "::: {.field label=\"Solved when\"}", para(c["solved"]), ":::", "",
         "::: {.field label=\"Literature check (28 October 2026)\"}", para(c["litcheck"]), ":::", "",
         "::: {.field label=\"Discussion\"}", f"[Issue {c['num']}]({REPO}/issues/{c['num']}) of the repository.",
         ":::", ":::", ""]
    return "\n".join(L)


def main():
    cards = load()
    p1 = [c for c in cards if c["num"] <= 35]
    p2 = [c for c in cards if c["num"] >= 36]
    part1 = ["# Part I. The Machine {.part #part-1}", "",
             "The problems of this part come from the two works on the architecture of a reasoning system for mathematics: "
             "Problems 1–17 from *GAI-MUA: The Grothendieckian Machine* [@S01] and Problems 18–35 from *GM-Omega-Infinity: "
             "Topos-Native Intelligence* [@S02]. Page numbers in [@S01] run through its six volumes.", ""]
    part1 += [card(c) for c in p1]
    part2 = ["# Part II. The Five Research Subjects {.part #part-2}", "",
             "Each of the five works of this part takes a named conjecture or programme as its research subject and records "
             "what its method establishes about it. The problems below are drawn from those records. None of them is the "
             "named conjecture, and a solution of any of them would not by itself prove one.", ""]
    for w in ("S03", "S04", "S05", "S06", "S07"):
        cs = [c for c in p2 if c["work"] == w]
        part2 += [f"## {WORKS[w].split(' [')[0]} (research subject: {SUBJECT[w]}) {{.unnumbered}}", ""]
        part2 += [card(c) for c in cs]
    # appendices
    ap = ["```{=latex}", "\\clearpage", "```", "",            # the appendices on a new page, Figure 5 with them
          "# Appendices {.unnumbered}", "", "## A. The problems by thesis and by work {.unnumbered}", "",
          "\\figref{matrix} places each problem by its thesis and its work. The first table below lists the problems of "
          "each thesis, the second counts the problems of each work by kind.", "",
          "::: {.figure #fig:matrix file=\"fig-matrix\" place=\"here\"}",
          "The problems by thesis and by work. Each small cell is a problem, tinted by kind and linked to its card; the "
          "totals are by row and by column.", ":::", "",
          "| Thesis | Problems |", "|---|---|"]
    for n in range(1, 13):
        nums = ", ".join(str(c["num"]) for c in cards if c["thesis"] == n)
        ap.append(f"| {n}. {THESES[n]['title']} | {nums} |")
    ap += ["", "| Work | Problems | Mathematical | Machine | Formalization |", "|---|---|---|---|---|"]
    for w in WORKS:
        cs = [c for c in cards if c["work"] == w]
        k = Counter(c["kind"] for c in cs)
        ap.append(f"| {w} | {cs[0]['num']}–{cs[-1]['num']} | {k['math']} | {k['machine']} | {k['formal']} |")
    k = Counter(c["kind"] for c in cards)
    ap.append(f"| All | 1–57 | {k['math']} | {k['machine']} | {k['formal']} |")
    ap += ["", "## B. Changes made by the literature check {.unnumbered}", "",
           "The selection approved before the literature check was changed in seven places. The replaced problems are "
           "listed so that the reasons can be checked.", "",
           "| Problem | Approved candidate | Change and reason |", "|---|---|---|"]
    for row in yaml.safe_load((SRC / "changes.yaml").read_text(encoding="utf-8")):
        ap.append(f"| {row['num']} | {row['was']} | {row['why']} |")
    ap += ["", "## C. The machine-readable file {.unnumbered}", "",
           "`problems.json` in the repository contains, for each problem, the fields of its card and the identifiers of "
           "its source (work, DOI, pages, status), its thesis, its kind and level, the date of its literature check and "
           "the path of its Lean statement where one exists. The file is generated from the same source as this paper, and "
           "the two are checked to agree field by field.", ""]
    # declarations
    ap += ["# Declarations {.unnumbered}", "", (SRC / "declarations.md").read_text(encoding="utf-8").strip(), ""]
    body = {"20-part1.md": "\n".join(part1), "30-part2.md": "\n".join(part2), "80-appendices.md": "\n".join(ap)}
    texts = [(OUT / "01-introduction.md").read_text(encoding="utf-8")] + list(body.values())
    keys = refs.used(texts)
    body["90-references.md"] = "# References {.unnumbered}\n\n" + refs.reference_list(keys)
    for name, text in body.items():
        (OUT / name).write_text(refs.cite_text(text) + "\n", encoding="utf-8", newline="\n")
    words = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
             11: "Eleven", 12: "Twelve", 13: "thirteen", 19: "nineteen", 25: "twenty-five", 35: "Thirty-five"}
    lv, kd = Counter(c["level"] for c in cards), Counter(c["kind"] for c in cards)
    # the extracted items (candidates/pool.json, the list published as data/candidates.json): total and by work
    import json
    pool = Counter(p["work"] for p in json.loads((HERE / "candidates" / "pool.json").read_text(encoding="utf-8")))
    fill = {"n_entry": words[lv["entry"]], "n_research": words[lv["research"]], "n_programme": words[lv["programme"]],
            "n_math": words[kd["math"]].lower(), "n_machine": words[kd["machine"]].lower(),
            "n_formal": words[kd["formal"]].lower(), "n_pool": f"{sum(pool.values()):,}",
            "n_pool_works": ", ".join(f"{pool[w]} in [@{w}]" for w in WORKS)}
    intro = (OUT / "01-introduction.md").read_text(encoding="utf-8")
    for k, v in fill.items():
        intro = intro.replace("{" + k + "}", v)
    assert "{n_" not in intro, "unfilled count in the introduction"
    intro = refs.cite_text(intro)
    (OUT / "01-introduction.cited.md").write_text(intro, encoding="utf-8", newline="\n")
    (OUT / "ORDER.txt").write_text("# generated by tools/render_paper2.py\n01-introduction.cited.md\n20-part1.md\n"
                                   "30-part2.md\n80-appendices.md\n90-references.md\n", encoding="utf-8", newline="\n")
    print(f"paper II: {len(cards)} cards, {len(keys)} references; kinds {dict(kd)}; levels {dict(lv)}")


if __name__ == "__main__":
    main()
