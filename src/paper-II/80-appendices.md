```{=latex}
\clearpage
```

# Appendices {.unnumbered}

## A. The problems by thesis and by work {.unnumbered}

\figref{matrix} places each problem by its thesis and its work. The first table below lists the problems of each thesis, the second counts the problems of each work by kind.

::: {.figure #fig:matrix file="fig-matrix" place="here"}
The problems by thesis and by work. Each small cell is a problem, tinted by kind and linked to its card; the totals are by row and by column.
:::

| Thesis | Problems |
|---|---|
| 1. Worlds, not isolated theorems | 4, 15 |
| 2. Status is part of the type | 7, 8, 31 |
| 3. A structured latent space | 6, 18 |
| 4. Attention as descent | 19, 20, 22, 24, 25, 27, 28, 35 |
| 5. Report failure; abstain without evidence | 9, 16, 17, 21, 23, 30, 32, 47 |
| 6. A chain of non-implications | 5, 12, 26, 29, 34 |
| 7. Machines propose; humans authorize | 10, 11 |
| 8. The rising sea | 1, 36, 37, 38, 41, 51, 52, 55, 56 |
| 9. State what is not established | 33, 39, 40, 43, 44, 45, 48, 49, 53, 54 |
| 10. Discovery is recursive | 2, 3 |
| 11. Creating language | 14, 57 |
| 12. Judge a method by its open ledger | 13, 42, 46, 50 |

| Work | Problems | Mathematical | Machine | Formalization |
|---|---|---|---|---|
| S01 | 1–17 | 0 | 10 | 7 |
| S02 | 18–35 | 9 | 6 | 3 |
| S03 | 36–39 | 3 | 1 | 0 |
| S04 | 40–43 | 3 | 1 | 0 |
| S05 | 44–48 | 4 | 0 | 1 |
| S06 | 49–52 | 2 | 1 | 1 |
| S07 | 53–57 | 4 | 0 | 1 |
| All | 1–57 | 25 | 19 | 13 |

## B. Changes made by the literature check {.unnumbered}

The selection approved before the literature check was changed in seven places. The replaced problems are listed so that the reasons can be checked.

| Problem | Approved candidate | Change and reason |
|---|---|---|
| 26 | Robust exact group scan [S02, Open Problem 2.14.C] | Replaced by Question 11.11.18 of [S02]. Without the numerical setting of [S02, Ch. 2.14], the problem reduces to multiplying permutation matrices, which floating-point arithmetic performs exactly; stated on its own it would be misleading. |
| 34 | A second kernel [S02, Open Problem 13.15.D] | Narrowed and moved to entry level. Independent type checkers for Lean 4 exist [Car24; nanoda]; the remaining task is to replay the declarations of [S02] under two of them. |
| 38 | Pin(2)-twisted topological Hochschild homology [S03, Problem 28.13] | Narrowed. The first question of the source, whether a Pin(2)-equivariant lift of THH exists, has been answered by quaternionic THH [AMP26]; the second question is kept. The source’s statement that no construction is known is listed in the errata. |
| 39 | A certified finite-height computation [S03, Problem J.38] | Replaced by falsification predicate F2 [S03, Criterion 58.9]. Certified computation of the zeros of the zeta function to great height is established [PT21], and the source’s problem asks for a computation of a related kind with no decision criterion beyond it. |
| 40 | The Construction Problem [S04, Problem 54.1.1] | Replaced by Problem 22.7.1 of [S04]. The source records that its axiom F12 carries essentially the whole arithmetic content of the conjecture of Birch and Swinnerton-Dyer [S04, Remark 56.2.1], so the original would fall under the exclusion of problems whose solution proves a named conjecture. |
| 45 | The certification boundary [S05, Problem 71.9.3] | Replaced by Problem 71.3.4 of [S05]. In the form stated, the impossibility of certifying a relation from finite-precision data follows from the undecidability of equality of computable real numbers, a standard result of computable analysis. |
| 47 | The Rigidification Conjecture in rank two [S05, Problem 71.6.3] | Replaced by Problem 71.3.3 of [S05]. The relation of the rank-two case to known results, including the Lefschetz (1,1) theorem, needs an expert reading before it can be posed as open. |

## C. The machine-readable file {.unnumbered}

`problems.json` in the repository contains, for each problem, the fields of its card and the identifiers of its source (work, DOI, pages, status), its thesis, its kind and level, the date of its literature check and the path of its Lean statement where one exists. The file is generated from the same source as this paper, and the two are checked to agree field by field.

# Declarations {.unnumbered}

**Use of AI tools.** The main ideas and the architecture of the Grothendieckian Programme are the author's and come
from the author's research at WiseMotif.ai. In the seven works, AI tools assisted with drafting and with part of the
literature collation; all of the text was reviewed by the author. Lean verification of the seven works is incomplete.
Because of their size, the works are first drafts (Research Architecture Edition 1) and have not been peer-reviewed;
they need review by experts and further work on the programme. They are released openly for that purpose, in the hope
of further contributions and of more recursive mathematical discovery in AI for mathematics. For the present paper,
statements were extracted from the published works by script and checked against the PDFs; AI tools assisted with
drafting and with literature collation; the author selected the theses and problems and reviewed every statement.

**Funding and competing interests.** No external funding. The author is affiliated with WiseMotif.ai.

**Data availability.** The source texts are the sealed PDFs of the seven works and of the overview, each with a Zenodo
DOI given in the references. The extraction scripts and the list of extracted items, the record of the literature
check, the reference check, the Lean statements, the figures with their data and sources, and the machine-readable file
of the paper are in the repository
<https://github.com/AlienMuse/grothendieckian-problems>.

**Licence.** This paper, its figures and its data are released under the Creative Commons Attribution 4.0
International licence (CC BY 4.0); the code in the repository — the Lean files, the scripts and the source code of the
figures — under the Apache License 2.0. The seven works and the overview are released under CC BY-NC-ND
4.0, and the quotations from them in this paper are reproduced under that licence with attribution.

**Name.** The adjective *Grothendieckian* names a mathematical method used in the seven works. It carries no attribution
of design or endorsement to Alexander Grothendieck or to any other mathematician whose work is cited; no problem in this
paper was posed by Grothendieck unless the card says so.

