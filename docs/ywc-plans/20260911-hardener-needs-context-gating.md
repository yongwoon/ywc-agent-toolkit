# Hardener NEEDS_CONTEXT Gating for Wave Promotion and Resume

> Status: Draft
> Scale: Medium
> Created: 2026-09-11
> Author: yongwoon.kim (via ywc-plan)
> Spec Reference: GitHub issue #188 (follow-up to PR #186 / `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md` and `docs/ywc-plans/20260911-wave-int-checkpoint-ownership.md`)

## Global Constraints

- Code (variables, functions, comments) in English; this repo's skill-body language policy applies — `claude-code/skills/CLAUDE.md` §Writing Rules (README-only Korean/locale prose, all other files English).
- Python type annotations on function signatures, PEP 8 (`~/.claude/rules/python/coding-style.md`).
- `claude-code/skills/` and `codex/skills/` are **not auto-synced** — every change lands in both roots deliberately, by hand (`claude-code/skills/CLAUDE.md` §"Codex-skill: Maintained Independently").
- Bot-polling, PR-conflict, HTML-output, and schema-guide canonical procedures must be referenced, never re-inlined, in `SKILL.md` bodies (`claude-code/skills/CLAUDE.md`).
- Regression tests use no external framework (bash + `assert_eq`/`assert_contains` harness), matching `scripts/test-wave-int-checkpoint-ownership.sh`'s established pattern for this exact subsystem.

## Purpose

PR #186 introduced `wave-int/<N>` integration branches and gates promotion into the base branch on the Wave-boundary Hardener's verdict. The `hardener_verdict` checkpoint field (`.ywc-run-state.json`) and its `update-state.py hardener-verdict` CLI currently accept only `absent`, `PASS`, and `BLOCKED`. But Hardener (and Cleaner) dispatches are documented to return `NEEDS_CONTEXT` when a required `Baseline` artifact is absent or corrupt (`claude-code/skills/references/quality-gates.md:93`). Because `NEEDS_CONTEXT` has no home in the checkpoint contract, a wave whose Hardener dispatch returns it can still promote to base and stamp `wave-complete` — the promotion gate the whole isolation-branch mechanism exists to enforce collapses for this one outcome. Resume validation has the same blind spot: it never inspects `hardener_verdict` at all, so a fully-merged-not-promoted wave resumes as `valid` regardless of whether Hardener already returned `BLOCKED` or `NEEDS_CONTEXT`.

## Scope

- Add `NEEDS_CONTEXT` to the `hardener_verdict` checkpoint contract (`VALID_HARDENER_VERDICTS`) in both skill roots' `update-state.py`.
- Extend the Step 4e.5 checkpoint-write instruction and Step 4e.6 promotion gate in both roots' `SKILL.md` so an `enforced`-tier `NEEDS_CONTEXT` blocks promotion and `wave-complete` exactly like `BLOCKED`.
- Extend both roots' `references/wave-integration-branch.md` promotion section and Step 4i terminal-state bucket so `NEEDS_CONTEXT` is preserved (integration branch + task worktrees kept, Step 4g cleanup skipped) the same way `BLOCKED` is today.
- Extend both roots' `references/checkpoint-resume.md` fully-merged-not-promoted resume case so `hardener_verdict == NEEDS_CONTEXT` is a distinct, documented resume case with its own recovery path (provide context, then auto-rerun Hardener — no user confirmation required, unlike `BLOCKED`).
- Extend `resume-state.py` (both roots) to inspect the in-progress wave's `hardener_verdict` when `pending` is empty, and return a non-`"valid"` status (`"blocked"` / `"needs_context"`) instead of unconditionally reporting `"valid"`.
- Extend `scripts/test-wave-int-checkpoint-ownership.sh` with regression cases covering the new value end to end: CLI validation reuses the existing `ROOTS` array/loop, but `resume-state.py` coverage requires a **second**, parallel `RESUME_STATE_ROOTS`-style array and loop (see Existing Constraints Touched — `resume-state.py` is a structurally different script at a different path, not already covered by the existing `ROOTS` loop). Promotion-gate documentation presence is out of test-script scope (see Non-Functional Requirements) — the state-transition behavior is in scope.

## Out of Scope

