---
name: zhikexing-list-page
description: 已合并入 qifu-list-page 的智客星平台别名。智客星列表页现在通过 qifu-list-page 的 platform=zhikexing 生成（copyTemplate 策略）。本 skill 保留为兼容入口与 qifu-drawer-form 的底图协议依赖源；不要作为独立的列表页生成工作流使用。
---

# Zhikexing List Page（已合并）

> 本 skill 已并入 [`qifu-list-page`](../qifu-list-page/SKILL.md)。智客星列表页不再是独立 skill，而是 `qifu-list-page` 通过 `platform=zhikexing` 走 `copyTemplate` 策略生成。

## 现在怎么用

直接用 `qifu-list-page`，把平台指定为智客星：

```text
使用 qifu-list-page，在智客星的客户添加 > 加微链接下创建加微链接列表页；
筛选为加微名称、发布状态、渠道列表、渠道归属、创建日期；
左侧操作为批量修改欢迎语和批量关闭，右侧主操作为新建加微链接；
表格可多选，行操作为详情、编辑、更多。
```

`platform=zhikexing` 会自动触发 `copyTemplate`：复制人工基线 `4892:34812`（`Template / List Page / 智客星 / 1440 / 手动调整`，实际 `1366 x 768`），只改可回读属性，不直接写 Slot。

完整规则见 [`qifu-list-page/SKILL.md`](../qifu-list-page/SKILL.md) 的 4b 节与 [`qifu-shared/references/platform-zhikexing.md`](../qifu-shared/references/platform-zhikexing.md)。

## 本目录为什么保留

`qifu-drawer-form` 的「智客星列表页底图协议」仍引用本目录的 `references/`（`platform-zhikexing.md`、`component-invocation-contract.md`、`structural-validation.md`），用于验证抽屉底图的完整列表页。因此：

- `references/` 保留，作为 `copyTemplate` 的详细契约与抽屉底图验收依据。
- `SKILL.md` 不再承载独立工作流；唯一权威落图逻辑在 `qifu-list-page`。
- 不要在本目录新增或修改落图规则；需要改智客星规则时改 `qifu-shared/references/platform-zhikexing.md`，并在本目录 `references/` 同步标注。

## 迁移说明

| 旧写法 | 新写法 |
| --- | --- |
| 使用 `zhikexing-list-page` | 使用 `qifu-list-page`，`platform=zhikexing` |
| `zhikexing-list-page` 的基线模板 `4892:34812` | 同一基线，由 `platform-zhikexing.md` 声明 |
| 独立 `references/` | 权威在 `qifu-shared/references/`；本目录 `references/` 仅作抽屉底图协议兼容 |
