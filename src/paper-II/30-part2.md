# Part II. The Five Research Subjects {.part #part-2}

Each of the five works of this part takes a named conjecture or programme as its research subject and records what its method establishes about it. The problems below are drawn from those records. None of them is the named conjecture, and a solution of any of them would not by itself prove one.

## *Arithmetic Spectral Descent* (research subject: the Riemann Hypothesis) {.unnumbered}

::: {.problem #problem-36 title="Polarization of a cyclotomic spectrum" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 8 (The rising sea).
:::

::: {.field label="Source"}
*Arithmetic Spectral Descent* [S03], Problem 24.18, p. 539 (restated as Problems 29.8 and 30.16); Criterion 57.5, p. 1145.
:::

::: {.field label="Status in the source"}
O (open).
:::

::: {.field label="Statement"}
Define a polarization of a cyclotomic spectrum: extra data on Real topological Hochschild homology (THR) $(\mathrm{THR}(R),O(2),\{\varphi^{\mathbb R}_p\})$, generalising an ample class or a Kähler form, such that (i) it induces a real quadratic form on $\pi_*(\mathrm{THR}(R)^{hO(2)})$ through a trace state; (ii) “the form is definite on primitive parts with respect to a Lefschetz decomposition”; and (iii) for $X$ smooth projective over $\mathbb F_q$ with an ample line bundle, “it recovers the Hodge index theorem on crystalline cohomology / the positivity underlying the Weil conjectures.”
:::

::: {.field label="What the source establishes"}
The source explains why (iii) is already delicate: crystalline cohomology carries no real structure, and the Katz–Messing comparison transports eigenvalues but not the positivity mechanism. Criterion 57.5 fixes a test: a proposed polarization solves the problem only if, applied to the topological Hochschild homology $\mathrm{THH}(C)$ of a curve $C$ over $\mathbb F_q$ of genus $g\ge1$, it proves $|\alpha_i|=\sqrt q$ for the inverse roots of the numerator of $Z(C,t)$ without invoking Weil’s theorem, Riemann–Roch on $C\times C$ or the Hodge index theorem.
:::

::: {.field label="Proposed by"}
[S03].
:::

::: {.field label="Background"}
[NS18]; [DMPR21]; [Del74].
:::

::: {.field label="Solved when"}
A definition satisfying (i)–(iii), with the test of Criterion 57.5 passed for every curve over a finite field. The bound $|\alpha_i|=\sqrt q$ is a theorem (Weil); the problem is to obtain it from the new structure.
:::

::: {.field label="Literature check (28 October 2026)"}
Work on Real topological Hochschild homology and its cyclotomic structure was found [DMPR21]; no notion of polarization of the required kind was found.
:::

::: {.field label="Discussion"}
[Issue 36](https://github.com/AlienMuse/grothendieckian-problems/issues/36) of the repository.
:::
:::

::: {.problem #problem-37 title="Construction Problem A1 on the syntomic stack" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 8 (The rising sea).
:::

::: {.field label="Source"}
*Arithmetic Spectral Descent* [S03], Problem 22.9, p. 483.
:::

::: {.field label="Status in the source"}
O.
:::

::: {.field label="Statement"}
Construct, on quasi-coherent sheaves on the syntomic stack $\mathbb Z_p^{\mathrm{syn}}$ (equivalently on $F$-gauges over $\mathbb Z_p$), a $\mathbb C$-linear endomorphism $\Theta$ of the underlying object after $\otimes_{W,\iota}\mathbb C$ such that (A1.1) on the Hodge–Tate locus $\Theta=-\tfrac{2\pi i}{\log q}\Theta_{\mathrm{Sen}}$ for objects pulled back from $\mathbb F_q$; (A1.2) $q^\Theta=\mathrm{Fr}_q^*$ for $F$-gauges coming from smooth proper $X/\mathbb F_q$; (A1.3) $\Theta$ is $\mathbb C$-linear, which “rules out semilinear operators”; and (A1.4) the regularized determinant $\det_\infty(s-\Theta)$ on motivic cohomology converges and equals $\zeta(X,s)$.
:::

::: {.field label="What the source establishes"}
The source isolates the difficulty in (A1.3): the Frobenius part of $\Theta$ is semilinear over $W$, and over $\mathbb Z_p$ no power of $\varphi$ is $W$-linear. “The syntomic stack exists, but the operator on it does not—yet.”
:::

::: {.field label="Proposed by"}
[S03].
:::

::: {.field label="Background"}
[BS22]; [BL22]; [Dri20].
:::

::: {.field label="Solved when"}
A construction satisfying (A1.1)–(A1.4), or a proof that no endomorphism with (A1.1)–(A1.3) exists.
:::

::: {.field label="Literature check (28 October 2026)"}
The Sen operator on the Hodge–Tate stack is known [BL22; Dri20]; no operator with (A1.1)–(A1.4) was found.
:::

::: {.field label="Discussion"}
[Issue 37](https://github.com/AlienMuse/grothendieckian-problems/issues/37) of the repository.
:::
:::

::: {.problem #problem-38 title="Archimedean Frobenius from quaternionic THH" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 8 (The rising sea).
:::

::: {.field label="Source"}
*Arithmetic Spectral Descent* [S03], Problem 28.13, p. 604; Construction 28.14, p. 605.
:::

::: {.field label="Status in the source"}
O (first half answered since; see the literature check).
:::

::: {.field label="Statement"}
Problem 28.13 of [S03] asks two questions. The first — whether there is “a lift of THH to genuine Pin(2)-spectra rather than O(2)-spectra” — has been answered: quaternionic topological Hochschild homology THQ, defined for rings with twisted $C_4$-action, carries a $\mathrm{Pin}(2)$-action [AMP26]. The second remains: is its $\mathrm{Pin}(2)$-homotopy fixed-point theory “the correct 𝜑∞ for symplectically self-dual motives, with 𝑂(2) handling the orthogonal ones?” Concretely, determine whether $\mathrm{THQ}(R)^{h\mathrm{Pin}(2)}$ carries an operator $\Theta_\infty$ satisfying the analogue of requirement (C′1) of Construction 28.14 — its half-line spectrum, with Hodge multiplicities, gives the archimedean local factors of symplectically self-dual motives by $\det_\infty((s-\Theta_\infty)/2\pi)$.
:::

::: {.field label="What the source establishes"}
The source calls the question “a well-posed question in equivariant stable homotopy theory, independent of RH”, and states that “No existing construction is known”; that statement is corrected here (it is recorded in the errata of the repository). Construction 28.14 lists the requirements (C′1)–(C′4) for the orthogonal case.
:::

::: {.field label="Proposed by"}
[S03].
:::

::: {.field label="Background"}
[AMP26]; [DMPR21]; [Man16]; [NS18].
:::

::: {.field label="Solved when"}
An operator on $\mathrm{THQ}(R)^{h\mathrm{Pin}(2)}$ for a stated class of rings with the required structure, with a proof of the analogue of (C′1) for symplectically self-dual motives in that class; or a proof that no natural operator can satisfy it.
:::

::: {.field label="Literature check (28 October 2026)"}
Found: Angelini-Knoll, Merling and Péroux construct THQ with its Pin(2)-action (arXiv:2409.18187, 2024; Adv. Math. 2026) [AMP26]. This answers the first question of Problem 28.13; no work on the second was found.
:::

::: {.field label="Discussion"}
[Issue 38](https://github.com/AlienMuse/grothendieckian-problems/issues/38) of the repository.
:::
:::

::: {.problem #problem-39 title="A certified inertia for the pole-removed Weil form" tags="machine · entry level"}
::: {.field label="Thesis"}
Thesis 9 (State what is not established).
:::

::: {.field label="Source"}
*Arithmetic Spectral Descent* [S03], Criterion 58.9 (falsification predicate F2), p. 1169; Proposition 46.5 and Remark 46.13, pp. xxxv, 919.
:::

::: {.field label="Status in the source"}
E (finite measurement) / O.
:::

::: {.field label="Statement"}
For sixty-three cubic-spline test spaces $V_{T,N}$ ($0.15\le T\le 3$, $4\le N\le 64$) the source measured, in floating point with tolerance $10^{-9}$, that the pole-removed Weil form $B_N=W_N-P_N$ has inertia $(N-1,1)$. Certify this measurement in interval or exact arithmetic for each configuration — certify $N-1$ positive eigenvalues and exhibit a vector $z$ with a certified enclosure of $B_N(z,z)<0$ — or show for some configuration that the certified inertia differs, which is falsification predicate F2 of [S03, Criterion 58.9].
:::

::: {.field label="What the source establishes"}
Under RH the full Weil form is positive semidefinite and $n_-(B_N)\le1$ (Corollary 46.11); the lower bound $n_-(B_N)\ge1$ is not proved conditionally or otherwise (Warning 46.12). The measurement is finite evidence: “What the data exclude is a large second negative direction. What they do not exclude is a small one.” F2 asks for “the computation certified in interval arithmetic”.
:::

::: {.field label="Proposed by"}
[S03].
:::

::: {.field label="Background"}
Weil positivity at the archimedean place [CC21]; interval arithmetic [Joh17]; certified computation of zeta zeros [PT21]; certification for other finite truncations of the Weil form [Gro26].
:::

::: {.field label="Solved when"}
Certified inertia for all sixty-three configurations of Proposition 46.5, with the code and the enclosures published; a configuration whose certified inertia is not $(N-1,1)$ also solves the problem, by firing F2. The result is a statement about finitely many matrices; it is not evidence for or against RH.
:::

::: {.field label="Literature check (28 October 2026)"}
A certification rule and an interval factorization for the Galerkin truncations of the Weil quadratic form of Connes, van Suijlekom, Consani and Moscovici were found [Gro26]; no certified computation of the inertia of the Gram matrices of these sixty-three test spaces was found.
:::

::: {.field label="Discussion"}
[Issue 39](https://github.com/AlienMuse/grothendieckian-problems/issues/39) of the repository.
:::
:::

## *Fractured Adelic Geometry* (research subject: the conjecture of Birch and Swinnerton-Dyer) {.unnumbered}

::: {.problem #problem-40 title="The Tamagawa factor as a local term" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 9 (State what is not established).
:::

::: {.field label="Source"}
*Fractured Adelic Geometry* [S04], Problem 22.7.1, p. 173; §2.8.1, p. 19; §56.3, p. 437.
:::

::: {.field label="Status in the source"}
OPEN.
:::

::: {.field label="Statement"}
The source proposes three constructions of the bad-prime term $c_p$ of the conjecture of Birch and Swinnerton-Dyer: a vertical intersection multiplicity on the arithmetic surface, a Lefschetz–Verdier term of a fixed-point stack, and a determinant defect of the prismatic/Néron component lattice. Problem 22.7.1: “Construct the three local objects just described and prove that each has Euler characteristic c_p, compatibly with change of model, Frobenius action, and the integral orientation of the fundamental line.”
:::

::: {.field label="What the source establishes"}
The identification of $c_p$ as a Lefschetz–Verdier local term is listed among the book’s novelties, and the source fixes the test: “This is a particularly useful falsification test. Tate’s algorithm gives c_p independently for every database curve. If a proposed prismatic or fixed-point formula disagrees even once, that local construction is wrong. No appeal to BSD can repair such a disagreement.” The book lists this among the items that are “testable now, independently of BSD.”
:::

::: {.field label="Proposed by"}
[S04].
:::

::: {.field label="Background"}
[Tat75]; [BK90]; [BS22].
:::

::: {.field label="Solved when"}
The three constructions with proofs that each has Euler characteristic $c_p$ with the stated compatibilities; or a curve and a prime at which a proposed construction disagrees with Tate’s algorithm, which refutes that construction. The problem concerns local terms and does not bear on the truth of BSD.
:::

::: {.field label="Literature check (28 October 2026)"}
No prismatic or fixed-point formula for the Tamagawa factor was found.
:::

::: {.field label="Discussion"}
[Issue 40](https://github.com/AlienMuse/grothendieckian-problems/issues/40) of the repository.
:::
:::

::: {.problem #problem-41 title="The arithmetic flow" tags="mathematical · programme level"}
::: {.field label="Thesis"}
Thesis 8 (The rising sea).
:::

::: {.field label="Source"}
*Fractured Adelic Geometry* [S04], Problem 53.2.4 (Obstruction IV), p. 416; Problem 4.5.1, p. 37.
:::

::: {.field label="Status in the source"}
OPEN.
:::

::: {.field label="Statement"}
Construct a strongly continuous flow on a cohomology theory over $\operatorname{Spec}\mathbb Z$ whose primitive closed orbits are the primes, the orbit at $p$ having length $\log p$, with no spurious orbits and with a generator satisfying the weight adjunction. In the form of Problem 4.5.1: a foliated or laminated space with a flow and a leafwise cohomology admitting duality and regularized determinants, whose Lefschetz trace formula is the explicit formula.
:::

::: {.field label="What the source establishes"}
“The flow Φ𝑡 is postulated, not built. No ℝ≥0-action has ever been constructed on any cohomology theory over Specℤ whose primitive closed orbits are the primes with lengths log p”. For Problem 4.5.1: “No object satisfying these requirements is presently known.” The cyclotomic structure of THH supplies $\psi_p$ at each prime; the interpolation to a continuous action is missing.
:::

::: {.field label="Proposed by"}
Deninger [Den98]; restated, with the source’s axioms, in [S04].
:::

::: {.field label="Background"}
[Den98]; [NS18].
:::

::: {.field label="Solved when"}
A construction with the stated properties, or a no-go theorem showing that no $\mathbb R_{\ge0}$-action of the required kind exists on any cohomology of $\operatorname{Spec}\mathbb Z$ (item (ii) of the refutation list of [S04, §2.8.1]).
:::

::: {.field label="Literature check (28 October 2026)"}
Trace formulas for foliated flows and regularized-determinant formulas in Deninger’s framework were found; no construction over Spec ℤ was found.
:::

::: {.field label="Discussion"}
[Issue 41](https://github.com/AlienMuse/grothendieckian-problems/issues/41) of the repository.
:::
:::

::: {.problem #problem-42 title="Sub-conductor rank detection" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 12 (Judge a method by its open ledger).
:::

::: {.field label="Source"}
*Fractured Adelic Geometry* [S04], Question 46.2.1, p. 354.
:::

::: {.field label="Status in the source"}
OPEN.
:::

::: {.field label="Statement"}
Does there exist a natural family $\mathcal F_X$ of elliptic curves, a function $P(X)=X^{o(1)}$, and explicit statistics $S_X$ depending only on $\{a_p(E): p\le P(X)\}$, such that the conditional laws of $S_X$ for analytic rank $0$, $1$ and at least $2$ have distinct non-degenerate limits after the root number and all known local confounders are matched?
:::

::: {.field label="What the source establishes"}
The source explains the clause on confounders: “The matching clause matters. Without it, a classifier may merely learn the functional-equation sign or a database convention.” Either answer is informative: “A positive answer would ask for a new family trace formula; a negative answer would also be informative by locating the finite-sample origin of the observed signal.”
:::

::: {.field label="Proposed by"}
[S04].
:::

::: {.field label="Background"}
[HLOP22]; [Zub23]; [BKLPR15]; neural rank prediction from Frobenius traces [BCD+26].
:::

::: {.field label="Solved when"}
A theorem establishing distinct limits for a stated family and statistic with $P(X)=X^{o(1)}$, or a theorem that no statistic of this kind separates the ranks after matching.
:::

::: {.field label="Literature check (28 October 2026)"}
Machine-learning prediction of analytic rank from Frobenius traces has been reported with high accuracy [BCD+26] and murmurations studied [HLOP22; Zub23]; no theorem of the requested form, with the matching clause, was found.
:::

::: {.field label="Discussion"}
[Issue 42](https://github.com/AlienMuse/grothendieckian-problems/issues/42) of the repository.
:::
:::

::: {.problem #problem-43 title="Murmurations from the flow: a falsification test" tags="machine · entry level"}
::: {.field label="Thesis"}
Thesis 9 (State what is not established).
:::

::: {.field label="Source"}
*Fractured Adelic Geometry* [S04], Conjecture 36.4.6, pp. 276–277.
:::

::: {.field label="Status in the source"}
OPEN (a falsifiable prediction).
:::

::: {.field label="Statement"}
If the framework of [S04] is correct, the murmuration density arises as a transition term in its Lefschetz–Verdier localisation, and three computable predictions follow: (i) $y=p/N$ is the natural coordinate, and no other combination of $p$ and $N$ appears in the leading term; (ii) the density for elliptic curves, if it exists, has the same oscillation frequencies as the modular-form density $M_2$; (iii) the rank-conditioned densities are governed by the same density with the root number replaced by the Selmer fixed-point class. Carry out the tests.
:::

::: {.field label="What the source establishes"}
“Each clause is falsifiable by computation. Clause (i) fails if any family shows a leading term depending on p and N other than through p/N; clause (ii) fails if the observed elliptic-curve frequencies differ from those of M2.” The protocol is in Chapter 55.
:::

::: {.field label="Proposed by"}
[S04].
:::

::: {.field label="Background"}
[HLOP22]; [Zub23]; [SS25]; [Cow24].
:::

::: {.field label="Solved when"}
The tests of clauses (i) and (ii) carried out under the protocol of [S04, Ch. 55] against the densities of [Zub23] and [SS25], with data and code published and the outcome reported in either direction; clause (iii) when the Selmer class is computable.
:::

::: {.field label="Literature check (28 October 2026)"}
A conjectural explicit murmuration density for elliptic curves ordered by height has been given [SS25], and murmurations have been derived from ratios conjectures [Cow24]; these supply what clause (ii) is tested against. No test of the three clauses was found.
:::

::: {.field label="Discussion"}
[Issue 43](https://github.com/AlienMuse/grothendieckian-problems/issues/43) of the repository.
:::
:::

## *The Archimedean Prism* (research subject: the Hodge conjecture) {.unnumbered}

::: {.problem #problem-44 title="The Hodge decomposition in Lean" tags="formalization · programme level"}
::: {.field label="Thesis"}
Thesis 9 (State what is not established).
:::

::: {.field label="Source"}
*The Archimedean Prism* [S05], Problem 71.11.1, p. 1027; dossier, p. 1034; The five volumes, p. xv.
:::

::: {.field label="Status in the source"}
open.
:::

::: {.field label="Statement"}
“Formalise the Hodge decomposition for compact Kähler manifolds in Lean 4 with mathlib, the single largest absent prerequisite identified in Chapter 64.”
:::

::: {.field label="What the source establishes"}
The source records the verdict that “the Hodge conjecture cannot presently even be stated in Lean 4 with mathlib”, and estimates the formalisation “as an effort on the order of the Liquid Tensor Experiment.” Its dossier limits what success means: “Success would enable formal statements of the later conjectures; it would prove none of them by itself.” Problem 71.11.2 (Chow groups and the cycle class map) is the other missing prerequisite.
:::

::: {.field label="Proposed by"}
[S05].
:::

::: {.field label="Background"}
[Voi02b]; [mC20]; [Sch22].
:::

::: {.field label="Solved when"}
A Lean 4 development, accepted into Mathlib or released as a library building against it, that defines compact Kähler manifolds and proves the Hodge decomposition of their de Rham cohomology.
:::

::: {.field label="Literature check (28 October 2026)"}
GitHub code search (2026-10-28) found in mathlib a Hodge star on exterior powers and algebraic Kähler differentials, but no Kähler manifolds and no Hodge decomposition; formal-conjectures contains no Hodge-theoretic statement.
:::

::: {.field label="Discussion"}
[Issue 44](https://github.com/AlienMuse/grothendieckian-problems/issues/44) of the repository.
:::
:::

::: {.problem #problem-45 title="No δ-structure on the archimedean prism" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 9 (State what is not established).
:::

::: {.field label="Source"}
*The Archimedean Prism* [S05], Problem 71.3.4, p. 1023; dossier, p. 1029.
:::

::: {.field label="Status in the source"}
open.
:::

::: {.field label="Statement"}
“Make precise, as a no-go theorem, the claim that the archimedean prism carries no 𝛿-structure and hence no literal Frobenius lift.”
:::

::: {.field label="What the source establishes"}
“Chapter 16 argues the analogy with prismatic cohomology is structural only; a no-go theorem would settle the point rather than assert it.” The dossier sets the standard: “A no-go theorem must quantify over all functorial candidate operations and identify an invariant they cannot satisfy; observing that the current construction lacks one is not enough.”
:::

::: {.field label="Proposed by"}
[S05].
:::

::: {.field label="Background"}
δ-rings [Joy85; Bui05]; prisms [BS22].
:::

::: {.field label="Solved when"}
A theorem that quantifies over all functorial operations on the archimedean prism of [S05, Ch. 13–17] in a stated sense and proves that none is a δ-structure (or a Frobenius lift), by exhibiting an invariant that every such operation would have to satisfy and does not; or a functorial δ-structure, which would refute the claim.
:::

::: {.field label="Literature check (28 October 2026)"}
No result on δ-structures for archimedean or real Hodge-theoretic analogues of prisms was found.
:::

::: {.field label="Discussion"}
[Issue 45](https://github.com/AlienMuse/grothendieckian-problems/issues/45) of the repository.
:::
:::

::: {.problem #problem-46 title="Independence of the twelve prism axioms" tags="mathematical · entry level"}
::: {.field label="Thesis"}
Thesis 12 (Judge a method by its open ledger).
:::

::: {.field label="Source"}
*The Archimedean Prism* [S05], Problem 71.8.1, p. 1026; dossier, p. 1032.
:::

::: {.field label="Status in the source"}
open.
:::

::: {.field label="Statement"}
“Prove that the twelve prism axioms AP1–AP12 are logically independent by exhibiting, for each, a model satisfying the other eleven and failing it.”
:::

::: {.field label="What the source establishes"}
“Theorem 46.4.1 states the axioms; their independence is asserted but not demonstrated.” The dossier: “The twelve axioms are individually motivated, but motivation does not prove logical independence.”
:::

::: {.field label="Proposed by"}
[S05].
:::

::: {.field label="Background"}
Hodge theory [Del71]; the axioms and their sources are in [S05, Ch. 46].
:::

::: {.field label="Solved when"}
Twelve models, the $k$-th satisfying every axiom except AP$k$, each verified against the definitions of [S05, Ch. 46]; or a proof that one axiom follows from the others, which is a correction to the source.
:::

::: {.field label="Literature check (28 October 2026)"}
No work on these axioms outside [S05] was found.
:::

::: {.field label="Discussion"}
[Issue 46](https://github.com/AlienMuse/grothendieckian-problems/issues/46) of the repository.
:::
:::

::: {.problem #problem-47 title="Descent beyond the polarized case" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 5 (Report failure; abstain without evidence).
:::

::: {.field label="Source"}
*The Archimedean Prism* [S05], Problem 71.3.3, p. 1023; dossier, p. 1029.
:::

::: {.field label="Status in the source"}
open.
:::

::: {.field label="Statement"}
“Determine whether the descent theorem Theorem 15.4.2 holds for non-polarisable mixed Hodge structures, or exhibit the first obstruction to it.”
:::

::: {.field label="What the source establishes"}
In the source, “descent along the prism is proved only in the polarised pure case.” The dossier explains what changes: “Nonpolarisable mixed structures have nonsemisimple extension data and weight filtrations that need not split; automorphism groupoids can cease to be reductive”, and notes that the answer may be a counterexample rather than an extension theorem.
:::

::: {.field label="Proposed by"}
[S05].
:::

::: {.field label="Background"}
[Del71]; [Sch73]; [CDK95].
:::

::: {.field label="Solved when"}
A proof of the descent theorem for non-polarisable mixed Hodge structures in a stated class, or an explicit mixed Hodge structure for which descent fails, with the obstruction identified.
:::

::: {.field label="Literature check (28 October 2026)"}
No result on descent along the archimedean prism was found outside [S05].
:::

::: {.field label="Discussion"}
[Issue 47](https://github.com/AlienMuse/grothendieckian-problems/issues/47) of the repository.
:::
:::

::: {.problem #problem-48 title="A prism reading of Voisin’s counterexample" tags="mathematical · entry level"}
::: {.field label="Thesis"}
Thesis 9 (State what is not established).
:::

::: {.field label="Source"}
*The Archimedean Prism* [S05], Problem 71.6.6, p. 1025; dossier, p. 1031.
:::

::: {.field label="Status in the source"}
open.
:::

::: {.field label="Statement"}
“Compute the prism obstruction class of Voisin’s 2002 Weil-torus counterexample and verify that it is exactly the projectivity obstruction, not a new one.”
:::

::: {.field label="What the source establishes"}
“Theorem 37.2.4 predicts the counterexample strikes at the projectivity step; an explicit computation would confirm the negation of falsifier F8.” Voisin’s examples [Voi02] show that the Hodge conjecture fails for compact Kähler manifolds that are not projective.
:::

::: {.field label="Proposed by"}
[S05].
:::

::: {.field label="Background"}
[Voi02]; [Voi02b].
:::

::: {.field label="Solved when"}
An explicit computation of the prism obstruction class for the tori of [Voi02], showing that it is the projectivity obstruction of [S05, Theorem 37.2.4]; a computation showing that it is a different class refutes the prediction.
:::

::: {.field label="Literature check (28 October 2026)"}
No prism-theoretic analysis of Voisin’s examples was found outside [S05].
:::

::: {.field label="Discussion"}
[Issue 48](https://github.com/AlienMuse/grothendieckian-problems/issues/48) of the repository.
:::
:::

## *Strained Prismatic Geometry* (research subject: the $abc$ conjecture) {.unnumbered}

::: {.problem #problem-49 title="Close the formal algebra leaf" tags="formalization · entry level"}
::: {.field label="Thesis"}
Thesis 9 (State what is not established).
:::

::: {.field label="Source"}
*Strained Prismatic Geometry* [S06], Problem 62.1.5 (rank 2 of the critical path), p. 1275.
:::

::: {.field label="Status in the source"}
OPEN.
:::

::: {.field label="Statement"}
With pinned Lean and Mathlib versions, “Discharge PO-090 with definitions whose types separate a p-derivation from an ordinary derivation, proofs of the sum and product identities including p = 2, compatibility with the induced Frobenius lift, executable regression examples, no admitted declarations, and an axiom report containing only the approved logical foundations.”
:::

::: {.field label="What the source establishes"}
“This ranks second because the mathematics is known and the acceptance test is finite.” Failures of tooling do not count against the mathematics: “A library or elaboration failure is an engineering result, not a refutation.” The repository gives the statements in Lean (formal/GrothendieckianProblems/P49.lean).
:::

::: {.field label="Proposed by"}
[S06].
:::

::: {.field label="Background"}
[Joy85]; [Bui05]; [BS22]; [mC20].
:::

::: {.field label="Solved when"}
Proofs of the statements in formal/GrothendieckianProblems/P49.lean, with no sorry, no new axioms, and the regression examples of PO-090, checked at the pinned toolchain.
:::

::: {.field label="Literature check (28 October 2026)"}
GitHub code search (2026-10-28) found no δ-ring or p-derivation in mathlib.
:::

::: {.field label="Discussion"}
[Issue 49](https://github.com/AlienMuse/grothendieckian-problems/issues/49) of the repository.
:::
:::

::: {.problem #problem-50 title="Toward an algorithm for prismatic cohomology" tags="machine · research level"}
::: {.field label="Thesis"}
Thesis 12 (Judge a method by its open ledger).
:::

::: {.field label="Source"}
*Strained Prismatic Geometry* [S06], Obstruction 49.6.6, pp. 1029–1030.
:::

::: {.field label="Status in the source"}
OPEN.
:::

::: {.field label="Statement"}
“There is presently no general terminating algorithm which, from equations for an arbitrary p-adic formal scheme, computes its absolute prismatic cohomology together with derived completion, Nygaard filtration, Frobenius, and effective descent as an F-gauge”. “The frontier relevant to this book has five layers”: absolute descent; integral semistable gauges for curves with bad reduction, including the primes 2 and 3; the Habiro–prismatic comparison; archimedean assembly; and the global strain trace. Give a terminating, certified algorithm for one layer.
:::

::: {.field label="What the source establishes"}
The companion package of [S06] supplies finite inputs and hard failure states, and “implements none of these by renaming a local matrix.”
:::

::: {.field label="Proposed by"}
[S06].
:::

::: {.field label="Background"}
[BS22]; [BL22].
:::

::: {.field label="Solved when"}
A terminating algorithm for one of the five layers on a stated class of inputs, with a proof of correctness and an implementation whose outputs agree with known computations.
:::

::: {.field label="Literature check (28 October 2026)"}
Explicit computations of prismatic and syntomic cohomology in special cases were found; no general algorithm for any of the five layers was found.
:::

::: {.field label="Discussion"}
[Issue 50](https://github.com/AlienMuse/grothendieckian-problems/issues/50) of the repository.
:::
:::

::: {.problem #problem-51 title="The real-place gauge" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 8 (The rising sea).
:::

::: {.field label="Source"}
*Strained Prismatic Geometry* [S06], Problem 62.1.7 (rank 4 of the critical path), p. 1276.
:::

::: {.field label="Status in the source"}
OPEN.
:::

::: {.field label="Statement"}
In the analytic-stack and condensed setting of [S06, Ch. 17], “Construct the gauge stack of PO-017; prove the uniqueness, finite-place compatibility, coherent all-place gluing, Arakelov degree comparison, and exceptional-operation functoriality of PO-018–PO-022; and settle the archimedean coefficient overlap and dualisability issues represented by PO-097–PO-098.”
:::

::: {.field label="What the source establishes"}
The target is typed but no existence theorem is available. The source gives the falsifier: “A non-zero principal-rescaling defect, failure of real descent, or failure of dualisability for the required leg destroys this version of the all-place assembly.”
:::

::: {.field label="Proposed by"}
[S06].
:::

::: {.field label="Background"}
[Sch19]; [BS22]; [Efi24].
:::

::: {.field label="Solved when"}
A construction with proofs of PO-017–PO-022 and PO-097–PO-098, or an instance of one of the three named falsifiers.
:::

::: {.field label="Literature check (28 October 2026)"}
No construction of an archimedean gauge stack of this kind was found.
:::

::: {.field label="Discussion"}
[Issue 51](https://github.com/AlienMuse/grothendieckian-problems/issues/51) of the repository.
:::
:::

::: {.problem #problem-52 title="The gluing problem for the global substrate" tags="mathematical · programme level"}
::: {.field label="Thesis"}
Thesis 8 (The rising sea).
:::

::: {.field label="Source"}
*Strained Prismatic Geometry* [S06], Problem 18.1.5, p. 352.
:::

::: {.field label="Status in the source"}
open.
:::

::: {.field label="Statement"}
Construct an analytic stack $\mathfrak S$ with morphisms $\mathfrak S_v\to\mathfrak S$ for every place $v$ of $\mathbb Q$ and a morphism $\operatorname{Spec}\mathbb Z\to\mathfrak S$ such that (i) $D(\mathfrak S)$ maps to $D(\mathfrak S_v)$ for every $v$, compatibly with the rational realisations; (ii) the local structures — Frobenius and Nygaard filtration at finite $v$, weight filtration and dilation at $\infty$ — are matched by the comparison data; and (iii) $\mathfrak S$ is not terminal.
:::

::: {.field label="What the source establishes"}
“Condition (iii) is what makes the problem non-trivial: a terminal object satisfies (i) and (ii) vacuously.” The legs can be compared only through $\mathbb Q$ (Remark 18.1.4), and Obstruction 18.1.6 shows that a Frobenius datum on a glued object degenerates at infinity.
:::

::: {.field label="Proposed by"}
[S06].
:::

::: {.field label="Background"}
[Sch19]; [BL22]; [Dri20].
:::

::: {.field label="Solved when"}
A construction satisfying (i)–(iii), or a proof that every analytic stack satisfying (i) and (ii) is terminal.
:::

::: {.field label="Literature check (28 October 2026)"}
No construction of this kind was found.
:::

::: {.field label="Discussion"}
[Issue 52](https://github.com/AlienMuse/grothendieckian-problems/issues/52) of the repository.
:::
:::

## *The Arithmetic Topos* (research subject: the Langlands programme) {.unnumbered}

::: {.problem #problem-53 title="The multiplicative-group gate" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 9 (State what is not established).
:::

::: {.field label="Source"}
*The Arithmetic Topos* [S07], Criterion 1.26, p. 28.
:::

::: {.field label="Status in the source"}
FORMAL TARGET.
:::

::: {.field label="Statement"}
Let $\mathrm{Bun}^{\mathrm{ar}}_{\mathbb G_m}$ be the arithmetic Picard stack of the global arithmetic curve $\mathfrak X_{\mathbb Z}$ of [S07] and $\mathrm{Gauge}$ its category of gauge sheaves. Construct them and prove or refute that $\zeta(\mathrm{TC}(\Phi\mid\mathrm{Gauge}(\mathrm{Bun}^{\mathrm{ar}}_{\mathbb G_m})),s)=\pi^{-s/2} \Gamma(s/2)\zeta(s)$, the completed Riemann zeta function, with the archimedean factor produced by the archimedean chart and not inserted.
:::

::: {.field label="What the source establishes"}
The source calls this “the primary go/no-go test for the framework”: “If the framework yields anything else — in particular, if it yields 𝜁(𝑠) without the Γ-factor, or with a Γ-factor of the wrong argument — then it is wrong, and no amount of repair at higher strata will save it.” “This criterion is designated for formal verification; its current status is recorded in Appendix F.”
:::

::: {.field label="Proposed by"}
[S07].
:::

::: {.field label="Background"}
Archimedean factors as regularized determinants [Den98]; [CC21]; [NS18].
:::

::: {.field label="Solved when"}
A construction of the objects in the abelian case and a proof of the displayed identity, or a proof that the construction yields a different function, which refutes the framework as stated. The completed zeta function and its functional equation are classical; the problem is whether this construction produces them.
:::

::: {.field label="Literature check (28 October 2026)"}
No construction of the arithmetic Picard stack of this framework was found outside [S07].
:::

::: {.field label="Discussion"}
[Issue 53](https://github.com/AlienMuse/grothendieckian-problems/issues/53) of the repository.
:::
:::

::: {.problem #problem-54 title="The first falsification test for GL$_2$" tags="mathematical · research level"}
::: {.field label="Thesis"}
Thesis 9 (State what is not established).
:::

::: {.field label="Source"}
*The Arithmetic Topos* [S07], Problem 28.28, pp. 1108–1109.
:::

::: {.field label="Status in the source"}
CONJECTURE (a falsification test).
:::

::: {.field label="Statement"}
“For the standard GL2 monoid over Q, construct a global distribution on the rank-one stratum whose local normal residue is the coefficient of” Proposition 28.16 of [S07], “and prove that its spectral expansion is exactly the sum of the trivial, special, and maximal-parabolic terms removed in Altuğ’s Poisson reorganisation.”
:::

::: {.field label="What the source establishes"}
A mismatch of coefficients would refute the simplest form of the source’s Conjecture 28.20. The problem precedes functoriality on purpose: “It asks whether the diagnosis reproduces a known rank-one calculation without changing its constants. A framework that cannot pass this comparison has no claim on the general problem.”
:::

::: {.field label="Proposed by"}
[S07]; the rank-one calculation is Altuğ’s [Alt15].
:::

::: {.field label="Background"}
[Alt15]; [EEKW24].
:::

::: {.field label="Solved when"}
The distribution constructed and its spectral expansion proved equal to the terms removed in [Alt15], or a proof that the coefficients differ.
:::

::: {.field label="Literature check (28 October 2026)"}
Altuğ’s Beyond Endoscopy computations for GL$_2$ over the rationals [Alt15] and their extension to totally real fields, which removes the trivial and special representations by Poisson summation on the regular elliptic terms [EEKW24], were found; no boundary-resolution reading of them was found.
:::

::: {.field label="Discussion"}
[Issue 54](https://github.com/AlienMuse/grothendieckian-problems/issues/54) of the repository.
:::
:::

::: {.problem #problem-55 title="Ambidexterity over the arithmetic base" tags="mathematical · programme level"}
::: {.field label="Thesis"}
Thesis 8 (The rising sea).
:::

::: {.field label="Source"}
*The Arithmetic Topos* [S07], Problem 40.11, p. 1603.
:::

::: {.field label="Status in the source"}
CONJECTURE.
:::

::: {.field label="Statement"}
Let $q\colon\mathrm{Bun}_G(\mathfrak X_{\mathbb Z})\to\mathrm{pt}$ be the structure map. Prove or refute that $q_!\simeq q_*$ on $\mathrm{Shv}_{\mathcal N}(\mathrm{Bun}_G(\mathfrak X_{\mathbb Z}))$ after Whittaker renormalisation; if the equivalence holds only after a renormalisation, identify it explicitly and determine whether it is canonical.
:::

::: {.field label="What the source establishes"}
“This is the load-bearing hypothesis of the entire framework.” Over a curve the corresponding statement, miraculous duality, is a theorem of Drinfeld and Gaitsgory; over $\mathfrak X_{\mathbb Z}$ the local finiteness its proof uses is unavailable. “It is also the gap about which the least can currently be said.”
:::

::: {.field label="Proposed by"}
[S07]; over a curve the source cites miraculous duality as a theorem of Drinfeld and Gaitsgory; see [Gai18] and [AGK+20].
:::

::: {.field label="Background"}
[DG15]; [Gai18]; [AGK+20].
:::

::: {.field label="Solved when"}
A proof or a refutation of the equivalence, with the renormalisation identified if one is needed.
:::

::: {.field label="Literature check (28 October 2026)"}
Miraculous duality and duality for automorphic sheaves over curves were found [Gai18; AGK+20]; no arithmetic analogue was found.
:::

::: {.field label="Discussion"}
[Issue 55](https://github.com/AlienMuse/grothendieckian-problems/issues/55) of the repository.
:::
:::

::: {.problem #problem-56 title="Construct the global arithmetic curve" tags="mathematical · programme level"}
::: {.field label="Thesis"}
Thesis 8 (The rising sea).
:::

::: {.field label="Source"}
*The Arithmetic Topos* [S07], Problem 40.10, p. 1602.
:::

::: {.field label="Status in the source"}
CONJECTURE.
:::

::: {.field label="Statement"}
Exhibit a condensed analytic stack over the sphere spectrum satisfying the eight clauses of the definition of the global arithmetic curve $\mathfrak X_{\mathbb Z}$ [S07, Definition 10.15] — finite syntomic charts, an archimedean chart, a restricted adelic halo with a rational diagonal, the gluing as a homotopy fibre product, an absolute Frobenius, a gauge map to $\mathbb A^1/\mathbb G_m$, a place map to $\operatorname{Spec}\mathbb Z$, and a fundamental class in degree three — prove it unique up to canonical equivalence, and equip it with a six-functor formalism with proper base change and Verdier duality.
:::

::: {.field label="What the source establishes"}
“What exists at present is a specification and two of its charts.” The finite charts are theorems of Bhatt–Lurie and Drinfeld; the archimedean chart is stipulated. “The obstacle is not the charts. It is the gluing, and the reason is specific. Adelic descent along a restricted product is not a standard operation in any existing formalism.”
:::

::: {.field label="Proposed by"}
[S07].
:::

::: {.field label="Background"}
[BL22]; [Dri20]; [BL95]; [FS21]; [Sch19].
:::

::: {.field label="Solved when"}
A construction with the eight clauses, the uniqueness statement and the six-functor formalism, or a proof that no object satisfies the eight clauses.
:::

::: {.field label="Literature check (28 October 2026)"}
No construction of this kind was found.
:::

::: {.field label="Discussion"}
[Issue 56](https://github.com/AlienMuse/grothendieckian-problems/issues/56) of the repository.
:::
:::

::: {.problem #problem-57 title="Coherence for arithmetic modes" tags="formalization · research level"}
::: {.field label="Thesis"}
Thesis 11 (Creating language).
:::

::: {.field label="Source"}
*The Arithmetic Topos* [S07], Problem 6.29, p. 228.
:::

::: {.field label="Status in the source"}
CONJECTURE.
:::

::: {.field label="Statement"}
For the modal directed type theory $\mathrm{TT}^{\mathrm{comp}}_{\mathrm{KH}}$ of [S07, Ch. 6], construct a finite presentation of its mode two-category and “prove a coherence theorem deciding equality of generated two-cells”, while retaining the Beck–Chevalley, projection-formula, place-commutation, Frobenius and $\flat\dashv\sharp$ structures of the chapter.
:::

::: {.field label="What the source establishes"}
“A positive solution would not construct the semantic functors, but it would make their formal composites manageable. A negative solution would force a proof-relevant representation of coherence cells in the kernel and would weaken the decidability prospect.”
:::

::: {.field label="Proposed by"}
[S07].
:::

::: {.field label="Background"}
[GKNB21]; [Gra22]; [RS17].
:::

::: {.field label="Solved when"}
A finite presentation and a coherence theorem with a decision procedure for equality of generated two-cells, mechanised or proved on paper with all cases, or a proof that equality is undecidable for every finite presentation retaining the listed structures.
:::

::: {.field label="Literature check (28 October 2026)"}
Multimodal type theory [GKNB21] and its normalization theorem, which reduces conversion to the conversion problem of the mode theory and gives decidable type checking for a decidable mode theory [Gra22], were found; no coherence theorem for these modes was found.
:::

::: {.field label="Discussion"}
[Issue 57](https://github.com/AlienMuse/grothendieckian-problems/issues/57) of the repository.
:::
:::

