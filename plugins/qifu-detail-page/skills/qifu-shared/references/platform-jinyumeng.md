# 金毓盟平台资产适配

本轮登记已回读资产与主题，capabilities.drawer=pending-adapter、capabilities.detail=unsupported。列表生成继续使用独立 qfin-list-page 插件的金毓盟子 Skill；注册成功不代表抽屉、详情已完成生成验收。

## 真实来源

- 列表外壳：Templates / Jinyumeng / List Page Shell，5022:16，COMPONENT，1366×1024；使用真实实例。
- Header：4993:1440，1366×56；固定品牌和用户区，只写公开的账号名称属性。
- 菜单：JYM-SideMenuItem，4746:46261，24 个变体，208×48，Level=1/2/3。
- Workspace：5022:8，sidebarSlot=208px；Content Shell：5022:2，原生插槽 tabs/filter/action/table。
- 列表试稿：6017:2723；抽屉试稿：6089:64073；三种标签布局验证位于 Page 6082:61231。试稿不自动升级 Golden Sample。

## 主题与页面边界

主题键 jinyumeng-blue，绑定 basic 基础（VariableCollectionId:9:8）的金毓盟/Light（4717:0）。本次语义 brand/default 回读 #0F6FFC，仅用于校验；颜色不能代替变量绑定。

菜单、图标和控件取金毓盟真实组件。表单间距可参考已确认的智能运营布局原则，不能借用其菜单、Header 或主题。详情页只复用平台导航与视觉适配，不把详情写入列表 tableSlot 冒充支持。

抽屉专属控件、标签和分割线适配未完成前返回 BLOCKED_PLATFORM_ADAPTER；详情仍返回 UNSUPPORTED_PLATFORM。历史口述 token divider/primay 没有精确本地变量匹配；当前读到分割线/--qifu-divider-color-primary，先记录候选映射，不擅自改名或替换。
