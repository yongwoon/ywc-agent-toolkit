# yw-000038-020-domain-hardener-needs-context-gating-codex

## Purpose
Same promotion-gate gap as `yw-000038-010`, applied independently to the codex root: `hardener_verdict` has no `NEEDS_CONTEXT` value, so a wave whose Hardener dispatch returns it can promote to base. Codex's wave-boundary aggregation already ranks `NEEDS_CONTEXT` in its precedence (`BLOCKED > NEEDS_CONTEXT > DONE_WITH_CONCERNS > DONE`, `SKILL.md:367`) but the checkpoint write-through still only accepts `absent|PASS|BLOCKED`, discarding that rank. This task fixes the write-through and extends the promotion gate, Step 4g/4i logic, resume documentation, and `resume-state.py` — for the codex root, independently (no auto-sync between roots).

## Scope
- `codex/skills/scripts/update-state.py:210-221` — extend `VALID_HARDENER_VERDICTS` to include `"NEEDS_CONTEXT"` (byte-identical range to claude-code's file per spec's `## Existing Constraints Touched`) (FR-1).
- `codex/skills/ywc-parallel-executor/SKILL.md:367` — checkpoint call `hardener-verdict <N> <absent|PASS|BLOCKED>` gains `NEEDS_CONTEXT`; the existing precedence-computation prose is unchanged, only the write-through's accepted value domain (FR-2, per spec's explicit note distinguishing codex's `outcome` vocabulary from the `hardener_verdict` checkpoint field).
- `codex/skills/ywc-parallel-executor/SKILL.md:368` — promotion condition "is not an `enforced`-tier `BLOCKED`" → "is neither an `enforced`-tier `BLOCKED` nor `NEEDS_CONTEXT`" (FR-2).
- `codex/skills/ywc-parallel-executor/SKILL.md:372` and `:415` — Step 4g exclusion and Step 4i terminal bucket extend from `hardener_verdict == "BLOCKED"` to `hardener_verdict in {"BLOCKED", "NEEDS_CONTEXT"}`; introduce `Hardener-NEEDS_CONTEXT` alongside `Hardener-BLOCKED` (FR-3).
- `codex/skills/ywc-parallel-executor/references/wave-integration-branch.md` (Promotion section, step `4e.6`) — "is not `BLOCKED`" → "is neither `BLOCKED` nor `NEEDS_CONTEXT`" (FR-2).
- `codex/skills/ywc-parallel-executor/references/checkpoint-resume.md`:
  - State File Format `hardener_verdict` description gains the fourth value (FR-1).
  - `### Resume with wave-int/<N>` gains case 4 after today's case 3 (`:85`), mirroring case 3's existing "requires explicit user confirmation before re-running the gate" phrasing convention — not codex's own `--resume-disposition` non-interactive-prompt framing (`:13`, `:22-25`), which is a pre-existing tension this task does not reconcile (FR-4).
- `codex/skills/ywc-parallel-executor/scripts/resume-state.py:174-` (`in_progress` branch) — same `hardener_verdict` inspection added when `pending` is empty, short-circuiting to `status: "blocked"` / `"needs_context"` (FR-4).

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260911-hardener-needs-context-gating.md` — full spec; this task implements FR-1, FR-2, FR-3, FR-4 (codex half)
- `docs/ywc-plans/20260911-hardener-needs-context-gating.md#acceptance-criteria` — AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC9 (codex half of each; AC8 verified jointly by `yw-000038-030`)
- `docs/ywc-plans/20260911-hardener-needs-context-gating.md#functional-requirements` — FR-2's codex-specific note (`outcome` vs. `hardener_verdict`) and FR-4's codex-specific note (case-4 mirrors case-3 wording, does not resolve `--resume-disposition`)
- `codex/skills/scripts/update-state.py:210-221`
- `codex/skills/ywc-parallel-executor/SKILL.md:367,368,372,415`
- `codex/skills/ywc-parallel-executor/references/wave-integration-branch.md` (Promotion section, step 4e.6)
- `codex/skills/ywc-parallel-executor/references/checkpoint-resume.md:13,22-25,45-95` (State File Format, Resume with `wave-int/<N>`, `--resume-disposition` framing)
- `codex/skills/ywc-parallel-executor/scripts/resume-state.py:125-233` (`fail()`, `in_progress` branch, unconditional `"valid"` result)
- `yw-000038-010` (claude-code implementation) — same edit shape; consult it for the exact resume-state.py branch structure but do not copy its file paths.

### Summary
Codex's aggregation already computes `NEEDS_CONTEXT` as a ranked outcome — this FR only fixes the lossy checkpoint write-through, not the aggregation logic itself. Codex's `checkpoint-resume.md` case 3 already carries a pre-existing tension between its file-level `--resume-disposition` non-interactive-prompt design and case 3's own "requires explicit user confirmation" wording; this task's new case 4 mirrors case 3's existing convention rather than resolving that tension (explicitly out of scope, per spec).

