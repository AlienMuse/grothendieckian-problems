# Introduction

A system that reasons about mathematics must settle what it stores, what it may assert, and who may turn an assertion
into a result. The Grothendieckian Programme is a series of works that answers these questions by design and then
tests the answers on hard problems. The Series Note of its five research subjects states the aim in one sentence: “The Programme has a single
research aim: machine intelligence that discovers mathematical structure on its own account.” [S03, p. iv] The
method is modelled on Grothendieck’s image of the rising sea [McL07]: “A hard problem is not attacked where it
stands; a theory is raised around it until the problem becomes natural and gives way.” [S03, p. iv]

The Programme consists of seven works and an overview volume [S00], released on Zenodo between 20 and 26 October 2026
(\figref{programme}). Two of the works specify a reasoning architecture. The other five each take one named problem
as research subject and record what the method establishes about it, what it reduces to stated hypotheses and what it
leaves open. The works sit beside four bodies of existing work: machine-guided discovery, in which an external
evaluator stands outside the generator [DVB+21; RBN+24; TWL+24]; formal verification under the
de Bruijn criterion [BW05], with Lean and Mathlib [MU21; mC20] and public
collections of formally stated open problems [FLM+26]; structured representations in machine learning,
among them sheaf neural networks [HG19; BDCLB22]; and the practice of mathematics, from proofs and
refutations [Lak76] to the debate on how speculative mathematics should be labelled [JQ93; Thu94].

This paper describes the Programme as published: the architecture (Section 2), the five research subjects
(Section 3), the method and its discipline of reporting (Section 4), the series and its records (Section 5), the
research plan and the ways to take part (Section 6), and the limits of what has been done (Section 7). It is the first
of three papers released together. The second, *The Rising-Sea Theses* [Liu26b], states twelve theses on which the works rest,
each with the passages that support it and an observation that would refute it. The third, *The 57 Grothendieckian
Problems* [Liu26c], states fifty-seven open problems drawn from the works, each with a criterion that decides when it is
solved. This paper adds no mathematical result to the works, and none of them claims a proof of the Riemann
Hypothesis, the conjecture of Birch and Swinnerton-Dyer, the Hodge conjecture, the $abc$ conjecture or the Langlands
correspondence.

