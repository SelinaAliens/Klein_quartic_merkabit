# Paper 8: The Klein Quartic Connection

**Merkabit Research Program — Paper 8**

## Overview

This paper establishes a rigorous, zero-free-parameter bridge between the Klein quartic (the maximally symmetric genus-3 algebraic curve) and the merkabit architecture. Seven theorems are proved computationally, closing all major open questions.

## Seven Theorems

| # | Theorem | Status |
|---|---------|--------|
| 1 | **Vertex Bijection** — Equivariant bijection between 56-element coset spaces, verified across all 9,408 (g, coset) pairs | PROVED |
| 2 | **Azygetic Graph** — 28 bitangent theta characteristics form srg(28,12,6,4) isomorphic to T(8) = L(K_8) | PROVED |
| 3 | **Route B Forcing** — Coefficients (12, 5) in alpha^{-1} = N(12+5omega)+28 = 137 forced by E_6 architecture with zero free parameters | PROVED |
| 4 | **Cyclotomic Unification** — Ternary Golay (E_6) and binary Golay (E_8) both live in Q(zeta_21) subfield lattice | PROVED |
| 5 | **PSL(2,7) Conjugacy** — All 56 order-3 elements form a single conjugacy class; all Z_3 subgroups are conjugate | PROVED |
| 6 | **Spectral Match** — Azygetic graph eigenvalues {12, 4, -2} with multiplicities {1, 7, 20} match T(8) exactly | PROVED |
| 7 | **Weyl Chamber Selection** — Quadratic b^2-12b+35=0 gives b in {5,7}; Weyl chamber of E_6 selects b=5 uniquely | PROVED |

## The Forcing Chain

```
{binary + threshold + dim=4} -> Z_3 -> 1/3 -> (1/3)/(1/4) = 4/3 -> x 78|gamma_0|/pi = 137.036
                                        |           |                    |
                                  zero point    KWW exponent         fine structure
                                   constant      (threshold)       constant (coupling)
```

## Repository Contents

### Scripts
| File | Description |
|------|-------------|
| `klein_quartic_analysis.py` | Core Klein quartic analysis — PSL(2,7), Hurwitz surface, edge/face structure |
| `azygetic_graph.py` | Azygetic graph computation — theta characteristics, srg(28,12,6,4), T(8) isomorphism |
| `vertex_bijection.py` | Equivariant bijection — GL(3,F_2) conjugacy, coset space map, 9408-pair verification |
| `route_b_justification.py` | Route B forcing proof — Eisenstein prime enumeration, (12,5) uniqueness |
| `cyclotomic_analysis.py` | Cyclotomic field analysis — Q(zeta_21) subfield lattice, Golay code embedding |
| `theta_analysis.py` | Theta characteristic analysis — symplectic pairing, azygetic/syzygetic classification |
| `generate_figures.py` | Figure generation — all 6 publication-quality matplotlib figures at 300 DPI |
| `build_paper8.js` | Paper builder — docx-js script generating the full Paper 8 Word document |

### Figures
| File | Description |
|------|-------------|
| `fig1_azygetic_graph.png` | 28-vertex azygetic graph colored by 8 maximum cliques |
| `fig2_adjacency_matrix.png` | Adjacency matrix heatmap reordered by T(8) clique structure |
| `fig3_subfield_lattice.png` | Q(zeta_21) subfield lattice diagram |
| `fig4_forcing_chain.png` | Route B zero-parameter derivation flow |
| `fig5_conjugacy_classes.png` | PSL(2,7) conjugacy class structure |
| `fig6_spectral_comparison.png` | Eigenvalue spectrum overlay: azygetic graph vs T(8) |

### Output
| File | Description |
|------|-------------|
| `Paper_8_Klein_Quartic.docx` | Final paper with embedded figures (1.5 MB) |
| `output.txt` | Computation logs |
| `results_summary.json` | Machine-readable results summary |

## Key Mathematical Objects

- **PSL(2,7)** = GL(3,F_2): order 168, the automorphism group of the Klein quartic
- **Klein quartic**: x^3 y + y^3 z + z^3 x = 0, genus 3, 168 automorphisms (Hurwitz bound)
- **28 bitangents**: Lines tangent to the quartic at two points, forming the azygetic graph
- **T(8) = L(K_8)**: Triangular graph on 8 vertices = line graph of K_8
- **E_6**: Exceptional Lie algebra, h(E_6) = 12, dim(E_6) = 78
- **Eisenstein integers Z[omega]**: omega = e^{2pi i/3}, norm N(a+b*omega) = a^2-ab+b^2

## Dependencies

**Python scripts:**
```
numpy, scipy, sympy, matplotlib, itertools, networkx
```

**Paper builder (Node.js):**
```
npm install docx
```

## Building the Paper

```bash
# Generate figures
python generate_figures.py

# Build the docx
node build_paper8.js
```

## Citation

Part of the Merkabit Research Program.

## License

MIT
