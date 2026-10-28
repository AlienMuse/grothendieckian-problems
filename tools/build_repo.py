"""Generate the repository AlienMuse/grothendieckian-problems in campaign/repo/ from the single sources.

  python tools/build_repo.py      → repo/README.md, THESES.md, problems/NN.md, problems.json, formal/, papers/, NOTICE …

Everything is generated: edit src/, not repo/. Text files are written with LF. The two PDFs are copied from out/ when
present (papers/). Citations are rendered as in the papers, with a references section per file.
"""
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "tools"))
import refs  # noqa: E402
from render_paper1 import with_page  # noqa: E402  (evidence items with their pages, as in paper II's companion)
from figures import FIGS, PAPERS, numbers as figures_numbers  # noqa: E402
PAPER_NAME = {"overview": "An Overview", "paper-I": "The Rising-Sea Theses", "paper-II": "The 57 Grothendieckian Problems"}

SRC, REPO = HERE / "src", HERE / "repo"
LEAKPATS = ("/workspace/", "v_5f55", "v_58db", "Creative Project", "release-kit/private", "ghp_")  # LEAK patterns
GH = "https://github.com/AlienMuse/grothendieckian-problems"
SITE = "https://alienmuse.github.io"
# the three papers: Zenodo records reserved in S4 (zenodo-state.json, kept out of the repository)
_ZS = json.loads((HERE / "zenodo-state.json").read_text(encoding="utf-8")) if (HERE / "zenodo-state.json").exists() else {}
PAPER_DOI = {k: _ZS[k]["concept_doi"] for k in ("overview", "theses", "problems") if k in _ZS}
DOI = {"S00": "10.5281/zenodo.23669107", "S01": "10.5281/zenodo.23480696", "S02": "10.5281/zenodo.23538544",
       "S03": "10.5281/zenodo.23564898", "S04": "10.5281/zenodo.23585887", "S05": "10.5281/zenodo.23597954",
       "S06": "10.5281/zenodo.23610034", "S07": "10.5281/zenodo.23629681"}
TITLE = {"S01": "GAI-MUA: The Grothendieckian Machine", "S02": "GM-Omega-Infinity: Topos-Native Intelligence",
         "S03": "Arithmetic Spectral Descent", "S04": "Fractured Adelic Geometry", "S05": "The Archimedean Prism",
         "S06": "Strained Prismatic Geometry", "S07": "The Arithmetic Topos"}
