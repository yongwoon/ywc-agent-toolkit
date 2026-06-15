#!/usr/bin/env bash
#
# _lib.sh — shared helpers for ywc-docker-isolate scripts.
#
# Sourced by setup-docker-ports.sh / teardown-docker.sh / audit-docker-stacks.sh.
# The three scripts MUST share these functions verbatim: a sanitize mismatch
# between setup and teardown would make teardown delete the wrong Docker project
# (spec §A1.W), and a port-check divergence would break the live-check (AC13).
#
# This file defines functions and constants only — it does not execute work.

# ---- Constants (spec §A1.W / FR-3.2 / §A2.W) -------------------------------

PORT_BASE=20000          # FR-3.2: base port
PORT_BLOCK_COUNT=100     # FR-3.2: number of blocks (hash % 100)
PORT_BLOCK_WIDTH=100     # FR-3.2: ports per block (service_index 0..99)
SALT_CHAIN=("" "alt1" "alt2" "alt3" "alt4")   # §A1.6 / §A2.W: depth >= 5
PERSIST_FILE_NAME=".ywc-docker-ports"
PROJECT_PREFIX="ywc-"    # FR-3.3: COMPOSE_PROJECT_NAME = ywc-<sanitized-task>
readonly PORT_BASE PORT_BLOCK_COUNT PORT_BLOCK_WIDTH PERSIST_FILE_NAME PROJECT_PREFIX

# ---- sanitize_task_name (spec §A1.W / §A2.W) ------------------------------
#
# lowercase -> [^a-z0-9_-] => '-' -> collapse repeats -> strip edges -> 50-char cut.
# Result must start with a lowercase letter or digit and be non-empty.
# Empty result is a fail-loud condition for the CALLER (returns 1, prints nothing).
sanitize_task_name() {
  local raw="$1" out
  out=$(printf '%s' "$raw" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9_-]+/-/g; s/-+/-/g; s/^-+//; s/-+$//' \
    | cut -c1-50)
  # cut may re-expose a trailing '-' at the 50-char boundary; strip again.
  out=$(printf '%s' "$out" | sed -E 's/-+$//')
  if [[ -z "$out" || ! "$out" =~ ^[a-z0-9] ]]; then
    return 1
  fi
  printf '%s' "$out"
}

# ---- check_port_in_use (spec §A4.1) ---------------------------------------
#
# exit 0 = the TCP port is currently LISTENing (occupied), 1 = free.
# Priority: ss (Linux/iproute2) -> lsof (macOS default) -> netstat (fallback).
# Boundary-safe match avoids 20300 matching 203000.
check_port_in_use() {
  local port="$1"
  if command -v ss >/dev/null 2>&1; then
    ss -tlnp 2>/dev/null | grep -qE ":${port}(\s|$)"
  elif command -v lsof >/dev/null 2>&1; then
    lsof -iTCP:"${port}" -sTCP:LISTEN -nP 2>/dev/null | grep -q .
  elif command -v netstat >/dev/null 2>&1; then
    netstat -an 2>/dev/null | grep -qE "[.:]${port}\b.*LISTEN"
  else
    # No probe tool — fail safe: treat as occupied so the salt chain advances
    # and the squatter live-check (AC13) never silently passes (§A4.1).
    echo "WARN: no port-check tool (ss/lsof/netstat) — assuming port $port in use" >&2
    return 0
  fi
}

# ---- port_check_tool (diagnostic) -----------------------------------------
port_check_tool() {
  if command -v ss >/dev/null 2>&1; then printf 'ss'
  elif command -v lsof >/dev/null 2>&1; then printf 'lsof'
  else printf 'netstat'; fi
}

# ---- find_compose_file (spec FR-1.1) --------------------------------------
#
# Echo the first compose file found in <dir>, or nothing (caller treats as no-op).
find_compose_file() {
  local dir="$1" f
  for f in docker-compose.yml docker-compose.yaml compose.yml compose.yaml; do
    if [[ -f "$dir/$f" ]]; then
      printf '%s' "$dir/$f"
      return 0
    fi
  done
  return 1
}

