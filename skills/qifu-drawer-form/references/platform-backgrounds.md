# 金毓盟与电销完整背景抽屉

本协议仅覆盖金毓盟/电销，优先于通用蓝图和智客星48px/200px背景协议。其他平台继续使用其自身Adapter。当前两平台drawer=preflight-required，已有普通Create/Edit规则；没有开放数据详情、Readonly、Advanced Create、其他宽度或其他标签排布。

## 写前计划

完整读取当前shared平台Adapter与平台注册表drawerAdapter，执行 `python3 scripts/plan_platform_drawer.py --spec <JSON>`。该命令只读；注册表可关闭能力或限制操作、控件、readiness、宽度、标签和viewport，计划成功不代表Figma通过。

本轮背景模式只支持AUTO（默认）与EXISTING_LIST_PAGE。显式EXISTING必须提供本平台表中背景业务来源或已验收Create Scene的sourceNode；AUTO缺省归一化为背景业务来源。计划输出background保留选定来源，sceneSourceNodeId是组装参考，不替换显式请求。TEMPLATE、STRUCTURE_PREVIEW与其他模式尚未在这两个Adapter实现，明确阻塞；不得套用通用协议静默改成真实背景。

范围：1366×768 Scene，640宽；Simple Create（单区≤6字段）、Sectioned Create（2–3区，≤15字段）、Edit（需回填）。控件仅Input/Select/DateRange/Textarea。金毓盟默认上置标签，电销默认左侧标签；其他标签模式、480/680/840/960宽度和复杂控件需新一轮适配，不能静默近似。

## 来源和平台边界

| 项目 | 金毓盟 | 电销 |
| --- | --- | --- |
| 当前已验收Create Scene | 6197:8368 | 6205:11709 |
| 当前已验收Edit Scene | 6204:10171 | 6205:14118 |
| 背景业务来源 | 6017:2723 | 6034:4860 |
| Shell真实owner | 5022:16 | 5829:31 |
| Header真实owner/高度 | 4993:1440 / 56 | 5824:4491 / 56 |
| 菜单owner/宽度 | 4746:46261 / 208 | 5763:1753 / 200 |
| Mode | 4717:0 | 5722:0 |
| Footer高 | 64 | 52 |
| 标签/控件 | top，间距8，控件592宽 | left，标签96、间距12，控件304；Textarea484 |

优先克隆当前已验收Scene，保留其中真实背景、蒙层和控件版本，再按本次DrawerSpec重新生成Body字段。原6089试稿仅为历史来源，未经重验不得继续当Golden。JYM原Shell母版1366×1024；本次验收的是其响应为1366×768的真实实例和滚动/可见性，不允许直接裁切1024背景假装适配。

电销没有actionSlot。智能运营菜单6158:1989与电销5763:1753独立；本轮电销自身样式维护有独立备份，不能拿它适配智能运营。

## 动态组装

1. 核对目标Page、当前平台、操作、主题和范围；更新目标前保存带时间戳的可编辑副本。新建时克隆验收Scene，原Scene不覆盖。
2. 保留Background < Overlay Mask < Drawer；Scene1366×768，Drawer在(726,0)，640×768。Header56固定，Footer按平台固定；Body垂直滚动并裁切，固定Header/Footer。
3. 不把样本四个业务字段当固定表单。先从已验收Body中按控件类型读取FormItem原型（strategyName/Input、validPeriod/DateRange、strategyType/Select、remark/Textarea），再为本次每个字段克隆对应真实控件和布局；重建实际Section/field数量，移除旧业务字段。页级标签、必填星、帮助文案保留批准Text Style与语义色。
4. Section间距24，区内字段间距12，Body四边24。JYM上置标签22高、距控件8；DX横向标签96、距控件12，控件默认304，Textarea取剩余484。长标签换行后同步行高并截图确认，不挤压控件。
5. 使用真实公开Key设置placeholder/defaultValue和状态：Input、Textarea的content=Placeholder或Value；DateRange的filled=false或true，value与placeholder各自设置；Edit回填保留输入值。Select公开value后，已填value文字绑定 `文本颜色/--qifu-text-color-primary`（VariableID:9:112）；Create占位沿用原次要文字色。这是语义色适配，不覆盖字体或重画控件。
6. JYM使用Entry/Jinyumeng/Input5010:19、Select5010:7028、DateRange5010:7055的真实wrapper；wrapper无公开值时先解析内部真实组件，再按实际Key写入。DX表单使用Input3406:853、Select2859:2820、DateRange2967:30327；Textarea2936:3834可共享。普通Create/Edit控件为14px，与DX背景列表12px区分。
7. DX背景筛选专用12px组件：Input6214:14907、Select6214:14913，200×28，真实component，公开动态解析的value文本属性；只覆盖Default Placeholder，不冒充完整状态矩阵。共享Small Input/Select的14px母版保留，不能用实例字体覆盖伪造12px来源。
8. 所有字段、分区、Footer文案按输入更新；默认Create确定/取消，Edit保存/取消。JYM取消text，DX取消outline，主按钮base；允许计划器验证的自定义文案。不得重复主操作或把旧样本字段保留下来。
9. 模式写入Scene并回读Body、Footer主按钮的实际brand；JYM#0F6FFC、DX#009E73仅作校验，使用变量绑定写入。找不到变量/组件/字体/公开属性即停止，不借其他平台补缺口。
10. 样式缺口先定位母版并备份后修复。历史实例空style覆盖仅在字体、字重、字号、行高与已批准母版完全一致时恢复相同Text Style关联，不改字体字段；不一致时使用独立平台组件。缺失旧Semibold字体的维护过程和字体变量保留记录在迭代JSON，不作为生成时自动字体替换许可。

## 每次验收

回读背景Shell/Header/menu真实owner、56/208或56/200、1366×768与选中菜单可见性；电销不出现actionSlot或智能运营菜单。检查控件/字段数量、初始值、主题、全部文字样式，验证Body可滚动、Footer固定且唯一主按钮。创建/编辑分别截图：值与占位区分、无旧业务文案、无截断/覆盖。只有结构和整页截图均PASS才可交付；候选/计划通过不能代替实际验收。
