#!/usr/bin/env python3
"""Receive external update ZIPs through the Scientific Ontology repository boundary.

Workflow:
    inspect -> register -> plan -> apply

The package identity is the exact ZIP SHA-256. The tool never deletes repository files.
It accepts repository-relative ZIPs (the normal AI handoff format) and may also accept a
single top-level wrapper directory matching the repository directory name or a configured
wrapper name.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = ROOT / "tools" / "repository_handoff_policy.json"
DEFAULT_REGISTRY = ROOT / "tools" / "zip_package_registry.tsv"
REGISTRY_HEADER = "# sha256<TAB>layout<TAB>filename\n"


class HandoffError(RuntimeError):
    pass


@dataclass(frozen=True)
class PackageEntry:
    zip_name: str
    repo_path: str
    file_size: int
    compressed_size: int
    sha256: str


@dataclass(frozen=True)
class Inspection:
    zip_path: Path
    filename: str
    sha256: str
    layout: str
    entries: tuple[PackageEntry, ...]
    total_uncompressed: int


@dataclass(frozen=True)
class RegistryRecord:
    sha256: str
    layout: str
    filename: str


@dataclass(frozen=True)
class PlanItem:
    state: str
    repo_path: str
    boundary: bool
    ignored: bool
    package_sha256: str
    repository_sha256: str | None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_stream(stream) -> str:
    h = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        h.update(chunk)
    return h.hexdigest()


def load_policy(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise HandoffError(f"Policy file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise HandoffError(f"Invalid policy JSON: {path}: {exc}") from exc

    required = {
        "schema_version",
        "repository_id",
        "repository_markers",
        "accepted_wrapper_roots",
        "forbidden_exact_paths",
        "forbidden_prefixes",
        "forbidden_segments",
        "boundary_exact_paths",
        "boundary_prefixes",
        "archive_limits",
        "text_contract",
        "verification_hooks",
    }
    missing = sorted(required - data.keys())
    if missing:
        raise HandoffError(f"Policy missing required keys: {', '.join(missing)}")
    return data


def assert_repository_identity(root: Path, policy: dict) -> None:
    missing = [p for p in policy["repository_markers"] if not (root / p).exists()]
    if missing:
        raise HandoffError(
            "Repository identity check failed; missing markers: " + ", ".join(missing)
        )
    proc = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if proc.returncode != 0:
        raise HandoffError("Repository identity check failed: this is not a Git work tree.")
    git_root = Path(proc.stdout.strip()).resolve()
    if git_root != root.resolve():
        raise HandoffError(f"Repository identity check failed: Git root is {git_root}, expected {root.resolve()}")


def normalize_zip_name(raw: str) -> str:
    name = raw.replace("\\", "/")
    if not name or name == "/":
        return ""
    if name.startswith("/") or (len(name) >= 2 and name[1] == ":"):
        raise HandoffError(f"ZIP contains an absolute path: {raw}")
    while name.endswith("/"):
        name = name[:-1]
    if not name:
        return ""
    parts = name.split("/")
    for segment in parts:
        if segment in {"", ".", ".."}:
            raise HandoffError(f"ZIP contains invalid/traversal path syntax: {raw}")
        if segment.endswith(" ") or segment.endswith(".") or ":" in segment:
            raise HandoffError(f"ZIP contains a Windows-unsafe path segment: {raw}")
        base = segment.split(".", 1)[0].upper()
        if base in {
            "CON", "PRN", "AUX", "NUL",
            "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
            "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
        }:
            raise HandoffError(f"ZIP contains a reserved Windows path segment: {raw}")
    return "/".join(parts)


def is_zip_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0o170000
    return mode == stat.S_IFLNK


def is_forbidden(repo_path: str, policy: dict) -> bool:
    key = repo_path.casefold()
    if any(key == p.casefold() for p in policy["forbidden_exact_paths"]):
        return True
    if any(key.startswith(p.casefold().rstrip("/") + "/") for p in policy["forbidden_prefixes"]):
        return True
    segments = {part.casefold() for part in PurePosixPath(repo_path).parts}
    return any(str(seg).casefold() in segments for seg in policy["forbidden_segments"])


def is_boundary(repo_path: str, policy: dict) -> bool:
    key = repo_path.casefold()
    if any(key == p.casefold() for p in policy["boundary_exact_paths"]):
        return True
    return any(key.startswith(p.casefold().rstrip("/") + "/") for p in policy["boundary_prefixes"])


def detect_layout(normalized_files: list[str], root: Path, policy: dict) -> tuple[str, str | None]:
    if not normalized_files:
        raise HandoffError("ZIP contains no files.")
    first_parts = [name.split("/", 1) for name in normalized_files]
    wrapper_candidates = {root.name.casefold()}
    wrapper_candidates.update(str(x).casefold() for x in policy["accepted_wrapper_roots"])
    if all(len(parts) == 2 for parts in first_parts):
        first = first_parts[0][0]
        if all(parts[0].casefold() == first.casefold() for parts in first_parts):
            if first.casefold() in wrapper_candidates:
                return f"wrapped:{first}", first
    return "relative", None


def repo_path_from_zip_name(name: str, wrapper: str | None) -> str:
    if wrapper is None:
        return name
    prefix = wrapper + "/"
    if not name.casefold().startswith(prefix.casefold()):
        raise HandoffError(f"ZIP wrapper layout is inconsistent: {name}")
    relative = name[len(prefix):]
    if not relative:
        raise HandoffError(f"ZIP contains wrapper-only file path: {name}")
    return relative


def validate_text_bytes(repo_path: str, data: bytes, policy: dict) -> None:
    contract = policy["text_contract"]
    exact = {p.casefold(): v for p, v in contract.get("exact_paths", {}).items()}
    suffix_rules = {k.casefold(): v for k, v in contract.get("suffixes", {}).items()}
    rule = exact.get(repo_path.casefold())
    if rule is None:
        suffix = Path(repo_path).suffix.casefold()
        rule = suffix_rules.get(suffix)
    if rule is None:
        return

    if data.startswith(b"\xef\xbb\xbf"):
        raise HandoffError(f"Text contract violation (UTF-8 BOM): {repo_path}")
    try:
        data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise HandoffError(f"Text contract violation (not strict UTF-8): {repo_path}: {exc}") from exc

    eol = rule.get("eol")
    if eol == "lf":
        if b"\r" in data:
            raise HandoffError(f"Text contract violation (LF required): {repo_path}")
    elif eol == "crlf":
        without_crlf = data.replace(b"\r\n", b"")
        if b"\r" in without_crlf or b"\n" in without_crlf:
            raise HandoffError(f"Text contract violation (CRLF required): {repo_path}")

    if rule.get("final_newline", False) and data and not data.endswith(b"\n"):
        raise HandoffError(f"Text contract violation (final newline required): {repo_path}")


def inspect_package(zip_path: Path, root: Path, policy: dict) -> Inspection:
    zip_path = zip_path.expanduser().resolve()
    if not zip_path.is_file() or zip_path.suffix.casefold() != ".zip":
        raise HandoffError(f"ZIP file not found or not .zip: {zip_path}")
    try:
        zip_path.relative_to(root.resolve())
    except ValueError:
        pass
    else:
        raise HandoffError("Incoming ZIP must be kept outside the repository root.")

    limits = policy["archive_limits"]
    max_files = int(limits["max_files"])
    max_total = int(limits["max_total_uncompressed_bytes"])
    max_file = int(limits["max_single_file_bytes"])
    max_ratio = float(limits["max_compression_ratio"])

    package_sha = sha256_file(zip_path)
    normalized_info: list[tuple[zipfile.ZipInfo, str]] = []

    try:
        archive = zipfile.ZipFile(zip_path, "r")
    except zipfile.BadZipFile as exc:
        raise HandoffError(f"Invalid ZIP archive: {zip_path}") from exc

    with archive:
        total = 0
        seen_raw: set[str] = set()
        for info in archive.infolist():
            raw = info.filename
            name = normalize_zip_name(raw)
            if not name:
                continue
            if info.is_dir():
                continue
            if info.flag_bits & 0x1:
                raise HandoffError(f"Encrypted ZIP entries are not accepted: {raw}")
            if is_zip_symlink(info):
                raise HandoffError(f"Symlink entries are not accepted: {raw}")
            raw_key = name.casefold()
            if raw_key in seen_raw:
                raise HandoffError(f"ZIP contains duplicate/case-colliding entry: {raw}")
            seen_raw.add(raw_key)
            if info.file_size > max_file:
                raise HandoffError(f"ZIP entry exceeds single-file limit: {raw}")
            total += info.file_size
            if total > max_total:
                raise HandoffError("ZIP exceeds total uncompressed-size limit.")
            if info.file_size > 0:
                if info.compress_size == 0:
                    raise HandoffError(f"ZIP entry has suspicious compression ratio: {raw}")
                ratio = info.file_size / info.compress_size
                if ratio > max_ratio:
                    raise HandoffError(f"ZIP entry exceeds compression-ratio limit: {raw}")
            normalized_info.append((info, name))

        if not normalized_info:
            raise HandoffError("ZIP contains no files.")
        if len(normalized_info) > max_files:
            raise HandoffError(f"ZIP exceeds file-count limit ({max_files}).")

        bad = archive.testzip()
        if bad is not None:
            raise HandoffError(f"ZIP CRC verification failed: {bad}")

        layout, wrapper = detect_layout([name for _, name in normalized_info], root, policy)
        entries: list[PackageEntry] = []
        seen_repo: set[str] = set()
        for info, name in normalized_info:
            repo_path = repo_path_from_zip_name(name, wrapper)
            key = repo_path.casefold()
            if key in seen_repo:
                raise HandoffError(f"ZIP maps multiple entries to one repository path: {repo_path}")
            seen_repo.add(key)
            if is_forbidden(repo_path, policy):
                raise HandoffError(f"Incoming ZIP is forbidden from carrying: {repo_path}")
            with archive.open(info, "r") as stream:
                data = stream.read()
            validate_text_bytes(repo_path, data, policy)
            entries.append(
                PackageEntry(
                    zip_name=info.filename,
                    repo_path=repo_path,
                    file_size=info.file_size,
                    compressed_size=info.compress_size,
                    sha256=hashlib.sha256(data).hexdigest(),
                )
            )

    return Inspection(
        zip_path=zip_path,
        filename=zip_path.name,
        sha256=package_sha,
        layout=layout,
        entries=tuple(sorted(entries, key=lambda x: x.repo_path.casefold())),
        total_uncompressed=sum(e.file_size for e in entries),
    )


def load_registry(path: Path) -> list[RegistryRecord]:
    if not path.exists():
        raise HandoffError(f"Registry not found: {path}")
    records: list[RegistryRecord] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != 3:
            raise HandoffError(f"Invalid registry line {lineno}; expected sha256<TAB>layout<TAB>filename")
        sha, layout, filename = parts
        if len(sha) != 64 or any(c not in "0123456789abcdefABCDEF" for c in sha):
            raise HandoffError(f"Invalid SHA-256 in registry line {lineno}")
        records.append(RegistryRecord(sha.casefold(), layout, filename))
    return records


def registration_status(inspection: Inspection, records: list[RegistryRecord]) -> tuple[str, RegistryRecord | None]:
    same_sha = [r for r in records if r.sha256 == inspection.sha256]
    filename_rows = [r for r in records if r.filename.casefold() == inspection.filename.casefold()]
    if same_sha:
        record = same_sha[0]
        if record.layout != inspection.layout:
            return "HASH MATCH / LAYOUT MISMATCH", record
        return "EXACT HASH REGISTERED", record
    if filename_rows:
        return "FILENAME COLLISION / DIFFERENT BYTES", filename_rows[0]
    return "UNREGISTERED", None


def register_package(inspection: Inspection, registry_path: Path) -> None:
    records = load_registry(registry_path)
    status_text, record = registration_status(inspection, records)
    if status_text == "EXACT HASH REGISTERED":
        print(f"Already registered by exact SHA-256: {record.filename}")
        return
    if status_text == "HASH MATCH / LAYOUT MISMATCH":
        raise HandoffError("The same package SHA is registered with a different layout; review registry manually.")
    if status_text == "FILENAME COLLISION / DIFFERENT BYTES":
        raise HandoffError(
            "The same ZIP filename is already registered with different bytes. "
            "Rename the new package before registering it."
        )

    existing = registry_path.read_text(encoding="utf-8")
    if existing and not existing.endswith("\n"):
        existing += "\n"
    new_line = f"{inspection.sha256}\t{inspection.layout}\t{inspection.filename}\n"
    registry_path.write_text(existing + new_line, encoding="utf-8", newline="\n")
    print(f"REGISTERED: {inspection.filename}")
    print("Registry changed; this is expected local provenance state.")


def assert_registered(inspection: Inspection, registry_path: Path) -> None:
    status_text, _ = registration_status(inspection, load_registry(registry_path))
    if status_text != "EXACT HASH REGISTERED":
        raise HandoffError(f"Package is not registered by exact SHA/layout: {status_text}")


def git_run(root: Path, args: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and proc.returncode != 0:
        raise HandoffError(f"git {' '.join(args)} failed:\n{proc.stderr or proc.stdout}")
    return proc


def path_is_ignored(root: Path, repo_path: str) -> bool:
    proc = git_run(root, ["check-ignore", "--quiet", "--no-index", "--", repo_path])
    return proc.returncode == 0


def build_plan(inspection: Inspection, root: Path, policy: dict) -> list[PlanItem]:
    plan: list[PlanItem] = []
    for entry in inspection.entries:
        dest = root / Path(*PurePosixPath(entry.repo_path).parts)
        if not dest.exists():
            state = "NEW"
            repo_sha = None
        elif not dest.is_file():
            raise HandoffError(f"Destination exists but is not a file: {entry.repo_path}")
        else:
            repo_sha = sha256_file(dest)
            state = "SAME" if repo_sha == entry.sha256 else "OVERWRITE"
        plan.append(
            PlanItem(
                state=state,
                repo_path=entry.repo_path,
                boundary=is_boundary(entry.repo_path, policy),
                ignored=path_is_ignored(root, entry.repo_path) if state == "NEW" else False,
                package_sha256=entry.sha256,
                repository_sha256=repo_sha,
            )
        )
    return sorted(plan, key=lambda x: x.repo_path.casefold())


def print_inspection(inspection: Inspection, status_text: str) -> None:
    print()
    print(f"ZIP:              {inspection.filename}")
    print(f"SHA-256:          {inspection.sha256}")
    print(f"Layout:           {inspection.layout}")
    print(f"Files:            {len(inspection.entries)}")
    print(f"Uncompressed:     {inspection.total_uncompressed} bytes")
    print(f"Registry:         {status_text}")
    print("Archive safety:   PASS")
    print("SO text contract: PASS")
    print()


def print_plan(plan: list[PlanItem]) -> None:
    for item in plan:
        flags: list[str] = []
        if item.boundary and item.state != "SAME":
            flags.append("BOUNDARY")
        if item.ignored:
            flags.append("IGNORED")
        suffix = "" if not flags else " [" + "][".join(flags) + "]"
        print(f"{item.state:<10} {item.repo_path}{suffix}")
    counts = {state: sum(1 for x in plan if x.state == state) for state in ("NEW", "SAME", "OVERWRITE")}
    boundary = sum(1 for x in plan if x.boundary and x.state != "SAME")
    ignored = sum(1 for x in plan if x.ignored)
    print()
    print(
        "Plan summary: "
        f"NEW={counts['NEW']} SAME={counts['SAME']} OVERWRITE={counts['OVERWRITE']} "
        f"BOUNDARY_CHANGE={boundary} IGNORED_NEW={ignored}"
    )


def assert_clean_worktree(root: Path, registry_path: Path, allow_dirty: bool) -> None:
    if allow_dirty:
        return
    proc = git_run(root, ["status", "--porcelain", "--untracked-files=all"], check=True)
    allowed = registry_path.relative_to(root).as_posix().casefold()
    unexpected: list[str] = []
    for line in proc.stdout.splitlines():
        if len(line) < 4:
            continue
        path_part = line[3:].strip().strip('"').replace("\\", "/")
        # Renames contain "old -> new" and are never the registry-only dirtiness.
        if " -> " in path_part or path_part.casefold() != allowed:
            unexpected.append(line)
    if unexpected:
        raise HandoffError(
            "Working tree has changes other than the ZIP registry. Review/commit them first, "
            "or use --allow-dirty-working-tree deliberately:\n  " + "\n  ".join(unexpected)
        )


def extract_entry(archive: zipfile.ZipFile, entry: PackageEntry, dest: Path) -> None:
    info = archive.getinfo(entry.zip_name)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with archive.open(info, "r") as src, dest.open("wb") as out:
        shutil.copyfileobj(src, out)


def run_verification_hooks(root: Path, policy: dict) -> None:
    print()
    print("Repository verification hooks:")
    for hook in policy["verification_hooks"]:
        label = hook["label"]
        command = [str(x) for x in hook["command"]]
        print(f"  RUN  {label}: {' '.join(command)}")
        proc = subprocess.run(
            command,
            cwd=root,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
        if proc.stdout:
            print(proc.stdout.rstrip())
        if proc.returncode != 0:
            if proc.stderr:
                print(proc.stderr.rstrip(), file=sys.stderr)
            raise HandoffError(f"Repository verification failed: {label}")
        print(f"  PASS {label}")

    diff_check = git_run(root, ["diff", "--check"])
    if diff_check.returncode != 0:
        raise HandoffError(f"git diff --check failed:\n{diff_check.stdout or diff_check.stderr}")
    print("  PASS git diff --check")


def apply_package(
    inspection: Inspection,
    plan: list[PlanItem],
    root: Path,
    policy: dict,
    registry_path: Path,
    *,
    allow_overwrite: bool,
    allow_boundary_change: bool,
    allow_dirty_working_tree: bool,
    allow_ignored_paths: bool,
    skip_repository_checks: bool,
) -> None:
    overwrite = [x for x in plan if x.state == "OVERWRITE"]
    boundary = [x for x in plan if x.boundary and x.state != "SAME"]
    ignored = [x for x in plan if x.ignored]
    if overwrite and not allow_overwrite:
        raise HandoffError("Plan contains OVERWRITE entries. Re-run apply with --allow-overwrite after review.")
    if boundary and not allow_boundary_change:
        raise HandoffError(
            "Plan contains repository-boundary changes. Re-run apply with --allow-boundary-change after review."
        )
    if ignored and not allow_ignored_paths:
        raise HandoffError(
            "Plan contains NEW files ignored by current .gitignore. Re-run only with --allow-ignored-paths after review."
        )

    assert_clean_worktree(root, registry_path, allow_dirty_working_tree)

    changed = [x for x in plan if x.state != "SAME"]
    by_repo = {e.repo_path: e for e in inspection.entries}
    created_files: list[Path] = []
    created_dirs: list[Path] = []

    with tempfile.TemporaryDirectory(prefix="so-handoff-") as temp:
        backup_root = Path(temp) / "backup"
        for item in changed:
            dest = root / Path(*PurePosixPath(item.repo_path).parts)
            if item.state == "OVERWRITE":
                backup = backup_root / Path(*PurePosixPath(item.repo_path).parts)
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dest, backup)

        try:
            with zipfile.ZipFile(inspection.zip_path, "r") as archive:
                for item in changed:
                    dest = root / Path(*PurePosixPath(item.repo_path).parts)
                    if item.state == "NEW":
                        parent = dest.parent
                        missing_chain: list[Path] = []
                        while parent != root and not parent.exists():
                            missing_chain.append(parent)
                            parent = parent.parent
                        for directory in reversed(missing_chain):
                            directory.mkdir()
                            created_dirs.append(directory)
                        created_files.append(dest)
                    extract_entry(archive, by_repo[item.repo_path], dest)
                    if sha256_file(dest) != by_repo[item.repo_path].sha256:
                        raise HandoffError(f"Applied bytes do not match package entry SHA-256: {item.repo_path}")
                    print(f"APPLIED {item.repo_path}")

            if not skip_repository_checks:
                run_verification_hooks(root, policy)
            else:
                print("WARNING: repository verification hooks were skipped by explicit request.")
        except Exception:
            print("Apply failed; rolling back package-changed repository files.", file=sys.stderr)
            for item in changed:
                dest = root / Path(*PurePosixPath(item.repo_path).parts)
                if item.state == "OVERWRITE":
                    backup = backup_root / Path(*PurePosixPath(item.repo_path).parts)
                    if backup.exists():
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(backup, dest)
                elif item.state == "NEW" and dest.exists():
                    dest.unlink()
            for directory in sorted(created_dirs, key=lambda p: len(p.parts), reverse=True):
                try:
                    directory.rmdir()
                except OSError:
                    pass
            raise

    print()
    print("ZIP apply complete. No repository file was deleted.")
    print("Applied bytes were re-hashed against the registered package.")
    if not skip_repository_checks:
        print("Configured SO repository verification hooks passed.")
    print("Next: review git status and git diff, then commit only after human review.")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Scientific Ontology incoming ZIP handoff boundary")
    p.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    p.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    sub = p.add_subparsers(dest="mode", required=True)
    for name in ("inspect", "register", "plan"):
        sp = sub.add_parser(name)
        sp.add_argument("--zip", dest="zip_path", type=Path, required=True)
    ap = sub.add_parser("apply")
    ap.add_argument("--zip", dest="zip_path", type=Path, required=True)
    ap.add_argument("--allow-overwrite", action="store_true")
    ap.add_argument("--allow-boundary-change", action="store_true")
    ap.add_argument("--allow-dirty-working-tree", action="store_true")
    ap.add_argument("--allow-ignored-paths", action="store_true")
    ap.add_argument("--skip-repository-checks", action="store_true")
    return p


def main() -> int:
    args = parser().parse_args()
    root = ROOT
    try:
        policy_path = args.policy if args.policy.is_absolute() else root / args.policy
        registry_path = args.registry if args.registry.is_absolute() else root / args.registry
        policy = load_policy(policy_path)
        assert_repository_identity(root, policy)
        inspection = inspect_package(args.zip_path, root, policy)
        records = load_registry(registry_path)
        status_text, _ = registration_status(inspection, records)
        print_inspection(inspection, status_text)

        if args.mode == "inspect":
            return 0
        if args.mode == "register":
            register_package(inspection, registry_path)
            return 0

        assert_registered(inspection, registry_path)
        plan = build_plan(inspection, root, policy)
        print_plan(plan)
        if args.mode == "plan":
            print("No repository file was changed.")
            return 0

        apply_package(
            inspection,
            plan,
            root,
            policy,
            registry_path,
            allow_overwrite=args.allow_overwrite,
            allow_boundary_change=args.allow_boundary_change,
            allow_dirty_working_tree=args.allow_dirty_working_tree,
            allow_ignored_paths=args.allow_ignored_paths,
            skip_repository_checks=args.skip_repository_checks,
        )
        return 0
    except HandoffError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
