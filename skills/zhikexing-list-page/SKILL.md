---
name: zhikexing-list-page
description: Use when creating or auditing a standard Zhikexing desktop list page in the Qifu Figma component-library file from a business description, fields, or a verified Zhikexing list template. Do not use for dashboards, forms, detail pages, or a list whose structure differs from an approved template.
---

# Zhikexing List Page

基于已人工确认的智客星列表页模板，生成可编辑的 1366 桌面端列表页。保留真实组件实例和已有 Slot 内容关系；不把模板截图当成页面，不分离实例，也不写入 Figma Connector 当前不支持的 Slot 属性。

## 读取路由

每次完整读取：

- [页面规则](references/page-rules.md)：1366 画板、筛选、操作栏、表格和分页规则。
- [智客星平台基线](references/platform-zhikexing.md)：顶部栏、侧栏、菜单状态和变量使用。
- [组件映射](references/component-map.md)：模板中的真实组件与可安全修改的范围。
- [调用契约](references/component-invocation-contract.md)：复制模板、属性回读和 Slot 边界。
- [结构化验收](references/structural-validation.md)：模板关系、几何和截图门禁。

同时读取根目录 `VERSION`。调用 Figma 前加载并遵循 `figma-use`；创建或更新完整页面时同时加载 `figma-generate-design`。业务提示词首句必须显式调用 `@figma` 插件。

## 固定基线

当前唯一基线位于奇富组件库文件 `gTV3VdC6a5e9vpkRHIZSXA`：

```text
Template / List Page / 智客星 / 1440 / 手动调整
node: 4892:34812
实际尺寸: 1366 x 768
```

名称中的 `1440` 是历史命名，不得据此改变画板宽度。后续新页面均按实际 `1366 x 768` 创建；模板重命名由人工单独处理，不在生成任务中改动。

## PageSpec 输入

接受自然语言、字段清单、截图或线框，提取：

```text
pageName / pageTitle
targetPage / insertPosition
sidePath[] / sideActive / sideExpanded[]
filters[]: field, control, placeholder, defaultValue
filterTrigger=按钮触发
listActions.left[] / primaryAction
columns[] / rowActions[] / status
tableSelection=true|false
pagination / data
```

当前模板对应 `Zhikexing List / Filtered Selectable Table / 1366`：4 个首行筛选、1 个第二行日期筛选、按钮触发、左侧批量操作、右侧单一主操作、可选择表格和分页。

当 PageSpec 的筛选数量、是否多选、列数、表格密度或状态与该模板不同，先寻找同文件中已人工确认的匹配智客星模板；找不到时停止并报告 `BLOCKED_TEMPLATE`。不得为满足业务字段改写 Slot、手绘表格或临时拼装另一套页面。

## 工作流

1. 读取基线模板，确认实际为 `1366 x 768`，并检查 Header、SideNavigation、List Page Shell、Filter Bar、Table Shell 和 Pagination 都存在。
2. 解析 PageSpec。`sidePath` 只控制左侧菜单；页面标题、筛选、列表操作、表格列、行操作和分页互不推断。
3. 在用户指定 Page 的空白区域复制**整个基线顶层 Frame**，命名为 `Page / List / <pageName> / Default`。不覆盖、移动或改名基线模板。
4. 只修改复制页中可回读成功的文字、布尔、变体与 INSTANCE_SWAP 属性；每次遵循“读取真实 Key -> 校验类型 -> 写入 -> 回读”。
5. 禁止直接写入 `pageHeaderSlot`、`filterBarSlot`、`tableSlot`、`controlSlot`、`headerSlot`、`rowsSlot`、`cellsSlot`、`contentSlot` 或 `paginationSlot`。当前 Connector 对这些写入失败时，复制后的既有内容仍保持有效。
6. 需要变更 Slot 内结构时，标记 `BLOCKED_TEMPLATE`，说明缺少哪一种人工模板；不以裸 Text、Frame、Group、覆盖层或截图补齐。
7. 按结构化验收和截图检查通过后交付；失败则明确返回 `FAIL` 或 `BLOCKED_TEMPLATE`，不得称为完成。

## 硬性约束

- 不跨平台套用毓数、金毓盟或电销的菜单、颜色和 Header 规则。
- 不分离组件实例，不破坏变量或文本样式绑定。
- 页面只允许一个当前叶子菜单；仅其祖先可以展开。
- 所有状态使用真实 Tag，统一 `light / semantic theme / medium / square`，不带图标和关闭按钮。
- 表格列宽在表头与所有行保持一致；分页位于表格内的既有分页区域并右对齐。
- 不在模板内或其附近删除人工 Golden Sample。

## 交付

返回：Skill 版本、模板节点、生成页节点、PageSpec 假设、修改过的组件实例、属性回读摘要、结构状态、截图状态，以及 `BLOCKED_TEMPLATE` 或组件缺口（如有）。
