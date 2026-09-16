#!/usr/bin/env python3
"""Validate a BusinessFlowSpec and derive a deterministic FlowPlan."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


SOURCE_STATUSES = {"confirmed", "recommended", "TBD"}
DEFAULT_SKILLS = {
    "list": "qifu-list-page",
    "drawer": "qifu-drawer-form",
    "page": "qifu-detail-page",
}
SHELL_ACTIONS = {"close"}


class BusinessFlowError(ValueError):
    """Raised when the BusinessFlowSpec violates the contract."""


def _require_mapping(value: Any, location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise BusinessFlowError(f"{location} must be an object")
    return value


def _require_list(value: Any, location: str) -> list[Any]:
    if not isinstance(value, list):
        raise BusinessFlowError(f"{location} must be a list")
    return value


def _unique_items(items: list[Any], location: str, key_name: str = "key") -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(items):
        item = _require_mapping(raw, f"{location}[{index}]")
        key = item.get(key_name)
        if not isinstance(key, str) or not key:
            raise BusinessFlowError(f"{location}[{index}].{key_name} must be non-empty text")
        if key in result:
            raise BusinessFlowError(f"{location}: duplicate {key_name} '{key}'")
        result[key] = item
    return result


def _check_source_status(item: dict[str, Any], location: str) -> None:
    status = item.get("sourceStatus")
    if status not in SOURCE_STATUSES:
        raise BusinessFlowError(
            f"{location}.sourceStatus must be confirmed, recommended, or TBD"
        )


def validate_model(model: dict[str, Any]) -> None:
    for key in ("schemaVersion", "flow", "platform", "entity", "fields", "views", "transitions"):
        if key not in model:
            raise BusinessFlowError(f"missing root key: {key}")

    if not isinstance(model["schemaVersion"], str):
        raise BusinessFlowError("schemaVersion must be text")
    _require_mapping(model["flow"], "flow")
    platform = _require_mapping(model["platform"], "platform")
    entity = _require_mapping(model["entity"], "entity")
    _check_source_status(platform, "platform")

    fields = _unique_items(_require_list(model["fields"], "fields"), "fields")
    for key, field in fields.items():
        _check_source_status(field, f"fields.{key}")

    for pointer in ("idField", "titleField", "statusField"):
        field_key = entity.get(pointer)
        if field_key is not None and field_key not in fields:
            raise BusinessFlowError(f"entity.{pointer} references unknown field '{field_key}'")

    views = _require_mapping(model["views"], "views")
    if not views:
        raise BusinessFlowError("views must not be empty")

    view_actions: dict[str, set[str]] = {}
    for view_key, raw_view in views.items():
        view = _require_mapping(raw_view, f"views.{view_key}")
        view_type = view.get("type")
        if view_type not in DEFAULT_SKILLS:
            raise BusinessFlowError(f"views.{view_key}.type is unsupported: {view_type!r}")

        references: list[tuple[str, Any]] = [("fields", view.get("fields", []))]
        for index, section in enumerate(view.get("sections", [])):
            section_map = _require_mapping(section, f"views.{view_key}.sections[{index}]")
            references.append((f"sections[{index}].fields", section_map.get("fields", [])))
        data_table = view.get("dataTable", {})
        if data_table:
            data_table = _require_mapping(data_table, f"views.{view_key}.dataTable")
            references.append(("dataTable.columns", data_table.get("columns", [])))

        for suffix, raw_refs in references:
            for field_key in _require_list(raw_refs, f"views.{view_key}.{suffix}"):
                if field_key not in fields:
                    raise BusinessFlowError(
                        f"views.{view_key}.{suffix} references unknown field '{field_key}'"
                    )

        actions = _unique_items(
            _require_list(view.get("actions", []), f"views.{view_key}.actions"),
            f"views.{view_key}.actions",
        )
        for action_key, action in actions.items():
            _check_source_status(action, f"views.{view_key}.actions.{action_key}")
        view_actions[view_key] = set(actions)

        view_status = view.get("sourceStatus")
        if view_status is not None and view_status not in SOURCE_STATUSES:
            raise BusinessFlowError(f"views.{view_key}.sourceStatus is invalid")

    transitions = _unique_items(
        _require_list(model["transitions"], "transitions"),
        "transitions",
        key_name="id",
    )
    for transition_id, transition in transitions.items():
        location = f"transitions.{transition_id}"
        _check_source_status(transition, location)
        source = transition.get("from")
        target = transition.get("to")
        if source not in views:
            raise BusinessFlowError(f"{location}.from references unknown view '{source}'")
        if not isinstance(target, str) or not target:
            raise BusinessFlowError(f"{location}.to must be non-empty text")

        has_action = "action" in transition
        has_actions = "actions" in transition
        if has_action == has_actions:
            raise BusinessFlowError(f"{location} must define exactly one of action or actions")
        actions = transition.get("actions", [transition.get("action")])
        if not isinstance(actions, list) or not actions or not all(isinstance(a, str) and a for a in actions):
            raise BusinessFlowError(f"{location} actions must be non-empty text values")
        unknown_actions = set(actions) - view_actions[source] - SHELL_ACTIONS
        if unknown_actions:
            raise BusinessFlowError(
                f"{location} references unknown source actions: {', '.join(sorted(unknown_actions))}"
            )

        if target not in views and transition.get("presentation") != "overlayMenu":
            if transition.get("targetStatus") != "pending-skill" and transition.get("sourceStatus") != "TBD":
                raise BusinessFlowError(
                    f"{location}.to references unknown view '{target}' without pending/TBD status"
                )


def load_model(path: Path) -> dict[str, Any]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise BusinessFlowError(f"cannot read YAML: {exc}") from exc
    model = _require_mapping(raw, "root")
    validate_model(model)
    return model


def build_flow_plan(
    model: dict[str, Any], source_path: Path, skills_root: Path
) -> dict[str, Any]:
    views = model["views"]
    states: list[dict[str, Any]] = []
    pending_skills: list[dict[str, str]] = []
    pending_views: list[dict[str, str]] = []
    for view_key, view in views.items():
        skill = view.get("skill") or DEFAULT_SKILLS[view["type"]]
        available = (skills_root / skill).is_dir()
        target_status = view.get("targetStatus")
        status = "available"
        if not available or target_status == "pending-skill":
            status = "pending-skill"
        states.append(
            {
                "key": view_key,
                "type": view["type"],
                "title": view.get("title"),
                "fields": list(view.get("fields", [])),
                "implementationSkill": skill,
                "skillAvailability": "available" if available else "missing",
                "implementationStatus": status,
                "targetStatus": target_status,
                "sourceStatus": view.get("sourceStatus", "confirmed"),
            }
        )
        if not available:
            pending_skills.append({"view": view_key, "skill": skill})
        if target_status == "pending-skill":
            pending_views.append({"view": view_key, "reason": "model-target-status"})

    routes: list[dict[str, Any]] = []
    transient_states: list[str] = []
    for transition in model["transitions"]:
        actions = list(transition.get("actions", [transition.get("action")]))
        target = transition["to"]
        if target not in views and target not in transient_states:
            transient_states.append(target)
        routes.append(
            {
                "id": transition["id"],
                "from": transition["from"],
                "actions": actions,
                "to": target,
                "presentation": transition.get("presentation"),
                "effect": transition.get("effect"),
                "sourceStatus": transition["sourceStatus"],
                "prototypeEligible": transition["sourceStatus"] == "confirmed",
                "targetStatus": transition.get("targetStatus"),
            }
        )

    return {
        "schemaVersion": "1.0",
        "source": {"businessModelPath": str(source_path)},
        "flow": model["flow"],
        "platform": model["platform"],
        "navigation": model.get("navigation", {}),
        "states": states,
        "transientStates": transient_states,
        "routes": routes,
        "prototypeRoutes": [route["id"] for route in routes if route["prototypeEligible"]],
        "pendingSkills": pending_skills,
        "pendingViews": pending_views,
        "assumptions": model.get("assumptions", []),
        "tbd": model.get("tbd", []),
    }


def dump_plan(plan: dict[str, Any], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
    return yaml.safe_dump(plan, allow_unicode=True, sort_keys=False)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("business_model", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--format", choices=("yaml", "json"), default="yaml")
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Directory containing installed qifu-* skills",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        model = load_model(args.business_model)
        plan = build_flow_plan(model, args.business_model, args.skills_root)
    except BusinessFlowError as exc:
        print(f"INVALID_BUSINESS_FLOW_SPEC\n- {exc}", file=sys.stderr)
        return 1

    text = dump_plan(plan, args.format)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"PASS: wrote {args.output}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
