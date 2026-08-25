# qifu-drawer-form

在 Figma 中生成可继续编辑的奇富后台右侧抽屉。它会复用真实组件实例，而不是把控件画成分散的矩形和文字。

## 最短调用方式

普通场景只需要说清三件事：**平台、抽屉标题、字段**。例如：

```text
使用 qifu-drawer-form，在智客星生成“新建活动”右侧抽屉。
字段：活动名称 Input 必填；活动类型 Select 必填；有效期 DateRange 必填。
```

Skill 会自动补全默认组合、宽度和 Footer。字段较多或有明确交付要求时，再补充下列可选项：

| 可选项 | 何时需要写 | 示例 |
| --- | --- | --- |
| `platformKey` | 要准确切换平台时 | `zhikexing` |
| `themeKey` | 要明确切换主题色时 | `smartops-blue` |
| `compositionName` | 已确定抽屉组合时 | `Qifu Drawer Form / Sectioned Create` |
| `widthTier` | 有固定宽度要求时 | `680` |
| `componentMode` | 没有正式组件库权限时 | `PORTABLE_KIT` |
| `background` | 需要交付完整打开态页面时 | `EXISTING_LIST_PAGE + 节点 ID` |

默认 `componentMode=REAL_COMPONENT_ONLY`。没有正式组件库时，请明确写 `componentMode=PORTABLE_KIT`；不要让 Skill 用手绘控件替代组件。

## 平台和主题是两件事

- **平台 `platformKey`**：决定平台名称、菜单/底图规则和业务壳。
- **主题 `themeKey`**：只改变主按钮、选中态、链接、轻量 Tag 和强调色。

换主题不会改变字段、控件、间距、圆角、阴影或 Footer。也不要为蓝色主题复制一套组件库。

| 平台 | `platformKey` | 默认主题 | 完整页面底图规则 |
| --- | --- | --- | --- |
| 智客星 | `zhikexing` | `zhikexing-green` | 可使用已验证的智客星列表页模板。 |
| 毓数 | `yushu` | `yushu-green` | 使用毓数平台基线；需指定或验收底图。 |
| 智能运营平台 | `zhineng-yunying` | `smartops-blue` | 正式页面必须指定已验收的智能运营列表页节点。 |
| 奇富通用后台 | `qifu-generic` | `zhikexing-green` | 没有已批准通用底图时只做内部调试，正式交付需先提供底图。 |

| 主题 | `themeKey` | 主色 |
| --- | --- | --- |
| 智客星绿 | `zhikexing-green` | `#00B578` |
| 毓数绿 | `yushu-green` | 以目标文件变量为准 |
| 智能运营蓝 | `smartops-blue` | `#1677FF` |
| 自定义主题 | `custom` | 必须同时给出 `themePrimary` |

## 何时需要完整页面

正式交付默认生成抽屉“打开态”：`Background < Overlay Mask < Drawer`，画面为 `1366 × 768`。抽屉本体调试可以写 `presentationMode=STANDALONE_DEBUG`，但不能把它当成正式页面交付。

智能运营平台目前已有抽屉 Golden Sample，但没有已批准的原生列表页模板。因此：

- 只做抽屉本体，直接使用“智能运营平台策略关联抽屉 Golden Sample”。
- 做正式完整页面，必须提供 `background.source=EXISTING_LIST_PAGE` 和 `background.sourceNode=<已验收列表页节点 ID>`。
- 图片背景只能用于视觉对照，不能作为正式页面底图。

## 示例提示词

### 1. 通用抽屉，最短写法

```text
使用 qifu-drawer-form，生成“新建活动”右侧抽屉。
字段：活动名称 Input 必填；活动类型 Select 必填；活动有效期 DateRange 必填；活动说明 Textarea。
```

### 2. 智客星完整页面

