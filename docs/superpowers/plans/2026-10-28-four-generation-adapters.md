# 四项生成适配实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement task-by-task.

**Goal:** 让两种新增列表和两种新增抽屉拥有可执行的独立适配与真实样本证据。
**Architecture:** 列表router+五个子Skill；shared记录跨能力状态；drawer独立平台Adapter；历史资产事实与当前运行路由分开。
**Tech Stack:** Markdown/JSON/Python unittest/Figma Plugin API/Git。
**Spec:** docs/superpowers/specs/2026-10-28-four-generation-adapters-design.md

## Global Constraints

- 分支 codex/five-platform-adapters-20261028；备份 backup/before-five-platform-adapters-20261028-233328；不改main。
- Figma先备份可编辑副本再写；测试目标3497:651；智能运营外壳6155:1851与菜单6158:1989保留独立来源。
- 旧智客星4892:34812拒绝；5468:3233候选必须预检；菜单3650:998是允许的明确复用，Header3639:1529是错误来源。
- source登记、离线计划、真实Figma结构通过、视觉通过分别记录。
- 旧三列表子Skill保持内容不变，旧tag安装/回退仍可读；不更新本机缓存。

## Review Focus

- 协调替换主题或菜单、请求旧模板必须被阻止。
- 单选与多选、不同列数不能被旧4+1固定矩阵限制。
- JYM1366x1024来源不能直接裁切成768而不检查侧栏和正文可见性。
- 当前子Skill集合扩展不能破坏旧四组件tag恢复。
- 试稿含样式缺口不能以复制成功标为生成通过。

### Task 1: 两列表适配与路由

**Files:** list仓库plugins/qfin-list-page/skills/qifu-{zhineng-yunying,zhikexing}-list-page/；router/scripts/validate_router.py、SKILL.md、references/prompt-template.md；scripts/versioning_lib.py、install_version.py及tests。
**Interfaces:** plan_page(spec) -> dict；child固定platform；返回shell/header/menu/theme/contentStrategy和验收要求，不写Figma。

- [ ] 新写CLI场景测试，确认新平台无子Skill/计划器而失败。
- [ ] 实现智能运营子Skill与计划器；用真实外壳副本组装样本，结构和截图验收，再做消费复核。
- [ ] 实现智客星子Skill与计划器；拒旧来源并预检候选，用副本做真实样本和消费复核。
- [ ] 扩展router和版本管理，当前五平台、历史三平台tag均测试通过。
- [ ] 更新shared列表能力与版本，旧列表入口冲突统一指向独立插件。
- [ ] 提交推送第一个检查点。

### Task 2: 金毓盟和电销抽屉

**Files:** shared/references/platform-{jinyumeng,dianxiao}.md；drawer/references/platform-backgrounds.md；drawer/scripts/plan_platform_drawer.py与tests。
**Interfaces:** plan_drawer(spec) -> dict；返回来源、控件、主题、布局和实际验收范围；消费shared规则。

- [ ] 先写背景平台尺寸、主题、字段控件和未支持组合的失败测试。
- [ ] 实现金毓盟适配并在完整背景样本验收，记录56/208及独立主题。
- [ ] 实现电销适配并验收56/200、无actionSlot、正确独立菜单。
- [ ] 只有获证据的组合开放为preflight-required；更新releasePolicy，重生成detail插件载荷。
- [ ] 推送第二个检查点。

### Task 3: 最终核验与时间线

- [ ] 全套单元测试、契约、版本安装/回退兼容、payload一致性通过；记录实际数量。
- [ ] 新鲜上下文四场景消费复核和独立全分支审查，修复实际阻塞。
- [ ] 写明Figma源/备份/新增节点/样式变更、测试结果、剩余限制与回退方式。
- [ ] 推送最后记录检查点，回读远端SHA与本地tree一致、确认main和备份不动。

## Execution ruling

用户“开始吧”承接已讨论的继续适配与验收，授权执行和推送独立分支；不重复要求方案或实施审批。复用本会话专用干净clone，避免触碰用户原始工作目录。技能源在两个GitHub仓库，不复制到个人安装缓存或Nutstore目录。
