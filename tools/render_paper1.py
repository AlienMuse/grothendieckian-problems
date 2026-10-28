"""Generate the theses section, declarations and references of paper I from src/theses.yaml (single source).

  python tools/render_paper1.py      → src/paper-I/*.cited.md, 40-theses.md, 80-declarations.md, 90-references.md, ORDER.txt
"""
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "tools"))
import refs  # noqa: E402

SRC = HERE / "src"
OUT = SRC / "paper-I"
HAND = ["01-introduction.md", "45-together.md", "50-limits.md"]
INST = yaml.safe_load((SRC / "thesis-instances.yaml").read_text(encoding="utf-8"))


def para(s):
    return " ".join(str(s).split())


def problems_of(num):
    """The problems of a thesis come from the cards (single source), not from theses.yaml."""
    cards = []
    for f in sorted((SRC / "problems").glob("*.yaml")):
        cards += yaml.safe_load(f.read_text(encoding="utf-8"))
    return sorted(c["num"] for c in cards if c["thesis"] == num)


def pages_text(pages):
    """'p. 8250', 'pp. 8250–8251' for consecutive pages, else 'pp. 21, 23'"""
    if len(pages) == 1:
        return f"p. {pages[0]}"
    if all(p.isdigit() for p in pages) and [int(p) for p in pages] == list(range(int(pages[0]), int(pages[0]) + len(pages))):
        return f"pp. {pages[0]}–{pages[-1]}"
    return "pp. " + ", ".join(pages)


def with_page(e):
    """Every evidence item ends with a citation that names its page (the pages the item declares): the page goes into
    the item's last citation of its work when that citation names no page (one bracket, not two: round 5), else a
    citation of the page is added."""
    text = para(e["text"])
    if re.search(r"\[@S0\d[^\]]*\bpp?\.", text):
        return text
    loc = pages_text(e["pages"])
    last = list(re.finditer(rf"\[@{e['work']}(, [^\]]*)?\]\s*$", text))
    if last:
        m = last[-1]
        return text[:m.start()] + f"[@{e['work']}{m.group(1) or ''}, {loc}]" + text[m.end():]
    return text + f" [@{e['work']}, {loc}]"


def thesis(t):
    nums = problems_of(t["num"])
    probs = ", ".join(str(n) for n in nums)
    L = [f"::: {{.thesis #thesis-{t['num']} title=\"{t['title']}\"}}", "::: claim", t["claim"], ":::", "",
         "::: {.field label=\"Argument\"}", para(t["argument"]), ":::", "",
         "::: {.field label=\"Evidence in the seven works\"}"]
    for i, e in enumerate(t["evidence"]):
        L += [with_page(e), ""]
    L += [":::", "", "::: {.field label=\"An instance\"}", para(INST[t["num"]]), ":::", "",
          "::: {.field label=\"Relation to existing work\"}", para(t["relation"]), ":::", "",
          "::: {.field label=\"What would refute it\"}", para(t["refutation"]), ":::", "",
          "::: {.field label=\"Problems\"}",
          f"In *The 57 Grothendieckian Problems*: {'Problem' if len(nums) == 1 else 'Problems'} {probs}.", ":::", ":::", ""]
    return "\n".join(L)


def main():
    ths = yaml.safe_load((SRC / "theses.yaml").read_text(encoding="utf-8"))
    assert [t["num"] for t in ths] == list(range(1, 13))
    sec = ["# The twelve theses", "",
           "Each thesis is stated in italics and followed by its argument, the passages of the seven works on which it "
           "rests, its relation to existing work, an observation that would refute it, and the problems of *The 57 "
           "Grothendieckian Problems* at which it can be tested. Quotation marks enclose the words of the source on the page cited; the page "
           "numbers are the printed folios of the published PDFs. \\figref{theses} shows the twelve theses in their three "
           "groups, and \\figref{chain} draws Theses 6 and 7.", "",
           "::: {.figure #fig:theses file=\"fig-theses\" place=\"tbp\"}",
           "The twelve theses in their three groups — representation (Theses 1–3), operation (Theses 4–7) and method "
           "(Theses 8–12) — with the number of problems of *The 57 Grothendieckian Problems* at which each can be tested; the "
           "problems are listed with each thesis. Each cell links to its thesis.", ":::", ""]
    chain = ["::: {.figure #fig:chain file=\"fig-chain\" place=\"tbp\"}",
             "Theses 6 and 7. Above, the chain of non-implications of [@S01, Vol. III, Ch. 3, p. 8004], with the input "
             "that each passage requires and the way in which it fails, from the argument of Thesis 6. Below, the "
             "separation of proposing from authorising [@S01, Architectural Prospectus, p. 7966] and the four cases in "
             "which, by [@S01, Vol. V, Proposition 1.3, pp. 11913–11914], it fails.", ":::", ""]
    groups = {1: "## Representation {.unnumbered}", 4: "## Operation {.unnumbered}", 8: "## Method {.unnumbered}"}
    for t in ths:
        if t["num"] in groups:
            sec += [groups[t["num"]], ""]
        sec.append(thesis(t))
        if t["num"] == 6:
            sec += chain
    decl = "# Declarations {.unnumbered}\n\n" + (SRC / "declarations.md").read_text(encoding="utf-8").strip() + "\n"
    decl = decl.replace("no problem in this\npaper was posed by Grothendieck unless the card says so.", "the image of the rising sea is his, as reported\nin [@McLarty2007].")
    body = {"40-theses.md": "\n".join(sec), "80-declarations.md": decl}
    texts = [(OUT / h).read_text(encoding="utf-8") for h in HAND] + list(body.values())
    keys = refs.used(texts)
    body["90-references.md"] = "# References {.unnumbered}\n\n" + refs.reference_list(keys)
    for h in HAND:
        (OUT / h.replace(".md", ".cited.md")).write_text(refs.cite_text((OUT / h).read_text(encoding="utf-8")),
                                                        encoding="utf-8", newline="\n")
    for name, text in body.items():
        (OUT / name).write_text(refs.cite_text(text) + "\n", encoding="utf-8", newline="\n")
    (OUT / "ORDER.txt").write_text("# generated by tools/render_paper1.py\n01-introduction.cited.md\n40-theses.md\n"
                                   "45-together.cited.md\n50-limits.cited.md\n80-declarations.md\n90-references.md\n",
                                   encoding="utf-8", newline="\n")
    words = sum(len(re.findall(r"[A-Za-z0-9’'-]+", re.sub(r"\[[^\]]*\]|\$[^$]*\$|:::.*|#.*", " ", t)))
                for t in [(OUT / h).read_text(encoding="utf-8") for h in HAND] + [body["40-theses.md"]])
    print(f"paper I: 12 theses, {len(keys)} references, about {words} words of text")


if __name__ == "__main__":
    main()
