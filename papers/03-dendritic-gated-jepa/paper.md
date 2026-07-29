# Dendritron in ShardJEPA: A Deterministic Scalar-Branch Latent Transformer

**Author:** Sylvain Galliez  
**ORCID:** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)  
**Version:** 2026.07.29  
**Status:** Repository preprint; not peer reviewed; no DOI  
**License:** CC BY 4.0

## Abstract

ShardJEPA's `DendritronTransformer` is a deterministic scalar-branch latent
transformation and metrics fixture. It is inspired by gated aggregation but is
not a trained biological-neuron model, matrix layer, or attention mechanism.
For each scalar latent value it evaluates scaled tanh branches, weights them by
sigmoid gates, and returns their normalized weighted sum. A local
512-dimensional benchmark with four branches observed 14.45 to 23.61
microseconds per shard across tested sequence container sizes.

## 1. Implemented transformation

Let \(x\) be one scalar component of a latent vector, \(B\) the configured
number of branches, \(s_b=b/B\) for branch \(b\), and \(\beta\) the shared gate
bias. The current implementation computes

\[
g_b(x)=\sigma(s_b x + \beta)
\]

and

\[
T(x)=\frac{\sum_{b=1}^{B}g_b(x)\tanh(s_bx)}
{\max\left(\sum_{b=1}^{B}g_b(x),\epsilon_{f32}\right)}.
\]

This scalar operation is applied independently to every latent component. No
matrix \(W_d\), learned branch parameters, cross-channel mixing, or gradient
implementation exists in this reference block.

`DendritronTransformer::new` rejects zero branches and a non-finite bias. The
latent constructor enforces a non-empty, finite output.

## 2. Diagnostic metrics

`transform_with_metrics` evaluates the same gates and records:

- total and threshold-active branch evaluations;
- mean gate activation;
- active-branch ratio;
- branch sparsity, defined as one minus the active ratio.

The threshold must be finite and lie in `[0, 1]`. These metrics describe gate
activity in this deterministic fixture. They do not measure learned sparsity,
biological fidelity, or downstream model quality.

## 3. Local baseline

The release-mode harness uses 512-dimensional synthetic shards, four branches,
zero gate bias, 200 outer iterations, and sequence containers of different
lengths. Each Dendritron transformation is stateless; the sequence length only
changes the number and arrangement of repeated calls.

| Sequence length | Mean time per shard | Shards/s |
|---:|---:|---:|
| 1 | 14.45 us | 69,187 |
| 10 | 17.02 us | 58,756 |
| 100 | 17.41 us | 57,440 |
| 500 | 23.61 us | 42,351 |

The benchmark ran on an AMD Ryzen 9 5950X with Rust 1.97.0 and Windows 11.
Values are one elapsed-loop mean per configuration. Allocation counts,
variance, confidence intervals, and cache effects were not measured.

## 4. What is not established

This snapshot provides no evidence for:

- superior candidate discriminability;
- equal or lower parameter count than a trained baseline;
- stable gradient flow;
- accuracy after INT8 or INT4 quantization;
- biological equivalence to dendritic computation;
- superiority over a dense, recurrent, or attention layer.

Those questions require a training task, datasets, baselines, metrics, and
statistical evaluation that are outside the current runtime fixture.

## 5. Conclusion

Dendritron is currently best understood as an inspectable extension point and
diagnostic fixture for scalar gated aggregation. Its value in this release is
deterministic behavior, validation, and a local execution baseline—not a claim
of learned-model improvement.

## References

1. Yann LeCun. *A Path Towards Autonomous Machine Intelligence*, 2022.
2. Panayiota Poirazi, Terrence Brannon, and Bartlett W. Mel. *Pyramidal Neuron
   as Two-Layer Neural Network*. Neuron 37(6), 2003.

