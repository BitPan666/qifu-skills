#!/usr/bin/env python3
"""Validate every Qifu skill and the repository-level contracts."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOCAL_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata"}
NON_WORKFLOW_SKILLS = {"qifu-shared", "zhikexing-list-page"}
# release/ and plugins/ are generated payloads (standalone export, Codex plugin
# bundle) rebuilt from canonical skills/ by sync scripts; validate originals only.
SKIP_PARTS = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache", "release", "plugins", ".agents"}


def should_skip(path: Path) -> bool:
    return bool(SKIP_PARTS.intersection(path.parts))


def load_yaml(path: Path, errors: list[str]) -> object | None:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
        return None


def validate_skill(skill_dir: Path, errors: list[str], warnings: list[str]) -> None:
    skill_file = skill_dir / "SKILL.md"
    version_file = skill_dir / "VERSION"
    agent_file = skill_dir / "agents" / "openai.yaml"

    if not skill_file.is_file():
        errors.append(f"{skill_dir.relative_to(ROOT)}: missing SKILL.md")
        return

    text = skill_file.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not match:
        errors.append(f"{skill_file.relative_to(ROOT)}: missing YAML frontmatter")
        return

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        errors.append(f"{skill_file.relative_to(ROOT)}: invalid frontmatter: {exc}")
        return

    if not isinstance(frontmatter, dict):
        errors.append(f"{skill_file.relative_to(ROOT)}: frontmatter must be an object")
        return

    unexpected = set(frontmatter) - ALLOWED_FRONTMATTER
    if unexpected:
        errors.append(
            f"{skill_file.relative_to(ROOT)}: unsupported frontmatter keys: "
            + ", ".join(sorted(unexpected))
        )

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if name != skill_dir.name or not isinstance(name, str) or not SKILL_NAME.fullmatch(name):
        errors.append(f"{skill_file.relative_to(ROOT)}: name must equal folder name")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{skill_file.relative_to(ROOT)}: description must be non-empty text")
    elif len(description) > 200:
        warnings.append(
            f"{skill_file.relative_to(ROOT)}: description exceeds 200 characters; keep discovery metadata concise"
        )

    if not version_file.is_file():
        errors.append(f"{skill_dir.relative_to(ROOT)}: missing VERSION")
    else:
        version = version_file.read_text(encoding="utf-8").strip()
        if not SEMVER.fullmatch(version):
            errors.append(f"{version_file.relative_to(ROOT)}: expected non-empty SemVer")

    agent = load_yaml(agent_file, errors) if agent_file.is_file() else None
    if not isinstance(agent, dict) or not isinstance(agent.get("interface"), dict):
        errors.append(f"{agent_file.relative_to(ROOT)}: missing interface metadata")
    else:
        interface = agent["interface"]
        display_name = interface.get("display_name")
        short_description = interface.get("short_description")
        default_prompt = interface.get("default_prompt")
        if not isinstance(display_name, str) or not display_name.strip():
            errors.append(f"{agent_file.relative_to(ROOT)}: display_name must be non-empty text")
        if not isinstance(short_description, str) or not 25 <= len(short_description) <= 64:
            errors.append(
                f"{agent_file.relative_to(ROOT)}: short_description must be 25-64 characters"
            )
        if not isinstance(default_prompt, str) or f"${name}" not in default_prompt:
            errors.append(
                f"{agent_file.relative_to(ROOT)}: default_prompt must mention ${name}"
            )
        implicit = agent.get("policy", {}).get("allow_implicit_invocation")
        if implicit is not None and not isinstance(implicit, bool):
            errors.append(
                f"{agent_file.relative_to(ROOT)}: allow_implicit_invocation must be boolean"
            )
        if name in NON_WORKFLOW_SKILLS:
            if implicit is not False:
                errors.append(
                    f"{agent_file.relative_to(ROOT)}: dependency/archive entry must disable implicit invocation"
                )

    if len(text.encode("utf-8")) > 30_000:
        warnings.append(
            f"{skill_file.relative_to(ROOT)}: entrypoint exceeds 30 KB; move conditional detail to references"
        )


def validate_links(errors: list[str]) -> None:
    for markdown in ROOT.rglob("*.md"):
        if should_skip(markdown):
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in LOCAL_LINK.findall(text):
            target = raw_target.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_text = unquote(target.split("#", 1)[0])
            if not path_text:
                continue
            resolved = (markdown.parent / path_text).resolve()
            if not resolved.exists():
                errors.append(
                    f"{markdown.relative_to(ROOT)}: broken local link: {raw_target}"
                )


def validate_json(errors: list[str]) -> None:
    for path in ROOT.rglob("*.json"):
        if should_skip(path):
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")


def validate_yaml(errors: list[str]) -> None:
    for pattern in ("*.yaml", "*.yml"):
        for path in ROOT.rglob(pattern):
            if should_skip(path):
                continue
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError) as exc:
                errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")


def validate_repository_contract(errors: list[str]) -> None:
    required = (
        SKILLS / "qifu-shared" / "references" / "component-map.md",
        SKILLS / "qifu-shared" / "references" / "component-invocation-baseline.md",
        SKILLS / "qifu-shared" / "references" / "page-context.md",
        SKILLS / "qifu-shared" / "references" / "platform-yushu.md",
    )
    for path in required:
        if not path.is_file():
            errors.append(f"missing canonical reference: {path.relative_to(ROOT)}")

    duplicate_yushu = [
        path
        for path in ROOT.rglob("platform-yushu.md")
        if not should_skip(path)
        and path != SKILLS / "qifu-shared" / "references" / "platform-yushu.md"
    ]
    if duplicate_yushu:
        errors.append(
            "platform-yushu.md must have one canonical source; duplicates: "
            + ", ".join(str(path.relative_to(ROOT)) for path in duplicate_yushu)
        )

    drawer_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (SKILLS / "qifu-drawer-form").rglob("*.md")
    )
    if re.search(r"(?:默认宽度|默认档|默认控件宽度)[^\n]*\b320(?:px)?\b", drawer_text):
        errors.append("qifu-drawer-form: deprecated default control width 320 remains")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())

    for skill_dir in skill_dirs:
        validate_skill(skill_dir, errors, warnings)
    validate_links(errors)
    validate_json(errors)
    validate_yaml(errors)
    validate_repository_contract(errors)

    selector_validator = (
        SKILLS
        / "qifu-drawer-form"
        / "scripts"
        / "validate_selector_suffix_contract.py"
    )
    result = subprocess.run(
        [sys.executable, str(selector_validator)],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode:
        errors.append(
            "qifu-drawer-form: selector suffix contract validation failed: "
            + result.stdout.strip()
        )

    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {len(skill_dirs)} skill packages validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
