---
name: qifu-detail-page
description: 用于在 Figma 中创建、更新或审查奇富后台详情页，支持 Flat、Tabbed、Master Detail 和 Readonly，并以真实组件实例验证 PageHead、详情区块与页面状态。不用于新建编辑表单、多记录列表、看板、树表或工作台。
---

# Qifu Detail Page

将简短业务描述转换为结构清楚、可编辑、保持组件实例关系的详情页。把参考图作为信息架构基线,不机械复刻其中的品牌、业务名称或固定字段数。

本 Skill 与 [qifu-list-page](../qifu-list-page/SKILL.md)、[qifu-drawer-form](../qifu-drawer-form/SKILL.md) 共享同一套六层 AI 设计体系；Token、Component、Platform Adapter 是跨原型共享资产，详情页 Archetype 与组合规则由本 Skill 负责。

## 必读资料

开始前完整读取:

- [共享页面上下文](../qifu-shared/references/page-context.md):统一平台、目标位置、状态、权限与默认值。
- [共享组件调用基线](../qifu-shared/references/component-invocation-baseline.md):组件解析、写入回读与失败分类。
- [页面蓝图](references/page-blueprint.md):页面骨架、PageHead、Tabs、DetailBlock、操作位置、间距铁律。
- [区块路由表](references/detail-block-map.md):六种 bodyType(Descriptions / Table / Cards / Timeline / KeyMetrics / Empty)的选型规则。
- [组合注册表](references/detail-compositions.md):Flat / Tabbed / Master Detail / Readonly 四种形态与调用规则。
- `platform=zhikexing` 且明确为“类目导航 + 筛选 + 分组问答浏览”时，完整读取 [智客星分类问答组合](references/category-qa-zhikexing.md)。此为受限的第五种组合，不改变四种单记录组合。
- 当 `platform=yushu` 或用户提到"毓数"时,完整读取[毓数平台导航基线](../qifu-shared/references/platform-yushu.md)。
- 当平台未指定或 `platform=generic` 时，读取[通用平台适配器](../qifu-shared/references/platform-generic.md)，不套用毓数菜单。
- `platform=zhikexing` 仅在 `compositionName=Qifu Detail Page / Category Q&A` 时允许按专属规则创建候选页面；其他详情组合仍返回 `UNSUPPORTED_PLATFORM`。不得把列表模板或 generic 外壳冒充智客星详情页。其他未注册平台同样失败关闭。
- 组件名 / 节点 ID / 发布 Key 全部复用[组件映射](../qifu-shared/references/component-map.md),不在本 Skill 重复维护。

任何 `use_figma` 调用前加载并遵循 `figma-use`;创建或更新完整页面时同时加载并遵循 `figma-generate-design`。若目标项目另有 `AGENTS.md` 或项目级 Figma 规则,先读取并以其为准。

## 输入契约

接受自然语言,不要求用户填写完整表格。先形成共享 `PageContext`，再提取或合理补全以下 `DetailSpec`:

```text
object           对象名称(单数),如"客户"/"规则"/"策略"
pageTitle        详情页标题(默认 = object 名称)
compositionName  详情页组合的完整注册名称;未指定时按场景推断,无法区分时默认 Qifu Detail Page / Flat
platform         所属平台;未指定且无可靠上下文时默认 generic
headerActive     顶部导航当前入口
sidePath[]       侧栏完整菜单路径(规则与 list-page 相同)
sideActive       当前选中菜单
recordId         当前记录 ID(用于 PageHead 副信息)
recordName       当前记录名称(PageHead 主标题)
recordTags[]     详情头 1..2 个状态 Tag
recordMeta       更新时间 / 创建人 等副信息
primaryAction    主操作(编辑 / 启用 / 停用 / 上线 ...),唯一
secondaryActions[] 次要操作 0..2
danger           可选 {label, confirm} 危险操作

tabs[]           可选;仅 Tabbed / Master Detail 组合使用
  └─ tabTitle    名词性 2-4 字短语

blocks[]         1..N 个 DetailBlock,按"核心信息 → 业务 → 关联 → 历史"顺序
  ├─ blockTitle   名词性 2-6 字短语
  ├─ bodyType     Descriptions | Table | Cards | Timeline | KeyMetrics | Empty | Custom(<BizBlock>)
  ├─ fields[]     bodyType=Descriptions 时的字段列表 [{label, value, type}]
  ├─ columns[]    bodyType=Table 时的列定义
  ├─ rows[]       bodyType=Table 时的行数据
  ├─ items[]      bodyType=Cards / Timeline / KeyMetrics 时的项
  ├─ [可选] blockAction  BlockHeader 尾操作(如"新建子记录 / 查看全部")
  └─ [可选] emptyHint   当 bodyType=Empty

defaultState     Data / Loading / Error / Disabled,默认 Data
fallbackPolicy   block | allow；默认 block，只有用户明确允许降级时才为 allow
masterDetail     仅 Master Detail 组合
  ├─ listWidth   默认 320px
  ├─ searchPlaceholder
  ├─ items[]     左侧记录列表 [{name, subLabel, active}]
  └─ activeId    当前选中记录(决定右侧 Body 显示内容)

viewport         默认 1366 × 768,可选 1920 × 1080
targetPage       Figma 目标 Page;测试固定 Page `测试`(node 3497:651)
```

