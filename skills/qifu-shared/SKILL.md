---
name: qifu-shared
description: Internal dependency skill for Qifu page-generation skills. Provides the shared component map and Yushu navigation baseline required by qifu-list-page, qifu-detail-page, and qifu-drawer-form. Install it whenever any Qifu page skill is installed.
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
