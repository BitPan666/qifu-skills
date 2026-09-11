---
name: qifu-shared
description: Qifu 页面生成 Skill 的共享依赖包。提供 qifu-list-page、qifu-detail-page、qifu-drawer-form 所需的共享组件映射、毓数平台基线、智客星平台基线、通用平台适配器与主题变量。安装任一 Qifu 页面 Skill 时都需一并安装，不要单独作为页面生成工作流使用。Used by: qifu-list-page、qifu-detail-page、qifu-drawer-form。Not for: 单独页面生成、详情业务内容。
---

# Qifu Shared References

共享依赖包，不是独立页面生成工作流。

## Required companion skills

- `qifu-list-page`
- `qifu-detail-page`
- `qifu-drawer-form`

Keep this Skill installed beside those companion Skills. They resolve shared component maps, platform baselines, and theme variables from `../qifu-shared/`.

## Contents

- `references/component-map.md`: 组件名称、节点 ID、发布键、属性与已知缺口（仓库唯一权威；2026-09-11 起 `qifu-list-page` 不再保留副本）
- `references/platform-yushu.md`: 毓数导航基线。
- `references/platform-zhikexing.md`: 智客星列表页基线与 copyTemplate 策略（仓库唯一权威；2026-09-11 起 `qifu-list-page` 不再保留副本）。
- `references/platform-generic.md`: 通用 B 端平台适配器（`platform=unknown` 时使用）。
- `theme/`: Figma 变量快照（`tokens.json` + `source/*.json` + `*.less`）。AI 先读 `tokens.json`，需要核对模式和值时读 `source/<collection>.json`。

## 版本

- 当前版本：`VERSION` 字段（2026-09-11 起新建）。
- `qifu-list-page` `references/component-map.md` 与 `references/platform-zhikexing.md` 已删除；任何页面 Skill 的文档契约不再单独维护这两份文件，校验脚本 `scripts/validate_skill_contract.py` 直接读 `../qifu-shared/references/`。
