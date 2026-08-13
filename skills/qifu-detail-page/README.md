# qifu-detail-page

> 在 Figma 中按命名组合,使用「奇富科技中后台组件库 新」的真实组件实例生成奇富后台详情页(查看为主、局部可编辑)。

![Type](https://img.shields.io/badge/archetype-L4%20Detail-purple) ![Compositions](https://img.shields.io/badge/compositions-4-blue)

## 解决什么问题

把"查看单对象完整信息"这种详情页——基本信息 + Tabs(Tabbed 时)+ 1..N 个 DetailBlock——从中文描述直接生成,保持真实组件实例关系。

## 输入 → 输出示例

**输入**:
```
在毓数平台智能运营下查看"触发式任务"详情页。
任务名:预留白测试;ID:177571985055;Tag:运行中。
Tabs:基本信息、触发记录。
详情头主操作:启用/停用。
区块:
  - 基本信息(Descriptions)
  - 任务规则(Descriptions)
  - 触发记录(Table):触发时间/客户ID/结果/耗时
  - 关联客群(Cards):3 个客群快卡
```

**输出**:Figma Frame 中
- 整页沿用 list-page 外壳(Header/SideMenu/Content/Page Surface)
- Detail Page Shell 独立骨架:
  - `PageHead`(96px):对象身份 + Tags(≤2)+ 主操作(唯一)
  - `Tabs`(44px):基本信息 / 触发记录
  - `Body`:DetailBlock × 4,间距 16px

## 4 个注册组合

| 组合名 | 场景 | 主体形态 |
|---|---|---|
| `Qifu Detail Page / Flat` | 单对象信息一览无余 | 单栏通铺 |
| `Qifu Detail Page / Tabbed` | 多维关联信息(默认) | Tabs 分页 |
| `Qifu Detail Page / Master Detail` | 左 320px 实体列表 + 右详情 | 左右两栏 |
| `Qifu Detail Page / Readonly` | 严格只读、审计 | 单栏 + 仅返回 |

## 6 种 DetailBlock 内容类型

| bodyType | 控件 | 适用 |
|---|---|---|
| `Descriptions` | QFDescriptions / 自定义 | 基本信息、字段值 |
| `Table` | Table Shell-V2 + Cell-V2 | 关联记录、变更历史 |
| `Cards` | 3 列 Card Grid | 关联子对象快照 |
| `Timeline` | Timeline 组件 | 操作历史、状态流转 |
| `KeyMetrics` | KeyValue Grid | 关键指标 |
| `Empty` | Empty 组件 | 无数据但将来会有 |

外加 `Custom(<BizBlock>)` 用于非标准(富文本预览、JSON 编辑器等),配 Fallback + Audit。

## 关键铁律

- **首块必须是核心信息**(Descriptions 或 Descriptions + KeyMetrics),不能首块放 Timeline/Cards/Table
- **整页实心 Primary Button ≤ 2**(PageHead 主操作 + 可选 BlockHeader 操作)
- **PageHead Tag ≤ 2**;主次操作总数 ≤ 3;**Tabs ≤ 7**;Table 行内操作 ≤ 2
- **状态唯一**(Data/Loading/Error/Disabled),不堆叠
- **层级归属检查**(继承自 drawer-form 的 2026-08-12 踩坑):所有控件 INSTANCE 必须在 PageHead / Tabs / DetailBlock 之一内,不允许 Page 根级孤儿

## 与兄弟 skill 的边界

```
查多条记录     → qifu-list-page
新建 / 编辑    → qifu-drawer-form
查看单对象     → qifu-detail-page(本 skill)
```

## 文件导航

- `SKILL.md` — 9 步工作流 + DetailSpec 输入契约 + 验证清单
- `references/detail-compositions.md` — 4 组合
- `references/page-blueprint.md` — PageHead / Tabs / DetailBlock 间距铁律
- `references/detail-block-map.md` — 6 种 bodyType 的选型与细节规则
- `agents/openai.yaml`

## 共享依赖

- [`shared/references/component-map.md`](../../shared/references/component-map.md)
- [`shared/references/platform-yushu.md`](../../shared/references/platform-yushu.md)
