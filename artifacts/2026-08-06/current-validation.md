# ShardJEPA current validation snapshot — 2026-08-06

- Author: Sylvain Galliez
- ORCID: [0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)
- Source commit: `b94646aa38d9397bd7f306ee132984a2715822e3`
- Source state: commit plus concurrent modified and untracked development work
- Scope: local software, synthetic fixtures, and frozen local-provider outputs;
  not peer review, a clean source release, or a production-safety assessment

## Workspace gates

The following commands were run from the ShardJEPA workspace on 2026-08-06:

| Command | Observed result |
|---|---|
| `rtk cargo fmt --all -- --check` | passed |
| `rtk cargo check --workspace --all-targets` | passed |
| `rtk cargo test --workspace --lib --bins --tests` | 258 passed across 75 suites |
| `rtk cargo clippy --workspace --all-targets -- -D warnings` | failed on four `needless_range_loop` findings in the in-progress P4 `causal_bottleneck.rs` |
| `rtk cargo clippy -p shardjepa-agent-host --all-targets -- -D warnings` | passed |

The all-target test command also executes benchmark binaries and was not used
as the test-count source for this snapshot. One such invocation completed 58
tests before stopping during a benchmark executable without a Rust test
failure. Benchmarks used as evidence below were therefore run explicitly.

The P4 causal-bottleneck implementation appeared during concurrent work on
2026-08-06. It is excluded from every scientific claim in this release until
its strict lint gate, documentation, fixed-seed benchmark, and adoption
decision are complete.

## Neural Soroban P2 replay

Command:

```powershell
rtk cargo run -p shardjepa-pattern-lab -- benchmark-latent-multicolumn `
  --seeds 7,17,29,43,61 --epochs 80 `
  --artifact-dir target/publication-validation-2026-08-06/p2
```

P2 removes carry and borrow from both serialized observations and model input.
It uses 1,473 parameters and evaluates the same learned weights with recurrent
state intact and reset before every column.

| Measure | Five-seed mean |
|---|---:|
| Interpolation holdout, recurrent | 54.12% |
| OOD propagation lengths 4–7, recurrent | 50.73% |
| OOD propagation lengths 4–7, reset state | 51.46% |
| Recurrent minus reset-state OOD | -0.73 percentage point |
| Shuffled-label OOD | 50.94% |
| No-propagation OOD baseline | 50.00% |
| Exact arithmetic oracle | 100.00% |

Recurrent state won over the reset-state ablation on only two of five seeds.
P2 therefore reproduces a negative result: this curriculum did not learn a
usable hidden carry/borrow state.

## Neural Soroban P3 replay

Command:

```powershell
rtk cargo run -p shardjepa-pattern-lab -- benchmark-auxiliary-latent-multicolumn `
  --seeds 7,17,29,43,61 --epochs 80 `
  --artifact-dir target/publication-validation-2026-08-06/p3
```

P3 keeps the P2 observation and adds a training-only auxiliary head for exact
`propagation_out`. The paired control uses the same two-head architecture,
initialization, epoch order, and optimizer with auxiliary loss weight zero.

| Measure | P3 auxiliary | Paired `aux=0` control |
|---|---:|---:|
| Interpolation validity | 51.68% | 53.70% |
| OOD validity | 49.79% | 51.98% |
| OOD validity, reset state | 50.83% | 53.65% |

P3 beat its paired control on two of five seeds. Its OOD validity was 2.19
percentage points below the control and 1.04 points below its own reset-state
ablation, so the pre-declared adoption gate failed.

The auxiliary head reached 95.19% OOD, but reached 97.80% when recurrent state
was reset. Propagation is therefore largely decodable from the visible
same-step values; this score is not evidence of recurrent memory. Exact
arithmetic remains authoritative.

## Speculative reasoner draft-size sweep

The versioned raw report and interpretation are:

- [`reasoner-draft-sweep-v3.json`](reasoner-draft-sweep-v3.json)
- [`reasoner-draft-sweep-v3.md`](reasoner-draft-sweep-v3.md)

No fixed `draft_k` among 4, 8, 10, 16, 32, 64, and 128 passed the combined
fidelity and speed gate. Small drafts lost recall or top-1 agreement; large
drafts became slower than exhaustive ranking on the 50-candidate case. Exact
ranking remains the fallback while an adaptive policy is unverified.

## Creative Cognition Lab

The standalone crate passed formatting, strict Clippy, and 20 tests across four
suites; two opt-in provider tests remained ignored. Its frozen 32-case local
LM Studio run is preserved in the P1.2 report:

| Measure | Full 32 | Held-out 16 |
|---|---:|---:|
| Fully passed cases | 12 | 7 |
| Strict-valid candidates | 15 | 8 |
| Generation or parse failures | 17 | 8 |
| Golden structural matches | 0/8 | 0/4 |
| Adoption gate | rejected | rejected |

The model successfully abstained on some negative controls but matched none of
the authentic golden structural relations. This is evidence for the capture,
replay, and fail-closed evaluation path, not for creative transfer capability.

## Functional self-monitoring and constitutional risk gate

The standalone Sentience Lab passed formatting, strict Clippy, and 17 tests
across four suites. Its executable report reproduced:

- P0 private-state ablation: Brier score `0.056422` intact versus `0.225717`
  ablated; zero versus three overload failures; utility `9.100` versus `-1.600`;
- P1-G: a 113-parameter `12 -> 8 -> 1` classifier reached accuracy `0.993056`,
  unsafe recall `0.986111`, and combined deterministic-plus-learned safety
  recall `1.0` on each of five seeds in its synthetic development fixture.

Both executable paths return `supports_sentience_claim=false`. P0 is a paired
functional self-monitoring fixture. P1-G is a development-stage risk
classifier behind deterministic vetoes, abstention, an OOD guard, and a
latched circuit breaker. Neither result establishes consciousness, real-world
safety, moral status, or permission for autonomous external action.

## Agent Host boundary

The current Agent Host passed 28 tests across seven suites and strict Clippy.
These tests cover local protocol fixtures, bounded tool/model loops, streaming,
cancellation, named providers, and byte/tool-call budgets. No live cloud call
was made for this publication snapshot, and no provider credential is included.

## Publication-channel state

- GitHub remains the verified public distribution channel.
- No DOI has been assigned.
- Zenodo still requires an authorized access token or repository integration.
- arXiv/HAL still require submission credentials and manuscript-level TeX
  sources accepted by the local readiness gate.
- ORCID metadata is locally validated; no ORCID record mutation is implied.
