# 智能运营平台适配器

## 平台与真实外壳

platformKey=zhineng-yunying；默认主题 smartops-blue。2026-10-28已回读独立基础外壳；shellReadiness=source-verified 只表示来源存在，不代表三类页面生成验收通过。

| 资产 | 节点 | 类型与尺寸 |
| --- | --- | --- |
| 基础外壳 | 6155:1851 | FRAME，1366×768 |
| 顶部 | 6148:32454 | FRAME，1366×48 |
| 独立菜单组件集 | 6158:1989 | COMPONENT_SET，24变体，Level=1/2，单项200×40 |
| 已组装菜单 | 6155:1852 | FRAME，200×680，17项，间距0 |
| 工作区页签 | 6156:1989 | FRAME，1134×38 |
| 空白内容背景 | 6148:34365 | RECTANGLE，x216/y102，1134×633 |

基础外壳不是已发布组件，不使用 createInstance。后续先 clone-frame 保留可编辑副本，再在副本的内容背景范围内新建内容容器；RECTANGLE没有原生Slot，也不能appendChild。空白内容是有效外壳的一部分，不重搭Header、菜单或页签。

菜单实例必须归属6158:1989，禁止使用或修改电销5763:1753。历史属性Key后缀可能保留#5763，不能用它推断母版归属；回查mainComponent及其父组件集后再操作。

## 生成与背景状态

- 本轮列表pending-adapter，详情unsupported；共享注册不开放这两类工作流。
- 抽屉preflight-required：抽屉本体已有Golden Sample 5058:9322；完整打开态5066:9446使用中性STRUCTURE_PREVIEW，仍为PREVIEW_ONLY。
- 正式背景优先用户提供并验收的EXISTING_LIST_PAGE；没有时继续STRUCTURE_PREVIEW + Overlay Mask。新外壳可用于后续创建业务背景，但不能把空白壳存在直接写成已验收列表页。
- 外壳有7处文字尚未绑定Text Style，其中4处来自嵌套Tag标签。登记STYLE_MISSING / COMPONENT_SOURCE_GAP，不分离实例或覆盖母版字体，不借用其他平台底图。

## 主题

绑定basic 基础（VariableCollectionId:9:8）的智能运营/Light（2158:0），优先语义变量基础颜色拓展/brand/default与文本颜色/--qifu-text-color-link。本次实时brand/default为#1969F1；历史#1677FF及旧Scene Themes变量不覆盖当前语义绑定。Hex只用于回读核对。

单次或批量正式验收仍要求平台来源、主题、文字样式、结构和视觉全部通过；批量保持公共baseDrawer内容指纹一致。
