# Task: yw-000038-010-domain-hardener-needs-context-gating-claude

## Prerequisites
- [ ] N/A — root task, no predecessor task required.

## Allowed Edit Scope
Only the five claude-code-root files listed in README.md `## Ownership`:
`claude-code/skills/scripts/update-state.py`, `claude-code/skills/ywc-parallel-executor/SKILL.md`,
`claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md`,
`claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md`,
`claude-code/skills/ywc-parallel-executor/scripts/resume-state.py`. Do not touch any codex-root file.

## Stop Conditions
- If `update-state.py:210`'s `VALID_HARDENER_VERDICTS` line or `cmd_hardener_verdict`'s `die()` message format has diverged from the spec's `## Existing Constraints Touched` description, stop and report — do not guess at the current shape.
- If `resume-state.py`'s `in_progress` branch structure (lines 104-153) has materially changed since the spec was written, stop and report rather than patching around an unfamiliar shape.
- If any of the four target `SKILL.md` line numbers (357, 369, 373, 410) no longer contain the described wording, re-locate by grepping for `hardener-verdict`, `never on \`BLOCKED\``, `Hardener-BLOCKED`, and report if the wording itself has changed beyond a line-number shift.

## Implementation Steps

- [ ] In `claude-code/skills/scripts/update-state.py`, change `VALID_HARDENER_VERDICTS = {"absent", "PASS", "BLOCKED"}` to `VALID_HARDENER_VERDICTS = {"absent", "PASS", "BLOCKED", "NEEDS_CONTEXT"}`. No other change to `cmd_hardener_verdict` — its `die()` message already derives from `sorted(VALID_HARDENER_VERDICTS)`.
- [ ] In `claude-code/skills/ywc-parallel-executor/SKILL.md` Step 4e.5's checkpoint-write instruction (`:357`), extend the `hardener-verdict <N> <absent|PASS|BLOCKED>` invocation and its explanatory clause to `<absent|PASS|BLOCKED|NEEDS_CONTEXT>`, adding: "`NEEDS_CONTEXT` when Hardener ran under an `enforced` contract and returned `NEEDS_CONTEXT` (per `quality-gates.md:93`) — distinct from a dispatch failure, which still maps to `PASS`."
- [ ] In the same file's Step 4e.6 promotion condition (`:369`), change "never on `BLOCKED`" to "never on `BLOCKED` or `NEEDS_CONTEXT`".
- [ ] In the same file's Step 4g cleanup-exclusion condition (`:373`), change the parenthetical `(i.e. the wave created no wave-int/<N>, or its hardener_verdict is not BLOCKED — check .ywc-run-state.json)` to `(i.e. the wave created no wave-int/<N>, or its hardener_verdict is not in {BLOCKED, NEEDS_CONTEXT} — check .ywc-run-state.json)`, and update the bold label from `Hardener-BLOCKED` to a form that distinguishes both cases in prose (e.g. "not in a blocking-verdict wave (`Hardener-BLOCKED` or `Hardener-NEEDS_CONTEXT`)").
- [ ] In the same file's Step 4i terminal-state bucket (`:410`), extend the classification condition from `hardener_verdict == "BLOCKED"` to `hardener_verdict in {"BLOCKED", "NEEDS_CONTEXT"}`, and add a parallel bullet (or extend the existing one) introducing the `Hardener-NEEDS_CONTEXT` label alongside `Hardener-BLOCKED`, each keyed off the respective `hardener_verdict` value.
- [ ] In `claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md`, reword the "On a blocking Hardener verdict" paragraph (`:101`) so its trigger condition covers both `BLOCKED` and `NEEDS_CONTEXT` under one "blocking verdict" umbrella, preserving the existing behavior description (integration branch + every task worktree preserved, Step 4g cleanup skipped) verbatim for both values.
- [ ] In `claude-code/skills/ywc-parallel-executor/references/checkpoint-resume.md`'s `### State File Format` section, update the `hardener_verdict` inline comment/description (in the `waves[]` JSON example's surrounding prose, or the field's enum description if separately stated) to list all four values.
- [ ] In the same file's `### Resume with wave-int/<N>` section, insert a new numbered case 4 immediately after today's case 3 (`hardener_verdict == BLOCKED`): title it "Fully-merged-not-promoted, `hardener_verdict == NEEDS_CONTEXT`" `(pending empty, status != completed)`, and word it per spec FR-4 — resume stops and prints the recorded missing-context detail, then requires the context to be supplied (not a bare confirmation) before re-running Hardener, citing the `SKILL.md:220` per-subagent `NEEDS_CONTEXT` convention this mirrors at the wave-boundary layer.
- [ ] In `claude-code/skills/ywc-parallel-executor/scripts/resume-state.py`, inside the `in_progress` branch (after `pending = in_progress.get("pending", [])` and the existing worktree-validation loop, before falling through to the shared `result = {...}` construction), add: if `pending` is empty, read `verdict = in_progress.get("hardener_verdict")`; if `verdict in ("BLOCKED", "NEEDS_CONTEXT")`, build and print/return a non-`"valid"` result (`status: "blocked"` or `status: "needs_context"` respectively) carrying `resume_wave`, `mode`, `tasks_dir`, and `reason`/`blocked_detail` from `in_progress.get(...)` with absent-key omission (never `null`) in JSON mode, then exit non-zero (exit 1) — via a new small function, not `fail()` (which asserts `status: "error"`). Text-mode output mirrors `fail()`'s `CANNOT RESUME` block shape but is clearly a gate stop, not a script error.
- [ ] Add type annotations to every new/modified function signature in `resume-state.py` per PEP 8 / `~/.claude/rules/python/coding-style.md`.

## Task Verify
- [ ] `python3 claude-code/skills/scripts/update-state.py hardener-verdict 1 NEEDS_CONTEXT` against a fixture — exit 0, field written.
- [ ] `python3 claude-code/skills/scripts/update-state.py hardener-verdict 1 BOGUS` — non-zero exit, `die()` message lists all 4 values sorted.
- [ ] Hand-built fixtures (in_progress wave, `pending: []`, `hardener_verdict` = `NEEDS_CONTEXT` / `BLOCKED` / absent / `PASS`) against `resume-state.py --json` — statuses `needs_context` / `blocked` / `valid` / `valid` respectively.
- [ ] `grep -n "NEEDS_CONTEXT" claude-code/skills/ywc-parallel-executor/SKILL.md` — 4+ matches (4e.5, 4e.6, 4g, 4i).
- [ ] `grep -n "NEEDS_CONTEXT" claude-code/skills/ywc-parallel-executor/references/wave-integration-branch.md` and `references/checkpoint-resume.md` — both non-empty.

## Verification
- [ ] `bash scripts/validate.sh` passes (shellcheck, skill-structure checks, `--list` dry run — this repo has no separate lint/typecheck/build/test toolchain beyond this script).
- [ ] `python3 -c "import ast; ast.parse(open('claude-code/skills/ywc-parallel-executor/scripts/resume-state.py').read())"` — confirms no syntax error introduced.

## Implementation Notes
(Populated during execution — not authored at generation time.)
