# 详情页组合注册表

## 目的

用稳定名称描述"以查看为主、局部可编辑"的详情页结构。调用必须使用下表完整 `compositionName`;这些名称属于 Skill 的调用协议,不是 Figma 组件母版名称。

与 qifu-list-page(6 组合)、qifu-drawer-form(6 组合)是同一配方协议在不同原型上的复用,**不得跨原型借用组合名**。

## 已注册组合

| `compositionName` | 适用场景 | Head 信息 | 主体布局 | Tabs? | 操作形态 |
| --- | --- | --- | --- | --- | --- |
| `Qifu Detail Page / Flat` | 单对象核心信息一览无余(如用户、角色) | 完整 | 单栏通铺 | 无 | 顶部主操作 + 区块尾操作 |
| `Qifu Detail Page / Tabbed` | 单对象有 3+ 个关联信息维度 | 完整 | Tabs 分页 | 有 | 顶部主操作 + Tab 内操作 |
| `Qifu Detail Page / Master Detail` | 左对象列表 + 右详情联动(如规则管理) | 右侧 | 左 320 列表 + 右自适应 | 可选 | 列表操作 + 详情操作 |
| `Qifu Detail Page / Readonly` | 严格只读、审计/快照场景(如日志、历史版本) | 简化(仅 ID + 标题) | 单栏通铺 | 无 | 仅"关闭/返回" |

## 受限页面组合

| `compositionName` | 适用场景 | 平台 | 专属规则 |
| --- | --- | --- | --- |
| `Qifu Detail Page / Category Q&A` | 类目导航 + 筛选 + 分组问答浏览 | 仅 `zhikexing` | [智客星分类问答](category-qa-zhikexing.md) |

`Category Q&A` 不是单记录详情，也不是 `Master Detail` 的 320px 实体列表。它只复用智客星平台外壳；不继承固定 PageHead、首块 Descriptions、记录 ID/状态摘要或主操作。原有四种组合及其选择规则不变，其他平台不得因此获得详情页支持。

## 调用规则

1. 用户给出完整 `compositionName` 时精确匹配,大小写、空格和斜杠保持一致。
1a. 用户明确描述“类目导航 + 分组问题 + 多条回答”时，仅 `platform=zhikexing` 可选择 `Qifu Detail Page / Category Q&A`；先读取其专属规则，不能用关键词“详情”自动套入原有四组合。
2. 用户未给名称时按以下优先级选择:
   - 提到"快照 / 历史 / 日志 / 审计" → `Readonly`
   - 提到"左列表右详情 / 选择记录查看" → `Master Detail`
   - 关联维度 ≥ 3 或有明显切换语义 → `Tabbed`
   - 单对象信息展开 → `Flat`
3. 未指定且无法区分时使用 `Qifu Detail Page / Flat`；只有输入存在明确的维度切换语义时才生成 Tabs。
4. 组合名称只决定稳定结构(Head 形态、主体布局、操作位置);业务字段、文案、Tabs 名、操作项仍来自 `DetailSpec`。
5. 不把业务对象、Tab 名、状态拼进 `compositionName`,也不创建 `Simple`、`Normal` 等未注册别名。
6. 新场景先用最接近的已注册组合并记录缺口;只有用户确认长期复用,才新增组合名并同步本注册表、`SKILL.md`。

## 解析结果

```text
compositionName
headMode         full | compact | hidden
bodyMode         flat | tabs | masterDetail
tabsCount        0 | 2..N(Master Detail 可选)
readonly         true / false
primaryAction    主操作文案(如 编辑 / 关闭)
```

不得以重命名 Figma 组件的方式实现上述协议。真实组件仍按[组件映射](../../qifu-shared/references/component-map.md)中的正式名称解析。

## 与列表/抽屉的边界

| 场景 | 应使用 | 不应使用 |
| --- | --- | --- |
| 查多条记录,带筛选/批量 | qifu-list-page | qifu-detail-page |
| 新建/编辑单对象,密集字段 | qifu-drawer-form | qifu-detail-page |
| 查看单对象完整信息,局部可编辑 | qifu-detail-page | qifu-list-page / drawer-form |
| 详情页内嵌"新建子记录"按钮 | detail-page 跳转到 drawer-form | detail-page 内做抽屉 |