# ---- extract_service_set (spec §A2.2 / §A2.W) -----------------------------
#
# Echo LC_ALL=C-sorted, comma-joined service names from a compose file.
# python3+yaml is PRIMARY (§A3.W); section-aware awk is the FALLBACK.
# Returns 1 only on a hard parser error; an empty service list echoes "" (valid).
extract_service_set() {
  local compose_file="$1" names
  if command -v python3 >/dev/null 2>&1 && python3 -c "import yaml" >/dev/null 2>&1; then
    names=$(python3 - "$compose_file" <<'PY'
import sys, yaml
try:
    with open(sys.argv[1]) as fh:
        doc = yaml.safe_load(fh) or {}
except Exception:
    sys.exit(3)
svc = doc.get("services") or {}
if isinstance(svc, dict):
    print("\n".join(svc.keys()))
PY
) || return 1
  else
    # Section-aware awk: enter `services:` block, take 2-space-indented keys,
    # stop at the next root-level key. Ignores x-extensions and nested keys.
    names=$(awk '
      /^services:[[:space:]]*$/ { inblk=1; next }
      inblk && /^[^[:space:]#]/ { inblk=0 }
      inblk && /^  [A-Za-z0-9_.-]+:[[:space:]]*$/ {
        line=$0; sub(/:[[:space:]]*$/, "", line); gsub(/^  /, "", line); print line
      }
    ' "$compose_file")
  fi
  printf '%s' "$names" | grep -v '^[[:space:]]*$' | LC_ALL=C sort | paste -sd, -
}

# ---- hash_block (spec FR-3.2 / §A1.4 / §A2.W) -----------------------------
#
# Deterministic 0..99 block from a string, using a hex digest to soften
# modulo bias (2^32 % 100 = 96; documented in references/port-allocation.md).
# md5 (macOS) / md5sum (Linux) preferred; cksum fallback.
hash_block() {
  local s="$1" hex dec
  if command -v md5 >/dev/null 2>&1; then
    hex=$(printf '%s' "$s" | md5 | tr -d ' \n' | cut -c1-8)
  elif command -v md5sum >/dev/null 2>&1; then
    hex=$(printf '%s' "$s" | md5sum | cut -c1-8)
  else
    # cksum -> decimal CRC; hex-encode to keep the same code path.
    hex=$(printf '%s' "$s" | cksum | awk '{printf "%08x", $1}' | cut -c1-8)
  fi
  dec=$((16#$hex))
  printf '%d' $(( dec % PORT_BLOCK_COUNT ))
}

# ---- persist parse helpers (spec §A3.1 / §A4.2) ---------------------------
#
# Safe read of a KEY from .ywc-docker-ports without `source` (arbitrary-code risk).
# Exact key match via awk (no regex interpolation of $key); preserves '=' in value.
persist_get() {
  local file="$1" key="$2"
  awk -F= -v k="$key" '$1==k { sub(/^[^=]*=/, ""); print; exit }' "$file" 2>/dev/null
}

# Echo the *_PORT key=value lines (safe parse).
persist_port_lines() {
  local file="$1"
  grep -E '^[A-Za-z_][A-Za-z0-9_]*_PORT=' "$file" 2>/dev/null
}

# Validity predicate (§A4.2). Returns 0 = valid, 1 = CORRUPT (fail-loud).
persist_is_valid() {
  local file="$1" proj line val
  [[ -s "$file" ]] || return 1                       # zero-byte
  proj=$(persist_get "$file" "COMPOSE_PROJECT_NAME")
  [[ -n "$proj" ]] || return 1                       # missing/empty project name
  while IFS= read -r line; do
    val="${line#*=}"
    [[ "$val" =~ ^[0-9]+$ ]] || return 1             # non-numeric port value
  done < <(persist_port_lines "$file")
  return 0
}
