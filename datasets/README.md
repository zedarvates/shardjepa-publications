# ShardJEPA dataset catalog

One bounded numerical fixture is released in publication snapshot `v2026.07.29`.

| Dataset ID | Title | Status | DOI | Download |
|---|---|---|---|---|
| `DATA-2026-001` | Poincare Hyperbolic Latent Numerical Fixture | Repository release | None | [`DATA-2026-001-poincare-benchmark/`](DATA-2026-001-poincare-benchmark/) |

The fixture contains 1,000 synthetic 128-dimensional vectors, an independent
four-ary hierarchy label file, deterministic splits, a generator, a validator,
and checksums. It is suitable for numerical and pipeline checks. It does not
provide learned embeddings or evidence of hierarchy representation quality.

## Runtime-compatible raw data

The current `DiskStreamer` maps arbitrary bytes. Its optional float decoder
interprets a caller-selected range as contiguous little-endian IEEE 754
`f32` values. It does not parse a header or discover tensor dimensions.

The released fixture uses:

- a raw `.f32le` payload;
- a separate versioned JSON manifest;
- CSV labels and JSON splits.

This layout matches the current code without inventing an unsupported header.

## Release gate

A dataset becomes **released** only when all of these exist:

- deterministic generator and seed policy;
- downloadable data artifact;
- exact schema and endianness;
- tensor count, dimension, and byte-size metadata;
- SHA-256 computed from the released bytes;
- provenance, intended use, and limitations;
- explicit license;
- stable archive URL and, if assigned, a real DOI.
