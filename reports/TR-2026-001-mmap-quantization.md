# TR-2026-001: ShardJEPA Memory-Mapped Access Contract and Packed Quantization Baseline

**Author:** Sylvain Galliez  
**ORCID:** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)  
**Version:** 2026.07.29  
**Status:** Validated technical draft; not externally archived; no DOI  
**License:** CC BY 4.0

## 1. Executive summary

ShardJEPA exposes a read-only memory-mapped byte view and symmetric packed
quantizers. The mapped byte view avoids copying the whole file into a user
buffer at open time. Decoding little-endian floats is a separate operation that
allocates a `Vec<f32>`. The current repository has no controlled mmap-versus-
buffered-I/O benchmark, so this report makes no storage latency or throughput
claim.

The release-mode quantization harness measured exact packed-payload ratios of
4x for INT8 and 8x for INT4. These ratios exclude metadata and allocator
overhead.

## 2. Storage contract

`DiskStreamer::open(path)` opens a file and creates a read-only `memmap2`
mapping. `MappedShard` retains both the path, file handle, and mapping.

- `bytes()` returns a borrowed `&[u8]` over the mapping.
- `len()` and `is_empty()` describe mapped byte length.
- `read_f32_le(element_offset, count)` checks multiplication, addition, and
  final bounds before decoding four-byte little-endian chunks.
- Decoded floats are collected into a new vector.

There is no runtime-defined magic header, tensor count, dimension field, or
reserved header block in this API. A caller must obtain shape and offset
metadata from a separate trusted contract.

Read-only mapping does not make external file mutation safe. Callers must
prevent truncation or mutation while the mapping is alive, as documented by
the implementation's safety contract.

## 3. Quantization contract

`SymmetricQuantizer` accepts only 4 or 8 bits. It uses a per-tensor scale based
on the maximum absolute finite latent value. INT8 stores each signed value in
one byte. INT4 stores two signed four-bit values per byte and retains the
original element count for odd-length decoding.

Unit tests verify packed length and a reconstruction error bounded by one
quantization scale for a small fixture. The benchmark below measures time and
payload size, not mean-squared error or downstream accuracy.

## 4. Experimental setup

- Date: 2026-07-29.
- OS: Microsoft Windows 11 Home, build 10.0.26200, x86_64.
- CPU: AMD Ryzen 9 5950X, 16 cores / 32 logical processors.
- Memory: 34,280,726,528 bytes reported physical memory.
- Compiler: `rustc 1.97.0`, host `x86_64-pc-windows-msvc`.
- Command: `cargo bench --bench quantization_benchmarks`.
- Iterations: 1,000 per configuration.

## 5. Observed quantization baseline

| Dimensions | Encoding | Quantize | Elements/s | Dequantize | Packed payload |
|---:|---|---:|---:|---:|---:|
| 512 | INT8 | 1.28 us | 400,876,918 | 0.38 us | 512 B from 2,048 B |
| 512 | INT4 | 1.32 us | 387,057,756 | 0.64 us | 256 B from 2,048 B |
| 4,096 | INT8 | 7.89 us | 519,177,631 | 1.75 us | 4,096 B from 16,384 B |
| 4,096 | INT4 | 9.05 us | 452,506,684 | 3.77 us | 2,048 B from 16,384 B |

These are local loop means from one benchmark invocation. They are not latency
percentiles or cross-machine guarantees.

## 6. Open measurements

Before promoting this draft to an archived technical report:

1. add a committed storage benchmark with controlled file sizes;
2. define cold-cache and warm-cache procedures;
3. compare mmap byte access, buffered reads, and explicit full-file reads;
4. record allocation and resident-set behavior with appropriate tools;
5. compute quantization error and task-level effects on a released dataset;
6. repeat samples and report variance or confidence intervals.

## 7. Conclusion

The implemented evidence supports a read-only mapped-byte contract and exact
packed-payload ratios, plus local quantization timing. It does not yet support
claims of zero-copy float inference, 8.4 GB/s storage throughput, lower memory
use for the complete object graph, or unchanged ranking accuracy.

