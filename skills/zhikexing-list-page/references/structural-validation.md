# 智客星列表页结构化验收

## 1. 模板关系

- 根画板为 `1366 x 768`，且由人工基线 `4892:34812` 的顶层 Frame 复制而来。
- Header=48px，Workspace=720px，SideNavigation=200px，Content=1166px。
- Page Surface 在 Content 内 `x=12, y=12, w=1142, h=696`；Shell 在 Surface 内 `x=16, y=16, w=1110`。
- 必须可见 1 个 List Page Shell-V2、1 个 Filter Bar-V2、1 个 Table Shell-V2、1 个 Pagination-V2。

## 2. 筛选与操作

- `Filter / <field>` 可见数量为 5；首行 4 个、第二行 1 个。
- Filter Bar=76px，所有控件=32px，确定和重置各 1 个。
- 筛选栏到 List Action Bar=16px；List Action Bar 到 Table Shell=12px。
- List Action Bar 只存在一个主操作，且位于最右侧。

## 3. 表格

- Table Shell 为 selectable、44px、bordered；Header Selection Cell 根背景继承模板的 canvas 变量。
- 表头总列数=10，数据行可见列数=10，表头和每行使用同一列宽数组。
- 可见数据行 5-8 行；所有行使用真实 Row/Cell/Text/Action/Tag 实例。
- 所有状态 Tag 均为 `light / semantic theme / medium / square`，且无图标、无关闭按钮。
- Pagination 在 Table Shell 内，紧贴最后一行，右缘与表格右缘一致。

## 4. 禁止特征

以下任一出现则 `FAIL`：

```text
Navigation Text Overlay
Control Text Cover
Button Text Cover
Table / Clean
隐藏真实 Shell 后展示手绘表格
用裸 Text 或矩形覆盖组件默认文案
拆分组件实例
```

## 5. 状态

```text
structuralValidation PASS|BLOCKED_TEMPLATE|FAIL
```

只有结构和截图都通过时才为 `PASS`。截图检查必须覆盖：唯一当前菜单、品牌色图标、文字无截断、列对齐、Tag 样式、分页右对齐、无异常空白和无画板溢出。
