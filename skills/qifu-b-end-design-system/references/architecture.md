# 公司级 B 端组件库架构

## 1. 从 TDesign common 借鉴什么

`tdesign-common` 的核心启发不是照抄目录名，而是保持“公共资产、端/平台实现、文档与 AI 入口”分离：

| TDesign common | Qifu B 端对应物 | 说明 |
|---|---|---|
| `style/` | `shared/` + Figma 组件库 | 共享 Token、组件外观、布局和状态基线 |
| `style/web` / `style/mobile` | `platform-*` / 未来 `channel-*` | 平台或终端适配，不复制共享组件 |
| `js/<component>` | Component contract + Figma 属性 | 把组件名、变体、行为和调用参数结构化 |
| `docs/web/api` | `references/*` + 组件注册表 | AI 只读取与当前任务有关的文档 |
| `docs/mcp` | Skill 调用协议 | 先发现组件，再按契约生成实例 |
| 组件映射表 | `shared/references/component-map.md` | 节点 ID、发布 Key、属性、缺口、版本 |

## 2. 推荐仓库布局

```text
qifu-skills/
├── shared/
│   ├── tokens/                       # 可选：Token 导出
│   ├── references/
│   │   ├── component-map.md          # L1/L2 共享注册表
│   │   ├── platform-generic.md       # 通用平台适配器
│   │   └── platform-<name>.md        # 各平台差异
│   └── schemas/                      # PageSpec / ComponentSpec / AuditSpec
├── skills/
│   ├── qifu-b-end-design-system/     # 公司级编排入口
│   ├── qifu-list-page/               # 页面 Archetype
│   ├── qifu-detail-page/
│   ├── qifu-drawer-form/
│   ├── qifu-dashboard/               # 后续新增
│   ├── qifu-workspace/
│   ├── qifu-tree-table/
│   ├── qifu-wizard/
│   └── qifu-permission-page/
├── _docs/
│   ├── validation-log.md
│   └── limit-backfill.md
└── README.md
```

## 3. 维护规则

- **共享组件只登记一次**：任何页面 Skill 不复制 component-map；
- **平台差异只写 Adapter**：不要在 Component 名称中塞平台名；
- **Archetype 不能按业务菜单命名**：使用 `List / Detail / Drawer Form` 等稳定类型；
- **Pattern 优先于新组件**：能用合法组合实现时，不新增母版；
- **缺口可追踪**：Fallback 必须有 capability 名、场景、临时方案和建议属性；
- **版本可核对**：登记盘点日期、Figma 文件 Key、节点 ID、发布 Key 和变更原因。
