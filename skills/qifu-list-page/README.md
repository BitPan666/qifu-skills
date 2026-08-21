# qifu-list-page

> 在 Figma 中按命名组合,使用「奇富科技中后台组件库 新」的真实组件实例生成奇富后台列表页。

![Type](https://img.shields.io/badge/archetype-L4%20List-green) ![Compositions](https://img.shields.io/badge/compositions-6-blue)

## 解决什么问题

把"列表 + 筛选 + 批量操作 + 分页"这类 B 端最常见页面,从一句中文描述直接生成成 Figma 真实组件实例。组件保持实例关系可编辑,不是手绘、不是截图。

## 输入 → 输出示例

**输入**:
```
在毓数平台的订阅管理 > 群组管理下新建群组管理列表页,
筛选用名称(Input)、状态(Select)、创建时间(DateRange),
行操作:查看 / 编辑 / 停用。
```

**输出**:Figma Frame 中
- 顶部 `Yushu Header-V2` 真实实例
- 左侧 `SideMenuItem-V2` ×N(路径:订阅管理 → 群组管理,选中态正确)
- `List Page Shell-V2` 实例
  - `Filter Bar-V2`:3 个 Filter Item,宽度阶梯 200/200/408
  - `Table Shell-V2`:9 行差异化示例数据,含 Tag(启用/禁用)严格语义
  - `Pagination-V2`:`pageCount=6+`
- 全部 INSTANCE、无重叠、可直接给开发

## 6 个注册组合

| 组合名 | 场景 | 筛选栏 | 选择列 |
|---|---|---|---|
| `Qifu List Page / Basic Table` | 无筛选普通列表 | – | – |
| `Qifu List Page / Basic Filter Table` | 1–4 筛选(默认) | 单行 | – |
| `Qifu List Page / Advanced Filter Table` | 5+ 筛选 | 两行 | – |
| `Qifu List Page / Selectable Filter Table` | 需批量操作 | 单行/两行 | ✓ |
| `Qifu List Page / Loading Table` | 加载中 | 按需 | – |
| `Qifu List Page / Empty Table` | 空/失败/无权限 | 按需 | – |

**铁律**:不得临时造名或混用。

## 快速使用

```bash
# 已按根目录 README 装好软链后,在 Claude Code 里
$qifu-list-page 在毓数平台的权限管理 > 用户授权下新建用户授权列表页,顶部位于 QBI。
```

## 文件导航

- `SKILL.md` — 9 步工作流 + 30+ 验证项 + 输入契约 PageSpec
- `references/page-blueprint.md` — 画板骨架、间距铁律、命名约定
- `references/table-compositions.md` — 6 个组合的完整规则
- `agents/openai.yaml` — Codex 入口

## 共享依赖

本 skill 依赖以下共享文件(不写在自己 references/ 内,见仓库根 README):

- [`qifu-shared/references/component-map.md`](../qifu-shared/references/component-map.md) — 全部真实组件的节点 ID 与属性
- [`qifu-shared/references/platform-yushu.md`](../qifu-shared/references/platform-yushu.md) — 毓数平台导航

## 不适用场景

复杂分析看板、编辑表单(走 [qifu-drawer-form](../qifu-drawer-form/))、详情页(走 [qifu-detail-page](../qifu-detail-page/))、树表、高度定制工作台。

## 关键验证规则(节选)

完整清单在 [SKILL.md](./SKILL.md) 第 9 节:

- 所有组件 INSTANCE 嵌套于 `Header / SideMenu / Content / Page Surface / List Page Shell` 内,**不允许 Page 根级孤儿**
- 表头与每行列宽数组完全一致
- 操作列右侧固定 20px
- `pagination 右边缘 == table 右边缘`
- 选择列开启时 Selection Cell 数量 = 数据行数 + 1
- 启用/禁用 Tag 严格按 `light/success/medium/square`(启)/`light/danger/medium/square`(禁)
