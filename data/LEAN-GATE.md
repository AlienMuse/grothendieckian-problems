# Lean gate

Toolchain `leanprover/lean4:v4.36.0-rc2`; Mathlib `b7fb16a940e9` (pinned in lakefile.toml).

| check | result | detail |
|---|---|---|
| lake build | PASS | rc 0; errors 0 |
| P49.lean belongs to a formalization card | PASS | Problem 49 |
| P49.lean: axioms | PASS | 9 theorems; axioms used ['Classical.choice', 'Quot.sound', 'propext', 'sorryAx']; outside the standard set 0 |
| P49.lean: open statements | PASS | 12 `sorry` (the problem is to remove them) |

**ALL PASS**
