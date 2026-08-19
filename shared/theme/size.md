# Size Tokens

## 1. 尺寸层级

Qifu 页面按四层使用尺寸：`canvas → surface → pattern → component`。不要将页面外边距、区块间距、字段间距和控件高度混作一个“spacing”。

## 2. 已确认页面与 Pattern 尺寸

| Token | 值 | 用途 | 状态 |
|---|---:|---|---|
| `size.canvas.default` | `1366 × 768` | 未指定画板时的 List Page 默认画板 | confirmed |
| `size.canvas.wide` | `1920 × 1080` | 常规画板无法容纳信息、或明确需要宽屏时 | confirmed |
| `space.page.outer` | 12px | Page Surface 与 Content 的外侧空间 | confirmed |
| `space.surface.inner` | 16px | Page Surface 内边距 | confirmed |
| `space.block` | 12px | PageHeader / Filter Bar / Action Bar / Table Shell 相邻间距 | confirmed |
| `space.filter.item` | 12px | 筛选行中筛选项横向与换行间距 | confirmed |
| `space.filter.label-control` | 8px | 带标题筛选项中 Label 与控件间距 | confirmed |
| `space.table.pagination.y` | 12px | Table Shell V2 Pagination Slot 上下内边距 | confirmed |
| `space.form.section` | 24px | Drawer Form 的 Section 之间 | confirmed |
| `space.form.field` | 16px | Drawer Form 字段之间 | confirmed |
| `space.form.label-control` | 12px | Drawer Form label 与控件之间 | confirmed |

## 3. 组件高度与宽度

| Token | 值 | 组件 / 场景 | 状态 |
|---|---:|---|---|
| `size.control.default` | 32px | 常规 List Filter：Filter Item、Input、Select、Button | confirmed |
| `size.filter.compact` | 28px | 紧凑筛选模式 | confirmed |
| `size.table.row.large` | 44px | Table 大规格行高 | confirmed |
| `size.table.row.medium` | 40px | Table 中规格行高 | confirmed |
| `size.table.row.small` | 36px | Table 小规格行高 | confirmed |
| `size.filter.width.xs` | 120px | 短枚举、布尔筛选 | confirmed |
| `size.filter.width.s` | 160px | 短字段筛选 | confirmed |
| `size.filter.width.m` | 200px | 默认筛选项 | confirmed |
| `size.filter.width.l` | 304px | 日期范围、较长文本 | confirmed |
| `size.filter.width.xl` | 408px | 长文本、复杂条件 | confirmed |
| `size.drawer.s/m/l` | 480 / 640 / 840px | Drawer Form 宽度档位 | confirmed |

## 4. 调用约束

- Filter Item 是 `FIXED`；父级 Slot 可 `WRAP`，但筛选项不可 `FILL` 等分拉伸；
- 常规列表页面默认使用 32px 控件与 44px 表格行；紧凑模式必须由 PageSpec 明确指定；
- `1366 × 768` 常规列表优先显示 9 条不同数据行；
- 宽屏画板不能只 resize 根 Frame，必须同步调整 Page Surface、List Page Shell、Table Shell 和列宽；
- 所有 Auto Layout 留白优先绑定 Figma 已有 spacing variable；表中数值是变量未暴露时的已确认降级值。
