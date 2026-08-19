# Qifu B 端 Design System

这是面向公司全体 B 端产品的 AI 组件调用与页面抽象 Skill。它借鉴 `Tencent/tdesign-common` 的组织思路：

- 共享层与平台/端解耦；
- 组件以稳定的语义名称和索引统一发现；
- 页面能力以 Archetype / Pattern 复用，而不是复制具体业务页面；
- 文档、API/契约、组件映射和 AI 调用入口并列维护。

当前 Figma 组件源为 `奇富科技中后台组件库 新`。本 Skill 与现有 `qifu-list-page`、`qifu-detail-page`、`qifu-drawer-form` 配套使用：本 Skill 负责公司级抽象、页面类型选择、跨平台迁移与治理，具体 Archetype Skill 负责落图。

## 目录

```text
qifu-b-end-design-system/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── architecture.md
    ├── component-contract.md
    ├── page-archetypes.md
    └── platform-adapter.md
```

## 预览

![系统架构](../../screenshots/overview/architecture.svg)

![AI 调用流程](../../screenshots/overview/ai-call-flow.svg)

![平台迁移矩阵](../../screenshots/overview/platform-migration.svg)
