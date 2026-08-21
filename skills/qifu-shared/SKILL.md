---
name: qifu-shared
description: Qifu 页面生成 Skill 的共享依赖包。提供 qifu-list-page、qifu-detail-page、qifu-drawer-form 所需的共享组件映射（component-map）与毓数平台导航基线（platform-yushu）。安装任一 Qifu 页面 Skill 时都需一并安装，不要单独作为页面生成工作流使用。
---

# Qifu Shared References

This package is a shared dependency, not a standalone page-generation workflow.

## Required companion skills

- `qifu-list-page`
- `qifu-detail-page`
- `qifu-drawer-form`

Keep this Skill installed beside those companion Skills. They resolve the component map and Yushu navigation baseline from `../qifu-shared/references/`.

## Contents

- `references/component-map.md`: component names, node IDs, published keys, properties, and known gaps.
- `references/platform-yushu.md`: Yushu navigation baseline.
- `references/platform-generic.md`: generic B-end platform adapter (used when `platform=unknown`).
- `theme/`: Figma variable snapshot (`tokens.json` + `source/*.json` + `*.less`). AI reads `tokens.json` first, then `source/<collection>.json` when it needs to verify modes and values.
