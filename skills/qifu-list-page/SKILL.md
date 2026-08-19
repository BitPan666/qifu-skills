---
name: qifu-list-page
description: 根据业务描述、字段清单、截图或线框，在 Figma 中使用「奇富科技中后台组件库 新」的真实组件实例生成奇富后台列表页。适用于按稳定的组合名称调用基础表格、基础筛选表格、高级筛选表格、可选择筛选表格及加载或空状态列表，并完成页面导航、可选标题、筛选、列表操作栏、主操作、数据表格、状态与分页；也用于审查所需组件是否缺失。不要用于复杂分析看板、编辑表单、详情页、树表或高度定制的工作台。
---

# Qifu List Page

将简短业务描述转换为结构清楚、可编辑、保持组件实例关系的桌面端筛选列表页。把参考图作为信息架构基线，不机械复刻其中的品牌、业务名称或固定列数。

## 必读资料

开始前完整读取：

- [页面蓝图](references/page-blueprint.md)：页面结构、布局决策、筛选与表格规则。
- [组件映射](../qifu-shared/references/component-map.md)：组件名称、节点、发布键、属性和已知缺口。
- [表格组合注册表](references/table-compositions.md)：稳定组合名称、适用场景、组件结构和按名称调用规则。
- 当 `platform=yushu` 或用户提到“毓数”时，完整读取[毓数平台导航基线](../qifu-shared/references/platform-yushu.md)。

任何 `use_figma` 调用前加载并遵循 `figma-use`；创建或更新完整页面时同时加载并遵循 `figma-generate-design`。若目标项目另有 `AGENTS.md` 或项目级 Figma 规则，先读取并以其为准。

## 输入契约

接受自然语言，不要求用户填写完整表格。提取或合理补全以下 `PageSpec`：

```text
pageName       页面名称与对象，例如“群组管理”
pageTitle      可选页面标题；不需要时隐藏整个页头 Slot
compositionName 表格组合的完整注册名称；未指定时根据场景匹配，默认使用 Qifu List Page / Basic Filter Table
platform       所属平台；当前默认基准为 yushu
headerActive   顶部导航当前入口
sidePath[]     从一级菜单到当前页面的完整侧栏路径
sideActive     唯一选中的侧栏菜单
sideExpanded[] 需要展开的父菜单；与选中态分开
sideAncestorsActive[] 当前页的祖先菜单；由 sidePath 自动推导，用于父级路径视觉高亮
filters[]      字段、控件类型、占位文案、是否必填、默认值、可选 widthTier（120/160/200/304/408，默认 200）
primaryAction  主要动作，例如“新增群组”；没有新增动作时可为空
listActions.left[]  列表操作栏左侧动作；包含文案、语义、样式、是否危险、是否依赖行选择
listActions.right[] 列表操作栏右侧动作；包含文案、语义、样式、是否危险、是否依赖行选择
columns[]      表头、语义、宽度优先级、对齐、是否可排序/筛选
rowActions[]   行操作及危险级别
status         状态集合及语义
pagination     总数、每页条数、是否显示跳转
viewport       目标画板宽高；未指定时按列数选择
targetPage     Figma 目标 Page；测试、效果验证和 Skill 回归固定使用 `测试`（node `3497:651`），正式交付按用户指定
controlSize    筛选项与按钮的尺寸档位；默认使用 32px 常规大规格
filterItemDisplay 筛选项显示形式；`直接筛选框` 或 `带标题筛选项`，默认沿用直接筛选框
filterTrigger  筛选触发方式；`实时触发` 或 `按钮触发`，未指定时沿用实时触发
data           示例数据或数据特征
```

仅在缺少的信息会改变页面主结构或带来高风险误导时提问。其余内容按常见后台场景补全，并在交付说明中列出假设。

推荐用户按以下自然语言顺序描述；字段可省略，不要求填写表格：

```text
在【平台】的【顶部入口】中，
于【一级菜单 > 二级菜单 > 三级菜单】新增【页面名称】【列表页】。
页面【有/无】标题，标题为【标题】。
筛选项包括【字段 + 控件类型】；筛选项显示形式使用【直接筛选框 / 带标题筛选项】，触发方式为【实时触发 / 按钮触发】。
列表操作栏左侧包括【按钮】，右侧包括【按钮】。
表格包括【列名 + 内容形式】；行操作包括【操作】。
展示【行数】条示例数据，画板使用【1366×768 / 1920×1080】。
```

