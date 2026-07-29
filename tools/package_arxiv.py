#!/usr/bin/env python3
"""Check or package TeX sources for one ShardJEPA arXiv submission."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


ALLOWED_SUFFIXES = {
    ".tex",
    ".bib",
    ".bst",
    ".cls",
    ".sty",
    ".png",
    ".jpg",
    ".jpeg",
    ".pdf",
    ".eps",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_id", help="directory name below publications/papers")
    parser.add_argument("--check", action="store_true", help="check readiness only")
    parser.add_argument("--output", type=Path, help="override output ZIP path")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root = Path(__file__).resolve().parent.parent
    papers_root = (root / "papers").resolve()
    paper_dir = (papers_root / args.paper_id).resolve()
    if paper_dir.parent != papers_root or not paper_dir.is_dir():
        print(f"[ERROR] invalid paper directory: {args.paper_id}")
        return 2

    main_tex = paper_dir / "paper.tex"
    if not main_tex.is_file():
        print(f"[NOT READY] missing compilable TeX source: {main_tex}")
        print("Markdown paper.md is a repository preprint source, not an arXiv TeX bundle.")
        return 2

    files = [
        path
        for path in sorted(paper_dir.rglob("*"), key=lambda item: item.as_posix())
        if path.is_file() and not path.is_symlink() and path.suffix.lower() in ALLOWED_SUFFIXES
    ]
    print(f"[OK] TeX entry point: {main_tex}")
    print(f"[OK] allowed source files: {len(files)}")
    if args.check:
        return 0

    output = args.output or root / "dist" / f"arxiv-{args.paper_id}.zip"
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for path in files:
            zip_file.write(path, path.relative_to(paper_dir).as_posix())
    print(f"[OK] arXiv source bundle: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

