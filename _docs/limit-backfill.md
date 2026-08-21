# 已知限制回填指引(Limit Backfill)

> 跑通日志([validation-log.md](./validation-log.md))里的"沉淀建议"打勾后,按本指引把限制反向回填到对应文件。
> 这是把"个人踩坑"升级为"团队规则"的关键一步,**不要跳过**。

---

## 决策树 — 应该写到哪里?

```
这条限制说的是...
│
├─"AI 生成时必须每次检查的结构规则"
│   (如:层级归属、重复节点、列宽数组一致、Tag 严格语义)
│     ↓
│   → 写进 SKILL.md 第 9 节"验证",放在最前(优先级最高)
│
├─"某组合本身的能力边界"
│   (如:Sectioned Create 不适合字段 > 15、Master Detail 不支持三级菜单)
│     ↓
│   → 写进 references/<x>-compositions.md 对应组合的"适用场景"列
│     或在调用规则下加"已知边界"小节
│
├─"某种字段/控件/区块的选型约束"
│   (如:Radio.Group ≥ 4 项改 Select、Textarea 不并列双列)
│     ↓
│   → 写进 references/<x>-blueprint.md 或 <x>-control-map.md 对应小节
│
├─"组件库本身缺这个能力"
│   (如:WorkspaceTabs 未组件化、Header Cell 不支持动作组对齐)
│     ↓
│   → **不改 SKILL.md**,而是在 Audit / Missing Components 里加新条目,
│     并把"已知 Fallback 工具"登记在同文件的"Fallback 工具清单"段
│
└─"平台/业务规则的边界"
    (如:毓数侧栏只支持到三级、权限管理必须展开父菜单)
      ↓
    → 写进 qifu-shared/references/platform-yushu.md(或者将来的 platform-XX.md)
```

---

## 回填格式(统一)

所有写在 SKILL.md / blueprint.md / compositions.md / control-map.md 里的"已知限制",**都用相同格式**便于检索:

```markdown
> **已知限制(YYYY-MM-DD · <场景一句话>)**:<一句话规则>
> 来源:`_docs/validation-log.md` <YYYY-MM-DD> 那条记录
> 影响场景:<哪些 composition / 哪些控件 / 哪些字段类型会受影响>
```

例如:

```markdown
> **已知限制(2026-08-12 · 新建触发式任务抽屉)**:Drawer Frame 内的所有控件 INSTANCE
> 必须嵌套在 `Drawer/Header | Section/<name> | Drawer/Footer` 三容器之一,不允许 Page 根级孤儿。
> 来源:`_docs/validation-log.md` 2026-08-12 · 新建触发式任务抽屉
> 影响场景:全部 5 个 Drawer Form compositions
```

---

## 回填的检查清单

每次回填后,在提交前自检:

- [ ] 这条限制按上面的决策树放对了文件
- [ ] 这条限制使用了上方"已知限制"统一格式
- [ ] validation-log.md 里对应的"沉淀建议"从我打的 ☑ 改为 `[x]`(已完成)
- [ ] 累计指标表里的"沉淀条数" +1
- [ ] 该 SKILL.md 的"## 已知限制"小节(如果有)按时间倒序排列,最新在最前
- [ ] 如果这条限制**改变了原有规则**(比如把"建议"改成"必须"),同时在 SKILL.md 的 changelog 里加一行版本说明

---

## 已知限制的统一存放位置(每个 SKILL.md)

每个 SKILL.md 都有"## 已知限制"小节,位于 **硬性约束之后、交付内容之前**。这是给跑通后发现的限制预留的位置,按时间倒序追加。

```
## 硬性约束
...
## 已知限制

> 按时间倒序,最新在最前。跑通后发现并沉淀的限制统一放这里,
> 不要散落在 SKILL.md 各处。

### 2026-08-12 · 新建触发式任务抽屉
- 抽屉 frame 内不允许 Page 根级孤儿 INSTANCE...(以下引用验证清单)
- 抽屉 frame 内不允许重复节点...

### YYYY-MM-DD · (下一条)

## 交付内容
...
```

---

## 不要把什么放进来

以下三类**不属于"已知限制"**,不要塞进 SKILL.md:

1. **临时性 excuse**(如"那天 Figma 抽风") — 一次性事件,不是规则
2. **业务-specific 规则**(如"触发式任务必须有有效期")— 这是业务需求,不是 skill 限制,放到 DetailSpec/DrawerSpec/PageSpec 的输入示例或 platform-yushu.md
3. **AI 模型的临时偏差**(如"Claude 那天没读懂 X")— 这类应该通过增强 SKILL.md 的工作流/验证清单来解决,而不是写"已知限制"

---

## 月度回顾时怎么用

每月底跑以下两件事:

1. **看 SKILL.md 里"已知限制"小节的条数增长曲线**
   - 增长快 → skill 还在踩坑期,继续打磨
   - 增长停滞 → skill 稳定,可以把精力投向扩展 (新 composition / 新原型)

2. **对比"已沉淀"vs"待沉淀"**
   - 若 `_docs/validation-log.md` 里有 ☑ 但没回填的,本月内必须清掉;
   - 不清掉就是 SKILL.md 和真实跑通情况"脱钩",下次跑还会踩同样的坑。

相关:[[github-upload-standard]] 第 5 条(memory 同步)与本指引互补——回填的是 skill 工程规则,memory 同步的是仓库元信息。
