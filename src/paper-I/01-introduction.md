# Introduction

A system that reasons about mathematics has to settle three questions before it settles any mathematical one: what it
stores, what it may assert, and who may turn an assertion into a result. The answers are usually left implicit. A
language model stores text and parameters, asserts whatever it generates, and leaves the third question to whoever
reads the output; a proof assistant stores declarations, asserts what its kernel has checked, and leaves open whether
the declarations say what was meant. Neither answer is adequate for a system that is to propose new mathematics at a
scale that exceeds what readers can check.

This paper states twelve theses on how mathematics and machine reasoning should be combined. They are drawn from the
seven works of the Grothendieckian Programme [@S01; @S02; @S03; @S04; @S05; @S06; @S07], released openly in October 2026
with an overview [@S00]. Two of the works design a reasoning system for mathematics; five apply one method of
discovery to five named problems and record what it establishes, what it reduces to stated hypotheses and what it
leaves open. The theses are the principles on which the seven works rest, stated so that they can be argued with
independently of the works.

Each thesis is given in five parts: the thesis in one sentence; an argument for it; the passages of the seven works on
which it rests, quoted from the published PDFs with their pages; its relation to existing work; and an observation that
would refute it. The last part is not a formality. Several theses are claims about what will work, and they can be
tested. This is the second of three papers released together. The first, *The Grothendieckian Programme: An
Overview* [@Liu26a], describes the architecture of the Programme, its five research subjects, its method and the series;
Section 2 below summarises what the theses need from it. The third, *The 57 Grothendieckian Problems* [@Liu26c], states
fifty-seven open problems drawn from the same works, and each thesis lists the problems at which it can be tested.

The theses fall into three groups. Theses 1–3 concern representation: what a reasoning system should store (worlds,
not isolated theorems), how the status of a statement should be recorded (as part of its type), and on what it should
reason (a structured, non-vectorial carrier). Theses 4–7 concern operation: attention rebuilt as descent, the
reporting of failure and abstention, the separation of operational completion from validity, promotion and
publication, and the separation of proposing from authorising. Theses 8–12 concern method: raising the theory around
a hard problem, stating what a result does not establish, recursive discovery, the creation of language, and the
judgment of a method by an open ledger.

Two limits apply throughout. First, the paper adds no mathematical result to the seven works, and none of the seven
claims a proof of the Riemann Hypothesis, the Birch and Swinnerton-Dyer conjecture, the Hodge conjecture, the $abc$
conjecture or the Langlands correspondence. Where a thesis is illustrated by one of the five research subjects, the
illustration is the record of a method, not a claim about the conjecture. Second, the seven works are first drafts that
have not been peer-reviewed, and much of the architecture they describe is specified but not implemented. A thesis that rests on a specification is a thesis about a design; Section 6 says which theses are affected and how.

Section 2 describes the seven works and states what they contain and what they do not. Section 3 relates the theses to existing work. Section 4 states the theses, and Section 5 shows how they depend on one another. Section 6 discusses the limits of the evidence and the ways in which the theses could fail, and Section 7 concludes.

# The source works

The seven works were released on Zenodo between 20 and 25 October 2026 and the overview on 26 October 2026, each with a
DOI, under the Creative Commons BY-NC-ND 4.0 licence, as Research Architecture Edition 1 of the WiseMotif Monograph of
Mathematical Intelligence. Together the seven comprise 34 volumes, 26,021 pages and 995 chapters. Counted by two
independent methods on their sources and on the sealed PDFs, and taking the smaller count where the two differ, they
contain more than 349,000 formulas, more than 10,500 numbered statements (theorems, propositions, lemmas, corollaries,
definitions and conjectures), 714 numbered algorithms and 1,434 numbered figures and plates [@S00]. Each work is
published with a signed list of checksums of its files. igref{works} draws the seven works as the seven cells of one
honeycomb, as the overview does [@S00, Figure 1]: the two works on the architecture at the centre and above it, the five
works on research subjects around them.

