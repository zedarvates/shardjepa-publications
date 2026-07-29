# Poincare Candidate Ranking in ShardJEPA: Implementation Contract and Local Baseline

**Author:** Sylvain Galliez  
**ORCID:** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)  
**Version:** 2026.07.29  
**Status:** Repository preprint; not peer reviewed; no DOI  
**License:** CC BY 4.0

## Abstract

This implementation note documents ShardJEPA's finite-input projection and
candidate-ranking contract for a Poincare ball. A local release-mode loop over
128-dimensional synthetic vectors observed 33.63, 137.64, and 672.16
microseconds per complete ranking for 50, 200, and 1,000 candidates. The
implementation is scalar and allocates intermediate vectors; it is not SIMD or
allocation free. No hierarchy is learned and no representation-distortion
experiment is reported.

## 1. Motivation and scope

Hyperbolic spaces are useful candidates for representing hierarchical data
because their volume growth differs from Euclidean space [2, 3]. ShardJEPA
does not reproduce those learning studies. It provides geometry operations
and deterministic candidate ranking that later experiments can call.

This paper answers two narrow questions:

1. What projection, validation, and score does the current Rust code compute?
2. What local time does its brute-force ranking harness observe for fixed
   synthetic inputs?

## 2. Implemented geometry

For curvature magnitude \(c>0\), epsilon \(0 \le \epsilon < 1\), and a finite
non-empty point \(x\), `PoincareBall::project` uses

\[
r_{max}=\frac{1-\epsilon}{\sqrt{c}}.
\]

It returns \(x\) unchanged when \(\lVert x\rVert_2 \le r_{max}\); otherwise it
returns \(x\,r_{max}/\lVert x\rVert_2\). Projection allocates a new vector in
either branch.

For projected points \(u\) and \(v\), the conventional arcosh distance for
curvature \(-c\) is

\[
d_c(u,v)=\frac{1}{\sqrt{c}}\operatorname{arcosh}\left(
1+\frac{2c\lVert u-v\rVert_2^2}
{(1-c\lVert u\rVert_2^2)(1-c\lVert v\rVert_2^2)}
\right).
\]

The current Rust implementation clamps the denominator by `epsilon` and the
arcosh argument by 1, but returns **twice** this arcosh expression:

\[
s_c(u,v)=\frac{2}{\sqrt{c}}\operatorname{arcosh}(\cdots).
\]

This is an implementation discrepancy to correct before treating absolute
scores as standard Poincare distances. Multiplication by a positive constant
does not change candidate order when all scores are finite, so the current
nearest-neighbor ranking remains order equivalent to the conventional formula
under those conditions.

The module also contains Poincare/Lorentz conversions, but they are outside the
benchmark reported here. It does not implement Mobius layers, Riemannian
optimization, learned embeddings, or SIMD kernels.

## 3. Candidate ranking

`NearestNeighborReasoner::rank`:

1. collects a vector of candidate slices;
2. computes one score per candidate;
3. collects `(candidate_index, score)` pairs;
4. sorts ascending by score.

The path is brute force and allocates intermediate vectors. It has linear
score computation plus comparison-sort overhead; no approximate index is used.

## 4. Local baseline

The benchmark uses 128-dimensional constant-valued vectors, curvature 1.0,
epsilon \(10^{-5}\), and 100 complete ranking iterations. It ran in the
optimized bench profile on an AMD Ryzen 9 5950X with Rust 1.97.0 on Windows 11.

| Candidates | Mean time per complete rank | Candidate evaluations/s |
|---:|---:|---:|
| 50 | 33.63 us | 1,486,635 |
| 200 | 137.64 us | 1,452,971 |
| 1,000 | 672.16 us | 1,487,739 |

These are elapsed-loop means from one invocation. They do not include
variance, confidence intervals, independent repetitions, or comparisons with
Euclidean ranking. The throughput divides candidate evaluations by total loop
time; it is not completed rankings per second.

## 5. Limitations

- The input is synthetic and contains no hierarchy labels.
- No embedding is trained and no downstream accuracy is measured.
- The benchmark does not compare geometries or libraries.
- The path allocates and sorts all scores.
- The absolute-score factor discrepancy must be resolved before a metric
  accuracy study.
- Results came from a commit plus uncommitted working-tree changes.

## 6. Conclusion

ShardJEPA currently provides a bounded scalar Poincare ranking fixture and a
local throughput baseline. This is useful infrastructure evidence, but it does
not support claims of lower hierarchical distortion, SIMD acceleration, or
learned JEPA quality.

## References

1. Yann LeCun. *A Path Towards Autonomous Machine Intelligence*, 2022.
2. Maximilian Nickel and Douwe Kiela. *Poincare Embeddings for Learning
   Hierarchical Representations*. NeurIPS 2017.
3. Octavian Ganea, Gary Becigneul, and Thomas Hofmann. *Hyperbolic Neural
   Networks*. NeurIPS 2018.

