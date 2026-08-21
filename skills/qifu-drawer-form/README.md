# qifu-drawer-form

> 在 Figma 中按命名组合,使用「奇富科技中后台组件库 新」的真实组件实例生成奇富后台右侧抽屉表单(新建 / 编辑 / 查看)。

![Type](https://img.shields.io/badge/archetype-L4%20Drawer%20Form-cyan) ![Compositions](https://img.shields.io/badge/compositions-5-blue)

## 解决什么问题

把 B 端"新建 X / 编辑 X / 查看 X"这种最常见的右侧抽屉,从中文描述直接生成成结构化、可编辑、与组件库保持绑定的 Figma 实例。

## 输入 → 输出示例

**输入**:
```
在毓数平台智能运营下,新建触发式任务抽屉。
分区 1【基础信息】:任务名称(Input 必填)、所属项目(Select 必填)。
分区 2【选择客群】:人群圈选(Custom,必填)。
分区 3【任务规则】:触发事件、任务目标、任务有效期、强制提醒、任务说明。
```

**输出**:Figma Frame 中
- Drawer 宽度 640px(Standard 档)
- Header:标题"新建触发式任务" + 关闭按钮,56px
- Body(padding 24,gap 24):
  - Section × 3,每个 Section 有标题 + FormItem ×N
- Footer(pin 底):取消 + 确定(Primary)
- 控件全部 32px 高,真实组件 INSTANCE

## 5 个注册组合

| 组合名 | 场景 | Footer |
|---|---|---|
| `Qifu Drawer Form / Simple Create` | 字段 ≤ 6,无分组 | 取消 + 确定 |
| `Qifu Drawer Form / Sectioned Create` | 7–15 字段,有分组(最常用) | 取消 + 确定 |
| `Qifu Drawer Form / Advanced Create` | > 15 字段或分步 | 取消 + 上一步/下一步/提交 |
| `Qifu Drawer Form / Edit` | 编辑已有记录,字段回填 | 取消 + 保存 |
| `Qifu Drawer Form / Readonly` | 严格只读 | 关闭 |

## 宽度三档

| 档位 | 宽度 | 适用 |
|---|---:|---|
| Narrow | 480px | 极少字段 + 短控件 |
| Standard | 640px | **默认** |
| Wide | 840px | 双列 / 复杂控件 |

## 关键铁律(踩过的坑 — 2026-08-12)

AI 曾把抽屉内组件实例丢到 Page 根级(看起来结构对、实际 Frame 不嵌套),已把以下两条加入 SKILL.md 验证清单最前:

1. **层级归属检查** — 所有控件 INSTANCE 必须在 `Drawer/Header | Section/<name> | Drawer/Footer` 三容器之一内,不允许 Page 根级孤儿
2. **重复节点检查** — 抽屉内不存在位置/尺寸几乎一致的重复节点

配套清理插件(兜底)在 `Component Library/.figma-plugins/qifu-drawer-cleanup/`(外部,不在本仓)。

## 文件导航

- `SKILL.md` — 9 步工作流 + 输入契约 DrawerSpec + 验证清单
- `references/drawer-compositions.md` — 5 组合与调用规则
- `references/page-blueprint.md` — 宽度阶梯 / Header / Footer / Section 规则
- `references/field-control-map.md` — 字段类型 → 控件的路由表 + 32px 高度统一规格
- `agents/openai.yaml` — Codex 入口

## 共享依赖

- [`qifu-shared/references/component-map.md`](../qifu-shared/references/component-map.md)
- [`qifu-shared/references/platform-yushu.md`](../qifu-shared/references/platform-yushu.md)

## 不适用场景

复杂看板、向导流(Wizard,将来 qifu-wizard)、带批量编辑的列表页(走 [qifu-list-page](../qifu-list-page/))。