仅在缺少的信息会改变主结构或带来高风险误导时提问。其余按常见后台详情页场景补全,并在交付说明中列出假设。

推荐用户按以下自然语言顺序描述;字段可省略:

```text
在【平台】上查看【对象】的详情页,记录名【XX】,ID【XX】。
页面【Tabs?】含【Tab1/Tab2...】。
详情头主操作【XX】,次要操作【XX/XX】。
区块包括:
  - 【基本/核心信息】:【字段1/字段2/...】
  - 【关联/历史】:【Table/卡片/时间线】
【可选】左侧实体列表(仅 Master Detail 场景)。
```

解析优先级固定为:平台 → 对象 → 记录名 → Tabs → 操作 → blocks[] → 状态。不要把 Tag、字段名当成区块名。

## 工作流

### 1. 形成 DetailSpec

1. 从描述、截图或线框提取 `DetailSpec`。
1a. 命中 `Category Q&A` 时转入专属规则：提取类目、筛选、分组、问题、回答和展开状态；不推断 recordId、recordName、recordTags 或首块 Descriptions。后续通用详情头、Tabs、DetailBlock 和 Master Detail 固定尺寸规则均不适用，直接按专属规则执行组件预检、落图和验证。
2. 先从[组合注册表](references/detail-compositions.md)确定唯一 `compositionName`:精确匹配 → 推断规则 → 默认 `Flat`，不凭空制造 Tabs。
3. 为每个区块确定 `bodyType`(查 [detail-block-map](references/detail-block-map.md));第一个区块必须是 `Descriptions`(或 Descriptions + KeyMetrics)。
4. 检查 Sections/Tags/操作数量是否越界(Tags ≤ 2,Head 操作 ≤ 3,行内操作 ≤ 2);越界就近收纳并记录假设。

### 2. 盘点目标文件

1. 确认目标 Figma 文件、页面和插入位置;不写到组件介绍 Page。
2. 凡提示词包含"测试""效果验证""试生成"或"Skill 回归",必须复用 Page `测试`(node `3497:651`)。
2a. 用户明确给出目标 Figma Page 或节点链接时，以该节点所在 Page 为准，不因目标 Page 名称含“测试”而改写落点。
3. 检查同文件已有详情页,优先复用其外壳尺寸、变量、文字样式。
4. 按[组件映射](../qifu-shared/references/component-map.md)解析组件;节点 ID 失效时按名称重新发现。
5. 同文件用本地组件节点创建实例;跨文件用发布键导入。
6. 记录 `resolved / missing / ambiguous / failed`；所有必需能力均为 `resolved` 后才开始写页面。

### 3. 创建页面骨架

沿用 list-page 的"外壳四层"(HeaderMenu / SideMenu / Content / Page Surface),但**不复用** List Page Shell 的三个 Slot;详情页生成独立的 Detail Page Shell。

