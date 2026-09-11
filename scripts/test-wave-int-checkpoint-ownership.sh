#!/usr/bin/env bash
# Regression coverage for wave-int checkpoint ownership + tip-SHA verification
# (yw-000037-010 / yw-000037-020): exercises wave-int-owner / wave-int-blocked /
# wave-int-status and the reuse-verification procedure against both
# claude-code/skills/scripts/update-state.py and codex/skills/scripts/update-state.py.
#
# No external test framework, no network access. Every integration-boundary
# scenario runs against a disposable temp git repo with a local bare "origin".

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

DEFAULT_ROOTS=(
  "claude-code/skills/scripts/update-state.py"
  "codex/skills/scripts/update-state.py"
)

PASS_COUNT=0
FAIL_COUNT=0

assert_eq() {
  local expected="$1" actual="$2" label="$3"
  if [ "$expected" = "$actual" ]; then
    PASS_COUNT=$((PASS_COUNT + 1))
    echo "ok - $label"
  else
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "FAIL - $label: expected [$expected], got [$actual]"
  fi
}

assert_contains() {
  local haystack="$1" needle="$2" label="$3"
  if [[ "$haystack" == *"$needle"* ]]; then
    PASS_COUNT=$((PASS_COUNT + 1))
    echo "ok - $label"
  else
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "FAIL - $label: expected to contain [$needle], got [$haystack]"
  fi
}

# --- arg parsing -------------------------------------------------------------

ROOTS=("${DEFAULT_ROOTS[@]}")
if [ "${1:-}" = "--root" ]; then
  ROOTS=("$2")
fi

# --- helpers -------------------------------------------------------------

# Runs a python3 command against the script under test in a given cwd,
# capturing stdout+stderr into OUT and the exit code into RC without tripping
# `set -e`.
run_capture() {
  local cwd="$1"; shift
  set +e
  OUT="$(cd "$cwd" && python3 "$1" "${@:2}" 2>&1)"
  RC=$?
  set -e
}

write_state() {
  local wd="$1" json="$2"
  printf '%s' "$json" > "$wd/.ywc-run-state.json"
}

read_state_field() {
  local wd="$1" expr="$2"
  python3 -c "import json,sys; s=json.load(open('$wd/.ywc-run-state.json')); print($expr)"
}

new_workdir() {
  mktemp -d
}

# Classifies an exit code as "zero" or "nonzero" — git's failure exit codes
# for a missing ref vary (1, 2, 128) depending on the exact command, so
# assertions on "did this fail" compare classes, not a specific number.
rc_class() {
  if [ "$1" -eq 0 ]; then echo "zero"; else echo "nonzero"; fi
}

# --- unit-boundary scenarios (no git repo) -------------------------------

