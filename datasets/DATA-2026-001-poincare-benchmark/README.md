# DATA-2026-001: Poincare Hyperbolic Latent Numerical Fixture

**Creator:** Sylvain Galliez  
**ORCID:** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)  
**Version:** 2026.07.29  
**Status:** Repository dataset release  
**Archive DOI:** None  
**License:** CC BY 4.0

## Purpose

`DATA-2026-001` is a small deterministic numerical fixture for exercising
Poincare-ball bounds, exact candidate-ranking code, and packed quantization.
It is not a learned embedding dataset and does not demonstrate that hierarchy
is encoded in vector coordinates.

## Contents

| File | Description |
|---|---|
| `vectors.f32le` | 1,000 x 128 contiguous IEEE 754 binary32 values, little-endian |
| `hierarchy.csv` | Deterministic four-ary tree labels for the same 1,000 row IDs |
| `splits.json` | Disjoint train/validation/test index lists (700/150/150) |
| `manifest.json` | Shapes, bounds, generator provenance, byte size, and payload SHA-256 |
| `SHA256SUMS` | Checksums for released files and documentation |
| `generate.py` | Dependency-free deterministic generator, version 1.1.0 |
| `validate.py` | Invariant, checksum, and exact-regeneration validator |

The hierarchy labels are intentionally independent of vector coordinates. They
support plumbing and split tests only; they must not be used to claim
hierarchical representation quality.

## Geometry and generation

- Curvature magnitude: `1.0`.
- Projection epsilon: `1e-5`.
- Maximum valid norm: `(1 - epsilon) / sqrt(curvature)`.
- Seed: `42` using the documented 32-bit LCG in `generate.py`.
- Target vector norms span deterministic radii from 5% to 99% of the maximum.
- Payload byte size: `1,000 * 128 * 4 = 512,000` bytes.

The current `DiskStreamer` does not parse a container header. Shape and format
come from `manifest.json`; `vectors.f32le` contains payload bytes only.

## Reproduce and validate

From the ShardJEPA repository root:

```powershell
rtk python publications/datasets/DATA-2026-001-poincare-benchmark/generate.py
rtk python publications/datasets/DATA-2026-001-poincare-benchmark/validate.py
```

Validation checks payload size and SHA-256, finite values, every vector norm,
tree parent/depth consistency, split coverage, all listed checksums, and exact
regeneration in a temporary directory.

## FAIR status

- **Findable:** versioned in the public GitHub release and registry.
- **Accessible:** files are included in the repository release bundle.
- **Interoperable:** raw little-endian `f32`, CSV, and JSON formats.
- **Reusable:** generator, seed, validation, checksums, and CC BY 4.0 license are
  included.

No Zenodo, arXiv, or publisher DOI is assigned in this snapshot.

## Limitations

- The vectors are synthetic and do not represent real observations.
- Coordinates are independent of the hierarchy labels.
- The fixture is small and intended for deterministic correctness checks, not
  model training or generalization claims.
- No Euclidean-versus-hyperbolic quality comparison is bundled.