::: {.figure #fig:works file="fig-works" place="tbp"}
The seven works of the Grothendieckian Programme, as the seven cells of [@S00, Figure 1]. At the centre the core
[@S01]; above it, on a shared edge, the meta-reasoning kernel [@S02]; around them the five works on research subjects
[@S03; @S04; @S05; @S06; @S07]. Each cell gives the formula printed on the centre cell of the work's cover and the
number of pages of its sealed PDF. The short arrows across the shared edges are the three kinds of interface of
[@S00, Figure 1]; a port marks an interface, not a proof. The decomposition of the core drawn there is not repeated.
:::

## The architecture

*GAI-MUA: The Grothendieckian Machine* [@S01], in six volumes, sets out how mathematical worlds can be held by a machine
as typed, versioned objects and compared and transported between settings. Its first two volumes are mathematical:
schemes, topoi, descent, cohomology, motives, higher structures and their modern successors, with sources and hypotheses
recorded. The third specifies an architecture in two systems. The mathematical-universe system GMUS contains the
Motivic Unification Engine (MUE), a structured carrier for geometric, cohomological and realisation data; the Topos
Reasoning Engine (TRE), whose two engines propose new worlds and reason in admitted ones; and a source-audited
research lane (GRA). The language system GMLS contains a language forge for notation and theory, a contextual
cognitive layer, a descent workflow (GDRA) executed by capability-limited agents, and an experimental calculus
(AURORA). The remaining volumes specify algorithms, services and evaluation. In the words of its Series Note, the name
“names a research architecture, not a completed universal solver.” [@S01, p. iv]

*GM-Omega-Infinity: Topos-Native Intelligence* [@S02], in five volumes, states what a reasoning kernel must be if it is
to reason inside such worlds. A context is presented as a site, what it supports as a sheaf, and a conclusion as a
global section; the kernel covers, assigns, transports, glues, obstructs, decides by Kripke–Joyal forcing, and changes
base. The work proves a number of results on which its design rests — among them a dichotomy for the holonomy of
orthogonal cellular sheaves and an identity expressing the group-relative advantage of GRPO through a graph Laplacian
[@S02, §1.2.4] — and records its own position plainly: “the mathematics is written and partly proved, one finite
instance has been computed, and nothing has been trained or measured.” [@S02, §1.2.6, p. 23]

## The five research subjects

Each of the other five works takes one named problem as its research subject and applies to it the method that the
Series Notes call recursive mathematical discovery. *Arithmetic Spectral Descent* [@S03] takes the Riemann Hypothesis;
its recursion “ends in a proved conditional chain, twenty-three scoped obstructions, a certified computation stack, and
two obligations stated precisely enough to be attacked, rejected or falsified” [@S03, p. iv]. *Fractured Adelic
Geometry* [@S04] takes the conjecture of Birch and Swinnerton-Dyer and builds a framework from twelve axioms whose
consistency it does not prove; its table of output by status records zero cases of the conjecture established [@S04, Table 56.1, p. 437]. *The Archimedean Prism* [@S05] takes the Hodge conjecture; it records that the conjecture remains
open, that the book does not prove it, “and proves no case of it that was not already known.” [@S05, p. v]
*Strained Prismatic Geometry* [@S06] takes the $abc$ conjecture and publishes a census of its 1,420 statements by status [@S06, p. xvii]. *The Arithmetic Topos* [@S07] takes the Langlands programme and ends in a ledger of one hundred and eleven items, fifty-three of them conjectural [@S07, p. v]. None of the five claims a proof of its named problem.

## The method in the five works

The five works share a method and a discipline of reporting, set out in a common Series Note and applied to each
subject in its own way. A proposed structure is tested first against cases in which the answer is known. In
[@S03] the test is a firewall of four published counter-models — Davenport–Heilbronn functions, Beurling generalised
number systems, Selberg zeta functions with exceptional eigenvalues, Epstein zeta functions of class number greater
than one — and the rule is strict: “A mechanism is not admitted as a route to RH until the book explains why it fails,
or changes form, on all four objects.” [@S03, p. ix] In [@S07] the main conjecture is tested against the function-field
case, the de Rham limit, the local fields, the abelian case and the elliptic curve of conductor eleven [@S07, p. v].
What fails a test is kept: as a no-go theorem with explicit hypotheses in [@S03], as one of fourteen entries of an
obstruction atlas and twenty-two critical experiments with kill criteria in [@S06, p. v], and in
[@S05] as a falsifier. [@S05] closes with “eleven falsifiers, a self-assessment against seven criteria fixed in advance — four met, two
partially, one not met: a proof of the Hodge Conjecture — and sixty problems.” [@S05, p. vii]

Each work also states its claim boundary in its own words and prints a status with each statement. The notations
differ — seven codes in [@S01], grades of licence in [@S02], six labels in [@S06], five status marks in [@S07] — but the
rule is the same: no statement is printed at a strength greater than its support. The theses below take this
discipline as their subject.

## What the works do not contain

The works do not contain a running implementation of the architecture: the third volume of [@S01] is a specification,
and [@S02] reports no training run. Lean verification of the seven works is incomplete. They have not been reviewed by
others, and the author's declaration of the use of AI tools in their preparation is reproduced at the end of this
paper. The theses below therefore rest on the works as published texts — definitions, proved statements,
specifications and recorded failures — and not on any empirical result about a built system.

# Relation to existing work

The theses touch four bodies of work.

*Machine-guided mathematical discovery.* Machine learning has been used to suggest conjectures that mathematicians
then proved [@Davies2021]; program search guided by language models, with an external evaluator, has produced new
constructions in combinatorics [@RomeraParedes2024]; a neuro-symbolic system has solved olympiad geometry problems
[@Trinh2024]; and automated conjecturing has a longer history, from Graffiti [@Fajtlowicz1988] to systems that
propose formulas for fundamental constants [@Raayoni2021]. In these systems the evaluator — a proof, a verified
construction or a numerical test — stands outside the generator. Theses 6, 7 and 10 make the same separation a
requirement of the architecture, and extend it to the status of every intermediate artefact and to the record of
failures (Thesis 10).

*Formal verification.* The de Bruijn criterion — that proofs found by any means be checked by a small trusted kernel —
underlies the proof assistants now used in research mathematics [@BarendregtWiedijk2005; @deMouraUllrich2021], and large libraries such as Mathlib have made it possible to state much research mathematics formally [@mathlib2020]. The Liquid
Tensor Experiment showed that recent research-level results can be formalised [@Scholze2022]. Public collections of
formally stated open problems are used as benchmarks [@FormalConjectures2026], and autoformalization has made the
fidelity of a formal statement to its informal source a measured quantity [@Wu2022]. Avigad describes the turn of
mathematics toward formal methods [@Avigad2024]. Theses 2 and 6 take from this tradition the separation of checking
from search, and add two things it does not by itself provide: a status for artefacts that are not proofs, and a
separate obligation of fidelity between a formal target and the mathematics it is meant to express.

*Structured representations in machine learning.* Geometric deep learning builds the symmetries of a domain into a
network [@Bronstein2021]; categorical deep learning proposes algebraic theories of architectures [@Gavranovic2024];
cellular sheaves and sheaf neural networks attach structured stalks and restriction maps to graphs
[@HansenGhrist2019; @HansenGebhart2020; @Bodnar2022]; and topos-theoretic designs for language models have been
proposed [@Mahadevan2025]. Results on the circuit complexity of transformers bound what a fixed-depth attention
network can compute [@MerrillSabharwal2023]. Theses 3 and 4 belong to this line. They differ from it in asking that
gluing and obstruction be outputs of the kernel rather than regularisers, and in grading every architectural claim by
what has been shown.

*The practice of mathematics.* Jaffe and Quinn proposed that speculative mathematics be labelled as such
[@JaffeQuinn1993], and the replies, among them Thurston's account of proof as understanding communicated between people
[@Thurston1994], concerned what a label must carry. Lakatos described how concepts change under proofs and refutations
[@Lakatos1976]; Grothendieck's image of the rising sea is studied by McLarty [@McLarty2007]. In October 2026 a
repository for research works in the mathematical sciences was announced that accepts works generated entirely by
language models and records, for each, the extent of machine generation and of human understanding [@Antieau2026].
Theses 2, 7, 9 and 12 are proposals within this discussion.
