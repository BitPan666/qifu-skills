# Typography Tokens

## 1. 字体调用原则

- 优先继承 Figma 文本样式或组件实例中的文本样式；
- 使用语义层级（`page-title`、`body`、`caption`），不以“我想要 15px”作为第一选择；
- 中文、英文、数字和状态标签在同一表格/详情块中保持同一文本层级；
- 组件未暴露字体属性时不得分离实例改字重或字号。

## 2. 文本层级

| Token | 用途 | 已确认规格 | 状态 |
|---|---|---|---|
| `font.page-title` | 列表/详情页面标题 | 16px | confirmed |
| `font.filter-label.compact` | 28px 筛选控件的标题 | 12px，`#565656` | confirmed |
| `font.filter-label.default` | 32px 筛选控件的标题 | 14px，`#565656` | confirmed |
| `font.table.body.default` | 表格正文 | 14px（Text-V2 的 `contentFont=14px`） | confirmed |
| `font.table.body.compact` | 紧凑表格正文 | 12px（Text-V2 的 `contentFont=12px`） | confirmed |
| `font.section-title` | 分区标题 | 使用 Figma text style | variable-required |
| `font.detail-label` | 详情字段名 | 使用 Figma text style | variable-required |
| `font.detail-value` | 详情字段值 | 使用 Figma text style | variable-required |
| `font.caption` | 辅助说明/次级信息 | 使用 Figma text style | variable-required |

## 3. 页面调用规则

- List Page 的 PageHeader 标题为 `font.page-title`；关闭 PageHeader 时不留下空标题占位；
- 表格同一列不混用 12px 与 14px；仅紧凑数据密度使用 `font.table.body.compact`；
- 筛选项标题由 `Filter Item-V2` 管理：28px → 12px，32px → 14px；
- 表格状态、操作文字优先使用其正式 `Tag` / `Action Content` / `Button` 实例中的文字样式；
- 数字、金额、日期的对齐是数据 Pattern 规则，不能仅靠改变字号解决。

## 4. 待盘点项

需从 Figma Variables / Text Styles 补齐：字体族、字重、行高、标题/正文/说明的完整层级，以及中文/英文/等宽数字的回退策略。
