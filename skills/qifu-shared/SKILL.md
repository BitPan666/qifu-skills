---
name: qifu-shared
description: Qifu 页面生成 Skill 的共享依赖包。提供 qifu-list-page、qifu-detail-page、qifu-drawer-form 所需的共享组件映射、毓数平台基线、智客星平台基线、通用平台适配器与主题变量。安装任一 Qifu 页面 Skill 时都需一并安装，不要单独作为页面生成工作流使用。
---

# Qifu Shared References

This package is a shared dependency, not a standalone page-generation workflow.

## Required companion skills

- `qifu-list-page`
- `qifu-detail-page`
- `qifu-drawer-form`

Keep this Skill installed beside those companion Skills. They resolve shared component maps, platform baselines, and theme variables from `../qifu-shared/`.

## Contents

- `references/component-map.md`: component names, node IDs, published keys, properties, and known gaps.
- `references/platform-yushu.md`: Yushu navigation baseline.
- `references/platform-zhikexing.md`: Zhikexing list-page baseline and copyTemplate strategy.
- `references/platform-generic.md`: generic B-end platform adapter (used when `platform=unknown`).
- `theme/`: Figma variable snapshot (`tokens.json` + `source/*.json` + `*.less`). AI reads `tokens.json` first, then `source/<collection>.json` when it needs to verify modes and values.