解析优先级固定为：平台 → 顶部入口 → 侧栏完整路径 → 页面名称与类型 → 标题 → 筛选 → 列表操作栏 → 页面主动作 → 表格 → 行操作 → 数据与画板。不要把顶部入口当成侧栏菜单，也不要把侧栏父菜单当成页面标题。

## 工作流

### 1. 形成页面规格

1. 从描述、截图或线框提取 `PageSpec`。
2. 先从[表格组合注册表](references/table-compositions.md)确定唯一的 `compositionName`。用户给出完整名称时精确匹配；用户只描述场景时按注册表的决策顺序匹配。不得临时创造近义名称或把业务对象名写进组合名。
3. 先确定 `platform`、`headerActive`、`sidePath`、`sideActive` 和 `sideExpanded`，并从 `sidePath` 中排除 `sideActive` 后自动得到 `sideAncestorsActive`。当前项目中用户未指定平台时默认 `platform=yushu`；其他平台不得复用毓数菜单名称。
4. 将每个筛选条件映射为 `Input/Search`、`Select`、`Checkbox`、`DatePicker` 等控件。
5. 将页面按钮分为查询动作、列表操作栏左侧动作、列表操作栏右侧动作、单一主动作和行操作；同一动作只允许出现一次。
6. 将每一列标注为 `identifier`、`name`、`long-text`、`number`、`date`、`status`、`action` 等语义。
7. 画板只优先使用两档：常规桌面 `1366 × 768`、宽屏桌面 `1920 × 1080`。用户未指定时优先常规桌面；只有列数、长文本或横向信息密度无法在常规桌面合理容纳时才使用宽屏桌面或明确展示横向滚动。
8. 使用通用、可信且有差异的示例数据；不得把参考图中的具体产品名、账号或 URL 当作固定内容。

### 2. 盘点目标文件

1. 确认目标 Figma 文件、页面和插入位置；不要默认写到第一个 Page。凡提示词包含“测试”“效果验证”“试生成”或“Skill 回归”，必须复用 Page `测试`（node `3497:651`），不得写到组件介绍页、业务 Page，也不得新建近义测试 Page；正式交付且用户明确目标 Page 时按用户指定。
2. 检查同文件已有列表页，优先复用其画板尺寸、变量、文字样式和局部组合方式。
3. 按组件映射中的精确名称解析组件；节点 ID 失效时按名称重新发现，不猜测新 ID。
4. 同文件使用本地组件节点创建实例；跨文件使用发布键导入。
5. 记录组件覆盖结果：`resolved`、`fallback`、`missing`。未完成盘点前不得开始写页面。

### 3. 创建页面骨架

先创建唯一顶层画板，再把所有区域直接创建在画板内部。使用 Auto Layout 表达结构关系；内容区使用 `Templates / List Page Shell-V2` 真实实例，并严格按照 `compositionName` 配置 Slot。以下为默认组合 `Qifu List Page / Basic Filter Table`：

```text
Page / List / <pageName> / Default
├── Header
└── Workspace
    ├── SideNavigation
    └── Content（灰色背景）
        └── Page Surface（白色背景，距 Content 四周 12px）
            ├── ContextNavigation（按需）
            └── List Page Shell-V2 Instance（距 Page Surface 四周 16px）
                ├── pageHeaderSlot
                ├── filterBarSlot → Filter Bar-V2 Instance
                └── tableSlot
                    ├── 无列表操作：Table Shell-V2 Instance
                    └── 有列表操作：Data Region（Vertical，gap 12）
                        ├── List Action Bar（页面级组合）
                        └── Table Shell-V2 Instance
                            ├── headerSlot
                            ├── rowsSlot
                            └── paginationSlot
AuditNote（仅有缺口时，放在画板外侧相邻位置）
```

