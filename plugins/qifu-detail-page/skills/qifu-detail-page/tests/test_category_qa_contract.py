import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CategoryQaContractTest(unittest.TestCase):
    def test_existing_compositions_remain_registered(self):
        text = (ROOT / "references/detail-compositions.md").read_text()
        for name in ("Flat", "Tabbed", "Master Detail", "Readonly"):
            self.assertIn(f"Qifu Detail Page / {name}", text)

    def test_category_qa_is_zhikexing_only(self):
        skill = (ROOT / "SKILL.md").read_text()
        composition = (ROOT / "references/detail-compositions.md").read_text()
        rules = (ROOT / "references/category-qa-zhikexing.md").read_text()
        self.assertIn("Qifu Detail Page / Category Q&A", composition)
        self.assertIn("platform=zhikexing", rules)
        self.assertIn("其他详情组合仍返回 `UNSUPPORTED_PLATFORM`", skill)
        self.assertIn("BLOCKED_COMPONENT_GAP", rules)

    def test_no_record_header_or_fake_controls_in_category_qa(self):
        rules = (ROOT / "references/category-qa-zhikexing.md").read_text()
        self.assertIn("不把列表 Filter Bar、Table 或 PageHead", rules)
        self.assertIn("Collapse / Panel", rules)
        self.assertIn("不能分离实例或手绘折叠控件", rules)
        self.assertIn("本地 Text Style", rules)

    def test_category_qa_preserves_three_navigation_layers_and_two_level_qa(self):
        rules = (ROOT / "references/category-qa-zhikexing.md").read_text()
        for required in (
            "三层导航",
            "团队辅助 > 团队审核",
            "短线居中",
            "约 200px 类目栏",
            "弹性 Spacer",
            "分组 > 问题 > 回答",
            "两个后续分组收起",
            "仅问答内容区域滚动",
            "只使用**单列二级菜单**",
            "不得生成两列二级菜单",
        ):
            self.assertIn(required, rules)

    def test_category_qa_keeps_platform_gate_narrow(self):
        rules = (ROOT / "references/category-qa-zhikexing.md").read_text()
        self.assertIn("不得解析或保留 yushu、毓数、鲸数或 QBI", rules)
        self.assertIn("Navigation / HeaderMenu / 智客星 Header", rules)
        self.assertIn("没有新增 Text Style", rules)

    def test_category_search_resizes_only_at_the_outer_instance(self):
        rules = (ROOT / "references/category-qa-zhikexing.md").read_text()
        for required in (
            "最外层真实实例",
            "搜索实例固定为 `168 × 32`",
            "`FIXED`",
            "需要响应式类目栏时可改为 `FILL`",
            "不得修改母组件、分离实例、改变嵌套 `Input` 的尺寸",
        ):
            self.assertIn(required, rules)

    def test_category_qa_keeps_collapse_geometry_and_per_edge_borders(self):
        rules = (ROOT / "references/category-qa-zhikexing.md").read_text()
        for required in (
            "分组标题容器和 Group Collapse 实例高 `46px`",
            "展开问题的 Collapse 实例高 `48px`",
            "回答行高 `48px`",
            "四边 `1px` 描边",
            "只保留底边 `1px`",
            "上、右、左边均为 `0px`",
            "mode/green/--qifu-gray-color-4%",
        ):
            self.assertIn(required, rules)

    def test_team_audit_sidebar_state_and_icon_tokens_are_scoped(self):
        rules = (ROOT / "references/category-qa-zhikexing.md").read_text()
        for required in (
            "团队审核 / 模型话术",
            "客户添加",
            "State=Default",
            "expanded=false",
            "visible=false",
            "团队辅助",
            "State=Selected",
            "expanded=true",
            "图标颜色/--qifu-icon-color-brand",
            "mode/green/--qifu-gray-color-65%",
            "纵向 Auto Layout",
        ):
            self.assertIn(required, rules)

    def test_golden_sample_geometry_is_the_regeneration_baseline(self):
        rules = (ROOT / "references/category-qa-zhikexing.md").read_text()
        for required in (
            "Golden Sample / 智客星 / 团队审核 / 模型话术 / 1366 / v1",
            "Figma 节点 `5540:70719`",
            "全局 Header 为 `1366 × 48`",
            "`1166 × 32`",
            "`1134 × 614`",
            "类目栏宽 `200`",
            "搜索实例为 `168 × 32`",
            "筛选行固定 `886 × 32`",
            "问题搜索为 `304 × 32`",
            "固定 `886 × 536`",
            "分组标题容器和 Group Collapse 实例高 `46px`",
            "展开问题的 Collapse 实例高 `48px`",
        ):
            self.assertIn(required, rules)


if __name__ == "__main__":
    unittest.main()
