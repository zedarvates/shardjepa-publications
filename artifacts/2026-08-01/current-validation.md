# ShardJEPA current validation snapshot — 2026-08-01

- Author: Sylvain Galliez
- ORCID: [0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)
- Source commit: `b94646a`
- Source state: commit plus uncommitted and untracked development changes
- Scope: local software and synthetic-fixture validation; not peer review or a
  clean source release

## Workspace gates

The following commands were run from the ShardJEPA workspace on 2026-08-01:

| Command | Observed result |
|---|---|
| `rtk cargo fmt --all -- --check` | passed |
| `rtk cargo check --workspace --all-targets` | passed |
| `rtk cargo test --workspace --all-targets` | 208 passed across 69 suites |
| `rtk cargo clippy --workspace --all-targets -- -D warnings` | passed with no issue |

These gates establish the current covered software behavior. They do not prove
model generalization, physical-system safety, energy efficiency, or production
readiness.

## Neural Soroban P0 replay

Command:

```powershell
rtk cargo run -p shardjepa-pattern-lab -- benchmark `
  --seeds 7,17,29 --epochs 80 `
  --artifact-dir target/publication-validation-2026-08-01/p0
```

| Seed | Parameters | Holdout | Longer-carrier OOD | Shuffled labels | Artifact |
|---:|---:|---:|---:|---:|---:|
| 7 | 217 | 384/384 | 384/384 | 49.48% | 2,972 B |
| 17 | 217 | 384/384 | 384/384 | 51.82% | 2,966 B |
| 29 | 217 | 384/384 | 384/384 | 50.00% | 2,955 B |

The majority baseline and exact oracle were 50% and 100%. P0 projects every
carrier length into the same seven local features. Its OOD split measures
invariance to a longer carrier state, not learned carry/borrow, multicolumn
arithmetic, or cross-domain reasoning.

## Neural Soroban P1 replay

Command:

```powershell
rtk cargo run -p shardjepa-pattern-lab -- benchmark-multicolumn `
  --seeds 7,17,29 --epochs 60 `
  --artifact-dir target/publication-validation-2026-08-01/p1
```

| Seed | Parameters | Holdout (240) | OOD propagation 4–7 (192) | Shuffled labels | Artifact |
|---:|---:|---:|---:|---:|---:|
| 7 | 961 | 77.50% | 71.88% | 50.42% | 11,435 B |
| 17 | 961 | 77.92% | 73.96% | 52.50% | 11,431 B |
| 29 | 961 | 77.08% | 68.23% | 53.75% | 11,420 B |

The no-propagation baseline reached 70% on interpolation and 50% on OOD; the
exact oracle remained 100%. P1 is therefore a modest task-local learned gain on
longer propagation chains, not solved arithmetic or evidence of general
reasoning. The exact arithmetic oracle remains authoritative.

## Latent-compression replay

Two consecutive executions of
`rtk cargo run --example latent_compression_experiment` produced the same
current values:

| Trial | Payload ratio | Mean Poincaré-distance distortion | Combined score | Decision |
|---|---:|---:|---:|---|
| F32 baseline | 1.00x | 0.000000 | 0.200000 | baseline |
| symmetric INT8 | 4.00x | 0.003660 | 0.028660 | keep |
| packed INT4 | 8.00x | 0.085266 | 0.097766 | discard relative to INT8 |

The 2026-07-30 research note recorded smaller distortions (`0.001648` and
`0.048712`) from an earlier development state. The qualitative decision is
stable, but the exact values are source-snapshot dependent and must not be
presented as an immutable benchmark.

## Other validated advances

The passing workspace suite covers the current implementations of:

- columnar latent batches and multi-step prediction contracts;
- action-conditioned affine latent dynamics with complete-sequence holdouts;
- hierarchical latent planning fixtures;
- deterministic chess, Xiangqi, four-player chess, and pattern-guided search
  contracts;
- the standalone Pattern Lab training and portable inference paths;
- the Agent Host session and tool boundary;
- JSON/TOML/TOON specification-report serialization paths.

Some research notes contain stronger historical performance statements than
their executable tests currently emit. Those values remain historical notes,
not promoted measurements in this publication snapshot.

## External publication state at validation time

- GitHub authentication was active for `zedarvates`.
- The public repository
  [`zedarvates/shardjepa-publications`](https://github.com/zedarvates/shardjepa-publications)
  and release `v2026.07.29` existed.
- No Zenodo access token or GitHub-to-Zenodo hook was available.
- No ORCID Member API credentials or write permission were available.
- No HAL credentials were available.
- The manuscripts still lacked compilable `paper.tex` sources required by the
  local arXiv readiness gate.