- Hardener's own decision logic for *when* it emits `NEEDS_CONTEXT` (that is `ywc-qa-engineer`'s and `quality-gates.md`'s existing behavior — unchanged).
- `promotion_retry_count` / `PROMOTION_RETRY_CAP` mechanics — unchanged; `NEEDS_CONTEXT` does not consume a promotion-retry attempt, since no promotion attempt is made while it is outstanding.
- Non-contract-bearing waves (`integration_branch` is `None`) — unaffected, as today.
- Any `hardener_verdict` value other than `NEEDS_CONTEXT` — `absent`, `PASS`, `BLOCKED` semantics are unchanged.
- `--per-task-pr` mode — the Hardener dispatch is already reporting-only there and never assigned to `gate_state`/`hardener_verdict`; no change.
- Both `subagent-status-actions.md` files (`codex/skills/references/subagent-status-actions.md` and `codex/skills/ywc-sequential-executor/references/subagent-status-actions.md`) — they govern per-subagent dispatch reply handling (`NEEDS_CONTEXT` → "provide context, re-dispatch the same subagent"), not the wave-boundary checkpoint field this spec extends. FR-4 cites the *convention* they document as a naming precedent only; no edit to either file is required.
- The `gate_state` sentinel vocabulary in `quality-gates.md` §9 (Completion-Report-only, never written to `.ywc-run-state.json` per `SKILL.md:355`) — the issue's ask is scoped to `hardener_verdict`, not `gate_state`; adding a `gate_state` sentinel for this case is a separate, non-required change.
- Codex root's wave-boundary aggregation precedence rule (`BLOCKED > NEEDS_CONTEXT > DONE_WITH_CONCERNS > DONE`, `codex/skills/ywc-parallel-executor/SKILL.md:367`) — already correctly ranks `NEEDS_CONTEXT`; only the downstream checkpoint-write and promotion-gate steps that discard this ranking are in scope.
- Reconciling codex `checkpoint-resume.md`'s `--resume-disposition`-driven non-interactive-prompt design (`:13`, `:22-25`) with its own case-3 "requires explicit user confirmation" wording (`:85`) — a pre-existing tension in that document, not introduced by this spec. The new case-4 wording (FR-4) mirrors case 3's existing convention rather than resolving it.

## Existing Constraints Touched

