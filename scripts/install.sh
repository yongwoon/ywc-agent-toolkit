#!/usr/bin/env bash
#
# ywc-agent-toolkit 통합 설치 스크립트
#
# Usage:
#   bash scripts/install.sh --cc                            Claude Code 전체 설치
#   bash scripts/install.sh --codex                         Codex 전체 설치
#   bash scripts/install.sh --all                           양쪽 전체 설치
#   bash scripts/install.sh --cc <skill> [skill...]         Claude Code 특정 스킬
#   bash scripts/install.sh --codex <skill> [skill...]      Codex 특정 스킬
#   bash scripts/install.sh --hooks [--global|--local] [hook-name...]  Hook 설치
#   bash scripts/install.sh --list [--cc|--codex|--hooks]   설치 가능한 목록
#   bash scripts/install.sh --help                          이 도움말
#
# Environment:
#   CLAUDE_SKILLS_DIR   Claude Code 설치 경로 override (default: ~/.claude/skills)
#   CODEX_HOME          Codex 홈 경로 override (default: ~/.codex)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CC_SRC="$REPO_ROOT/claude-code/skills"
CODEX_SRC="$REPO_ROOT/codex/skills"
HOOKS_SRC="$REPO_ROOT/claude-code/hooks"
HOOKS_REGISTRY="$HOOKS_SRC/hooks-registry.json"
CC_DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
CODEX_DEST="${CODEX_HOME:-$HOME/.codex}/skills"
CC_MANIFEST="$CC_DEST/.ywc-agent-toolkit.manifest"
CODEX_MANIFEST="$CODEX_DEST/.ywc-agent-toolkit.manifest"

CC_INSTALLED=0
CODEX_INSTALLED=0
CC_PRUNED=0
CODEX_PRUNED=0
HOOKS_INSTALLED=0

# ---- helpers ----------------------------------------------------------------

is_skill_dir() {
  [ -f "$1/SKILL.md" ]
}

list_skills() {
  local src="$1"
  [ -d "$src" ] || return 0
  local d
  for d in "$src"/*/; do
    [ -d "$d" ] || continue
    is_skill_dir "$d" || continue
    basename "$d"
  done
}

read_manifest() {
  local manifest="$1"
  [ -f "$manifest" ] || return 0
  grep -Ev '^(#|$)' "$manifest" || true
}

write_manifest() {
  local manifest="$1"
  local skills="$2"
  {
    echo "# ywc-agent-toolkit install manifest"
    echo "# Auto-generated — do not edit manually."
    [ -n "$skills" ] && printf '%s\n' "$skills"
  } > "$manifest"
}

# ---- install / prune --------------------------------------------------------

install_skill() {
  local src_dir="$1"
  local dest_dir="$2"
  local name
  name="$(basename "$src_dir")"
  is_skill_dir "$src_dir" || return 0
  rm -rf "${dest_dir:?}/$name"
  cp -R "$src_dir" "$dest_dir/$name"
  echo "  ✓ $name"
}

install_support_dir() {
  local src_dir="$1"
  local dest_dir="$2"
  local name
  name="$(basename "$src_dir")"
  [ -d "$src_dir" ] || return 0
  rm -rf "${dest_dir:?}/$name"
  cp -R "$src_dir" "$dest_dir/$name"
  echo "  ✓ $name/"
}

install_cc_support_dirs() {
  install_support_dir "$CC_SRC/references" "$CC_DEST"
}

install_codex_support_dirs() {
  install_support_dir "$CODEX_SRC/references" "$CODEX_DEST"
  install_support_dir "$CODEX_SRC/scripts" "$CODEX_DEST"
}

prune_orphans() {
  local dest="$1"
  local manifest="$2"
  local current="$3"
  local previous orphans name

  previous="$(read_manifest "$manifest")"
  [ -n "$previous" ] || return 0

  orphans="$(comm -23 \
    <(printf '%s\n' "$previous" | sort -u) \
    <(printf '%s\n' "$current" | sort -u))"

  [ -n "$orphans" ] || return 0

  echo "  고아 스킬 제거 중:"
  while IFS= read -r name; do
    [ -n "$name" ] || continue
    local target="$dest/$name"
    [ -d "$target" ] || continue
    if [ ! -f "$target/SKILL.md" ]; then
      echo "    ! $name (SKILL.md 없음, skip)"
      continue
    fi
    rm -rf "$target"
    echo "    ✗ $name"
    if [ "$dest" = "$CC_DEST" ]; then
      CC_PRUNED=$((CC_PRUNED + 1))
    else
      CODEX_PRUNED=$((CODEX_PRUNED + 1))
    fi
  done <<< "$orphans"
}

# ---- Claude Code ------------------------------------------------------------

run_cc_install() {
  local skills=("$@")
  mkdir -p "$CC_DEST"
  echo "Claude Code → $CC_DEST"
  install_cc_support_dirs

  local current
  current="$(list_skills "$CC_SRC")"

  if [ "${#skills[@]}" -eq 0 ]; then
    prune_orphans "$CC_DEST" "$CC_MANIFEST" "$current"
    local d
    for d in "$CC_SRC"/*/; do
      [ -d "$d" ] || continue
      is_skill_dir "$d" || continue
      install_skill "$d" "$CC_DEST"
      CC_INSTALLED=$((CC_INSTALLED + 1))
    done
    write_manifest "$CC_MANIFEST" "$current"
  else
    local name
    for name in "${skills[@]}"; do
      local src="$CC_SRC/$name"
      if [ ! -d "$src" ] || ! is_skill_dir "$src"; then
        echo "  알 수 없는 스킬: $name" >&2
        echo "  사용 가능한 스킬:" >&2
        list_skills "$CC_SRC" >&2
        exit 1
      fi
      install_skill "$src" "$CC_DEST"
      CC_INSTALLED=$((CC_INSTALLED + 1))
    done
    local merged
    merged="$({ read_manifest "$CC_MANIFEST"; printf '%s\n' "${skills[@]}"; } | sort -u | awk 'NF')"
    write_manifest "$CC_MANIFEST" "$merged"
  fi
}

