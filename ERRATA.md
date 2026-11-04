# Errata

Corrections to the source works and to the papers, with the date on which each was recorded.

## Source works

| Source | Place | Correction | Found by |
|---|---|---|---|
| *Arithmetic Spectral Descent* (S03) | Problem 28.13, p. 604 | The source states that no construction of a Pin(2)-equivariant lift of THH is known. Quaternionic topological Hochschild homology THQ, with a Pin(2)-action, is constructed by Angelini-Knoll, Merling and Péroux (arXiv:2409.18187; Adv. Math. 2026). The first question of Problem 28.13 is answered; see Problem 38. | literature check, 28 October 2026 |
| *GM-Omega-Infinity: Topos-Native Intelligence* (S02) | Master bibliography (Appendix A16) and Chapter 11.1 | Existing work on toposes and stacks for neural networks and AI is not cited. The work cites Caramello's *Theories, Sites, Toposes* (Oxford University Press, 2017) and discusses its method of topos-theoretic bridges (p. 1894), but not: J.-C. Belfiore and D. Bennequin, *Topos and Stacks of Deep Neural Networks* (arXiv:2106.14587, 2021), in which the architecture of a network defines a site and the invariance structures of its layers are stacks over it; O. Caramello and R. Zanfa, *Relative topos theory via stacks* (arXiv:2107.04417, 2021), with which the relative Topos-MoE over a base (Definition 4.1.15, p. 953) is to be compared; L. Lafforgue, *Some sketches for a topos-theoretic AI* (Barcelona Mathematics and Machine Learning Colloquium, 8 February 2024, https://www.laurentlafforgue.org/Expose_Lafforgue_IA_Barcelone_fevrier_2024.pdf) and *Computing with subspaces* (Westlake University, June 2026, https://www.laurentlafforgue.org/Expose_Lafforgue_June_2026_Computing_with_subspaces.pdf), which describe syntactic learning in terms of quotient theories and subtoposes; O. Caramello and L. Lafforgue, *Engendrement de topologies de Grothendieck, démontrabilité et opérations sur les sous-topos* (arXiv:2508.21134, 2025); and M. J. Villani and P. McBurney, *The Topos of Transformer Networks* (arXiv:2403.18415, 2024). They are to be cited and compared in the next edition. | author, 4 November 2026 |

## Papers

| Paper | Place | Correction | Found by |
|---|---|---|---|
| *The 57 Grothendieckian Problems* (version 1.0) | Problem 18, literature check | The check records that "no procedure that learns the site itself was found". It missed Lafforgue's principle for syntactic learning (*Some sketches for a topos-theoretic AI*, 2024, slides 19–20), in which the topology on a finitely presented category of partial knowledge is derived from a quotient theory sought so that the partial-knowledge functors induce topos morphisms, and the treatment of the generation of Grothendieck topologies by Caramello and Lafforgue (arXiv:2508.21134, 2025). We have not found in them a procedure that constructs the site from a corpus with a stated sufficiency criterion, so Problem 18 stands as stated; the check is to cite both in the next version. If either work, or another, settles part of the problem, please open an issue. | author, 4 November 2026 |
