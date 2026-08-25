#!/usr/bin/env bash
# sync.sh —— 把"工作目录"中的 qifu / zhikexing skill 同步到本仓,准备推 GitHub
# 使用:
#   chmod +x sync.sh
#   ./sync.sh
#   ./sync.sh qifu-drawer-form
#
# 工作目录("/Nutstore Files/360数科-共享/skill/")是日常改动的地方;
# 本仓(qifu-skills-repo)是发布到 GitHub 的干净版本,不要直接在本仓改 SKILL.md。
#
# 关键约定(2026-08-20):
# - 工作目录:list-page 自己持有 references/component-map.md 与 platform-yushu.md;
#            drawer/detail 用 `../qifu-list-page/references/xxx.md` 或
#            references 子目录里用 `../../qifu-list-page/references/xxx.md` 跨目录引用。
# - 本仓:     共享资产统一上提到 `skills/qifu-shared/references/`,子 skill 用
#            `../qifu-shared/references/xxx.md`(SKILL.md)或 `../../qifu-shared/references/xxx.md`(references 子目录)引用。
# 本脚本在 rsync 后自动做路径"翻译",保持两边引用各自可用。
#
# rsync 的 --exclude 保护(不要删):
# - README.md                 工作目录没有;删掉会把仓里写好的 README 清掉
# - references/component-map.md / platform-yushu.md   已上提到 skills/qifu-shared/references/,不再拷子目录
#
# 顶层目录保护(本脚本的 rsync 只动 skills/qifu-{list-page,drawer-form,detail-page} 与
# skills/qifu-shared/references/,其它目录不在同步范围):
# - _docs/                    钩通日志 + 已知限制回填指引(只在仓里,不下发给工作目录)
# - screenshots/              全仓统一展示图(用户在仓里维护)
# - skills/qifu-b-end-design-system/  公司级编排入口(只在仓里维护)
# - skills/qifu-shared/theme/          Figma 变量快照,源是 Figma 而非工作目录,不在此同步
# - 仓根 README.md / .gitignore / sync.sh 自身        这些是"发布视图"资产,工作目录不需要

set -euo pipefail

SRC="/Users/shijingya/Nutstore Files/360数科-共享/skill"
DST="$(cd "$(dirname "$0")" && pwd)"

if [[ ! -d "$SRC" ]]; then
  echo "✗ 工作目录不存在: $SRC" >&2
  exit 1
fi

ONLY_SKILL="${1:-}"
if [[ -n "$ONLY_SKILL" ]]; then
  case "$ONLY_SKILL" in
    qifu-b-end-design-system|qifu-list-page|qifu-drawer-form|qifu-detail-page|zhikexing-list-page) ;;
    *) echo "✗ 不支持同步的 skill: $ONLY_SKILL" >&2; exit 1 ;;
  esac
fi

echo "→ 同步 skills/ ..."
for s in qifu-b-end-design-system qifu-list-page qifu-drawer-form qifu-detail-page; do
  [[ -n "$ONLY_SKILL" && "$ONLY_SKILL" != "$s" ]] && continue
  if [[ ! -d "$SRC/$s" ]]; then
    echo "  ⚠ 跳过: 工作目录缺少 $s" >&2
    continue
  fi
  rsync -a --delete \
    --exclude='.DS_Store' \
    --exclude='README.md' \
    --exclude='references/component-map.md' \
    --exclude='references/platform-yushu.md' \
    "$SRC/$s/" "$DST/skills/$s/"
  echo "  ✔ $s"

  # 把"工作目录相对路径"翻译成"本仓相对路径"
  # 三种形态都要覆盖:
  #   (a) SKILL.md 里的      `../qifu-list-page/references/xxx.md`
  #   (b) references/ 子目录里的 `../../qifu-list-page/references/xxx.md`
  #   (c) list-page 自己 references 里的裸引用 `](references/xxx.md`
  find "$DST/skills/$s" -type f -name "*.md" -exec sed -i '' \
    -e 's|\.\./qifu-list-page/references/component-map\.md|../qifu-shared/references/component-map.md|g' \
    -e 's|\.\./qifu-list-page/references/platform-yushu\.md|../qifu-shared/references/platform-yushu.md|g' \
    -e 's|\.\./\.\./qifu-list-page/references/component-map\.md|../../qifu-shared/references/component-map.md|g' \
    -e 's|\.\./\.\./qifu-list-page/references/platform-yushu\.md|../../qifu-shared/references/platform-yushu.md|g' \
    {} +

  if [[ "$s" == "qifu-drawer-form" ]]; then
    # 源目录带本地组件映射；发布仓统一引用 qifu-shared。
    find "$DST/skills/$s" -maxdepth 1 -type f -name "*.md" -exec sed -i '' \
      -e 's|](references/component-map\.md|](../qifu-shared/references/component-map.md|g' \
      -e 's|](references/platform-yushu\.md|](../qifu-shared/references/platform-yushu.md|g' \
      {} +
    find "$DST/skills/$s/references" -type f -name "*.md" -exec sed -i '' \
      -e 's|](component-map\.md|](../../qifu-shared/references/component-map.md|g' \
      {} +
  fi
done

# 智客星列表页独立持有参考文件，不沿用上方 qifu-shared 的排除与路径翻译规则。
if [[ -z "$ONLY_SKILL" || "$ONLY_SKILL" == "zhikexing-list-page" ]] && [[ -d "$SRC/zhikexing-list-page" ]]; then
  rsync -a --delete \
    --exclude='.DS_Store' \
    --exclude='README.md' \
    "$SRC/zhikexing-list-page/" "$DST/skills/zhikexing-list-page/"
  echo "  ✔ zhikexing-list-page"
elif [[ -z "$ONLY_SKILL" || "$ONLY_SKILL" == "zhikexing-list-page" ]]; then
  echo "  ⚠ 跳过: 工作目录缺少 zhikexing-list-page" >&2
fi

if [[ -z "$ONLY_SKILL" || "$ONLY_SKILL" == "qifu-list-page" ]]; then
  # list-page 自己原本写 `references/component-map.md`,也要翻译成 qifu-shared
  find "$DST/skills/qifu-list-page" -type f -name "*.md" -exec sed -i '' \
    -e 's|](references/component-map\.md|](../../qifu-shared/references/component-map.md|g' \
    -e 's|](references/platform-yushu\.md|](../../qifu-shared/references/platform-yushu.md|g' \
    {} +

  echo "→ 同步 skills/qifu-shared/references/ ..."
  rsync -a \
    "$SRC/qifu-list-page/references/component-map.md" \
    "$DST/skills/qifu-shared/references/component-map.md"
  rsync -a \
    "$SRC/qifu-list-page/references/platform-yushu.md" \
    "$DST/skills/qifu-shared/references/platform-yushu.md"
  echo "  ✔ component-map.md / platform-yushu.md"
fi

echo "→ 校验路径翻译 ..."
leftover=$(grep -rE "\]\((\.\./)?(\.\./)?qifu-list-page/references|](references/component-map\.md|](references/platform-yushu\.md" "$DST/skills" 2>/dev/null | grep -v "qifu-shared/references" || true)
if [[ -n "$leftover" ]]; then
  echo "  ✗ 仍有未翻译的引用,请检查:" >&2
  echo "$leftover" >&2
  exit 1
fi
echo "  ✔ 全部指向 qifu-shared/references"

echo ""
echo "✔ 同步完成。下一步:"
echo "  cd $DST"
echo "  git status -sb"
echo "  git add -A && git commit -m \"你的说明\" && git push"
