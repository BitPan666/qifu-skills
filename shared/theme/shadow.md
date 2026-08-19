# Shadow & Layer Tokens

## 1. 层级语义

| Token | 语义 | 推荐组件 | 状态 |
|---|---|---|---|
| `elevation.base` | 普通页面/表格容器，通常不依赖浮层阴影 | Page Surface、Table Shell | variable-required |
| `elevation.hover` | 可悬浮的行、卡片或菜单项 | Table Row、Card、Menu Item | variable-required |
| `elevation.popup` | 下拉、气泡确认、选择器 | Select Menu、Dropdown、Popconfirm | variable-required |
| `elevation.overlay` | Drawer、Dialog、Notification 等最高层浮层 | Drawer、Dialog、Message | variable-required |
| `mask.overlay` | Overlay 与背景的层级隔离 | Drawer / Dialog Mask | variable-required |

## 2. 调用规则

- 阴影必须跟随正式 Popup / Drawer / Dialog 实例；不手绘或复制 CSS 阴影；
- 普通表格、筛选栏和 Page Surface 不为“显得高级”额外加投影；
- Overlay 使用组件库提供的遮罩，不通过自定义透明黑矩形替代；
- 一个层级只使用一种阴影语义；同层 Popup 不得出现深浅不一致的手工阴影；
- Dark mode 的遮罩与阴影值目前为 `reserved`，需要 Variables 盘点后才能启用。
