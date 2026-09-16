# 验证与交付

## 1. 模型检查

- YAML 可解析，`schemaVersion`、flow、platform、entity、fields、views、transitions 存在。
- 字段、view 和 transition key 无重复。
- view、section 和数据表只引用根级 fields。
- transition 来源 view、动作和目标关系有效。
- `confirmed`、`recommended`、`TBD` 没有被升级或混写。
- assumptions 和 tbd 集中维护，不散落成确定规则。

## 2. 字段一致性

逐个 view 比较：

```text
BusinessFlowSpec fields
→ 派生页面 Spec 字段
→ Figma 可见标签/列/控件
```

允许页面增加布局和显示规则，不允许缺失必填字段、擅自新增业务字段或改变业务含义。背景列表中的字段不能误判为抽屉字段；检查抽屉或内容区自身的边界。

## 3. 页面结构

- 每个正式状态只有一个顶层 Frame，尺寸与平台或用户要求一致。
- 已验证页面没有被重新生成或覆盖。
- 核心控件是 `INSTANCE`，存在 `mainComponent`，并位于正确容器。
- 没有分离实例、孤儿节点、重复节点、截图页面、文字覆盖层或手绘核心控件。
- 页面只引用当前平台 Adapter、变量和组件。
- 页面级文字使用组件库已有本地 Text Style；组件内部文字继承母版，不以页面级未绑定检查误判。

## 4. Prototype

- confirmed transition 数量与 Prototype 逻辑路由数量一致。
- 多个关闭触发点可以共享一条逻辑路由，需同时报告逻辑路由数和点击目标数。
- 每个来源节点的 reaction 能回读到预期 destination。
- recommended、TBD 和仅保留入口的动作没有连线。
- transient overlay 使用真实组件实例，且不计入页面状态数。
- 返回规则的 `effect` 在交付中明确说明；静态 Prototype 不冒充真实数据刷新或状态持久化。

## 5. 视觉检查

逐个正式状态和关键 transient 状态导出截图，检查：

- 页面完整、无裁切、无异常空白；
- 平台外壳、Logo、导航和品牌色正确；
- 抽屉遮罩、位置和宽度正确；
- 菜单靠近触发操作且不越界；
- 文字无截断，控件没有重叠；
- 页面之间的业务对象、状态和测试数据一致。

结构检查通过但未截图时，输出 `VISUAL_CHECK_REQUIRED`，不得写 `VISUAL_PASS`。

## 6. 交付报告

```text
BUSINESS_FLOW_SPEC: PASS | FAIL
FIELD_CONSISTENCY: PASS | FAIL
PAGE_REGISTRY: <页面清单>
COMPONENT_CHECK: PASS | FAIL
PROTOTYPE_CHECK: PASS | PARTIAL | FAIL
VISUAL_CHECK: PASS | FAIL | NOT_CHECKED
PENDING_SKILLS: <列表>
UNIMPLEMENTED_ENTRIES: <入口与原因>
GOLDEN_SAMPLE_UPDATED: NO，除非用户明确验收
```
