---
name: zhikexing-list-page
description: 已合并入 qifu-list-page 的智客星平台别名。智客星列表页现在通过 qifu-list-page 的 platform=zhikexing 生成（copyTemplate 策略）。本目录保留为历史存档入口，2026-09-11 起不再承载独立落图逻辑，也没有消费方；不要安装或作为独立工作流使用。
---

# Zhikexing List Page（已归档）

> 本 skill 已并入 [`qifu-list-page`](../qifu-list-page/SKILL.md)。智客星列表页不再是独立 skill，而是 `qifu-list-page` 通过 `platform=zhikexing` 走 `copyTemplate` 策略生成。

## 状态

- 状态：历史存档；2026-09-11 起本目录不再有任何消费方。
- 落图逻辑唯一权威：`qifu-list-page` 的 4b 节（copyTemplate）+ [`qifu-shared/references/platform-zhikexing.md`](../qifu-shared/references/platform-zhikexing.md)。
- 目录现状：仅保留 `SKILL.md` / `README.md` / `agents/openai.yaml` / `VERSION`，`references/` 已删除。
- 不再安装：Codex/Claude Code 安装脚本已不再把 `zhikexing-list-page` 加入链接列表；如已软链，请删除。

## 触发示例（请改用 qifu-list-page）

```text
使用 qifu-list-page，在智客星的客户添加 > 加微链接下创建加微链接列表页；
筛选为加微名称、发布状态、渠道列表、渠道归属、创建日期；
左侧操作为批量修改欢迎语和批量关闭，右侧主操作为新建加微链接；
表格可多选，行操作为详情、编辑、更多。
```

`platform=zhikexing` 会自动触发 `copyTemplate`：复制人工基线 `4892:34812`（`Template / List Page / 智客星 / 1440 / 手动调整`，实际 `1366 x 768`），只改可回读属性，不直接写 Slot。

## 迁移说明

| 旧写法 | 新写法 |
| --- | --- |
| 使用 `zhikexing-list-page` | 使用 `qifu-list-page`，`platform=zhikexing` |
| 独立 `references/` | 权威在 `qifu-shared/references/`；本目录已删除 |
| 抽屉底图协议依赖本目录 references | 已改为依赖 `qifu-shared/references/platform-zhikexing.md` |