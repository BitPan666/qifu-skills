# 数据详情抽屉 Golden Sample

## 适用范围

用于右侧数据详情抽屉：顶部展示对象摘要，下方以筛选控件和内嵌表格展示明细。稳定组合名称：

`Qifu Drawer Form / Data Detail with Table`

唯一 Golden Sample：组件库文件 `gTV3VdC6a5e9vpkRHIZSXA`，Page `3932:405` 的 `Golden Sample / Drawer / 数据详情 / 680 · 0821 根据手搓重生成`（node `4725:1548`）。该 Frame 是未来数据详情抽屉的唯一结构、组件关系和视觉基线；旧的 `4659:420` 仅保留为历史对照，不再作为生成来源。参考其信息层级和节奏，不复制固定业务文案。

本 Golden Sample 的 Scene 固定为 `1366 × 768`。其底图必须是完整、可编辑的真实列表页，当前验证来源为 `Template / List Page / 智客星 / 1440 / 手动调整`（node `4892:34812`，实际尺寸 `1366 × 768`）；禁止使用截图、IMAGE 填充矩形、导出图片或展平底图替代。

## 组件覆盖

必须先在同文件按精确名称解析，并保留 `mainComponent`：

- `Icon/basic/close`
- `Data Display / Tag / Tag`
- `录入组件 / Select / Base`
- `Data Display / Table / Shell-V2`
- `Data Display / Table / Header Cell-V2`
- `Data Display / Table / Row-V2`
- `Data Display / Table / Content Cell-V2`
- `Data Display / Table / Cell Content / Text-V2`
- `Navigation / Pagination / Pagination-V2`

缺失时返回 `COMPONENT_MISSING` 并停止对应区域，不自绘近似组件。页面级 Auto Layout、Section 容器、3×12 标题 rail 和 Table Border 属于组合结构，不冒充组件库母版。

## 结构

```text
Golden Sample / Drawer / <Object> / 680
├── Background / List Page                    1366×768，完整真实列表页副本
│   ├── Header / Global
│   └── Workspace / Navigation + Content Shell
├── Overlay Mask                              1366×768，位于底图之上
└── Drawer / <Object>                         680px，right=0
    ├── Drawer / Header                      680×56
    │   ├── Title                            x=24，标题/Medium
    │   └── INSTANCE / Icon/basic/close      16×16，right=24
    └── Drawer / Body                        padding=16，Vertical
        └── Content Stack                    width=648，gap=16，Vertical
            ├── Section / Summary            padding=20 24，gap=16
            │   ├── Section Heading Row      Horizontal
            │   │   ├── Heading Group        rail 3×12 + 标题/Small，gap=5
            │   │   └── Tag                  与 Heading Group gap=8
            │   └── Body/Regular
            └── Section / Detail             padding=20 24，gap=16
                ├── Section Heading Row      rail 3×12 + 标题/Small
                ├── Form Row                 label + Select，gap=24
                └── Table Region             Vertical
                    ├── Table Border          仅表头+数据行
                    └── Pagination-V2         描边外，右对齐
```

所有结构容器使用 Auto Layout；仅 `1366×768` Scene、完整列表页底图、遮罩与右侧抽屉定位允许绝对坐标。底图不是 Slot 覆盖物，也不是静态矩形；应复制完整列表页 Frame，使 Header、侧栏、List Page Shell、Filter Bar、Table Shell 与 Pagination 仍保留真实组件实例。

## 尺寸与文本

- Drawer 宽 680；Header 高 56；Body 内容距抽屉四周 16px。
- 内容卡片宽 648px，圆角 4；上下 padding 20px、左右 24px；卡片间 gap 16px。
- 标题 rail 为 3×12，使用品牌色变量；rail 与标题 gap 5px；标题后 Tag gap 绑定 `--qifu-size/8`。
- Form label 与控件默认 gap 24px；内嵌表格使用 small 36px，表格和分页器不得超过卡片 600px 内容宽。
- Header Title 使用 `标题/Medium` 16/24；Section Title 使用 `标题/Small` 14/22；普通正文和 Form label 使用 `Body/Regular` 14/22。
- 表格正文通过 `Text-V2 / contentFont 内容字号=14px` 实例继承 `Body/Regular`；表头、链接与组件内部文字维持各自语义样式。

## 表格与分页

1. Table Shell-V2 使用 `small 小 36px / bordered 边框线 / selection off 隐藏`。
2. Header Cell-V2、Row-V2、Content Cell-V2 逐层同步 small + both divider；表头 `showSort=false`、`showFilter=false`，除非业务明确要求。
3. `Table Border / 四边完整` 是单独页面级 Frame：圆角 4、1px Inside 描边、`Clip content=true`。
4. Table Border 只包围表头与数据行。Pagination-V2 位于其下方、边框之外并右对齐；页面仅保留一个可见分页器。
5. 非 Empty / Loading 状态下，每个可见数据行的每个可见单元格必须有真实内容；表头与数据行列宽逐列一致。
6. 本 Golden Sample 的六列表格宽度为 `114 + 114 + 95 + 95 + 95 + 87 = 600px`。

## QA

- Golden Sample Scene 精确为 `1366×768`；图层顺序固定为 `Background / List Page < Overlay Mask < Drawer`，Drawer 宽 680 且 `x=686`、right=0。
- Background 必须是完整真实列表页副本；不得出现 `IMAGE` 填充的 `底图`、截图、导出图片、展平矩形或裸 Text 作为整页底图。当前基线应能追溯到 `4892:34812` 或用户明确指定并通过同等结构检查的现有列表页。
- Background 内的 Header、侧栏、List Page Shell、Filter Bar、Table Shell 与 Pagination 必须继续是可解析组件实例；对底图仅允许替换业务文案和既有组件的合法属性，不得 detach 或手绘覆盖。
- 页面级自由文本应用组件库 Text Style；Header 只有 Title + `Icon/basic/close`；两张内容卡片均在 Body 16px 安全边距内。
- 表格所有可见单元格为真实组件实例，表头和行列宽一致；Pagination 位于 Table Border 外。
- 新建页面组合层必须使用整数几何。正式组件实例内部 Vector、Text、Slot 或母版 Auto Layout 的分数值不做页面层修正，不得为凑整数 detach 或改写母版。
- 无孤儿实例、无重复节点、无文字截断、无越界。
