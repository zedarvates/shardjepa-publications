#!/usr/bin/env python3
"""Validate DATA-2026-001 files, invariants, checksums, and determinism."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import struct
import subprocess
import sys
import tempfile
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise ValueError(message)


def validate(root: Path) -> None:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    count = int(manifest["count"])
    dimension = int(manifest["dimension"])
    max_norm = float(manifest["max_norm"])
    vectors_path = root / manifest["payload"]["file"]
    vector_bytes = vectors_path.read_bytes()

    expected_size = count * dimension * 4
    if len(vector_bytes) != expected_size or len(vector_bytes) != manifest["payload"]["byte_size"]:
        fail("vector payload size does not match count, dimension, and manifest")
    if sha256(vectors_path) != manifest["payload"]["sha256"]:
        fail("vector payload SHA-256 does not match manifest")

    values = struct.iter_unpack("<f", vector_bytes)
    for index in range(count):
        vector = [next(values)[0] for _ in range(dimension)]
        if not all(math.isfinite(value) for value in vector):
            fail(f"vector {index} contains a non-finite value")
        norm = math.sqrt(sum(value * value for value in vector))
        if not norm < max_norm:
            fail(f"vector {index} is outside the configured Poincare ball")

    with (root / manifest["hierarchy"]["file"]).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != count:
        fail("hierarchy row count does not match vector count")
    depths: dict[int, int] = {}
    for expected_id, row in enumerate(rows):
        node_id = int(row["node_id"])
        parent_id = int(row["parent_id"])
        depth = int(row["depth"])
        if node_id != expected_id:
            fail(f"hierarchy node order mismatch at {expected_id}")
        if node_id == 0:
            if parent_id != -1 or depth != 0:
                fail("root node must have parent -1 and depth 0")
        elif parent_id not in depths or depth != depths[parent_id] + 1:
            fail(f"invalid parent/depth relationship at node {node_id}")
        depths[node_id] = depth

    splits = json.loads((root / "splits.json").read_text(encoding="utf-8"))
    flattened = [index for name in ("train", "validation", "test") for index in splits[name]]
    if sorted(flattened) != list(range(count)) or len(set(flattened)) != count:
        fail("splits must cover every index exactly once")

    expected_checksums = {}
    for line in (root / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        digest, name = line.split("  ", 1)
        expected_checksums[name] = digest
    for name, digest in expected_checksums.items():
        if sha256(root / name) != digest:
            fail(f"SHA256SUMS mismatch for {name}")

    with tempfile.TemporaryDirectory(prefix="shardjepa-data-check-") as temp_dir:
        subprocess.run(
            [sys.executable, str(root / "generate.py"), "--output-dir", temp_dir],
            check=True,
            capture_output=True,
            text=True,
        )
        generated = Path(temp_dir)
        for name in ("vectors.f32le", "hierarchy.csv", "splits.json", "manifest.json"):
            if (generated / name).read_bytes() != (root / name).read_bytes():
                fail(f"deterministic regeneration mismatch for {name}")


def main() -> int:
    root = Path(__file__).resolve().parent
    try:
        validate(root)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"[ERROR] {error}")
        return 1
    print("[OK] DATA-2026-001 files, invariants, checksums, and regeneration are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

