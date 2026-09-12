# DetailBlock 内容路由表

## 目的

决定 `DetailSpec.blocks[].bodyType` 使用哪种真实组件或稳定的页面级组合。优先命中本表,本表没有时使用 `Custom(<BizBlock>)` 并记录缺口。

所有真实组件的节点 ID / 发布 Key / 属性,请直接查询[组件映射](../../qifu-shared/references/component-map.md);本表只做"语义 → 区块形态"的路由。

## 通用区块类型

| bodyType | 控件 / 组合 | 适用场景 | 关键属性 |
| --- | --- | --- | --- |
| `Descriptions` | QFDescriptions 或 自定义 Descriptions | 基本信息、配置参数、账号字段 | column 2 或 3,label 宽 120px,align left |
| `Table` | Table Shell-V2 + Header/Row/Content Cell-V2 | 变更记录、关联记录、子对象列表 | `type=basic`、`size=medium`、行数 5–10 |
| `Cards` | 页面级 `Card Grid`(3 列) | 关联客户、子对象快照、快捷入口 | 列数固定 3,卡内仅头像 + 标题 + 副标题 |
| `Timeline` | Timeline 组件 | 操作历史、状态流转、审批流程 | 节点最多 10 条,超出显示"查看全部" |
| `KeyMetrics` | 页面级 `KeyValue Grid`(3 或 4 列) | 关键指标、汇总数据、计数卡 | 数值与标签分别绑定已批准的数字展示 / 正文 Text Style |
| `Empty` | Empty 组件 | 该区块本身无数据 | `status=NoData` + 一句引导 |
| `Custom(<BizBlock>)` | 页面级自定义 + Audit 记录 | 富文本预览、地图、配置 JSON、嵌套子区块 | 仅当现有组件无法表达时使用 |

## 区块类型选择速查

```
是"字段名 → 值" 的扁平集合?                → Descriptions
是"多条记录" 且列固定?                     → Table
是"几个并列的子对象/入口卡片"?              → Cards
是"时间维度的事件史"?                       → Timeline
是"几个关键数字"?                           → KeyMetrics
都没数据但将来会有?                         → Empty
以上试过都不合适?                           → Custom(<BizBlock>) + Audit
```

## 各类型的细节规则

### Descriptions

- 每行 2 或 3 列;**不写 1 列**(除非文档级长描述)和 ≥ 4 列(密度过低)。
- label 宽固定 120px,右对齐,与 value 间距 12px。
- value 类型:
  - 短文本 → 组件库正文 Text Style / `文本颜色/--qifu-text-color-primary`
  - 长文本(URL/Webhook/富文本片段) → 单行 ellipsis + Tooltip 查看
  - 状态 → `Tag` 严格语义映射(同 qifu-list-page):启用=success / 禁用=danger / pending=info
  - 日期 → `YYYY-MM-DD HH:mm` 统一格式
  - ID → 可加 `copy` 图标
- 整组 `Descriptions` 内**不混用** Tag、状态点、纯文本 三种状态表达;选其一(优先 Tag)。

### Table

- 使用 Table Shell-V2,规则沿用 qifu-list-page component-map "Table Shell V2 Slot 替换后的逐层同步"。
- 行数控制在 5–10 行;关联记录条数更多时,用"查看全部"链接而不是无限滚动。
- 行内操作最多 2 个;更多进"更多"菜单。
- 不提供筛选 / 批量(那是列表页);Table 上方只放可选 BlockAction(如"新建子记录")。
- 空数据 → 整块显示 Empty 而不是空表格。

### Cards

- 列数固定 3;每个 Card 高度一致。
- Card 内**只能**有:头像/图标 + 标题 + 副标题 + [可选] 1 个 action。
- Card 不放表格、不放 Descriptions、不放操作组——那是 DetailBlock 的事。
- 子对象需要点击进详情时,整卡可点;不在卡内单独放一个"查看 →"。

### Timeline

- 节点顺序:最新的在最上方。
- 每节点:icon + 时间 + 操作人 + 动作 + [可选]备注。
- 超过 10 条节点 → 显示前 10 条 + "查看全部 N 条"链接。
- 不使用装饰插画,不用大面积色块。

### KeyMetrics

- 列数固定 3 或 4,不并排 2 个也不并排 ≥ 5 个。
- 每个 KeyMetric：value 使用组件库批准的数字展示 Text Style 与 `文本颜色/--qifu-text-color-primary`；label 使用正文 Text Style 与 `文本颜色/--qifu-text-color-secondary`；可选趋势显示 `±x%`。若没有合适的数字展示 Text Style，返回 `STYLE_MISSING`，不手填字号或字重冒充。
- 数字**不做**颜色编码(红色 = 跌、绿色 = 涨),除非业务上有极明确的正负语义。
- 趋势用文字 + ↑↓ 符号,不用 sparkline 图(易视觉杂乱)。

### Empty

- Empty `size=M`,文案说明"该区块当前没有 XXX";原因明确时给一句引导。
- Empty 不放插画;仅使用 Empty 组件的默认样式。
- 一个详情页**最多出现 1 个 Empty Block**——多个空块应合并到一个"暂无关联数据"块。

### Custom(<BizBlock>)

仅在以下情形使用:

- 业务有非标准内容:富文本预览、JSON Schema 编辑器、代码片段、地图、签名图等。
- 先用现有真实组件形成页面级组合，命名 `Custom / <BizBlock>`。
- 无法表达时记录 `COMPONENT_MISSING`。只有 `DetailSpec.fallbackPolicy=allow` 才创建 `Fallback / <BizBlock>`；默认返回 `BLOCKED_COMPONENT_GAP`。
- 必配 Audit / Missing Components 记录：需要什么能力、候选降级方案、期望的组件形态和授权状态。

## 首块必须是核心信息

任何组合下,**第一个 DetailBlock** 都满足:

- bodyType = `Descriptions`(或 `Descriptions + KeyMetrics` 组合)。
- 内容覆盖对象的"身份字段":名称、编码、归属、当前状态、关键时间。
- 第一个 Block 不放 Timeline、不放 Cards 子对象、不放 Table——这些都是"次级维度"。

## 高度规格(详情页内)

详情页**不使用** form 抽屉那套 32px 硬性规格,因为绝大多数字段是只读:

- Descriptions label / value 行高 32px,间距 12px。
- Table 行高 44px(沿用 qifu-list-page 表格 size=medium)。
- 行内按钮(若有)使用 28px 小号 + `variant=text` 或 `link`,不使用 32px 实心按钮。
- 页头的主/次操作使用 32px 标准大小。

**铁律**:整个详情页内**只允许出现 ≤ 2 个实心 Primary Button**(一个在 PageHead,一个在关键 BlockHeader);其余按钮用 text/link/base 形态。