| Existing artifact | Behavior (verified by reading the file) | New code's interaction |
|---|---|---|
| `claude-code/skills/scripts/update-state.py:210` | `VALID_HARDENER_VERDICTS = {"absent", "PASS", "BLOCKED"}` — `cmd_hardener_verdict` (`:213-221`) rejects any other value via `die()`. | Extend the set to include `"NEEDS_CONTEXT"`; no change to the reject/`die()` behavior for genuinely invalid values. |
| `codex/skills/scripts/update-state.py:210-221` | Byte-identical to the claude-code file for this range (verified `diff`). | Same edit, applied independently (no auto-sync). |
| `claude-code/skills/ywc-parallel-executor/SKILL.md:357` | Checkpoint instruction: `hardener-verdict <N> <absent\|PASS\|BLOCKED>` — `absent` no contract, `PASS` ran without enforced `BLOCKED` (dispatch failure counts as `PASS`), `BLOCKED` only on enforced-tier `BLOCKED`. | Add a fourth branch: `NEEDS_CONTEXT` when Hardener ran under an `enforced` contract and returned `NEEDS_CONTEXT` (per `quality-gates.md:93`, e.g. missing/corrupt `Baseline`). Dispatch-failure-as-`PASS` mapping is unchanged — `NEEDS_CONTEXT` is a successful dispatch whose *verdict* needs context, distinct from a *dispatch* failure. |
| `claude-code/skills/ywc-parallel-executor/SKILL.md:369` | Promotion gate: "promote it into base only on a non-blocking Hardener verdict (`absent`, `PASS`, or a dispatch failure — never on `BLOCKED`)". | Change "never on `BLOCKED`" to "never on `BLOCKED` or `NEEDS_CONTEXT`". |
| `codex/skills/ywc-parallel-executor/SKILL.md:367` | Wave-boundary aggregation already computes `NEEDS_CONTEXT` as a ranked outcome (`BLOCKED > NEEDS_CONTEXT > DONE_WITH_CONCERNS > DONE`) but the same line's checkpoint call still only accepts `<absent\|PASS\|BLOCKED>`, silently discarding the `NEEDS_CONTEXT` rank at the checkpoint-write step. | Checkpoint call gains the `NEEDS_CONTEXT` value; the aggregation's existing precedence computation is unchanged (it already produces the right in-memory outcome — only the write-through was lossy). |
| `codex/skills/ywc-parallel-executor/references/wave-integration-branch.md` (Promotion section, "step `4e.6`") | "promote it into the base branch only when the aggregate outcome under an `enforced` contract is not `BLOCKED`". | Change "is not `BLOCKED`" to "is neither `BLOCKED` nor `NEEDS_CONTEXT`". |
| `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md:101` | "On a blocking Hardener verdict ... base is left untouched, `wave-complete` is not stamped, the integration branch is preserved, and Step 4g cleanup is skipped for every task in the wave". | Same preservation behavior extends to a blocking-by-`NEEDS_CONTEXT` outcome — reworded to cover both values under one label ("blocking verdict"). |
| `claude-code/skills/ywc-parallel-executor/SKILL.md:373` and `:410`; `codex/skills/ywc-parallel-executor/SKILL.md:372` and `:415` | Step 4g cleanup exclusion and Step 4i third-bucket definition both key off `hardener_verdict == "BLOCKED"` specifically (`Hardener-BLOCKED` label). | Extend the exclusion/bucket condition to `hardener_verdict in {"BLOCKED", "NEEDS_CONTEXT"}`. Keep the existing `Hardener-BLOCKED` label for the `BLOCKED` case; introduce a parallel `Hardener-NEEDS_CONTEXT` label for the new case so Completion Report / terminal-state audit text can distinguish "unresolved gate failure, needs a decision" from "needs more input, needs a rerun". |
| `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md:101-102` (cases 2 and 3 of "Resume with `wave-int/<N>`") | Case 2: `absent`/`PASS` → auto-retry, no prompt. Case 3: `BLOCKED` → stop, print findings, require explicit user confirmation before re-running Hardener. | Add case 4: `NEEDS_CONTEXT` → stop, print the missing-context detail, and require the *context to be supplied* (not a bare confirmation) before re-running Hardener — matching the general `NEEDS_CONTEXT` handling convention already defined for per-task subagents at `SKILL.md:220` ("provide the missing context and re-dispatch the same subagent at the same model class"), applied here at the wave-boundary checkpoint layer. |
| `claude-code/skills/ywc-parallel-executor/scripts/resume-state.py:104-134` | `in_progress` branch (status `"in_progress"`, found first) sets `resume_wave`/`pending`/`merged_in_wave` from the wave and always proceeds to the unconditional `result = {"status": "valid", ...}` at `:145-153` — the wave's `hardener_verdict` field is never read anywhere in the file. A fully-merged-not-promoted wave (`pending == []`, `status == "in_progress"`) currently returns `status: valid` regardless of `hardener_verdict`. | After computing `pending`/`merged_in_wave` for the `in_progress` wave, when `pending` is empty, read `wave.get("hardener_verdict")`. If it is `"BLOCKED"` or `"NEEDS_CONTEXT"`, short-circuit to a non-`"valid"` result (`status: "blocked"` / `status: "needs_context"`) carrying the wave's `reason`/`blocked_detail` fields, instead of falling through to the unconditional `"valid"` result. |
| `codex/skills/ywc-parallel-executor/scripts/resume-state.py` | Same `in_progress`/`pending`/unconditional-`"valid"` structure as the claude-code file (diff shows only unrelated `worktree_root` additions in this range). | Same edit, applied independently. |
| `claude-code/skills/ywc-parallel-executor/references/aggregate-pr.md:46` | References `checkpoint-resume.md`'s `hardener_verdict` branching generically ("the user must resolve promotion... before the aggregate/draft branch can be safely carved") — a generic pointer, not an enumeration of the value set. | No wording change needed — the reference stays correct once a fourth (`NEEDS_CONTEXT`) value exists, since it never enumerates the value set itself. |
| `scripts/test-wave-int-checkpoint-ownership.sh:1-19` | Existing harness: `assert_eq`/`assert_contains`, `ROOTS` array hardwired to one script name (`update-state.py`) at two root-relative paths of identical shape, disposable temp-git-repo fixtures, no external framework. | Reuse the `assert_eq`/`assert_contains` helpers and the same file (DRY; no new script). `update-state.py hardener-verdict` coverage (AC1, AC2) adds assertion blocks inside the **existing** `ROOTS` loop. `resume-state.py` coverage (AC5, AC6) cannot reuse that loop as-is — `resume-state.py` lives at a structurally different path (`<root>/ywc-parallel-executor/scripts/resume-state.py`, not `<root>/scripts/update-state.py`) and is a different script — so add a **second**, parallel `RESUME_STATE_ROOTS` array (`claude-code/skills/ywc-parallel-executor/scripts/resume-state.py`, `codex/skills/ywc-parallel-executor/scripts/resume-state.py`) and a second per-root loop, with its own fixture: a hand-constructed state file with an in-progress wave, empty `pending`, and `hardener_verdict` set to `BLOCKED` or `NEEDS_CONTEXT`. |

