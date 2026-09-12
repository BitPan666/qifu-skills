# Component Contract：AI 组件注册与调用契约

## 1. 组件记录格式

`qifu-shared/references/component-map.md` 中的每个正式组件建议具备以下字段：

```yaml
component:
  semanticName: Select
  category: input
  componentSet: 录入组件 / Select / Base
  nodeId: 2859:2820
  publishedKey: 1684c11d727996e0a41ebee921cf15444e395d8d
  sourceFileKey: gTV3VdC6a5e9vpkRHIZSXA
  status: stable | experimental | deprecated | missing
  supports: [filter, form, inline-edit]
  properties:
    - name: mode
      values: [single, multiple]
    - name: size
      values: [SM, MD, LG]
    - name: state
      values: [default, hover, focus, disabled, error]
  slots: [prefix, clear, search, suffix, tag]
  constraints:
    height: 32
    widths: [200, 304, 408, FULL]
  fallback: null
  fallbackAuthorized: false
  lastVerified: 2026-07-29
```

字段不确定时写 `unknown`，不要编造属性名。

## 2. AI 发现顺序

1. 语义类别：navigation / input / feedback / data / overlay / layout；
2. 组件集精确名称；
3. 使用场景与允许的 Pattern；
4. 变体属性与状态；
5. 节点 ID 或发布 Key；
6. 缺口与合法降级。

搜索不到时，按以下顺序处理：

```text
精确组件集 → 同语义组件 → 组合现有组件 → 记录 Missing Components
```

只有共享调用基线确认 `COMPONENT_MISSING`，并且用户明确允许当前交付降级时，才在记录缺口后创建 `Fallback / <capability>`。属性、权限、字体、导入、Slot 或工具失败都必须停止，不得沿这条路径降级。

## 3. 创建约束

- 同组件库文件：优先通过节点 ID 创建实例；
- 跨文件：优先使用发布 Key 导入实例；
- 不分离实例、不改主组件、不手绘替代已有能力；
- 文案、图标、数据可通过公开属性或实例覆盖修改；
- 组合节点使用 `Pattern / <name>`，降级节点使用 `Fallback / <capability>`；
- 所有正式组件在交付前必须可回答“它来自哪个组件集、哪个节点或发布 Key”。

## 4. 状态、属性与缺口

每个调用至少确定：

- `variant`：视觉/结构变体；
- `state`：default / hover / focus / selected / disabled / loading / error / empty；
- `size`：SM / MD / LG 或组件库登记的尺寸；
- `content`：显示文案和数据；
- `permission`：用户是否可操作；
- `fallback`：能力不存在时的候选降级方案；默认只记录建议。
- `fallbackAuthorized`：用户是否明确允许在当前交付中创建该降级，默认 `false`。

缺口审计格式：

```yaml
missingComponent:
  capability: Range date filter
  scenario: 订单列表筛选
  currentFallback: 两个 DatePicker + 页面级连接符
  desiredComponent: DateRangePicker / Base
  suggestedProperties: [value, startPlaceholder, endPlaceholder, state]
  priority: P1
```