### Out of Scope (from spec)
- The claude-code root's identical hand-edit — `yw-000038-010`.
- The regression test file exercising both roots — `yw-000038-030`.
- Reconciling codex `checkpoint-resume.md`'s `--resume-disposition`-driven design with case 3's "requires explicit user confirmation" wording — a pre-existing tension, not introduced by this task.
- Codex's wave-boundary aggregation precedence rule (`SKILL.md:367`, `BLOCKED > NEEDS_CONTEXT > DONE_WITH_CONCERNS > DONE`) itself — already correct; only the downstream checkpoint-write and promotion-gate steps are in scope.
- Hardener's own decision logic for *when* it emits `NEEDS_CONTEXT`, `promotion_retry_count` mechanics, non-contract-bearing waves, `--per-task-pr` mode, `subagent-status-actions.md`, `quality-gates.md` §9's `gate_state` vocabulary — all unchanged, per spec `## Out of Scope`.
- The plugin mirror at `plugins/ywc-agent-toolkit/skills/` auto-syncs via the repo's pre-commit hook when `codex/skills/` changes — do not hand-edit it; this task's own Task Verify confirms the sync output matches.

## Criticality
`normal` — internal orchestration state (`.ywc-run-state.json`, `.gitignore`d); no auth/payment/PII surface.

## Dependencies

### Depends On
- (None — root task, parallel-safe against `yw-000038-010` since the two touch disjoint files)

### Depended By
- `yw-000038-030-test-hardener-needs-context-gating-regression` — exercises this task's `update-state.py`/`resume-state.py` changes against the codex root.

## Key Files
- `codex/skills/scripts/update-state.py` — `VALID_HARDENER_VERDICTS` set literal.
- `codex/skills/ywc-parallel-executor/SKILL.md` — Step 4e.5 checkpoint call, Step 4e.6 promotion condition, Step 4g exclusion, Step 4i bucket.
- `codex/skills/ywc-parallel-executor/references/wave-integration-branch.md` — promotion section.
- `codex/skills/ywc-parallel-executor/references/checkpoint-resume.md` — State File Format description, Resume with `wave-int/<N>` case 4.
- `codex/skills/ywc-parallel-executor/scripts/resume-state.py` — new `hardener_verdict` inspection branch.
- `plugins/ywc-agent-toolkit/skills/` — auto-synced output only, verified not hand-edited.

## Notes
- Same label decision as `yw-000038-010`: `Hardener-BLOCKED` / `Hardener-NEEDS_CONTEXT` as two distinct labels.
- Same `resume-state.py` exit-code decision as `yw-000038-010`: new non-`"valid"` statuses use a sibling of `fail()` (not `fail()` itself, which is `status: "error"`), exit 1.
- Follow `~/.claude/rules/python/coding-style.md`: PEP 8, type annotations — matches this file's existing fully-typed style.
- Do not attempt to reconcile the `--resume-disposition` framing tension in `checkpoint-resume.md` — mirror case 3's existing wording convention for the new case 4, per spec FR-4's codex-specific note.

## Parallel Execution Metadata

### Ownership
- `codex/skills/scripts/update-state.py`
- `codex/skills/ywc-parallel-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/references/wave-integration-branch.md`
- `codex/skills/ywc-parallel-executor/references/checkpoint-resume.md`
- `codex/skills/ywc-parallel-executor/scripts/resume-state.py`

### Owned Interface
- `hardener_verdict` value domain gains `"NEEDS_CONTEXT"` (codex root) — downstream `yw-000038-030` trusts `die()` lists exactly the four sorted values.
- `resume-state.py`'s `status` output domain gains `"blocked"` / `"needs_context"` (codex root).

### Shared Surfaces
- `.ywc-run-state.json` schema and `resume-state.py` `status` domain — must match the claude-code root (`yw-000038-010`) in effect per AC8; no direct file overlap.

### Conflicts With
- (None identified)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `python3 codex/skills/scripts/update-state.py hardener-verdict 1 NEEDS_CONTEXT` against a fixture — exit 0, field written.
- `python3 codex/skills/scripts/update-state.py hardener-verdict 1 BOGUS` — non-zero exit, `die()` lists all 4 values sorted.
- Hand-built fixtures against `resume-state.py --json` — `needs_context` / `blocked` / `valid` / `valid` for `NEEDS_CONTEXT` / `BLOCKED` / absent / `PASS`.
- `diff <(python3 codex/skills/scripts/update-state.py --help) <(python3 claude-code/skills/scripts/update-state.py --help)` — subcommand list identical between roots (AC8 partial).
- `grep -n "NEEDS_CONTEXT" codex/skills/ywc-parallel-executor/SKILL.md` — matches at 4e.5, 4e.6, 4g, 4i (AC3, AC9).
- `grep -n "NEEDS_CONTEXT" codex/skills/ywc-parallel-executor/references/checkpoint-resume.md` — case 4 present (AC7).
- `bash scripts/sync-codex-plugin.sh && diff -r codex/skills/ywc-parallel-executor plugins/ywc-agent-toolkit/skills/ywc-parallel-executor` — exits 0, no residual diff.
- `bash scripts/validate.sh`
