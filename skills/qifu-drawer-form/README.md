# qifu-drawer-form

在 Figma 中生成可继续编辑的奇富后台右侧抽屉，复用真实组件实例，不把控件画成分散的矩形和文字。

本 README 只展示两个已验证的业务案例：**智能运营平台的“新增短信模板策略”**和**智客星的“超频流控配置”**。两个案例共用下方同一套提示词模板；其他平台、数据详情和内部路由规则不在这里展开。

## 已验证的业务案例

![智能运营平台新增短信模板策略](assets/screenshots/smartops-strategy-drawer.png)

- [查看 Figma Golden Sample](https://www.figma.com/design/gTV3VdC6a5e9vpkRHIZSXA/%E5%A5%87%E5%AF%8C%E7%A7%91%E6%8A%80%E4%B8%AD%E5%90%8E%E5%8F%B0%E7%BB%84%E4%BB%B6%E5%BA%93-%E6%96%B0?node-id=5066-9446)：`1366 × 768`，包含结构预览底图、蒙层和右侧 `680px` 抽屉。
- 已验证组合：策略名称、有效期、主模板 + 模板明细表、关联运营策略 + 多选 Tag + 策略明细表、灰度比例，以及“关闭 / 保存”Footer。
- 结构预览只表达抽屉打开态；未提供已验收的智能运营列表页时，不代表已经完成正式平台底图验收。

![智客星超频流控配置](assets/screenshots/zhikexing-overfrequency-drawer.png)

- 智客星“超频流控配置”：`1366 × 768` 打开态，包含智客星列表页底图、蒙层和右侧抽屉。
- 已验证组合：规则名称、适用人群类型、适用人群、策略类型、触达间隔、单日上限、生效时间、优先级、状态和规则说明，以及“取消 / 保存”Footer。
- 截图来自本机可交互页面的真实打开态，用于说明业务结构与视觉目标；正式 Figma 交付仍需按 Skill 的组件实例和结构化验收执行。

## 安装到个人 Skills

使用者需要已连接自己的 Figma 账号，并拥有目标业务文件和「奇富科技中后台组件库 新」的访问权限。

### Codex

```bash
git clone https://github.com/jingjingtu/qifu-skills.git ~/Documents/qifu-skills
mkdir -p ~/.codex/skills
ln -sfn ~/Documents/qifu-skills/skills/qifu-shared ~/.codex/skills/qifu-shared
ln -sfn ~/Documents/qifu-skills/skills/qifu-drawer-form ~/.codex/skills/qifu-drawer-form
```

### Claude Code

```bash
git clone https://github.com/jingjingtu/qifu-skills.git ~/Documents/qifu-skills
mkdir -p ~/.claude/skills
ln -sfn ~/Documents/qifu-skills/skills/qifu-shared ~/.claude/skills/qifu-shared
ln -sfn ~/Documents/qifu-skills/skills/qifu-drawer-form ~/.claude/skills/qifu-drawer-form
```

完成后新开任务，使用 `$qifu-drawer-form` 或直接说“使用 qifu-drawer-form”。更新时进入 `~/Documents/qifu-skills` 执行 `git pull`；软链不需要重新创建。

## 一套模板

只复制下面这一套。替换 `<...>` 内的业务值；没有的分区或字段直接删除，不保留占位符。

```text
使用 qifu-drawer-form，并调用 @figma 插件，在 <目标 Figma 文件或节点链接> 的 <目标 Page 画布> 中 <指定落点，例如画布空白处或参考 Frame 右侧空白处> 生成“<新建 / 编辑 / 查看><业务对象>”右侧抽屉。
不要新建 Figma Page；只在上述目标画布内生成。

页面平台：<智能运营平台 / 智客星>。
platformKey：<zhineng-yunying / zhikexing>
themeKey：<smartops-blue / zhikexing-green>
componentMode：REAL_COMPONENT_ONLY
compositionName：Qifu Drawer Form / Sectioned Create
widthTier：600
presentationMode：DRAWER_OPEN_WITH_BACKGROUND
background.source：<AUTO / TEMPLATE / EXISTING_LIST_PAGE / STRUCTURE_PREVIEW>
<使用已有已验收列表页时填写> background.sourceNode：<列表页节点 ID>

分区：
- <分区一，例如基础信息>：<字段标签> <控件> <必填或选填>；<字段标签> <控件> <必填或选填>。
- <分区二，例如策略配置>：<字段标签> <控件> <必填或选填>；<字段标签> <控件> <必填或选填>。

<编辑场景补充> 默认值：<字段标签>=<业务值>。
底部按钮：<关闭 / 取消>、<保存 / 确定>。
```

`目标 Figma 文件 + 目标 Page + 指定落点` 决定生成到哪里；`页面平台 / platformKey / themeKey` 只决定页面壳、业务术语和主题，不能代替 Figma 生成位置。

`background.source=AUTO` 会优先使用已验收列表页；未提供时生成 `1366 × 768` 的结构预览底图 + 蒙层 + 抽屉，不会生成裸抽屉。

普通表单默认 `widthTier：600`；`680` 仅用于数据详情和智能运营策略关联 Golden Sample，复杂双列使用 `840`，多个复合规则区或双列表格使用 `960`。

## 两份案例提示词

### 案例一：智能运营平台“新增短信模板策略”

```text
使用 qifu-drawer-form，并调用 @figma 插件，在 <目标 Figma 文件或节点链接> 的 <目标 Page 画布> 中 <指定落点> 生成“新增短信模板策略”右侧抽屉。
不要新建 Figma Page；只在上述目标画布内生成。

页面平台：智能运营平台。
platformKey：zhineng-yunying
themeKey：smartops-blue
themePrimary：#1677FF
componentMode：REAL_COMPONENT_ONLY
compositionName：Qifu Drawer Form / Sectioned Create
widthTier：680
presentationMode：DRAWER_OPEN_WITH_BACKGROUND
background.source：AUTO
使用“智能运营平台策略关联抽屉 Golden Sample”。

分区：
- 基础信息：策略名称 Input 必填；有效期 DateRange 必填。
- 策略配置：主模板 Select 必填；选择后在下方展示模板明细表。关联运营策略 Multiple Select 必填，已选项显示可关闭 Tag；选择后在下方展示策略明细表。灰度比例 Select 必填，选项“10%/30%/50%/100%”，默认值“100%”。

底部按钮：关闭、保存。
```

### 案例二：智客星“超频流控配置”

```text
使用 qifu-drawer-form，并调用 @figma 插件，在 <目标 Figma 文件或节点链接> 的 <目标 Page 画布> 中 <指定落点> 生成“超频流控配置”右侧抽屉。
不要新建 Figma Page；只在上述目标画布内生成。

页面平台：智客星。
platformKey：zhikexing
themeKey：zhikexing-green
componentMode：REAL_COMPONENT_ONLY
compositionName：Qifu Drawer Form / Sectioned Create
widthTier：600
presentationMode：DRAWER_OPEN_WITH_BACKGROUND
background.source：TEMPLATE

分区：
- 基础信息：规则名称 Input 必填；适用人群类型 Radio.Group 必填，选项“人群包/客群标签”；适用人群 Search 必填。
- 策略配置：策略类型 Select 必填；触达间隔 InputNumber 必填，单位“分钟”；单日上限 InputNumber 必填，单位“次/日”；生效时间 Radio.Group 必填，选项“全天/指定时间段”；优先级 Select 必填。
- 状态与说明：状态 Switch 选填，默认“启用”；规则说明 Textarea 选填，rows=4。

底部按钮：取消、保存。
```

## 字段怎么写

提示词按“**字段名 + 控件 + 必填/选填 + 默认值、选项或说明**”描述即可；无需填写 Figma 节点 ID 或组件内部路径。

| 业务字段 | 提示词写法 | Skill 使用的真实组件 |
| --- | --- | --- |
| 短文本 | `策略名称 Input 必填，placeholder“请输入策略名称”` | `Input / Base-V2` |
| 单选下拉 | `灰度比例 Select 必填，选项“10%/30%/50%/100%”` | `Select / Base` |
| 多选下拉 | `关联运营策略 Multiple Select 必填，已选项显示可关闭 Tag` | `Select / Base` 多选 + `Tag / small` |
| 日期范围 | `有效期 DateRange 必填` | `DatePicker / DateRange` |
| 长文本 | `策略说明 Textarea 选填，rows=4` | `Textarea` |
| 选择后展示明细 | `主模板 Select 必填；选择后在下方展示模板明细表` | `Select / Base` + 真实表格组合 |

## 智能运营案例固定规则

- 标题使用 `标题/Large` `18/26`；关闭图标绑定 `qifu-icon-color-secondary`。
- “关联运营策略”标签使用 `Body/Regular` `14/22`；已选项使用可关闭的 `Tag / small`。
- “主模板”和“关联运营策略”都遵循 `Select -> 8px -> 明细表`，高度随表格内容撑开。
- 表格外层不加描边；只对表头加 `INNER_SHADOW`：`0 1 2 0 rgba(0,0,0,0.08)`。
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
- [智能运营平台策略关联抽屉 Golden Sample](references/golden-sample-smartops-strategy-drawer.md)：完整字段与验收基线。
- [Figma 执行与结构化验收](references/figma-execution-validation.md)：组件实例、Slot 和属性回读检查。
