# 页面编排规则

## 职责分离

`qifu-business-flow` 管理跨页面语义和连接；页面 Skill 管理单页结构和视觉。

| 能力 | 所有者 |
| --- | --- |
| 业务字段、view、transition、返回效果 | BusinessFlowSpec |
| 列表筛选、列、分页、列表操作 | `qifu-list-page` |
| 新建、编辑、只读、数据详情抽屉 | `qifu-drawer-form` |
| 独立详情页面 | `qifu-detail-page` |
| 平台导航、主题和组件映射 | `qifu-shared` |
| 页面复用、状态清单、路由和 Prototype | `qifu-business-flow` |

不得把页面 Skill 的布局规则复制进本 Skill，也不得把单个业务案例字段写入任何通用 Skill。

## 复用优先

每个 view 按以下顺序处理：

1. 用户明确绑定并已验证的 Frame；
2. 目标 Page 内名称、平台、业务对象和状态一致的已验证 Frame；
3. 对应页面 Skill 新生成的 Frame；
4. 页面 Skill 缺失时标记 `pending-skill`。

复用检查至少包含：平台、Frame 尺寸、页面状态、字段、动作、真实实例、文本样式、溢出和截图。只凭节点名称相似不得复用。

## 页面登记

执行时维护 PageRegistry：

```yaml
<viewKey>:
  nodeId: <Frame ID>
  nodeName: <Frame 名称>
  implementationSkill: <页面 Skill>
  origin: reused | generated
  structureStatus: PASS | FAIL | BLOCKED
  visualStatus: PASS | FAIL | NOT_CHECKED
```

只有正式 view 进入 PageRegistry。菜单等瞬时状态进入 `transientStates`。

## Prototype 映射

- `confirmed-only` 是默认策略。
- `action` 对应一个触发点；`actions` 可以对应多个触发点，但仍是一条逻辑 transition。
- `presentation=drawer|page` 通常映射为 `NAVIGATE`。
- `presentation=overlayMenu` 映射为 `OVERLAY`，目标必须是真实菜单组件所在 Frame。
- `presentation=closeDrawer` 返回来源列表或 Spec 指定目标。
- `effect` 是业务语义，不自动转换为 Figma 数据操作。
- Prototype 起点使用链路的首个 list 或 BusinessFlowSpec 明确的起点，不覆盖 Page 内无关起点。

建立连线前必须找到来源点击节点和目标 Frame。缺失时返回 `PROTOTYPE_TARGET_MISSING`，不得把整行、整页或无关父容器设为替代点击热区。

## 平台锁定

页面链路只能使用 `platform.key` 对应的 Adapter。每个复用和生成页面都要扫描 Logo、导航、组件名和变量引用；发现其他平台引用时返回 `COMPONENT_INTEGRITY_FAIL`。`fallbackPlatform` 默认为 forbidden。

## Candidate 与 Golden Sample

业务链路画板默认命名为 Candidate。自动结构和截图验证通过，只能说明该次链路可用；没有用户明确视觉验收，不得升级页面或模板为 Golden Sample。