run_unit_scenarios() {
  local root="$1" abs_root="$2"

  # AC7: init-parallel writes a top-level run_id, 8 hex chars.
  local wd; wd=$(new_workdir)
  run_capture "$wd" "$abs_root" init-parallel --mode local-merge --tasks-dir tasks/ \
    --waves '[{"wave":0,"tasks":["t"],"has_contract":true}]'
  local run_id; run_id=$(read_state_field "$wd" "s['run_id']")
  if [[ "$run_id" =~ ^[0-9a-f]{8}$ ]]; then
    assert_eq "match" "match" "AC7 run_id format ($root)"
  else
    assert_eq "8 hex chars" "$run_id" "AC7 run_id format ($root)"
  fi
  rm -rf "$wd"

  # AC10 / wave-int-owner: executor-mismatch, run_id-unset, wave-not-found.
  wd=$(new_workdir)
  write_state "$wd" '{"executor":"sequential","run_id":"aaaaaaaa","waves":[{"wave":0}]}'
  run_capture "$wd" "$abs_root" wave-int-owner 0 --tip-sha abc
  assert_eq "1" "$RC" "wave-int-owner executor-mismatch exit ($root)"
  assert_contains "$OUT" "requires executor='parallel'" "wave-int-owner executor-mismatch message ($root)"

  write_state "$wd" '{"executor":"parallel","waves":[{"wave":0}]}'
  run_capture "$wd" "$abs_root" wave-int-owner 0 --tip-sha abc
  assert_eq "1" "$RC" "wave-int-owner run_id-unset exit ($root)"
  assert_contains "$OUT" "re-run init-parallel" "wave-int-owner run_id-unset message ($root)"

  write_state "$wd" '{"executor":"parallel","run_id":"aaaaaaaa","waves":[]}'
  run_capture "$wd" "$abs_root" wave-int-owner 0 --tip-sha abc
  assert_eq "1" "$RC" "wave-int-owner wave-not-found exit ($root)"
  assert_contains "$OUT" "wave 0 not found in state" "wave-int-owner wave-not-found message ($root)"

  # AC10 / wave-int-blocked: identical three die() rows.
  write_state "$wd" '{"executor":"sequential","run_id":"aaaaaaaa","waves":[{"wave":0}]}'
  run_capture "$wd" "$abs_root" wave-int-blocked 0 --reason test-reason
  assert_eq "1" "$RC" "wave-int-blocked executor-mismatch exit ($root)"
  assert_contains "$OUT" "requires executor='parallel'" "wave-int-blocked executor-mismatch message ($root)"

  write_state "$wd" '{"executor":"parallel","waves":[{"wave":0}]}'
  run_capture "$wd" "$abs_root" wave-int-blocked 0 --reason test-reason
  assert_eq "1" "$RC" "wave-int-blocked run_id-unset exit ($root)"
  assert_contains "$OUT" "re-run init-parallel" "wave-int-blocked run_id-unset message ($root)"

  write_state "$wd" '{"executor":"parallel","run_id":"aaaaaaaa","waves":[]}'
  run_capture "$wd" "$abs_root" wave-int-blocked 0 --reason test-reason
  assert_eq "1" "$RC" "wave-int-blocked wave-not-found exit ($root)"
  assert_contains "$OUT" "wave 0 not found in state" "wave-int-blocked wave-not-found message ($root)"

  # AC10 / wave-int-status: executor-mismatch and wave-not-found only; a
  # run_id-unset state must NOT die() (Iteration 3's negative case).
  write_state "$wd" '{"executor":"sequential","run_id":"aaaaaaaa","waves":[{"wave":0}]}'
  run_capture "$wd" "$abs_root" wave-int-status 0
  assert_eq "1" "$RC" "wave-int-status executor-mismatch exit ($root)"
  assert_contains "$OUT" "requires executor='parallel'" "wave-int-status executor-mismatch message ($root)"

  write_state "$wd" '{"executor":"parallel","run_id":"aaaaaaaa","waves":[]}'
  run_capture "$wd" "$abs_root" wave-int-status 0
  assert_eq "1" "$RC" "wave-int-status wave-not-found exit ($root)"
  assert_contains "$OUT" "wave 0 not found in state" "wave-int-status wave-not-found message ($root)"

  write_state "$wd" '{"executor":"parallel","waves":[{"wave":0}]}'
  run_capture "$wd" "$abs_root" wave-int-status 0
  assert_eq "0" "$RC" "wave-int-status run_id-unset does not die ($root)"
  assert_eq "unset unset" "$OUT" "wave-int-status run_id-unset prints unset unset ($root)"

  # Success-path print-format assertions, matching the API Contract exactly.
  write_state "$wd" '{"executor":"parallel","run_id":"abcdef12","waves":[{"wave":0}]}'
  run_capture "$wd" "$abs_root" wave-int-owner 0 --tip-sha deadbeef
  assert_eq "0" "$RC" "wave-int-owner success exit ($root)"
  assert_eq "wave 0: integration_branch_owner -> abcdef12, tip_sha -> deadbeef" "$OUT" \
    "wave-int-owner success print format ($root)"

  run_capture "$wd" "$abs_root" wave-int-blocked 0 --reason wave-int-tip-mismatch --detail "some detail"
  assert_eq "0" "$RC" "wave-int-blocked success (with detail) exit ($root)"
  assert_eq "wave 0: status -> BLOCKED (wave-int-tip-mismatch) — some detail" "$OUT" \
    "wave-int-blocked success print format with detail ($root)"

  write_state "$wd" '{"executor":"parallel","run_id":"abcdef12","waves":[{"wave":0}]}'
  run_capture "$wd" "$abs_root" wave-int-blocked 0 --reason wave-int-tip-mismatch
  assert_eq "0" "$RC" "wave-int-blocked success (no detail) exit ($root)"
  assert_eq "wave 0: status -> BLOCKED (wave-int-tip-mismatch)" "$OUT" \
    "wave-int-blocked success print format without detail ($root)"

  write_state "$wd" '{"executor":"parallel","run_id":"abcdef12","waves":[{"wave":0}]}'
  run_capture "$wd" "$abs_root" wave-int-owner 0 --tip-sha deadbeef
  run_capture "$wd" "$abs_root" wave-int-status 0
  assert_eq "0" "$RC" "wave-int-status success exit ($root)"
  assert_eq "abcdef12 deadbeef" "$OUT" "wave-int-status success print format ($root)"

  rm -rf "$wd"
}

