# yw-000038-010-domain-hardener-needs-context-gating-claude

## Purpose
Close the promotion-gate gap in the claude-code `ywc-parallel-executor`: a wave whose Hardener dispatch returns `NEEDS_CONTEXT` (missing/corrupt `Baseline` per `quality-gates.md:93`) currently has no home in the `hardener_verdict` checkpoint contract, so it can silently promote to base and stamp `wave-complete` exactly like a passing wave. This task extends the checkpoint value domain, the promotion gate, the Step 4g/4i cleanup-exclusion and terminal-state logic, the resume documentation, and `resume-state.py` so `NEEDS_CONTEXT` blocks promotion and is never reported `valid` on resume — for the claude-code root.

## Scope
- `claude-code/skills/scripts/update-state.py:210` — extend `VALID_HARDENER_VERDICTS` to `{"absent", "PASS", "BLOCKED", "NEEDS_CONTEXT"}` (FR-1).
- `claude-code/skills/ywc-parallel-executor/SKILL.md:357` — checkpoint-write instruction gains a `NEEDS_CONTEXT` branch: written when Hardener ran under an `enforced` contract and returned `NEEDS_CONTEXT` (FR-2).
- `claude-code/skills/ywc-parallel-executor/SKILL.md:369` — promotion condition: "never on `BLOCKED`" → "never on `BLOCKED` or `NEEDS_CONTEXT`" (FR-2).
- `claude-code/skills/ywc-parallel-executor/SKILL.md:373` and `:410` — Step 4g cleanup-exclusion condition and Step 4i terminal-state bucket condition extend from `hardener_verdict == "BLOCKED"` to `hardener_verdict in {"BLOCKED", "NEEDS_CONTEXT"}`; introduce the label `Hardener-NEEDS_CONTEXT` alongside the existing `Hardener-BLOCKED` (FR-3 — two distinct labels chosen, resolving the spec's first Open Question, since the Completion Report must let a human resuming later tell "supply context" apart from "make a BLOCKED-recovery decision").
- `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md:101` — reword the "On a blocking Hardener verdict" preservation paragraph to cover both `BLOCKED` and `NEEDS_CONTEXT` under one "blocking verdict" umbrella (FR-2).
- `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md`:
  - `### State File Format` — update the `hardener_verdict` comment/enum description to name all four values (FR-1).
  - `### Resume with wave-int/<N>` — insert case 4 after today's case 3: `hardener_verdict == NEEDS_CONTEXT` stops resume, prints the recorded missing-context detail, and requires the context to be supplied (not a bare confirmation) before an unprompted Hardener rerun — distinct from case 3's explicit-confirmation requirement (FR-4).
- `claude-code/skills/ywc-parallel-executor/scripts/resume-state.py:104-134` — after computing `pending`/`merged_in_wave` for the `in_progress` wave, when `pending` is empty, read `wave.get("hardener_verdict")`. `None`/`"absent"`/`"PASS"` fall through unchanged to today's `"valid"` result; `"BLOCKED"` short-circuits to `status: "blocked"`; `"NEEDS_CONTEXT"` short-circuits to `status: "needs_context"` — both carrying `wave.get("reason")`/`wave.get("blocked_detail")` (`.get()` with absent-key fallback, never `null` in JSON output) and the same top-level shape as today's `"valid"` result (`resume_wave`, `mode`, `tasks_dir`) (FR-4).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260911-hardener-needs-context-gating.md` — full spec; this task implements FR-1, FR-2, FR-3, FR-4 (claude-code half)
- `docs/ywc-plans/20260911-hardener-needs-context-gating.md#acceptance-criteria` — AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC9 (claude-code half of each; AC8 is verified jointly by `yw-000038-030`)
- `docs/ywc-plans/20260911-hardener-needs-context-gating.md#api-contract` — exact `die()` message text (`sorted()` order) and `resume-state.py`'s new JSON result shape
- `docs/ywc-plans/20260911-hardener-needs-context-gating.md#existing-constraints-touched` — the exact before/after wording table this task's doc edits must match
- `claude-code/skills/scripts/update-state.py:210-221` (`VALID_HARDENER_VERDICTS`, `cmd_hardener_verdict`)
- `claude-code/skills/ywc-parallel-executor/SKILL.md:357,369,373,410`
- `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md:101`
- `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md:46-104` (State File Format + Resume with `wave-int/<N>`)
- `claude-code/skills/ywc-parallel-executor/scripts/resume-state.py:59-153` (`fail()` helper shape, `in_progress` branch, unconditional `"valid"` result)

### Summary
`hardener_verdict` today only ever takes `absent`/`PASS`/`BLOCKED`; `cmd_hardener_verdict`'s `die()` already prints `sorted(VALID_HARDENER_VERDICTS)`, so extending the set is the only code change FR-1 needs there. The promotion gate, Step 4g/4i bucket logic, and resume documentation all currently branch on `BLOCKED` alone and must be extended to also catch `NEEDS_CONTEXT` — but the *recovery* semantics differ: `BLOCKED` requires explicit user confirmation before a Hardener rerun, `NEEDS_CONTEXT` requires the missing context to be supplied first (no confirmation gate), matching the per-subagent `NEEDS_CONTEXT` convention already documented at `SKILL.md:220`. `resume-state.py` is the only executable code among these five files carrying real behavior change; the rest are LLM-followed procedure documents verified by text-presence checks (AC3, AC7, AC9).

### Out of Scope (from spec)
- The codex root's identical hand-edit — `yw-000038-020`.
- The regression test file exercising both roots — `yw-000038-030`.
- Hardener's own decision logic for *when* it emits `NEEDS_CONTEXT` — `ywc-qa-engineer`'s and `quality-gates.md`'s existing behavior, unchanged.
- `promotion_retry_count` / `PROMOTION_RETRY_CAP` mechanics — unchanged.
- Non-contract-bearing waves (`integration_branch` is `None`) and `--per-task-pr` mode — unaffected, per spec `## Out of Scope`.
- Both `subagent-status-actions.md` files — governs per-subagent dispatch reply handling, not this wave-boundary checkpoint field; no edit required.
- The `gate_state` sentinel vocabulary in `quality-gates.md` §9 — out of scope per spec.

## Criticality
`normal` — internal orchestration state (`.ywc-run-state.json`, `.gitignore`d); no auth/payment/PII surface (spec's own `## Critical Surfaces` states N/A).

## Dependencies

### Depends On
- (None — root task, parallel-safe against `yw-000038-020` since the two touch disjoint files)

### Depended By
- `yw-000038-030-test-hardener-needs-context-gating-regression` — exercises this task's `update-state.py`/`resume-state.py` changes against the claude-code root.

## Key Files
- `claude-code/skills/scripts/update-state.py` — `VALID_HARDENER_VERDICTS` set literal.
- `claude-code/skills/ywc-parallel-executor/SKILL.md` — Step 4e.5 checkpoint instruction, Step 4e.6 promotion condition, Step 4g cleanup-exclusion condition, Step 4i terminal-state bucket.
- `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md` — promotion/preservation paragraph.
- `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md` — State File Format `hardener_verdict` description, Resume with `wave-int/<N>` case 4.
- `claude-code/skills/ywc-parallel-executor/scripts/resume-state.py` — new `hardener_verdict` inspection branch on the `in_progress`/`pending`-empty path.

## Notes
- Label choice (spec Open Question 1): use two distinct labels, `Hardener-BLOCKED` (unchanged) and `Hardener-NEEDS_CONTEXT` (new), rather than one combined bucket — keeps the Completion Report / Step 4i audit text able to tell a human resuming later whether to supply context (`NEEDS_CONTEXT`) or make a BLOCKED-recovery decision (`BLOCKED`).
- `resume-state.py`'s new non-`"valid"` result is a *non-error* stop, distinct from the existing `fail()` helper's `status: "error"` shape — do not route through `fail()`. Introduce a small sibling that prints the equivalent `CANNOT RESUME` block (naming wave, verdict, `reason`, `blocked_detail`) and exits with a non-zero code (exit 1 is sufficient — no existing caller branches on this script's exit code, only its `status` field, per `checkpoint-resume.md`'s "Manual Inspection" usage; spec Open Question 2, left to implementer, resolved here as exit 1 for consistency with `fail()`'s existing exit code).
- Follow `~/.claude/rules/python/coding-style.md`: PEP 8, type annotations on all new/modified function signatures (matches `resume-state.py`'s existing style).
- AC4's guard is a documentation/logic check, not a new code guard: `update-state.py wave-complete` already refuses while any task is `pending`; the new resume validator (this task) is what actually prevents a `NEEDS_CONTEXT`-blocked wave from silently completing on a *later* resume. `wave-integration-branch.md`'s promotion-section citation of `update-state.py:162-163` for this guard is stale (moved to `:173-174`) — a pre-existing issue flagged in the spec, no fix required as part of this task.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/scripts/update-state.py`
- `claude-code/skills/ywc-parallel-executor/SKILL.md`
- `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md`
- `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md`
- `claude-code/skills/ywc-parallel-executor/scripts/resume-state.py`

### Owned Interface
- `hardener_verdict` value domain gains `"NEEDS_CONTEXT"` — downstream consumers (`yw-000038-030`) trust `die()` lists exactly the four sorted values.
- `resume-state.py`'s `status` output domain gains `"blocked"` / `"needs_context"` alongside `"valid"` / `"error"`.

### Shared Surfaces
- `.ywc-run-state.json` `waves[].hardener_verdict` schema and `resume-state.py`'s `status` domain — the codex root (`yw-000038-020`) independently implements the same value domain; no direct file overlap, but behavior must match in effect per AC8.

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 claude-code/skills/scripts/update-state.py hardener-verdict 1 NEEDS_CONTEXT` against a fixture state with wave `1` present — confirm exit 0 and `waves[].hardener_verdict == "NEEDS_CONTEXT"`.
- `python3 claude-code/skills/scripts/update-state.py hardener-verdict 1 BOGUS` — confirm non-zero exit and `die()` message `verdict must be one of ['BLOCKED', 'NEEDS_CONTEXT', 'PASS', 'absent'], got 'BOGUS'`.
- Hand-construct a state file with an `in_progress` wave, `pending: []`, `hardener_verdict: "NEEDS_CONTEXT"` — `python3 claude-code/skills/ywc-parallel-executor/scripts/resume-state.py --json` prints `status: "needs_context"` (not `"valid"`); repeat with `hardener_verdict: "BLOCKED"` → `status: "blocked"`; repeat with `hardener_verdict` absent/`"PASS"` → `status: "valid"` (regression).
- `grep -n "NEEDS_CONTEXT" claude-code/skills/ywc-parallel-executor/SKILL.md` — confirms the Step 4e.5 checkpoint instruction, Step 4e.6 promotion condition, Step 4g exclusion, and Step 4i bucket all mention it (AC3, AC9).
- `grep -n "NEEDS_CONTEXT" claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md` — confirms case 4 and the State File Format description mention it (AC7).
- `bash scripts/validate.sh`
