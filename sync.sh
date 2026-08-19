#!/usr/bin/env bash
# sync.sh —— 把"工作目录"中的 3 个 qifu skill 同步到本仓,准备推 GitHub
# 使用:
#   chmod +x sync.sh
#   ./sync.sh
#
# 工作目录("/Nutstore Files/360数科-共享/skill/")是日常改动的地方;
# 本仓(qifu-skills-repo)是发布到 GitHub 的干净版本,不要直接在本仓改 SKILL.md。
#
# 关键约定(2026-08-13):
# - 工作目录:子 skill 用 `../qifu-list-page/references/xxx.md` 引用共享文件
# - 本仓:     子 skill 用 `../../shared/references/xxx.md` 引用共享文件
# 本脚本在 rsync 后自动做路径"翻译",保持两边引用各自可用。
#
# rsync 的 --exclude 保护(不要删):
# - README.md                 工作目录没有;删掉会把仓里写好的 README 清掉
# - references/component-map.md / platform-yushu.md   已上提到 shared/,不再拷子目录
#
# 顶层目录保护(本脚本的 rsync 只动 skills/ 与 shared/,顶层其它目录不在同步范围):
# - _docs/                    钩通日志 + 已知限制回填指引(只在仓里,不下发给工作目录)
# - screenshots/              全仓统一展示图(用户在仓里维护)
# - 仓根 README.md / .gitignore / sync.sh 自身        这些是"发布视图"资产,工作目录不需要

set -euo pipefail

SRC="/Users/shijingya/Nutstore Files/360数科-共享/skill"
DST="$(cd "$(dirname "$0")" && pwd)"

if [[ ! -d "$SRC" ]]; then
  echo "✗ 工作目录不存在: $SRC" >&2
  exit 1
fi

echo "→ 同步 skills/ ..."
for s in qifu-b-end-design-system qifu-list-page qifu-drawer-form qifu-detail-page; do
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
  find "$DST/skills/$s" -type f -name "*.md" -exec sed -i '' \
    -e 's|\.\./qifu-list-page/references/component-map\.md|../../shared/references/component-map.md|g' \
    -e 's|\.\./qifu-list-page/references/platform-yushu\.md|../../shared/references/platform-yushu.md|g' \
    {} +
done

# list-page 自己原本写 `references/component-map.md`,也要翻译成 shared
find "$DST/skills/qifu-list-page" -type f -name "*.md" -exec sed -i '' \
  -e 's|](references/component-map\.md|](../../shared/references/component-map.md|g' \
  -e 's|](references/platform-yushu\.md|](../../shared/references/platform-yushu.md|g' \
  {} +

echo "→ 同步 shared/references/ ..."
rsync -a \
  "$SRC/qifu-list-page/references/component-map.md" \
  "$DST/shared/references/component-map.md"
rsync -a \
  "$SRC/qifu-list-page/references/platform-yushu.md" \
  "$DST/shared/references/platform-yushu.md"
echo "  ✔ component-map.md / platform-yushu.md"

echo "→ 校验路径翻译 ..."
leftover=$(grep -rE "\]\((\.\./)?(qifu-list-page/references|[^s][^h][^a][^r][^e][^d]/references)" "$DST/skills" 2>/dev/null | grep -v "shared/references" || true)
if [[ -n "$leftover" ]]; then
  echo "  ✗ 仍有未翻译的引用,请检查:" >&2
  echo "$leftover" >&2
  exit 1
fi
echo "  ✔ 全部指向 shared/references"

echo ""
echo "✔ 同步完成。下一步:"
echo "  cd $DST"
echo "  git status -sb"
echo "  git add -A && git commit -m \"你的说明\" && git push"
