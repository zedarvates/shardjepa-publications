# Abstract: Poincare candidate ranking in ShardJEPA

**Author:** Sylvain Galliez  
**ORCID:** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)  
**Version:** 2026.07.29  
**Status:** Repository preprint; not peer reviewed; no DOI

This implementation note documents ShardJEPA's finite-input projection and
candidate-ranking contract for a Poincare ball. A local release-mode loop over
128-dimensional synthetic vectors observed 33.63, 137.64, and 672.16
microseconds per complete ranking for 50, 200, and 1,000 candidates. The
implementation is scalar and allocates intermediate vectors; it is not SIMD or
allocation free. Its absolute distance score currently contains an extra
factor of two relative to the conventional arcosh form, although this positive
constant does not change finite candidate order. No hierarchy is learned and
no Euclidean-versus-hyperbolic distortion experiment is reported.