# ---- Codex ------------------------------------------------------------------

run_codex_install() {
  local skills=("$@")
  mkdir -p "$CODEX_DEST"
  echo "Codex → $CODEX_DEST"
  install_codex_support_dirs

  local current
  current="$(list_skills "$CODEX_SRC")"

  if [ "${#skills[@]}" -eq 0 ]; then
    prune_orphans "$CODEX_DEST" "$CODEX_MANIFEST" "$current"
    local d
    for d in "$CODEX_SRC"/*/; do
      [ -d "$d" ] || continue
      is_skill_dir "$d" || continue
      install_skill "$d" "$CODEX_DEST"
      CODEX_INSTALLED=$((CODEX_INSTALLED + 1))
    done
    write_manifest "$CODEX_MANIFEST" "$current"
  else
    local name
    for name in "${skills[@]}"; do
      local src="$CODEX_SRC/$name"
      if [ ! -d "$src" ] || ! is_skill_dir "$src"; then
        echo "  알 수 없는 스킬: $name" >&2
        echo "  사용 가능한 스킬:" >&2
        list_skills "$CODEX_SRC" >&2
        exit 1
      fi
      install_skill "$src" "$CODEX_DEST"
      CODEX_INSTALLED=$((CODEX_INSTALLED + 1))
    done
    local merged
    merged="$({ read_manifest "$CODEX_MANIFEST"; printf '%s\n' "${skills[@]}"; } | sort -u | awk 'NF')"
    write_manifest "$CODEX_MANIFEST" "$merged"
  fi
}

# ---- Hooks ------------------------------------------------------------------

# Merge a single (event, matcher, command) entry into settings.json idempotently.
# Creates the file as '{}' if it does not exist. Backs up before modifying.
# Atomic: writes to a temp file and renames.
merge_hook_settings() {
  local settings_file="$1"
  local event="$2"
  local matcher="$3"
  local command="$4"

  [ -f "$settings_file" ] || echo '{}' > "$settings_file"

  if ! jq empty "$settings_file" 2>/dev/null; then
    echo "  ! 유효하지 않은 JSON: $settings_file" >&2
    return 1
  fi

  cp "$settings_file" "${settings_file}.bak"

  # jq filter covers all 4 merge cases from spec:
  #   1. no .hooks key          → create it
  #   2. no .hooks[$event]      → create the event array
  #   3. no matching matcher    → append new matcher group
  #   4. matcher exists         → append command only if not already present
  # shellcheck disable=SC2016  # $event/$matcher/$cmd are jq --arg variables, not bash
  local filter='
    .hooks //= {} |
    .hooks[$event] //= [] |
    if (.hooks[$event] | any(.matcher == $matcher)) then
      .hooks[$event] |= map(
        if .matcher == $matcher then
          if (.hooks | any(.command == $cmd)) then .
          else .hooks += [{"type": "command", "command": $cmd}]
          end
        else .
        end
      )
    else
      .hooks[$event] += [{"matcher": $matcher, "hooks": [{"type": "command", "command": $cmd}]}]
    end
  '

  local tmp
  tmp="$(mktemp "$(dirname "$settings_file")/.settings.json.tmp.XXXXXX")"
  if jq --arg event "$event" --arg matcher "$matcher" --arg cmd "$command" \
        "$filter" "$settings_file" > "$tmp" \
      && jq empty "$tmp" 2>/dev/null; then
    mv "$tmp" "$settings_file"
    rm -f "${settings_file}.bak"
  else
    echo "  ! settings.json 병합 실패, 복원 중..." >&2
    cp "${settings_file}.bak" "$settings_file"
    rm -f "$tmp"
    return 1
  fi
}

run_hook_install() {
  local scope="$1"
  shift
  local hook_names=("$@")

  if ! command -v jq >/dev/null 2>&1; then
    echo "Error: jq가 필요합니다." >&2
    echo "  macOS:  brew install jq" >&2
    echo "  Ubuntu: sudo apt-get install jq" >&2
    exit 1
  fi

  if ! command -v uv >/dev/null 2>&1; then
    echo "Warning: uv 미설치. Python hook은 실행 시 오류가 발생합니다." >&2
    echo "  설치: curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
  fi

  local dest_hooks settings manifest cmd_key claude_home
  claude_home="$(dirname "$CC_DEST")"
  if [ "$scope" = "global" ]; then
    dest_hooks="$claude_home/hooks"
    settings="$claude_home/settings.json"
    manifest="$dest_hooks/.ywc-agent-toolkit-hooks.manifest"
    cmd_key="command_global"
  else
    dest_hooks="$(pwd)/.claude/hooks"
    settings="$(pwd)/.claude/settings.json"
    manifest="$dest_hooks/.ywc-agent-toolkit-hooks.manifest"
    cmd_key="command_local"
  fi

  mkdir -p "$dest_hooks"
  mkdir -p "$(dirname "$settings")"

  echo "Hooks → $dest_hooks"
  echo "Settings → $settings"

  # Default: install all hooks
  if [ "${#hook_names[@]}" -eq 0 ]; then
    while IFS= read -r _hook; do
      hook_names+=("$_hook")
    done < <(jq -r '.hooks | keys[]' "$HOOKS_REGISTRY")
  fi

  # Validate names before touching anything
  local name
  for name in "${hook_names[@]}"; do
    if ! jq -e --arg n "$name" '.hooks | has($n)' "$HOOKS_REGISTRY" >/dev/null 2>&1; then
      echo "  알 수 없는 hook: $name" >&2
      echo "  사용 가능한 hook:" >&2
      jq -r '.hooks | keys[]' "$HOOKS_REGISTRY" >&2
      exit 1
    fi
  done

  local installed_names=()
  for name in "${hook_names[@]}"; do
    local entry
    entry="$(jq -c --arg n "$name" '.hooks[$n]' "$HOOKS_REGISTRY")"

    local cmd_path
    cmd_path="$(jq -r ".$cmd_key" <<< "$entry")"

    # Extract the hooks filepath token from the command (robust against flags like --auto-allow)
    local hooks_word filename
    hooks_word="$(printf '%s' "$cmd_path" | tr ' ' '\n' | grep '\.claude/hooks/')"
    filename="$(basename "$hooks_word")"

    local src_file="$HOOKS_SRC/$filename"
    if [ ! -f "$src_file" ]; then
      echo "  ! $name (소스 파일 없음: $filename)" >&2
      exit 1
    fi

    cp "$src_file" "$dest_hooks/$filename" || {
      echo "  ! $name (파일 복사 실패)" >&2
      exit 1
    }
    [ "${filename##*.}" = "sh" ] && chmod 755 "$dest_hooks/$filename"
    echo "  ✓ $name ($filename)"
    HOOKS_INSTALLED=$((HOOKS_INSTALLED + 1))

    # Notify-permission requires a webhook env var
    if [ "$name" = "notify-permission" ]; then
      echo "    → CCH_SLA_WEBHOOK 환경변수를 설정해야 Slack 알림이 작동합니다."
    fi

    # Merge settings.json: cost-tracker has multi-event (events array)
    if jq -e 'has("events")' <<< "$entry" >/dev/null 2>&1; then
      local events=()
      while IFS= read -r _evt; do
        events+=("$_evt")
      done < <(jq -r '.events[]' <<< "$entry")
      local evt
      for evt in "${events[@]}"; do
        local matcher
        matcher="$(jq -r --arg k "matcher_${evt}" '.[$k]' <<< "$entry")"
        merge_hook_settings "$settings" "$evt" "$matcher" "$cmd_path"
      done
    else
      local event matcher
      event="$(jq -r '.event' <<< "$entry")"
      matcher="$(jq -r '.matcher' <<< "$entry")"
      merge_hook_settings "$settings" "$event" "$matcher" "$cmd_path"
    fi

    installed_names+=("$name")
  done

  # Prune orphaned hook files from previous installs
  if [ -f "$manifest" ]; then
    local previous
    previous="$(grep -Ev '^(#|$)' "$manifest" || true)"
    if [ -n "$previous" ]; then
      local current_set orphans
      if [ "${#installed_names[@]}" -gt 0 ]; then
        current_set="$(printf '%s\n' "${installed_names[@]}" | sort -u)"
      else
        current_set=""
      fi
      orphans="$(comm -23 \
        <(printf '%s\n' "$previous" | sort -u) \
        <(printf '%s\n' "$current_set" | sort -u) || true)"
      if [ -n "$orphans" ]; then
        echo "  고아 hook 제거 중:"
        while IFS= read -r orphan; do
          [ -n "$orphan" ] || continue
          local orphan_entry
          orphan_entry="$(jq -c --arg n "$orphan" '.hooks[$n] // empty' "$HOOKS_REGISTRY" 2>/dev/null || true)"
          [ -n "$orphan_entry" ] || continue
          local orphan_cmd orphan_word orphan_file
          orphan_cmd="$(jq -r ".$cmd_key" <<< "$orphan_entry")"
          orphan_word="$(printf '%s' "$orphan_cmd" | tr ' ' '\n' | grep '\.claude/hooks/')"
          orphan_file="$dest_hooks/$(basename "$orphan_word")"
          if [ -f "$orphan_file" ]; then
            rm "$orphan_file"
            echo "    ✗ $orphan"
          fi
          # Remove the command entry from settings.json to prevent stale hook invocations
          if [ -f "$settings" ] && [ -n "$orphan_cmd" ]; then
            local stmp
            stmp="$(mktemp "$(dirname "$settings")/.settings.json.tmp.XXXXXX")"
            # shellcheck disable=SC2016
            if jq --arg cmd "$orphan_cmd" \
                '.hooks //= {} |
                 .hooks |= with_entries(
                   .value |= (
                     map(.hooks |= map(select(.command != $cmd)))
                     | map(select((.hooks | length) > 0))
                   )
                   | select(length > 0)
                 )' \
                "$settings" > "$stmp" && jq empty "$stmp" 2>/dev/null; then
              mv "$stmp" "$settings"
            else
              rm -f "$stmp"
            fi
          fi
        done <<< "$orphans"
      fi
    fi
  fi

  # Write manifest
  {
    echo "# ywc-agent-toolkit hooks install manifest"
    echo "# Auto-generated — do not edit manually."
    if [ "${#installed_names[@]}" -gt 0 ]; then
      printf '%s\n' "${installed_names[@]}" | sort -u
    fi
  } > "$manifest"
}

# ---- usage ------------------------------------------------------------------

usage() {
  cat >&2 <<'EOF'
Usage:
  bash scripts/install.sh --cc                            Claude Code 전체 설치
  bash scripts/install.sh --codex                         Codex 전체 설치
  bash scripts/install.sh --all                           양쪽 전체 설치
  bash scripts/install.sh --cc <skill> [skill...]         Claude Code 특정 스킬
  bash scripts/install.sh --codex <skill> [skill...]      Codex 특정 스킬
  bash scripts/install.sh --hooks [--global|--local] [hook-name...]  Hook 설치
  bash scripts/install.sh --list [--cc|--codex|--hooks]   설치 가능한 목록
  bash scripts/install.sh --help                          이 도움말

Environment:
  CLAUDE_SKILLS_DIR   Claude Code 설치 경로 (default: ~/.claude/skills)
  CODEX_HOME          Codex 홈 경로 (default: ~/.codex)
EOF
}

# ---- main -------------------------------------------------------------------

if [ "$#" -eq 0 ]; then
  usage
  exit 1
fi

MODE=""
HOOK_SCOPE="global"
IN_HOOKS=0
declare -a SKILLS=()
declare -a HOOK_NAMES=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    --cc)
      MODE="cc"
      shift
      ;;
    --codex)
      MODE="codex"
      shift
      ;;
    --all)
      MODE="all"
      shift
      ;;
    --hooks)
      MODE="hooks"
      IN_HOOKS=1
      shift
      ;;
    --global)
      if [ "$IN_HOOKS" -eq 1 ]; then
        HOOK_SCOPE="global"
      else
        echo "Error: --global은 --hooks 와 함께 사용해야 합니다" >&2
        usage
        exit 1
      fi
      shift
      ;;
    --local)
      if [ "$IN_HOOKS" -eq 1 ]; then
        HOOK_SCOPE="local"
      else
        echo "Error: --local은 --hooks 와 함께 사용해야 합니다" >&2
        usage
        exit 1
      fi
      shift
      ;;
    --list)
      shift
      if [ "${1:-}" = "--hooks" ]; then
        if ! command -v jq >/dev/null 2>&1; then
          echo "Error: jq가 필요합니다." >&2
          exit 1
        fi
        echo "=== Hooks ==="
        jq -r '.hooks | to_entries[] | "  \(.key)\t\(.value.description)"' "$HOOKS_REGISTRY"
      elif [ "${1:-}" = "--cc" ]; then
        echo "=== Claude Code ==="
        list_skills "$CC_SRC"
      elif [ "${1:-}" = "--codex" ]; then
        echo "=== Codex ==="
        list_skills "$CODEX_SRC"
      else
        echo "=== Claude Code ==="
        list_skills "$CC_SRC"
        echo ""
        echo "=== Codex ==="
        list_skills "$CODEX_SRC"
      fi
      exit 0
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [ "$IN_HOOKS" -eq 1 ]; then
        HOOK_NAMES+=("$1")
      else
        SKILLS+=("$1")
      fi
      shift
      ;;
  esac
done

case "$MODE" in
  cc)
    run_cc_install "${SKILLS[@]+"${SKILLS[@]}"}"
    ;;
  codex)
    run_codex_install "${SKILLS[@]+"${SKILLS[@]}"}"
    ;;
  all)
    run_cc_install
    echo ""
    run_codex_install
    ;;
  hooks)
    run_hook_install "$HOOK_SCOPE" "${HOOK_NAMES[@]+"${HOOK_NAMES[@]}"}"
    ;;
  *)
    echo "Error: --cc / --codex / --all / --hooks のいずれかを指定してください" >&2
    usage
    exit 1
    ;;
esac

echo ""
if [ "$CC_INSTALLED" -gt 0 ]; then
  msg="Claude Code: ${CC_INSTALLED}개 스킬 설치"
  [ "$CC_PRUNED" -gt 0 ] && msg+=" / ${CC_PRUNED}개 제거"
  echo "$msg → $CC_DEST"
  echo "Claude Code 를 재시작하면 설치된 스킬이 반영됩니다."
fi
if [ "$CODEX_INSTALLED" -gt 0 ]; then
  msg="Codex: ${CODEX_INSTALLED}개 스킬 설치"
  [ "$CODEX_PRUNED" -gt 0 ] && msg+=" / ${CODEX_PRUNED}개 제거"
  echo "$msg → $CODEX_DEST"
fi
if [ "$HOOKS_INSTALLED" -gt 0 ]; then
  echo "Hooks: ${HOOKS_INSTALLED}개 설치 완료"
  echo "Claude Code 를 재시작하면 설치된 hook이 반영됩니다."
fi