KIND = {"math": "mathematical", "machine": "machine", "formal": "formalization"}
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def w(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def para(s):
    return " ".join(str(s).split())


def md_cite(text, used):
    for k in refs.used([text]):
        if k not in used:
            used.append(k)
    return refs.cite_text(text)


def ref_section(used):
    if not used:
        return ""
    ok = refs.verified()
    assert all(k in ok for k in used), [k for k in used if k not in ok]
    keys = sorted(used, key=lambda k: (not refs.REFS[k]["label"].startswith("S0"), refs.REFS[k]["label"].lower()))
    return "\n## References\n\n" + "\n\n".join(refs.entry(k) for k in keys) + "\n"


def load_cards():
    cards = []
    for f in sorted((SRC / "problems").glob("*.yaml")):
        cards += yaml.safe_load(f.read_text(encoding="utf-8"))
    return sorted(cards, key=lambda c: c["num"])


def main():
    cards = load_cards()
    theses = yaml.safe_load((SRC / "theses.yaml").read_text(encoding="utf-8"))
    inst = yaml.safe_load((SRC / "thesis-instances.yaml").read_text(encoding="utf-8"))
    tmap = {t["num"]: t for t in theses}
    if REPO.exists():
        for p in REPO.iterdir():
            if p.name != ".git":
                shutil.rmtree(p) if p.is_dir() else p.unlink()
    REPO.mkdir(exist_ok=True)
    lean = {int(re.match(r"P(\d+)", f.stem).group(1)): f"formal/GrothendieckianProblems/{f.name}"
            for f in (HERE / "formal" / "GrothendieckianProblems").glob("P*.lean")}

    # problems/NN.md and problems.json
    data = []
    for c in cards:
        used = []
        t = tmap[c["thesis"]]
        body = [f"# Problem {c['num']} · {c['title']}", "",
                f"**Kind.** {KIND[c['kind']].capitalize()} problem, {c['level']} level. Thesis {c['thesis']} "
                f"([{t['title']}](../THESES.md#thesis-{c['thesis']})).", "",
                f"**Source.** *{TITLE[c['work']]}* [@{c['work']}], {c['source']}. DOI [{DOI[c['work']]}](https://doi.org/{DOI[c['work']]}).", "",
                f"**Status in the source.** {para(c['status'])}.", "",
                f"**Statement.** {para(c['statement'])}", "",
                f"**What the source establishes.** {para(c['established'])}", "",
                f"**Proposed by.** {para(c['proposer'])}", "",
                f"**Background.** {para(c['background'])}", "",
                f"**Solved when.** {para(c['solved'])}", "",
                f"**Literature check (28 October 2026).** {para(c['litcheck'])}", ""]
        if c["num"] in lean:
            body += [f"**Lean statement.** [`{lean[c['num']]}`](../{lean[c['num']]}).", ""]
        body += [f"**Discussion.** [Issue {c['num']}]({GH}/issues/{c['num']}). Solutions, partial results, counterexamples "
                 "to the problem as stated and reports that it is already solved are all welcome; see "
                 "[CONTRIBUTING](../CONTRIBUTING.md).", ""]
        text = md_cite("\n".join(body), used) + ref_section(used)
        w(REPO / "problems" / f"{c['num']:02d}.md", text)
        data.append({"number": c["num"], "title": c["title"], "part": 1 if c["num"] <= 35 else 2,
                     "kind": c["kind"], "level": c["level"], "thesis": c["thesis"],
                     "source": {"work": c["work"], "title": TITLE[c["work"]], "doi": DOI[c["work"]],
                                "locator": c["source"], "pages": c["pages"], "status": para(c["status"])},
                     "statement": refs.cite_text(para(c["statement"])), "established": refs.cite_text(para(c["established"])),
                     "proposed_by": refs.cite_text(para(c["proposer"])), "background": refs.cite_text(para(c["background"])),
                     "solved_when": refs.cite_text(para(c["solved"])), "literature_check": {
                         "date": "2026-10-28", "finding": refs.cite_text(para(c["litcheck"]))},
                     "lean": lean.get(c["num"]), "discussion": f"{GH}/issues/{c['num']}"})
    meta = {"title": "The 57 Grothendieckian Problems", "version": "1.0", "licence": "CC-BY-4.0",
            "doi": PAPER_DOI.get("problems"), "companion_papers": {"overview": PAPER_DOI.get("overview"),
                                                                   "theses": PAPER_DOI.get("theses")},
            "code_licence": "Apache-2.0", "author": {"name": "Vincent Liu", "orcid": "0009-0000-8718-222X",
                                                     "affiliation": "WiseMotif.ai"},
            "source_works": {k: {"title": TITLE.get(k, "The Grothendieckian Programme"), "doi": v} for k, v in DOI.items()},
            "problems": data}
    w(REPO / "problems.json", json.dumps(meta, ensure_ascii=False, indent=1))

    # THESES.md
    used = []
    th = ["# The Rising-Sea Theses", "", "*Twelve Theses on Mathematics and Machine Reasoning.* The full text, with its "
          "introduction, the relation to existing work and the limits of the evidence, is the paper "
          "[`papers/The-Rising-Sea-Theses.pdf`](papers/The-Rising-Sea-Theses.pdf). Quotations are from the published "
          "PDFs of the seven works, on the pages cited.", ""]
    for t in theses:
        probs = ", ".join(f"[{n}](problems/{n:02d}.md)" for n in t["problems"])
        th += [f'<a id="thesis-{t["num"]}"></a>', f"## {t['num']}. {t['title']}", "", f"> {t['claim']}", "",
               para(t["argument"]), "", "**Evidence in the seven works.**", ""]
        th += [f"- {with_page(e)}" for e in t["evidence"]]
        th += ["", f"**An instance.** {para(inst[t['num']])}", "", f"**Relation to existing work.** {para(t['relation'])}", "",
               f"**What would refute it.** {para(t['refutation'])}", "", f"**Problems.** {probs}", ""]
    w(REPO / "THESES.md", md_cite("\n".join(th), used) + ref_section(used))

    # README.md
    used = []
    rows = "\n".join(f"| [{c['num']}](problems/{c['num']:02d}.md) | {c['title']} | {c['work']} | {KIND[c['kind']]} | "
                     f"{c['level']} | {c['thesis']} |" for c in cards)
    claims = "\n".join(f"{t['num']}. **{t['title']}.** {t['claim']}" for t in theses)
    pdf_size = {k: (HERE / "out" / f).stat().st_size / 1e6 for k, f in (("overview", "overview.pdf"), ("theses", "paper-I.pdf"),
                                                                       ("problems", "paper-II.pdf"))}
    d0 = PAPER_DOI.get("overview", "")
    badge = lambda label, value, colour: (f"https://img.shields.io/badge/{label.replace('-', '--').replace(' ', '%20')}-"
                                          f"{value.replace('-', '--').replace(' ', '%20')}-{colour}?style=flat")
    head = f"""<p align="center">
  <a href="https://doi.org/{d0}"><img src="assets/hero.png" alt="The 57 Grothendieckian Problems — the seven works of the Grothendieckian Programme as a seven-cell honeycomb, each cell with the range of the problems drawn from it: Series 01 problems 1–17, Series 02 18–35, Series 03 36–39, Series 04 40–43, Series 05 44–48, Series 06 49–52, Series 07 53–57" width="100%"></a>
</p>

<p align="center">
  <a href="https://doi.org/{PAPER_DOI.get('overview', '')}"><img src="{badge('overview', 'doi ' + PAPER_DOI.get('overview', '').split('.')[-1], '1E5A88')}" alt="The overview: doi:{PAPER_DOI.get('overview', '')}"></a>
  <a href="https://doi.org/{PAPER_DOI.get('theses', '')}"><img src="{badge('theses', 'doi ' + PAPER_DOI.get('theses', '').split('.')[-1], '1E5A88')}" alt="The theses: doi:{PAPER_DOI.get('theses', '')}"></a>
  <a href="https://doi.org/{PAPER_DOI.get('problems', '')}"><img src="{badge('problems', 'doi ' + PAPER_DOI.get('problems', '').split('.')[-1], '1E5A88')}" alt="The problems: doi:{PAPER_DOI.get('problems', '')}"></a>
  <a href="LICENSE"><img src="{badge('license', 'CC BY 4.0', '0A131E')}" alt="License: CC BY 4.0"></a>
  <a href="LICENSE-CODE"><img src="{badge('code', 'Apache 2.0', '0A131E')}" alt="Code: Apache 2.0"></a>
  <a href="{GH}/releases/tag/v1.0.0"><img src="{badge('release', '1.0', '1E5A88')}" alt="Release 1.0"></a>
  <img src="{badge('theses', '12', '536372')}" alt="12 theses">
  <img src="{badge('problems', '57', '536372')}" alt="57 problems">
  <img src="{badge('Lean 4', 'Mathlib pinned', '536372')}" alt="Lean 4, Mathlib pinned">
  <a href="https://orcid.org/0009-0000-8718-222X"><img src="{badge('ORCID', '0009-0000-8718-222X', 'A6CE39')}" alt="ORCID 0009-0000-8718-222X"></a>
  <a href="papers/VERIFY.md"><img src="{badge('OpenPGP', 'signed', 'B8913B')}" alt="OpenPGP signed"></a>
</p>

<p align="center">
  <b><a href="papers/The-Grothendieckian-Programme-An-Overview.pdf">Read the overview</a></b> ({pdf_size['overview']:.1f} MB) ·
  <a href="papers/The-Rising-Sea-Theses.pdf">The theses</a> ({pdf_size['theses']:.1f} MB) ·
  <a href="papers/The-57-Grothendieckian-Problems.pdf">The problems</a> ({pdf_size['problems']:.1f} MB) ·
  <a href="#the-fifty-seven-problems">Problem table</a> ·
  <a href="#taking-part">Take part</a> ·
  <a href="{SITE}/grothendieckian-programme/">Website</a>
</p>

"""
    readme = head + f"""# The 57 Grothendieckian Problems

**An overview, twelve theses and fifty-seven open problems on mathematics and machine reasoning, drawn from the seven
works of the [Grothendieckian Programme]({SITE}/grothendieckian-programme/).**

> “All right, take 57.” — as told in A. Jackson, *Notices of the AMS* 51 (2004), p. 1196. Fifty-seven is 3 × 19.

This repository holds three papers and their data, released together:

1. **The Grothendieckian Programme: An Overview** — *Seven Open Works on Mathematics and Machine Reasoning*
   ([PDF](papers/The-Grothendieckian-Programme-An-Overview.pdf), doi:[{PAPER_DOI.get('overview', '')}](https://doi.org/{PAPER_DOI.get('overview', '')})):
   the architecture, the five research subjects, the method, the series and its records, and the research plan, in
   ten pages.
2. **The Rising-Sea Theses** — *Twelve Theses on Mathematics and Machine Reasoning* ([PDF](papers/The-Rising-Sea-Theses.pdf),
   doi:[{PAPER_DOI.get('theses', '')}](https://doi.org/{PAPER_DOI.get('theses', '')}), [text](THESES.md)).
3. **The 57 Grothendieckian Problems** — *Open Problems for Mathematics and Machine Reasoning from the Grothendieckian
   Programme* ([PDF](papers/The-57-Grothendieckian-Problems.pdf), doi:[{PAPER_DOI.get('problems', '')}](https://doi.org/{PAPER_DOI.get('problems', '')}),
   [cards](problems/), [`problems.json`](problems.json), [Lean statements](formal/)).

The thirteen figures of the three papers, with their sources and data, are in [`figures/`](figures/). The PDFs are
signed: [`papers/SHA256SUMS`](papers/SHA256SUMS) with its OpenPGP signature and timestamps; see
[`papers/VERIFY.md`](papers/VERIFY.md).

<p align="center">
  <a href="figures/fig-rose.png"><img src="figures/fig-rose.png" alt="Figure 1 of The 57 Grothendieckian Problems: the fifty-seven problems in the seven works, in the honeycomb of the Programme; each small cell is a problem, tinted by kind, with its level as one to three dots" width="100%"></a>
  <br><sub>Figure 1 of <i>The 57 Grothendieckian Problems</i> (600 ppi; the 13 figures of the three papers are in <a href="figures/">figures/</a>).</sub>
</p>

The seven source works ([@S01; @S02; @S03; @S04; @S05; @S06; @S07]; overview volume [@S00]) comprise 34 volumes and 26,021
pages, released on Zenodo in October 2026 as first drafts that have not been peer-reviewed. None of them claims a proof
of the Riemann Hypothesis, the Birch and Swinnerton-Dyer conjecture, the Hodge conjecture, the *abc* conjecture or the
Langlands correspondence, and none of the problems below is one of those conjectures.

## The twelve theses

{claims}

## The fifty-seven problems

Problems 1–35 come from the two works on the architecture of a reasoning system for mathematics (Series 01 and 02);
Problems 36–57 from the five works that each take a named conjecture or programme as research subject (Series 03–07).
Every problem states what counts as a solution. Every quotation has been checked against the published PDFs, and every
problem against the literature (28 October 2026; the records are in the paper and in `problems.json`).

| # | Problem | Source | Kind | Level | Thesis |
|---|---|---|---|---|---|
{rows}

## Taking part

Each problem has an issue: post a solution, a partial result, a counterexample to the problem as stated, a reference
showing that it is already solved, or a correction. A solution that meets the criterion of its card is recorded,
under the solver's name, in the next version of the papers, in the next edition of the source work, and in
[SOLVED.md](SOLVED.md). No prize is attached. Corrections to the papers go to [ERRATA.md](ERRATA.md). See
[CONTRIBUTING.md](CONTRIBUTING.md).

For AI laboratories and tool builders: `problems.json` lists every problem with its source, status, kind and decision
criterion, and `formal/` contains Lean 4 statements against a pinned Mathlib; both may be used as a benchmark under
the licences below.

## Licence and name

Text, data and figures: [CC BY 4.0](LICENSE). Code — the Lean files (`formal/`), the scripts (`tools/`), the
typesetting files (`styles/`, `filters/`) and the source code of the figures (`figures/web/`): [Apache-2.0](LICENSE-CODE).
The fonts and three.js in `figures/web/` keep their own licences. The seven works keep their own licence
(CC BY-NC-ND 4.0). The adjective *Grothendieckian* names a method used in the works and implies no attribution of
design or endorsement to Alexander Grothendieck; see [NOTICE](NOTICE). Author: Vincent Liu, WiseMotif.ai, ORCID
[0009-0000-8718-222X](https://orcid.org/0009-0000-8718-222X), <vincent.liu@wisemotif.ai>.
"""
    foot = """
---

<p align="center"><sub>
  <a href="https://wisemotif.ai">WiseMotif Monograph of Mathematical Intelligence</a> · Three papers on the Grothendieckian Programme<br>
  Series 00: <a href="https://github.com/AlienMuse/grothendieckian-programme"><i>The Grothendieckian Programme</i></a> ·
  Series 01: <a href="https://github.com/AlienMuse/grothendieckian-machine"><i>GAI-MUA: The Grothendieckian Machine</i></a> ·
  Series 02: <a href="https://github.com/AlienMuse/topos-native-intelligence"><i>GM-Omega-Infinity: Topos-Native Intelligence</i></a> ·
  Series 03: <a href="https://github.com/AlienMuse/arithmetic-spectral-descent"><i>Arithmetic Spectral Descent</i></a> ·
  Series 04: <a href="https://github.com/AlienMuse/fractured-adelic-geometry"><i>Fractured Adelic Geometry</i></a> ·
  Series 05: <a href="https://github.com/AlienMuse/the-archimedean-prism"><i>The Archimedean Prism</i></a> ·
  Series 06: <a href="https://github.com/AlienMuse/strained-prismatic-geometry"><i>Strained Prismatic Geometry</i></a> ·
  Series 07: <a href="https://github.com/AlienMuse/the-arithmetic-topos"><i>The Arithmetic Topos</i></a><br>
  © 2026 Vincent Liu · <a href="https://orcid.org/0009-0000-8718-222X">ORCID 0009-0000-8718-222X</a> · <a href="https://alienmuse.github.io">alienmuse.github.io</a>
</sub></p>
"""
    w(REPO / "README.md", md_cite(readme, used) + ref_section(used) + foot)

    # supporting files
    w(REPO / "CONTRIBUTING.md", f"""# Contributing

Each of the 57 problems has an issue in this repository, numbered as the problem. Please use the issue templates.

- **A solution or a partial result.** Link a preprint, a proof, a formal development or a published record, and say
  which part of the card's *Solved when* criterion it meets. Solutions are checked against that criterion only.
- **A counterexample to a problem as stated**, or a proof that it is ill-posed: this also counts as a solution.
- **Already solved.** If a problem, or part of it, was settled before 28 October 2026, give the reference; the card
  and the papers are corrected and the finding is credited.
- **A correction** to a quotation, a page, a status or a reference: open an issue with the template *Correction*.

Credit: a solution that meets its criterion is recorded under the solver's name in the next version of the papers, in
the next edition of the source work, and in SOLVED.md. Corrections are credited in ERRATA.md.

Contributions to the text and data are licensed under CC BY 4.0, contributions to the code (`formal/`, `tools/`,
`styles/`, `filters/`, `figures/web/`) under Apache-2.0.
""")
    w(REPO / "SOLVED.md", "# Solutions\n\nNone recorded yet. Each entry gives the problem, the solver, the date, the reference and the part of the criterion met.\n")
    errata = ["# Errata", "", "Corrections to the source works found while preparing the papers (28 October 2026).", "",
              "| Source | Place | Correction | Found by |", "|---|---|---|---|",
              "| *Arithmetic Spectral Descent* (S03) | Problem 28.13, p. 604 | The source states that no construction of a Pin(2)-equivariant lift of THH is known. Quaternionic topological Hochschild homology THQ, with a Pin(2)-action, is constructed by Angelini-Knoll, Merling and Péroux (arXiv:2409.18187; Adv. Math. 2026). The first question of Problem 28.13 is answered; see Problem 38. | literature check |",
              "", "Corrections to the papers will be listed here with the version in which they are made."]
    w(REPO / "ERRATA.md", "\n".join(errata))
    w(REPO / "NOTICE", """The Grothendieckian Programme: An Overview; The Rising-Sea Theses; The 57 Grothendieckian Problems
Copyright (c) 2026 Vincent Liu, WiseMotif.ai

Licences
  Text, data and figures — the papers (papers/), README.md, THESES.md, problems/, problems.json, src/, data/,
  figures/*.png, the banner (assets/) and the other Markdown files — are licensed under the Creative Commons Attribution 4.0 International licence
  (CC-BY-4.0, LICENSE).
  Code — formal/ (the Lean files), tools/ (the scripts), styles/ and filters/ (the typesetting files) and figures/web/
  (the source code of the figures) — is licensed under the Apache License, Version 2.0 (Apache-2.0, LICENSE-CODE;
  formal/LICENSE). tools/pdf_cache.py and figures/web/lib.js and style.css are copied from the sources of the
  overview (Series 00) and are licensed here under Apache-2.0 by their author.
  Third-party files keep their own licences: the TGP faces in figures/web/fonts/ (derived from TeX Gyre Pagella and
  STIX Two Math: GUST Font License and SIL Open Font License 1.1, texts beside them) and three.js r186 in
  figures/web/vendor/three/ (MIT licence, vendor/three/LICENSE). The figures name Segoe UI, which is not included.

Quotations from the seven works of the Grothendieckian Programme (Series 01-07) and its overview (Series 00) are
reproduced under their licence, CC BY-NC-ND 4.0, with attribution; the works themselves are not relicensed.

Name. The adjective "Grothendieckian" names a mathematical method used in the seven works. It carries no attribution
of design or endorsement to Alexander Grothendieck or to any other mathematician whose work is cited. No problem in
this repository was posed by Grothendieck unless its card says so.

Use of AI tools: see the declarations in either paper.
""")
    # the licence texts, as published (licences/: apache.org and creativecommons.org, 2026-10-28)
    for name, dst in (("CC-BY-4.0.txt", REPO / "LICENSE"), ("Apache-2.0.txt", REPO / "LICENSE-CODE"),
                      ("Apache-2.0.txt", REPO / "formal" / "LICENSE")):
        dst.parent.mkdir(parents=True, exist_ok=True)
        w(dst, (HERE / "licences" / name).read_text(encoding="utf-8"))
    author_cff = """  - family-names: Liu
    given-names: Vincent
    orcid: "https://orcid.org/0009-0000-8718-222X"
    affiliation: WiseMotif.ai"""
    papers_cff = [("overview", "The Grothendieckian Programme: An Overview — Seven Open Works on Mathematics and Machine Reasoning"),
                  ("theses", "The Rising-Sea Theses: Twelve Theses on Mathematics and Machine Reasoning"),
                  ("problems", "The 57 Grothendieckian Problems: Open Problems for Mathematics and Machine Reasoning from the Grothendieckian Programme")]

    def ref(k, title, indent):
        p = " " * indent
        return (f'{p}type: article\n{p}title: "{title}"\n{p}authors:\n' + "\n".join(p + l[2:] if False else " " * (indent - 2) + l for l in author_cff.split("\n"))
                + f'\n{p}year: 2026\n{p}doi: "{PAPER_DOI.get(k, "")}"\n{p}publisher:\n{p}  name: Zenodo')
    w(REPO / "CITATION.cff", f"""cff-version: 1.2.0
message: "If you use the overview, the theses or the problems, please cite the papers."
title: "The Grothendieckian Programme: An Overview, The Rising-Sea Theses and The 57 Grothendieckian Problems"
version: "1.0"
date-released: "2026-10-28"
license: [CC-BY-4.0, Apache-2.0]
repository-code: "{GH}"
authors:
{author_cff}
    email: vincent.liu@wisemotif.ai
keywords: [Grothendieckian Programme, open problems, machine reasoning, formal verification, Lean]
preferred-citation:
{ref(*papers_cff[0], 2)}
references:
  - {ref(*papers_cff[1], 4).lstrip()}
  - {ref(*papers_cff[2], 4).lstrip()}
""")
    tmpl = REPO / ".github" / "ISSUE_TEMPLATE"
    for name, title, body in (("solution", "Solution or partial result", "Problem number:\n\nLink to the proof, preprint, formal development or record:\n\nWhich part of the *Solved when* criterion it meets:\n"),
                              ("already-solved", "Already solved", "Problem number:\n\nReference (with date) settling the problem or a part of it:\n"),
                              ("counterexample", "Counterexample or ill-posed", "Problem number:\n\nThe counterexample, or why the problem as stated is ill-posed:\n"),
                              ("correction", "Correction", "Paper or card, and place:\n\nWhat is wrong (quotation, page, status, reference):\n\nThe correction:\n")):
        w(tmpl / f"{name}.md", f"---\nname: {title}\nabout: {title}\ntitle: \"[{title}] \"\n---\n\n{body}")
    # Lean
    dst = REPO / "formal"
    for f in ("lakefile.toml", "lean-toolchain", "lake-manifest.json", "GrothendieckianProblems.lean"):
        shutil.copy2(HERE / "formal" / f, dst / f) if dst.exists() else (dst.mkdir(parents=True), shutil.copy2(HERE / "formal" / f, dst / f))
    (dst / "GrothendieckianProblems").mkdir(exist_ok=True)
    for f in (HERE / "formal" / "GrothendieckianProblems").glob("*.lean"):
        shutil.copy2(f, dst / "GrothendieckianProblems" / f.name)
    w(dst / "README.md", "# Lean statements\n\nLean 4 statements of the formalization problems that can be stated against Mathlib today. Proofs are `sorry` by convention, as in google-deepmind/formal-conjectures; a solution replaces every `sorry` and adds no axiom.\n\n```\nlake exe cache get\nlake build\n```\n\n| Problem | File |\n|---|---|\n" +
      "\n".join(f"| [{n}](../problems/{n:02d}.md) | [`{Path(p).name}`](GrothendieckianProblems/{Path(p).name}) |" for n, p in sorted(lean.items())))
    w(REPO / ".gitattributes", "* text=auto eol=lf\n*.pdf binary\n")
    w(REPO / ".gitignore", "formal/.lake/\n")
    # papers
    (REPO / "papers").mkdir(exist_ok=True)
    # the banner of the series (tools/banner.py)
    hero = HERE / "figures" / "banner" / "hero.png"
    if not hero.exists():
        raise SystemExit("figures/banner/hero.png missing: run tools/banner.py")
    (REPO / "assets").mkdir(exist_ok=True)
    shutil.copy2(hero, REPO / "assets" / "hero.png")
    dist = HERE / "dist"
    for src, dst_name in (("overview.pdf", "The-Grothendieckian-Programme-An-Overview.pdf"),
                          ("paper-I.pdf", "The-Rising-Sea-Theses.pdf"), ("paper-II.pdf", "The-57-Grothendieckian-Problems.pdf")):
        # the sealed release files when dist/ holds them, else the latest build
        shutil.copy2(dist / dst_name if (dist / dst_name).exists() else HERE / "out" / src, REPO / "papers" / dst_name)
    for f in ("SHA256SUMS", "SHA256SUMS.asc", "SHA256SUMS.tsr", "SHA256SUMS.ots", "VincentLiu-signing-key.asc"):
        if (dist / f).exists():
            shutil.copy2(dist / f, REPO / "papers" / f)
    w(REPO / "papers" / "VERIFY.md", """# Verifying the papers

`SHA256SUMS` lists the SHA-256 digests of the three PDFs. `SHA256SUMS.asc` is its detached OpenPGP signature by the
author's key (`VincentLiu-signing-key.asc`), `SHA256SUMS.tsr` an RFC 3161 timestamp token over it and
`SHA256SUMS.ots` an OpenTimestamps proof anchored in Bitcoin. The same files are in the Zenodo record of each paper.

```
sha256sum -c SHA256SUMS
gpg --import VincentLiu-signing-key.asc
gpg --verify SHA256SUMS.asc SHA256SUMS
ots verify SHA256SUMS.ots
```
""")
    # sources, scripts and records (data availability statement of both papers)
    for sub in ("problems", "overview", "paper-I", "paper-II"):
        (REPO / "src" / sub).mkdir(parents=True, exist_ok=True)
    for f in ["theses.yaml", "thesis-instances.yaml", "refs.yaml", "changes.yaml", "declarations.md",
              "litcheck-queries.yaml", "claims-ALLOW.json"]:
        shutil.copy2(SRC / f, REPO / "src" / f)
    shutil.copy2(HERE.parent / "programme.yaml", REPO / "src" / "programme.yaml")      # Series 00's single source (figures)
    for f in (SRC / "problems").glob("*.yaml"):
        shutil.copy2(f, REPO / "src" / "problems" / f.name)
    for paper in ("overview", "paper-I", "paper-II"):
        for f in (SRC / paper).iterdir():
            if f.suffix in (".md", ".yaml", ".txt"):
                shutil.copy2(f, REPO / "src" / paper / f.name)
    (REPO / "tools").mkdir(exist_ok=True)
    for f in ["portable.py", "extract_candidates.py", "quote_gate.py", "verify_refs.py", "litcheck.py",
              "find_phrases.py", "dump_sections.py", "page_text.py", "refs.py", "render_overview.py", "render_paper1.py", "render_paper2.py",
              "paper_gates.py", "lean_gate.py", "build_repo.py", "complete_refs.py", "build.py", "figures.py",
              "litcheck_retry.py", "zenodo_facts.py", "banner.py", "figures_png.py", "code_archive.py"]:
        shutil.copy2(HERE / "tools" / f, REPO / "tools" / f)
    shutil.copy2(HERE.parent / "master" / "tools" / "pdf_cache.py", REPO / "tools" / "pdf_cache.py")
    for d in ("styles", "filters"):
        shutil.copytree(HERE / d, REPO / d, dirs_exist_ok=True)
    w(REPO / "tools" / "README.md", """# Scripts

The scripts that produced and checked the two papers. They read the page text of the sealed PDFs of the seven works:
download the PDFs from Zenodo (DOIs in the papers), extract their page text with `pdf_cache.py`, and set `GP_CORPUS` to
the directory it writes. The single sources of the papers are in `src/`; the records of the checks are in `data/`.

| Script | Role |
|---|---|
| `extract_candidates.py` | candidate open items, by each work's status notation |
| `find_phrases.py`, `page_text.py`, `dump_sections.py` | locate passages and read pages |
| `litcheck.py` | literature check (arXiv, OpenAlex, zbMATH Open, Crossref, GitHub code search) → `data/litcheck/` |
| `verify_refs.py`, `complete_refs.py` | every reference against its DOI, arXiv id, zbMATH record or page → `data/REFS-CHECK.md` |
| `quote_gate.py` | every quotation against the page it cites → `data/QUOTE-GATE.md` |
| `paper_gates.py`, `lean_gate.py` | the remaining gates of the papers → `data/PAPER-GATES.md`, `data/LEAN-GATE.md` |
| `render_paper1.py`, `render_paper2.py`, `build_repo.py` | generate the papers' Markdown and this repository from `src/` |

The papers are typeset with Pandoc 3.9 and LuaHBTeX (TeX Live 2025) using `styles/` and `filters/`.

Licence: Apache-2.0 ([`../LICENSE-CODE`](../LICENSE-CODE)), as `styles/`, `filters/`, `formal/` and `figures/web/`.
""")
    # the figures: PDFs, a PNG of each for the web (150 ppi), and their sources (modules, data, the Series 00 design
    # library with its faces and three.js, each under its own licence); not the light layers (regenerated)
    fig = REPO / "figures"
    (fig / "web").mkdir(parents=True, exist_ok=True)
    import pymupdf
    for f in sorted((HERE / "figures").glob("fig-*.pdf")):    # the PDFs are in the papers and are made by figures.py
        (fig / f.name).unlink(missing_ok=True)
        shutil.copy2(f.with_suffix(".tex"), fig / f.with_suffix(".tex").name)
        png = HERE / "figures" / "png600" / f.with_suffix(".png").name      # 600 ppi (tools/figures_png.py)
        if not png.exists():
            raise SystemExit(f"{png.name} missing: run tools/figures_png.py")
        shutil.copy2(png, fig / png.name)
    web = HERE / "figures" / "web"
    for f in web.rglob("*"):
        if f.is_file() and not f.name.startswith(("gl-", "hud-")) and ".tmp." not in f.name:
            dst = fig / "web" / f.relative_to(web)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst)
    shutil.copy2(HERE.parent / "master" / "figures" / "web" / "data-programme.json", fig / "web" / "s00-data-programme.json")
    w(fig / "README.md", "# Figures\n\nThe thirteen figures of the three papers, as PNG at 600 ppi (3119 px across the "
      "132 mm measure of the papers). In the papers each is a PDF "
      "132 mm wide, made by `../tools/figures.py` (`fig-<id>.tex` places the links of the figure over it). Every word and number of a figure "
      "comes from the sources in `../src/` and is checked there and in the PDF text by `../tools/figures.py` "
      "(`../data/FIGURE-GATE.md`).\n\n`web/` holds the sources: one module per figure (`fig-<id>.js`), its data "
      "(`data-<id>.json`), `rs.js`, and the figure library of the overview (Series 00: `lib.js`, `style.css`, the TGP "
      "faces with their licences, three.js r186 under the MIT licence), unchanged (`DESIGN-SOURCE.json`). Rendering "
      "needs Chrome; the labels are set in Segoe UI, which is not included.\n\nLicences: the PNG figures CC BY 4.0 "
      "([`../LICENSE`](../LICENSE)); the source code in `web/` Apache-2.0 ([`../LICENSE-CODE`](../LICENSE-CODE)); the "
      "faces in `web/fonts/` and three.js in `web/vendor/three/` their own licences, beside them.\n\n"
      "| Paper | Figure | File |\n|---|---|---|\n" +
      "\n".join(f"| {PAPER_NAME[FIGS[k][0]]} | {n} | [`fig-{k}.png`](fig-{k}.png) |"
                for k, n in sorted(figures_numbers().items(), key=lambda kv: (PAPERS.index(FIGS[kv[0]][0]), kv[1]))) + "\n")
    # the items extracted from the seven works (paper II, Section 1.1): identifiers, status and page, not their text
    pool = json.loads((HERE / "candidates" / "pool.json").read_text(encoding="utf-8"))
    (REPO / "data").mkdir(exist_ok=True)
    (REPO / "data" / "candidates.json").write_text(json.dumps(
        [{"id": p["id"], "work": p["work"], "kind": p["kind"], "number": p["number"], "status": p["status"],
          "page": p["folio"], "location": p["running"]} for p in pool], ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    (REPO / "data" / "litcheck").mkdir(parents=True, exist_ok=True)
    for f in (HERE / "out" / "litcheck").glob("*"):
        if f.suffix in (".json", ".md") and f.name != "DIGEST.txt":
            shutil.copy2(f, REPO / "data" / "litcheck" / f.name)
    for f in ["refs-check.json", "REFS-CHECK.md", "QUOTE-GATE.md", "PAPER-GATES.md", "LEAN-GATE.md", "REVIEW-2.md",
              "REVIEW-3.md", "REVIEW-4.md", "REVIEW-5.md", "FIGURE-GATE.md", "ZENODO-FACTS.md"]:
        if (HERE / "out" / f).exists():
            shutil.copy2(HERE / "out" / f, REPO / "data" / f)
    # licence check: the three licence files are the published texts; every top-level directory is assigned in NOTICE;
    # the papers' declarations name both licences (author, 2026-10-28: code under Apache-2.0)
    lic = []
    for f, name in (("LICENSE", "CC-BY-4.0.txt"), ("LICENSE-CODE", "Apache-2.0.txt"), ("formal/LICENSE", "Apache-2.0.txt")):
        if (REPO / f).read_text(encoding="utf-8").rstrip("\n") != (HERE / "licences" / name).read_text(encoding="utf-8").rstrip("\n"):
            lic.append(f"{f} is not the text of {name}")
    notice = (REPO / "NOTICE").read_text(encoding="utf-8")
    for d in sorted(p.name for p in REPO.iterdir() if p.is_dir() and not p.name.startswith(".")):
        if d + "/" not in notice:
            lic.append(f"NOTICE does not assign {d}/")
    decl = (SRC / "declarations.md").read_text(encoding="utf-8")
    if "Apache License 2.0" not in decl or "CC BY 4.0" not in decl or "scripts" not in decl:
        lic.append("the declarations do not name both licences")
    if lic:
        raise SystemExit("licence check failed:\n" + "\n".join(lic))
    # leak scan: no local path, no private marker
    leaks = []
    for f in REPO.rglob("*"):
        if f.is_file() and f.suffix in (".md", ".py", ".json", ".yaml", ".toml", ".tex", ".lua", ".txt", ".cff", ".js",
                                        ".html", ".css", ""):
            t = f.read_text(encoding="utf-8", errors="replace")
            lines = [l for l in t.split("\n") if "LEAK" not in l and "for pat in" not in l]
            for pat in LEAKPATS:
                if pat in "\n".join(lines):
                    leaks.append(f"{f.relative_to(REPO)}: {pat}")
    if leaks:
        raise SystemExit("leak scan failed:\n" + "\n".join(leaks[:20]))
    n = sum(1 for _ in REPO.rglob("*") if _.is_file() and ".git" not in _.parts)
    print(f"repo: {n} files; {len(data)} problems in problems.json; Lean files {sorted(lean)}")


if __name__ == "__main__":
    main()
