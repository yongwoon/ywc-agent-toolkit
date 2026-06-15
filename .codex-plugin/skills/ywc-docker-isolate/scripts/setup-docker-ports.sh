#!/usr/bin/env bash
#
# setup-docker-ports.sh — derive a deterministic, per-worktree Docker host-port
# block and write it to a worktree-local .env + .ywc-docker-ports persist file.
#
# Never mutates the committed compose / .env (NFR-1). See spec
# docs/ywc-plans/ywc-docker-isolate-codex.md and parent Docker isolate spec.
#
# Usage:
#   setup-docker-ports.sh --task-name <name> --worktree-path <dir> \
#     [--compose-file <file>] [--port-vars VAR1,VAR2]
#
# Exit: 0 = isolation applied OR no-op (AC4); 1 = hardcoded-port (AC5) /
#       salt-chain exhausted / corrupt persist / squatter live-check (AC13) /
#       sanitize-empty.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
. "$SCRIPT_DIR/_lib.sh"

TASK_NAME=""
WORKTREE_PATH=""
COMPOSE_FILE=""
PORT_VARS_OVERRIDE=""

die() { printf 'ywc-docker-isolate setup: %s\n' "$1" >&2; exit 1; }

# --- write_env_block: managed marker block in worktree-local .env -----------
# Replaces an existing ywc-managed block in place, preserving all other lines;
# never touches the committed compose/.env outside the markers (NFR-1).
write_env_block() {
  local wt="$1" proj="$2"; shift 2
  local envf="$wt/.env" begin="# >>> ywc-docker-isolate (managed) >>>"
  local end="# <<< ywc-docker-isolate (managed) <<<"
  local tmp body kv
  body=$(printf '%s\n%s=%s\n' "$begin" "COMPOSE_PROJECT_NAME" "$proj")
  for kv in "$@"; do body=$(printf '%s\n%s' "$body" "$kv"); done
  body=$(printf '%s\n%s' "$body" "$end")
  tmp="$envf.ywc.tmp"
  if [[ -f "$envf" ]]; then
    awk -v b="$begin" -v e="$end" '
      $0==b {skip=1; next} $0==e {skip=0; next} !skip {print}
    ' "$envf" > "$tmp"
  else
    : > "$tmp"
  fi
  printf '%s\n' "$body" >> "$tmp"
  mv "$tmp" "$envf"
  warn_gitignore "$wt"
}

# FR-4.2: warn (do not modify tracked .gitignore — NFR-1) if files are tracked.
warn_gitignore() {
  local wt="$1" f
  command -v git >/dev/null 2>&1 || return 0
  git -C "$wt" rev-parse --is-inside-work-tree >/dev/null 2>&1 || return 0
  for f in ".env" "$PERSIST_FILE_NAME"; do
    if ! git -C "$wt" check-ignore -q "$f" 2>/dev/null; then
      echo "WARN: '$f' is not gitignored in $wt — add it to .gitignore to avoid committing port state" >&2
    fi
  done
}

emit_map() {
  echo "COMPOSE_PROJECT_NAME=$1"; shift
  local kv
  for kv in "$@"; do echo "$kv"; done
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task-name)     TASK_NAME="${2:-}"; shift 2 ;;
    --worktree-path) WORKTREE_PATH="${2:-}"; shift 2 ;;
    --compose-file)  COMPOSE_FILE="${2:-}"; shift 2 ;;
    --port-vars)     PORT_VARS_OVERRIDE="${2:-}"; shift 2 ;;
    *) die "unknown argument: $1" ;;
  esac
done

[[ -n "$TASK_NAME" ]]     || die "--task-name is required"
[[ -n "$WORKTREE_PATH" ]] || die "--worktree-path is required"
[[ -d "$WORKTREE_PATH" ]] || die "--worktree-path does not exist: $WORKTREE_PATH"

SANITIZED=$(sanitize_task_name "$TASK_NAME") \
  || die "task name sanitizes to empty — cannot derive COMPOSE_PROJECT_NAME: '$TASK_NAME'"
PROJECT="${PROJECT_PREFIX}${SANITIZED}"
PERSIST="$WORKTREE_PATH/$PERSIST_FILE_NAME"

# --- FR-1.1 precondition: compose file present? ----------------------------
if [[ -z "$COMPOSE_FILE" ]]; then
  COMPOSE_FILE=$(find_compose_file "$WORKTREE_PATH") || COMPOSE_FILE=""
fi
if [[ -z "$COMPOSE_FILE" || ! -f "$COMPOSE_FILE" ]]; then
  # compose removed but a stale persist remains -> clear it (§A3.1).
  if [[ -f "$PERSIST" ]]; then
    rm -f "$PERSIST"
    echo "compose removed — clearing port record ($PERSIST_FILE_NAME)"
  fi
  echo "no docker — skipping isolation"
  exit 0