## Acceptance Criteria

Test seam: `update-state.py hardener-verdict` / `resume-state.py` CLI boundary (state-file mutation and read-back), exercised against a disposable temp git repo — the same seam `scripts/test-wave-int-checkpoint-ownership.sh` already tests.

- [ ] **AC1 — `NEEDS_CONTEXT` accepted by the checkpoint CLI**: When `update-state.py hardener-verdict <N> NEEDS_CONTEXT` is run against a valid parallel-executor state with wave `<N>` present, system writes `hardener_verdict: "NEEDS_CONTEXT"` to the wave entry, observable as exit code `0` and `.ywc-run-state.json`'s `waves[].hardener_verdict` equal to `"NEEDS_CONTEXT"`. Verified against both `claude-code/skills/scripts/update-state.py` and `codex/skills/scripts/update-state.py`.
- [ ] **AC2 — Invalid verdict still rejected**: When `update-state.py hardener-verdict <N> <anything-other-than-absent|PASS|BLOCKED|NEEDS_CONTEXT>` is run, system rejects it, observable as a non-zero exit code and a `die()` message listing all four valid values (`BLOCKED`, `NEEDS_CONTEXT`, `PASS`, `absent` — `sorted()` order, matching the API Contract's `die()` message exactly).
- [ ] **AC3 — Promotion blocked on `NEEDS_CONTEXT`**: For a contract-bearing wave under `--local-merge`/`--draft`/`--aggregate-pr` whose `hardener_verdict` is `NEEDS_CONTEXT`, `SKILL.md`'s promotion instruction (4e.6, both roots) explicitly excludes `NEEDS_CONTEXT` from the "promote" condition — verified by a text-presence check against both roots' `SKILL.md` and `wave-integration-branch.md` (the executor itself is an LLM-followed procedure, not a script, so this AC is a documentation-text assertion, not a runtime assertion — see Non-Functional Requirements).
- [ ] **AC4 — `wave-complete` not stamped while `NEEDS_CONTEXT`**: When `update-state.py wave-complete <N>` is attempted for a wave whose `pending` is empty but whose promotion never ran (simulating the `NEEDS_CONTEXT`-blocked state), the existing "refuses while any task is pending" guard is insufficient by itself (pending is empty) — verify instead that the documented procedure (4e.6) never issues `wave-complete` until after a successful promotion, and that `hardener_verdict == NEEDS_CONTEXT` is one of the states the resume validator (AC5) refuses to call `valid`, which is what actually prevents the wave from silently reaching `completed` on a later resume. Note: `wave-integration-branch.md`'s promotion section cites this guard as `update-state.py:162-163`; the guard has since moved to `:173-174` (`cmd_wave_complete`) — a pre-existing stale citation outside this spec's own table, flagged here for implementer awareness, no fix required as part of this spec.
- [ ] **AC5 — Resume validator refuses `valid` for fully-merged-not-promoted + `BLOCKED`/`NEEDS_CONTEXT`**: When `resume-state.py` (both roots) is run against a state file whose in-progress wave has `pending: []` and `hardener_verdict` equal to `"BLOCKED"` or `"NEEDS_CONTEXT"`, system returns a non-`"valid"` `status` (`"blocked"` for `BLOCKED`, `"needs_context"` for `NEEDS_CONTEXT`) in both text and `--json` output, observable as the printed/JSON `status` field never equal to `"valid"` for these two hand-constructed fixtures.
- [ ] **AC6 — Resume validator still returns `valid` for the unaffected cases**: When `resume-state.py` is run against (a) a fully-merged-not-promoted wave with `hardener_verdict` absent or `"PASS"`, or (b) a genuinely in-progress wave with non-empty `pending`, system returns `status: "valid"` exactly as before — this is a non-regression check against the resume-state.py behavior AC5 changes.
- [ ] **AC7 — Resume guidance text distinguishes `BLOCKED` from `NEEDS_CONTEXT`**: `checkpoint-resume.md` (both roots) documents case 4 (`NEEDS_CONTEXT`) as requiring the missing context to be supplied before an unprompted Hardener rerun, distinct from case 3 (`BLOCKED`)'s explicit user-confirmation requirement — verified by a text-presence check against both roots' `checkpoint-resume.md`.
- [ ] **AC8 — Cross-root consistency**: `VALID_HARDENER_VERDICTS`, the promotion-gate wording, the Step 4g/4i exclusion condition, and the resume-validator status values are identical in effect (not necessarily byte-identical prose, given the two roots' pre-existing documentation-style divergence) between `claude-code/skills/` and `codex/skills/` — verified by running the extended `scripts/test-wave-int-checkpoint-ownership.sh` against both `--root` targets and confirming equal pass counts for the new assertion groups.
- [ ] **AC9 — Step 4g/4i documentation actually updated**: `SKILL.md` (both roots) Step 4g's cleanup-exclusion wording and Step 4i's terminal-state bucket wording each explicitly include `NEEDS_CONTEXT` alongside `BLOCKED` in their exclusion/classification condition, observable as a text-presence check (grep) against both roots' `SKILL.md` finding the updated wording at Step 4g and Step 4i — mirroring AC3's and AC7's text-presence-check approach for their respective documentation deltas.

## Functional Requirements

### FR-1: Extend the `hardener_verdict` checkpoint contract

`VALID_HARDENER_VERDICTS` in both roots' `update-state.py` becomes `{"absent", "PASS", "BLOCKED", "NEEDS_CONTEXT"}`. `cmd_hardener_verdict` requires no other change — its `die()` message already lists `sorted(VALID_HARDENER_VERDICTS)`, which will include the new value automatically. State-file schema documentation (`checkpoint-resume.md`'s `### State File Format` JSON example, both roots) updates its `hardener_verdict` comment/enum description to name all four values.

### FR-2: Block promotion and `wave-complete` on `NEEDS_CONTEXT`

Step 4e.5's checkpoint-write instruction (`SKILL.md`, both roots) adds the `NEEDS_CONTEXT` branch: written when Hardener ran under an `enforced` contract and returned `NEEDS_CONTEXT` (as opposed to a dispatch failure, which is still mapped to `PASS` per the existing no-block rule). Step 4e.6's promotion condition (`SKILL.md` + `wave-integration-branch.md`, both roots) excludes `NEEDS_CONTEXT` from the set of verdicts that permit `git merge --ff-only` into base — base is left untouched, `wave-complete` is not stamped, exactly as the existing `BLOCKED` path. The `wave-integration-branch.md` "On a blocking Hardener verdict" / "On a blocking outcome" paragraph (both roots) is reworded to cover both `BLOCKED` and `NEEDS_CONTEXT` under one "blocking verdict" umbrella, preserving the integration branch and every task worktree in both cases.

Note for the codex root specifically: codex's wave-boundary aggregation already computes a wider **outcome** vocabulary (`BLOCKED > NEEDS_CONTEXT > DONE_WITH_CONCERNS > DONE`, `codex/skills/ywc-parallel-executor/SKILL.md:367`) than the `hardener_verdict` checkpoint field it writes through to (`absent`/`PASS`/`BLOCKED`/`NEEDS_CONTEXT`). These are related-but-distinct concepts — `outcome` is the in-memory aggregation result, `hardener_verdict` is its lossy write-through to `.ywc-run-state.json` — and this FR only fixes the write-through's value domain; it does not change codex's aggregation logic itself.

### FR-3: Extend Step 4g cleanup exclusion and Step 4i terminal-state bucket

The Step 4g cleanup loop condition ("whose wave is not `Hardener-BLOCKED`") extends to also exclude a wave whose `hardener_verdict` is `NEEDS_CONTEXT` — introduce the label `Hardener-NEEDS_CONTEXT` (or a combined "Hardener-blocking" label covering both — implementer's choice, but the two must remain textually distinguishable in the Completion Report so a human resuming later knows whether to supply context or make a BLOCKED-recovery decision). The Step 4i third-bucket definition (both roots) extends its classification condition from `hardener_verdict == "BLOCKED"` to `hardener_verdict in {"BLOCKED", "NEEDS_CONTEXT"}`.

### FR-4: Resume validation refuses `valid` for `BLOCKED`/`NEEDS_CONTEXT`

`checkpoint-resume.md`'s "Resume with `wave-int/<N>`" section (both roots) gains a fourth numbered case, inserted after today's case 3 (`BLOCKED`):

> 4. **Fully-merged-not-promoted, `hardener_verdict == NEEDS_CONTEXT`** (`pending` empty, `status != completed`) — Hardener could not render a verdict for lack of required context (e.g. missing/corrupt `Baseline`). Resume **stops and prints the recorded missing-context detail**, then requires the context to be supplied (not a bare go-ahead) before re-running Hardener — matching the general `NEEDS_CONTEXT` handling convention for subagent returns (`SKILL.md`'s "provide the missing context and re-dispatch... at the same model class"), applied here at the wave-boundary checkpoint layer rather than per-task.

For the **codex root** specifically, case 4's wording mirrors case 3's existing phrasing convention ("requires explicit user confirmation before re-running the gate", `codex/.../checkpoint-resume.md:85`) rather than the file's own `--resume-disposition`-driven non-interactive-prompt framing (`:13`, `:22-25`) — codex's case 3 already carries this same tension pre-existing this spec, and reconciling it is out of scope here (see Out of Scope).

`resume-state.py` (both roots) implements the machine-checkable half of this: when the in-progress wave's `pending` is empty, inspect `wave.get("hardener_verdict")`. `None`/`"absent"`/`"PASS"` → unchanged behavior (falls through to today's unconditional `"valid"` result). `"BLOCKED"` → `status: "blocked"`, carrying `wave.get("reason")` and `wave.get("blocked_detail")` into the result payload. `"NEEDS_CONTEXT"` → `status: "needs_context"`, carrying the same `reason`/`blocked_detail` fields (Hardener's missing-context detail is expected to be recorded there by the same `wave-int-blocked`-style write path Step 4e.5 already uses for `BLOCKED`, or a new equivalently-shaped write — implementer's choice, but the detail must be readable by `resume-state.py` without re-dispatching anything). Both new statuses keep the same top-level shape as today's `"valid"` result (`resume_wave`, `mode`, `tasks_dir` present) so callers that only branch on `status` degrade gracefully.

## Quality Gate Contract

N/A — no quality gate contract (this toolkit's own skill-and-script source is not itself a task carrying a declared `quality_gate_contract`; it is edited directly, matching the precedent set by the prior `wave-int-checkpoint-ownership` implementation).

## Module Boundaries

N/A — this change extends an existing CLI contract (`update-state.py` subcommand) and existing documentation files; it introduces no new module or public interface.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Consistency | `hardener_verdict` semantics, promotion-gate behavior, and resume-`status` values must be equivalent in claude-code and codex roots even where prose diverges (per the roots' pre-existing independent-maintenance convention) — verified by AC8. |
| Testability | `SKILL.md`/`wave-integration-branch.md`/`checkpoint-resume.md` are LLM-followed procedure documents, not executable code — AC3 and AC7 are necessarily text-presence assertions (grep for the updated wording), not behavioral test runs. Only `update-state.py` and `resume-state.py` changes get true state-transition regression coverage (AC1, AC2, AC5, AC6). |
| Backward compatibility | A pre-existing `.ywc-run-state.json` with no `hardener_verdict` field, or `hardener_verdict` in `{None, "absent", "PASS", "BLOCKED"}`, must behave exactly as before this change — `resume-state.py`'s new branch only activates on the literal string `"NEEDS_CONTEXT"`. |
| Reliability | `resume-state.py`'s new `"blocked"`/`"needs_context"` statuses must never regress the `pending`-non-empty (case 1, partial-merge) or `hardener_verdict` absent/`PASS` (case 2) resume paths — AC6 is the regression guard. |

## Critical Surfaces

N/A — no critical surface (state-file/CLI contract for an internal developer-tooling checkpoint mechanism; no auth, payment, PII, or secret handling).

## Data Model

`.ywc-run-state.json`'s existing `waves[].hardener_verdict` field (documented in `checkpoint-resume.md`'s `### State File Format`) gains one additional valid string value. No new field, no new file, no migration.

| Field | Type | Existing valid values | New valid value |
|---|---|---|---|
| `waves[].hardener_verdict` | string, optional (absent until Step 4e.5 first writes it) | `"absent"`, `"PASS"`, `"BLOCKED"` | `"NEEDS_CONTEXT"` |

### Migration Notes

N/A — no schema migration. The field is JSON-schema-free (read via `dict.get()`); an existing state file with no `hardener_verdict` key, or one already carrying one of the three prior values, requires no transformation. `resume-state.py`'s new branch is additive (only triggers on the new literal), so it is safe to deploy against in-flight runs created before this change.

## API Contract

The only "API" this spec changes is the `update-state.py hardener-verdict` CLI subcommand's accepted argument domain, and `resume-state.py`'s output `status` field domain.

### `update-state.py hardener-verdict <N> <verdict>`

**Before:** `<verdict>` ∈ `{absent, PASS, BLOCKED}`.
**After:** `<verdict>` ∈ `{absent, PASS, BLOCKED, NEEDS_CONTEXT}`.

**Errors:**

| Condition | Behavior |
|---|---|
| `<verdict>` not in the valid set | `die()` with message `verdict must be one of ['BLOCKED', 'NEEDS_CONTEXT', 'PASS', 'absent'], got '<value>'` (sorted order) — unchanged mechanism, updated message content. |
| State has no `run_id` / wrong executor / wave not found | Unchanged existing error paths (`require_executor`, `find_wave`) — not touched by this spec. |

### `resume-state.py [--json]`

**Before (fully-merged-not-promoted wave, any `hardener_verdict`):** always `status: "valid"`.

**After:**

| `hardener_verdict` of the in-progress wave (when `pending` is empty) | `status` |
|---|---|
| absent / `None` / `"absent"` / `"PASS"` | `"valid"` (unchanged) |
| `"BLOCKED"` | `"blocked"` |
| `"NEEDS_CONTEXT"` | `"needs_context"` |

**New non-`"valid"` result shape (JSON mode):**

```json
{
  "status": "blocked",
  "resume_wave": 2,
  "mode": "local-merge",
  "tasks_dir": "tasks/",
  "reason": "example-reason-string",
  "blocked_detail": "example-detail-string"
}
```

Text mode prints the equivalent as a `CANNOT RESUME` block naming the wave, the verdict, and the recorded reason/detail — following the existing `fail()` helper's shape, but this is a *non-error* stop (exit code choice is an implementation decision the task should make explicitly: either reuse `fail()`'s exit 1, or a distinct exit code — either is acceptable as long as it is not exit 0 conflated with today's `"valid"` success path).

## Edge Cases

- **`hardener_verdict` is `NEEDS_CONTEXT` but `pending` is non-empty** (a wave interrupted mid-merge, before Hardener even ran): `resume-state.py`'s existing partial-merge case (case 1, non-empty `pending`) takes precedence — the new `hardener_verdict` check only applies once `pending` is empty, matching `checkpoint-resume.md`'s existing case-ordering ("Only once `pending` is empty does the wave enter case 2 or 3 below").
- **A wave transitions from `NEEDS_CONTEXT` to `BLOCKED` or `PASS` on a Hardener rerun**: the checkpoint call simply overwrites `hardener_verdict` (existing `cmd_hardener_verdict` behavior, unchanged) — no special transition logic needed; `resume-state.py` always reads the current value.
- **A pre-this-change state file has `hardener_verdict: "NEEDS_CONTEXT"` written by some out-of-band process** (shouldn't happen today since no code path writes it, but the field is free-text via `dict.get()`): `update-state.py`'s new validation accepts it going forward; `resume-state.py`'s new branch handles it correctly regardless of when it was written.
- **`reason`/`blocked_detail` absent even though `hardener_verdict` is `NEEDS_CONTEXT`** (e.g. a manually-edited state file, or a future write path that doesn't populate them): `resume-state.py` must not crash — use `.get()` with `None`/absent-key fallback, omit the key from JSON output rather than emitting `null`, matching the existing `blocked_detail` omission convention documented in `checkpoint-resume.md:77`.
- **`--per-task-pr` wave with `hardener_verdict` somehow set**: cannot occur under the existing carve-out (never written to `.ywc-run-state.json` for that mode) — no new handling needed, out of scope per this spec's Scope section.

## Dependencies

N/A — no external dependencies; extends existing in-repo Python scripts and Markdown documentation only.

## Open Questions

- [ ] Should the Completion Report / Step 4i terminal-state label be a single combined `Hardener-blocking` bucket, or two distinct labels (`Hardener-BLOCKED` / `Hardener-NEEDS_CONTEXT`)? FR-3 leaves this to the implementer since either satisfies the acceptance criteria (AC3/AC7 only require the *recovery guidance* to distinguish the two cases, not necessarily the bucket label) — resolve during task decomposition if `ywc-task-generator` needs a single canonical term for task Ownership/README text.
- [ ] Exact exit code for `resume-state.py`'s new `"blocked"`/`"needs_context"` non-`"valid"`, non-error statuses (reuse `fail()`'s exit 1, or introduce a distinct exit code) — either satisfies AC5's observable ("status field never equal to valid"); left to the implementing task since no existing caller branches on `resume-state.py`'s exit code today (only its `status` field, per `checkpoint-resume.md`'s "Manual Inspection" usage).

## References

- GitHub issue #188 — https://github.com/yongwoon/ywc-agent-toolkit/issues/188
- PR #186 — https://github.com/yongwoon/ywc-agent-toolkit/pull/186 (original `wave-int/<N>` isolation + promotion gate)
- `docs/ywc-plans/20260910-parallel-executor-hardener-delivery-isolation.md` — parent spec for the `wave-int/<N>` mechanism this issue amends
- `docs/ywc-plans/20260911-wave-int-checkpoint-ownership.md` — immediately prior follow-up (issue #187), same subsystem, same dual-root pattern, same regression-test script

## Amendment Log

### Iteration 1 — 2026-09-11

**Driven by**: DONE_WITH_CONCERNS, 1 Critical / 2 Warning / 4 Suggestion findings (Phase 1 4-dimension review; no Phase 2 advisor escalation used — the one candidate finding was resolved directly by reading the cited file, see note below)
**Signatures**: `consistency:ac2-sorted-order-contradicts-api-contract`, `consistency:fr3-orphan-ac-for-step4g-4i-doc-delta`, `feasibility:test-harness-resume-state-py-not-covered-by-existing-loop`, `completeness:aggregate-pr-and-subagent-status-actions-out-of-scope`, `consistency:fr2-outcome-vs-hardener-verdict-terminology`, `code-compat:fr4-codex-case4-mirrors-case3-not-resume-disposition`, `code-compat:ac4-stale-line-citation-note`

> Code Compatibility's one advisor-candidate finding (codex `checkpoint-resume.md`'s `--resume-disposition` non-interactive design vs. case 3's "requires user confirmation" wording) was resolved without an Opus escalation: reading `codex/.../checkpoint-resume.md` directly confirmed this tension already exists in case 3 today, pre-dating this spec — the fix is for FR-4's new case 4 to mirror case 3's existing convention, not to reconcile it, which the edit below and the corresponding Out of Scope bullet now state explicitly.

| Section edited | What changed | Why |
|---|---|---|
| `## Acceptance Criteria` (AC2) | Fixed the `sorted()` ordering example in AC2's parenthetical from `absent, BLOCKED, NEEDS_CONTEXT, PASS` to `BLOCKED, NEEDS_CONTEXT, PASS, absent` | AC2 contradicted the API Contract's correct ASCII-sorted ordering at (then) line 138 — Consistency Critical |
| `## Acceptance Criteria` (new AC9) | Added AC9: text-presence check that Step 4g/4i documentation in both roots' `SKILL.md` actually includes `NEEDS_CONTEXT` | FR-3's doc delta had no dedicated AC, unlike FR-2 (AC3) and FR-4 (AC7) — Consistency Warning |
| `## Scope` | Reworded the test-harness bullet to state `resume-state.py` needs a second, parallel harness loop, not reuse of the existing `ROOTS` loop | Scope implied one shared loop already covers both scripts — Feasibility Warning |
| `## Existing Constraints Touched` (harness row) | Reworded to specify a second `RESUME_STATE_ROOTS` array + loop + fixture shape for `resume-state.py` coverage | Same Feasibility Warning — harness row made the same incorrect implication |
| `## Existing Constraints Touched` (new row) | Added `aggregate-pr.md:46` row confirming no wording change needed there | Completeness Suggestion — cross-reference was unaudited |
| `## Out of Scope` | Added a bullet excluding both `subagent-status-actions.md` files | Completeness Suggestion — scope of FR-4's convention citation was ambiguous |
| `## Functional Requirements` (FR-2) | Added a note distinguishing codex's `outcome` vocabulary from the `hardener_verdict` checkpoint field | Consistency Suggestion — risk of conflating the two |
| `## Functional Requirements` (FR-4) | Added a note that codex's case-4 wording mirrors case 3's existing convention rather than resolving `--resume-disposition` | Code Compatibility advisor-candidate, resolved directly (see note above) |
| `## Out of Scope` | Added a bullet naming the pre-existing `--resume-disposition` vs. case-3-wording tension as out of scope | Same Code Compatibility item |
| `## Acceptance Criteria` (AC4) | Added a note flagging `wave-integration-branch.md:82`'s stale `update-state.py:162-163` citation (now `:173-174`) | Code Compatibility Suggestion — pre-existing staleness AC4's implementer would otherwise follow uncorrected |
