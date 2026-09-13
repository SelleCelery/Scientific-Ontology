#!/usr/bin/env python3
"""Validate current metadata, role contracts, coverage and fixed-source identity."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from document_contract import load_manifest, validate_manifest

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--release-gate',action='store_true',help='Unresolved historical integrity blocks publication, not local editing.')
    args=p.parse_args();root=args.root.resolve()
    try:
        m=load_manifest(root);errors,warnings=validate_manifest(root,m)
    except Exception as exc:
        print(f'MANIFEST CONTRACT ERROR: {exc}',file=sys.stderr);return 1
    for s in warnings:print('WARNING: '+s)
    for s in errors:print('ERROR: '+s,file=sys.stderr)
    if errors or (warnings and args.release_gate):
        print(f'MANIFEST CONTRACT BLOCKED: errors={len(errors)} unresolved={len(warnings)}');return 1
    print(f"MANIFEST CONTRACT PASS: documents={len(m['documents'])} managed_assets={len(m['managed_assets'])} retired={len(m['retired_documents'])}; assessment approval is separate")
    return 0
if __name__=='__main__':raise SystemExit(main())
