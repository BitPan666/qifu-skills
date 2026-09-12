# Platform Adapter：平台适配器契约

## 1. 适配器的职责

Platform Adapter 是把通用 Page Archetype 落到具体平台的薄层配置，不是另一套组件库。每个平台一个文件：`qifu-shared/references/platform-<platform>.md`。

## 2. 推荐格式

```yaml
adapter:
  id: platform-yushu
  displayName: 毓数平台
  version: 2026-07
  shell:
    header: Yushu Header-V2
    sidebar: SideMenuItem-V2
    breadcrumb: BreadcrumbItem
    contentMaxWidth: 1440
  navigation:
    menuSource: platform-yushu.md
    selectedRule: leaf-selected + ancestor-highlight
  vocabulary:
    list: 数据列表
    detail: 详情
    create: 新建
  theme:
    primary: component-library-default
  slots:
    - name: audience-selector
      allowed: [custom-instance, audited-fallback]
  permissions:
    actionVisibility: hide-when-forbidden
```

## 3. 必须提供的内容

1. 平台 ID、显示名、版本与负责人；
2. Header、SideMenu、Breadcrumb 的正式组件名；
3. 菜单树和当前页/祖先高亮规则；
4. 平台术语、Logo、用户区和品牌主题；
5. 平台专属 Slot 及其允许的组件；
6. 权限、数据范围、默认状态和空态文案规则；
7. 已知缺口与迁移注意事项。

## 4. 通用平台规则

当用户没有指定平台、或明确要求中性跨平台草案时：

- 使用 `platform-generic`；
- Header 和侧栏使用已确认的通用组件或中性占位；
- 不虚构平台菜单；
- 用 `Adapter TODO` 标记待补信息；
- 页面仍必须完成 Archetype、Pattern 和组件级验证。

用户明确指定的平台尚未注册时返回 `UNSUPPORTED_PLATFORM`。只有用户明确要求建立新 Adapter 时才进入平台盘点，不把 `platform-generic` 伪装成该平台。`audited-fallback` 仍须满足共享调用基线的 `COMPONENT_MISSING + 用户明确授权` 条件。

## 5. 禁止事项

- 在共享组件名中写 `YushuSelect`、`RiskTable` 等平台前缀；
- 为一个平台复制一整套 List / Detail / Form 页面 Skill；
- 通过分离实例满足平台定制；
- 把平台业务组件偷偷写进通用组件注册表；
- 用 Adapter 覆盖组件库的 Token、状态和无障碍约束。
