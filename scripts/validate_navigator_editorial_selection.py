#!/usr/bin/env python3
"""Validate a Developer Navigator editorial-reading selection transaction.

The browser editor never writes canonical repository files. It exports a
transaction that is rebound to the current navigator/public-content.json before
any repository-side apply is allowed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_CONTENT = ROOT / "navigator/public-content.json"
PUBLIC_CATALOG = ROOT / "tools/docs_public_catalog.json"
TARGET = "navigator/public-content.json"
SCHEMA_VERSION = "0.1"
MUTABLE_FIELDS = {"enabled", "documents"}


class EditorialSelectionError(ValueError):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise EditorialSelectionError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EditorialSelectionError(f"invalid JSON: {path}: {exc}") from exc


def current_channels() -> list[dict[str, Any]]:
    content = load_json(PUBLIC_CONTENT)
    channels = content.get("reading_channels")
    if not isinstance(channels, list) or not channels:
        raise EditorialSelectionError("navigator/public-content.json has no reading_channels")
    if not all(isinstance(item, dict) for item in channels):
        raise EditorialSelectionError("reading_channels must contain objects")
    return channels


def public_documents() -> list[dict[str, Any]]:
    catalog = load_json(PUBLIC_CATALOG)
    documents = catalog.get("documents")
    if not isinstance(documents, list):
        raise EditorialSelectionError("tools/docs_public_catalog.json has no documents array")
    if not all(isinstance(item, dict) for item in documents):
        raise EditorialSelectionError("public catalog documents must be objects")
    return documents


def document_id(doc: dict[str, Any]) -> str:
    value = doc.get("id") or doc.get("doc_id") or doc.get("path")
    return str(value or "")


def family_key(doc: dict[str, Any]) -> str:
    presentation = doc.get("presentation") if isinstance(doc.get("presentation"), dict) else {}
    language_relation = doc.get("language_relation") if isinstance(doc.get("language_relation"), dict) else {}
    return str(
        presentation.get("family_key")
        or language_relation.get("family_id")
        or document_id(doc)
    )


def validate_channel_shape(
    after: dict[str, Any],
    canonical: dict[str, Any],
    docs_by_id: dict[str, dict[str, Any]],
) -> None:
    channel_id = str(canonical.get("id") or "")
    if not channel_id or str(after.get("id") or "") != channel_id:
        raise EditorialSelectionError(f"channel identity changed: expected {channel_id!r}")

    immutable_keys = (set(canonical) | set(after)) - MUTABLE_FIELDS
    for key in sorted(immutable_keys):
        if after.get(key) != canonical.get(key):
            raise EditorialSelectionError(
                f"channel {channel_id!r}: field {key!r} is not editor-mutable"
            )

    enabled = after.get("enabled", True)
    if not isinstance(enabled, bool):
        raise EditorialSelectionError(f"channel {channel_id!r}: enabled must be boolean")

    selected = after.get("documents")
    if not isinstance(selected, list) or not all(isinstance(value, str) and value for value in selected):
        raise EditorialSelectionError(f"channel {channel_id!r}: documents must be a list of non-empty document IDs")
    if len(set(selected)) != len(selected):
        raise EditorialSelectionError(f"channel {channel_id!r}: duplicate document ID")

    seen_families: set[str] = set()
    for selected_id in selected:
        doc = docs_by_id.get(selected_id)
        if not doc:
            raise EditorialSelectionError(
                f"channel {channel_id!r}: document is not in the public catalog: {selected_id}"
            )
        family = family_key(doc)
        if family in seen_families:
            raise EditorialSelectionError(
                f"channel {channel_id!r}: duplicate JA/EN document family: {family}"
            )
        seen_families.add(family)


def validate_transaction(path: Path) -> dict[str, Any]:
    root = load_json(path)
    payload = root.get("navigator_editorial_selection") if isinstance(root, dict) else None
    if not isinstance(payload, dict):
        raise EditorialSelectionError("missing navigator_editorial_selection object")
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise EditorialSelectionError(
            f"unsupported schema_version: {payload.get('schema_version')!r}; expected {SCHEMA_VERSION!r}"
        )
    if payload.get("target") != TARGET:
        raise EditorialSelectionError(f"unexpected target: {payload.get('target')!r}")

    before = payload.get("before")
    after = payload.get("after")
    if not isinstance(before, list) or not isinstance(after, list):
        raise EditorialSelectionError("before/after must be arrays")

    canonical = current_channels()
    if before != canonical:
        raise EditorialSelectionError(
            "stale transaction: before does not exactly match the current reading_channels"
        )
    if len(after) != len(canonical):
        raise EditorialSelectionError("after must preserve the current channel set")

    docs = public_documents()
    docs_by_id: dict[str, dict[str, Any]] = {}
    for doc in docs:
        key = document_id(doc)
        if not key:
            raise EditorialSelectionError("public catalog contains a document without a usable ID")
        if key in docs_by_id:
            raise EditorialSelectionError(f"public catalog document ID is not unique: {key}")
        docs_by_id[key] = doc

    for index, (after_channel, canonical_channel) in enumerate(zip(after, canonical, strict=True)):
        if not isinstance(after_channel, dict):
            raise EditorialSelectionError(f"after channel #{index + 1} is not an object")
        validate_channel_shape(after_channel, canonical_channel, docs_by_id)

    return payload


def summarize(channels: list[dict[str, Any]]) -> str:
    parts = []
    for channel in channels:
        parts.append(
            f"{channel.get('id')}: enabled={str(channel.get('enabled', True)).lower()}, "
            f"documents={len(channel.get('documents') or [])}"
        )
    return "; ".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transaction", type=Path)
    args = parser.parse_args()
    try:
        payload = validate_transaction(args.transaction.resolve())
    except EditorialSelectionError as exc:
        raise SystemExit(f"Navigator editorial selection: FAIL\n{exc}") from exc
    print("Navigator editorial selection: PASS")
    print(summarize(payload["after"]))


if __name__ == "__main__":
    main()
