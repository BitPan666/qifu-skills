# BusinessFlowSpec 契约

BusinessFlowSpec 是一条业务链路的唯一业务语义来源。页面 Spec 和 Figma 页面引用它，不反向复制或改写字段定义。

## 最小结构

```yaml
schemaVersion: "1.0"

flow:
  id: <稳定 key>
  name: <业务链路名称>

platform:
  key: <平台注册 key>
  name: <平台名称>
  adapter: skills/qifu-shared/references/platform-<key>.md
  sourceStatus: confirmed | recommended | TBD

navigation: {}

entity:
  key: <实体 key>
  name: <实体名称>
  idField: <fields 中存在的 key>
  titleField: <fields 中存在的 key>

fields:
  - key: <唯一字段 key>
    label: <业务名称>
    type: <业务类型>
    sourceStatus: confirmed | recommended | TBD
    source: <证据来源>
    visibleIn: [<viewKey>]

views:
  <viewKey>:
    type: list | drawer | page
    title: <页面标题>
    fields: [<根级字段 key>]
    actions:
      - key: <动作 key>
        sourceStatus: confirmed | recommended | TBD

transitions:
  - id: <唯一 transition id>
    from: <viewKey>
    action: <动作 key>
    to: <viewKey 或瞬时状态 key>
    presentation: page | drawer | closeDrawer | overlayMenu
    effect: <可选业务效果>
    sourceStatus: confirmed | recommended | TBD
    source: <证据来源>

assumptions: []
tbd: []
```

## 引用规则

- `fields[].key`、`views` 和 `transitions[].id` 各自唯一。
- `entity.idField`、`entity.titleField` 和可选的 `statusField` 必须存在于根级 `fields`。
- `views.<key>.fields`、`sections[].fields`、`dataTable.columns` 只能引用根级字段 key。
- 页面 Spec 可以增加 display、宽度、对齐或 overflow 规则，但不得重新定义字段 label、type 或业务枚举。
- `transitions.from` 必须是正式 view。
- `transitions.to` 应是正式 view；`presentation=overlayMenu` 时允许使用瞬时状态 key。
- `action` 与 `actions` 二选一。`actions` 用于多个触发点共享一条业务语义。
- `close` 允许作为页面外壳动作，不要求重复登记到 view actions。

## 来源状态

- `confirmed`：有用户明确要求、业务文档、参考图或已验收页面证据。
- `recommended`：为保证训练或演示完整性提出的建议，不作为正式业务规则。
- `TBD`：缺少证据，入口可以保留，但不得生成目标页面或正式交互。

任意派生 Spec、FlowPlan 和 Prototype 必须保留来源状态。禁止因页面已经画出或技术上可以实现，就把 `recommended`、`TBD` 提升为 `confirmed`。

## 页面与 transient 状态

`views` 只登记需要独立验证的正式页面状态。菜单、Popover、Tooltip 等瞬时状态可由 confirmed transition 的 `presentation` 表达，并在 FlowPlan 的 `transientStates` 中登记，不必伪装成正式页面。

## 校验命令

```bash
python3 scripts/build_flow_plan.py <business-model.yaml>
```

校验失败统一返回 `INVALID_BUSINESS_FLOW_SPEC`，并逐项指出字段或路由位置。
