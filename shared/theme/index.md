# Theme Index

## 1. 主题包元信息

| 字段 | 值 |
|---|---|
| Token source | `奇富科技中后台组件库 新` |
| Figma file key | `gTV3VdC6a5e9vpkRHIZSXA` |
| 默认模式 | Light / 企业 Web 后台 |
| Dark mode | 结构预留，等待 Figma Variables 或 Dark 组件实例盘点 |
| 状态 | `partial-verified`：仅下表“已确认”项可直接由 AI 使用 |
| 最后盘点 | 2026-08-19 |

## 2. Token 状态标记

| 标记 | 含义 | AI 行为 |
|---|---|---|
| `confirmed` | 已从组件实例、现有 page blueprint 或 component map 验证 | 可直接使用 |
| `variable-required` | 应由 Figma Variable / 组件属性提供，但尚未导出具体值 | 绑定变量或复用实例，不手填色值 |
| `reserved` | 目录与命名已建立，但组件库还未盘点 | 不得虚构数值；记录审计项 |
| `deprecated` | 不再用于新页面 | 不使用，仅为历史页面兼容 |

## 3. AI 查询顺序

1. 根据意图进入 `color.md`、`typography.md`、`size.md`、`radius.md` 或 `shadow.md`；
2. 确认 Token 的状态；
3. 需要真实 Figma 值时，优先保留/复用组件实例的变量绑定；
4. 未暴露变量时，读取对应页面 Pattern 的 blueprint；
5. 仍无正式能力时，创建最小 `Fallback / <Capability>` 并写入 `Audit / Missing Components`。

## 4. 主题切换规则

- 目前只交付 `Light` 页面，除非用户明确提供 Dark 组件或变量；
- 不通过反色、降低不透明度或复制 TDesign dark token 来“猜测”深色主题；
- Theme mode 必须由页面根级或系统级变量统一控制，不允许单个组件自行切换；
- 同一个交付页面不能混用 Light 与 Dark 表面、边框和文本语义。
