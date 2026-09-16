# qifu-business-flow

奇富后台多页面业务链路编排 Skill。它从自然语言或 BusinessFlowSpec 建立统一业务模型，复用已验证页面，委派缺失页面给对应页面 Skill，并只为 confirmed transitions 建立 Figma Prototype。

## 适用场景

- 列表 → 新建/编辑抽屉 → 返回列表；
- 列表 → 更多菜单 → 数据详情抽屉；
- 列表、抽屉、详情页等多个状态需要统一字段和跳转；
- 需要明确 pending Skill、TBD 和未实现入口。

单独生成一张页面时，直接使用 `qifu-list-page`、`qifu-drawer-form` 或 `qifu-detail-page`。

## 推荐提示词

```text
使用 qifu-business-flow，并调用 @figma，在【目标 Figma Page】的空白处建立【业务名称】页面链路。

平台：【platform key】；菜单路径：【一级 / 二级 / 当前页面】。
业务模型：【已有 YAML 路径；没有则写“新建”】。
页面状态：【状态 1、状态 2、状态 3】。
页面关系：【入口动作 → 目标状态；关闭/提交 → 返回规则】。
不实现入口：【入口及原因】。

优先复用目标 Page 中已验证页面；只生成缺失状态。所有页面使用当前平台真实组件和本地文本样式。只建立 confirmed 路由，最后返回字段一致性、页面节点、Prototype 和视觉检查结果。
```

## 命令

```bash
python3 scripts/build_flow_plan.py path/to/business-model.yaml
python3 scripts/validate_skill_contract.py
python3 -m unittest discover -s tests -v
```
