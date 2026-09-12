#!/usr/bin/env python3
"""Export qifu-drawer-form and qifu-shared to the standalone release repo."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "release" / "qifu-drawer-form"
PACKAGE_NAMES = ("qifu-drawer-form", "qifu-shared")
EXPECTED_REMOTE = "github.com/jingjingtu/qifu-drawer-form"
MANAGED_PATHS = (
    Path(".gitignore"),
    Path("README.md"),
    Path("AGENTS.md"),
    Path(".github/workflows/validate.yml"),
    Path("scripts/validate_release.py"),
    Path("skills/qifu-drawer-form"),
    Path("skills/qifu-shared"),
    Path("RELEASE_MANIFEST.json"),
)
LEGACY_PATHS = (Path("screenshots"),)
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache"}
SOURCE_PATHS = (
    Path("skills/qifu-drawer-form"),
    Path("skills/qifu-shared"),
    Path("release/qifu-drawer-form"),
    Path("scripts/sync_drawer_release.py"),
)


def run(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def release_files(stage: Path) -> list[Path]:
    return sorted(
        path
        for path in stage.rglob("*")
        if path.is_file()
        and path.name != "RELEASE_MANIFEST.json"
        and not SKIP_PARTS.intersection(path.parts)
    )


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def copy_path(source: Path, destination: Path) -> None:
    if source.is_dir():
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"),
        )
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build_release(stage: Path, source_commit: str) -> None:
    if stage.exists():
        remove_path(stage)
    stage.mkdir(parents=True)
    for source in sorted(path for path in TEMPLATE.rglob("*") if path.is_file()):
        copy_path(source, stage / source.relative_to(TEMPLATE))
    for package in PACKAGE_NAMES:
        copy_path(ROOT / "skills" / package, stage / "skills" / package)

    versions = {
        package: (stage / "skills" / package / "VERSION")
        .read_text(encoding="utf-8")
        .strip()
        for package in PACKAGE_NAMES
    }
    files = {
        path.relative_to(stage).as_posix(): sha256(path) for path in release_files(stage)
    }
    manifest = {
        "schemaVersion": 1,
        "sourceRepository": "jingjingtu/qifu-skills",
        "sourceCommit": source_commit,
        "packages": versions,
        "files": files,
    }
    (stage / "RELEASE_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def validate_stage(stage: Path) -> None:
    validator = stage / "scripts" / "validate_release.py"
    result = run(sys.executable, str(validator), cwd=stage, check=False)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode:
        raise RuntimeError("generated release failed validation")


def ensure_clean_repo(repo: Path, label: str) -> None:
    result = run("git", "status", "--porcelain", cwd=repo)
    if result.stdout.strip():
        raise RuntimeError(f"{label} has uncommitted changes; commit or stash them first")


def ensure_clean_source() -> None:
    result = run(
        "git",
        "status",
        "--porcelain",
        "--",
        *(path.as_posix() for path in SOURCE_PATHS),
        cwd=ROOT,
    )
    if result.stdout.strip():
        raise RuntimeError(
            "release source files have uncommitted changes; commit them before publishing"
        )


def preflight_target(target: Path, allow_any_target: bool) -> None:
    if not target.is_dir() or not (target / ".git").exists():
        raise RuntimeError(f"target is not a Git checkout: {target}")
    if target.resolve() == ROOT.resolve():
        raise RuntimeError("target must not be the source repository")
    ensure_clean_repo(target, "target repository")
    if not allow_any_target:
        remote = run("git", "remote", "get-url", "origin", cwd=target).stdout.strip()
        normalized = remote.removesuffix(".git").replace(":", "/")
        if EXPECTED_REMOTE not in normalized:
            raise RuntimeError(f"unexpected target origin: {remote}")


def apply_release(stage: Path, target: Path) -> None:
    for relative in (*MANAGED_PATHS, *LEGACY_PATHS):
        destination = target / relative
        if destination.exists() or destination.is_symlink():
            remove_path(destination)
    for relative in MANAGED_PATHS:
        copy_path(stage / relative, target / relative)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synchronize the standalone qifu-drawer-form release repository."
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=ROOT.parent / "qifu-drawer-form",
        help="clean checkout of jingjingtu/qifu-drawer-form",
    )
    parser.add_argument(
        "--allow-any-target",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = args.target.expanduser().resolve()
    try:
        ensure_clean_source()
        preflight_target(target, args.allow_any_target)
        source_commit = run("git", "rev-parse", "HEAD", cwd=ROOT).stdout.strip()
        with tempfile.TemporaryDirectory(prefix="qifu-drawer-release-") as temp:
            stage = Path(temp) / "release"
            build_release(stage, source_commit)
            validate_stage(stage)
            apply_release(stage, target)
        validate_stage(target)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    status = run("git", "status", "--short", cwd=target).stdout
    print(f"Synchronized standalone release to {target}")
    if status:
        print(status, end="")
    else:
        print("No release changes detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
