# 智客星列表页组件映射

此 Skill 只使用复制模板内已存在的实例；创建新实例前必须按完整名称在当前文件解析，禁止猜测节点 ID。

| 角色 | 模板中的实例形态 | 规则 |
| --- | --- | --- |
| 页面外壳 | `Templates / List Page Shell-V2` | 保留已有 pageHeader、filterBar、table Slot 内容，不直接写 Slot。 |
| 筛选栏 | `Filter Bar / <pageName> / 按钮触发` | 保留按钮触发、展开两行状态。 |
| 筛选项 | `Filter / <field>` | 使用既有 Input、Select、DateRange 实例和标题，改字前回读属性。 |
| 操作按钮 | `Button / <action>` | 使用现有 Button 实例，校验 `text`、`variant`、`size`。 |
| 表格 | `Table Shell / <pageName> / Selectable` | 保留 `selection=on`、44px、bordered 与完整 Slot 层级。 |
| 表头 | `Header / <field>` | 继承表头文字样式与列宽。 |
| 单元格 | `Cell / <field>` + `Text / <value>` | 使用既有 Text-V2 或行动作实例，不能用裸 Text 覆盖。 |
| 状态 | `Tag / <status> / medium square` | 必须为真实 Tag，统一 medium/square。 |
| 分页 | `Pagination-V2 / <total> items / <pages> pages` | 放在既有 Pagination Bar 内，不移动至表格外。 |
| 导航 | `Navigation / <label>` | 一级菜单需保留真实图标实例和属性回读。 |

当前基线根节点为 `4892:34812`。解析顺序为：先用该节点；节点不可用时按完整名称 `Template / List Page / 智客星 / 1440 / 手动调整` 搜索，随后校验其真实尺寸仍为 `1366 x 768`。
