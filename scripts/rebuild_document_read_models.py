#!/usr/bin/env python3
"""Rebuild current read models locally, preserving rollback on verification failure.

No canonical metadata, source/evidence bytes, or assessment scores are written.
The incoming ZIP manager protects package files; this inner transaction protects
locally generated outputs. It is an editing gate, not publication approval.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Callable, Sequence

ROOT = Path(__file__).resolve().parents[1]
GENERATED_FILES = (
    'tools/docs_index.json',
    'tools/docs_graph.json',
    'tools/docs_public_catalog.json',
    'tools/docs_public_graph.json',
    'tools/docs_registration_workbench.preview.json',
)
BUILD_DIRECTORY = '_build/pages'


def transactional_rebuild(root: Path, operation: Callable[[], None]) -> None:
    """Restore derived files/directories on a failed build, including first builds."""
    with tempfile.TemporaryDirectory(prefix='so-read-model-backup-') as tmp:
        backup = Path(tmp)
        original = {}
        for name in GENERATED_FILES:
            path = root / name
            original[name] = path.is_file()
            if path.is_file():
                dest = backup / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dest)
        build = root / BUILD_DIRECTORY
        build_existed = build.is_dir()
        if build_existed:
            shutil.copytree(build, backup / 'pages')
        try:
            operation()
        except BaseException:
            for name, existed in original.items():
                path = root / name
                if existed:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup / name, path)
                elif path.exists():
                    path.unlink()
            if build.exists():
                shutil.rmtree(build)
            if build_existed:
                shutil.copytree(backup / 'pages', build)
            print('READ-MODEL ROLLBACK: generated files restored.', file=sys.stderr)
            raise


def commands(report_dir: Path) -> list[tuple[str, Sequence[str]]]:
    py = sys.executable
    return [
        ('Manifest and role contract', [py, 'scripts/validate_docs_manifest.py']),
        ('Index', [py, 'scripts/build_docs_index.py', '--visibility', 'public']),
        ('Graph', [py, 'scripts/build_docs_graph.py', '--visibility', 'public']),
        ('Public catalog', [py, 'scripts/build_public_catalog.py']),
        ('Public graph', [py, 'scripts/build_public_graph.py']),
        ('Registration preview', [py, 'scripts/build_registration_workbench_preview.py']),
        ('Contract regression tests', [py, 'scripts/check_document_contract.py']),
        ('Navigator interface', [py, 'scripts/check_navigator_interface.py']),
        ('Language resolution', ['node', 'scripts/check_navigator_language_resolution.mjs']),
        ('Reader/search regression', ['node', 'scripts/check_navigator_reading.mjs']),
        ('Registration self-test', [py, 'scripts/validate_registration_review.py', '--self-test']),
        ('Registration boundary', [py, 'scripts/check_registration_workbench.py']),
        ('UTF-8 reader', [py, 'scripts/serve_navigator.py', '--check']),
        ('Public format', [py, 'scripts/check_public_format.py', '--root', '.', '--check-anchors', '--manifest-check-unlisted',
                           '--md-log', str(report_dir / 'public-format.md'), '--json-log', str(report_dir / 'public-format.json')]),
        ('Public site build', [py, 'scripts/build_public_site.py']),
        ('Public site artifact', [py, 'scripts/check_public_site.py']),
        ('Deterministic site', [py, 'scripts/build_public_site.py', '--check']),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    if root != ROOT:
        parser.error('Run the script belonging to the target repository; --root must match its root.')
    report_dir = Path(tempfile.mkdtemp(prefix='so-v51-document-check-'))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
    def operation() -> None:
        for label, command in commands(report_dir):
            print('\n== '+label+' ==', flush=True)
            result = subprocess.run(command, cwd=root, env=env, check=False)
            if result.returncode:
                raise RuntimeError(label+' failed (exit '+str(result.returncode)+')')
        if (root / '.git').exists():
            subprocess.run(['git', 'diff', '--check'], cwd=root, check=True)
    try:
        transactional_rebuild(root, operation)
    except Exception as exc:
        print('DOCUMENT PIPELINE BLOCKED: '+str(exc), file=sys.stderr)
        print('Temporary diagnostics: '+str(report_dir), file=sys.stderr)
        return 1
    print('\nDOCUMENT PIPELINE PASS. Current read models regenerated locally.')
    print('Temporary diagnostics: '+str(report_dir))
    print('No score approval, Git commit, remote write or publication was performed.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