先创建外层，再实例化 List Page Shell V2，最后逐个替换 Slot 内容。内容区保持灰色背景；白色 `Page Surface` 与 Content 四周固定 12px，所有页面内容必须位于白色容器内并与其四周保持 16px。Page Surface 的 16px 是唯一的页面内容外边距；PageHeader、Filter Bar、List Action Bar、Table Shell 和 Pagination 不得再叠加左右或上下外层 padding。相邻区块之间固定 12px。没有列表操作时 `tableSlot` 直接承载 Table Shell-V2；存在列表操作时，`tableSlot` 承载页面级 `Data Region`，内部按 12px 间距依次放 List Action Bar 和 Table Shell-V2。不要重复创建独立 Pagination；它由 Table Shell V2 的 `paginationSlot` 管理。List Page Shell V2 默认内容宽度为 1248px；需要其他宽度时同步调整操作栏、表头、数据行和分页区域，无法稳定适配时记录响应式缺口。

组合名称只负责选择稳定结构，不替代组件正式名称，也不要求在 Figma 中重命名母版。先记录 `compositionName`，再按注册表解析 `showFilterBar`、`expanded`、`selection`、`rowsSlot` 和分页策略；筛选字段、列、文案、数据和 `TableStyleSpec` 仍由当前 `PageSpec` 决定。

### 4. 组装导航与标题

- `platform=yushu` 时，顶部必须使用 `Navigation / HeaderMenu / Yushu Header-V2`，通过 `activeMenu 当前菜单` 设置 `headerActive`；用户名固定为 `panyue`，不重新拼装头像和功能图标。
- 毓数侧栏按[毓数平台导航基线](../qifu-shared/references/platform-yushu.md)使用 `Navigation / SideMenu / SideMenuItem-V2` 真实实例逐项组装。一级菜单通过 `icon 图标` 替换本地图标，并用 `showIcon 显示图标` 控制显隐；二、三级菜单保持纯文本。`sideActive` 是唯一的当前页菜单；`sideExpanded` 中的父项设置 `expanded 展开=True` 并插入已确认子项，其他父项设置为 `False`。页面位于子菜单时，把 `sidePath` 中除 `sideActive` 外的全部祖先加入 `sideAncestorsActive`：这些父项使用组件的 `State=Selected` 取得“白底 + 文字、图标、箭头主题绿”的祖先激活样式，同时保持展开；非当前路径上仅为展示而展开的父项仍使用 `State=Default`。叶子选中与祖先路径高亮是两种结构语义，不得把普通展开项误设为绿色。
- 其他平台使用对应平台映射中的真实 HeaderMenu 与 SideMenu；组合组件无法改业务文案时，使用对应 `HeaderMenuItem` / `SideMenuItem` 真实实例合法组合，不覆盖成手绘菜单。
- 侧栏宽度为 200px并填充 Header 以下高度；菜单内容放入可纵向滚动区域，底部收起按钮固定保留，不随菜单滚动。静态画板需要完整显示菜单时允许增加画板高度。
- 仅在存在多层路径时使用 Breadcrumb；存在同级内容切换时使用 Tabs。
- 参考图中的“可关闭页签”不是普通 Tabs 的默认能力；组件缺失时使用最接近的现有实例并记录缺口，不手绘成正式组件。
- 页面标题不是必选项。需要标题时使用 16px，PageHeader 自身 padding 为 0；标题文字直接落在 Page Surface 的左上 16px 内容边界。标题说明当前对象或任务，不重复当前菜单的全部层级。
- 不需要标题时关闭 `showPageHeader`，不要保留空页头；此时筛选栏直接从 Page Surface 的 16px 顶部内边距开始。

### 5. 组装筛选工具栏

