# Page Archetypes：跨平台页面类型与迁移矩阵

## 1. 页面类型不是平台类型

平台是业务和品牌上下文；Archetype 是可迁移的任务结构。相同页面类型可被多个平台复用：

| Archetype | 主要任务 | 标准 Patterns | 当前落图 Skill |
|---|---|---|---|
| List | 找到、筛选、批量处理多条记录 | Page Header / Filter Bar / Action Bar / Table / Pagination | `qifu-list-page` |
| Detail | 查看、核验、局部操作单个对象 | Page Header / Tabs / Detail Block / Timeline / Action | `qifu-detail-page` |
| Drawer Form | 新建、编辑、查看且保持上下文 | Drawer Header / Form Section / Field / Footer | `qifu-drawer-form` |
| Dashboard | 监控、比较、定位异常 | KPI / Chart / Ranking / Filter / Empty | 待建 `qifu-dashboard` |
| Workspace | 快捷入口、待办、最近访问 | Shortcut / Todo / Recent / Notice | 待建 `qifu-workspace` |
| Tree Table | 层级浏览、父子汇总、批量展开 | Tree Filter / Tree Table / Summary | 待建 `qifu-tree-table` |
| Wizard | 分步骤完成复杂配置 | Stepper / Form Section / Review / Result | 待建 `qifu-wizard` |
| Permission | 授权角色、资源、操作与数据范围 | Role List / Resource Tree / Check Matrix / Save | 待建 `qifu-permission-page` |

## 2. 迁移规则

迁移一张页面时只替换以下内容：

```text
保持：Archetype、Pattern、组件语义、状态模型、间距和验证规则
替换：Header、SideMenu、Logo、菜单树、术语、业务槽位、权限、品牌色
重新评估：平台容器宽度、导航密度、平台特有数据组件
```

不要把“毓数列表页”复制成“风控列表页”。应表达为：

```yaml
archetype: List
patterns: [Filter Bar, List Action Bar, Table Shell]
adapter: platform-risk
businessSlots: [risk-rule-selector]
```

## 3. 组合命名

已有落图 Skill 必须返回其注册表中的完整名称，例如：

- `Qifu List Page / Basic Table`
- `Qifu List Page / Basic Filter Table`
- `Qifu Detail Page / Tabbed`
- `Qifu Drawer Form / Sectioned Create`

Dashboard、Permission 等 `planned` Archetype 当前不分配可执行 `compositionName`；只返回建议 Pattern 和 `UNSUPPORTED_ARCHETYPE`，避免让未实现名称看起来可调用。组合名称描述结构与任务，不描述具体平台、菜单或业务对象。

## 4. 页面状态矩阵

同一页面一次只交付一种主状态：

| 状态 | 适用 | 规则 |
|---|---|---|
| Data | 默认交付 | 使用代表性数据，不堆满页面 |
| Loading | 首次加载或提交 | Skeleton / Button loading，保留结构 |
| Empty | 无数据 | 保留标题、筛选和主操作，显示空态 |
| Error | 请求失败 | 明确错误原因和重试操作 |
| Disabled | 权限或业务不可用 | 组件保留但不可操作，说明原因 |

## 5. 平台迁移验收

- 替换 Adapter 后页面主任务仍能完成；
- 组件语义未被平台名污染；
- 业务专属组件都位于 `Slot / <name>`；只有确认 `COMPONENT_MISSING` 且用户明确授权降级时，才允许出现可审计的 `Fallback / <capability>`；
- 页面不依赖某个平台的隐含菜单、Logo 或用户头像；
- 真实组件实例、状态和属性在迁移前后可核对。
