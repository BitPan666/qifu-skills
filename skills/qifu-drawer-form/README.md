# qifu-drawer-form

> 在 Figma 中按命名组合,使用「奇富科技中后台组件库 新」的真实组件实例生成奇富后台右侧抽屉表单(新建 / 编辑 / 查看)。

![Type](https://img.shields.io/badge/archetype-L4%20Drawer%20Form-cyan) ![Compositions](https://img.shields.io/badge/compositions-6-blue)

## 解决什么问题

把 B 端"新建 X / 编辑 X / 查看 X"这种最常见的右侧抽屉,从中文描述直接生成成结构化、可编辑、与组件库保持绑定的 Figma 实例。

## 输入 → 输出示例

**输入**:
```
在智客星平台智能运营下,新建触发式任务抽屉。
platformKey=zhikexing, themeKey=zhikexing-green。
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

## 6 个注册组合

| 组合名 | 场景 | Footer |
|---|---|---|
| `Qifu Drawer Form / Simple Create` | 字段 ≤ 6,无分组 | 取消 + 确定 |
| `Qifu Drawer Form / Sectioned Create` | 7–15 字段,有分组(最常用) | 取消 + 确定 |
| `Qifu Drawer Form / Advanced Create` | > 15 字段或分步 | 取消 + 上一步/下一步/提交 |
| `Qifu Drawer Form / Edit` | 编辑已有记录,字段回填 | 取消 + 保存 |
| `Qifu Drawer Form / Readonly` | 严格只读 | 关闭 |
| `Qifu Drawer Form / Data Detail with Table` | 摘要 + 筛选 + 内嵌表格 | 可无 Footer |

## 宽度三档

| 档位 | 宽度 | 适用 |
|---|---:|---|
| Narrow | 480px | 极少字段 + 短控件 |
| Standard | 640px | **默认** |
| Wide | 840px | 双列 / 复杂控件 |

## 平台与主题切换

平台切换和主题切换是两个独立维度：

- `platformKey`：决定平台壳、菜单、业务词汇、底图协议和平台缺口。
- `themeKey/themePrimary`：只决定主按钮、选中态、链接色、轻量标签和强调色。

| platformKey | 平台 | 默认主题 | 说明 |
|---|---|---|---|
| `zhikexing` | 智客星 | `zhikexing-green` | 当前主平台；可独立抽屉，也可叠加智客星列表页底图。 |
| `yushu` | 毓数 | `yushu-green` | 只有明确指定毓数时使用，不再作为默认平台。 |
| `zhineng-yunying` | 智能运营平台 | `smartops-blue` | 预留蓝色主题平台；平台壳未补齐时先生成独立抽屉。 |
| `qifu-generic` | 奇富通用后台 | `zhikexing-green` | 未指定平台时使用，只生成抽屉本体。 |

| themeKey | 主色 | 说明 |
|---|---:|---|
| `zhikexing-green` | `#00B578` | 智客星默认绿色主题。 |
| `yushu-green` | `#00B578` | 毓数当前绿色主题，以目标文件变量为准。 |
| `smartops-blue` | `#1677FF` | 智能运营平台蓝色主题。 |
| `custom` | 用户指定 | 必须同时写 `themePrimary`。 |

换平台不能改变 `compositionName`、字段顺序、控件类型和 Footer；换主题不能 detach 组件或手改实例内部颜色。

## 示例提示词

### 智客星超频流控配置

```text
使用 qifu-drawer-form，在智客星平台生成“超频流控配置”右侧抽屉。
platformKey：zhikexing
themeKey：zhikexing-green
presentationMode：STANDALONE
componentMode：REAL_COMPONENT_ONLY
compositionName：Qifu Drawer Form / Simple Create
widthTier：840

字段：规则名称 Select 必填；超频人群 Radio.Group 必填，选项为人群包/客群；选择人群 Custom(SelectedAudienceTag)；有效期 DateRange 必填；触达方式 Select 必填；超频规则 Custom(OverFrequencyRuleBuilder)。
Footer：取消 + 确定。
完成后返回 platformKey/themeKey 回读、ComponentResolutionManifest、Slot 验证、structuralValidation 和 visualValidation。
```

### 蓝色主题智能运营平台

```text
使用 qifu-drawer-form，在智能运营平台生成“超频流控配置”右侧抽屉。
platformKey：zhineng-yunying
platformName：智能运营平台
themeKey：smartops-blue
themePrimary：#1677FF
presentationMode：STANDALONE
componentMode：REAL_COMPONENT_ONLY

字段与智客星超频流控配置一致。只把主按钮、Radio 选中态、链接色、轻量标签和强调色切换为蓝色主题；不得改变字段、布局、控件实例、间距、圆角、阴影或 Slot 结构。
如果智能运营平台专属导航壳缺失，记录 PLATFORM_PROFILE_MISSING，不要借用毓数菜单冒充。
```

### 智客星列表页叠加抽屉

```text
使用 qifu-drawer-form 和 zhikexing-list-page，在智客星平台生成“超频流控配置”右侧抽屉。
platformKey：zhikexing
themeKey：zhikexing-green
presentationMode：OVERLAY_ON_ZHIKEXING_LIST
background.source：TEMPLATE
当前菜单：客户运营 / 流控管理
```

## 关键铁律(踩过的坑 — 2026-08-12)

AI 曾把抽屉内组件实例丢到 Page 根级(看起来结构对、实际 Frame 不嵌套),已把以下两条加入 SKILL.md 验证清单最前:

1. **层级归属检查** — 所有控件 INSTANCE 必须在 `Drawer/Header | Section/<name> | Drawer/Footer` 三容器之一内,不允许 Page 根级孤儿
2. **重复节点检查** — 抽屉内不存在位置/尺寸几乎一致的重复节点

配套清理插件(兜底)在 `Component Library/.figma-plugins/qifu-drawer-cleanup/`(外部,不在本仓)。

## 文件导航

- `SKILL.md` — 9 步工作流 + 输入契约 DrawerSpec + 验证清单
- `references/drawer-compositions.md` — 6 组合与调用规则
- `references/page-blueprint.md` — 宽度阶梯 / Header / Footer / Section 规则
- `references/field-control-map.md` — 字段类型 → 控件的路由表 + 32px 高度统一规格
- `references/platform-theme-switching.md` — 平台与主题切换协议
- `references/figma-execution-validation.md` — 结构化验收、属性回读和 Slot 验证
- `agents/openai.yaml` — Codex 入口

## 共享依赖

- [`qifu-shared/references/component-map.md`](../qifu-shared/references/component-map.md)
- [`qifu-shared/references/platform-yushu.md`](../qifu-shared/references/platform-yushu.md)

## 不适用场景

复杂看板、向导流(Wizard,将来 qifu-wizard)、带批量编辑的列表页(走 [qifu-list-page](../qifu-list-page/))。
