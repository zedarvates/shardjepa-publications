#!/usr/bin/env python3
"""Create a deterministic ZIP of the ShardJEPA publication directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from datetime import datetime
from pathlib import Path


EXCLUDED_PARTS = {".git", "__pycache__", "dist"}
EXCLUDED_NAMES = {"arxiv_paper_01.zip"}


def iter_release_files(root: Path):
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root)
        if EXCLUDED_PARTS.intersection(relative.parts):
            continue
        if path.name in EXCLUDED_NAMES or path.suffix == ".pyc":
            continue
        yield path, relative


def release_timestamp(version: str) -> tuple[int, int, int, int, int, int]:
    try:
        parsed = datetime.strptime(version, "%Y.%m.%d")
    except ValueError as error:
        raise ValueError("release version must use YYYY.MM.DD") from error
    return (parsed.year, parsed.month, parsed.day, 0, 0, 0)


def add_deterministic(
    zip_file: zipfile.ZipFile,
    source: Path,
    relative: Path,
    timestamp: tuple[int, int, int, int, int, int],
) -> None:
    info = zipfile.ZipInfo(relative.as_posix(), date_time=timestamp)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    zip_file.writestr(info, source.read_bytes())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", help="release version, for example 2026.07.29")
    parser.add_argument("--output", type=Path, help="override output ZIP path")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root = Path(__file__).resolve().parent.parent
    registry = json.loads((root / "ORCID_INDEX.json").read_text(encoding="utf-8"))
    version = args.version or registry["repository"]["release"].removeprefix("v")
    try:
        timestamp = release_timestamp(version)
    except ValueError as error:
        print(f"[ERROR] {error}")
        return 2
    output = args.output or root / "dist" / f"shardjepa-publications-{version}.zip"
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    files = list(iter_release_files(root))
    if not files:
        print("[ERROR] no publication files found")
        return 1

    with zipfile.ZipFile(output, "w") as zip_file:
        for source, relative in files:
            add_deterministic(zip_file, source, relative, timestamp)

    digest = sha256(output)
    checksum_path = output.with_suffix(output.suffix + ".sha256")
    checksum_path.write_text(f"{digest}  {output.name}\n", encoding="ascii")
    print(f"[OK] files: {len(files)}")
    print(f"[OK] archive: {output}")
    print(f"[OK] sha256: {digest}")
    print(f"[OK] checksum: {checksum_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
