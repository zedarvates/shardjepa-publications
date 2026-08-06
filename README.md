# ShardJEPA research publications

This directory contains repository drafts, technical notes, metadata, and
reproducibility evidence for ShardJEPA. It is written for machine-learning
researchers and Rust systems developers who want to inspect what the current
prototype implements and reproduce its local measurements.

**Author:** Sylvain Galliez  
**ORCID:** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)  
**Repository release:** [zedarvates/shardjepa-publications](https://github.com/zedarvates/shardjepa-publications)  
**Latest snapshot date:** 2026-08-06

## Publication status

| Identifier | Output | Status on 2026-08-06 | Evidence |
|---|---|---|---|
| `PUB-2026-001` | ShardJEPA runtime paper | Repository preprint, revised | Runtime contract and dated baselines |
| `PUB-2026-002` | Poincare implementation note | Repository preprint | Deterministic reasoner baseline |
| `PUB-2026-003` | Dendritron implementation note | Repository preprint | Deterministic transformer baseline |
| `PUB-2026-004` | [Multi-rate embodied agents position paper](papers/04-multirate-embodied-agents/paper.md) | Repository preprint | [English](papers/04-multirate-embodied-agents/paper.md) / [français](papers/04-multirate-embodied-agents/paper-fr.md) |
| `TR-2026-001` | mmap and quantization report | Repository technical report | Quantization and dated distortion evidence; mmap performance pending |
| `TR-2026-002` | [Task-local learning and bounded planning](reports/TR-2026-002-task-local-learning-planning.md) | Repository technical report, revised | P0–P3, latent dynamics, fixed-draft rejection |
| `TR-2026-003` | [Governed local cognition experiments](reports/TR-2026-003-governed-local-cognition.md) | Repository technical report | Creative-transfer failure, self-monitoring, P1-G risk gate |
| `DATA-2026-001` | Poincare numerical fixture | Repository dataset release | Generator, invariants, and checksums |

“Repository preprint” means that a versioned manuscript is publicly available
in the repository. It does not mean peer reviewed, accepted by a venue,
deposited on arXiv or HAL, or assigned a DOI. The repository dataset is public
but no output in this snapshot has a DOI.

## Contents

```text
publications/
|-- artifacts/                    # Dated validation and benchmark evidence
|-- CONCLUSIONS_2026-08-06.md     # Latest evidence-based assessment and limits
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

## Reproduce the 2026-08-06 validation snapshot

Run from the ShardJEPA repository root:

```powershell
rtk cargo check --workspace --all-targets
rtk cargo test --workspace --lib --bins --tests
rtk cargo run -p shardjepa-pattern-lab -- benchmark-latent-multicolumn --seeds 7,17,29,43,61 --epochs 80 --artifact-dir target/neural-soroban-p2
rtk cargo run -p shardjepa-pattern-lab -- benchmark-auxiliary-latent-multicolumn --seeds 7,17,29,43,61 --epochs 80 --artifact-dir target/neural-soroban-p3
rtk cargo test --manifest-path tools/shardjepa-creative-cognition-lab/Cargo.toml --all-targets
rtk cargo run --quiet --manifest-path tools/shardjepa-sentience-lab/Cargo.toml
rtk python publications/tools/export_metadata.py
```

The current commands, exact P2/P3 results, standalone-laboratory gates,
source-state caveat, and publication-channel audit are recorded in
[`artifacts/2026-08-06/current-validation.md`](artifacts/2026-08-06/current-validation.md).
Earlier runtime measurements and their machine description remain in
[`artifacts/2026-07-29/benchmark-results.md`](artifacts/2026-07-29/benchmark-results.md).
The later reasoner benchmark v2 adds warm-up, repeated samples, p95, raw JSON,
and ranking-fidelity measurements; see
[`artifacts/2026-07-29/reasoner-benchmark-v2.md`](artifacts/2026-07-29/reasoner-benchmark-v2.md).
The 2026-08-06 acceptance sweep tests seven fixed draft sizes and rejects all
of them under the combined speed-and-fidelity gate; see
[`artifacts/2026-08-06/reasoner-draft-sweep-v3.md`](artifacts/2026-08-06/reasoner-draft-sweep-v3.md).
The external CogniARC/Botte nano-network evidence used by `PUB-2026-004`,
including reproduced results and unresolved model-card claims, is recorded in
[`artifacts/2026-07-29/nano-nn-huggingface-audit.md`](artifacts/2026-07-29/nano-nn-huggingface-audit.md).
The latest evidence-based interpretation and required validation gates are
summarized in [`CONCLUSIONS_2026-08-06.md`](CONCLUSIONS_2026-08-06.md).
The benchmarks use `std::time::Instant` loops rather than a statistical
benchmarking framework, so the numbers are local baselines, not portable
performance guarantees.

Strict workspace Clippy was not green at snapshot time because the concurrent
P4 causal-bottleneck implementation had four lint findings. P4 is excluded from
the release claims; the remaining validated packages and both standalone
laboratories passed their scoped strict checks.

## External channels

- GitHub is the verified public distribution channel for this snapshot.
- No DOI has been assigned. Zenodo publication requires a personal access token
  with deposit scopes or an explicitly configured repository integration.
- arXiv/HAL submission remains blocked until manuscript-level TeX sources and
  author submission credentials are available.
- ORCID metadata is locally validated; the record is not modified by these
  scripts.

## Licenses

- Source code remains covered by the repository MIT license.
- Publication text and locally authored metadata are released under
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see
  [`LICENSE.md`](LICENSE.md).
- Third-party references remain under their respective terms.
