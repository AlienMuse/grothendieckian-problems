/-
Copyright (c) 2026 Vincent Liu. Released under Apache 2.0 license.
-/
import Mathlib

/-!
# Problem 49 · Close the formal algebra leaf

*The 57 Grothendieckian Problems*, Problem 49; source: *Strained Prismatic Geometry* (Series 06), Problem 62.1.5 and
Proof Obligation 53.2.1 (PO-090), with the interface proposed in its Listing 53.2.

The statements below are the standard theory of `p`-derivations (δ-rings) of Joyal and Buium, in the form used for
prisms by Bhatt and Scholze. Definitions are given in full; the theorems are the problem and are left as `sorry`, as
in `google-deepmind/formal-conjectures`. Solving Problem 49 means replacing every `sorry` below by a proof, adding the
adapter to Mathlib's `p`-typical Witt-vector Frobenius required by PO-090, and introducing no axioms.

Two choices differ from Listing 53.2 of the source and are recorded here: the correction polynomial is defined
explicitly rather than left as `sorry`, and `δ 1 = 0` is an axiom of the structure, as in the standard definition.
-/

namespace GrothendieckianProblems.P49

open Finset

/-- The integral addition-correction polynomial `(X^p + Y^p - (X + Y)^p) / p`, evaluated at `x y : A`, written as
`-∑_{0 < i < p} (choose p i / p) x^i y^(p - i)`; for a prime `p` the quotient `choose p i / p` is exact. -/
def addCorrection (p : ℕ) {A : Type*} [CommRing A] (x y : A) : A :=
  -∑ i ∈ Ioo 0 p, (((p.choose i) / p : ℕ) : A) * x ^ i * y ^ (p - i)

/-- A `p`-derivation on a commutative ring: a map `δ` with the sum and product rules of a δ-ring. Its type is
separate from that of an ordinary derivation (`Derivation`). -/
class PDerivation (p : ℕ) (A : Type*) [CommRing A] where
  /-- the `p`-derivation -/
  delta : A → A
  delta_zero : delta 0 = 0
  delta_one : delta 1 = 0
  delta_add : ∀ x y, delta (x + y) = delta x + delta y + addCorrection p x y
  delta_mul : ∀ x y, delta (x * y) = x ^ p * delta y + y ^ p * delta x + (p : A) * delta x * delta y

/-- A ring homomorphism commuting with the `p`-derivations. -/
structure PDerivationHom (p : ℕ) (A B : Type*) [CommRing A] [CommRing B] [PDerivation p A] [PDerivation p B]
    extends A →+* B where
  map_delta' : ∀ x, toFun (PDerivation.delta (p := p) x) = PDerivation.delta (p := p) (toFun x)

/-- The Frobenius lift attached to a `p`-derivation: `φ(x) = x^p + p δ(x)`. -/
def frobeniusLift (p : ℕ) {A : Type*} [CommRing A] [PDerivation p A] (x : A) : A :=
  x ^ p + (p : A) * PDerivation.delta (p := p) x

variable {p : ℕ} [Fact p.Prime] {A B : Type*} [CommRing A] [CommRing B]

/-- The correction polynomial is `(x^p + y^p - (x + y)^p) / p`: multiplying by `p` recovers the numerator. -/
theorem p_mul_addCorrection (x y : A) :
    (p : A) * addCorrection p x y = x ^ p + y ^ p - (x + y) ^ p := by
  sorry

/-- The case `p = 2`, which the source asks to treat explicitly: the correction is `-x y`. -/
theorem addCorrection_two (x y : A) : addCorrection 2 x y = -(x * y) := by
  sorry

section FrobeniusLift

variable [PDerivation p A]

theorem frobeniusLift_add (x y : A) :
    frobeniusLift p (x + y) = frobeniusLift p x + frobeniusLift p y := by
  sorry

theorem frobeniusLift_mul (x y : A) :
    frobeniusLift p (x * y) = frobeniusLift p x * frobeniusLift p y := by
  sorry

theorem frobeniusLift_one : frobeniusLift p (1 : A) = 1 := by
  sorry

/-- The Frobenius lift is a ring endomorphism lifting the `p`-th power map modulo `p`. -/
theorem exists_ringHom_frobeniusLift :
    ∃ φ : A →+* A, (∀ x, φ x = frobeniusLift p x) ∧ ∀ x, φ x - x ^ p = (p : A) * PDerivation.delta (p := p) x := by
  sorry

end FrobeniusLift

/-- Homomorphisms of `p`-derivations commute with the Frobenius lifts. -/
theorem PDerivationHom.map_frobeniusLift [PDerivation p A] [PDerivation p B] (f : PDerivationHom p A B) (x : A) :
    f.toRingHom (frobeniusLift p x) = frobeniusLift p (f.toRingHom x) := by
  sorry

/-- On `ℤ`, `δ(n) = (n - n^p) / p` (exact by Fermat's little theorem) is a `p`-derivation, and its Frobenius lift is
the identity. This example exercises negative integers. -/
theorem int_example :
    ∃ inst : PDerivation p ℤ, ∀ n : ℤ,
      @PDerivation.delta p ℤ _ inst n = (n - n ^ p) / p ∧ @frobeniusLift p ℤ _ inst n = n := by
  sorry

/-- On `ℤ[X]`, the structure of `int_example` extends by `φ(X) = X^p`, and then `δ(X) = 0`. -/
theorem polynomial_example :
    ∃ inst : PDerivation p (Polynomial ℤ),
      (∀ n : ℤ, @PDerivation.delta p _ _ inst (Polynomial.C n) = Polynomial.C ((n - n ^ p) / p)) ∧
      @PDerivation.delta p _ _ inst Polynomial.X = 0 ∧
      @frobeniusLift p _ _ inst Polynomial.X = Polynomial.X ^ p := by
  sorry

end GrothendieckianProblems.P49
