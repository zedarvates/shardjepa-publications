# Publication snapshot 2026.07.29

This snapshot is the first evidence-corrected repository release of the
ShardJEPA publication set.

## Corrected before release

- Replaced anonymous group authorship with the confirmed repository author.
- Removed a fabricated Zenodo DOI. The subsequently generated dataset is a
  repository release only and has no archive DOI.
- Changed the technical report from “published” to a validated draft.
- Replaced untraceable latency tables with measurements observed on
  2026-07-29.
- Corrected `DiskStreamer`: raw mapped bytes can be borrowed, but decoded
  little-endian floats are returned in an allocated vector.
- Corrected the Dendritron equations to match the scalar-branch reference
  implementation.
- Removed unsupported claims about SIMD, learned hierarchy distortion,
  candidate discriminability, energy profiling, and peer review.
- Replaced the misleading Markdown-only arXiv package with a TeX readiness
  check.
- Changed Zenodo automation to dry-run by default and bearer-header
  authentication.
- Corrected the generated four-ary hierarchy depths, documented that vector
  coordinates are independent of hierarchy labels, and added exact regeneration
  validation.

## Validation summary

- `cargo fmt --all -- --check`: passed on the final publication worktree.
- `cargo check --workspace --all-targets`: passed.
- `cargo test --workspace --all-targets`: 122 passed across 39 suites on the
  final publication worktree.
- `cargo clippy --workspace --all-targets -- -D warnings`: passed.
- Four release-mode benchmark programs: passed.

The numeric benchmark tables were measured earlier in the same task from the
source state recorded in the evidence log; final checks do not retroactively
change those measurements.
