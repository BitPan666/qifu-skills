# 智客星列表页调用契约

## 1. 复制优先

先复制整个已审批模板顶层 Frame，再在复制页内修改。复制后必须保留以下核心实例：

```text
List Page Shell-V2
Filter Bar-V2
Table Shell-V2
Pagination-V2
SideMenuItem instances
```

## 2. 属性闭环

对每个拟改实例：

1. 读取 `componentProperties`；
2. 从逻辑名称动态解析唯一真实 Key；
3. 校验 `expectedType=TEXT|BOOLEAN|VARIANT|INSTANCE_SWAP`；
4. 写入并立即回读；
5. 回读不一致时返回 `PROPERTY_READBACK_MISMATCH`。

不把当前出现的 `Label#...`、`text#...` 等内部后缀写死进 Skill。

## 3. Slot 边界

以下均为不可直接写入的 Slot：`pageHeaderSlot`、`filterBarSlot`、`tableSlot`、`controlSlot`、`headerSlot`、`rowsSlot`、`cellsSlot`、`contentSlot`、`paginationSlot`。

Connector 返回 `Slot component property values cannot be edited`、`Cannot move node. New parent is an instance or is inside of an instance` 或等效错误时，记录 `SLOT_WRITE_FAILED`。当前 Skill 的合法处理是保持复制模板原有 Slot 内容，或请求相同结构的人工模板；不得手绘替代。

## 4. 失败分类

| 代码 | 处理 |
| --- | --- |
| `PROPERTY_NOT_FOUND` | 停止该属性改写，报告候选属性。 |
| `PROPERTY_WRITE_FAILED` | 停止并保留实例 ID。 |
| `PROPERTY_READBACK_MISMATCH` | 停止，不以视觉近似代替。 |
| `INSTANCE_SWAP_FAILED` | 停止，不绘制替代图标。 |
| `SLOT_WRITE_FAILED` | 使用完整模板复制流程；若结构需要改变则 `BLOCKED_TEMPLATE`。 |
| `BLOCKED_TEMPLATE` | 请求用户提供或人工创建匹配结构的模板。 |

只有 `COMPONENT_MISSING` 才可以记录为组件缺口；Slot、权限、字体和属性写入问题不属于组件缺口。
