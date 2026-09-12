#!/usr/bin/env bash
# GitHub working tree is the canonical Skill structure.
# Sync selected Skill packages to the local Codex runtime and, when configured, Nutstore:
#   ./sync.sh qifu-drawer-form qifu-shared
# With no arguments, all active managed packages are synchronized.
#
# CODEX_ROOT defaults to ${CODEX_HOME:-$HOME/.codex}/skills.
# NUTSTORE_ROOT is optional and must be provided explicitly:
#   NUTSTORE_ROOT=/path/to/nutstore CODEX_ROOT=/path/to/codex ./sync.sh
#   DRY_RUN=1 ./sync.sh               # 只打印动作，不实际 rsync
#
# 已归档 skill（zhikexing-list-page, 2026-09-11）不再同步；如仍保留旧目录，请手动删除。

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

# Portable defaults: local Codex is enabled; Nutstore is opt-in.
NUTSTORE_ROOT="${NUTSTORE_ROOT:-}"
CODEX_ROOT="${CODEX_ROOT:-${CODEX_HOME:-$HOME/.codex}/skills}"

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
if [[ "$DRY_RUN" != "0" && "$DRY_RUN" != "1" ]]; then
  echo "DRY_RUN must be 0 or 1" >&2
  exit 1
fi

TARGET_ROOTS=("$CODEX_ROOT")
if [[ -n "$NUTSTORE_ROOT" ]]; then
  TARGET_ROOTS+=("$NUTSTORE_ROOT")
fi

validate_target_root() {
  local target_root="$1"
  if [[ -z "$target_root" || "$target_root" == "/" || "$target_root" == "$HOME" ]]; then
    echo "Unsafe sync root: $target_root" >&2
    exit 1
  fi
}

directories_equal() {
  local left="$1"
  local right="$2"
  [[ -d "$left" && -d "$right" ]] || return 1
  [[ "$(cd "$left" && pwd -P)" == "$(cd "$right" && pwd -P)" ]]
}

validate_target_dir() {
  local source_dir="$1"
  local target_dir="$2"
  if [[ -L "$target_dir" ]]; then
    if [[ ! -d "$target_dir" ]]; then
      echo "Broken target symlink: $target_dir" >&2
      exit 1
    fi
    if ! directories_equal "$source_dir" "$target_dir"; then
      echo "Target Skill is a symlink to another directory: $target_dir" >&2
      exit 1
    fi
  elif [[ -e "$target_dir" && ! -d "$target_dir" ]]; then
    echo "Target Skill exists but is not a directory: $target_dir" >&2
    exit 1
  fi
}

for target_root in "${TARGET_ROOTS[@]}"; do
  validate_target_root "$target_root"
done

if [[ "$DRY_RUN" == "0" ]]; then
  command -v rsync >/dev/null 2>&1 || {
    echo "Required command not found: rsync" >&2
    exit 1
  }
  command -v diff >/dev/null 2>&1 || {
    echo "Required command not found: diff" >&2
    exit 1
  }
fi

# Validate the complete request before the first filesystem mutation.
for skill in "${SKILLS[@]}"; do
  if is_archived_skill "$skill"; then
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
  for target_root in "${TARGET_ROOTS[@]}"; do
    validate_target_dir "$source_dir" "$target_root/$skill"
  done
done

if [[ "$DRY_RUN" == "1" ]]; then
  LOG_PREFIX="[DRY] "
else
  LOG_PREFIX=""
fi

for skill in "${SKILLS[@]}"; do
  if is_archived_skill "$skill"; then
    echo "⚠️  $skill 已归档，跳过同步；如目标目录仍有旧副本，请手动删除对应的 $skill 目录" >&2
    continue
  fi
  source_dir="$REPO_ROOT/skills/$skill"

  for target_root in "${TARGET_ROOTS[@]}"; do
    target_dir="$target_root/$skill"
    if directories_equal "$source_dir" "$target_dir"; then
      echo "${LOG_PREFIX}Already linked $skill -> $source_dir"
    elif [[ "$DRY_RUN" == "1" ]]; then
      echo "[DRY] rsync -a --delete --exclude='.DS_Store' $source_dir/ $target_dir/"
    else
      mkdir -p "$target_dir"
      rsync -a --delete --exclude='.DS_Store' "$source_dir/" "$target_dir/"
      diff -qr --exclude='.DS_Store' "$source_dir" "$target_dir" >/dev/null
    fi
  done

  echo "${LOG_PREFIX}Synced $skill"
done

echo "${LOG_PREFIX}Sync complete: GitHub -> ${TARGET_ROOTS[*]}"
