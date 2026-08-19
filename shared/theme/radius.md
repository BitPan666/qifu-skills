# Radius Tokens

## 1. 调用原则

圆角是组件视觉契约的一部分。当前 Qifu 组件注册表尚未导出完整 Radius Variable 数值，因此 AI 必须优先复用真实实例，不手工修改实例圆角。

| Token | 预期用途 | 状态 | AI 行为 |
|---|---|---|---|
| `radius.control` | Input、Select、Button 等控件 | variable-required | 调用组件实例 |
| `radius.surface` | Card、Page Surface、Table 容器 | variable-required | 调用模板/容器实例 |
| `radius.overlay` | Drawer、Dialog、Popup | variable-required | 调用 Overlay 实例 |
| `radius.tag` | Tag、Badge | variable-required | 调用 Tag/Badge 实例 |
| `radius.round` | Avatar、圆形 Icon Button | variable-required | 调用组件实例 |

## 2. 禁止事项

- 不将 TDesign 的 `2 / 3 / 6 / 9 / 12px` 直接作为 Qifu 圆角；
- 不因截图相似性对组件实例强写 Radius；
- 不在同一页面中混用近似但不一致的圆角；
- 新建 Fallback 时，优先使用相邻同层级正式实例的可见圆角，并记录为审计项。
