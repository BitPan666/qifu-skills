# zhikexing-list-page

> 基于人工确认的智客星 1366 列表页模板，在 Figma 中生成保持真实组件与 Slot 关系的列表页。

![Type](https://img.shields.io/badge/archetype-L4%20List-green) ![Viewport](https://img.shields.io/badge/viewport-1366%C3%97768-blue) ![Platform](https://img.shields.io/badge/platform-%E6%99%BA%E5%AE%A2%E6%98%9F-brightgreen)

## 解决什么问题

将“侧边导航 + 筛选 + 批量操作 + 可勾选表格 + 分页”的智客星列表页，稳定复用为 Figma 可编辑页面。它复制经过人工调整的完整模板，而不是重新手绘页面，也不尝试写入 Connector 当前不支持的 Slot。

## 基线模板

| 项目 | 值 |
| --- | --- |
| Figma 文件 | `gTV3VdC6a5e9vpkRHIZSXA` |
| 模板节点 | `4892:34812` |
| 模板名称 | `Template / List Page / 智客星 / 1440 / 手动调整` |
| 实际画板 | `1366 x 768` |
| 页面组合 | 4+1 筛选、按钮触发、可选择表格、批量操作、右侧主操作、表格内分页 |

模板名称保留历史“1440”字样，但生成与验收一律以实际 `1366 x 768` 为准。

## 快速使用

```text
使用 $zhikexing-list-page 并调用 @figma 插件，
在智客星的“客户添加 > 加微链接”下创建加微链接列表页；
筛选为加微名称、发布状态、渠道列表、渠道归属、创建日期，
左侧操作为批量修改欢迎语和批量关闭，右侧主操作为新建加微链接，
表格可多选，行操作为详情、编辑、更多。
```

## 关键规则

- 基线模板整页复制到指定 Page 的空白区域，原模板不修改。
- 保留 `List Page Shell-V2`、`Filter Bar-V2`、`Table Shell-V2` 与 `Pagination-V2` 的既有 Slot 关系。
- 只改可回读成功的 TEXT、BOOLEAN、VARIANT 与 INSTANCE_SWAP 属性；不直接改 Slot。
- 结构变化超过基线能力时返回 `BLOCKED_TEMPLATE`，请求对应的人工模板，不手绘临时页面。
- 使用智客星 48px 顶栏、200px 侧栏、品牌色菜单状态和组件库既有变量。
- 表格为 selectable、44px、bordered；状态 Tag 统一 `light / semantic theme / medium / square`。

## 文件导航

- `SKILL.md`：输入契约、生成流程与交付门禁。
- `references/page-rules.md`：1366 页面、筛选、表格与分页几何。
- `references/platform-zhikexing.md`：智客星外壳、菜单和变量规则。
- `references/component-map.md`：模板内真实组件映射。
- `references/component-invocation-contract.md`：属性写入和 Slot 边界。
- `references/structural-validation.md`：结构与截图验收。

## 验证截图

![智客星列表页验证](../../screenshots/validation/06-zhikexing-list-page.png)

截图来自 Figma 验证页 `4893:4225`，用于证明模板复制后仍保留完整页面外观；具体业务字段仍需通过可回读属性或匹配的人工模板调整。
