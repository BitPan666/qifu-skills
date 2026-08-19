# Qifu Skills

> 奇富 B 端 5 层 AI 设计体系的 skill 集合——把 Token、Component、Pattern、Page Archetype、Business 五层方法论,翻译成 AI 可执行的 Figma 生成 skill。

![Language](https://img.shields.io/badge/lang-Markdown-blue) ![Platform](https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex-orange) ![Status](https://img.shields.io/badge/status-active-brightgreen) ![License](https://img.shields.io/badge/scope-private-lightgrey)

---

## 这个仓库解决什么问题

B 端后台设计碎片化严重:每张页面都从零画图、组件绑定靠手、间距对齐靠眼。本仓库把"5 层 AI 设计体系"落到 **可执行的 Figma 生成 skill** 上:

- 输入:一句中文业务描述(如"在订阅管理下新建群组列表页")
- 输出:Figma 中**保持真实组件实例关系**的完整页面(不是截图、不是手绘)
- 沿途:有契约、有配方、有验证清单、有缺口记录

```
自然语言描述                        Figma 真实组件实例树
"在毓数新建群组列表页,              ── Header(Yushu Header-V2 真实实例)
 筛选有名称/状态/时间"      ──▶    ── SideMenu(SideMenuItem-V2 ×N)
                                   ── List Page Shell-V2
                                       ├── Filter Bar-V2(真实控件 32px)
                                       ├── Table Shell-V2(9 行示例)
                                       └── Pagination-V2
```

## 5 层 AI 设计体系

| 层级 | 名称 | 它是什么 | 在本仓库 |
|---|---|---|---|
| L1 | Design Token | 颜色 / 字体 / 圆角 / 间距 / 边框 | `shared/references/component-map.md` 第一段 |
| L2 | Component | 真实组件实例 + 节点 ID + 发布 Key | `shared/references/component-map.md` |
| L3 | Pattern | Filter Bar / Action Bar / DetailBlock 等组合区块 | 各 skill 的 `references/page-blueprint.md` |
| L4 | Page Archetype | 列表 / 抽屉表单 / 详情 / 向导… | `skills/qifu-*`(本仓库主资产) |
| L5 | Platform Adapter | 平台导航、品牌、术语、权限、业务槽位 | `shared/references/platform-*.md` |
| L6 | Business Page | 业务菜单树、用户上下文、业务名词 | 具体交付页面 |

**关键设计**:L1 / L2 / L5 是**跨原型共享资产**,只维护一份(`shared/references/`);L4 每新增一种原型,只需写 3 份新文件(SKILL.md + blueprint + compositions),复用骨架和共享层。

## 当前 Skill 家族

| Skill | 作用 |
|---|---|
| [qifu-b-end-design-system](./skills/qifu-b-end-design-system/) | 公司级编排入口：页面类型、Pattern、组件调用、跨平台 Adapter 与缺口治理 |

### 页面 Archetype Skills

| Skill | 覆盖场景 | 配方数 | 标准组合 |
|---|---|---|---:|---|
| [qifu-list-page](./skills/qifu-list-page/) | 列表 + 筛选 + 表格 + 批量 | 6 | Basic Table / Basic Filter / Advanced Filter / Selectable / Loading / Empty |
| [qifu-drawer-form](./skills/qifu-drawer-form/) | 右侧抽屉内新建 / 编辑 / 查看 | 5 | Simple Create / Sectioned Create / Advanced Create / Edit / Readonly |
| [qifu-detail-page](./skills/qifu-detail-page/) | 详情查看 + 局部操作 | 4 | Flat / Tabbed / Master Detail / Readonly |

**真实业务流串起来**:

```
列表页(list) ──点新建──▶ 抽屉表单(drawer-form)
   │                          │
   │                          └─保存─┐
   │                                 ▼
   └──点查看──▶ 详情页(detail) ◀──新建后跳转
                       │
                       └─点编辑──▶ 抽屉表单(Edit)
```

3 个 skill 边界清晰、互不重叠、可相互跳转,覆盖 B 端 90% 高频页面需求。

## 仓库结构

```
qifu-skills-repo/
├── README.md                        ← 你正在读的这份
├── shared/                          ← 跨原型共享资产(L1/L2/L5)
│   ├── theme/                       ← 主题 Token 索引（Color / Typography / Size / Radius / Shadow）
│   └── references/
│       ├── component-map.md         ← 全部真实组件的节点 ID / 发布 Key / 属性
│       ├── platform-yushu.md        ← 毓数平台导航基线 / 菜单树 / 图标映射
│       └── platform-generic.md      ← 未指定平台时的中性适配器
├── skills/                          ← L4 原型 skill 家族
│   ├── qifu-b-end-design-system/     ← 公司级页面抽象与组件调用编排
│   ├── qifu-list-page/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── page-blueprint.md
│   │   │   └── table-compositions.md
│   │   ├── agents/openai.yaml
│   │   └── README.md                ← 单个 skill 的详细说明
│   ├── qifu-drawer-form/            ← 同结构
│   └── qifu-detail-page/            ← 同结构
└── screenshots/                     ← 全仓库统一效果截图(待补)
```


## Theme Token 索引

参照 TDesign Web Theme 的目录分层，新增 Qifu 的主题调用索引：

- [Theme Index](./shared/theme/index.md)：Token 来源、状态与 AI 查询顺序；
- [Color](./shared/theme/color.md)：语义色、背景、边框、遮罩；
- [Typography](./shared/theme/typography.md)：标题、正文、筛选项与表格文字；
- [Size](./shared/theme/size.md)：页面、Pattern、控件与表格尺寸；
- [Radius](./shared/theme/radius.md)、[Shadow](./shared/theme/shadow.md)：仅通过真实实例/变量调用。

> 当前清单标记了 `confirmed`、`variable-required`、`reserved` 三类状态；AI 只能直接使用已确认数值，其他 Token 必须继承 Figma Variables 或真实组件实例。

## 架构与调用截图

### 公司级分层架构

![Qifu B 端 Design System 架构](./screenshots/overview/architecture.svg)

### AI 组件调用流程

![AI 组件调用流程](./screenshots/overview/ai-call-flow.svg)

### 跨平台页面迁移矩阵

![跨平台页面迁移矩阵](./screenshots/overview/platform-migration.svg)

> 以上图片是仓库文档用的结构说明图，不替代 Figma 中的真实组件实例。真实组件来源仍以“奇富科技中后台组件库 新”及 `shared/references/component-map.md` 为准。

## 快速开始

### 安装到 Claude Code

```bash
# 1. 克隆
git clone git@github.com:jingjingtu/qifu-skills.git
cd qifu-skills

# 2. 逐个把 skill 软链到 ~/.claude/skills
mkdir -p ~/.claude/skills
for s in qifu-b-end-design-system qifu-list-page qifu-drawer-form qifu-detail-page; do
  ln -sf "$(pwd)/skills/$s" ~/.claude/skills/$s
done

# 3. 在 Claude Code 中触发
#    $qifu-list-page / $qifu-drawer-form / $qifu-detail-page
```

### 安装到 Codex

```bash
# 1. 同上克隆

# 2. 软链到 Codex skills 目录
mkdir -p ~/.codex/skills
for s in qifu-b-end-design-system qifu-list-page qifu-drawer-form qifu-detail-page; do
  ln -sf "$(pwd)/skills/$s" ~/.codex/skills/$s
done
# Codex 通过每个 skill 下的 agents/openai.yaml 识别入口
```

### 在 Figma 中使用

需要:

- Figma 桌面端(选中目标 Page 后,AI 会在其中创建 Frame)
- 目标 Figma 文件已能访问「奇富科技中后台组件库 新」(文件 key `gTV3VdC6a5e9vpkRHIZSXA`)
- AI 客户端已配置 Figma MCP 工具(`use_figma`、`figma-generate-design` 等)

测试 / 效果验证 / Skill 回归时,统一放入 Page **测试**(node `3497:651`),禁止新建近义 Page。

## 截图展示

> 待补充。首次上传后,请按以下排列添加:

| 缩略 | 说明 | 来源 |
|---|---|---|
| `screenshots/01-list-page.png` | qifu-list-page 在毓数平台生成的列表页全景 | 真实 prompt 跑一次后截图 |
| `screenshots/02-drawer-form.png` | qifu-drawer-form 生成的"新建触发式任务"抽屉 | 已有 Figma 文件 |
| `screenshots/03-detail-page.png` | qifu-detail-page 生成的任务详情页 | 真实 prompt 跑一次后截图 |
| `screenshots/04-component-tree.png` | Figma 内的组件实例结构(展示"非手绘") | 任一页面右侧 Inspector 截图 |
| `screenshots/05-audit-missing.png` | Audit / Missing Components 缺口清单 | 跑出 Fallback 时截图 |

## 边界声明

每个 skill 都有明确的"不做什么",在 `SKILL.md` 的 frontmatter `description` 字段和"硬性约束"一节:

- **qifu-list-page** 不做:复杂分析看板、编辑表单、详情页、树表、高度定制工作台
- **qifu-drawer-form** 不做:复杂看板、向导流、带批量编辑的列表页
- **qifu-detail-page** 不做:新建/编辑表单(走 drawer-form)、多记录列表(走 list-page)、数据看板、树表

跨原型借用组合名是**严格禁止**的,每个 skill 的 compositions 只对自己的原型负责。

## 设计原则

- **真实组件实例,不手绘 / 不分离 / 不改母版**
- **组合名严格注册,L4 一个 skill 一种原型**
- **共享资产跨原型复用,不拷贝**
- **缺口诚实记录 Fallback / Audit,不冒充已支持**
- **设计师是规则制定者与验收者,AI 是执行者**

## 路线图

- [x] 5 层方法论(PPT 汇报)
- [x] qifu-list-page(2026-08-12 前已有)
- [x] qifu-drawer-form(2026-08-12)
- [x] qifu-detail-page(2026-08-12)
- [ ] qifu-wizard(分步向导,如 AB 实验创建)
- [ ] qifu-workbench(工作台)
- [ ] qifu-page-form(整页表单,非抽屉)
- [ ] 用真实业务跑通 3 个 skill 并沉淀"已知限制"清单

## 相关链接

- 方法论汇报:可在 [design-meeting](https://github.com/jingjingtu/design-meeting)(私有)找到本期 PPT
- 月报生成:[monthly-report](https://github.com/jingjingtu/monthly-report)
- HTML → Figma 高保真导入:[html-to-figma-fidelity](https://github.com/jingjingtu/html-to-figma-fidelity)

---

**维护者**:师静雅 · Qifu B 端设计
**首次推送**:2026-08-13
**结构版本**:v1.0(5 层体系落地的最初形态)

## Codex installation

The Qifu page skills share component and navigation references. Install all four packages together so every page skill can resolve its dependencies:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo jingjingtu/qifu-skills \
  --path skills/qifu-shared skills/qifu-list-page skills/qifu-detail-page skills/qifu-drawer-form \
  --method git
```

`qifu-shared` is an internal dependency package; it should remain installed beside the three page-generation skills.
