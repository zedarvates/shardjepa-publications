#!/usr/bin/env python3
"""Generate the deterministic DATA-2026-001 numerical Poincare fixture."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from pathlib import Path


SEED = 42
COUNT = 1_000
DIMENSION = 128
CURVATURE = 1.0
EPSILON = 1e-5
BRANCHING_FACTOR = 4
GENERATOR_VERSION = "1.1.0"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def lcg(state: int) -> int:
    return (state * 1_664_525 + 1_013_904_223) & 0xFFFFFFFF


def generate(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    max_norm = (1.0 - EPSILON) / math.sqrt(CURVATURE)
    state = SEED
    vector_bytes = bytearray()
    hierarchy_rows = ["node_id,parent_id,depth"]
    depths = [0] * COUNT

    for index in range(COUNT):
        direction: list[float] = []
        for _ in range(DIMENSION):
            state = lcg(state)
            direction.append((state / 4_294_967_295.0) - 0.5)

        direction_norm = math.sqrt(sum(value * value for value in direction))
        phase = (index % 100) / 99.0
        target_norm = max_norm * (0.05 + 0.94 * phase)
        scale = target_norm / direction_norm
        for value in direction:
            vector_bytes.extend(struct.pack("<f", value * scale))

        if index == 0:
            parent = -1
            depth = 0
        else:
            parent = (index - 1) // BRANCHING_FACTOR
            depth = depths[parent] + 1
        depths[index] = depth
        hierarchy_rows.append(f"{index},{parent},{depth}")

    vectors_path = output_dir / "vectors.f32le"
    vectors_path.write_bytes(vector_bytes)
    (output_dir / "hierarchy.csv").write_text(
        "\n".join(hierarchy_rows) + "\n", encoding="utf-8", newline="\n"
    )

    splits = {
        "train": list(range(0, 700)),
        "validation": list(range(700, 850)),
        "test": list(range(850, 1_000)),
    }
    (output_dir / "splits.json").write_text(
        json.dumps(splits, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    generator_path = Path(__file__).resolve()
    manifest = {
        "schema_version": 1,
        "dataset_id": "DATA-2026-001",
        "title": "Poincare Hyperbolic Latent Numerical Fixture",
        "status": "repository_release",
        "count": COUNT,
        "dimension": DIMENSION,
        "curvature": CURVATURE,
        "epsilon": EPSILON,
        "max_norm": max_norm,
        "seed": SEED,
        "generator_version": GENERATOR_VERSION,
        "generator_sha256": sha256(generator_path),
        "payload": {
            "file": "vectors.f32le",
            "format": "contiguous IEEE 754 binary32, little-endian",
            "byte_size": len(vector_bytes),
            "sha256": hashlib.sha256(vector_bytes).hexdigest(),
        },
        "hierarchy": {
            "file": "hierarchy.csv",
            "branching_factor": BRANCHING_FACTOR,
            "relationship_to_vectors": "labels are independent of vector coordinates",
        },
        "splits": {name: len(indices) for name, indices in splits.items()},
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    checksum_names = ["vectors.f32le", "hierarchy.csv", "splits.json", "manifest.json"]
    if output_dir.resolve() == generator_path.parent:
        checksum_names.extend(["generate.py", "validate.py", "README.md"])
    checksum_lines = [f"{sha256(output_dir / name)}  {name}" for name in checksum_names]
    (output_dir / "SHA256SUMS").write_text(
        "\n".join(checksum_lines) + "\n", encoding="ascii", newline="\n"
    )

    print(f"[OK] generated DATA-2026-001: {COUNT} vectors x {DIMENSION} dimensions")
    print(f"[OK] vector SHA-256: {manifest['payload']['sha256']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="target directory; defaults to the dataset directory",
    )
    args = parser.parse_args()
    generate(args.output_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