- 先执行 `compositionName` 的筛选栏规则：无筛选组合关闭 `showFilterBar`；基础筛选组合使用单行；高级筛选组合使用两行。不要因为当前字段少就把高级组合改名为基础组合，也不要在无筛选组合中保留空工具栏。
- 优先使用 `Data Display / Filter Bar-V2`。把高频字段放入 `primaryFiltersSlot`，第二行字段放入 `moreFiltersSlot`，Checkbox 等快捷条件放入 `quickFiltersSlot`，确定/重置放入 `queryActionsSlot`，页面主操作放入 `primaryActionSlot`。
- 常用筛选与更多筛选中的每个字段优先使用 `Data Display / Filter Item-V2` 包裹真实控件。`display 显示形式=直接筛选框` 保持现有纯控件形式；`display 显示形式=带标题筛选项` 使用“标题：+ 筛选控件”。标题通过 `label 标题` 配置，冒号属于标题文案；标题右边缘到筛选控件左边缘的水平间距固定为 `8px`，不得设为 0，也不得由页面实例覆盖成其他值。
- `size 尺寸=28px` 时标题为 12px；`size 尺寸=32px` 时标题为 14px；两档标题颜色均固定为 `#565656`。同一筛选栏不得混用标题字号或控件高度。
- 筛选控件宽度使用固定阶梯 `120 / 160 / 200 / 304 / 408px`，默认从 `200px` 起选。`120/160px` 仅用于文案短且选项稳定的枚举或布尔条件；日期范围、长编号、Webhook 等按内容使用 `304/408px`。不得任意写入阶梯之外的宽度，也不得把同排 Filter Item 设置为 FILL 后机械等分拉伸。
- `直接筛选框` 的 Filter Item 总宽度等于所选阶梯；其内部控件允许在这个已定宽的 Filter Item 内使用 FILL，但最终可见宽度必须等于阶梯值。`带标题筛选项` 的控件本体按阶梯定宽，Filter Item 总宽度为“标题 HUG + 8px + 控件阶梯宽度”。Filter Item 本身必须使用 `layoutSizingHorizontal=FIXED`，不得因同行空余空间被拉宽。
- `primaryFiltersSlot`、`moreFiltersSlot` 和承载它们的行使用水平 Auto Layout，水平间距 12px、换行间距 12px，并开启 `layoutWrap=WRAP`。横向空间不足时按字段整体换行，不得把控件压缩到所选阶梯以下；画板放大后保留语义宽度，不为铺满空间而拉长。查询按钮保持 HUG，作为一组跟随最后一行，空间不足时整体换到下一行。
- 单行使用 `expanded=false`；两行使用 `expanded=true`。通过 `trigger 触发方式=实时触发/按钮触发` 选择唯一触发模式；`showQuickFilters`、`showPrimaryAction` 默认均为 `false`，只有 PageSpec 明确需要快捷条件或页面主操作时才按需开启，不删除母版结构。`showQueryActions` 已移除，不得继续设置或模拟该属性。
- 将筛选控件放在左侧，将页面级主要动作放在最右侧。
- Filter Bar 外层 padding 为 0。第一个筛选控件直接对齐 Page Surface 左侧 16px 内容边界，页面主操作右边缘直接对齐 Page Surface 右侧 16px 内容边界；不得在 Page Surface 的 16px 之外再叠加 Filter Bar 的 12px。
- 1–4 个条件使用单行；5–8 个条件允许换成两行；更多条件保留高频项并提供“更多筛选”入口。
- 实时触发的单字段模糊查询使用 Search；按钮触发的文本筛选统一使用 Input，避免 Search 自带触发与“确定”按钮形成双重触发。枚举使用 Select；独立布尔条件使用 Checkbox；时间范围使用 DatePicker。
- Search 的占位文案和当前查询值分别通过 `placeholder 文案`、`value 文案` Text 属性配置，不直接覆盖实例内部文本。
- `filterTrigger=实时触发` 时，值改变或 Search 字段内动作后刷新，不显示确定/重置；`filterTrigger=按钮触发` 时统一显示“确定 / 重置”。两种触发方式只能选择一种。
- 按钮触发默认使用 32px Button：确定=`variant 类型=base 基础`，重置=`variant 类型=outline 描边`，两者均为 `size 尺寸=large 大尺寸`。单行时按钮跟随第一行筛选项；两行时按钮跟随第二行筛选项。把“新增”等页面级主要动作固定在工具栏第一行最右侧，不与筛选确认按钮混成同一操作组。
- 标准数据表格页默认使用“32px 常规大规格”：Filter Item V2 选择 `size 尺寸=32px`，Input V2 选择原生 32px 的 `M 默认尺寸`，Select 选择 `LG 大尺寸`，Button 选择 `large 大尺寸`；筛选项按上述宽度阶梯定宽并允许整项换行，最终可见高度必须是 32px。同一工具栏必须统一规格，不再对 Input 实例做额外高度覆盖。仅在用户明确要求紧凑密度时才使用小尺寸。
- 插入控件后检查 `Primary Row`、`primaryFiltersSlot`、`queryActionsSlot`、`primaryActionSlot` 等容器均至少为 32px 且不裁切内容；不得只检查控件自身高度。
- 主要按钮文案使用动宾结构，如“新增群组”“创建规则”。没有创建权限或业务不支持新增时不强行添加。

