# ShardJEPA research publications

This directory contains repository drafts, technical notes, metadata, and
reproducibility evidence for ShardJEPA. It is written for machine-learning
researchers and Rust systems developers who want to inspect what the current
prototype implements and reproduce its local measurements.

**Author:** Sylvain Galliez  
**ORCID:** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)  
**Repository release:** [zedarvates/shardjepa-publications](https://github.com/zedarvates/shardjepa-publications)  
**Snapshot date:** 2026-07-29

## Publication status

| Identifier | Output | Status on 2026-07-29 | Evidence |
|---|---|---|---|
| `PUB-2026-001` | ShardJEPA runtime paper | Repository preprint | Predictor and quantization baselines |
| `PUB-2026-002` | Poincare implementation note | Repository preprint | Deterministic reasoner baseline |
| `PUB-2026-003` | Dendritron implementation note | Repository preprint | Deterministic transformer baseline |
| `TR-2026-001` | mmap and quantization report | Validated technical draft | Quantization baseline; mmap performance pending |
| `DATA-2026-001` | Poincare numerical fixture | Repository dataset release | Generator, invariants, and checksums |

“Repository preprint” means that a versioned manuscript is publicly available
in the repository. It does not mean peer reviewed, accepted by a venue,
deposited on arXiv or HAL, or assigned a DOI. The repository dataset is public
but no output in this snapshot has a DOI.

## Contents

```text
publications/
|-- artifacts/                    # Dated validation and benchmark evidence
|-- datasets/                     # Dataset catalog, generator, and released fixture
|-- papers/                       # Repository preprints
|-- reports/                      # Technical reports
|-- templates/                    # Honest publication templates
|-- tools/                        # Validation and packaging helpers
|-- GUIDELINES.md                 # Reproducibility and release gates
|-- ORCID_INDEX.json              # Machine-readable output registry
|-- PUBLISHING_GUIDE.md           # GitHub, Zenodo, arXiv/HAL, and ORCID workflow
`-- citations.bib                 # BibTeX for repository releases
```

## Reproduce the 2026-07-29 snapshot

Run from the ShardJEPA repository root:

```powershell
rtk cargo check --workspace --all-targets
rtk cargo test --workspace --all-targets
rtk cargo bench --bench predictor_benchmarks
rtk cargo bench --bench quantization_benchmarks
rtk cargo bench --bench reasoner_benchmarks
rtk cargo bench --bench transformer_benchmarks
rtk python publications/tools/export_metadata.py
```

The exact observed output, machine description, source-state caveat, and
limitations are recorded in
[`artifacts/2026-07-29/benchmark-results.md`](artifacts/2026-07-29/benchmark-results.md).
The benchmarks use `std::time::Instant` loops rather than a statistical
benchmarking framework, so the numbers are local baselines, not portable
performance guarantees.

## Licenses

- Source code remains covered by the repository MIT license.
- Publication text and locally authored metadata are released under
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see
  [`LICENSE.md`](LICENSE.md).
- Third-party references remain under their respective terms.
