# 智客星列表页底图协议

正式抽屉交付默认启用本协议：先生成完整 `1366×768` 页面打开态，再把右侧抽屉放在底图和蒙层之上。本协议不是新的抽屉组合；抽屉仍按 `drawer-compositions.md` 选择 `compositionName`。`STANDALONE_DEBUG` 仅用于用户明确要求“内部调试抽屉本体/不交付”时检查抽屉结构，不能作为正式交付结果。

## 输入

```text
presentationMode  DRAWER_OPEN_WITH_BACKGROUND(默认) | OVERLAY_ON_ZHIKEXING_LIST(智客星兼容别名) | STANDALONE_DEBUG
background
  source          TEMPLATE(智客星默认) | EXISTING_LIST_PAGE
  sourceNode      EXISTING_LIST_PAGE 时必填
  sidePath[]      仅控制底图已有菜单的展开与选中
  pageName        仅用于 Scene 命名
```

- `TEMPLATE` 复制 `zhikexing-list-page` 的人工基线 `4892:34812`，即 `Template / List Page / 智客星 / 1440 / 手动调整`；真实尺寸必须为 `1366 x 768`。
- `EXISTING_LIST_PAGE` 必须是用户明确指定、已通过 `zhikexing-list-page` 结构化验收的 `1366 x 768` 页面。
- 智客星未提供 `background` 时，`TEMPLATE` 为默认来源。模板或背景页面不可解析时返回 `BACKGROUND_TEMPLATE_MISSING`，不得手绘、截图化或展平底图。
- 非智客星平台未提供已批准平台模板或 `EXISTING_LIST_PAGE` 时，返回 `BACKGROUND_TEMPLATE_MISSING`；不得退回裸抽屉，也不得借用其他平台菜单冒充。

## 读取与边界

启用前完整读取 `../zhikexing-list-page/SKILL.md`、`platform-zhikexing.md`、`component-invocation-contract.md` 与 `structural-validation.md`。

不得写入底图的 `pageHeaderSlot`、`filterBarSlot`、`tableSlot`、`rowsSlot`、`cellsSlot` 或 `paginationSlot`。需要变更底图业务结构时，先用 `zhikexing-list-page` 单独生成和验收，再作为 `EXISTING_LIST_PAGE` 使用。

## 场景结构与验收

```text
Scene / Drawer / <pageName> / <drawerTitle>       1366 x 768, clip content=true
├── Background / <Platform> List Page             1366 x 768, whole-frame clone
├── Overlay Mask                                  1366 x 768, semantic overlay variable
└── Drawer / <object> / <action>                  right aligned, width=DrawerSpec.widthTier
```

- Scene、Background、Overlay Mask、Drawer 使用整数几何；图层顺序严格为 Background < Overlay Mask < Drawer。
- Background 保留真实组件实例、变量、文本样式与 Slot 内容关系；不得缩放、分离实例或改为截图。
- Overlay Mask 覆盖完整 Scene、绑定组件库既有语义遮罩变量；变量不可解析时返回 `STYLE_MISSING`，不得手填透明黑色。
- Drawer 贴 Scene 右侧、上下贴边；截图必须同时可见压暗底图和清晰抽屉，无溢出或裁切。
