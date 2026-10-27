#!/usr/bin/env python3
"""Rebuild the qifu-detail-page Codex plugin payload from canonical skills/.

The plugin under ``plugins/qifu-detail-page`` bundles the detail-page skill and
its hard dependency ``qifu-shared`` so the plugin is self-contained. Content is
never edited inside ``plugins/`` directly; run this script after changing
``skills/qifu-detail-page`` or ``skills/qifu-shared``:

    python3 scripts/build_detail_plugin.py [--check]

``--check`` verifies the plugin payload matches the canonical skills without
writing anything (used by CI to detect drift).
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins" / "qifu-detail-page"
SKILLS_DIR = PLUGIN_DIR / "skills"
BUNDLED_SKILLS = ("qifu-detail-page", "qifu-shared")
MANIFEST = PLUGIN_DIR / ".codex-plugin" / "plugin.json"
SKIP_NAMES = {".DS_Store", "__pycache__", ".pytest_cache"}


def iter_files(source: Path):
    for path in sorted(source.rglob("*")):
        if path.is_file() and path.name not in SKIP_NAMES:
            yield path


def sync_skill(skill: str, check_only: bool, problems: list[str]) -> None:
    source = ROOT / "skills" / skill
    target = SKILLS_DIR / skill
    if not source.is_dir():
        problems.append(f"missing canonical skill: {source}")
        return
    if check_only:
        source_files = {p.relative_to(source) for p in iter_files(source)}
        target_files = (
            {p.relative_to(target) for p in iter_files(target)}
            if target.is_dir()
            else set()
        )
        if source_files != target_files:
            problems.append(f"{skill}: file sets differ ({source_files ^ target_files})")
            return
        for rel in source_files:
            if not filecmp.cmp(source / rel, target / rel, shallow=False):
                problems.append(f"{skill}: content drift at {rel}")
        return
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    for path in iter_files(source):
        destination = target / path.relative_to(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    print(f"Synced {skill} -> {target.relative_to(ROOT)}")


def read_version(skill: str) -> str:
    version_file = ROOT / "skills" / skill / "VERSION"
    return version_file.read_text(encoding="utf-8").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify only, no writes")
    args = parser.parse_args()

    problems: list[str] = []
    if not MANIFEST.is_file():
        problems.append(f"missing plugin manifest: {MANIFEST}")

    for skill in BUNDLED_SKILLS:
        sync_skill(skill, args.check, problems)

    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        print(
            "Plugin payload is out of sync. Run: python3 scripts/build_detail_plugin.py",
            file=sys.stderr,
        )
        return 1

    if not args.check:
        manifest_version = read_version("qifu-detail-page")
        print(f"Plugin payload rebuilt (skill version {manifest_version}).")
    else:
        print("Plugin payload matches canonical skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