::: {.figure #fig:programme file="fig-programme" place="tbp"}
The seven works of the Grothendieckian Programme as the seven cells of one honeycomb [S00, Figure 1]. At the centre
the core [S01]; above it, on a shared edge, the meta-reasoning kernel [S02]; around them the five works on research
subjects [S03; S04; S05; S06; S07]. Each cell gives the formula printed on the centre cell of the work’s cover
and the number of pages of its sealed PDF. The short arrows across the shared edges are the three kinds of interface;
a port marks an interface, not a proof.
:::

# The architecture

*The core.* *GAI-MUA: The Grothendieckian Machine* [S01] is a work in six volumes with two stated obligations. The
mathematical one is to explain schemes, topoi, descent, cohomology, motives and higher structures “with exact
hypotheses and source-aware proof lineage”; the architectural one is “to express mathematical worlds as typed,
versioned, provenance-bearing artifacts that can be searched, compared, formalized, computed with, and evolved without
allowing statistical confidence to masquerade as proof.” [S01, p. iv] Volumes I and II carry the first obligation.
Volume III specifies the architecture in two systems. The mathematical-universe system GMUS contains the Motivic
Unification Engine (MUE), a structured carrier for geometric, cohomological and realisation data; the Topos Reasoning
Engine (TRE), whose two engines propose new worlds and reason in admitted ones; and a source-audited research lane
(GRA). The language system GMLS contains a language forge for notation and theory, a contextual cognitive layer, a
descent workflow (GDRA) executed by capability-limited agents, and an experimental calculus (AURORA). Volumes IV–VI
specify algorithms, services and evaluation. The work distinguishes seven kinds of statement — “Established
mathematics, structural synthesis, proposed definitions, research programs, conjectures, proof obligations, and
disputed claims” — and admits a theorem to the established layer “only with a checked statement, complete hypotheses,
an exact locator, and a recorded dependency closure.” [S01, p. iv]

*The kernel.* *GM-Omega-Infinity: Topos-Native Intelligence* [S02], in five volumes, states what a reasoning kernel
must be if it is to reason inside such worlds. A context is presented as a site, what it supports as a sheaf and a
conclusion as a global section; the kernel covers, assigns, transports, glues, obstructs, decides by Kripke–Joyal
forcing and changes base. Every claim in its claim ledger carries a licence grade and a falsification condition [S02, §1.2.6, p. 22].
Among the results on which the design rests are a dichotomy for the holonomy of orthogonal cellular sheaves
[S02, §1.2.4] and an identity: the advantages used by group-relative policy optimisation (GRPO) are the degree-zero
Laplacian of the rollout nerve applied to the reward [S02, Preface, p. xiv]. The work states its position once:
“It has several proved local specialisations and no proved global subsumption or replacement result.” [S02, p. xxvii] And it states what has been done: “the mathematics is written and partly proved, one finite instance has
been computed, and nothing has been trained or measured.” [S02, §1.2.6, p. 23]

*Interfaces.* In \figref{programme} the kernel sits above the core on a shared edge, because it reasons over the
worlds the core holds. Three kinds of interface cross the shared edges: worlds and their transports leave the core;
descent reasoning and verification come from the kernel; obstructions, new structures and new conjectures return to
the core [S00, Figure 1]. A port on an edge marks an interface, not a proof: nothing that crosses it is promoted by
crossing.

# The five research subjects

Each of the other five works is a self-contained system and one research subject of the Programme, that is, “a
problem on which this method is carried through in full, with every step recorded in a form that a mathematician can
check and a machine can execute.” [S03, p. iv] Four of them say that the recursion changes the object rather
than the bridge, the argument, the inequality or the statement [S04, p. v; S05, p. v; S06, p. v; S07, p. v]; the
first replaces a positivity condition by an index condition [S03, p. xv]. Each tests its steps against the cases in
which the answer is known and ends by stating where the recursion stops. Table 1 gives, for each, the key change, the
state in which the recursion ends, and the boundary of the work’s
claims in its own words. The open items in its third column are the starting points of Section 6.

::: {.small}
| Work and subject | The key change | Where the recursion ends | Boundary, in the work’s words |
|:---------------|:-----------------------|:----------------------------|:-------------------------|
| *Arithmetic Spectral Descent* [S03]: the Riemann Hypothesis | “the replacement of a positivity condition by an index condition” [S03, p. xv]; four published counter-models test every mechanism | “a proved conditional chain, twenty-three scoped obstructions, a certified computation stack, and two obligations stated precisely enough to be attacked, rejected or falsified” [S03, p. iv] | “The Riemann Hypothesis remains open. This work does not claim a proof of it, of the generalized Riemann hypotheses, or of any equivalent statement.” [S03, p. iv] |
| *Fractured Adelic Geometry* [S04]: the conjecture of Birch and Swinnerton-Dyer | one arithmetic spectrum with one determinant line; the conjecture as “the agreement of the line’s two trivialisations” [S04, p. v] | “a register of twelve conjectures with stated difficulty, an atlas of fourteen obstructions with attack plans, a computational and formal-verification architecture, and a staged construction programme with explicit criteria for abandonment” [S04, p. v] | “The Birch and Swinnerton-Dyer conjecture remains open. This work does not prove it, proves no case of it that was not already known” [S04, p. v] |
| *The Archimedean Prism* [S05]: the Hodge conjecture | algebraicity as “a descent datum that a class carries along a prism” [S05, p. v] | “a master equivalence of five formulations, a ledger of nine obstructions of which exactly two are live, a computational and formal-verification architecture, eleven named falsifiers, and sixty problems” [S05, p. v] | “The Hodge conjecture remains open. This work does not prove it, and proves no case of it that was not already known.” [S05, p. v] |
| *Strained Prismatic Geometry* [S06]: the $abc$ conjecture | a substrate over which $\operatorname{Spec}\mathbb Z$ “acquires a relative cotangent direction”, bad reduction read “as strain in that direction” [S06, p. v] | Theorems A and B, “both conditional on a named ledger of ninety-eight obligations”; Theorem C, “an unconditional categorical theorem of trace invariance” [S06, p. v]; fourteen obstructions; twenty-two critical experiments | “The $abc$ conjecture remains open. This work does not prove it.” [S06, p. vi] |
| *The Arithmetic Topos* [S07]: the Langlands programme | a global arithmetic curve carrying “a six-functor formalism with a primitive trace” [S07, p. v] | “a statement ledger of one hundred and eleven items, twenty-eight axioms and eighty-three entries, fifty-three of them conjectural” [S07, p. v]; seventeen falsification tests; four gaps of the first rank of difficulty; fourteen research problems in dependency order | “This work does not prove the Langlands correspondence, and no case of its Main Conjecture is established unconditionally in it” [S07, p. vi] |

: The five research subjects. Quotation marks enclose the words of the work on the page cited.
:::

# The method and its discipline

The method is called recursive mathematical discovery. In the words of the Series Note, “a proposed structure is
tested, what survives the test is abstracted into a new setting, and the question is posed again in that setting.”
[S03, p. iv] \figref{method} draws the cycle. The tests are fixed before the construction is judged: four published
counter-models for every mechanism proposed for the Riemann Hypothesis [S03, p. iv]; divisors, dimension at most
three, cubic fourfolds and abelian surfaces for the Hodge conjecture [S05, p. v]; the function-field case, the
de Rham limit, the local fields, the abelian case and the curve of conductor eleven for the Langlands programme
[S07, p. v].

What does not survive a test is kept, in a form that can be used again. In [S03] “A mechanism that failed for a
structural reason became a no-go theorem” [S03, p. iv]; in [S04] and [S05] what fails “is recorded as an
obstruction” [S04, p. v]; in [S06] “What fails is recorded as a proof obligation.” [S06, p. v]; in [S07] “What
fails is recorded where it fails.” [S07, p. v]

Every work prints a status with each statement, and the Series Note of each of the five research subjects states
the same rule: “No result is presented at a strength greater than its proof.” [S03, p. iv; S07, p. vi] The notations differ. [S01] distinguishes the seven kinds of
statement quoted above; [S02] grades the licence of each claim; [S03] marks every substantive claim with one of six
labels [S03, p. v]; [S04] and [S05] use four, KNOWN, CONDITIONAL, NEW and OPEN [S04, p. v; S05, p. v]; [S06] adds REPROVED
and DISPUTED [S06, p. vi]; [S07] uses five marks, of which DESIGN carries no truth claim and FORMAL TARGET marks a
statement written for a proof assistant and not yet checked by one [S07, p. vi]. Status attaches to the parts of an
argument separately: in [S03] an open premise together with a proved implication “yields an open route to RH, not a
theorem of RH.” [S03, p. v]

::: {.figure #fig:method file="fig-method" place="tbp"}
Recursive mathematical discovery, as the Series Note of the five works states it: a structure is proposed, tested
against the cases in which the answer is known, abstracted into a new setting if it survives, and the question is
posed again there. What does not survive is kept. Below, the status labels with which each work reports its results.
:::

# The series and its records

The seven works comprise 34 volumes, 26,021 pages and 995 chapters. Counted by two independent methods on their
sources and on the sealed PDFs, and taking the smaller count where the two differ, they contain more than 349,000
formulas, more than 10,500 numbered statements (theorems, propositions, lemmas, corollaries, definitions and
conjectures), 714 numbered algorithms and 1,434 numbered figures and plates [S00]. These numbers measure size, not
correctness.

All eight works are released as Research Architecture Edition 1, version 1.0.0, under the Creative Commons BY-NC-ND 4.0
licence (\figref{series}). Each has a Zenodo record with a concept DOI that resolves to every version and a version DOI
for the edition, a public GitHub repository holding the release files, and a signed list of the checksums of its files,
so that a correction can name the exact edition it corrects. The records are collected in the Zenodo community *The
Grothendieckian Programme*, and the author’s records are linked to an ORCID iD. The overview volume [S00] gives five routes
through the works, for a first reading and for mathematical, machine-reasoning, formal and sceptical readers
[S00, Table 4].

::: {.figure #fig:series file="fig-series" place="tbp"}
The series and its records. Above, the eight works in the order of their release, with the date, the number of volumes
and pages, the concept DOI and the repository of each. Below, the three papers released together and the repository of
the problems, through which solutions and corrections are submitted and recorded.
:::

# Research plan and taking part

The plan is the one the works state. Each ends with what it leaves open, stated precisely enough to be taken up
(Table 1, third column); [S01] and [S02] leave specifications to be implemented and experiments to be run [S01, Vol. III; S02, p. xvi]. The second
work names the contributions that would count, and the overview volume applies them to every work [S00]: “Three kinds of contribution would matter
most.” The first is refutation — “a counterexample to a theorem, a failure of a stated degeneration, or an experiment
in which a module fails the gate it names”; the second is completion, since “the obligations printed as open are
stated precisely enough to be taken up”; the third is construction, an implementation run against a programme fixed in
advance [S02, p. xvi].

The process is public. The third of the papers released together selects fifty-seven of the open items, each with a statement, its
source and page, the status the source gives it, a literature check and a criterion that decides when it is solved.
Each has its own thread in the repository of the papers, where a solution, a partial result, a counterexample, a report
that a problem is already solved, or a correction can be submitted. A solution that meets its criterion is recorded
under the solver’s name in the next version of the papers and in the next edition of the work from which the problem
comes; corrections are listed with the version in which they are made. The works keep their own instruments:
“Corrections are welcome and will be maintained in a public errata.” [S05, p. xix] No date is set for the next
editions.

# Limits

None of the seven works claims a proof of the conjectures that are its research subjects; each states its boundary
in its first pages (Table 1). The works are first drafts and have not been peer-reviewed. Much of the architecture is
specified and not implemented: Volume III of [S01] is a specification, and [S02] reports that nothing has been
trained or measured. Lean verification of the works is incomplete. The counts of Section 5 are of the published sources
and PDFs. The declaration below states how AI tools were used in the preparation of the works and of this paper.
