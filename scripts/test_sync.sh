#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEST_ROOT="$(mktemp -d /tmp/qifu-sync-test.XXXXXX)"

cleanup() {
  case "$TEST_ROOT" in
    /tmp/qifu-sync-test.*) rm -rf -- "$TEST_ROOT" ;;
    *) echo "Refusing to remove unexpected test path: $TEST_ROOT" >&2 ;;
  esac
}
trap cleanup EXIT

dry_codex="$TEST_ROOT/dry-codex"
dry_nutstore="$TEST_ROOT/dry-nutstore"
DRY_RUN=1 CODEX_HOME="$dry_codex" NUTSTORE_ROOT="$dry_nutstore" \
  "$REPO_ROOT/sync.sh" qifu-shared >"$TEST_ROOT/dry.log"
test ! -e "$dry_codex"
test ! -e "$dry_nutstore"

real_codex="$TEST_ROOT/real-codex"
CODEX_HOME="$real_codex" "$REPO_ROOT/sync.sh" qifu-shared >"$TEST_ROOT/real.log"
test -f "$real_codex/skills/qifu-shared/SKILL.md"
if grep -q '\[DRY\]' "$TEST_ROOT/real.log"; then
  echo "Real sync was incorrectly labeled as dry-run" >&2
  exit 1
fi

invalid_codex="$TEST_ROOT/invalid-codex"
if CODEX_HOME="$invalid_codex" "$REPO_ROOT/sync.sh" qifu-shared not-a-skill \
  >"$TEST_ROOT/invalid.log" 2>&1; then
  echo "Invalid Skill request unexpectedly succeeded" >&2
  exit 1
fi
test ! -e "$invalid_codex"

linked_root="$TEST_ROOT/linked-skills"
mkdir -p "$linked_root"
ln -s "$REPO_ROOT/skills/qifu-shared" "$linked_root/qifu-shared"
CODEX_ROOT="$linked_root" "$REPO_ROOT/sync.sh" qifu-shared >"$TEST_ROOT/linked.log"
grep -q 'Already linked qifu-shared' "$TEST_ROOT/linked.log"

foreign_root="$TEST_ROOT/foreign-skills"
foreign_target="$TEST_ROOT/foreign-target"
mkdir -p "$foreign_root" "$foreign_target"
ln -s "$foreign_target" "$foreign_root/qifu-shared"
if CODEX_ROOT="$foreign_root" "$REPO_ROOT/sync.sh" qifu-shared \
  >"$TEST_ROOT/foreign.log" 2>&1; then
  echo "Foreign target symlink unexpectedly succeeded" >&2
  exit 1
fi

echo "PASS: sync dry-run, real-copy, preflight, and symlink safety"
