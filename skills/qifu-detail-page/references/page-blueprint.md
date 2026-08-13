# 标准详情页蓝图

## 目录

- [参考图的可复用信息](#1-参考图的可复用信息)
- [画板与主体骨架](#2-画板与主体骨架)
- [PageHead 详情头](#3-pagehead-详情头)
- [Tabs 区](#4-tabs-区)
- [Body 主体](#5-body-主体)
- [DetailBlock 区块](#6-detailblock-区块)
- [操作位置](#7-操作位置)
- [布局与间距铁律](#8-布局与间距铁律)
- [状态](#9-状态)
- [响应与约束](#10-响应与约束)
- [推荐节点命名](#11-推荐节点命名)

## 1. 参考图的可复用信息

典型 B 端详情页(如客户详情、规则详情、策略详情)的稳定结构是:

1. 顶部"详情头"——对象身份 + 关键状态 + 主操作;
2. 可选 Tabs——切换关联维度(基本信息 / 变更记录 / 关联数据);
3. 主体"区块"——1..N 个 DetailBlock,每块一个主题;
4. 区块尾或右上角局部操作。

参考图中的业务名(所属项目、创建人、当前状态)只用于理解场景,不得成为默认输出。

## 2. 画板与主体骨架

详情页与列表页**同属整页原型**,沿用 qifu-list-page 的画板与外壳:

```text
Root (1366 × 768 | 1920 × 1080)
├── HeaderMenu(与 list-page 同 Header)
└── Workspace
    ├── SideMenu(与 list-page 同)
    └── Content(灰底)
        └── Page Surface(白底,距 Content 12px)
            └── Detail Page Shell(距 Page Surface 16px)
                ├── PageHead(详情头,固定 96px)
                ├── Tabs(可选,固定 44px)
                └── Body(flex,分块)
```

**规则**:

- 只复用 List Page Shell 的"外壳层"(Header/SideMenu/Content/Page Surface),**不复用**其 `pageHeaderSlot / filterBarSlot / tableSlot`;详情页有独立骨架命名 Detail Page Shell。
- 平台导航与 sidePath 解析规则完全沿用 [platform-yushu.md](../../shared/references/platform-yushu.md)。
- Shell 与 Page Surface 间距规则与 list-page 相同:Page Surface ↔ Content 12px,Shell ↔ Page Surface 16px。

## 3. PageHead 详情头

详情头是详情页**最不可省略**的部分,它回答"我是谁、我现在什么状态、我能干什么"。

固定高度 96px,三段布局:

```text
PageHead (Horizontal, 96px, padding 16 24, border-bottom 1px, bg #fff)
├── Left: 对象身份(Horizontal, gap 12)
│   ├── [可选 avatar / icon 48×48]
│   └── Meta(Vertical)
│       ├── Title row(Horizontal, gap 8)
│       │   ├── Name         20px / 700 / #111827
│       │   └── [0..2] Tags  Tag `light/{success,danger,info}/medium/square`
│       └── Sub row(Horizontal, gap 12)
│           ├── ID: <copyable>      12px / #6b7280
│           └── 更新时间: <datetime> 12px / #6b7280
├── Spacer
└── Right: 关键操作(Horizontal, gap 12)
    ├── [次要操作 1..2] Button base
    └── 主操作         Button primary
```

**铁律**:

- 详情头**只能放 1..2 个 Tag**,溢出挪到下方区块;不要把 N 个状态堆在标题旁。
- 主操作**唯一且必须可见**;不允许只放在 Tabs 内或 Body 底部。
- 次要操作包括:启用/停用、删除、复制(按业务取舍);编辑永远是主操作。
- `Readonly` 组合下,详情头无主次操作,仅返回/关闭。

## 4. Tabs 区

适用于 `Tabbed` / `Master Detail` 组合,高度 44px:

```text
Tabs (Horizontal, padding 0 24, border-bottom 1px, bg #fff)
└── Tabs 真实组件(type=line, size=medium)
    └── item=2..N, active=1
```

**铁律**:

- Tab 数 2..7 个;> 7 个必须重设计,把次要 Tab 收入"更多"。
- Tab 名:名词性 2-4 字短语:`基本信息 / 变更记录 / 关联客户 / 操作日志`;不写句子,不写疑问。
- 第一项永远是"基本信息"或同义;变更/日志类 Tab 放最后。
- `Flat` 组合不使用 Tabs。
- 切 Tab 不刷 PageHead——详情头对所有 Tab 保持可见,这是和"跳新页面"的关键区别。

## 5. Body 主体

Body 高度自适应,向下滚动(Page Surface 不滚,Detail Page Shell 内部滚)。

```text
Body (Vertical, padding 24, gap 16, scrollable)
└── DetailBlock × 1..N
```

### Flat / Tabbed 的 Body

- 单列通铺(最大宽度 = Page Surface - 32px)。
- DetailBlock 与 DetailBlock 之间间距固定 16px。
- 第一个 DetailBlock 永远是**核心信息块**(用于回答"这对象是谁、现在什么状态")。

### Master Detail 的 Body

- 左边固定 320px `EntityList`(可滚动)。
- 右边 padding-left 16px,空间自适应,同样用 DetailBlock 堆叠。
- 左边 List 选中某项,右边 Body 整体替换为该记录的详情;选中的 List 项有 Selected 状态。
- 左边 List 顶部有搜索框(Search 组件,`trigger=Icon`)。

## 6. DetailBlock 区块

DetailBlock 是详情页的最小信息单位,一个主题一块。

```text
DetailBlock (Vertical, bg #fff, border 1px, border-radius 8px)
├── BlockHeader (Horizontal, padding 16 20, border-bottom 1px #e5e7eb)
│   ├── Title          16px / 600 / #111827
│   └── [可选] BlockAction  尾操作(右对齐, Button base/text 或 link)
└── BlockBody (padding 20)
    └── 内容(描述列表 / 表格 / 卡片网格 / 时间线 / 嵌套子区块)
```

**铁律**:

- BlockTitle 名词性 2-6 字短语:`基本信息` / `账户信息` / `权限配置` / `变更记录`;不写"以下是 XXX 信息"。
- Block 出现顺序:`核心信息` → `业务详情` → `关联数据` → `操作历史`;**首块必须是核心信息**,不能一上来就放"历史版本"。
- BlockHeader 允许可选的尾操作(BlockAction),仅一件,不堆多个按钮。
- BlockBody 的 padding 固定 20px;**不允许再叠加自定义 padding**。

### BlockBody 允许的内容类型

由 [detail-block-map](detail-block-map.md) 决定;常见 6 种:

| 内容类型 | 控件 | 适用 |
| --- | --- | --- |
| 描述列表 | QFDescriptions / 自定义 Descriptions | 基本信息、字段值展示 |
| 表格(只读或轻操作) | Table Shell-V2 + TableContentCell | 变更记录、关联记录 |
| 卡片网格 | 简单 Card 网格 | 关联客户、子对象快照 |
| 时间线 | Timeline 组件 | 操作历史、状态流转 |
| 键值对大图(数字/指标) | Description + 大字号值 | 关键指标、汇总 |
| 嵌套子区块 | DetailBlock(无 header) | 复杂业务(少用,不超过 2 层) |

**禁止**:

- 在 DetailBlock 内放筛选栏——那是列表页的职责。Body 里嵌的"列表"是只读/轻操作的关联数据,不是"区块内的子列表页"。
- 在 DetailBlock 内放 Tabs——Tabs 已经在主体层级了;再嵌套就失了层级。

## 7. 操作位置

| 操作类型 | 位置 |
| --- | --- |
| 主操作(编辑/启用/停用) | PageHead 右侧 |
| 次要操作(复制/删除/导出) | PageHead 右侧主操作左侧 |
| 返回 / 关闭 | 仅 `Readonly` 组合,放 PageHead 最左(面包屑位) |
| 区块尾操作(新建子记录、查看全部) | DetailBlock 的 BlockHeader 右侧(BlockAction) |
| 行内操作(查看 / 编辑行) | DetailBlock 内 Table 的 Action Content-V2 |

**禁止**:

- 把编辑主操作放在 DetailBlock 内或 Body 底部——必须露出在 PageHead。
- 在 PageHead 同时出现 ≥ 3 个按钮。
- 行内操作使用抽屉未弹出式编辑,而不是直接跳走。

## 8. 布局与间距铁律

| 项 | 数值 | 说明 |
| --- | --- | --- |
| Page Surface ↔ Content | 12px | 与 list-page 一致 |
| Detail Page Shell ↔ Page Surface | 16px | 与 list-page 一致 |
| PageHead 高度 | 96px | |
| Tabs 高度 | 44px | |
| Body padding | 24px | 上下左右一致 |
| DetailBlock 间距 | 16px | |
| DetailBlock Header padding | 16 20px | |
| DetailBlock Body padding | 20px | |
| Description label 宽 | 120px | |
| Description column 数 | 2 或 3 | 不随意设 |

**铁律**:所有留白从这 10 项取;不在 Detail Page Shell、PageHead、Tabs、Body、DetailBlock 上叠加自定义 padding/margin。

## 9. 状态

一个详情页默认只展示一种状态;通过 `DetailSpec.defaultState` 指定。

| 状态 | 处理 |
| --- | --- |
| Data | 已有数据,可正常渲染;默认 |
| Loading | 首次打开,骨架屏;PageHead、Tabs 不隐藏,Body 显示 Skeleton |
| Error | 加载失败;PageHead 保留,Body 显示 `Empty status=Failed` + "重新加载" |
| Disabled | 无权限,PageHead 保留但操作禁用,Body 显示 `Empty status=NoPermission` |

**禁止**:

- 在同一详情页同时展示两种状态(如 Loading + Data 并存)。
- 当对象不存在(404 类)时,仍使用 Error 状态文案说明"记录不存在或已被删除"。

## 10. 响应与约束

- 画板默认 `1366 × 768`;宽屏可选 `1920 × 1080`,需手动重新分配列宽。
- Tabs 数 ≥ 6 时,不强求塞下;用"更多 + 下拉"收纳次要 Tab,并保持首 Tab 可见。
- DetailBlock 中 Description 默认 2 或 3 列;长文本类标签单独占 FULL 行。
- Master Detail 左 320px 固定,不随 viewport 拉宽;右 Body 内的 DetailBlock 数量、宽度自适应。

## 11. 推荐节点命名

```text
Page / Detail / <Object> / <compositionName>
├── Header / Global
├── Workspace
│   ├── Navigation / Side
│   └── Content
│       └── Page Surface
│           └── Detail Page Shell
│               ├── PageHead
│               │   ├── ObjectIdentity (Name + Tags + ID + 更新时间)
│               │   └── HeadActions (Main + Secondary)
│               ├── Tabs (可选)
│               ├── Body
│               │   └── DetailBlock / <blockName> × N
│               │       ├── BlockHeader (Title + BlockAction)
│               │       └── BlockBody (Descriptions / Table / Timeline / Cards)
│               └── Audit / Missing Components(仅有缺口时)
```
