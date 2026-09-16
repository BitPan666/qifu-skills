---
name: qifu-business-flow
description: 用于把新的奇富后台多页面业务需求整理为 BusinessFlowSpec，并编排列表、抽屉、详情页复用或生成、字段一致性检查和已确认的 Figma Prototype。单页设计请直接使用对应页面 Skill。
---

# Qifu Business Flow

把一条跨列表、抽屉、详情或其他页面状态的业务需求，转换为可验证、可复用的业务模型与 Figma 页面链路。本 Skill 只负责编排，不复制页面 Skill 的字段规则、组件映射、平台样式或页面蓝图。

## 使用边界

使用本 Skill：

- 用户描述的是两个及以上页面状态及其跳转关系；
- 需要先建立或更新 `BusinessFlowSpec`；
- 需要复用现有页面，并只补齐缺失状态；
- 需要检查字段、动作、返回规则和 Prototype 是否一致。

以下情况不要使用：

- 单独生成列表、表单抽屉或详情页：直接调用对应页面 Skill；
- 只做视觉修正：直接编辑指定节点；
- 用户尚未确认页面关系，只需要讨论方案：先输出草案，不写 Figma。

## 必读资料

每次完整读取：

- [BusinessFlowSpec 契约](references/business-flow-spec.md)：字段、视图、状态、路由和来源状态。
- [页面编排规则](references/orchestration.md)：页面 Skill 委派、复用优先、Prototype 映射和失败关闭。
- [验证与交付](references/validation.md)：模型、字段、节点、组件、Prototype 和视觉验收。
- `../qifu-shared/references/page-context.md`：平台、目标 Figma、Page 和权限上下文。

只读取当前平台对应的唯一 Adapter。用户明确平台时禁止读取或回退到其他平台。需要创建或修改 Figma 时，先加载 `figma-use`；生成完整页面时同时加载 `figma-generate-design`。

## 输入契约

接受自然语言或已有模型。结构化输入优先使用：

```yaml
businessModelPath: <BusinessFlowSpec YAML 路径>
targetFigma: <文件或节点链接>
targetPage: <Page 名称或节点 ID>
placement: <空白处或参考节点旁>
reusePolicy: reuse-first
prototypePolicy: confirmed-only
pageBindings:
  <viewKey>: <已验证 Frame 节点 ID，可选>
```

自然语言输入至少提取：平台、业务对象、页面状态、入口动作、目标状态、关闭/提交后的返回规则，以及明确不实现的入口。缺失内容不得靠常识补成 `confirmed`。

## 工作流

### 1. 建立业务模型

1. 已提供 `businessModelPath` 时读取并增量更新；没有时创建一份 BusinessFlowSpec。
2. 业务字段只维护在根级 `fields`。各 `views` 只引用字段 key，不复制 label、type 或枚举。
3. 每个字段、动作和 transition 保留 `sourceStatus=confirmed|recommended|TBD` 与来源。
4. 用户明确的关系才是 `confirmed`；建议写入 `recommended`，未解决内容集中写入 `tbd`。
5. 运行：

```bash
python3 scripts/build_flow_plan.py <business-model.yaml> --output <flow-plan.yaml>
```

脚本失败时停止，不进入 Figma。

### 2. 形成 FlowPlan

FlowPlan 至少包含：平台、状态清单、页面实现 Skill、字段引用、路由、可建立 Prototype 的 confirmed 路由、pending Skill、假设和 TBD。

页面类型默认委派：

| view.type | 页面 Skill |
| --- | --- |
| `list` | `qifu-list-page` |
| `drawer` | `qifu-drawer-form` |
| `page` | `qifu-detail-page` |

`views.<key>.skill` 明确指定时优先使用该值。指定 Skill 不存在时保留状态和入口，标记 `pending-skill`；不得偷偷改用近似 Skill。

### 3. 盘点并复用页面

1. 确认目标文件、目标 Page 和空白落点，不新建近义 Page。
2. 根据 `pageBindings` 和目标 Page 检查已有 Frame、结构验收、视觉验收、平台、尺寸和字段。
3. 已验证页面直接复用；禁止为了“统一”重新生成。
4. 仅对缺失状态调用对应页面 Skill。页面 Skill 负责自己的组件、布局和视觉；本 Skill 不手绘页面。
5. 复用页面与新页面都必须使用同一 BusinessFlowSpec 的字段 key 和同一平台 Adapter。

### 4. 建立 Prototype

1. 只建立 `sourceStatus=confirmed` 的 transitions。
2. 一个 transition 可以包含多个等价触发点，例如“取消”和关闭图标共同映射到 `create-dismiss`。
3. 菜单、Popover 等瞬时状态可作为 transient overlay，不计入正式页面状态。
4. Prototype 只模拟跳转；`refreshList`、`preserveFiltersAndPagination` 等数据效果必须保留在 Spec 和交付说明中，不宣称 Figma 已执行真实数据逻辑。
5. 未确认、recommended 或 TBD 路由不得偷偷连线。

### 5. 验证并交付

按 [验证与交付](references/validation.md)完成模型、页面、组件、字段、路由和截图检查。结构通过不等于视觉通过；未截图检查不得写 `VISUAL_PASS`。

## 失败关闭

出现以下任一情况时停止对应步骤并报告：

- `INVALID_BUSINESS_FLOW_SPEC`：模型结构、字段引用或动作引用无效；
- `UNSUPPORTED_PLATFORM`：平台 Adapter 不存在，禁止回退其他平台；
- `PENDING_PAGE_SKILL`：目标页面 Skill 不存在且没有已验证页面可复用；
- `PAGE_FIELD_MISMATCH`：页面字段与 BusinessFlowSpec 不一致；
- `PROTOTYPE_TARGET_MISSING`：confirmed 路由缺少来源点击节点或目标 Frame；
- `COMPONENT_INTEGRITY_FAIL`：核心控件不是组件实例、实例被分离或混入其他平台；
- `VISUAL_CHECK_REQUIRED`：结构已通过但尚未完成截图检查。

失败时保留已验证资产，不生成替代页面、不手绘控件、不修改组件母版，也不把 Candidate 登记为 Golden Sample。

## 硬性约束

- 不把业务字段复制进本通用 Skill。
- 不修改页面 Skill、共享组件映射或平台 Token 来迁就单个业务链路。
- 不把参考截图直接放入 Figma 作为页面。
- 不覆盖、移动或删除用户已有页面。
- 不将 `recommended` 或 `TBD` 提升为 `confirmed`。
- 不为未确认入口创建页面或 Prototype。
- 不在用户确认前登记 Golden Sample。

## 交付内容

完成后返回：

1. BusinessFlowSpec 与 FlowPlan 路径；
2. 业务链路图和页面清单；
3. 页面节点 ID、复用或新建状态及对应页面 Skill；
4. 页面间跳转和每个动作的返回规则；
5. 未实现入口、pending Skill、recommended 和 TBD；
6. 字段一致性、组件结构、视觉截图和 Prototype 检查结果。
