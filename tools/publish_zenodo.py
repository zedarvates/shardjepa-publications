#!/usr/bin/env python3
"""Preview, draft, or publish one ShardJEPA artifact through the Zenodo API."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


PRODUCTION_API = "https://zenodo.org/api/deposit/depositions"
SANDBOX_API = "https://sandbox.zenodo.org/api/deposit/depositions"
DEFAULT_ORCID = "0009-0009-1286-3683"


def request_json(
    url: str,
    token: str,
    method: str = "GET",
    payload: dict | None = None,
    raw_data: bytes | None = None,
    content_type: str = "application/json",
) -> dict:
    if payload is not None and raw_data is not None:
        raise ValueError("payload and raw_data are mutually exclusive")
    data = raw_data
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = content_type
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = response.read()
            return json.loads(body.decode("utf-8")) if body else {}
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Zenodo HTTP {error.code}: {detail}") from error


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_metadata(args: argparse.Namespace) -> dict:
    return {
        "title": args.title,
        "upload_type": "publication",
        "publication_type": "report",
        "description": args.description,
        "creators": [{"name": args.creator, "orcid": args.orcid}],
        "access_right": "open",
        "license": "cc-by-4.0",
        "keywords": ["ShardJEPA", "JEPA", "Rust", "latent representations"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument(
        "--description",
        default="Versioned ShardJEPA repository preprints and reproducibility evidence.",
    )
    parser.add_argument("--creator", default="Sylvain Galliez")
    parser.add_argument("--orcid", default=DEFAULT_ORCID)
    parser.add_argument("--deposition-id", type=int, help="reuse an existing draft")
    parser.add_argument("--sandbox", action="store_true")
    parser.add_argument("--execute", action="store_true", help="create or update a draft")
    parser.add_argument("--publish", action="store_true", help="publish after upload")
    parser.add_argument("--yes", action="store_true", help="confirm the network mutation")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    artifact = args.artifact.resolve()
    if not artifact.is_file():
        print(f"[ERROR] artifact not found: {artifact}")
        return 2
    if args.publish and not args.execute:
        print("[ERROR] --publish requires --execute")
        return 2

    metadata = build_metadata(args)
    preview = {
        "endpoint": "sandbox" if args.sandbox else "production",
        "artifact": str(artifact),
        "bytes": artifact.stat().st_size,
        "sha256": file_sha256(artifact),
        "metadata": metadata,
        "requested_action": "publish" if args.publish else "draft",
    }
    print(json.dumps(preview, ensure_ascii=False, indent=2))
    if not args.execute:
        print("[DRY RUN] no Zenodo request sent; add --execute --yes to create/update a draft")
        return 0
    if not args.yes:
        print("[ERROR] --execute requires --yes")
        return 2

    token = os.environ.get("ZENODO_API_TOKEN")
    if not token:
        print("[ERROR] ZENODO_API_TOKEN is not set")
        return 2

    base_url = SANDBOX_API if args.sandbox else PRODUCTION_API
    try:
        if args.deposition_id:
            deposition = request_json(f"{base_url}/{args.deposition_id}", token)
        else:
            deposition = request_json(base_url, token, method="POST", payload={})

        deposition_id = deposition["id"]
        html_url = deposition.get("links", {}).get("html")
        print(f"[OK] draft deposition: {deposition_id}")
        if html_url:
            print(f"[OK] draft URL: {html_url}")

        bucket_url = deposition.get("links", {}).get("bucket")
        if not bucket_url:
            raise RuntimeError("Zenodo response did not include an upload bucket")
        upload_url = f"{bucket_url}/{urllib.parse.quote(artifact.name)}"
        request_json(
            upload_url,
            token,
            method="PUT",
            raw_data=artifact.read_bytes(),
            content_type="application/octet-stream",
        )
        print(f"[OK] uploaded: {artifact.name}")

        updated = request_json(
            f"{base_url}/{deposition_id}",
            token,
            method="PUT",
            payload={"metadata": metadata},
        )
        reserved_doi = updated.get("metadata", {}).get("prereserve_doi", {}).get("doi")
        if reserved_doi:
            print(f"[OK] reserved DOI: {reserved_doi}")

        if args.publish:
            published = request_json(
                f"{base_url}/{deposition_id}/actions/publish", token, method="POST"
            )
            print(f"[PUBLISHED] DOI: {published.get('doi')}")
            print(f"[PUBLISHED] URL: {published.get('links', {}).get('record_html')}")
        else:
            print("[DRAFT] review the Zenodo record before rerunning with --publish")
    except (RuntimeError, KeyError, OSError) as error:
        print(f"[ERROR] {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

