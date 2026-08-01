# Publication and reproducibility guidelines

These rules apply to all ShardJEPA research outputs. The goal is to let a
reader distinguish implemented behavior, local measurements, planned work,
and externally published records without inference.

## Evidence classes

Every technical claim must be labelled by one of these evidence classes:

1. **Implemented:** directly traceable to a named source file and covered by a
   compiling test or check.
2. **Measured:** produced by a committed command or benchmark with raw output,
   machine context, date, and source revision.
3. **Observed fixture:** true only for a deterministic test fixture; it is not
   a learned-model or real-world result.
4. **Planned:** a proposal without a released artifact or measurement.

Do not turn “implemented” into “faster,” “accurate,” or “zero-copy” without a
measurement that proves the narrower claim. In particular,
`MappedShard::bytes()` borrows mapped bytes, while `read_f32_le()` allocates a
decoded `Vec<f32>`.

## Required release gates

Before publishing a repository preprint:

- [ ] Author name and ORCID are confirmed.
- [ ] Manuscript status and version are explicit.
- [ ] Each formula matches the current implementation or is labelled proposed.
- [ ] Each numeric table links to dated raw evidence.
- [ ] Limitations and negative results are present.
- [ ] `ORCID_INDEX.json` and `citations.bib` agree with the manuscript.
- [ ] `python publications/tools/export_metadata.py` passes.
- [ ] Workspace checks and tests pass, or unrelated failures are disclosed.
- [ ] The release bundle has a SHA-256 checksum.

Additional gates for an external archive:

- [ ] The archive contains the exact manuscript and evidence snapshot.
- [ ] The creator metadata uses a personal name; an ORCID iD is not assigned to
      a project or informal group.
- [ ] A real DOI or archive URL replaces any placeholder only after the record
      exists.
- [ ] The DOI is added to ORCID only after publication.

Additional gates for a dataset:

- [ ] Data file and deterministic generator are included.
- [ ] Schema matches the actual reader implementation.
- [ ] Size and SHA-256 are computed from the released file.
- [ ] License, provenance, intended use, and known limitations are documented.

## Status vocabulary

Use only these public labels:

- **Draft:** incomplete and not released.
- **Repository preprint:** versioned public manuscript; not peer reviewed.
- **Repository technical report:** versioned public technical report; not peer reviewed.
- **Archived preprint:** deposited in a recognized archive with a stable ID.
- **Published:** accepted or formally published by the named venue.
- **Planned dataset:** no data artifact exists yet.
- **Released dataset:** downloadable data, checksum, schema, and license exist.

## Benchmark reporting

Record the command, compiler, OS, CPU, input shape, iteration count, and source
state. Report the statistic the harness actually computes. A single elapsed
loop divided by iterations is a local mean; it is not a confidence interval,
percentile, or cross-machine comparison.
