# Qifu Theme / Figma Variables

本目录 **Figma Variables 是唯一的命名与值来源**。

2026-10-28新增 [`live-platform-bindings.json`](live-platform-bindings.json)：只采集五个语义颜色变量在四个平台Mode中的真实绑定与解析值。当前平台路由和颜色校验以该定向快照及theme-registry.json为准；下方279个变量的tokens/source/Less是保留原采集日期的历史全量导出，不代表本轮重新导出。两个来源重叠时，定向快照覆盖当前平台绑定核验；未核验字段必须实时回读，不补造历史值。

- Figma 文件：[奇富科技中后台组件库-新](https://www.figma.com/design/gTV3VdC6a5e9vpkRHIZSXA/%E5%A5%87%E5%AF%8C%E7%A7%91%E6%8A%80%E4%B8%AD%E5%90%8E%E5%8F%B0%E7%BB%84%E4%BB%B6%E5%BA%93-%E6%96%B0?node-id=2874-9924&view=variables)
- 采集范围：`基础` 108、`色彩` 82、`字体` 27、`圆角` 7、`尺寸` 55，共 **279** 个变量。
- 原始数据：[`source/`](source/)；可供 AI 精确检索的总索引：[`tokens.json`](tokens.json)；平台注册主题映射：[`theme-registry.json`](theme-registry.json)。
- 组件绑定契约：[`component-token-contract.json`](component-token-contract.json)。它记录真实组件应绑定的变量，不复制变量值。
- 人读核对表：[`figma-variable-inventory.md`](figma-variable-inventory.md)。

## 目录

```text
skills/qifu-shared/theme/
├── _index.less
├── _light.less          # 基础 collection，默认导出毓数/Light
├── _font.less
├── _radius.less
├── _size.less
├── tokens.json          # collection / mode / Figma 原路径与真实值或 alias
├── theme-registry.json  # themeKey → collection mode / 颜色变量组 / 绑定策略
├── component-token-contract.json # 组件插槽 → 已存在的组件或语义变量
├── figma-variable-inventory.md
└── source/              # collection 级原始变量数据
```

## AI 调用规则

1. 先读取 `tokens.json`，再按 `source/<collection>.json` 查 `figmaPath`、`name`、`type`、`values`。
2. 仅使用 `figmaPath` 和 `name` 作为 Figma 资产名称。例如 `--qifu-text-color-primary`、`--qifu-bg-color-canvas`、`--qifu-size/16` 均保持原样。
3. `基础颜色拓展/brand/default` 这种路径是 Figma 的真实分组路径；不要擅自改为 `--qifu-brand-default`。
4. `.less` 内的 `@...` 标识符是为代码合法性生成的导出映射（`/`、`%` 等字符被转换），**不是 Figma 原变量名**；回写 Figma 或描述设计资产时必须用 JSON 中的原路径。
5. 当前实时collection名为 `basic 基础`（`VariableCollectionId:9:8`），有 `毓数/Light`、`智能运营/Light`、`金毓盟/Light`、`电销/Light` 四种Mode。智客星继承通过预检的模板绑定，不新建或假设专属Mode。`mode/green` 与 `mode/blue` 是 `色彩` collection 内的变量路径分组，不是 Figma mode；具体映射以 `theme-registry.json` 为准。

## Less 使用

```less
@import 'skills/qifu-shared/theme/_index.less';
// @qifu-text-color-primary  ← Figma: 文本颜色/--qifu-text-color-primary
```

> `tokens.json` 是 AI/自动化的权威输入；Less 是面向工程的辅助导出。

## 三层变量调用

当前 Figma 变量按以下层级使用；层级描述是 `tokens.json` 中的派生元数据，不改变 Figma 的原 collection、变量名或值。

1. **基础值**：`色彩`、`字体`、`圆角`、`尺寸`。其中的色阶和值不能被页面或实例直接绑定。
2. **语义值**：`基础` collection 中的背景、文本、边框、图标、菜单和投影变量。页面和尚未具备组件变量的组件只能绑定这一层。
3. **组件值**：`基础/组件`。当前仅 Tag 的四个 light 背景已真实存在；其他组件的已批准语义绑定与后续迁移位置见 `component-token-contract.json`。

内置主题中的 `primary` Hex 仅用于核对解析结果。调用时必须从 `theme-registry.json` 的 `semanticBindings` 取变量路径；只有 `custom` 主题可以把用户显式输入作为主题主色。
