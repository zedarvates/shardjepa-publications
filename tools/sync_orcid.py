#!/usr/bin/env python3
"""Check local ORCID/BibTeX readiness without mutating an ORCID record."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="retained for explicit workflows")
    args = parser.parse_args()
    del args

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    root = Path(__file__).resolve().parent.parent
    try:
        registry = json.loads((root / "ORCID_INDEX.json").read_text(encoding="utf-8"))
        bibliography = (root / "citations.bib").read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as error:
        print(f"[ERROR] {error}")
        return 1

    errors: list[str] = []
    orcid_id = registry.get("orcid_id", "")
    if orcid_id not in bibliography:
        errors.append("citations.bib does not contain the registry ORCID")

    for output in registry.get("research_outputs", []):
        citation_key = output.get("citation_key")
        if citation_key and f"{{{citation_key}," not in bibliography:
            errors.append(f"missing BibTeX record: {citation_key}")

    for error in errors:
        print(f"[ERROR] {error}")
    if errors:
        return 1

    print(f"[OK] local bibliography is consistent for ORCID {orcid_id}")
    print("[INFO] no ORCID network request was sent")
    print(
        "[INFO] automated writes require an ORCID Member API integration and "
        "record-holder permission"
    )
    print("[INFO] otherwise import citations.bib manually after public release")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

