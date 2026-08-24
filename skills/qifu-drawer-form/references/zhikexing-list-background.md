# 智客星列表页底图协议

仅当 `platform=zhikexing` 且 `presentationMode=OVERLAY_ON_ZHIKEXING_LIST` 时启用。本协议不是新的抽屉组合；抽屉仍按 `drawer-compositions.md` 选择 `compositionName`。未指定展示方式时固定为 `STANDALONE`，只生成抽屉。

## 输入

```text
presentationMode  STANDALONE | OVERLAY_ON_ZHIKEXING_LIST
background
  source          TEMPLATE(默认) | EXISTING_LIST_PAGE
  sourceNode      EXISTING_LIST_PAGE 时必填
  sidePath[]      仅控制底图已有菜单的展开与选中
  pageName        仅用于 Scene 命名
```

- `TEMPLATE` 复制 `zhikexing-list-page` 的人工基线 `4892:34812`，即 `Template / List Page / 智客星 / 1440 / 手动调整`；真实尺寸必须为 `1366 x 768`。
- `EXISTING_LIST_PAGE` 必须是用户明确指定、已通过 `zhikexing-list-page` 结构化验收的 `1366 x 768` 页面。
- 模板或背景页面不可解析时返回 `BACKGROUND_TEMPLATE_MISSING`，不得手绘、截图化或展平底图。

## 读取与边界

启用前完整读取 `../zhikexing-list-page/SKILL.md`、`platform-zhikexing.md`、`component-invocation-contract.md` 与 `structural-validation.md`。

不得写入底图的 `pageHeaderSlot`、`filterBarSlot`、`tableSlot`、`rowsSlot`、`cellsSlot` 或 `paginationSlot`。需要变更底图业务结构时，先用 `zhikexing-list-page` 单独生成和验收，再作为 `EXISTING_LIST_PAGE` 使用。

## 场景结构与验收

```text
Scene / Drawer / <pageName> / <drawerTitle>       1366 x 768, clip content=true
├── Background / Zhikexing List Page              1366 x 768, whole-frame clone
├── Overlay Mask                                  1366 x 768, semantic overlay variable
└── Drawer / <object> / <action>                  right aligned, width=DrawerSpec.widthTier
```

- Scene、Background、Overlay Mask、Drawer 使用整数几何；图层顺序严格为 Background < Overlay Mask < Drawer。
- Background 保留真实组件实例、变量、文本样式与 Slot 内容关系；不得缩放、分离实例或改为截图。
- Overlay Mask 覆盖完整 Scene、绑定组件库既有语义遮罩变量；变量不可解析时返回 `STYLE_MISSING`，不得手填透明黑色。
- Drawer 贴 Scene 右侧、上下贴边；截图必须同时可见压暗底图和清晰抽屉，无溢出或裁切。