fi

# --- FR-2 / FR-1.2: detect isolation-target port VARs ----------------------
# Priority: explicit --port-vars override > compose auto-detect.
# Auto-detect short-syntax ${VAR:-NNNN} env-var port mappings.
# Echoes: first line "HAS_PORTS <0|1>", "HARDCODED <0|1>", then "VAR <name>" lines.
detect_compose_ports() {
  local file="$1"
  if command -v python3 >/dev/null 2>&1 && python3 -c "import yaml" >/dev/null 2>&1; then
    python3 - "$file" <<'PY'
import sys, re, yaml
try:
    doc = yaml.safe_load(open(sys.argv[1])) or {}
except Exception:
    print("HAS_PORTS 0"); print("HARDCODED 0"); sys.exit(0)
services = doc.get("services") or {}
pat = re.compile(r'\$\{([A-Za-z_][A-Za-z0-9_]*):-\d+\}')
has_ports = False; hardcoded = False; varset = {}
if isinstance(services, dict):
    for body in services.values():
        if not isinstance(body, dict):
            continue
        ports = body.get("ports")
        if not ports:
            continue
        for p in ports:
            has_ports = True
            if isinstance(p, dict):
                # long-syntax published: — not auto-detected (§A1.W)
                hardcoded = True
                continue
            s = str(p)
            m = pat.search(s)
            if m:
                varset.setdefault(m.group(1), True)
            elif re.match(r'^"?\d+(\.\d+){0,3}:?\d*', s):
                hardcoded = True
print("HAS_PORTS", 1 if has_ports else 0)
print("HARDCODED", 1 if hardcoded else 0)
for v in sorted(varset):  # ASCII sort == LC_ALL=C for VAR names
    print("VAR", v)
PY
  else
    # awk fallback: scan `ports:` list items for ${VAR:-NNNN}.
    awk '
      /^[[:space:]]*ports:[[:space:]]*$/ { inp=1; print "HAS_PORTS 1"; next }
      inp && /^[[:space:]]*[a-zA-Z_]/ && !/^[[:space:]]*-/ { inp=0 }
      inp && /\$\{[A-Za-z_][A-Za-z0-9_]*:-[0-9]+\}/ {
        match($0, /\$\{[A-Za-z_][A-Za-z0-9_]*:-/);
        v=substr($0, RSTART+2, RLENGTH-4); print "VAR", v
      }
      inp && /-[[:space:]]*"?[0-9]+:/ && !/\$\{/ { print "HARDCODED 1" }
    ' "$file" | LC_ALL=C sort -u
  fi
}

declare -a TARGET_VARS=()
if [[ -n "$PORT_VARS_OVERRIDE" ]]; then
  IFS=',' read -r -a TARGET_VARS <<< "$PORT_VARS_OVERRIDE"
else
  DETECT=$(detect_compose_ports "$COMPOSE_FILE")
  HAS_PORTS=$(printf '%s\n' "$DETECT" | awk '/^HAS_PORTS/{print $2}' | head -n1)
  HARDCODED=$(printf '%s\n' "$DETECT" | awk '/^HARDCODED/{print $2}' | tail -n1)
  while IFS= read -r v; do [[ -n "$v" ]] && TARGET_VARS+=("$v"); done \
    < <(printf '%s\n' "$DETECT" | awk '/^VAR/{print $2}')
  if [[ ${#TARGET_VARS[@]} -eq 0 ]]; then
    if [[ "${HAS_PORTS:-0}" == "1" ]]; then
      # ports exist but none are isolatable env-var mappings (AC5).
      die "ports hardcoded — cannot isolate (use short-syntax \${VAR:-NNNN} or pass --port-vars)"
    fi
    # compose has no host-port mappings at all -> nothing to isolate.
    echo "no host ports to isolate — skipping (COMPOSE_PROJECT_NAME=$PROJECT only)"
    write_env_block "$WORKTREE_PATH" "$PROJECT"
    exit 0
  fi
  if [[ "${HARDCODED:-0}" == "1" ]]; then
    die "ports hardcoded — cannot isolate (mixed hardcoded port mapping detected)"
  fi
fi

for i in "${!TARGET_VARS[@]}"; do
  TARGET_VARS[$i]="${TARGET_VARS[$i]%%=*}"
  [[ "${TARGET_VARS[$i]}" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] \
    || die "invalid port variable name: '${TARGET_VARS[$i]}'"
done

# LC_ALL=C sort target VARs -> 0-based service_index (spec §A1.4 / §A3.1 example).
IFS=$'\n' read -r -d '' -a TARGET_VARS < <(printf '%s\n' "${TARGET_VARS[@]}" | LC_ALL=C sort -u && printf '\0')
if [[ ${#TARGET_VARS[@]} -gt $PORT_BLOCK_WIDTH ]]; then
  die "more than $PORT_BLOCK_WIDTH isolation-target ports (${#TARGET_VARS[@]}) — block width exceeded"
fi

SERVICE_SET=$(extract_service_set "$COMPOSE_FILE") || SERVICE_SET=""

# --- §A1.W: warn if shell exports COMPOSE_PROJECT_NAME (overrides .env) -----
if [[ -n "${COMPOSE_PROJECT_NAME:-}" ]]; then
  echo "WARN: COMPOSE_PROJECT_NAME is exported in the shell ('$COMPOSE_PROJECT_NAME') and overrides .env" >&2
fi

# --- §A3.1 persist read-back ----------------------------------------------
if [[ -f "$PERSIST" ]]; then
  if ! persist_is_valid "$PERSIST"; then
    die "corrupt port map ($PERSIST_FILE_NAME) — delete it and re-run"
  fi
  PERSISTED_SET=$(persist_get "$PERSIST" "SERVICE_SET")
  if [[ "$PERSISTED_SET" == "$SERVICE_SET" ]]; then
    # service-set unchanged -> read-back verbatim, then live-check (AC13).
    declare -a KV=()
    while IFS= read -r line; do KV+=("$line"); done < <(persist_port_lines "$PERSIST")
    # Cross-check the persisted port count against current targets. A truncated
    # persist (header written but port lines lost) would otherwise pass
    # persist_is_valid and silently yield a portless .env -> AC1 regression.
    if [[ ${#KV[@]} -eq ${#TARGET_VARS[@]} && ${#KV[@]} -gt 0 ]]; then
      for line in "${KV[@]}"; do
        port="${line#*=}"
        if check_port_in_use "$port"; then
          die "port squatted ($port, via $(port_check_tool)) — delete $PERSIST_FILE_NAME after freeing it, then re-run"
        fi
      done
      write_env_block "$WORKTREE_PATH" "$PROJECT" "${KV[@]}"
      emit_map "$PROJECT" "${KV[@]}"
      echo "(read-back from $PERSIST_FILE_NAME — deterministic, no re-allocation)"
      exit 0
    fi
    # persisted port set does not cover current targets -> re-allocate.
    rm -f "$PERSIST"
    echo "persisted port set incomplete vs current targets — re-allocating"
  else
    # stale service-set -> invalidate and re-allocate.
    rm -f "$PERSIST"
    echo "service set changed — re-allocating ports"
  fi
fi

# --- §A1.6 first allocation via task-name-derived salt chain ---------------
CHOSEN_BLOCK=""
declare -a CHOSEN_KV=()
for salt in "${SALT_CHAIN[@]}"; do
  hash_input="$SANITIZED"
  [[ -n "$salt" ]] && hash_input="${SANITIZED}-${salt}"
  block=$(hash_block "$hash_input")
  declare -a KV=()
  all_free=1
  idx=0
  for var in "${TARGET_VARS[@]}"; do
    port=$(( PORT_BASE + block * PORT_BLOCK_WIDTH + idx ))
    if check_port_in_use "$port"; then all_free=0; break; fi
    KV+=("${var}=${port}")
    idx=$(( idx + 1 ))
  done
  if [[ $all_free -eq 1 ]]; then
    CHOSEN_BLOCK="$block"; CHOSEN_KV=("${KV[@]}"); break
  fi
done

if [[ -z "$CHOSEN_BLOCK" ]]; then
  die "salt chain exhausted (depth ${#SALT_CHAIN[@]}) — all candidate port blocks are occupied; free ports or rename the task"
fi

# --- write persist atomically (tmp -> mv), then .env -----------------------
TMP="$PERSIST.tmp"
{
  echo "# generated by ywc-docker-isolate setup — DO NOT EDIT"
  echo "SERVICE_SET=$SERVICE_SET"
  echo "COMPOSE_PROJECT_NAME=$PROJECT"
  for kv in "${CHOSEN_KV[@]}"; do echo "$kv"; done
} > "$TMP"
mv "$TMP" "$PERSIST"

write_env_block "$WORKTREE_PATH" "$PROJECT" "${CHOSEN_KV[@]}"
emit_map "$PROJECT" "${CHOSEN_KV[@]}"
echo "(allocated block $CHOSEN_BLOCK — persisted to $PERSIST_FILE_NAME)"
exit 0
