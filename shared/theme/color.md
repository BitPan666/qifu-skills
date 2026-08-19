# Color Tokens

## 1. 语义分类

AI 以“用途”调用颜色，不以裸 HEX 调用。下表的 `variable-required` 项应优先继承真实组件的变量绑定。

| Token | 用途 | 状态 | 允许使用位置 |
|---|---|---|---|
| `color.text.primary` | 标题、表头、主要正文 | variable-required | Page Header、Table Header、Detail Label Value |
| `color.text.secondary` | 次要信息、说明、辅助文案 | variable-required | 筛选说明、元信息、时间线辅助文案 |
| `color.text.placeholder` | 空输入、弱提示 | variable-required | Input / Select / Textarea 实例 |
| `color.text.disabled` | 禁用内容 | variable-required | disabled 实例内部 |
| `color.text.link` | 可点击文字 | variable-required | 表格操作、详情跳转 |
| `color.brand.default` | 主操作、当前选中、焦点 | variable-required | Primary Button、选中导航、Focus ring |
| `color.success.default` | 成功、已启用、已完成 | variable-required | Tag、Alert、Result |
| `color.warning.default` | 提醒、风险待处理 | variable-required | Tag、Alert、表格状态 |
| `color.error.default` | 失败、危险、校验错误 | variable-required | Error state、Danger Button、FormItem required |
| `color.info.default` | 进行中、信息提示 | variable-required | Tag、Alert、通知 |
| `color.bg.page` | 页面底色 | variable-required | App / Workspace 根容器 |
| `color.bg.surface` | 主内容容器 | variable-required | Page Surface、Card、Table Surface |
| `color.bg.subtle` | 次级容器、表头或弱分区 | variable-required | Filter 区、Table Header、Skeleton |
| `color.bg.hover` | 悬浮背景 | variable-required | Row hover、Menu hover、Button hover |
| `color.border.default` | 常规边框 | variable-required | Input、Table、Card |
| `color.border.divider` | 分割线 | variable-required | Form Section、Table row、Detail Block |
| `color.mask.overlay` | Drawer / Dialog 浮层遮罩 | variable-required | Overlay 实例 |

## 2. 已确认的颜色规则

| Token / 规则 | 值 | 证据 | 状态 |
|---|---:|---|---|
| `color.filter.label` | `#565656` | `Filter Item-V2` 12px / 14px 标题 | confirmed |
| `color.form.required` | `#dc2626` | FormItem 必填星号 | confirmed |

## 3. 功能色调用规则

- 业务状态先使用 `Tag`、`Alert` 等真实实例的类型属性，避免手选功能色；
- 错误提示使用组件的 `error` 状态，不仅靠红色文本表达；
- 当前导航、当前 Tabs、表格选中和主按钮必须共享 `color.brand.default` 语义，而不是各自设置近似色；
- 禁用状态优先设置组件 `disabled=true`，不手动降透明度；
- 不将红、黄、绿作为唯一信息渠道，必须配合状态文案或图标。

## 4. Dark mode 预留

`color.*` 的语义名称在 Dark mode 中保持不变，只替换变量值。当前没有经过盘点的 Qifu Dark token；AI 不得引用或改写 TDesign 的蓝色、灰色、遮罩数值作为 Qifu Dark 值。
