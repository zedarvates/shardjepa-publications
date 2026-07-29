# Abstract: Dendritron in ShardJEPA

**Author:** Sylvain Galliez  
**ORCID:** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)  
**Version:** 2026.07.29  
**Status:** Repository preprint; not peer reviewed; no DOI

ShardJEPA's `DendritronTransformer` is a deterministic scalar-branch latent
transformation and metrics fixture. It is inspired by gated aggregation but is
not a trained biological-neuron model, matrix layer, or attention mechanism.
For each scalar latent value it evaluates a configured number of scaled tanh
branches, weights them by sigmoid gates, and returns their normalized weighted
sum. On one 512-dimensional release-mode benchmark with four branches, mean
elapsed time ranged from 14.45 to 23.61 microseconds per shard across the tested
sequence container sizes. No gradient, representation quality, parameter-count
comparison, or quantized-accuracy experiment is reported.

