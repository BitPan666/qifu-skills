# zhikexing-list-page（已归档）

> ⚠️ 本 skill 已并入 [`qifu-list-page`](../qifu-list-page/SKILL.md)。智客星列表页现在通过 `qifu-list-page` 的 `platform=zhikexing`（`copyTemplate` 策略）生成。本目录 2026-09-11 起仅保留为历史存档入口，**没有任何消费方**；请勿安装，也不要作为独立工作流使用。

## 迁移后怎么用

```text
使用 qifu-list-page，在智客星的"客户添加 > 加微链接"下创建加微链接列表页；
筛选为加微名称、发布状态、渠道列表、渠道归属、创建日期，
左侧操作为批量修改欢迎语和批量关闭，右侧主操作为新建加微链接，
表格可多选，行操作为详情、编辑、更多。
```

`platform=zhikexing` 自动触发 `copyTemplate`：复制人工基线 `4892:34812`（`Template / List Page / 智客星 / 1440 / 手动调整`，实际 `1366 x 768`），只改可回读属性，不直接写 Slot。

## 归档说明

- 状态：历史存档；落图逻辑唯一权威在 `qifu-list-page` 与 `qifu-shared/references/platform-zhikexing.md`。
- 本目录 `references/` 已删除；`qifu-drawer-form` 的底图协议已改为依赖 `qifu-shared/references/platform-zhikexing.md`。
- 安装脚本已不再链接本目录；如已软链，请执行 `rm ~/.claude/skills/zhikexing-list-page ~/.codex/skills/zhikexing-list-page`。

## 基线模板（权威声明在 qifu-shared）

| 项目 | 值 |
| --- | --- |
| Figma 文件 | `gTV3VdC6a5e9vpkRHIZSXA` |
| 模板节点 | `4892:34812` |
| 模板名称 | `Template / List Page / 智客星 / 1440 / 手动调整` |
| 实际画板 | `1366 x 768` |
| 页面组合 | 4+1 筛选、按钮触发、可选择表格、批量操作、右侧主操作、表格内分页 |

## 验证截图

![智客星列表页验证](../../screenshots/validation/06-zhikexing-list-page.png)