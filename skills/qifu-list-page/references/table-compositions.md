# 表格组合注册表

## 目的

用稳定名称描述列表页中 `List Page Shell-V2 + Filter Bar-V2 + 可选 List Action Bar + Table Shell-V2` 的结构组合。后续调用必须使用下表中的完整 `compositionName`；这些名称属于 Skill 的调用协议，不是 Figma 组件母版名称。

## 已注册组合

| `compositionName` | 适用场景 | Filter Bar | List Action Bar | Table Shell | `rowsSlot` | Pagination |
| --- | --- | --- | --- | --- | --- | --- |
| `Qifu List Page / Basic Table` | 无筛选条件的普通数据列表 | 隐藏 | 按 `listActions` 显示 | `selection=off` | 数据行 | 默认显示 |
| `Qifu List Page / Basic Filter Table` | 1–4 个常用筛选条件的标准列表；默认组合 | 显示，`expanded=false` | 按 `listActions` 显示 | `selection=off` | 数据行 | 默认显示 |
| `Qifu List Page / Advanced Filter Table` | 5 个以上筛选条件，或明确要求“更多筛选” | 显示，`expanded=true` | 按 `listActions` 显示 | `selection=off` | 数据行 | 默认显示 |
| `Qifu List Page / Selectable Filter Table` | 需要行选择或批量操作的筛选列表 | 显示；1–4 项时单行，更多时两行 | 批量动作存在时显示 | `selection=on` | 数据行 | 默认显示 |
| `Qifu List Page / Loading Table` | 首次加载或刷新中的列表状态 | 按当前筛选需求显示或隐藏 | 默认隐藏，明确要求时显示 | `selection=off` | Loading 实例 | 隐藏 |
| `Qifu List Page / Empty Table` | 无数据、无结果、无权限或加载失败状态 | 按当前筛选需求显示或隐藏 | 默认隐藏，明确要求时显示 | `selection=off` | Empty 实例及对应 `status` | 隐藏 |

## 调用规则

1. 用户给出完整 `compositionName` 时精确匹配，大小写、空格和斜杠保持一致。
2. 用户未给名称时按以下优先级选择：Loading/Empty 状态 → 需要选择或批量操作 → 5 个以上筛选条件 → 1–4 个筛选条件 → 无筛选条件。
3. 未指定且无法区分时使用 `Qifu List Page / Basic Filter Table`。
4. 组合名称只决定稳定结构；业务字段、文案、列数、数据、`listActions`、表格 `size/type` 和分页总数继续来自 `PageSpec`。增加或删除操作栏不创建新的 `compositionName`。
5. 不把业务对象、页面名称、状态文案或视觉尺寸拼进 `compositionName`，也不创建 `Simple`、`Normal`、`Default` 等未注册别名。
6. 新场景无法由现有组合表达时，先使用最接近的已注册组合并记录缺口。只有用户确认需要形成长期复用结构后，才新增组合名称并同步本注册表、`SKILL.md` 和验证规则。

## 解析结果

每次调用在内部形成以下结构，并在交付时回报 `compositionName`：

```text
compositionName
showFilterBar
filterBarExpanded
showListActionBar
tableSelection
rowsState
showPagination
```

不得以重命名 Figma 组件的方式实现上述协议。真实组件仍按[组件映射](../../qifu-shared/references/component-map.md)中的正式名称解析。
