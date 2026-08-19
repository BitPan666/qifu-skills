# Qifu Web Theme（AI 调用主题索引）

本目录是奇富科技中后台组件库“新”的**主题 Token 清单与调用契约**。它借鉴 TDesign `style/web/theme` 的分类，但不复制其颜色数值：Qifu 的真实值必须以 Figma Variables、组件实例和 `component-map.md` 的已盘点数据为准。

```text
shared/theme/
├── index.md       # 主题入口、Token 查询顺序、状态
├── color.md       # 语义色、文本、背景、边框、遮罩
├── typography.md  # 字体、字号、行高、字重、层级
├── size.md        # 8px 间距体系、控件尺寸、页面/表格规格
├── radius.md      # 圆角语义及调用边界
└── shadow.md      # 层级、遮罩与浮层投影
```

## 与 TDesign 的对应关系

| TDesign `style/web/theme` | Qifu 文件 | AI 调用方式 |
|---|---|---|
| `_index.less` | `index.md` | 先读取，确认 Token 来源与主题状态 |
| `_light.less` | `color.md` 的 Light 基线 | 默认 Web 后台主题 |
| `_dark.less` | `color.md` 的 Dark 预留区 | 未经组件库盘点，不得凭空产出 Dark 数值 |
| `_font.less` | `typography.md` | 按语义文本层级而非裸字号调用 |
| `_size.less` | `size.md` | 按页面、区块、控件、表格四层调用 |
| `_radius.less` | `radius.md` | 只用组件库已暴露的圆角或实例 |

## 调用优先级

```text
Figma Variable（已绑定）
  → 真实组件 INSTANCE 的公开属性
  → 本目录的已确认 Token
  → Pattern / Page blueprint 的固定几何规则
  → Fallback + Audit / Missing Components
```

禁止将 TDesign 的 `--td-*` 数值直接移植到 Qifu 页面；TDesign 仅提供“如何分层和命名”的参考。
