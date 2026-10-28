# Round 4 (2026-10-28): layout, figures, and what building the figures found

The author's instructions: remove the author's location from the papers; bring the title and layout to the standard of
the leading journals; add figures in the design of the series (D6 honeycomb, AURORA), drawn only from published
content. The plan (`../PLAN-LAYOUT-FIGURES.md`) was approved as recommended.

## Changes made at the author's instruction

| # | Item | Change |
|---|---|---|
| 1 | Address | Both papers: affiliation "WiseMotif.ai" only. Also removed from `programme.yaml` and from the site (21 pages: footer, About, schema.org `workLocation`); site rebuilt, its ten checks pass, staged for the author's push |
| 2 | Title block | Title 17 pt bold in mixed case (was 10.9 pt capitals, the size of the text); subtitle 12 pt italic; author in small capitals; affiliation, e-mail and ORCID iD on the first page (were at the end); a line with version, date and licence above (DOI from S4) |
| 3 | Measure | 150 → 132 mm (about 78 characters a line, was 88) |
| 4 | Headings | Bold, flush left; the parts of paper II centred between hairlines, each on a new page |
| 5 | Cards | Heading line with number, title and, on the right, kind and level; the field *Kind* became *Thesis*; bars beside *Statement* and *Solved when*; a hairline between cards; a heading never ends a page |
| 6 | Theses | The one-sentence thesis framed under its heading |
| 7 | Links | Visible, in the darkest teal of the AURORA scale |
| 8 | Figures | Ten, five in each paper (`../figures/`), 132 mm wide, light layer 605 ppi, all text searchable |

## Findings and fixes

| # | Finding | Fix |
|---|---|---|
| 1 | Every unnumbered heading appeared twice in the PDF bookmarks (amsart and Pandoc both wrote a contents line) | The filter sets unnumbered headings itself; 57 card bookmarks added under parts and works |
| 2 | The introduction of paper II says each problem was searched with two or more strings; Problems 15–17 had one each | A second string for each, run; arXiv refused some requests (HTTP 429), so they were run again slowly (`tools/litcheck_retry.py`) until answered |
| 3 | OpenAlex had refused 21 searches (HTTP 429) for Problems 26, 39, 45, 47 and 49–57, although the paper says every problem was searched there | All 21 run again and answered; every result read |
| 4 | From finding 3: a certification rule and interval factorization for other truncations of the Weil quadratic form (Groskin 2026) bears on Problem 39 | Cited in its background and literature check, with what it does not cover (the sixty-three test spaces of the source) |
| 5 | From finding 3: Altuğ's first step has been extended to totally real fields (Emory, Espinosa-Lara, Kundu, Wong 2024) | Cited in Problem 54 |
| 6 | Problem 57 credited "coherence and decidability results" to GKNB21, which contains neither; decidability is Gratzer's normalization theorem (LICS 2022), which reduces conversion to the mode theory — the part the problem asks for | Literature check rewritten and Gratzer 2022 cited; references 118 → 121, all read back |
| 7 | Paper II said "more than a thousand items" were extracted | The number, 1,040, with each work's share; the list (identifiers, status, page; no text) is now in the repository (`data/candidates.json`) |
| 8 | Paper II, Section 1.1, rule 3 said twice that the changes are in Appendix B | Once |
| 9 | Appendix A said its two tables "give the same data" as the figure | They do not: the sentence now says what each table gives |
| 10 | Under simulated protanopia the blue and violet accents differ by ΔE 4 | Categories use blue, cyan and gold (least ΔE 25 under protanopia, deuteranopia and tritanopia), each with a second, non-colour mark |
| 11 | The sign ⇏ in a semibold label was emboldened synthetically by Chrome, as a Type 3 font | Set in the regular mathematics face; the figure gate rejects Type 3 |
| 12 | Three figures printing at once could print before the light layer or the faces had loaded (a 12 pt page; a page without text) | Every print is checked for image and text and printed again if incomplete |
| 13 | The figure of Appendix A floated four pages past its reference (the long tables) | The appendices begin a page; the figure stands where it is cited |
| 14 | Data availability did not name the figures or the list of extracted items | Both named |
| 15 | The figure PDFs (65 MiB) would have been duplicated in the repository | The repository keeps a PNG of each and the sources; 76 MiB |

## New gate

`tools/figures.py` → `FIGURE-GATE.md`: every phrase a figure prints occurs in its source (94 phrases); every drawn line
is searchable in the figure's PDF; page 132 mm wide; light layer ≥ 600 ppi, lossless; no Type 3; only Segoe UI and the
TGP faces; type ≥ 6.5 pt, nothing condensed or overflowing; "FIGURE n" equals the figure's place in its paper; category
colours apart under simulated colour-vision deficiency; every link target is a label of the paper.
