#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
audit="$script_dir/scripts/audit-skills.sh"
codex_audit="$(CDPATH= cd -- "$script_dir/../../.." && pwd)/codex/skills/ywc-skill-author/scripts/audit-skills.sh"
tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/audit-skills-test.XXXXXX")"
trap 'rm -rf "$tmpdir"' EXIT
root="$tmpdir/root"
counterpart="$tmpdir/counterpart"
mkdir -p "$root/ywc-alpha/references" "$root/ywc-beta/references" "$counterpart/ywc-alpha"

{
  printf '%s\n' 'Use $ywc-beta before continuing.' '@ywc-force-load'
  i=2
  while [ "$i" -le 451 ]; do
    printf '# fixture line %s\n' "$i"
    i=$((i + 1))
  done
  printf '%s\n' 'linked.md'
} > "$root/ywc-alpha/SKILL.md"
printf '%s\n' 'linked reference' > "$root/ywc-alpha/references/linked.md"
printf '%s\n' 'orphan reference' > "$root/ywc-beta/references/orphan.md"

bash "$audit" --root "$root" --counterpart-root "$counterpart" > "$tmpdir/report"
grep -Fx '## Inventory' "$tmpdir/report"
grep -Fx -- '- ywc-alpha: 453 lines' "$tmpdir/report"
grep -Fx '## Near Line Cap' "$tmpdir/report"
grep -Fx -- '- ywc-alpha: 453 lines' "$tmpdir/report"
grep -Fx -- '- ywc-beta/orphan.md' "$tmpdir/report"
grep -F -- '- ywc-alpha:2:@ywc-force-load' "$tmpdir/report"
grep -Fx -- '- ywc-alpha -> ywc-beta' "$tmpdir/report"
grep -Fx -- '- ywc-beta' "$tmpdir/report"

set +e
bash "$audit" --root /missing --counterpart-root "$counterpart" >/dev/null 2>&1
missing_status=$?
bash "$audit" --root "$root" --counterpart-root "$counterpart" --near-line-cap 0 >/dev/null 2>&1
cap_status=$?
set -e
[ "$missing_status" -eq 2 ] && [ "$cap_status" -eq 2 ]
cmp -s "$audit" "$codex_audit"
bash "$audit" --root "$root/ywc-alpha" --counterpart-root "$counterpart/ywc-alpha" > "$tmpdir/single-report"
grep -Fx -- '- ywc-alpha: 453 lines' "$tmpdir/single-report"
echo "PASS: audit-skills contract fixtures"
