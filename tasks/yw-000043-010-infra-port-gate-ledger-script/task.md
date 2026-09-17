# yw-000043-010-infra-port-gate-ledger-script — Implementation Checklist

## Prerequisites
- [ ] None — this is a root task; confirm no other in-flight task already owns `claude-code/skills/ywc-verify-done/` or is mid-edit on `claude-code/skills/CLAUDE.md`'s Bundled Execution Scripts table

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md`: `claude-code/skills/ywc-verify-done/scripts/gate-check.py`, `claude-code/skills/ywc-verify-done/scripts/test_gate_check.py`, `claude-code/skills/ywc-verify-done/references/gate-ledger.md`, and only the `## Bundled Execution Scripts` table inside `claude-code/skills/CLAUDE.md`
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if the upstream source files at `/Users/yongwoon.kim/Desktop/yongwoon/source/private/develop-with-llm/tools/claude-code/skills/ywc-verify-done/{scripts/gate-check.py,scripts/test_gate_check.py,references/gate-ledger.md}` are missing or unreadable — do not reconstruct from memory
- [ ] Stop if a diff against the upstream file reveals a behavioral difference beyond the two permitted edit categories (path strings; the one dangling-reference sentence) — do not silently "improve" ported logic
- [ ] Stop if `claude-code/skills/CLAUDE.md`'s `## Bundled Execution Scripts` table has already gained a `gate-check.py` row (would indicate a race with another task/session)

## Implementation Steps

- [ ] **Port `gate-check.py`**
  - [ ] Copy `develop-with-llm/tools/claude-code/skills/ywc-verify-done/scripts/gate-check.py` to `claude-code/skills/ywc-verify-done/scripts/gate-check.py` verbatim
  - [ ] Replace every embedded example invocation string containing `tools/claude-code/skills/ywc-verify-done/scripts/gate-check.py` with `claude-code/skills/ywc-verify-done/scripts/gate-check.py`
  - [ ] In the module docstring, replace the reference to `docs/ywc-plans/20260824-verify-done-gate-ledger.md` with a reference to `docs/ywc-plans/20260917-verify-done-gate-ledger-port.md`, or drop the sentence if it reads awkwardly standalone
  - [ ] Confirm no other line differs from the upstream source (diff the two files mentally or with `diff`, accounting only for the edits above)
  - [ ] Verify `stop_process_group()` still sends `SIGKILL` to the whole process group unconditionally after the grace period (not only on a `wait()` timeout) — this is the security property FR-1 requires to survive unmodified
  - [ ] Verify `matches_expect()` still runs the regex match inside a `multiprocessing.Process` capped at 5 seconds (never a thread) — the second security property FR-1 requires to survive unmodified

- [ ] **Port `test_gate_check.py`**
  - [ ] Copy `develop-with-llm/tools/claude-code/skills/ywc-verify-done/scripts/test_gate_check.py` to `claude-code/skills/ywc-verify-done/scripts/test_gate_check.py` verbatim
  - [ ] Apply the same path-string adjustment wherever the test file invokes `gate-check.py` by path (`tools/claude-code/skills/...` → `claude-code/skills/...`)
  - [ ] Confirm the file still uses only Python 3 stdlib (no new imports introduced by the port)

- [ ] **Port `references/gate-ledger.md`**
  - [ ] Copy `develop-with-llm/tools/claude-code/skills/ywc-verify-done/references/gate-ledger.md` to `claude-code/skills/ywc-verify-done/references/gate-ledger.md` verbatim
  - [ ] Rewrite the opening sentence to drop the dangling `external-repositories/unlazy/references/gates.md` reference and the "narrowed subset of X" framing — write a self-contained opening sentence instead
  - [ ] Adjust the three example invocation lines' repo-relative path prefix the same way as `gate-check.py` (`tools/claude-code/skills/...` → `claude-code/skills/...`)
  - [ ] Confirm the explicit "read every `CHECK:` line before running a ledger you did not author yourself" security warning is preserved verbatim (Critical Surfaces requirement)

- [ ] **Register in `claude-code/skills/CLAUDE.md`**
  - [ ] Open `claude-code/skills/CLAUDE.md`, locate `## Bundled Execution Scripts` (~line 325) and its table
  - [ ] Append one new row following the existing `Script | Skill | Purpose` column convention: script path `ywc-verify-done/scripts/gate-check.py <ledger> [--status\|--reverify]`, skill `ywc-verify-done`, purpose stating the three modes and exit-code semantics (0 = all runnable gates met / well-formed on `--status`; 1 = at least one unmet or malformed ledger)
  - [ ] Do not reformat, reorder, or otherwise touch any other row in the table

## Task Verify
- [ ] `python3 claude-code/skills/ywc-verify-done/scripts/test_gate_check.py` — stdout ends in `ALL PASS`, exit code `0`
- [ ] `grep -n "gate-check.py" claude-code/skills/CLAUDE.md` — exactly one match, with a path resolving from repo root
- [ ] `test -f claude-code/skills/ywc-verify-done/scripts/gate-check.py && echo OK`

## Verification
- [ ] Self-check passes: `python3 claude-code/skills/ywc-verify-done/scripts/test_gate_check.py` → `ALL PASS`, exit `0` (AC1)
- [ ] `--status` mode is read-only: manually construct a scratch ledger with a `CHECK:` that would write a temp file, run `python3 claude-code/skills/ywc-verify-done/scripts/gate-check.py --status <scratch-ledger>`, confirm the temp file is never created (AC2)
- [ ] Default mode executes only unmet gates: construct a scratch ledger with one gate carrying a valid cached-PASS `EVIDENCE:` fingerprint and one `pending` gate, run default mode, confirm the cached-PASS gate's report line reads `PASS (skipped, fingerprint matched)` (AC3)
- [ ] `--reverify` forces re-execution: construct a scratch ledger where a previously-passing gate's command would now fail, run `--reverify`, confirm `EVIDENCE:` is rewritten to `FAIL; ...` and exit code is `1` (AC4)
- [ ] Malformed ledger fails closed: construct a scratch ledger with a gate having only `CHECK:` or only `EXPECT:`, run default mode, confirm stderr names the offending gate id and missing field, exit code `1` (AC5)
- [ ] Manual gates never block exit 0: construct a scratch ledger with only manual gates (neither `CHECK:` nor `EXPECT:`), run default mode, confirm each reports `manual (skipped)` and exit code `0` (AC6)
- [ ] Registration discoverable: `grep -n "gate-check.py" claude-code/skills/CLAUDE.md` returns exactly one match; `test -f claude-code/skills/ywc-verify-done/scripts/gate-check.py` succeeds (AC7)

## Implementation Notes (optional)

<!-- Starts empty at generation time. Add bullets here in real time as
     unanticipated issues surface during implementation. -->
