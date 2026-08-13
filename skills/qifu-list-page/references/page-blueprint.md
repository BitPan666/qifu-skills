# 标准数据表格页蓝图

## 目录

- [参考图的可复用信息](#1-参考图的可复用信息)
- [画板与区域](#2-画板与区域)
- [上下文导航](#3-上下文导航)
- [页面标题与主要动作](#4-页面标题与主要动作)
- [筛选条件决策](#5-筛选条件决策)
- [列表操作栏](#6-列表操作栏)
- [表格列规则](#7-表格列规则)
- [数据与状态](#8-数据与状态)
- [响应与约束](#9-响应与约束)
- [推荐节点命名](#10-推荐节点命名)

## 1. 参考图的可复用信息

参考图表达的是典型中后台对象管理页，而不是必须逐像素复制的模板。其稳定结构为：

1. 全局顶部菜单；
2. 左侧分层导航；
3. 内容区上下文页签；
4. 页面标题；
5. 横向筛选工具栏；
6. 可选列表操作栏；
7. 右侧主要动作；
8. 多列表格；
9. 状态与行操作；
10. 右下分页。

参考图中的业务品牌、菜单名、用户头像、群组字段和示例 URL 只用于理解场景，不得成为默认输出。

## 2. 画板与区域

默认只生成桌面端，并优先在两种标准画板中选择：

| 使用场景 | 标准画板 | 处理方式 |
| --- | ---: | --- |
| 常规中后台页面 | 1366 × 768 | 默认选择；压缩非关键列，保持组件真实字号与高度 |
| 宽屏、高信息密度页面 | 1920 × 1080 | 长文本列弹性扩展；必要时横向滚动或冻结关键列 |

用户未指定画板时优先 `1366 × 768`。不要因为列数达到 7–9 列就自动扩到 1600px；先压缩序号、状态等短列，并让名称、日期和操作列保有合理宽度。只有常规画板无法稳定容纳信息时才使用 `1920 × 1080` 或明确横向滚动。不要为塞入更多行压缩组件真实高度。

测试、效果验证、试生成和 Skill 回归画板统一放入既有 Figma Page `测试`（node `3497:651`）。不得把测试内容放入组件介绍页或业务 Page，也不得创建 `Test`、`Skill Test` 等近义 Page；正式交付且用户明确目标 Page 时例外。

页面使用灰色工作区与白色内容容器：

```text
Root（Vertical）
├── HeaderMenu（Full width）
└── Workspace（Horizontal, Fill）
    ├── SideMenu（Fixed）
    └── Content（Vertical, Fill, 灰色背景）
        └── Page Surface（白色背景）
            └── Page Content
```

Page Surface 与 Content 四周固定 12px；Page Content 与 Page Surface 四周固定 16px。标题、筛选栏、列表操作栏、表格和分页均属于 Page Content，不得悬浮在白色容器外。Page Surface 的 16px 是唯一的内容外边距，内部区块不得再次叠加外层 padding。PageHeader、Filter Bar、List Action Bar、Table Shell 的相邻可见区块之间固定 12px。优先绑定文件已有 spacing 变量；不存在时使用上述已确认数值。

## 3. 上下文导航

先确定平台导航，再判断内容区是否需要 Breadcrumb 或 Tabs。当前毓数平台的顶部入口、侧栏菜单树、图标与展开规则见 [platform-yushu.md](platform-yushu.md)。

按信息架构选择一种或组合使用：

- 单一路径、无同级切换：按业务需要使用页面标题；标题不是必选项。
- 多层路径：Breadcrumb + 页面标题。
- 同级视图切换：Tabs + 页面标题。
- 多任务工作区、可关闭标签：需要独立 WorkspaceTabs 能力，不用普通 Tabs 冒充；缺失时记录组件缺口。

不要同时堆叠无意义的 Breadcrumb、Tabs、页签条和重复标题。

平台导航规则：

- 顶部导航只切换平台或产品入口，不根据单个业务页面随意新增菜单。
- 侧栏当前页由完整菜单路径决定；一张默认页面只允许一个叶子项显示绿色选中背景和右侧指示条。
- 父菜单展开、当前页选中和祖先路径高亮分别处理；当前项位于子菜单时必须展开全部祖先，并让祖先文字、一级图标和箭头显示主题色。非当前路径上的普通展开父项保持默认黑色。
- 侧栏菜单区可滚动，底部收起按钮固定保留；画板增高时侧栏随 Workspace 填充高度。

## 4. 页面标题与主要动作

PageHeader 包含：

- 可选标题：对象或任务名称，16px；PageHeader padding 为 0，标题直接位于 Page Surface 左上 16px；
- 可选辅助说明：只有当标题不能解释范围或权限时添加；
- 可选主要动作：没有 List Action Bar 时放在筛选区右侧或标题右侧；存在 List Action Bar 时放入右侧按钮组最右端。整页只保留一个视觉最强主动作。

主要动作使用“动词 + 对象”，例如“新增群组”“创建策略”“导出明细”。“查看”“编辑”“删除”属于行操作，不进入 PageHeader。

不需要标题时关闭整个 PageHeader，不保留空白占位；筛选栏从 Page Surface 的 16px 顶部内边距开始。

## 5. 筛选条件决策

| 字段语义 | 控件 | 示例 |
| --- | --- | --- |
| 实时触发的模糊文本 | Search | 名称、关键词 |
| 按钮触发的模糊文本 | Input | 名称、关键词 |
| 精确文本/编号 | Input | 工单号、Webhook、手机号 |
| 单选枚举 | Select Single | 状态、类型、所属部门 |
| 多选枚举 | Select Multiple | 标签、角色 |
| 独立布尔条件 | Checkbox | 仅看我创建、包含停用 |
| 单日/日期范围 | DatePicker | 创建日期、统计周期 |
| 级联层级 | Cascader | 组织、地区、类目 |

布局规则：

- 1–4 项：单行，主要动作贴右。
- 5–8 项：允许两行；保持字段顺序为高频到低频。
- > 8 项：首屏保留 3–5 个高频项，其余进入“更多筛选”。
- 同一行筛选项高度与显示形式一致。每个字段使用 Filter Item V2 包裹真实控件，宽度只使用 `120 / 160 / 200 / 304 / 408px` 阶梯，默认 200px；120/160px 仅给短枚举或布尔条件，日期范围与长文本按内容使用 304/408px。Filter Item 为 FIXED，不使用 FILL 等分拉伸；直接筛选框的内部控件可在已定宽的 Filter Item 内 FILL，但最终可见宽度仍须等于阶梯值。
- 筛选 Slot 使用水平 Auto Layout，水平与换行间距均为 12px，并开启 WRAP；空间不足时整项换行，不缩小到阶梯以下。直接筛选框总宽度等于控件阶梯；带标题筛选项为“标题 HUG + 8px + 控件阶梯宽度”。查询按钮保持 HUG 并作为一组跟随最后一行。
- Filter Bar 外层 padding 为 0；首个控件与主操作直接对齐 Page Surface 的左右 16px 内容边界。
- 快捷条件与页面主操作默认不展示：`showQuickFilters=false`、`showPrimaryAction=false`。只有 PageSpec 明确声明对应内容时才开启；按钮触发型的“确定 / 重置”不受这两个属性影响。
- `display 显示形式=直接筛选框` 为纯控件形式；`display 显示形式=带标题筛选项` 为“标题：+ 筛选控件”。标题与控件之间固定为 8px，并以 `controlLeft - labelRight = 8px` 验证实际几何间距。28px 控件对应 12px 标题，32px 控件对应 14px 标题，标题颜色均为 `#565656`。
- 普通页面统一使用“32px 常规大规格”：Filter Item V2=`size 尺寸=32px`、Input V2=`M 默认尺寸`、Select=`LG 大尺寸`、Button=`large 大尺寸`。筛选项按宽度阶梯定宽并允许整项换行，高度保持 32px；仅在明确要求紧凑模式时使用小尺寸。
- 控件所在的 Row 与 Slot 必须至少为 32px 且不得裁切内容；不能只把控件本身设为 32px。
- 占位文案用于提示格式或示例，不替代难以理解的字段标签。
- 按钮触发时，单行的“确定 / 重置”跟随第一行最后一个筛选项；两行的“确定 / 重置”跟随第二行最后一个筛选项。页面级“新增”固定在第一行最右侧。

触发方式只能选择一种，并通过 Filter Bar V2 的 `trigger 触发方式` 真实变体设置：

- `实时触发`：值改变或 Search 字段内动作后刷新，不显示确定/重置；
- `按钮触发`：文本字段使用 Input，统一显示“确定 / 重置”。确定使用 32px 主要按钮，重置使用 32px 线框按钮。

## 6. 列表操作栏

列表操作栏是页面级组合，不单独创建或发布 Figma 母版。存在 `listActions.left[]` 或 `listActions.right[]` 时，`tableSlot` 放入垂直 `Data Region`，内部依次为 List Action Bar 与 Table Shell-V2，间距 12px；Filter Bar 到操作栏的间距由 List Page Shell-V2 的区块间距提供，同样为 12px。

```text
tableSlot → Data Region（Vertical, Fill, gap 12）
├── List Action Bar（Horizontal, Fill, height 32, padding 0）
│   ├── List Actions / Left（Hug, gap 8）
│   ├── Flexible Spacer（Fill）
│   └── List Actions / Right（Hug, gap 8）
└── Table Shell-V2 Instance
```

- 左侧：当前数据或选择相关的批量/上下文动作。依赖选择的按钮在零选择时禁用，危险动作需要确认。
- 右侧：刷新、导入、导出、列设置等全局列表工具，以及唯一的页面主动作；Primary 按钮固定在最右侧。
- 确定/重置留在 Filter Bar；单条记录动作留在表格行内。
- 操作栏出现时关闭 Filter Bar 的 `showPrimaryAction`，避免主动作重复。
- 操作栏为空时不创建 Data Region 包装，`tableSlot` 直接使用 Table Shell-V2。

## 7. 表格列规则

为每列标记语义和宽度优先级：

| 语义 | 建议行为 |
| --- | --- |
| 序号、短 ID | 窄列，通常不排序 |
| 名称 | 中等宽度，保持可读 |
| 长文本、URL | 弹性列，单行省略，配 Tooltip/查看 |
| 数字 | 右对齐；数量级差异大时使用千分位 |
| 日期时间 | 稳定宽度，格式一致 |
| 状态 | 稳定宽度；Tag 或状态点 + 文本 |
| 操作 | 内容右对齐，右边距 20px，宽度按操作数量计算 |

列宽先按内容语义确定基准，再把剩余宽度分配给中间列，使所有列宽之和等于表格宽度。第一列从左边界开始，最后一列到达右边界；表头和每行使用同一列宽数组。不要用 `SPACE_BETWEEN` 在单元格之间制造空白带，避免表头背景和行分割线断裂。

优先级顺序：

1. 保证名称、状态和操作可见；
2. 压缩序号和短 ID；
3. 对长文本省略；
4. 必要时启用横向滚动；
5. 不把字号缩小到组件规范之外。

行操作规则：

- 1–2 个：直接展示；
- 3–4 个：展示高频操作，保持稳定间距；
- > 4 个：保留 2–3 个高频项，其余进入更多菜单；
- 删除、解绑、停用等高风险操作必须有确认。
- 状态切换动作必须随记录状态变化：启用态显示“停用”，停用态显示“启用”。
- 操作列内的 Action Content-V2 整体靠右排列，单元格右侧固定保留 20px；“操作”表头文字的左边缘与动作组第一个文案的左边缘对齐，而不是贴到操作列右侧。Header Cell-V2 未暴露动作组起点对齐时使用页面级最小回退并记录缺口。

## 8. 数据与状态

示例数据应能验证布局：

- 名称长度有长有短；
- 至少包含两种状态；
- 长文本列至少有一条触发省略；
- 日期、数字或成员列表使用真实格式；
- 不使用真实个人敏感信息。

二元启用状态使用 Tag 真实实例：启用为 `light / success / medium / square`，禁用为 `light / danger / medium / square`；两者均保持 `disabled=false`、隐藏 icon 与 closeBtn，文案分别为“启用”“禁用”。“禁用”描述业务数据，不表示组件交互被禁用。pending、error、processing 等多状态场景继续使用 Status Content V2。

默认展示 5–10 行。`1366 × 768`、16px 可选标题、单行筛选、44px 行高的常规结构优先 9 行；若仍有明显空白且能保留 16px 底边距可使用 10 行。若用户只提供字段，不提供数据，生成结构化假数据并明确标注为示例。

需要考虑但不同时展示全部状态：

- Default：默认交付画面；
- Loading：刷新或首次加载；
- Empty：筛选无结果或尚无数据；
- Error：加载失败；
- Selected：存在批量操作时。

若库中没有 Empty 或错误态组件，在缺口清单中提出，不在默认画面堆叠所有状态。

## 9. 响应与约束

- Header 固定宽度填充，SideMenu 保持组件推荐宽度，Content 填充剩余空间。
- FilterToolbar 允许换行，主要动作保持在可预期位置。
- List Action Bar 不换行：左右按钮组贴边，空间不足时把低频动作收纳到现有更多菜单；不得缩小按钮、重叠或让左右组交叉。
- Table 宽度随 Content 变化；关键列固定，长列承担收缩。
- Pagination 紧跟最后一条数据行，不悬浮在页面任意位置。`paginationSlot` 上下内边距均为 12px、左右内边距为 0，使用内容高度且 `layoutGrow=0`；可见分页右边缘必须与 Table Shell 可见右边缘相等。若母版 Slot 更宽，使用同宽右对齐包装层，并令 `paddingRight=slotWidth-visibleTableWidth` 进行补偿。`1366 × 768` 下通过 9–10 条真实示例行减少空白，不拉伸分页 Slot 填空。
- 只在用户要求时制作窄屏或移动端；中后台桌面页不得自动缩成手机布局。

## 10. 推荐节点命名

```text
Page / List / <Object> / Default
Header / Global
Workspace
Navigation / Side
Content
ContextNavigation
PageHeader
FilterToolbar
Filter / <field>
Action / Primary
DataRegion
List Action Bar
List Actions / Left
List Actions / Right
Table
Column / <field>
Row / <index>
Cell / <field>
Pagination-V2
Audit / Missing Components
Fallback / <capability>
```
