# 五平台基础配置迭代与回退时间线

时区：Asia/Shanghai（UTC+08:00）。用户要求所有修改都作为版本迭代，保留按时间选择检查点的回退能力。

## 基线与阶段

| 阶段 | 时间/来源 | 结果 |
| --- | --- | --- |
| 原始交接备份 | backup/before-five-platform-shells-20261028083105 | 不移动或覆盖 |
| 本轮开始 | 2026-10-28T22:49:16+08:00 | 再次核实远端main，建立本轮备份与迭代分支 |
| 01 时间线工具 | 独立提交，按Git提交时间查询 | 只读查看和选择历史提交，输出新恢复分支命令 |
| 02 五平台基础配置 | 独立提交，按Git提交时间查询 | 注册、来源门禁、主题快照、测试与详情插件载荷 |
| 03 核验记录 | 独立提交，按Git提交时间查询 | 记录阶段提交SHA与跨仓库配对信息 |

两个仓库均使用工作分支 `codex/five-platform-foundation-20261028` 和迭代前备份 `backup/before-five-platform-iteration-20261028-224916`：

- `BitPan666/qifu-skills` 基线：`cae1b393564ee40bd3e870607324e1442e0636f8`。
- `BitPan666/qfin-list-page` 基线：`df21008eb2a489d4b105992b21ddb7def8386d5c`。

各自SHA只用于各自仓库。main、既有交接分支、业务流分支不修改，不合并或发布安装版本。源码正本在GitHub；安装缓存、凭据和运行环境留在本机，不反向覆盖仓库或复制凭据。

## 本轮范围

1. shared登记五平台资产，明确Frame/Component、来源、内容装配方法与每类页面的capabilities。识别平台不等于准许生成。
2. 智客星默认来源改为候选5468:3233，另有5408:13969；候选保留未验收状态。旧4892:34812引用毓数Header，解析为BLOCKED_SOURCE（退出码4），不能当后备。
3. 智能运营登记6155:1851基础Frame、6158:1989独立菜单、6148:34365空白RECTANGLE；后续仅在可编辑副本建立内容容器，不重搭源外壳，也不改电销菜单。
4. 定向采集5个语义颜色变量在4个平台Mode中的绑定，保存live-platform-bindings.json。当前语义品牌核验：毓数#00B85C、智能运营#1969F1、金毓盟#0F6FFC、电销#009E73。智客星primary=null，必须继承并回读候选；不能假设毓数绿色。
5. 历史全量tokens/source/Less保留原采集日期与内容；定向实时快照只覆盖本次核验字段，不伪造全量重新导出。
6. shared 1.3.2→1.3.3、drawer 1.6.0→1.6.1、detail及其插件1.5.0→1.5.1。详情payload由build_detail_plugin.py生成，不手改生成物。
7. 独立列表仓库Plugin 0.1.1→0.1.2、router载荷0.1.0→0.1.1，仅增加资产登记与校验；原三子Skill字节不变，智客星/智能运营路由仍pending-adapter。

Figma本轮只有只读回读，没有创建、修改、发布或删除节点，因此没有发生需要恢复的Figma写入。未来修改源资产必须先保留可编辑副本，并在同一阶段记录源节点、副本节点和恢复方法；Git备份不能替代Figma副本。

## 测试与限制

- RED→GREEN：新增平台解析、旧来源拒绝、跨平台菜单、矩形误作Slot、主题值/Mode漂移和候选误升级等16个测试；运行时共21个drawer测试通过。
- 本仓库单元测试：root 3、list 20、drawer 21、detail 9，共53项。另跑repo、list、multi-platform、portable、同步脚本和独立drawer release校验。
- 列表仓库151项测试及路由/三子Skill/资产契约通过；原三平台内容指纹保持。
- 独立复核发现并修复旧背景文档、协调主题替换和能力/候选状态提升三个问题；新增4个真实CLI变异回归，先复现失败再修复。releasePolicy独立记录本轮可发布状态，下一轮必须结合新验收证据版本化更新。
- 新鲜上下文消费场景已做修改前/修改后对照：四个中文名、新旧模板与智能运营外壳共7次实际解析；旧来源明确阻止。
- 测试日志保存在本机/private/tmp/five-platform-iteration-20261028，不是跨电脑可依赖的文件；以下命令可重跑。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_repo.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/qifu-list-page/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/qifu-drawer-form/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/qifu-detail-page/tests -v
python3 skills/qifu-drawer-form/scripts/validate_multi_platform_contract.py
python3 scripts/build_detail_plugin.py --check
```

本轮没有新页面生成或15场景视觉验收。金毓盟、电销抽屉仍pending-adapter；智能运营、智客星抽屉仍需实际样式/背景预检；详情的缺失平台没有因共享登记而开放。智能运营7处、智客星当前候选50处文字样式缺口作为源资产问题保留，未通过覆盖或分离实例掩盖。抽屉独立插件包装与完整五平台生成属于后续版本。

## 按时间回退

先在目标仓库查看时间线，时间必须带时区：

```bash
python3 scripts/iteration_timeline.py --repo .
python3 scripts/iteration_timeline.py --repo . --before '2026-10-28T22:49:16+08:00'
```

工具只读，返回selected.sha、committedAt、dirtyWorktree与restoreCommand。核对后运行restoreCommand，会在新目录和新codex/restore-*分支打开该历史版本；原分支、后续提交和未提交文件都保留。无历史提交或缺少时区时返回退出码2。重复恢复到相同位置时先查看已有恢复目录，不覆盖它。

正式撤销某阶段时，在保存当前工作后检查并使用 `git revert <该阶段提交SHA>`，产生新的回退提交。若后续版本有依赖，先逐一检查相关提交，再按由新到旧顺序撤销。不要reset --hard、强推main或移动备份分支。

跨仓库选择相同阶段的一对提交，不能将另一个仓库的SHA用于本仓库。恢复旧代码后重跑契约与测试；需要恢复Figma时使用该阶段登记的可编辑副本，本轮不存在Figma写入检查点。

## 已推送的配对检查点

以下时间均为 Asia/Shanghai（UTC+08:00），SHA 已从 GitHub 回读，两个仓库各自的远端 tree 与本机生成的 tree 完全一致。

| 阶段 | qifu-skills | qfin-list-page |
| --- | --- | --- |
| 01 时间线工具 | `9379438b725f3f80f2e1cb9eb15520515247580f` · 2026-10-28T23:16:08+08:00 | `f8a4f745bf2d7b326d7c7999cabe37ecc880c288` · 2026-10-28T23:16:17+08:00 |
| 02 五平台基础配置 | `c345e20c34a44398f7543322595737ebadad90ce` · 2026-10-28T23:17:29+08:00 | `e3778311340888af0aaddcbdbd4e70d483cc505e` · 2026-10-28T23:17:40+08:00 |
| 03 核验记录 | 见本文件当前版本所属提交 | 见本文件当前版本所属提交 |

最终本地复跑：qifu-skills 53 项、qfin-list-page 151 项，共 204 项单元测试全部通过；另外资产、路由、Skill、主题、插件载荷和 release/sync 契约通过。独立复核提出的三项 P2 均修复并复核通过。GitHub Actions 查询未返回本分支运行记录，不能将本地通过称为远端 CI 通过。

阶段 03 仅更新交接/计划/验证记录，不修改运行时规则。若需恢复阶段 01，后续基础配置尚未存在；恢复阶段 02 包含完整本轮配置。按时间查询各自分支的实际提交时间，并以本表配对，避免两个提交间的秒差造成跨仓库版本错配。
