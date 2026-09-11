#!/usr/bin/env bash
# GitHub working tree is the canonical Skill structure.
# Sync selected Skill packages to Nutstore and the local Codex runtime:
#   ./sync.sh qifu-drawer-form qifu-shared
# With no arguments, all active managed packages are synchronized.
#
# ⚠️ 目标路径是原作者本机环境：
#   NUTSTORE_ROOT = /Users/shijingya/Nutstore Files/360数科-共享/skill
#   CODEX_ROOT    = /Users/shijingya/.codex/skills
# 协作者请在文件首部改成本机路径，或通过环境变量覆盖：
#   NUTSTORE_ROOT=/path/to/nutstore CODEX_ROOT=/path/to/codex ./sync.sh
#   DRY_RUN=1 ./sync.sh               # 只打印动作，不实际 rsync
#
# 已归档 skill（zhikexing-list-page, 2026-09-11）不再同步；如仍保留旧目录，请手动删除。

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

# 允许通过环境变量覆盖默认本机路径；未提供则使用默认值。
NUTSTORE_ROOT="${NUTSTORE_ROOT:-/Users/shijingya/Nutstore Files/360数科-共享/skill}"
CODEX_ROOT="${CODEX_ROOT:-/Users/shijingya/.codex/skills}"

# 活跃 Skill 列表：zhikexing-list-page 已归档，不在此处维护。
MANAGED_SKILLS=(
  qifu-b-end-design-system
  qifu-list-page
  qifu-drawer-form
  qifu-detail-page
  qifu-shared
)

# 已归档（不再同步，但保留历史入口以兼容老引用）。
ARCHIVED_SKILLS=(zhikexing-list-page)

if [[ $# -gt 0 ]]; then
  SKILLS=("$@")
else
  SKILLS=("${MANAGED_SKILLS[@]}")
fi

is_managed_skill() {
  local candidate="$1"
  local skill
  for skill in "${MANAGED_SKILLS[@]}"; do
    [[ "$candidate" == "$skill" ]] && return 0
  done
  return 1
}

is_archived_skill() {
  local candidate="$1"
  local skill
  for skill in "${ARCHIVED_SKILLS[@]}"; do
    [[ "$candidate" == "$skill" ]] && return 0
  done
  return 1
}

DRY_RUN="${DRY_RUN:-0}"

mkdir -p "$NUTSTORE_ROOT" "$CODEX_ROOT"

for skill in "${SKILLS[@]}"; do
  if is_archived_skill "$skill"; then
    echo "⚠️  $skill 已归档，跳过同步；如本地仍有旧目录，请手动删除：$NUTSTORE_ROOT/$skill 与 $CODEX_ROOT/$skill" >&2
    continue
  fi
  if ! is_managed_skill "$skill"; then
    echo "Unsupported Skill: $skill" >&2
    exit 1
  fi

  source_dir="$REPO_ROOT/skills/$skill"
  if [[ ! -d "$source_dir" ]]; then
    echo "Canonical Skill is missing: $source_dir" >&2
    exit 1
  fi

  for target_root in "$NUTSTORE_ROOT" "$CODEX_ROOT"; do
    target_dir="$target_root/$skill"
    mkdir -p "$target_dir"
    if [[ "$DRY_RUN" == "1" ]]; then
      echo "[DRY] rsync -a --delete --exclude='.DS_Store' $source_dir/ $target_dir/"
    else
      rsync -a --delete --exclude='.DS_Store' "$source_dir/" "$target_dir/"
      diff -qr --exclude='.DS_Store' "$source_dir" "$target_dir" >/dev/null
    fi
  done

  echo "${DRY_RUN:+[DRY] }Synced $skill"
done

echo "${DRY_RUN:+[DRY] }Sync complete: GitHub -> Nutstore + ~/.codex/skills"