### 6. 组装列表操作栏

- 当 `listActions.left[]` 与 `listActions.right[]` 均为空时不创建操作栏，`tableSlot` 继续直接承载 Table Shell-V2。
- 任一侧存在动作时，在 `tableSlot` 中创建页面级 `Data Region`：垂直 Auto Layout、宽度 FILL、间距 12px、padding 0；先放 `List Action Bar`，再放 Table Shell-V2。该结构是 Skill 允许的页面级组合，不是新的 Figma 母版，不因它单独生成组件缺口 Audit。
- `List Action Bar` 使用水平 Auto Layout、宽度 FILL、高度 32px、padding 0、垂直居中。内部依次为 `List Actions / Left`、FILL 的 `Flexible Spacer`、`List Actions / Right`；左右按钮组均为 HUG，组内默认间距 8px，并优先绑定现有 spacing 变量。
- 左侧承载与当前数据或所选行相关的批量/上下文动作，例如批量启用、批量停用、批量删除、分配。`requiresSelection=true` 的动作在未选择行时保持可见但禁用；危险动作使用危险语义并提供确认。
- 右侧承载不依赖当前行选择的列表级动作与工具，例如刷新、导入、导出、列设置，以及唯一的页面强主动作。右侧从次要到主要排列，唯一 Primary 按钮放在最右侧。
- 确定/重置始终属于 Filter Bar 的 `queryActionsSlot`；查看/编辑/删除单条记录始终属于表格行操作。不得把这两类动作塞进 List Action Bar。
- 独立 List Action Bar 出现时，Filter Bar 设置 `showPrimaryAction=false`。原 `primaryAction` 若未明确指定侧别，迁移到 `listActions.right[]` 最右侧；不得在 Filter Bar 和操作栏重复展示同一动作。
- 两侧动作过多导致 1366px 画板无法稳定容纳时，保留高频动作，次要动作进入现有“更多”菜单能力；没有可复用菜单组件时记录缺口，不允许按钮换行、重叠或缩小到组件规范之外。

### 7. 组装表格与分页

