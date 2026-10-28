# Part I. The Machine {.part #part-1}

The problems of this part come from the two works on the architecture of a reasoning system for mathematics: Problems 1–17 from *GAI-MUA: The Grothendieckian Machine* [S01] and Problems 18–35 from *GM-Omega-Infinity: Topos-Native Intelligence* [S02]. Page numbers in [S01] run through its six volumes.

::: {.problem #problem-1 title="The first rising-sea event" tags="machine · programme level"}
::: {.field label="Thesis"}
Thesis 8 (The rising sea).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. III, §5.1, p. 8034, and §5.8, p. 8039.
:::

::: {.field label="Status in the source"}
S/R (source-grounded synthesis; falsifiable research construction).
:::

::: {.field label="Statement"}
Carry out one operational rising-sea event in the sense of [S01, Vol. III, §5.1]. Such an event “must begin from an explicit obstruction or language deficit, propose a typed extension, compile bounded probes, preserve or explicitly surrender recovery, record costs and residuals, and submit any status request to authority outside the producing engines.” The problem asks for an event of this kind after which the original difficulty, stated before the event, has become tractable in the extended setting without the question having been changed.
:::

::: {.field label="What the source establishes"}
The source fixes the sequence obstruction → typed extension → bounded execution and checking → computed, partial or failed → recovery and transport → external request, observes that “Each arrow may fail”, and declines to promote the strategy: “Volume III does not turn that strategy into a universal theorem of problem solving. It turns it into a falsifiable campaign record.” It names four ways in which an extension changes the question instead of answering it: an extension that “deletes the predicate expressing a contradiction, forgets the invariant detecting failure, weakens equality until disagreement disappears, or renames an unknown as a new primitive has not resolved the original obstruction.” Section 5.8 specifies the residual and non-equivalence records that a partial outcome must leave. No event has been carried out.
:::

::: {.field label="Proposed by"}
The image of the rising sea is Grothendieck’s [McL07]; its operational form and this problem are from [S01].
:::

::: {.field label="Background"}
[McL07]; [Lak76]; machine-guided discovery with an external evaluator [DVB+21; RBN+24].
:::

::: {.field label="Solved when"}
A campaign record is published that a third party can replay, in which (i) every step of the §5.1 sequence is present as a typed artifact; (ii) the target statement, frozen before the campaign, receives in the extended setting a kernel-checked proof, a kernel-checked refutation, or a reduction to named hypotheses with their statuses recorded; and (iii) a reviewer independent of the producing system certifies that none of the four failures of §5.1 applies. A complete record of a failed campaign is listed as a partial result.
:::

::: {.field label="Literature check (28 October 2026)"}
No published campaign record of this form was found. Machine-guided discovery systems [DVB+21; RBN+24; TWL+24] evaluate candidates externally but do not record the four failure patterns or a separate status request.
:::

::: {.field label="Discussion"}
[Issue 1](https://github.com/AlienMuse/grothendieckian-problems/issues/1) of the repository.
:::
:::

::: {.problem #problem-2 title="A bounded fixed point of the coupled world–language cycle" tags="formalization · programme level"}
::: {.field label="Thesis"}
Thesis 10 (Discovery is recursive).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. III, §75.17, pp. 9503–9504; §75.11, pp. 9499–9500; §56.15, pp. 9130–9131.
:::

::: {.field label="Status in the source"}
O (obligation).
:::

::: {.field label="Statement"}
Give a formal transition model of the coupled world–language cycle of [S01, Vol. III, Ch. 71–78] and prove, in a proof assistant, three properties of it: (a) the obligation-preservation inclusion $O^{\mathrm{open}}_n \subseteq O^{\mathrm{open}}_{n+1} \cup O^{\mathrm{dis}}_{n+1} \cup O^{\mathrm{term}}_{n+1}$ of §75.11 holds for every accepted step; (b) the six conditions of §75.17 under which “A cycle reaches BOUNDED_FIXED_POINT” are decidable from the records; and (c) every run terminates, since “A conforming campaign therefore carries a well-founded repair measure or a hard policy bound.”
:::

::: {.field label="What the source establishes"}
The conditions are stated as contracts; none is proved. Failure of the inclusion in (a) “is sufficient for refusal or quarantine, regardless of the attractiveness of the new result.” The source limits what a fixed point means: “This is not equality of world and language, global convergence, consistency, optimality, or future stability.”
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
Transition systems and invariants in the style of [HW90]; mechanised metatheory [BW05].
:::

::: {.field label="Solved when"}
A machine-checked development (Lean, Rocq, Isabelle or Agda) that defines the model, documents its correspondence with §§75.11 and 75.17 clause by clause, and proves (a)–(c); or a machine-checked counterexample showing that one of them fails in every model faithful to the source.
:::

::: {.field label="Literature check (28 October 2026)"}
No formal model of this cycle was found; the searches returned general work on invariants in refinement-based verification only.
:::

::: {.field label="Discussion"}
[Issue 2](https://github.com/AlienMuse/grothendieckian-problems/issues/2) of the repository.
:::
:::

::: {.problem #problem-3 title="From obstruction to conjecture" tags="machine · research level"}
::: {.field label="Thesis"}
Thesis 10 (Discovery is recursive).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. IV, §109.1, p. 11670, and §109.5, p. 11675 (algorithm ALG-118).
:::

::: {.field label="Status in the source"}
ALG-R (research algorithm).
:::

::: {.field label="Statement"}
Implement the obstruction-driven conjecture generator ALG-118 of [S01, Vol. IV, Ch. 109], which takes replayable, typed records of failed constructions or proof attempts and returns scoped conjectures, each with at least one executable falsifier, and run it until it produces a conjecture that is then settled by others.
:::

::: {.field label="What the source establishes"}
The source specifies the contract and its limits: “An obstruction can explain why a particular construction, proof route, or finite experiment failed. It does not by itself establish the negation, necessity, naturalness, or novelty of a conjecture inferred from that failure.” Status is not affected by how a candidate looks: “Frequency, linguistic plausibility, retrieval rank, model agreement, elegance, and apparent usefulness do not change its epistemic status.” Falsifiers are part of the output, and “No finite search can certify an unrestricted conjecture.” No implementation exists.
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
[Lak76]; automated conjecturing [Faj88; RGM+21]; [DVB+21].
:::

::: {.field label="Solved when"}
An implementation run on a published set of typed obstructions, with the full record of every candidate and of its falsifiers, such that at least one generated conjecture that is not in the frozen corpus (in the scoped sense of [S01, Vol. IV, §110.8]) is afterwards proved, or refuted by a replayed counterexample, by parties independent of the generator.
:::

::: {.field label="Literature check (28 October 2026)"}
Theory exploration and conjecturing systems were found [Faj88; RGM+21]; none takes typed obstruction records as input or attaches falsifiers to each output.
:::

::: {.field label="Discussion"}
[Issue 3](https://github.com/AlienMuse/grothendieckian-problems/issues/3) of the repository.
:::
:::

::: {.problem #problem-4 title="Minimal extension questions" tags="machine · research level"}
::: {.field label="Thesis"}
Thesis 1 (Worlds, not isolated theorems).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. III, §24.10, pp. 8440–8441.
:::

::: {.field label="Status in the source"}
O (obligation).
:::

::: {.field label="Statement"}
“MinimalExtensionQuestion turns a diagnosed deficit into an ordered search over semantic deltas.” For a declared class of mathematical worlds and a declared partial order on deltas, give a procedure that, from an independently checked obstruction, returns an extension that is minimal for that order, consistent, conservative over the predecessor world, and reopens the blocked obligation; or prove that no such procedure exists for the class.
:::

::: {.field label="What the source establishes"}
The question belongs to the Topos New-Creation Architecture (TNCA), the engine of [S01] that proposes successor worlds. The source fixes the meaning of minimality — “Minimality is relative to that declared partial order, not to implementation effort or textual brevity” — and gives the two failure modes it must avoid (jumping to a stronger logic, and refusing an extension that is needed). It states what is missing: “TNCA has not shown existence, consistency, conservativity, or usefulness of any answer.”
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
Conservative extensions in logic and type theory; [Mac78] for the categorical constructions involved.
:::

::: {.field label="Solved when"}
A stated class of worlds (for example finitely axiomatised first-order theories or finite presentations of categories), a declared order on deltas, and a machine-checked proof that the procedure is correct on the class, with an implementation evaluated on published obstructions; or a machine-checked impossibility result for a class of comparable generality.
:::

::: {.field label="Literature check (28 October 2026)"}
Work on conservative extension and minimal extensions in logic was found; no procedure with the inputs and guarantees of §24.10 was found.
:::

::: {.field label="Discussion"}
[Issue 4](https://github.com/AlienMuse/grothendieckian-problems/issues/4) of the repository.
:::
:::

::: {.problem #problem-5 title="Target fidelity" tags="machine · research level"}
::: {.field label="Thesis"}
Thesis 6 (A chain of non-implications).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. III, §30.10, p. 8574, and §64.17, p. 9294; Architectural Prospectus, p. 7966; Vol. IV, §5.16, p. 9846.
:::

::: {.field label="Status in the source"}
O (obligation).
:::

::: {.field label="Statement"}
A proof kernel checks a proof against a formal statement; it does not check that the formal statement is the mathematics it was meant to express. In the source: “A named, pinned formal kernel may check a proof term against a formal target; target fidelity and publication authority remain separate obligations.” Give a certificate format and checker for the fidelity of a formal statement to a statement in a source text, within a declared fragment of mathematical language and a declared library.
:::

::: {.field label="What the source establishes"}
The source treats every machine proof as a candidate “until source-target fidelity, kernel replay, and axiom-closure review pass under the same canonical subject key”, and lists among the open obligations of the formal layer to “verify that adapted definitions and rule candidates faithfully reflect the cited locators and declared deltas” and “target-fidelity theorems connecting source constructs to generated declarations”.
:::

::: {.field label="Proposed by"}
[S01]; the question is shared with the autoformalization literature [WJL+22; FLM+26].
:::

::: {.field label="Background"}
[BW05]; [WJL+22]; misformalization records in [FLM+26].
:::

::: {.field label="Solved when"}
A certificate format that binds a formal target, a source locator and a declared map of definitions, and a checker that rejects every certificate in a published adversarial suite of statement pairs with deliberately introduced misformalizations (quantifier order, hypothesis loss, changed definitions) while accepting the faithful pairs, with the suite, the checker and the results released for independent replay.
:::

::: {.field label="Literature check (28 October 2026)"}
Many 2025–2026 preprints measure faithfulness of autoformalization by scores or round-trip tests; none found issues a fidelity certificate of the kind required here.
:::

::: {.field label="Discussion"}
[Issue 5](https://github.com/AlienMuse/grothendieckian-problems/issues/5) of the repository.
:::
:::

::: {.problem #problem-6 title="Verified encodings of universal properties" tags="formalization · research level"}
::: {.field label="Thesis"}
Thesis 3 (A structured latent space).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. III, §18.5, p. 8307, and §21.16, item 8, p. 8370.
:::

::: {.field label="Status in the source"}
O (obligation).
:::

::: {.field label="Statement"}
The component MUF-H (Motivic Universal Factorization Algorithm—Hybrid) of [S01] solves universal-property constraints for finite proxies of categories. “A solver that returns a satisfying assignment only proves satisfiability of the encoded finite constraints if the encoding and certificate are independently checked. It does not establish that the encoding captures the intended universal property.” For finite categories given by their composition tables, give an encoding of the statement that a cone (or cocone) is a limit (colimit) of a finite diagram into constraints a solver can decide, and prove the encoding correct.
:::

::: {.field label="What the source establishes"}
The source requires that “Universality encodings still require an independently checked correspondence between mathematical quantifiers and constraints”, and that existence of mediating maps and their uniqueness be recorded as separate obligations, since “Universality requires a quantified mediating property and generally uniqueness at an explicitly stated identity strength.”
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
[Mac78]; [MM94].
:::

::: {.field label="Solved when"}
A machine-checked theorem that, for every finite diagram in a finite category, the solutions of the encoded constraints correspond bijectively to mediating morphisms and that the uniqueness check is complete, together with a verified checker for solver certificates.
:::

::: {.field label="Literature check (28 October 2026)"}
General work on constraint solving and finite model finding was found; no verified encoding of universal properties was found.
:::

::: {.field label="Discussion"}
[Issue 6](https://github.com/AlienMuse/grothendieckian-problems/issues/6) of the repository.
:::
:::

::: {.problem #problem-7 title="The AURORA-K0 kernel, I: syntax and checking" tags="formalization · research level"}
::: {.field label="Thesis"}
Thesis 2 (Status is part of the type).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. III, §70.19, pp. 9428–9429 (obligations K0-META-001 to K0-META-009).
:::

::: {.field label="Status in the source"}
O (“Every item begins OPEN”).
:::

::: {.field label="Statement"}
Mechanise AURORA-K0, the small formal kernel of the experimental calculus AURORA [S01, Vol. III, Ch. 70], and discharge the first nine obligations of its registry, among them that the “Concrete grammar has unique parsing after canonical Unicode normalization”, that “Substitution preserves K0 typing”, that “Registered reduction preserves typing”, that “Algorithmic checking agrees with declarative K0 rules”, and that the “Definitional equality procedure is decidable for the declared finite fragment”.
:::

::: {.field label="What the source establishes"}
The registry lists each obligation with the evidence required before its status may change, and rules out the shortcut: “No row may become RECEIPT_BOUND merely because a checker returns success.” No obligation is discharged.
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
The de Bruijn criterion and small kernels [BW05]; [MU21]; [Car24].
:::

::: {.field label="Solved when"}
A development in a proof assistant that defines K0 as in the exact edition of Chapter 70 and proves K0-META-001 to K0-META-009 using no axioms beyond the assistant’s standard ones; a machine-checked counterexample to any item also counts and is recorded as a correction to the source.
:::

::: {.field label="Literature check (28 October 2026)"}
Mechanised metatheory of type theories is an established field; no mechanisation of K0 was found.
:::

::: {.field label="Discussion"}
[Issue 7](https://github.com/AlienMuse/grothendieckian-problems/issues/7) of the repository.
:::
:::

::: {.problem #problem-8 title="The AURORA-K0 kernel, II: a model and relative consistency" tags="formalization · research level"}
::: {.field label="Thesis"}
Thesis 2 (Status is part of the type).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. III, §70.19, pp. 9428–9429 (obligations K0-META-010 to K0-META-012).
:::

::: {.field label="Status in the source"}
O.
:::

::: {.field label="Statement"}
For the kernel K0 of Problem 7, discharge the semantic obligations of the registry: “At least one nontrivial model validates the rules”; “Relative consistency, if pursued”, relative to a named base theory; and “Conservativity over any source theory” for the source theories that the architecture embeds.
:::

::: {.field label="What the source establishes"}
The registry requires an explicit model construction with independent validation, a proposition-exact metatheorem for relative consistency, and an explicit interpretation with a conservativity proof, and records all three as open.
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
Models of type theory; [Uni13]; conservativity results for extensions of type theory.
:::

::: {.field label="Solved when"}
A machine-checked model of K0 that is not trivial in the sense of §70.19, and machine-checked proofs of relative consistency and of conservativity over at least one named source theory.
:::

::: {.field label="Literature check (28 October 2026)"}
Mechanised relative-consistency proofs exist for other systems; none for K0 was found.
:::

::: {.field label="Discussion"}
[Issue 8](https://github.com/AlienMuse/grothendieckian-problems/issues/8) of the repository.
:::
:::

::: {.problem #problem-9 title="The seven obligations of descent execution" tags="formalization · research level"}
::: {.field label="Thesis"}
Thesis 5 (Report failure; abstain without evidence).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. III, §56.15, pp. 9130–9132, and §56.1, p. 9119.
:::

::: {.field label="Status in the source"}
O.
:::

::: {.field label="Statement"}
The Grothendieckian Descent Reasoning Architecture (GDRA) of [S01], the layer that executes local-to-global campaigns, exists to prevent one error: “The central architectural error is to convert operational completion into global meaning.” Give a formal transition model of GDRA campaigns and prove the seven properties that §56.15 leaves open: “canonical serialization must preserve identity; every accepted transition must preserve the invariants; forbidden authority effects must be noninterfering; budget events must conserve declared dimensions; event replay must converge to the same eligible head under the stated delivery model; counterevidence closure must be omission-resistant; and adapters must preserve the disjoint failure constructors.”
:::

::: {.field label="What the source establishes"}
The source states the seven properties and the delivery model (at-least-once delivery with idempotent effects), and records: “None has a supplied mechanized proof.”
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
Noninterference [GM82]; linearizability [HW90].
:::

::: {.field label="Solved when"}
Machine-checked proofs of all seven properties for a model whose correspondence with Chapter 56 is documented clause by clause, or a machine-checked counterexample to one of them.
:::

::: {.field label="Literature check (28 October 2026)"}
Noninterference and replay-safety proofs exist for other systems; none for this model was found.
:::

::: {.field label="Discussion"}
[Issue 9](https://github.com/AlienMuse/grothendieckian-problems/issues/9) of the repository.
:::
:::

::: {.problem #problem-10 title="Non-self-authorization" tags="formalization · research level"}
::: {.field label="Thesis"}
Thesis 7 (Machines propose; humans authorize).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. V, Proposition 1.3, p. 11913; Proposition 5.1, p. 11940; Proposition 10.1, p. 11979.
:::

::: {.field label="Status in the source"}
D/O (definition; obligation).
:::

::: {.field label="Statement"}
The rule that machines propose and humans authorise publication is stated in [S01, Vol. V] as three propositions, each conditional on assumptions about capabilities. Proposition 1.3 concludes that “a non-root module cannot, through a conforming Volume V interface, make its own output both authoritative and active”; Proposition 10.1 that “adding a validated evidence edge to an artifact cannot by itself increase the artifact’s epistemic class”. Give a formal model of capabilities, signing and status transitions in which the hypotheses of Propositions 1.3, 5.1 and 10.1 are definitions, and prove the three conclusions.
:::

::: {.field label="What the source establishes"}
The propositions are argued informally and marked D/O: “The proposition is conditional on correct capability isolation and validator independence; those conditions are test obligations, not assumptions to be hidden.” The negative cases (a worker writing to the status store, a signature detached from the artifact hash) are listed.
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
[DV66]; [SS75]; [GM82].
:::

::: {.field label="Solved when"}
Machine-checked proofs of the three propositions in a published model, and a test suite showing that each listed negative case is rejected by an implementation conforming to the model.
:::

::: {.field label="Literature check (28 October 2026)"}
Verified capability machines and separation kernels exist; no formalisation of these three propositions was found.
:::

::: {.field label="Discussion"}
[Issue 10](https://github.com/AlienMuse/grothendieckian-problems/issues/10) of the repository.
:::
:::

::: {.problem #problem-11 title="Evolution without authority" tags="formalization · research level"}
::: {.field label="Thesis"}
Thesis 7 (Machines propose; humans authorize).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. VI, §11.11, p. 13204; Vol. III, §21.16, item 12, pp. 8370–8371.
:::

::: {.field label="Status in the source"}
O (obligation O-V6-11-04).
:::

::: {.field label="Statement"}
A self-improving component may propose changes to itself but must not acquire authority. In [S01, Vol. VI] the obligation reads: “O-V6-11-04 — prove that no composition of EvolutionContract ports reaches signing, promotion, activation, root mutation, or rollback capabilities”. Prove it for a formal model of the evolution interface.
:::

::: {.field label="What the source establishes"}
In the released architecture “Evolution remains inert: telemetry cannot evaluate candidates, adapt routing, update policy, canary, promote, deploy, or roll back.” The source does not claim more: “Until these obligations are discharged, policy morphisms and version graphs are precise governance objects, not a claim that safe whole-system evolution has been solved.”
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
[SS75]; reward hacking as the failure this obligation guards against [SHKK22].
:::

::: {.field label="Solved when"}
A machine-checked reachability theorem over all finite compositions of the ports of the published EvolutionContract model, with the model’s correspondence to Vol. VI, Ch. 11 documented; or a composition that reaches a forbidden capability.
:::

::: {.field label="Literature check (28 October 2026)"}
Recent work studies privilege escalation in AI agents empirically; no formal reachability proof for an evolution interface of this kind was found.
:::

::: {.field label="Discussion"}
[Issue 11](https://github.com/AlienMuse/grothendieckian-problems/issues/11) of the repository.
:::
:::

::: {.problem #problem-12 title="Deterministic identity across implementations" tags="machine · entry level"}
::: {.field label="Thesis"}
Thesis 6 (A chain of non-implications).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. V, Proposition 2.2, p. 11920, and Proposition 3.2, p. 11927.
:::

::: {.field label="Status in the source"}
D/O.
:::

::: {.field label="Statement"}
Build two independent implementations of the canonical serialization and replay profile of [S01, Vol. V] and show that they agree: identical canonical bytes and identifiers for the same artifacts (Proposition 2.2), and identical kernel judgments under identical inputs and environments (Proposition 3.2).
:::

::: {.field label="What the source establishes"}
Proposition 2.2 is “an interoperability obligation to be tested by cross-language fixtures.” For replay, “A disagreement is a first-class incident”, and “The system does not choose the favorable result by majority vote.” No second implementation exists.
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
[LZ22]; [Nec97].
:::

::: {.field label="Solved when"}
Two implementations in different languages by different authors, and a published fixture suite (Unicode normalisation, exact numbers, ordered and unordered collections, extension fields) on which they agree byte for byte, with every disagreement found during development recorded as an incident.
:::

::: {.field label="Literature check (28 October 2026)"}
Reproducible-builds practice [LZ22] addresses the same property for software artifacts; no implementation of this profile was found.
:::

::: {.field label="Discussion"}
[Issue 12](https://github.com/AlienMuse/grothendieckian-problems/issues/12) of the repository.
:::
:::

::: {.problem #problem-13 title="A frozen benchmark for counterexample and proof discovery" tags="machine · entry level"}
::: {.field label="Thesis"}
Thesis 12 (Judge a method by its open ledger).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. IV, §113.1, p. 11744; §113.12.12 to §113.12.15, pp. 11763–11764.
:::

::: {.field label="Status in the source"}
D (specified, not run).
:::

::: {.field label="Statement"}
Release the first version of the benchmark specified in [S01, Vol. IV, Ch. 113]. “A benchmark is not merely a directory of examples and a script that prints a score.” Before any run, it “must freeze the task, version, population, split, metric, abstention policy, leakage boundary, resource model, and reporting semantics”, and it must separate counterexample tasks into strata A–F and proof tasks into the seven types of §113.12.13.
:::

::: {.field label="What the source establishes"}
The specification is complete and unexecuted. Its scoring rules include that “Stratum E evaluates whether the system reports bounded unknown honestly; it does not reward a claim that the theorem is true”, and that “Hidden proofs are protected evaluation assets, not canonical solution paths.”
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
[ZHP22]; [FLM+26].
:::

::: {.field label="Solved when"}
A release with the four boundaries of §113.1 frozen by digest, at least one item in every counterexample stratum and every proof-task type, a working challenge process (§113.12.15), and results for at least two systems reported stratum by stratum.
:::

::: {.field label="Literature check (28 October 2026)"}
Benchmarks for formal and research mathematics exist [ZHP22; FLM+26]; none found has the stratification, the abstention strata or the frozen constitution of Ch. 113.
:::

::: {.field label="Discussion"}
[Issue 13](https://github.com/AlienMuse/grothendieckian-problems/issues/13) of the repository.
:::
:::

::: {.problem #problem-14 title="The language forge, end to end" tags="machine · programme level"}
::: {.field label="Thesis"}
Thesis 11 (Creating language).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. III, Preface, p. 7956; §43.14, p. 8873; §44.16, pp. 8888–8889; §45.8, p. 8898.
:::

::: {.field label="Status in the source"}
O.
:::

::: {.field label="Statement"}
“The language forge follows a deliberately articulated cycle: collect, mine, name, notate, ground, reconstruct, axiomatize, grow, re-encode, and validate.” Run the cycle of [S01, Vol. III, Ch. 41–48] end to end on a published corpus and produce a new notation and language package for a declared mathematical domain, with its metatheoretic obligations discharged.
:::

::: {.field label="What the source establishes"}
The source specifies each stage and leaves completeness open: “The order organizes a bounded language-formation workflow and leaves completeness as an open research question.” It requires that “Notation earns trust by declaring what it compresses, what it preserves, and what it cannot recover”, and that “An obligation is not promoted because it is conventional for a language family or appears plausible from examples.”
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
[Gan13]; [CF09].
:::

::: {.field label="Solved when"}
A package for a declared domain in which every introduced primitive is linked to the structural motifs and counterexamples that motivated it, whose substitution, preservation and conservativity obligations (§44.16) are machine-checked, and whose round trips (Ch. 43) pass on a held-out set of statements from the domain.
:::

::: {.field label="Literature check (28 October 2026)"}
Work on mathematical concept formation and on the language of mathematics [Gan13] was found; no end-to-end language-formation system with these obligations was found.
:::

::: {.field label="Discussion"}
[Issue 14](https://github.com/AlienMuse/grothendieckian-problems/issues/14) of the repository.
:::
:::

::: {.problem #problem-15 title="A preregistered test of typed base change" tags="machine · entry level"}
::: {.field label="Thesis"}
Thesis 1 (Worlds, not isolated theorems).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. I, §11.12, p. 277 (Conjecture V1-CH-011-C001); definitions, pp. 275–276.
:::

::: {.field label="Status in the source"}
C (conjecture).
:::

::: {.field label="Statement"}
Test the conjecture of [S01, Vol. I, §11.12]: “For a corpus whose categorical claims are already expressed as finite typed diagrams, requiring an RCP/RCT pair for each use of “base change” will reduce orientation and hypothesis errors relative to an untyped prose baseline.” Here an RCP (relative change passport) records the bases, the base arrow and its variance, and an RCT (relative claim trace) records the status and hypotheses of the claim made after the change (Definitions V1-CH-011-D003 and D004).
:::

::: {.field label="What the source establishes"}
“This is a falsifiable editorial-engineering conjecture. It requires a preregistered corpus, error taxonomy, reviewers, and comparison protocol; no performance result is claimed here.”
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
Preregistration [NEDM18].
:::

::: {.field label="Solved when"}
A study whose corpus, error taxonomy, reviewer assignment and analysis are registered before data are collected, with independent reviewers, reporting the result in either direction.
:::

::: {.field label="Literature check (28 October 2026)"}
No study of this question was found.
:::

::: {.field label="Discussion"}
[Issue 15](https://github.com/AlienMuse/grothendieckian-problems/issues/15) of the repository.
:::
:::

::: {.problem #problem-16 title="A preregistered test of the four judgments of gluing" tags="machine · entry level"}
::: {.field label="Thesis"}
Thesis 5 (Report failure; abstain without evidence).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. I, §15.12, p. 361 (Conjecture V1-CH-015-C001).
:::

::: {.field label="Status in the source"}
C.
:::

::: {.field label="Statement"}
Test the conjecture of [S01, Vol. I, §15.12]: “On a preregistered corpus of local-to-global mathematical arguments, mandatory separation of compatibility, effectivity, uniqueness, and property return will reduce false “gluing succeeds” judgments relative to an untyped prose baseline.”
:::

::: {.field label="What the source establishes"}
“Testing requires fixed cases, independent reviewers, and an error taxonomy; no empirical result is claimed here.”
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
[NEDM18]; descent in [SGA4].
:::

::: {.field label="Solved when"}
A preregistered study as in Problem 15, reporting the result in either direction.
:::

::: {.field label="Literature check (28 October 2026)"}
No study of this question was found.
:::

::: {.field label="Discussion"}
[Issue 16](https://github.com/AlienMuse/grothendieckian-problems/issues/16) of the repository.
:::
:::

::: {.problem #problem-17 title="A preregistered test of obstruction records" tags="machine · entry level"}
::: {.field label="Thesis"}
Thesis 5 (Report failure; abstain without evidence).
:::

::: {.field label="Source"}
*GAI-MUA: The Grothendieckian Machine* [S01], Vol. I, Ch. 17, p. 404 (Conjecture V1-CH-017-C001).
:::

::: {.field label="Status in the source"}
C.
:::

::: {.field label="Statement"}
Test the conjecture of [S01, Vol. I, Ch. 17]: “For a fixed benchmark of finite, fully enumerated lifting and gluing problems with independently verified ground truth, requiring the fields of ObstructionRecordV1 will reduce false “no solution” classifications relative to an otherwise identical checker that stores only a Boolean success flag.”
:::

::: {.field label="What the source establishes"}
“This is an empirical systems conjecture, not a mathematical theorem.” The same section forbids the strengthening that every failed construction determines a cohomology class whose vanishing solves the problem.
:::

::: {.field label="Proposed by"}
[S01].
:::

::: {.field label="Background"}
[NEDM18]; [Gir71] for obstruction classes.
:::

::: {.field label="Solved when"}
A preregistered comparison of the two checkers on a published benchmark with enumerated ground truth, reporting the false-negative rates of both with confidence intervals.
:::

::: {.field label="Literature check (28 October 2026)"}
No study of this question was found.
:::

::: {.field label="Discussion"}
[Issue 17](https://github.com/AlienMuse/grothendieckian-problems/issues/17) of the repository.
:::
:::

::: {.problem #problem-18 title="Discovering the site" tags="machine · programme level"}
::: {.field label="Thesis"}
Thesis 3 (A structured latent space).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], §1.2.5, p. 22.
:::

::: {.field label="Status in the source"}
open (listed among “The five things we are least sure of”).
:::

::: {.field label="Statement"}
In the architecture of [S02] a context is a site, the information it supports is a sheaf, and a conclusion is a global section. The site itself is supplied by hand: “The site must be imposed. We do not know how to discover the evidence-atom locale from a corpus; we construct it.” Give a procedure that constructs the evidence-atom locale, its refinement order and its covering families from a corpus, with a stated sufficiency criterion, and show that the result does not merely reflect the design of the procedure.
:::

::: {.field label="What the source establishes"}
The source states the objection it cannot answer: “a critic who says the invariants measure our design choices rather than the model’s structure has a real point that we cannot fully answer.” Learned restriction maps are studied elsewhere on a fixed graph [BDCLB22; DBDL24]; the base space is not learned there.
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
[HG19]; [BDCLB22]; [DBDL24]; [MM94].
:::

::: {.field label="Solved when"}
A procedure and a published evaluation in which (i) planted sites in synthetic corpora are recovered up to a declared isomorphism budget, (ii) the site constructed from a natural corpus is stable under resampling within that budget, and (iii) invariants computed on it survive the gaming controls of [S02, §9.1] (terminal-site collapse, zero restrictions, filled nerve).
:::

::: {.field label="Literature check (28 October 2026)"}
Sheaf neural networks with learned restriction maps on a given graph were found [BDCLB22; DBDL24]; no procedure that learns the site itself was found.
:::

::: {.field label="Discussion"}
[Issue 18](https://github.com/AlienMuse/grothendieckian-problems/issues/18) of the repository.
:::
:::

::: {.problem #problem-19 title="The capability wager" tags="machine · research level"}
::: {.field label="Thesis"}
Thesis 4 (Attention as descent).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], Conjecture 3.6.17, p. 778; §1.2.5, p. 22.
:::

::: {.field label="Status in the source"}
D (design-grade conjecture).
:::

::: {.field label="Statement"}
On an orthogonal cellular sheaf the non-abelian holonomy capacity $\beta$ of [S02] is either $0$ or at least a constant $c(d)$ depending only on the stalk dimension. The wager is that $\beta$ governs capability. In the words of the source: “At matched parameters, data and compute, compare models with CERTIFIED_VIRTUALLY_ABELIAN and CERTIFIED_FREE reports on tasks requiring route-dependent evidence.” Decide the wager.
:::

::: {.field label="What the source establishes"}
The dichotomy is proved; the wager is not. “That β governs capability is grade D and we have no proof. It is the most interesting claim in the document and the least supported.” The comparison is set up so that a negative result costs only the wager: “No theorem links the verdict to capability; failure of the registered comparison removes the capability claim while leaving the group theorem intact.”
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
The Tits alternative [Tit72]; uniform growth gaps [Bre11]; [HG19].
:::

::: {.field label="Solved when"}
A preregistered comparison at matched parameters, data and compute, with certificates computed as in [S02, Ch. 3.6], published with its outcome in either direction.
:::

::: {.field label="Literature check (28 October 2026)"}
No study linking holonomy growth of cellular sheaves to model capability was found.
:::

::: {.field label="Discussion"}
[Issue 19](https://github.com/AlienMuse/grothendieckian-problems/issues/19) of the repository.
:::
:::

::: {.problem #problem-20 title="Nerve baselines between GRPO and RLOO" tags="machine · research level"}
::: {.field label="Thesis"}
Thesis 4 (Attention as descent).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], §1.2.4, pp. 21–22 (claim C11 of Appendix A7).
:::

::: {.field label="Status in the source"}
open empirical question.
:::

::: {.field label="Statement"}
The source proves that the group-relative advantage of group relative policy optimisation (GRPO) [SWZ+24] equals $\Delta_0 R/\lVert\delta_0 R\rVert_2$ for the $0$-Laplacian of the nerve of the sampling group, wherever $\sigma>0$. This places GRPO in “a family of graph baselines indexed by a nerve, of which the complete-graph member is GRPO and the i.i.d. leave-one-out member is RLOO.” (RLOO is the leave-one-out REINFORCE baseline [ACG+24].) Determine whether another member of the family reduces the variance of the policy-gradient estimate at matched cost.
:::

::: {.field label="What the source establishes"}
The identity is proved and the family defined; “Whether any other member of that family reduces variance at matched cost is an open empirical question, tested by claim C11 of A7 and unanswered here.”
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
[SWZ+24]; [ACG+24]; recent baselines for reinforcement learning with verifiable rewards [ZZA+25].
:::

::: {.field label="Solved when"}
A theorem identifying, under stated assumptions on rewards, a nerve whose baseline has strictly smaller variance than both GRPO and RLOO at matched sampling cost, or proving that no member of the family does; or the registered experiment C11 with its outcome.
:::

::: {.field label="Literature check (28 October 2026)"}
Variance-reduction baselines for GRPO-type methods are an active topic [ZZA+25]; no study of the nerve family was found.
:::

::: {.field label="Discussion"}
[Issue 20](https://github.com/AlienMuse/grothendieckian-problems/issues/20) of the repository.
:::
:::

::: {.problem #problem-21 title="Relative obstruction as a predictor of unsupported answers" tags="machine · research level"}
::: {.field label="Thesis"}
Thesis 5 (Report failure; abstain without evidence).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], §10.1.7.3, pp. 1854–1855; instrument N5, §9.1.7, p. 1766.
:::

::: {.field label="Status in the source"}
T for the mathematics; D for what remains; N5 withdrawn.
:::

::: {.field label="Statement"}
For an evidence subdomain $A\subseteq X$, a coefficient sheaf $F$ and a partial section $s_A$, the connecting class $\partial(s_A)\in H^1(X,A;F)$ is a genuine obstruction to extending $s_A$. Supply the typed record that the source requires before this class may be used as an instrument, and test prospectively whether it predicts unsupported answers of a language model.
:::

::: {.field label="What the source establishes"}
The mathematics is proved; the instrument is not: “N5 is therefore WITHDRAWN as a validation or falsification instrument.” Reinstatement requires six items, including “at least one worked non-zero example, together with a zero control, computed before labels are revealed”. The remaining task is stated as “What remains is the difficult empirical part: the evidence sheaf must reflect factual support, the relative class must be approximated at scale, and prospective prediction must beat entropy, retrieval sufficiency, self-consistency and correctness probes without site collapse.”
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
[HG19]; [FKKG24]; [HRH24].
:::

::: {.field label="Solved when"}
The six reinstatement items of §9.1.7 published for one benchmark, followed by a prospective comparison against entropy, sequence likelihood, verbal confidence, retrieval sufficiency, self-consistency and a trained correctness probe, reported in either direction.
:::

::: {.field label="Literature check (28 October 2026)"}
Hallucination detectors based on entropy and probes exist [FKKG24]; sheaf-based consistency rating has been proposed [HRH24]; no instrument based on a relative connecting class was found.
:::

::: {.field label="Discussion"}
[Issue 21](https://github.com/AlienMuse/grothendieckian-problems/issues/21) of the repository.
:::
:::

::: {.problem #problem-22 title="Topos-MoE against modern sparse mixture-of-experts" tags="machine · research level"}
::: {.field label="Thesis"}
Thesis 4 (Attention as descent).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], §10.1.7.2, p. 1854; instrument N7, §9.1.9, pp. 1768–1769.
:::

::: {.field label="Status in the source"}
D.
:::

::: {.field label="Statement"}
In Topos-MoE, the mixture-of-experts layer of [S02], each expert is an open sub-topos and routing constructs a sufficient cover. Run the registered comparison N7 of [S02, §9.1.9] against a modern fine-grained sparse mixture-of-experts at matched total and active parameters, executed FLOPs, wall time and communication. “Coverage routing must beat top-k on quality and on total cost; lowering its own deficiency score proves nothing about either.”
:::

::: {.field label="What the source establishes"}
The descent typing is proved; the benefit is not. In the released configuration the coverage router cannot yet be trained, and it “may not report the coverage router as a trained component until that backward exists and is finite-difference checked.” The thresholds are fixed in advance: “Confirmation requires a 10 per cent relative reduction in multi-expert composition error or a 3-point absolute improvement, while remaining within 1 per cent of the top-k baseline on single-expert tasks and within 10 per cent of its throughput.”
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
[SMM+17]; [FZS22]; categorical approaches to architectures [GLD+24; Mah25].
:::

::: {.field label="Solved when"}
A trainable coverage router with a finite-difference-checked backward pass, and the N7 comparison executed under the registered protocol, reporting confirmation or one of the registered null outcomes.
:::

::: {.field label="Literature check (28 October 2026)"}
Many routing variants for mixture-of-experts were found; none uses sheaf-theoretic coverage routing with these controls.
:::

::: {.field label="Discussion"}
[Issue 22](https://github.com/AlienMuse/grothendieckian-problems/issues/22) of the repository.
:::
:::

::: {.problem #problem-23 title="A defence against a globally coherent falsehood" tags="machine · programme level"}
::: {.field label="Thesis"}
Thesis 5 (Report failure; abstain without evidence).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], §1.2.5, p. 22.
:::

::: {.field label="Status in the source"}
open (“we have no structural defence to propose”).
:::

::: {.field label="Statement"}
“Descent verification provably catches local inconsistency. Against a globally coherent falsehood it offers nothing, and we have no structural defence to propose.” Give a verification method that detects a stated class of globally coherent falsehoods, or prove that no verifier with access only to stated information can do so.
:::

::: {.field label="What the source establishes"}
The source proves the local guarantee and records the global gap as one of “The five things we are least sure of”; Part VI of [S02] discusses reward hacking at length without proposing a defence.
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
[SHKK22]; selective prediction [EW10]; [FKKG24].
:::

::: {.field label="Solved when"}
Either a method with a theorem stating which globally coherent falsehoods it detects and at what cost, evaluated on a published adversarial benchmark, or an impossibility theorem for a stated class of verifiers.
:::

::: {.field label="Literature check (28 October 2026)"}
Consistency- and verification-based hallucination detection was found; no structural defence or impossibility theorem for globally coherent falsehoods was found.
:::

::: {.field label="Discussion"}
[Issue 23](https://github.com/AlienMuse/grothendieckian-problems/issues/23) of the repository.
:::
:::

::: {.problem #problem-24 title="Compiled-to-streaming descent stability" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 4 (Attention as descent).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], Conjecture 2.2.15, p. 104.
:::

::: {.field label="Status in the source"}
D/OPEN.
:::

::: {.field label="Statement"}
Consider a session tower of finite certified sites and solid-valued states $(\mathcal C_n,P_n,F_n)_{n\ge 0}$ with the site maps of [S02, §2.2]. Conjecture 2.2.15: “If the cd-certificates are uniformly compatible under these site morphisms, the density bound is uniform, the coefficient towers satisfy the required derived-limit vanishing condition, and the finite probe systems form a conservative filtered family, then the limit state satisfies Nisnevich descent with solid condensed coefficients.” Prove or refute it.
:::

::: {.field label="What the source establishes"}
“The hypotheses are not discharged.” The source explains which hypotheses fail in practice — “Uniform density generally fails when new maximal atoms are added; derived-limit vanishing is not certified by the runtime; and no conservative finite probe family has been proved for arbitrary state classes” — and that “The conjecture therefore cannot be used to upgrade stagewise FINITE-ONLY certificates to a session-wide theorem.”
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
Nisnevich descent [MV99]; condensed and solid mathematics [Sch19]; [Lur09].
:::

::: {.field label="Solved when"}
A proof of the conjecture as stated, or a counterexample tower satisfying the four hypotheses whose limit state fails Nisnevich descent.
:::

::: {.field label="Literature check (28 October 2026)"}
Work on descent for condensed and syntomic coefficients was found; no result on limits of towers of finite certified sites was found.
:::

::: {.field label="Discussion"}
[Issue 24](https://github.com/AlienMuse/grothendieckian-problems/issues/24) of the repository.
:::
:::

::: {.problem #problem-25 title="The Beck–Chevalley square 12.6.3" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 4 (Attention as descent).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], §2.4.4, pp. 157–158 (Proposition 2.4.24, Theorem 2.4.25).
:::

::: {.field label="Status in the source"}
globally open.
:::

::: {.field label="Statement"}
For a context family $\mathrm{Rep}\colon\mathcal C_{\mathrm{ref}}\to\mathrm{Cat}_\infty$, transport along refinements is coherent by straightening, but “Straightening supplies no Beck–Chevalley comparison for that square” formed by a refinement arrow and a cover restriction, and Proposition 2.4.24 shows that “The gap is real even in discrete categories.” Characterise the families and covers for which the comparison $\rho_V\circ r_!\Rightarrow (r_i)_!\circ\rho_U$ exists, is invertible, and satisfies the identity, composition and overlap coherence laws, so that the conditional Theorem 2.4.25 applies.
:::

::: {.field label="What the source establishes"}
Theorem 2.4.25 proves coverwise transport under exactly these hypotheses, and Chapter 13.5 audits finite fixtures; the source calls this “a scope restriction and conditional local closure, not a general solution.” “The monograph does not close the gap globally.”
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
[Lur09]; [MM94]; [SGA4].
:::

::: {.field label="Solved when"}
A theorem giving necessary and sufficient conditions, in a stated generality, for the comparison of Theorem 2.4.25 to exist with its coherences, or a proof that no condition weaker than the hypothesis itself suffices in that generality.
:::

::: {.field label="Literature check (28 October 2026)"}
Recent work on Beck–Chevalley fibrations concerns ambidexterity and norm squares; no result on refinement–cover squares of this kind was found.
:::

::: {.field label="Discussion"}
[Issue 25](https://github.com/AlienMuse/grothendieckian-problems/issues/25) of the repository.
:::
:::

::: {.problem #problem-26 title="Sharp accumulation bounds for equivariance defects" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 6 (A chain of non-implications).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], Question 11.11.18, p. 2259.
:::

::: {.field label="Status in the source"}
X (open question).
:::

::: {.field label="Statement"}
The accumulation bound of [S02, Theorem 11.9.28] for the equivariance defects of successive layers is tight in the worst case, but its use as a certificate needs a lower bound on output norms that is not available. Question 11.11.18 asks: “Is there a class of architectures with certified lower norm control on which a usable ratio of bound to witness is O(1)? Failing that, is there a sharper bound that tracks the direction of the equivariance defect rather than only its magnitude, for instance by carrying a covariance rather than a scalar?”
:::

::: {.field label="What the source establishes"}
“Theorem 11.9.28 is tight in the worst case, with both of its constants attained.” Without the lower-norm premise the gate leaves the claim open: “A witness may still falsify a claim but cannot replace the missing certificate.” The source suggests, without attempting it, that defects may add in quadrature under a randomness assumption.
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
Error accumulation in composed computations [Hig02]; equivariance in deep learning [BBCV21].
:::

::: {.field label="Solved when"}
Either a class of architectures with certified lower norm control on which the ratio of bound to witness is proved O(1), or a direction-sensitive bound strictly sharper than Theorem 11.9.28 on a stated class, with proof.
:::

::: {.field label="Literature check (28 October 2026)"}
No result of this form for equivariance defects was found.
:::

::: {.field label="Discussion"}
[Issue 26](https://github.com/AlienMuse/grothendieckian-problems/issues/26) of the repository.
:::
:::

::: {.problem #problem-27 title="Local dynamics of the restriction-frame locus" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 4 (Attention as descent).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], Table 13.16.13, entry O8, p. 3174.
:::

::: {.field label="Status in the source"}
OPEN.
:::

::: {.field label="Statement"}
Determine “whether the head-indexed restriction-frame embedded locus is attracting, repelling or a saddle under unfrozen frame dynamics”, the open entry O8 of the unproved register of [S02, Part P].
:::

::: {.field label="What the source establishes"}
Proposition 13.11.46 proves a parameter-specific departure from the locus and refutes universal invariance, but does not classify the local dynamics. The register names the missing tool: “a Lyapunov, centre-manifold or other local-dynamics argument for the frame manifold”.
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
[Car81]; optimisation on matrix manifolds [AMS08].
:::

::: {.field label="Solved when"}
A proof classifying the locus as attracting, repelling or a saddle (possibly depending on stated parameters) under the dynamics of Chapter 13.11.
:::

::: {.field label="Literature check (28 October 2026)"}
Work on Stiefel-manifold training dynamics was found; no classification of this locus was found.
:::

::: {.field label="Discussion"}
[Issue 27](https://github.com/AlienMuse/grothendieckian-problems/issues/27) of the repository.
:::
:::

::: {.problem #problem-28 title="A base-change bound for the descent solve" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 4 (Attention as descent).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], Table 13.16.13, entry O14, pp. 3174–3175.
:::

::: {.field label="Status in the source"}
open.
:::

::: {.field label="Statement"}
Prove “a base-change bound for the descent solve”: a bound relating the outputs of the descent solve of [S02, Ch. 13.10] at two bases, on which every cross-base stability statement of the book depends.
:::

::: {.field label="What the source establishes"}
The register records where the argument stops: “no bound relates the solve at two bases; the available Jacobian square measures a different quantity”.
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
Spectral theory of sheaf Laplacians [HG19]; perturbation bounds [Hig02].
:::

::: {.field label="Solved when"}
A proved bound, with explicit constants, on the difference of the descent solves at two bases in terms of a stated distance between the bases, or a family of examples showing that no such bound holds.
:::

::: {.field label="Literature check (28 October 2026)"}
Work on sheaf diffusion and its stability was found; no base-change bound for this solve was found.
:::

::: {.field label="Discussion"}
[Issue 28](https://github.com/AlienMuse/grothendieckian-problems/issues/28) of the repository.
:::
:::

::: {.problem #problem-29 title="The training-to-serving deviation" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 6 (A chain of non-implications).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], Table 13.16.13, entry O16, pp. 3174–3175.
:::

::: {.field label="Status in the source"}
open.
:::

::: {.field label="Statement"}
Prove that “the training-to-serving deviation is bounded” for the forward map of [S02, Ch. 13.10–13.11], or remove the failure: the register asks for “a proved bound, or a tie-break that removes the failure”.
:::

::: {.field label="What the source establishes"}
Bitwise equality between training and serving is proved under stated contracts and fails outside them: “equality fails through the tie-break under rounding; no bound on the output difference is proved”.
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
[IEEE19]; [Hig02]; deterministic inference across parallel configurations [ZDY+25].
:::

::: {.field label="Solved when"}
A proved bound on the output difference between training and serving under the rounding model of Chapter 13.11, or a tie-break rule with a proof that it restores equality.
:::

::: {.field label="Literature check (28 October 2026)"}
Engineering work on deterministic inference was found [ZDY+25]; no proved bound for this forward map was found.
:::

::: {.field label="Discussion"}
[Issue 29](https://github.com/AlienMuse/grothendieckian-problems/issues/29) of the repository.
:::
:::

::: {.problem #problem-30 title="Monotone refinement budgets" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 5 (Report failure; abstain without evidence).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], Question 11.11.19, p. 2259.
:::

::: {.field label="Status in the source"}
X.
:::

::: {.field label="Statement"}
The recomputed refinement budget of [S02, Proposition 11.9.20] is not monotone along refinement. Question 11.11.19: “Is there a natural class of covers — closed under the refinements one actually performs — on which some useful instrument is monotone?” The source names two candidate classes, nerve-preserving refinements and split-only refinements.
:::

::: {.field label="What the source establishes"}
For both candidates the needed facts are unproved, and “No such theorem is currently available.” A proved monotone direction would let the diameter of a totally ordered class be read at its endpoints.
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
Cellular sheaves and their cohomology [HG19].
:::

::: {.field label="Solved when"}
A theorem identifying such a class and an instrument monotone on it, or a proof that each of the two named classes admits no useful monotone instrument.
:::

::: {.field label="Literature check (28 October 2026)"}
No result on monotone instruments under cover refinement was found.
:::

::: {.field label="Discussion"}
[Issue 30](https://github.com/AlienMuse/grothendieckian-problems/issues/30) of the repository.
:::
:::

::: {.problem #problem-31 title="How many ambiguity axes are there?" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 2 (Status is part of the type).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], Question 11.11.20, p. 2259.
:::

::: {.field label="Status in the source"}
X.
:::

::: {.field label="Statement"}
The indeterminacy calculus of [S02, Ch. 11.9] separates the ways a reported number can depend on arbitrary choices. “Chapter 11.9 opened with three and closed with four: the comparison link of Definition 11.9.42 was found only after the first three had been written up, which is evidence that the enumeration is incomplete.” Determine whether routing tie-breaking is a fifth axis with useful exact invariants, and whether the enumeration is complete.
:::

::: {.field label="What the source establishes"}
“Whether tie rules form a separate typed transformation family with useful exact invariants remains open; no fifth calculus is asserted.” Simplicial orientation and numerical precision are examined and dismissed with reasons.
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
Gauge and presentation invariance [BBCV21]; [HG19].
:::

::: {.field label="Solved when"}
A typed transformation family for tie rules with its exact invariants, or a proof that tie rules reduce to the four existing axes; a completeness theorem for a stated class of instruments also solves the problem.
:::

::: {.field label="Literature check (28 October 2026)"}
No result on this classification was found.
:::

::: {.field label="Discussion"}
[Issue 31](https://github.com/AlienMuse/grothendieckian-problems/issues/31) of the repository.
:::
:::

::: {.problem #problem-32 title="Second-order disagreement without engineering" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 5 (Report failure; abstain without evidence).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], §1.1.13, p. 15; §1.2.5, p. 22; §9.1.7, p. 1766.
:::

::: {.field label="Status in the source"}
open.
:::

::: {.field label="Statement"}
“On a graph, and under standard top-k routing, H2 vanishes identically.” The degree-two (gerbe) theory of disagreement among experts is therefore vacuous unless the cover is built for it: “The minimal non-vacuous configuration is four experts arranged as ∂Δ3, and it must be engineered deliberately.” Determine whether covers produced by a data-driven routing or cover-construction procedure, on natural tasks, carry non-zero second cohomology with the coefficient data of [S02].
:::

::: {.field label="What the source establishes"}
The source proves the vanishing results and warns that “engineering a structure into existence in order to measure it is a move that deserves suspicion.” A gerbe diagnostic is “vacuous unless the cover has a deliberate, data-justified sparse nerve with genuine two-dimensional cycles and explicitly defined coefficient data.”
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
[Gir71]; [HG19].
:::

::: {.field label="Solved when"}
A procedure, not tuned to produce two-cycles, whose covers on a published natural task carry a certified non-zero class in degree two; or a theorem that a stated class of procedures always yields vanishing second cohomology.
:::

::: {.field label="Literature check (28 October 2026)"}
No result on second cohomology of routing nerves was found.
:::

::: {.field label="Discussion"}
[Issue 32](https://github.com/AlienMuse/grothendieckian-problems/issues/32) of the repository.
:::
:::

::: {.problem #problem-33 title="Formalizing uniform circuit classes" tags="formalization · research level"}
::: {.field label="Thesis"}
Thesis 9 (State what is not established).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], Open Problem 13.15.B, p. 3135; cut ledger, Table 13.15.7, p. 3133.
:::

::: {.field label="Status in the source"}
OPEN.
:::

::: {.field label="Statement"}
“Formalise L-uniform circuit families and the AC$^0$ many-one reduction convention of Definition 2.14.5 to the point where clauses 4 and 5 of Theorem 13.13.24 become statable, and decide whether the Barrington construction of Chapter 2.14 is within reach of a proof term.”
:::

::: {.field label="What the source establishes"}
The source’s separation results use L-uniform circuit classes and Barrington’s theorem on paper; the machine-checked part stops at statements, and the cut ledger records that “a Barrington formalisation is a project in itself”.
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
[Bar89]; [BIS90]; a recent Lean formalisation of the non-uniform PARITY lower bound [Wes26].
:::

::: {.field label="Solved when"}
A Lean (or other assistant) library defining L-uniform circuit families and AC$^0$ many-one reductions in which clauses 4 and 5 of Theorem 13.13.24 are stated, together with either a formal proof of Barrington’s theorem or a documented estimate of what such a proof requires.
:::

::: {.field label="Literature check (28 October 2026)"}
The non-uniform PARITY lower bound has been formalised in Lean [Wes26]; uniformity and Barrington’s theorem were not found in mathlib or in formal-conjectures (GitHub code search).
:::

::: {.field label="Discussion"}
[Issue 33](https://github.com/AlienMuse/grothendieckian-problems/issues/33) of the repository.
:::
:::

::: {.problem #problem-34 title="A second kernel" tags="formalization · entry level"}
::: {.field label="Thesis"}
Thesis 6 (A chain of non-implications).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], Open Problem 13.15.D, p. 3135.
:::

::: {.field label="Status in the source"}
OPEN / D.
:::

::: {.field label="Statement"}
“Establish whether an independent type-checker covers the features used by the 13.11 and 13.13 developments, and if so make REPLAYED require two kernels rather than two machines.” Independent checkers for Lean 4 now exist [Car24; nanoda]; the problem is to elaborate the Lean declarations of [S02, Table 13.15.1] at a pinned toolchain and replay them under Lean’s kernel and under an independent checker.
:::

::: {.field label="What the source establishes"}
In the release no declaration was elaborated, and the source says of its replay status: “The present definition of REPLAYED is weaker than the name suggests, and this is stated rather than hidden.”
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
[BW05]; [MU21]; [Car24]; [nanoda].
:::

::: {.field label="Solved when"}
The declarations elaborated at a pinned toolchain and replayed by two independent kernels, with a report of the features used and of any declaration that one kernel rejects.
:::

::: {.field label="Literature check (28 October 2026)"}
Independent Lean 4 checkers were found [Car24; nanoda]; the Lean 4 repository contains a replay checker and an export format (src/LeanChecker.lean, src/LeanExport; GitHub code search, leanprover/lean4). No replay of these declarations was found.
:::

::: {.field label="Discussion"}
[Issue 34](https://github.com/AlienMuse/grothendieckian-problems/issues/34) of the repository.
:::
:::

::: {.problem #problem-35 title="The computational-univalence bridge" tags="formalization · programme level"}
::: {.field label="Thesis"}
Thesis 4 (Attention as descent).
:::

::: {.field label="Source"}
*GM-Omega-Infinity: Topos-Native Intelligence* [S02], Hypothesis 4.7.26, p. 1103.
:::

::: {.field label="Status in the source"}
X.
:::

::: {.field label="Statement"}
Build the checker of Hypothesis CU-MJ of [S02]: “There exists an approved external checker that: 1. represents proof-relevant paths and a univalent universe independently of Lean equality; 2. computes coercion along equivalences using cubical composition or an equivalent certified mechanism; 3. checks the higher coherences required by the transported family; 4. emits a replayable term rather than a Boolean success flag;” and 5. binds that term to the canonical target, equivalence, site, cover, universe and checker of the justification being transported.
:::

::: {.field label="What the source establishes"}
“No such integrated component is supplied by this chapter, so CU-MJ is graded X.” Every theorem that assumes it is conditional; the finite branch of the chapter does not need it.
:::

::: {.field label="Proposed by"}
[S02].
:::

::: {.field label="Background"}
[CCHM18]; [VMA21]; [Uni13].
:::

::: {.field label="Solved when"}
A checker satisfying the five clauses, and one transported justification from [S02, Ch. 4.7] checked end to end with its replayable term published.
:::

::: {.field label="Literature check (28 October 2026)"}
Cubical proof assistants and proof-transfer tools exist [CCHM18; VMA21]; no checker bound to Lean targets in the sense of clause 5 was found.
:::

::: {.field label="Discussion"}
[Issue 35](https://github.com/AlienMuse/grothendieckian-problems/issues/35) of the repository.
:::
:::

