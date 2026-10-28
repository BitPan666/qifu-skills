# 电销平台资产适配

本轮登记已回读资产与主题，capabilities.drawer=preflight-required、capabilities.detail=unsupported。列表生成继续使用独立 qfin-list-page 插件的电销子 Skill，不因共享注册而开放尚未验证的抽屉或详情生成。

## 真实来源

- 列表外壳：Templates / Dianxiao / List Page Shell，5829:31，COMPONENT，1366×768。
- Header：5824:4491，1366×56，固定品牌、签到、状态和用户区；当前不暴露可写业务属性。
- 业务菜单：5763:1753，36 个变体，200×40，Level=1/2/3；顶层分类：5762:1537。
- Workspace：5829:24；Content Shell：5829:15，原生插槽 tabs/filter/table，没有金毓盟的 actionSlot。
- 列表试稿：6034:4860；抽屉试稿：6089:64515；三种标签布局验证位于 Page 6082:61231。

## 平台隔离与主题

电销菜单5763:1753与智能运营菜单6158:1989是独立母组件。实例检查真实 mainComponent 所属组件集；Label#5763:0 等历史属性后缀不是母组件归属证据。智能运营适配不得改动电销菜单。

主题键 dianxiao-green，绑定 basic 基础（VariableCollectionId:9:8）的电销/Light（5722:0）。brand/default 实时值 #009E73；原始颜色变量组名为 mode/dianxian，保留库内原拼写。

17个固定一级菜单与侧栏规则由电销列表子 Skill 维护，共享层不复制业务菜单树。抽屉可参考毓数已确认的表单间距，但控件取电销模式下真实组件。普通Create/Edit已接入独立平台规则，逐次预检并验收；超出范围返回明确阻塞，详情返回UNSUPPORTED_PLATFORM。

## 当前抽屉执行入口

完整读取 `../../qifu-drawer-form/references/platform-backgrounds.md`，以其平台差异覆盖通用蓝图；执行 `../../qifu-drawer-form/scripts/plan_platform_drawer.py`。默认640宽、1366×768；支持Input/Select/DateRange/Textarea和默认标签排布。真实样本仅证明本轮Sectioned Create/Edit四字段场景，其他普通组合仍须逐次结构与截图验收。