```text
使用 qifu-drawer-form，在智客星生成“新建活动”右侧抽屉的完整打开态页面。
platformKey：zhikexing
themeKey：zhikexing-green
componentMode：REAL_COMPONENT_ONLY
background.source：TEMPLATE
当前菜单：客户运营 / 活动管理

字段：活动名称 Input 必填；活动类型 Select 必填；活动有效期 DateRange 必填；活动说明 Textarea。
底部按钮：取消、确定。
```

### 3. 毓数平台

```text
使用 qifu-drawer-form，在毓数生成“编辑数据任务”右侧抽屉。
platformKey：yushu
themeKey：yushu-green
componentMode：REAL_COMPONENT_ONLY
compositionName：Qifu Drawer Form / Edit

字段：任务名称 Input 必填，默认值“用户标签同步”；执行周期 Select 必填，默认值“每日”；生效时间 DateRange；任务说明 Textarea。
底部按钮：取消、保存。
```

### 4. 智能运营 Golden Sample 抽屉

```text
使用 qifu-drawer-form，在智能运营平台生成“新增短信模板策略”右侧抽屉。
platformKey：zhineng-yunying
platformName：智能运营平台
themeKey：smartops-blue
themePrimary：#1677FF
componentMode：REAL_COMPONENT_ONLY
compositionName：Qifu Drawer Form / Sectioned Create
widthTier：680
使用“智能运营平台策略关联抽屉 Golden Sample”。

字段：策略名称 Input 必填；有效期 DateRange 必填；主模板 Select 必填并在下方展示模板明细表；关联运营策略 Multiple Select 必填并在下方展示策略明细表；灰度比例 Select 必填，默认值“100%”。
底部按钮：关闭、保存。
```

### 5. 智能运营正式完整页面

```text
使用 qifu-drawer-form，根据“智能运营平台策略关联抽屉 Golden Sample”生成完整打开态页面。
platformKey：zhineng-yunying
themeKey：smartops-blue
componentMode：REAL_COMPONENT_ONLY
background.source：EXISTING_LIST_PAGE
background.sourceNode：<已验收的智能运营平台列表页节点 ID>

在该列表页右侧打开“新增短信模板策略”抽屉。
不要复用智客星或毓数菜单；不要使用截图或图片作为正式底图。
```

## SmartOps Golden Sample 的固定规则

“新增短信模板策略”使用 `Qifu Drawer Form / Sectioned Create` 和 `680px` 宽度：

- 标题用 `标题/Large` `18/26`；关闭图标绑定 `qifu-icon-color-secondary`。
- “关联运营策略”标签使用 `Body/Regular` `14/22`；已选项是可关闭的 `Tag / small`。
- “主模板”和“关联运营策略”都按 `Select -> 8px -> 明细表` 组合；高度随表格内容撑开。
- 表格外层不加描边，只对表头加 `INNER_SHADOW`：`0 1 2 0 rgba(0,0,0,0.08)`。
- Footer 的关闭使用文字按钮，保存使用主按钮，两者均不加页面级描边。

完整字段和验收要求见 [智能运营平台策略关联抽屉 Golden Sample](references/golden-sample-smartops-strategy-drawer.md)。

## 输出时应看到什么

完成后，Skill 应返回节点 ID、`platformKey/themeKey` 回读、使用的组合、组件来源、字段清单，以及：

```text
structuralValidation = PASS | BLOCKED | FAIL
visualValidation     = PASS | BLOCKED | FAIL
```

只有两项都是 `PASS` 才能算正式完成。

## 文件导航

- [SKILL.md](SKILL.md)：输入契约、工作流、组件规则和验收清单。
- [平台与主题切换协议](references/platform-theme-switching.md)：平台识别和主题变量约束。
- [智能运营平台策略关联抽屉 Golden Sample](references/golden-sample-smartops-strategy-drawer.md)：本次智能运营抽屉的固定基线和完整提示词。
- [Figma 执行与结构化验收](references/figma-execution-validation.md)：组件实例、Slot 和属性回读检查。