```text
Page / Detail / <object> / <compositionName>
├── Header / Global
├── Workspace
│   ├── Navigation / Side
│   └── Content(灰底)
│       └── Page Surface(白底,距 Content 12px)
│           └── Detail Page Shell(距 Page Surface 16px)
│               ├── PageHead(96px)
│               ├── Tabs(可选,44px)
│               └── Body(padding 24, gap 16)
│                   └── DetailBlock × N
└── Audit / Missing Components(仅缺口时)
```

`Master Detail` 组合下,Body 内部再分:左 320px `EntityList` + 右自适应 `DetailBlocks`。

### 4. 组装 PageHead

- 高度 96px；Title 与副信息分别绑定组件库批准的标题/正文 Text Style；副信息颜色绑定 `文本颜色/--qifu-text-color-secondary`。字号和行高只用于核对，不以手填字体属性代替 Text Style。
- Tag **最多 2 个**,使用 Tag 真实实例(`light/{success|danger|info}/medium/square`);语义严格遵循 component-map。
- 主操作 Button primary 一个;次要操作 ≤ 2 个 Button base;再多次要操作进"更多"。
- `Readonly` 组合不显示主次操作,仅在 Head 最左放返回。

### 5. 组装 Tabs(可选)

- 仅 `Tabbed` / `Master Detail` 使用;`Flat` 不使用。
- Tab 数 2..7;超过 7 必须重设计。
- Tab 顺序:`基本信息` 永远第一;`变更记录 / 操作日志` 永远最后。
- 切 Tab 时 PageHead 保持可见——这是详情页和"跳新页面"的核心差异。

### 6. 组装 DetailBlock

- 按 `blocks[]` 顺序生成,Section 之间间距 16px。
- 每个 Block 由 `BlockHeader + BlockBody` 组成;BlockHeader padding `16 20`,BlockBody padding `20`。
- bodyType 对应的控件与规则全部按 [detail-block-map](references/detail-block-map.md) 执行。
- 第一个 Block 必须是"核心信息块"(Descriptions 或 Descriptions + KeyMetrics);**不允许**首块放 Timeline / Cards / Table。
- Table 类 Block 严格沿用 component-map 的 Table Shell-V2 同步规则;没有筛选、没有批量、行内操作 ≤ 2。
- `Custom(<BizBlock>)` 先尝试由现有真实组件形成页面级组合 `Custom / <BizBlock>`。无法表达时记录 `COMPONENT_MISSING`；仅当 `fallbackPolicy=allow` 时创建 `Fallback / <BizBlock>`，否则返回 `BLOCKED_COMPONENT_GAP`。

### 7. 状态管理

通过 `defaultState` 指定;**同一详情页只交付一种状态**。

- `Data`:默认;所有字段渲染。
- `Loading`:PageHead/Tabs 可见,Body 显示 Skeleton。
- `Error`:Body 使用 `Empty status=Failed` + "重新加载";PageHead 保留。
- `Disabled`:Body 使用 `Empty status=NoPermission`,Head 操作禁用。

### 8. 处理组件缺口

发现缺失能力时：

1. 优先使用现有组件的合法组合。
2. 不修改组件库母版,不分离实例,不在业务详情页中创建冒充正式库组件的母版。
3. 只有共享调用基线确认 `COMPONENT_MISSING` 且 `fallbackPolicy=allow` 时，才创建页面级最小降级，节点命名 `Fallback / <Capability>`；默认返回 `BLOCKED_COMPONENT_GAP`。
4. 在画板右侧创建 `Audit / Missing Components`,逐项写明:
   - 需要的组件或能力;
   - 当前详情页场景;
   - 当前降级方案;
   - 建议的组件属性与状态。
5. 在交付信息中重复列出缺口,便于维护者补齐组件库。

属性 Key、写后回读、INSTANCE_SWAP、Slot、字体、权限或目标文件失败属于执行失败，直接返回 `FAIL`，不得改走 Fallback。

### 9. 验证

逐区截图检查,再检查整体。至少验证:

