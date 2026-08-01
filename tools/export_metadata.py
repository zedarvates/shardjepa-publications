#!/usr/bin/env python3
"""Validate the ShardJEPA publication registry and referenced artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PUBLIC_STATUSES = {
    "repository_preprint",
    "repository_technical_report",
    "archived_preprint",
    "published",
    "validated_draft",
    "planned",
    "released",
}


def resolve_publication_path(publications_root: Path, value: str) -> Path:
    normalized = value.replace("\\", "/")
    prefix = "publications/"
    if normalized.startswith(prefix):
        normalized = normalized[len(prefix) :]
    return publications_root / normalized


def valid_orcid(orcid_id: str) -> bool:
    compact = orcid_id.replace("-", "")
    if len(compact) != 16 or not compact[:15].isdigit():
        return False
    total = 0
    for character in compact[:15]:
        total = (total + int(character)) * 2
    result = (12 - total % 11) % 11
    expected = "X" if result == 10 else str(result)
    return compact[-1] == expected


def validate(publications_root: Path) -> tuple[list[str], list[str], dict]:
    registry_path = publications_root / "ORCID_INDEX.json"
    bibliography_path = publications_root / "citations.bib"
    errors: list[str] = []
    warnings: list[str] = []

    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"cannot read {registry_path}: {error}"], warnings, {}

    bibliography = ""
    try:
        bibliography = bibliography_path.read_text(encoding="utf-8")
    except OSError as error:
        errors.append(f"cannot read {bibliography_path}: {error}")

    orcid_id = registry.get("orcid_id", "")
    if not valid_orcid(orcid_id):
        errors.append(f"invalid ORCID checksum or format: {orcid_id!r}")

    creator = registry.get("creator", {})
    if not creator.get("name"):
        errors.append("creator.name is required")
    if creator.get("orcid") != f"https://orcid.org/{orcid_id}":
        errors.append("creator.orcid must match orcid_id")

    validation = registry.get("validation", {})
    evidence_value = validation.get("evidence")
    if not evidence_value:
        errors.append("validation.evidence is required")
    elif not resolve_publication_path(publications_root, evidence_value).is_file():
        errors.append(f"validation evidence is missing: {evidence_value}")

    outputs = registry.get("research_outputs")
    if not isinstance(outputs, list) or not outputs:
        errors.append("research_outputs must be a non-empty list")
        outputs = []

    seen_ids: set[str] = set()
    seen_keys: set[str] = set()
    for index, item in enumerate(outputs):
        label = item.get("id") or f"item[{index}]"
        if label in seen_ids:
            errors.append(f"duplicate output id: {label}")
        seen_ids.add(label)

        status = item.get("status")
        if status not in PUBLIC_STATUSES:
            errors.append(f"{label}: unsupported status {status!r}")

        path_value = item.get("path")
        if not path_value:
            errors.append(f"{label}: path is required")
        elif not resolve_publication_path(publications_root, path_value).is_file():
            errors.append(f"{label}: referenced file is missing: {path_value}")

        alternate_paths = item.get("alternate_paths", [])
        if not isinstance(alternate_paths, list):
            errors.append(f"{label}: alternate_paths must be a list when present")
        else:
            for alternate_path in alternate_paths:
                if not isinstance(alternate_path, str) or not alternate_path:
                    errors.append(f"{label}: alternate_paths entries must be non-empty strings")
                elif not resolve_publication_path(publications_root, alternate_path).is_file():
                    errors.append(f"{label}: alternate file is missing: {alternate_path}")

        citation_key = item.get("citation_key")
        if citation_key:
            if citation_key in seen_keys:
                errors.append(f"duplicate citation key: {citation_key}")
            seen_keys.add(citation_key)
            if f"{{{citation_key}," not in bibliography:
                errors.append(f"{label}: citation key absent from citations.bib")
        elif status not in {"planned"}:
            errors.append(f"{label}: citation_key is required for status {status}")

        doi = item.get("doi")
        if doi is not None and not str(doi).startswith("10."):
            errors.append(f"{label}: DOI must start with '10.' or be null")
        if status in {"archived_preprint", "published", "released"} and not (
            doi or item.get("url")
        ):
            errors.append(f"{label}: public status requires a DOI or URL")
        if status == "planned":
            if doi or item.get("url"):
                warnings.append(f"{label}: planned output unexpectedly has a DOI or URL")
            warnings.append(f"{label}: planned output has no released artifact")

    return errors, warnings, registry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json", action="store_true", help="emit a machine-readable validation result"
    )
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    publications_root = Path(__file__).resolve().parent.parent
    errors, warnings, registry = validate(publications_root)
    result = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "output_count": len(registry.get("research_outputs", [])),
        "orcid_id": registry.get("orcid_id"),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("ShardJEPA publication registry validation")
        print(f"ORCID: {result['orcid_id']}")
        print(f"Outputs: {result['output_count']}")
        for warning in warnings:
            print(f"[WARN] {warning}")
        for error in errors:
            print(f"[ERROR] {error}")
        print("[OK] registry is consistent" if not errors else "[FAIL] validation errors")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
