# Skill 跑通日志(Validation Log)

> 每个 skill 在真实 Figma 上跑一次,就往这里追加一条记录;攒够 2-3 条后,把"已知限制"反向回填到对应 SKILL.md(指引见 [limit-backfill.md](./limit-backfill.md))。
>
> **核心目的**:把"skill 自我感觉良好"和"skill 在真实业务上跑得通"区分开。前者是写出来就算数,后者要靠真实记录证明。

---

## 怎么用这份日志

1. 每跑通一次,**复制下面"单次记录模板"到对应的 skill 小节末尾**,按字段填。
2. **不要修改历史记录**——跑通过就是跑通过,跑挂了也如实写。历史对比才能看出 skill 是否在进步。
3. **每条记录必须有截图证据**:把 Figma 里生成的 Frame 截一张图,放到 `../screenshots/validation/<skill-name>/<YYYY-MM-DD>-<slug>.png`,在记录里引用相对路径。
4. 跑一次跑挂了,也算一次记录,状态写 `fail`,把"卡点描述"写清楚——这比跑通更有价值。

---

## 单次记录模板(复制用)

```markdown
### <YYYY-MM-DD> · <一句话场景>
- **skill**:qifu-xxx-page
- **compositionName**:Qifu Xxx Page / Xxx(或 Qifu Drawer Form / Xxx)
- **业务场景**:在哪个平台、哪个菜单、处理什么对象
- **输入 Prompt**:(粘贴你给 AI 的原话,用 > 引用块)
- **目标 Page**:测试(node 3497:651) / 业务 Page 名
- **执行 AI**:Claude Code / Codex / 其他
- **结果**:✅ pass | ⚠️ pass-with-fixes | ❌ fail
- **验收清单全过?**:是 / 否,哪几条没过
- **遇到的偏差**:
  1. <一句话描述偏差> → 我做的是 / skill 应该做的是
  2. ...
- **截图**:`../screenshots/validation/<skill>/<文件名>.png`
- **AI 自检准确率**:(你数出来的问题数 vs SKILL.md 第 9 节清单覆盖率)
- **是否人工干预**:是(干了什么) / 否
- **沉淀建议**:
  - [ ] 这条限制应该写进 SKILL.md
  - [ ] 这条限制应该写进 compositions.md
  - [ ] 这条限制应该写进 blueprint.md
  - [ ] 这条限制应该归到 Audit / Missing Components 的缺口清单
```

---

## qifu-list-page · 跑通记录

<!-- 从这里开始追加 qifu-list-page 的记录 -->

_(还没有记录,第一次跑通后写在下面)_

---

## qifu-drawer-form · 跑通记录

<!-- 从这里开始追加 qifu-drawer-form 的记录 -->

### 2026-08-12 · 新建触发式任务抽屉(已完成,记录补填)
- **skill**:qifu-drawer-form
- **compositionName**:Qifu Drawer Form / Sectioned Create
- **业务场景**:毓数平台智能运营 > 团队辅助 > 任务管理,新建触发式任务
- **输入 Prompt**:
  > 在毓数平台智能运营下,新建触发式任务抽屉。
  > 分区 1【基础信息】:任务名称(Input 必填)、所属项目(Select 必填)。
  > 分区 2【选择客群】:人群圈选(Custom,必填)。
  > 分区 3【任务规则】:触发事件(Select)、任务目标(Select)、任务有效期(Select)、强制提醒(Radio.Group 是/否)、任务说明(Textarea)。
- **目标 Page**:原记录未保留确切 Page;补截图前不得作为完整回归证据
- **执行 AI**:Claude Code;具体模型版本未记录
- **结果**:⚠️ pass-with-fixes
- **验收清单全过?**:否,2 条没过(见下)
- **遇到的偏差**:
  1. **AI 把控件 INSTANCE 丢到 Page 根级**,而不是嵌套进 Drawer Frame → 我做的是手动在 Figma 里把 12 个组件拖回 Section 容器;skill 应该做的是生成时主动归位
  2. **Drawer Frame 内残留与已嵌实例位置/尺寸几乎一致的重复节点**(疑似 AI 重复创建未清理)→ 我写了 `qifu-drawer-cleanup` 插件兜底清理;skill 应该做的是生成后自检并删除重复
- **截图**:待补 `../screenshots/validation/qifu-drawer-form/2026-08-12-trigger-task-drawer.png`;补图后再纳入 README 展示
- **证据状态**:缺截图,当前只作为历史问题回溯记录
- **AI 自检准确率**:SKILL.md 验证清单 25+ 条,人工发现 2 条未覆盖(层级归属 + 重复节点),已加入验证清单
- **是否人工干预**:是,Figma 里手动归位 + 调用清理插件删除 12 个重复节点
- **沉淀建议**:
  - [x] 这条限制应该写进 SKILL.md(已加入,2026-08-12 · "层级归属检查"+"重复节点检查"两条)
  - [ ] 这条限制应该写进 compositions.md
  - [ ] 这条限制应该写进 blueprint.md
  - [ ] 这条限制应该归到 Audit / Missing Components 的缺口清单(把"清理插件"作为已知 Fallback 工具记录)

---

## qifu-detail-page · 跑通记录

<!-- 从这里开始追加 qifu-detail-page 的记录 -->

_(还没有记录,第一次跑通后写在下面)_

---

## 累计指标(每月底更新一次)

| Skill | 累计跑通次数 | pass | pass-with-fixes | fail | 最新一次跑通日期 | 已沉淀到 SKILL.md 的限制条数 |
|---|---|---:|---:|---:|---|---:|
| qifu-list-page | 0 | 0 | 0 | 0 | — | 0 |
| qifu-drawer-form | 1 | 0 | **1** | 0 | 2026-08-12 | **2** |
| qifu-detail-page | 0 | 0 | 0 | 0 | — | 0 |

> 注:`qifu-drawer-form` 的 1 条为历史补填记录,截图证据仍缺失;补齐前只作为问题回溯,不作为完整回归证据。

**指标口径说明**:
- `pass`:SKILL.md 验证清单 100% 全过,无人工修复
- `pass-with-fixes`:基本结构正确,但需要手动调整 ≥ 1 处才能交付
- `fail`:生成结果无法用作起点,需要重做
- "沉淀条数":从这份 Limit Log 反向回填到 SKILL.md 验证清单 / 硬性约束 / 已知限制小节的条数

---

## 每月一次的复盘动作

每月最后一个工作日:

1. 看每个 skill 最近一个月的 `pass / pass-with-fixes / fail` 比例,有没有趋势变化
2. 把 `pass-with-fixes` 里的"偏差"全部反过来检查:它们有没有已经被沉淀到 SKILL.md?如果没有,马上回填
3. 把 `fail` 记录里的"卡点描述"挑出来,看是不是 skill 本身设计就需要扩展(新 composition、新 bodyType、新 Slot)
4. 更新上面的"累计指标"表
5. 把本月沉淀的限制数量写进月报(参见 [[monthly-report-skill-repo]] 和 [[design-meeting-skill]] 的分工)
