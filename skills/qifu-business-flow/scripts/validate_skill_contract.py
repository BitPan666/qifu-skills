#!/usr/bin/env python3
"""Validate the qifu-business-flow package contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


REQUIRED_FILES = (
    "SKILL.md",
    "VERSION",
    "agents/openai.yaml",
    "references/business-flow-spec.md",
    "references/orchestration.md",
    "references/validation.md",
    "scripts/build_flow_plan.py",
)
REQUIRED_PHRASES = {
    "SKILL.md": (
        "BusinessFlowSpec",
        "reuse-first",
        "confirmed-only",
        "PENDING_PAGE_SKILL",
        "PROTOTYPE_TARGET_MISSING",
        "不把业务字段复制进本通用 Skill",
    ),
    "references/business-flow-spec.md": (
        "confirmed | recommended | TBD",
        "transitions.from",
        "瞬时状态",
    ),
    "references/orchestration.md": (
        "qifu-list-page",
        "qifu-drawer-form",
        "qifu-detail-page",
        "Prototype",
        "pending-skill",
    ),
    "references/validation.md": (
        "FIELD_CONSISTENCY",
        "PROTOTYPE_CHECK",
        "VISUAL_CHECK",
        "GOLDEN_SAMPLE_UPDATED",
    ),
}


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    texts: dict[str, str] = {}
    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")
            continue
        texts[relative] = path.read_text(encoding="utf-8")

    skill = texts.get("SKILL.md", "")
    if not re.match(r"^---\n.*?^name:\s*qifu-business-flow\s*$.*?^---$", skill, re.M | re.S):
        errors.append("SKILL.md: invalid frontmatter or name")

    version = texts.get("VERSION", "").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("VERSION: expected SemVer")

    agent_path = root / "agents" / "openai.yaml"
    if agent_path.is_file():
        try:
            agent = yaml.safe_load(agent_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"agents/openai.yaml: invalid YAML: {exc}")
        else:
            prompt = (agent or {}).get("interface", {}).get("default_prompt", "")
            if "$qifu-business-flow" not in prompt:
                errors.append("agents/openai.yaml: default_prompt must mention $qifu-business-flow")

    for relative, phrases in REQUIRED_PHRASES.items():
        text = texts.get(relative, "")
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{relative}: missing required contract '{phrase}'")
    return errors


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    print(f"PASS qifu-business-flow {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
