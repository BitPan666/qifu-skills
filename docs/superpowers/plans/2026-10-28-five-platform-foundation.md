# 五平台基础配置迭代计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 把已核实的五平台资产、主题与安全边界接入配置，并留下按时间回退的源码检查点。

**Architecture:** qifu-skills 的 shared 是抽屉/详情共享适配的正本；qfin-list-page 保持独立平台子 Skill。本轮仅建立统一资产事实与解析门禁，后续生成能力独立迭代，不把注册成功升级为页面验收成功。

**Tech Stack:** Markdown、JSON、Python unittest、Git、Figma 只读 Plugin API。

**Spec:** 用户已确认的交接要求和 2026-10-28 Figma 只读核查；摘要保存在 docs/iterations/2026-10-28-five-platform-foundation.md。

## Global Constraints

- 所有改动在 codex/five-platform-foundation-20261028；main 与既有备份保持不动。
- 迭代前备份：backup/before-five-platform-iteration-20261028-224916。
- 智能运营复用 Frame 6155:1851，菜单独立使用 6158:1989；不修改电销母版。
- 当前五平台页面不得被标为全部通过；Figma 原资产修改必须先保留可编辑副本。
- GitHub 源码是跨电脑正本；不更新安装缓存或重复写入个人 Skill 目录。
- 历史全量 Token 快照保持原采集日期；本轮新增的实时绑定快照只声明实际核验范围。

## Review Focus

1. 智客星历史模板仍可识别平台，但不能选为已验证默认模板。
2. 智能运营空白内容是有效外壳边界；不是 SLOT，必须在副本中创建内容容器。
3. 菜单属性键的历史后缀不能被误判为电销母组件引用。
4. 金毓盟、电销的设计试稿不等于抽屉/详情生成规则已就绪。
5. 时间点回退只生成建议命令，不覆盖当前工作或强推分支。

### Task 1: shared 注册与主题解析

**Files:** skills/qifu-shared/references/platform-registry.json；新增 platform-jinyumeng.md、platform-dianxiao.md；platform-zhineng-yunying.md；theme/theme-registry.json；新增 theme/live-platform-bindings.json；skills/qifu-drawer-form/scripts/resolve_platform.py、validate_multi_platform_contract.py 及 tests。

**Interfaces:** 平台解析保留现有状态/退出码，增加资产来源和 readiness；主题校验读取实时绑定快照，历史 tokens.json 继续作为历史全量快照。

- [x] 为金毓盟、电销中文名/模式解析，新外壳解析和跨平台冲突写失败测试。
- [x] 为旧模板来源、主题值/Mode 缺失、错误菜单母版写失败测试。
- [x] 补齐注册、平台规则与实时绑定快照；保留 Candidate 和 PREVIEW_ONLY 边界。
- [x] 运行现有解析/契约测试及新增测试，生成 detail 插件载荷并验证一致性。
- [x] shared 与受影响插件版本增加 patch，提交独立检查点。

### Task 2: 独立列表插件资产登记

**Files:** qfin-list-page 中新增平台资产注册表、验证器和测试，补充平台资产说明与版本记录。

**Interfaces:** 现有三平台路由与三个子 Skill 保持不变；新增两平台以 pending-adapter 登记，不宣称可以路由生成。

- [x] 先测试资产注册表缺失/跨平台菜单/候选误升级等失败场景。
- [x] 登记五平台节点类型、尺寸、组件关系和内容装配方式。
- [x] 跑现有全套测试、路由验证与新资产验证，保留原三个子 Skill 内容指纹。
- [x] 提交独立检查点。

### Task 3: 时间线与回退

**Files:** docs/iterations/2026-10-28-five-platform-foundation.md；scripts/iteration_timeline.py；tests/test_iteration_timeline.py。

**Interfaces:** python3 scripts/iteration_timeline.py --before <带时区ISO时间> 查询当前分支祖先提交并输出新恢复分支命令；脚本不执行回退。Git revert 作为保留时间线的正式回退方式。

- [x] 用临时 Git 仓库测试时间筛选、未知时间点、脏工作区提示和无修改副作用。
- [x] 保存基线、阶段、测试与回退说明，包含跨仓库检查点配对。
- [x] 检查完整差异，提交推送，回读 GitHub 分支 SHA 与文件内容。

## Execution ruling

用户明确要求“开始改”和“任何修改都是版本迭代”，已授权按上述核查结论执行及推送独立分支，不重复请求实施确认。不同仓库可并行实现，最终统一核验。
