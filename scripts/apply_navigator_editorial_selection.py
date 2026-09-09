#!/usr/bin/env python3
"""Dry-run or explicitly apply a validated Navigator editorial selection."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_navigator_editorial_selection import (
    EditorialSelectionError,
    PUBLIC_CONTENT,
    summarize,
    validate_transaction,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transaction", type=Path)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write only reading_channels in navigator/public-content.json; without this flag, dry-run only",
    )
    args = parser.parse_args()

    try:
        payload = validate_transaction(args.transaction.resolve())
    except EditorialSelectionError as exc:
        raise SystemExit(f"Navigator editorial apply: FAIL\n{exc}") from exc

    after = payload["after"]
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"Navigator editorial apply: {mode}")
    print(summarize(after))
    if not args.apply:
        print("No repository file was changed. Re-run with --apply after reviewing this plan.")
        return

    content = json.loads(PUBLIC_CONTENT.read_text(encoding="utf-8-sig"))
    content["reading_channels"] = after
    PUBLIC_CONTENT.write_text(
        json.dumps(content, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Updated only reading_channels: {PUBLIC_CONTENT.relative_to(PUBLIC_CONTENT.parents[1])}")


if __name__ == "__main__":
    main()