- **层级归属检查**:页面内所有 Descriptions / Table / Tag / Button / Timeline / Empty 等真实组件 INSTANCE,都必须嵌套在 `PageHead`、`Tabs`、`DetailBlock / <name>` 这三个容器之内;不允许出现在 Page 根级或 Page Surface 之外的"孤儿组件"。发现即归位到正确容器。
- **重复节点检查**:Page Surface 内不存在与已嵌实例位置、尺寸几乎一致的重复节点(常见于 AI 未清理旧实例);发现即删除,并计入 Audit / Missing Components。
- 所有设计系统元素仍为 `INSTANCE`,且主组件名称正确。
- `compositionName` 与注册表完全一致,且 headMode / bodyMode / tabsCount / readonly 符合该组合。
- PageHead 高度 96px;Tag ≤ 2;主次操作 ≤ 3;主操作唯一。
- `Tabs` 数量 2..7,首 Tab 是"基本信息",末 Tab 是"变更/日志"类。
- `Flat` 组合不存在 Tabs;`Readonly` 主次操作为空。
- 第一个 DetailBlock 是 Descriptions 或 Descriptions + KeyMetrics,不是 Timeline/Cards/Table。
- DetailBlock 间距 16px;BlockHeader padding `16 20`;BlockBody padding `20px`。
- Descriptions 列数 2 或 3,label 宽 120px;状态字段同一组内只使用一种状态表达(优先 Tag)。
- Table 类 Block 沿用 Table Shell-V2 同步规则;行内操作 ≤ 2;无筛选无批量;空数据显示 Empty。
- Cards 列数固定 3;Card 内仅"图/头像 + 标题 + 副标题 + ≤1 action"。
- Timeline 节点 ≤ 10;最新在上;超出有"查看全部"。
- KeyMetrics 列数 3 或 4;数字 24px / 700;不做颜色编码除非业务有明确语义。
- 整页实心 Primary Button ≤ 2 个(PageHead 主操作 + 可选关键 BlockHeader 操作)。
- `Master Detail` 左 320px 固定,左列表当前选中项 Selected 状态正确;右 Body 显示该项的 blocks 内容。
- `Category Q&A` 额外按 [智客星分类问答组合](references/category-qa-zhikexing.md) 回读：类目 Search 仅由最外层实例的 `FILL` 或 `FIXED` 控制；手搓基线的分组标题为 46px、展开问题与回答行为 48px；分组容器四边描边、回答行仅底边描边；侧栏只使用单列二级菜单，客户添加收起、团队辅助与团队审核选中，以及选中/默认图标变量绑定均正确。
- 状态唯一:Data / Loading / Error / Disabled 只有一种。
- 存在缺口时已生成 `Audit / Missing Components`。
- 无文字截断、节点重叠、画板溢出。
- 所有留白来自 page-blueprint 第 8 节的 10 项铁律,不叠加自定义。

## 硬性约束

- 不把参考图直接作为图片放进页面交付。
- 不重画已有组件,不分离实例来改外观。
- 不为追求截图相似度破坏组件属性或变量绑定。
- 不擅自改动、补充或发布组件库母版。
- 不为详情页新增"DetailShell" Figma 母版;Detail Page Shell 是页面级框架组合,不是组件库资产。
- 不在同一详情页堆叠多状态、混用状态表达、堆叠 Tabs 内 Tabs。
- 不把列表页(FilterBar + List Action Bar + Table)硬塞进详情页;DetailBlock 内的 Table 是关联数据展示,不是"子列表页"。
- 不宣称缺失组件已存在;明确区分正式实例与降级组合。

## 已知限制

> 按时间倒序,最新在最前。跑通后发现的限制统一放这里,不散落在正文各处。
> 仓库内回填方式见 `_docs/limit-backfill.md`(仅发布仓)。

### 2026-08-12 · 继承自 qifu-drawer-form 的踩坑
- 页面内所有控件 INSTANCE 必须嵌套在 `PageHead / Tabs / DetailBlock/<name>` 三容器之一,不允许 Page 根级孤儿(详见验证清单"层级归属检查")
- Page Surface 内不允许存在与已嵌实例位置/尺寸几乎一致的重复节点(详见验证清单"重复节点检查")

## 交付内容

完成后返回:

- 页面节点 ID 与名称;
- 使用的 `compositionName`;
- 使用的主要组件及关键变体;
- 区块清单(blockTitle + bodyType);
- 对输入描述做出的假设;
- 组件缺口及建议补充项;
- 视觉和结构验证结果。