- 先执行 `compositionName` 的表格规则，再形成 `TableStyleSpec`。组合注册表固定 `selection`、`rowsSlot` 状态和默认分页策略；`size` 与 `type` 仍按页面需求设置。状态组合只能展示注册状态，不得同时堆叠数据行、Loading 和 Empty。
- 优先使用 `Data Display / Table / Shell-V2`，通过 `size`、`type`、`selection` 选择整表结构。显示或隐藏选择列时默认外壳均为 1248px，不应让页面发生横向跳动。
- 在替换任何 Slot 前先确定唯一的 `TableStyleSpec={size,type,selection}`。Table Shell-V2 的三个属性只控制母版中的默认 Slot 内容；`headerSlot` 或 `rowsSlot` 被自定义实例替换后，外壳属性不会级联到 Header Cell-V2、Row-V2、Content Cell-V2 或 Selection Cell-V2。必须按照[组件映射中的逐层同步表](../qifu-shared/references/component-map.md#table-shell-v2-slot-替换后的逐层同步强制)显式设置所有后代实例，并在同一次生成操作中完成，不能只切换外壳变体。
- 自定义 `rowsSlot` 的行数与母版默认行数不一致时，切换 `size`、`type` 或 `selection` 可能把 Table Shell 实例高度重置为母版固定高度，即使内部 Slot 已正确增高也会裁切后续行和分页。每次完成后代同步后，必须重新计算 `requiredTableHeight = headerSlot.height + rowsSlot.height + paginationSlot.height`，把 Table Shell 实例高度显式设为该值，并确认外层 `tableSlot` 与 List Page Shell 已按内容高度重新包裹。
- 表头使用 Header Cell-V2；数据行使用 Row-V2；每个单元格使用 Content Cell-V2，并把 Text-V2、Status-V2 或 Action Content-V2 实例放入 `contentSlot`。任意列数通过 `cellsSlot` 和 `headerSlot` 合法组合，不回退到原版固定 Table。
- 根据语义分配列宽：序号/ID 最窄，名称中等，长文本或 URL 弹性扩展，状态与操作保持稳定宽度。以内容需求计算各列基准宽度，再让所有列宽之和等于表格可用宽度；列背景和分割线必须连续，不使用会在单元格之间产生空白带的 `SPACE_BETWEEN`。
- 第一列从表格左边界开始，最后一列到达表格右边界；中间列通过内容优先级分配剩余宽度。表头与每行必须使用完全相同的列宽数组。
- 长内容保留单行并省略；需要阅读全文时提供 Tooltip 或查看操作，不让一行无限增高。
- 二元“启用 / 禁用”业务状态直接使用 `Data Display / Tag / Tag`：启用=`variant=light 亮色`、`theme=success 成功色`、`size=medium 中尺寸`、`shape=square 矩形`、`disabled=false`、`Show icon=false`、`Show closeBtn=false`、`text=启用`；禁用除 `theme=danger 危险色`、`text=禁用` 外参数相同。这里的“禁用”是业务状态，Tag 自身的 `disabled` 仍为 `false`。pending、error、processing 等多状态场景继续使用 Status Content V2；若视觉必须是“圆点 + 文本”，使用克制的页面级组合并标记 `missing`。
- 行操作优先使用 Action Content V2，通过 `action1..4` 与 `showAction2..4` 配置 1–4 个动作。根据 `rowActions[]` 顺序把唯一危险操作映射到 `dangerAction=None/Action1/Action2/Action3/Action4`；不可逆操作同时使用 `Danger` Popconfirm。没有危险操作时必须选择 `None`，不得把“启用、查看、编辑”等普通动作误标为危险。若业务确有多个危险动作，保留风险最高的一项为直接危险操作，其余收纳或拆分确认流程并记录需求；操作超过 4 个时收纳次要操作。
- 操作列中的动作组整体右对齐，右侧保留 20px；“操作”表头不是贴右对齐，而是让文字左边缘与下方动作组第一个文案（通常为“查看”）的左边缘对齐。计算 `actionGroupStart = operationCellWidth - 20 - actionGroupWidth`，表头文字从同一位置开始。Header Cell-V2 尚未暴露该能力时，使用样式继承自 Header Cell-V2 的页面级最小回退 `Fallback / Header Cell / 操作 / Align to Action Group`，并在 Audit 中记录缺口。
- 行操作必须与当前状态一致：启用记录提供“停用”，停用记录提供“启用”；不要在停用记录上继续显示“停用”。批量状态同理。
- 展示 5–10 行有差异的示例数据。`1366 × 768` 且含标题、单行筛选和 44px 数据行时，优先生成 9 行；如果底部空间仍明显过大且能保留 Page Surface 的 16px 底边距，可增加到 10 行。不要用完全相同的一行机械复制。
- 在 `1366 × 768` 画板中优先用真实示例行占用表格高度，不拉高固定行高，也不拉伸 `paginationSlot` 填空。Pagination 必须紧跟最后一条数据行；`paginationSlot` 上下内边距均为 12px、左右内边距均为 0、使用内容高度且 `layoutGrow=0`。Pagination 可见右边缘必须与 Table Shell 可见右边缘精确相等。若母版 Slot 宽于当前已调整的 Table Shell 可见宽度，使用与 Slot 同宽的右对齐包装层，并设置 `paddingRight = slotWidth - visibleTableWidth`；不得让按可见表宽缩窄的分页条被过宽 Slot 再次向右推移。
- Data 状态保留 `rowsSlot` 中的数据行；Loading 或 Empty 时把 `rowsSlot` 内容替换为对应组件实例。默认画面只交付一个状态。
- Pagination-V2 放在 `paginationSlot` 中；先计算 `pageCount=ceil(total/pageSize)`，映射为 `1 单页 / 2 两页 / 3 三页 / 4 四页 / 5 五页 / 6+ 多页`，再设置 `size=medium 默认`、`showTotal`、`showPageSize`、`showJumper` 和各文案属性。普通列表默认展示第一页；无分页场景清空该 Slot。

### 8. 处理组件缺口

发现缺失能力时：

1. 优先使用现有组件的合法组合。
2. 不修改组件库母版，不分离实例，不在业务页面中创建冒充正式库组件的母版。
3. 使用页面级最小降级实现，并把节点命名为 `Fallback / <Capability>`。
4. 在画板右侧创建 `Audit / Missing Components`，逐项写明：
   - 需要的组件或能力；
   - 当前页面场景；
   - 当前降级方案；
   - 建议的组件属性与状态。
5. 在交付信息中重复列出缺口，便于维护者补齐组件库。

### 9. 验证

逐区截图检查，再检查整页。至少验证：

- 所有设计系统元素仍为 `INSTANCE`，且主组件名称正确。
- `compositionName` 与注册表完全一致，且筛选栏、展开方式、选择列、`rowsSlot` 状态和分页策略符合该组合；没有出现未注册别名。
- 平台、顶部入口、侧栏路径、唯一当前页菜单、祖先激活路径和展开组与 `PageSpec` 一致。毓数页面使用 `Yushu Header-V2`，不回退到通用 HeaderMenu。
- 侧栏使用 `SideMenuItem-V2`；确认所有实例的 `Label` 已实际显示业务文案，一级菜单通过组件公开的 `icon 图标` 属性使用已映射的本地图标实例，二、三级菜单不显示业务图标；菜单滚动区域与底部收起按钮相互独立。若存在展开父项，检查 `expanded 展开=True` 且子项已插入；当前页全部祖先应为“白底 + 文字、图标、箭头主题绿”，非祖先的普通展开项仍为默认黑色。只允许 `sideActive` 叶子出现绿色选中背景和右侧指示条。
- 内容区优先为 List Page Shell V2 实例；其 Filter Bar V2 与 Table Shell V2 仍保持嵌套实例和 Slot 关系。存在列表操作栏时，`tableSlot` 只增加一层页面级 Data Region，Table Shell V2 仍为真实嵌套实例。
- 筛选字段、属性和值与 `PageSpec` 一致。
- 测试、效果验证和 Skill 回归画板的直接父级为 Page `测试`（node `3497:651`）；没有落到组件介绍页、业务 Page 或新建的近义测试 Page。
- 列数、表头、数据、状态和行操作语义一致；Action Content V2 的 `dangerAction` 与实际危险动作位置一致，状态切换类动作中“停用”可为危险项，“启用”保持普通语义。
- 无文字截断、节点重叠、画板溢出和空白异常。
- 页面在目标宽度下无需无意义缩小控件；需要横向滚动时有明确容器。
- 常规桌面画板为 `1366 × 768`，宽屏桌面为 `1920 × 1080`；未明确要求时优先前者。
- Content 为灰色背景；白色 Page Surface 与 Content 四周间距均为 12px；页面内容与 Page Surface 四周间距均为 16px。
- 标题存在时为 16px 且 PageHeader padding 为 0，标题相对 Page Surface 左上偏移为 `(16,16)`；标题关闭时不存在空页头，筛选栏距 Page Surface 顶部 16px。
- PageHeader、Filter Bar、List Action Bar、Table Shell 的相邻可见区块之间均为 12px；操作栏不存在时不保留空白占位。
- Filter Bar 外层 padding 为 0；首个控件和页面主操作分别直接对齐 Page Surface 的左右 16px 内容边界。
- List Action Bar 宽度与 Table Shell 一致、高度 32px、padding 0；左组贴左、右组贴右、组内间距 8px，全部按钮为 Button 真实实例且高度 32px。
- List Action Bar 出现时 Filter Bar 的 `showPrimaryAction=false`；查询动作、列表操作、页面主动作与行操作没有重复或错位。依赖选择的动作在零选择时禁用，危险批量动作带确认。
- 普通页面的 Input、Select、Button 均为 32px 高，并分别映射到 `M 默认尺寸`、`LG 大尺寸`、`large 大尺寸`。
- 每个筛选控件最终可见宽度均属于 `120/160/200/304/408px` 阶梯，未指定时为 200px；Filter Item 为 FIXED，内部控件可在该定宽容器内 FILL，Slot 开启 WRAP，窄宽时整项换行而非缩小或等分拉伸。
- `filterItemDisplay=带标题筛选项` 时，每项均验证 `controlLeft - labelRight = 8px`；不得只检查 Auto Layout 属性而忽略实际几何间距。
- 筛选控件及其父行、Slot 均无上下描边裁切。
- 表头与数据行列宽逐列一致，所有列连续铺满表格；第一列贴左，操作动作组整体贴右并保留 20px，操作表头左边缘与第一个动作文案左边缘对齐。
- Pagination 紧跟最后一行，`paginationSlot` 上下内边距均为 12px、左右为 0 且不吸收剩余高度；验证 `paginationRight == tableRight`，母版 Slot 过宽时已用右侧补偿 padding 对齐。768px 高度下优先通过 9–10 条有差异的数据减少异常空白。
- 二元启用状态的每个状态单元格均为 Tag 真实实例：启用使用 success，禁用使用 danger；两者均为 light / medium / square、`disabled=false`、无图标、无关闭按钮，文案准确。
- 组件字体、颜色、间距、圆角优先继承变量和样式，不存在可用变量时才使用文件现有值。
- 使用 Pagination-V2 的 `total 总数`、`current 当前页`、`pageSize 每页条数`、`jump 跳转页`、`endPage 末页`、`jumpTotal 跳转总页数` 配置文案；验证可见数字页码数量与 `pageCount` 一致，只有 6+ 才出现 ellipsis。仅当提示词明确要求当前页大于 1、动态页码窗口或复杂首末页状态时记录缺口。
- Table Shell V2 的 `headerSlot`、`rowsSlot`、`paginationSlot` 各存在一次；切换 `selection` 时默认外壳宽度保持一致。
- 自定义 Slot 内所有 Header Cell-V2、Row-V2、Content Cell-V2、Selection Cell-V2 均与同一个 `TableStyleSpec` 一致；不得把“外壳属性已正确”当作后代实例已经同步的证据。
- Table Shell 实例高度等于 `headerSlot.height + rowsSlot.height + paginationSlot.height`，`paginationSlot.y + paginationSlot.height` 不得超过 Table Shell 高度；切换任一表格变体后均需重新验证，不能沿用母版默认行数对应的固定高度。
- `type=bordered` 时逐个检查表头、数据行和内容单元格的 `divider=both`；`type=basic` 时均为 `divider=horizontal`；`type=stripe` 时分割线为 `horizontal`，每行 Row、该行全部 Content Cell 和 Selection Cell 的 `background` 同步按 `default/stripe` 交替。
- `selection=on` 时表头和每个数据行各有一个 Selection Cell-V2，数量必须为“数据行数 + 1”；`selection=off` 时数量为 0。选择列位于第一业务列之前，不能只修改 Table Shell-V2 的 `selection`。
- 默认态不同时展开下拉菜单、弹窗或多个 Hover 状态。
- 没有遗留 placeholder shimmer、临时截图或参考图栅格。
- 存在缺口时已生成 `Audit / Missing Components`。

## 硬性约束

- 不把参考图直接作为图片放进画板交付。
- 不重画已有组件，不分离实例来改外观。
- 不为追求截图相似度破坏组件属性或变量绑定。
- 不擅自改动、补充或发布组件库母版。
- 不把页面级 List Action Bar 命名或发布成正式组件；只有后续明确确认需要长期组件化时才另行创建母版与 Shell Slot。
- 不把复杂看板、树表、批量编辑或详情表单硬塞进本 Skill。
- 不宣称缺失组件已存在；明确区分正式实例与降级组合。

## 已知限制

> 按时间倒序，最新在最前。跑通后发现的限制统一放这里，不散落在正文各处。
> 仓库内回填方式见 `_docs/limit-backfill.md`(仅发布仓)。

_(暂无记录;首次跑通后按 limit-backfill 的格式追加)_

## 交付内容

完成后返回：

- 页面节点 ID 与名称；
- 使用的 `compositionName`；
- 使用的主要组件及关键变体；
- 对输入描述做出的假设；
- 组件缺口及建议补充项；
- 视觉和结构验证结果。
