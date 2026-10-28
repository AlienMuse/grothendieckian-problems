# Round 5 (2026-10-28): the overview paper, the three papers as one set, and the page check

The author's instruction: add a third paper in the same form and to the same standard — at most ten pages — that sets
out the Grothendieckian Programme, the open series and the research plan clearly and accurately; title A, *The
Grothendieckian Programme: An Overview — Seven Open Works on Mathematics and Machine Reasoning*; research plan as
option 甲 (only what is public: no dated commitments); the overview first, then *The Rising-Sea Theses*, then *The 57
Grothendieckian Problems*, the two earlier papers adapted to cite it.

## The overview paper

| Item | Result |
|---|---|
| Length | 10 pages including declarations and references (gate `pages · overview`); about 2,180 words of text, Table 1, three figures, 21 references (13 outside the works) |
| Sections | 1 Introduction; 2 The architecture (core, kernel, interfaces); 3 The five research subjects (Table 1: key change, where the recursion ends, boundary in each work's words); 4 The method and its discipline; 5 The series and its records; 6 Research plan and taking part; 7 Limits; declarations; references |
| Figures | 1 the seven works (the honeycomb of paper I, Figure 1); 2 recursive mathematical discovery, with what each work keeps of what fails and the status labels of the seven works; 3 the series and its records — the eight works by release date with size, concept DOI and repository, the three papers and the repository of the problems |
| Sources | 37 quotations, each checked on its page; every number of Section 5 from `programme.yaml` (`render_overview.py`), and the eight Zenodo records read back: concept DOI, version 1.0.0, date, licence, community, ORCID (`tools/zenodo_facts.py` → `ZENODO-FACTS.md`, ALL PASS) |
| Core decomposition | Not drawn (D5): the systems are named with their components as in paper I §2 |

## Editorial rounds on the overview

| # | Finding | Change |
|---|---|---|
| 1 | "every Series Note states the same rule" — the rule is in the Series Notes of the five research subjects only | Stated so, with two citations |
| 2 | "Each work changes the object of study rather than the argument" — four Series Notes say so, each of something else (the bridge, the argument, the inequality, the statement); the third replaces a positivity condition by an index condition | Stated so, with five citations; Table 1's column renamed *The key change* |
| 3 | The four labels of S04 were cited only to S04 | Cited to S04 and S05 |
| 4 | The open items of S01 and S02 had no citation | Cited |
| 5 | The abstract could be read as giving 34 volumes and 26,021 pages to the seven works and the overview together | The totals attached to the seven works |
| 6 | "four bodies of existing work" listed three | The fourth (structured representations, sheaf neural networks) named and cited |
| 7 | This paper is *An Overview* and Series 00 is "the overview" elsewhere: ambiguous | Series 00 is "the overview volume" throughout this paper, its declarations and Figure 3 |
| 8 | "they apply to every work" (the three kinds of contribution) was this paper's own extension | Attributed to the overview volume |
| 9 | "Every claim carries a licence grade" — the grades are attached to the claim ledger | "Every claim in its claim ledger" |
| 10 | "No date is attached to the next editions; they follow from what review finds" (a forecast) | "No date is set for the next editions." |
| 11 | The AI declaration said the author "selected the theses and problems" — not this paper | "the author reviewed every statement"; the data statement names what this paper's repository holds |

## The three papers as one set

- Paper I (*The Rising-Sea Theses*) and paper II (*The 57 Grothendieckian Problems*) each say in their introduction that
  they are the second and third of three papers and what the first contains; "the companion paper" (ambiguous with
  three) is replaced by the title of the paper meant, in the text, in the theses' *Problems* field, in Figure 2 of
  paper I and in the description of the card in paper II and its Figure 3. Nothing else in them changes.
- New gate `numbers · three papers`: the series' totals, wherever any of the three prints them, are those of
  `programme.yaml` (22 printed totals).
- The repository holds the three papers, the overview first; `src/overview/`, `render_overview.py` and
  `zenodo_facts.py` are added.

## A page check made strict (papers I and II)

Writing the overview, one page reference was found to be one page early: S02 §1.2.6 begins on p. 22 and the quoted
sentence is on p. 23. `quote_gate` had allowed a quotation to be found on the page after the one cited, so that a
sentence crossing a page break would pass; it also let pass a quotation that lies wholly on the next page. The gate now
allows the next page only for a quotation that begins on the named page. It found 31 quotations, all in papers I and II,
that lie wholly on the page after the one cited (the quoted words were right; the page was not):

- 14 cards (2, 4, 7, 8, 11, 14, 20, 21, 22, 28, 29, 43, 50, 54): the Source of each now prints the range, for example
  "§75.17, pp. 9503–9504", and the card's pages include the page of the quotation;
- 2 evidence items of Theses 3 and 4: their pages corrected (pp. 8250–8251; p. 23);
- 2 citations in the text of paper I: S02 §1.2.6, p. 22 → p. 23; S01 Vol. III, p. 8217 → p. 8218.

At the same time an evidence item's page goes into its last citation instead of a second bracket ("[S01, Vol. III,
§15.4, pp. 8250–8251]", not "[S01, Vol. III, §15.4] [S01, p. 8250]").

## A figure check added

A new check of the figures finds two lines of text that run into each other (their boxes overlap). It found the
overview's Figure 1 title against its right-hand label and three cases in figures of papers I and II (a column title
of Figure 3 of paper I, a label and a check mark in Figure 5 of paper I, a name and a size in Figure 3 of the overview);
all moved apart. Thirteen figures, ALL PASS.

## Gates after round 5

Quotations 263/263 on the named page (strict); references 121/121; `paper_gates` ALL PASS on the three PDFs (with
`pages · overview` 10 and `numbers · three papers`); `lean_gate` ALL PASS; figures 13/13 ALL PASS; Zenodo read-back
8/8; no overfull line, no missing glyph. Overview 10 pages, paper I 26, paper II 54. Repository 298 files.