# --- integration-boundary scenarios (disposable git repo) -------------------

setup_git_repo() {
  local wd="$1"
  local origin="$wd/origin.git"
  local work="$wd/work"
  git init -q --bare "$origin"
  git init -q -b main "$work"
  (
    cd "$work"
    git config user.email test@example.com
    git config user.name "Test"
    git remote add origin "$origin"
    echo base > base.txt
    git add base.txt
    git commit -q -m base
    git push -q origin main
  )
}

run_integration_scenarios() {
  local root="$1" abs_root="$2"
  local wd; wd=$(new_workdir)
  setup_git_repo "$wd"
  local work="$wd/work"

  # Shared state file for all scenarios in this repo — one run_id for the
  # whole integration-boundary suite, one wave per scenario.
  local waves_json='[{"wave":0,"tasks":["t"],"has_contract":true},{"wave":1,"tasks":["t"],"has_contract":true},{"wave":2,"tasks":["t"],"has_contract":true},{"wave":3,"tasks":["t"],"has_contract":true},{"wave":4,"tasks":["t"],"has_contract":true},{"wave":5,"tasks":["t"],"has_contract":true},{"wave":6,"tasks":["t"],"has_contract":true}]'
  run_capture "$work" "$abs_root" init-parallel --mode local-merge --tasks-dir tasks/ --waves "$waves_json"
  local run_id; run_id=$(read_state_field "$work" "s['run_id']")

  # AC1: same-run resume tolerates an intervening per-task merge that never
  # re-recorded ownership — the ancestor check, not exact equality, must pass.
  (
    cd "$work"
    git checkout -q -b wave-int/0 main
    git push -q origin wave-int/0
  )
  local tip0; tip0=$(cd "$work" && git rev-parse wave-int/0)
  run_capture "$work" "$abs_root" wave-int-owner 0 --tip-sha "$tip0"
  (
    cd "$work"
    echo task1 > t1.txt
    git add t1.txt
    git commit -q -m "task1 (unrecorded per-task merge)"
  )
  run_capture "$work" "$abs_root" wave-int-status 0
  assert_eq "$run_id $tip0" "$OUT" "AC1 recorded checkpoint before per-task merge ($root)"
  set +e
  (cd "$work" && git merge-base --is-ancestor "$tip0" wave-int/0)
  local ac1_rc=$?
  set -e
  assert_eq "0" "$ac1_rc" "AC1 ancestor-check passes after unrecorded per-task merge, reuse allowed ($root)"

  # AC2 (unset-owner variant): a branch with no wave-int-owner call ever
  # recorded must report "no owner" via wave-int-status.
  (
    cd "$work"
    git checkout -q -b wave-int/1 main
    git push -q origin wave-int/1
  )
  run_capture "$work" "$abs_root" wave-int-status 1
  assert_eq "unset unset" "$OUT" "AC2 unset-owner reported by wave-int-status ($root)"
  run_capture "$work" "$abs_root" wave-int-blocked 1 --reason wave-int-ownership-mismatch \
    --detail "branch=wave-int/1 no owner recorded for run $run_id"
  assert_eq "0" "$RC" "AC2 unset-owner wave-int-blocked call succeeds ($root)"
  local status1; status1=$(read_state_field "$work" "s['waves'][1]['status']")
  assert_eq "BLOCKED" "$status1" "AC2 unset-owner wave marked BLOCKED ($root)"

  # AC2 (owner-mismatch variant): recorded owner belongs to a different run_id.
  (
    cd "$work"
    git checkout -q -b wave-int/2 main
    git push -q origin wave-int/2
  )
  local tip2; tip2=$(cd "$work" && git rev-parse wave-int/2)
  run_capture "$work" "$abs_root" wave-int-owner 2 --tip-sha "$tip2"
  local recorded_owner2; recorded_owner2=$(read_state_field "$work" "s['waves'][2]['integration_branch_owner']")
  local other_run_id="ffffffff"
  assert_eq "1" "$([ "$recorded_owner2" != "$other_run_id" ] && echo 1 || echo 0)" \
    "AC2 owner-mismatch: recorded owner differs from a different run's run_id ($root)"
  run_capture "$work" "$abs_root" wave-int-blocked 2 --reason wave-int-ownership-mismatch \
    --detail "branch=wave-int/2 owner=$recorded_owner2 current-run=$other_run_id"
  local status2; status2=$(read_state_field "$work" "s['waves'][2]['status']")
  assert_eq "BLOCKED" "$status2" "AC2 owner-mismatch wave marked BLOCKED ($root)"

  # AC3: tip-SHA divergence detected via merge-base --is-ancestor, distinct
  # from a cat-file-failure (both variants below).
  (
    cd "$work"
    git checkout -q -b wave-int/3 main
    git push -q origin wave-int/3
  )
  local tip3; tip3=$(cd "$work" && git rev-parse wave-int/3)
  run_capture "$work" "$abs_root" wave-int-owner 3 --tip-sha "$tip3"
  (
    cd "$work"
    git checkout -q main
    git checkout -q --orphan wave-int-3-orphan
    git commit -q --allow-empty -m orphan
    git branch -f wave-int/3 wave-int-3-orphan
    git checkout -q wave-int/3
    git branch -D wave-int-3-orphan
  )
  set +e
  (cd "$work" && git cat-file -e "$tip3")
  local cat_file_rc=$?
  (cd "$work" && git merge-base --is-ancestor "$tip3" wave-int/3)
  local ancestor_rc=$?
  set -e
  assert_eq "0" "$cat_file_rc" "AC3 tip-mismatch variant: recorded sha still reachable ($root)"
  assert_eq "1" "$ancestor_rc" "AC3 tip-mismatch variant: ancestor check fails (real divergence) ($root)"
  run_capture "$work" "$abs_root" wave-int-blocked 3 --reason wave-int-tip-mismatch \
    --detail "branch=wave-int/3 recorded=$tip3 actual=$(cd "$work" && git rev-parse wave-int/3)"
  local status3; status3=$(read_state_field "$work" "s['waves'][3]['reason']")
  assert_eq "wave-int-tip-mismatch" "$status3" "AC3 tip-mismatch reason recorded ($root)"

  # AC3 (cat-file-failure variant): the recorded sha is pruned away entirely.
  (
    cd "$work"
    git checkout -q -b wave-int/4 main
    echo w4 > w4.txt
    git add w4.txt
    git commit -q -m w4
  )
  local tip4; tip4=$(cd "$work" && git rev-parse wave-int/4)
  run_capture "$work" "$abs_root" wave-int-owner 4 --tip-sha "$tip4"
  (
    cd "$work"
    git checkout -q main
    git branch -f wave-int/4 main
    git reflog expire --expire=now --all
    git gc -q --prune=now
  )
  set +e
  (cd "$work" && git cat-file -e "$tip4")
  local cat_file_rc4=$?
  set -e
  assert_eq "1" "$cat_file_rc4" "AC3 cat-file-failure variant: recorded sha unreachable after prune ($root)"
  run_capture "$work" "$abs_root" wave-int-blocked 4 --reason wave-int-materialize-failed \
    --detail "branch=wave-int/4 recorded-sha=$tip4 unreachable"
  local reason4; reason4=$(read_state_field "$work" "s['waves'][4]['reason']")
  assert_eq "wave-int-materialize-failed" "$reason4" "AC3 cat-file-failure reason recorded ($root)"

  # AC4: origin-only branch materialization — pushed to origin, deleted
  # locally, must be fetchable back into a local tracking ref.
  (
    cd "$work"
    git checkout -q -b wave-int/5 main
    git push -q origin wave-int/5
    git checkout -q main
    git branch -D wave-int/5
  )
  set +e
  (cd "$work" && git rev-parse --verify wave-int/5 2>/dev/null)
  local before_rc=$?
  set -e
  assert_eq "nonzero" "$(rc_class "$before_rc")" "AC4 branch absent locally before materialization ($root)"
  (cd "$work" && git fetch -q origin wave-int/5:wave-int/5)
  set +e
  (cd "$work" && git rev-parse --verify wave-int/5 >/dev/null 2>&1)
  local after_rc=$?
  set -e
  assert_eq "0" "$after_rc" "AC4 branch materialized locally after fetch ($root)"

  # AC9: checkpoint claims ownership of a branch that no longer exists
  # anywhere (local or origin) — must classify as branch-missing.
  (
    cd "$work"
    git checkout -q -b wave-int/6 main
    git push -q origin wave-int/6
  )
  local tip6; tip6=$(cd "$work" && git rev-parse wave-int/6)
  run_capture "$work" "$abs_root" wave-int-owner 6 --tip-sha "$tip6"
  (
    cd "$work"
    git checkout -q main
    git branch -D wave-int/6
    git push -q origin --delete wave-int/6
  )
  set +e
  (cd "$work" && git rev-parse --verify wave-int/6 2>/dev/null)
  local local_rc=$?
  (cd "$work" && git ls-remote --exit-code --heads origin wave-int/6 >/dev/null 2>&1)
  local origin_rc=$?
  set -e
  assert_eq "nonzero" "$(rc_class "$local_rc")" "AC9 branch absent locally ($root)"
  assert_eq "nonzero" "$(rc_class "$origin_rc")" "AC9 branch absent on origin ($root)"
  run_capture "$work" "$abs_root" wave-int-blocked 6 --reason wave-int-branch-missing \
    --detail "branch=wave-int/6 recorded-owner=$run_id recorded-tip=$tip6"
  local reason6; reason6=$(read_state_field "$work" "s['waves'][6]['reason']")
  assert_eq "wave-int-branch-missing" "$reason6" "AC9 branch-missing reason recorded ($root)"

  rm -rf "$wd"
}

# --- main --------------------------------------------------------------------

for root in "${ROOTS[@]}"; do
  abs_root="$REPO_ROOT/$root"
  if [ ! -f "$abs_root" ]; then
    echo "FAIL - script not found: $abs_root" >&2
    FAIL_COUNT=$((FAIL_COUNT + 1))
    continue
  fi
  run_unit_scenarios "$root" "$abs_root"
  run_integration_scenarios "$root" "$abs_root"
done

echo "$PASS_COUNT passed, $FAIL_COUNT failed"
if [ "$FAIL_COUNT" -gt 0 ]; then
  exit 1
fi
