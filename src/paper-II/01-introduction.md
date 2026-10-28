# Introduction

In a mathematical conversation, someone suggested to Grothendieck that they should consider a particular prime number;
asked whether that meant an actual number, and told that it did, Grothendieck answered “All right, take 57.” Allyn
Jackson tells the story as “the legend of the so-called “Grothendieck prime””, to illustrate how little his thinking
relied on examples [@Jackson2004, pp. 1196–1197]. Fifty-seven is $3 \times 19$. We take the title of this paper from
the story for a second reason as well: a list of problems drawn from first drafts will contain errors of its own, and
the place to report them is given with every problem below.

The fifty-seven problems are drawn from the seven works of the Grothendieckian Programme
[@S01; @S02; @S03; @S04; @S05; @S06; @S07], with the overview [@S00]. The works were released on Zenodo between 20 and 25
October 2026, under a CC BY-NC-ND 4.0 licence, as a Research Architecture Edition. Together they comprise 34 volumes and
26,021 pages. They are first drafts and have not been peer-reviewed. The first two works are on the architecture of
a reasoning system for mathematics: *GAI-MUA: The Grothendieckian Machine* [@S01] treats mathematical worlds as typed,
versioned objects that can be compared and carried from one setting to another, and *GM-Omega-Infinity: Topos-Native
Intelligence* [@S02] builds a reasoning kernel on sites, sheaves and descent. The other five works each take a research
subject — the Riemann Hypothesis, the conjecture of Birch and Swinnerton-Dyer, the Hodge conjecture, the $abc$
conjecture and the Langlands programme — and record what a single method, carried out in full, establishes about it,
what it reduces to stated hypotheses, and what it leaves open. None of the seven works claims a proof of any of these
conjectures, and none of the problems below is one of them.

This is the third of three papers released together. The first, *The Grothendieckian Programme: An Overview* [@Liu26a],
describes the architecture of the Programme, its five research subjects, its method and the series. The second,
*The Rising-Sea Theses* [@Liu26b], states twelve theses on mathematics and machine reasoning drawn from the same works. Each
problem below is attached to one thesis; the problems are the points at which the theses can be tested. \figref{rose} shows the fifty-seven problems in the seven works, with their kinds and levels.

::: {.figure #fig:rose file="fig-rose" place="p"}
The fifty-seven problems in the seven works, in the honeycomb of [@S00, Figure 1]: Problems 1–35 (Part I) from [@S01]
and [@S02], Problems 36–57 (Part II) from the five works on research subjects. Within each work the problems are
grouped by kind; the dots under a number give its level (one: entry, two: research, three: programme). Each small cell
links to its card.
:::

## Selection

The seven works state many items as open, conditional, conjectural or owed. We extracted them by script from the sealed
PDFs, using the status notation of each work: {n_pool} items in all ({n_pool_works}). From these we selected
fifty-seven by four rules (\figref{selection}); the list of extracted items, with work, number, status and page, is
in the repository.

::: {.figure #fig:selection file="fig-selection" place="tbp"}
How the problems were chosen: the items extracted from the seven works, the four rules below, the literature check of
Section 1.3, whose changes are listed in Appendix B, and the problems by part and by kind.
:::

1. *The problem is stated in the source.* Each problem is an open problem, conjecture, obligation, falsification test or question printed in one of the seven works, and the card quotes the source wherever it gives the source's words. Where the problem below
   narrows or makes precise the source's statement, the card says so.
2. *The problem is not a named conjecture.* The Riemann Hypothesis and its generalisations, the conjecture of Birch and
   Swinnerton-Dyer, the Hodge, standard, Tate, $abc$, Szpiro and Vojta conjectures, Grothendieck's section conjecture
   and the Langlands correspondence appear in the cards only as background. A problem whose solution would by itself
   prove one of them is excluded. So are problems that turn on the disputed step of inter-universal Teichmüller theory,
   on which the sources record a disagreement without adjudicating it [@S06].
3. *The problem is open as far as we can determine.* Every problem was checked against the literature on 28 October
   2026 (see below). Seven candidates were changed as a result: five were replaced by other problems from the same works and two were
   narrowed; the changes and their reasons are listed in Appendix B.
4. *The problem has a decision criterion.* Each card states what counts as a solution, so that a solution can be
   checked by someone other than its author and other than us.

Thirty-five problems come from the two architectural works and twenty-two from the five research subjects, four or five from each. By kind, {n_math} are mathematical problems, {n_machine} are *machine problems* — a system to be built or an experiment to be run, with its success criterion fixed in advance —
and {n_formal} are formalization problems. {n_entry} are marked *entry level*: a solution needs no new theory. {n_research} are *research level*. {n_programme} are marked *programme level*: they are the problems on which the respective work depends as a whole.

## What a card contains

Each problem is given in a fixed format. The heading of a card gives the number and title of the problem, its kind
and its level. *Thesis* names the thesis of *The Rising-Sea Theses* to which the problem belongs. *Source* names the work, the place in it and the page of the sealed PDF; the page is the
printed folio. *Status in the source* is the status that the source assigns, in its own notation. *Statement* states the problem.
*What the source establishes* records what has been proved or specified, and what the source itself says about the
gap. *Proposed by* names the source of the problem and, where the problem or its subject has an earlier origin, that
origin. *Background* cites the standard literature on which the problem rests. *Solved when* states the decision
criterion. *Literature check* records what the check of 28 October 2026 found. \figref{card} shows the card of Problem 49 in this
format.

::: {.figure #fig:card file="fig-card" place="tbp"}
What a card contains, with the card of Problem 49 as the example: on the left the heading and the first words of each
field, on the right what each field records. Below, what is published with every card.
:::

The words between quotation marks in a card are those of the source, on the pages named; this has been checked by
machine for every quotation. A quotation from a work of the Programme is not a claim of this paper that the quoted
statement is correct.

## The literature check

For each problem we ran two or more search strings against arXiv, OpenAlex, zbMATH Open and Crossref, and, for the
formalization problems, a code search of the Lean 4 repository, of Mathlib and of the Formal Conjectures collection
[@FormalConjectures2026]; we then read the results that bore on the problem. The searches, their dates and their first
results are published with the paper. A search can show that something exists; it cannot show that nothing exists. The
check is therefore scoped to what was searched, and a problem that turns out to have been answered elsewhere will be
recorded as such. One finding is a correction to a source: a construction that [@S03] describes as unknown has been published (Problem 38); it is recorded in the errata of the repository. The check also narrowed Problem 34 to what remains open, since independent checkers for Lean 4 now exist.

## Participation and credit

A solution, a partial result, a counterexample to a problem as stated, a report that a problem is already solved, or a
correction to a card is submitted through the repository of the paper. Each problem has its own discussion thread,
named in its card. A solution that meets the criterion of its card is recorded in the next version of this paper and
in the next edition of the work from which the problem comes, under the solver's name, and in a list of solutions kept
with the repository. No prize is attached to any problem (\figref{credit}).

::: {.figure #fig:credit file="fig-credit" place="tbp"}
Participation and credit: what can be submitted, where, how it is checked, and where a solution and a correction are
recorded.
:::

The cards and a machine-readable file of all fifty-seven problems are released under CC BY 4.0, and the statements of
the formalization problems in Lean 4, with the scripts that produced and checked this paper, under Apache-2.0, so that
they can be translated, adapted and used as a benchmark. The seven works keep their own licence, and the quotations from them are reproduced under it with attribution.
