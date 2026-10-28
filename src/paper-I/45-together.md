# How the theses fit together

The theses are not independent. Theses 1 and 2 together say what an artefact is: an object in a declared world, with a
status that belongs to its type. Thesis 6 depends on both, because the passages it separates — from completion to
validity, from validity to promotion, from promotion to publication — are changes of status that only a typed artefact
can record. Thesis 7 locates the last of these passages outside the producing system. Theses 4 and 5 describe the
reasoning step that the others constrain: local information is transported along restriction maps and glued where it
can be, and the system reports where it cannot. Theses 8 to 12 describe the method of discovery that the architecture
is meant to support, and the way its results should be reported and judged. \figref{relations} draws these relations
together with the two stated below.

::: {.figure #fig:relations file="fig-relations" place="tbp"}
The relations between the theses that this section states, each labelled with its words. Nodes are coloured by group
as in \figref{theses} and link to the theses.
:::

A worked example from [@S01] shows several theses at once (\figref{triangle}). Three charts $U_1,U_2,U_3$ carry local sections
$s_1,s_2,s_3$ describing the same finite object, each in a chart-specific normalisation. The three pairwise comparisons
pass: “All three edge predicates pass.” But one chart applies its normalisation after transport, and the direct path
from the first chart to the third applies it before, so that in the declared normalisation system
$t_{23}\circ t_{12}\neq t_{13}$. A checker of triangles reports the failure, and its record keeps what is needed to
reproduce it: the hashes of the three sections, the three local receipts, the oriented face, the transition digests,
the two composite results, the normalisation rule, the equality predicate, the checker and its environment, and the
counterexample. The record excludes an unrelated fourth chart. The outcome is stated without loss in either direction:
“The three pairwise receipts remain historically valid; they simply do not establish the failed triangular law.”
[@S01, Vol. III, §61.18, p. 9227]

In this example the world records of Thesis 1 are what make the failure locatable: without the normalisation rule and
the equality predicate there is nothing to compare. The statuses of Thesis 2 are what keep the pairwise receipts valid
while the triangle fails. Thesis 5 is the report itself, an obstruction with a location rather than a score. Thesis 6
is the refusal to read three successful comparisons as a successful gluing, and Thesis 10 is what happens next: the
failure becomes the input of a proposal to change the normalisation bridge or to split the cover, which must itself be
admitted and rechecked. Nothing in the example is deep mathematics. Its point is that each of these steps can be skipped, and that skipping any one of them turns true local statements into a false global one.

::: {.figure #fig:triangle file="fig-triangle" place="tbp"}
The worked example of this section, after [@S01, Vol. III, §61.18, p. 9227]: three charts carry local sections of one
finite object; the three pairwise comparisons pass and the triangular law fails. On the right, what the record of the
failure keeps and what it excludes; below, the step at which each of Theses 1, 2, 5, 6 and 10 acts. Each panel of the
lower row links to its thesis.
:::

The theses also constrain one another. Thesis 3, that reasoning needs a structured carrier, would be idle without
Thesis 11: a carrier whose vocabulary is fixed cannot represent the structures that a new problem requires. Thesis 9,
that a result must state what it does not establish, is what makes the ledger of Thesis 12 checkable entry by entry.
And Thesis 8, the rising sea, would be indistinguishable from changing the question if it were not held to the
conditions that [@S01] attaches to it: that an extension which deletes the predicate expressing a contradiction,
forgets the invariant detecting failure, weakens equality until disagreement disappears, or renames an unknown as a
primitive has not resolved the obstruction [@S01, Vol. III, §5.1, p. 8034].
