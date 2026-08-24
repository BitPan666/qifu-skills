# 智客星列表页规则

## 1. 画板骨架

唯一标准画板为 `1366 x 768`：

```text
Header / Global: 1366 x 48
Workspace: 1366 x 720, y=48
Navigation / Side: 200 x 720
Content: 1166 x 720, x=200
Page Surface: 1142 x 696, x=12, y=12
List Page Shell-V2: 1110 wide, x=16, y=16
```

Content 使用现有灰色背景变量，Page Surface 使用现有白色 surface 变量。不得用固定色值替代模板既有变量绑定。

## 2. 筛选区

标准为按钮触发的两行筛选：

- 第一行 4 个带标题筛选项，行高 32px；每项总宽 265.25px，标题 70px，控件约 195px，项间 12px。
- 第二行在第一项放日期或日期范围筛选；日期项标题宽按文本 Hug，默认控件宽 240px。
- `确定` 和 `重置` 位于第二行右侧，均为 32px；确定为主按钮，重置为线框按钮。
- 筛选栏高度 76px。筛选栏底部到列表操作栏顶部固定 16px。

筛选数量不是 4+1 时，不能在当前模板新增或删除 Slot 内容；按入口文件规则寻找匹配模板或阻塞。

## 3. 列表操作栏

列表操作栏高 32px：

- 左侧为批量或业务次要操作，按钮间距 8px。
- 右侧只保留一个视觉最强的主操作，使用“动词 + 对象”文案。
- 操作栏至表格固定 12px。
- 批量按钮不自动决定表格多选；仅 `tableSelection=true` 使用此基线。

## 4. 表格与分页

当前标准为 `selectable / 44px / bordered`：

- 表头与数据行均为 44px。
- 可见列宽数组为 `[48, 80, 160, 160, 90, 90, 120, 100, 100, 160]`，可见内容宽 1108px；表格外壳宽 1110px。
- 表头与所有数据行必须复用同一列宽数组；不可用 `SPACE_BETWEEN` 制造列间空白。
- 默认 Data 状态展示 8 行，最少 5 行、最多 8 行；名称、状态、操作文案需要有差异，不使用真实个人敏感信息。
- 状态一律使用真实 Tag：`variant=light`、`size=medium`、`shape=square`、`disabled=false`、`Show icon=false`、`Show closeBtn=false`。
- Pagination 位于 Table Shell 的既有分页区域，高 56px；其可见右边缘与表格右边缘对齐。

## 5. 命名

```text
Page / List / <pageName> / Default
Header / Global
Workspace
Navigation / Side
Content
Page Surface
Templates / List Page Shell-V2 / <pageName>
Filter Bar / <pageName> / 按钮触发
Data Region / <pageName>
List Action Bar / <pageName>
Table Shell / <pageName> / Selectable
Pagination Bar / <pageName>
```
