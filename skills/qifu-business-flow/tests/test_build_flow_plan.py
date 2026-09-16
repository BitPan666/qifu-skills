from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "build_flow_plan.py"
FIXTURE = SKILL_ROOT / "tests" / "fixtures" / "valid-flow.yaml"
TASK_FIXTURE = SKILL_ROOT / "tests" / "fixtures" / "task-management-flow.yaml"

spec = importlib.util.spec_from_file_location("build_flow_plan", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class BusinessFlowPlanTest(unittest.TestCase):
    def load_fixture(self) -> dict:
        return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))

    def test_valid_model_builds_page_and_transient_states(self) -> None:
        model = module.load_model(FIXTURE)
        plan = module.build_flow_plan(model, FIXTURE, REPO_ROOT / "skills")

        self.assertEqual([state["key"] for state in plan["states"]], ["list", "createDrawer"])
        self.assertEqual(plan["transientStates"], ["moreMenu"])
        self.assertEqual(
            plan["prototypeRoutes"],
            ["list-create", "create-dismiss", "create-success"],
        )
        dismiss = next(route for route in plan["routes"] if route["id"] == "create-dismiss")
        self.assertEqual(dismiss["actions"], ["cancel", "close"])

    def test_unknown_field_reference_is_rejected(self) -> None:
        model = self.load_fixture()
        model["views"]["list"]["fields"].append("missingField")
        with self.assertRaisesRegex(module.BusinessFlowError, "unknown field"):
            module.validate_model(model)

    def test_unknown_source_action_is_rejected(self) -> None:
        model = self.load_fixture()
        model["transitions"][0]["action"] = "delete"
        with self.assertRaisesRegex(module.BusinessFlowError, "unknown source actions"):
            module.validate_model(model)

    def test_explicit_missing_skill_remains_pending(self) -> None:
        model = self.load_fixture()
        model["views"]["createDrawer"]["skill"] = "qifu-missing-drawer"
        module.validate_model(model)
        plan = module.build_flow_plan(model, FIXTURE, REPO_ROOT / "skills")
        self.assertEqual(
            plan["pendingSkills"],
            [{"view": "createDrawer", "skill": "qifu-missing-drawer"}],
        )

    def test_cli_writes_flow_plan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "plan.yaml"
            result = module.main([str(FIXTURE), "--output", str(output)])
            self.assertEqual(result, 0)
            plan = yaml.safe_load(output.read_text(encoding="utf-8"))
            self.assertEqual(plan["flow"]["id"], "order-management")

    def test_task_management_training_model_keeps_six_confirmed_routes(self) -> None:
        model = module.load_model(TASK_FIXTURE)
        plan = module.build_flow_plan(model, TASK_FIXTURE, REPO_ROOT / "skills")

        self.assertEqual(model["platform"]["key"], "zhikexing")
        self.assertEqual(
            plan["prototypeRoutes"],
            [
                "list-create",
                "create-dismiss",
                "create-success",
                "list-more",
                "list-data",
                "data-close",
            ],
        )
        self.assertNotIn("list-detail", plan["prototypeRoutes"])
        self.assertIn(
            {"view": "taskDataDrawer", "skill": "qifu-detail-drawer"},
            plan["pendingSkills"],
        )
        self.assertIn(
            {"view": "taskDetail", "reason": "model-target-status"},
            plan["pendingViews"],
        )


if __name__ == "__main__":
    unittest.main()
