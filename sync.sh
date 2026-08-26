#!/usr/bin/env bash
# GitHub working tree is the canonical Skill structure.
# Sync selected Skill packages to Nutstore and the local Codex runtime:
#   ./sync.sh qifu-drawer-form qifu-shared zhikexing-list-page
# With no arguments, all managed packages are synchronized.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
NUTSTORE_ROOT="/Users/shijingya/Nutstore Files/360数科-共享/skill"
CODEX_ROOT="/Users/shijingya/.codex/skills"

MANAGED_SKILLS=(
  qifu-b-end-design-system
  qifu-list-page
  qifu-drawer-form
  qifu-detail-page
  qifu-shared
  zhikexing-list-page
)

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

mkdir -p "$NUTSTORE_ROOT" "$CODEX_ROOT"

for skill in "${SKILLS[@]}"; do
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
    rsync -a --delete --exclude='.DS_Store' "$source_dir/" "$target_dir/"
    diff -qr --exclude='.DS_Store' "$source_dir" "$target_dir" >/dev/null
  done

  echo "Synced $skill"
done

echo "Sync complete: GitHub -> Nutstore + ~/.codex/skills"
