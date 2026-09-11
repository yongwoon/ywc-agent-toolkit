# Task: yw-000038-020-domain-hardener-needs-context-gating-codex

## Prerequisites
- [ ] N/A — root task, no predecessor task required.

## Allowed Edit Scope
Only the five codex-root files listed in README.md `## Ownership`:
`codex/skills/scripts/update-state.py`, `codex/skills/ywc-parallel-executor/SKILL.md`,
`codex/skills/ywc-parallel-executor/references/wave-integration-branch.md`,
`codex/skills/ywc-parallel-executor/references/checkpoint-resume.md`,
`codex/skills/ywc-parallel-executor/scripts/resume-state.py`.
Do not hand-edit `plugins/ywc-agent-toolkit/skills/` (auto-synced by the repo's pre-commit hook)
and do not touch any claude-code-root file.

## Stop Conditions
- If `codex/skills/scripts/update-state.py:210-221` is no longer byte-identical in shape to the claude-code file's `VALID_HARDENER_VERDICTS`/`cmd_hardener_verdict` region, stop and report the divergence rather than guessing at intent.
- If `codex/skills/ywc-parallel-executor/SKILL.md`'s lines 367/368/372/415 no longer contain the wording described in README.md `## Scope`, re-locate by grepping for `hardener-verdict`, `BLOCKED > NEEDS_CONTEXT`, `Hardener-BLOCKED`, and report if the wording itself (not just line numbers) has changed materially.
- If `codex/skills/ywc-parallel-executor/references/checkpoint-resume.md`'s case-3 wording or the `--resume-disposition` framing at `:13`/`:22-25` has been edited since the spec was written, stop and report — do not silently pick a resolution for the pre-existing tension the spec explicitly leaves alone.

## Implementation Steps

- [ ] In `codex/skills/scripts/update-state.py`, extend `VALID_HARDENER_VERDICTS` to include `"NEEDS_CONTEXT"`, matching the exact edit made in `claude-code/skills/scripts/update-state.py` by `yw-000038-010`.
- [ ] In `codex/skills/ywc-parallel-executor/SKILL.md` (`:367`), extend the `hardener-verdict <N> <absent|PASS|BLOCKED>` checkpoint call to `<absent|PASS|BLOCKED|NEEDS_CONTEXT>` — leave the wave-boundary aggregation precedence prose (`BLOCKED > NEEDS_CONTEXT > DONE_WITH_CONCERNS > DONE`) on the same line untouched; only the checkpoint-call value domain changes.
- [ ] In the same file (`:368`), change the promotion condition "the aggregate outcome above is not an `enforced`-tier `BLOCKED`" to "the aggregate outcome above is neither an `enforced`-tier `BLOCKED` nor `NEEDS_CONTEXT`".
- [ ] In the same file (`:372`), extend the Step 4g exclusion condition from `hardener_verdict is not BLOCKED` to `hardener_verdict is not in {BLOCKED, NEEDS_CONTEXT}`, updating the `Hardener-BLOCKED` label reference to distinguish both cases in prose.
- [ ] In the same file (`:415`), extend the Step 4i terminal-state bucket condition from `hardener_verdict == "BLOCKED"` to `hardener_verdict in {"BLOCKED", "NEEDS_CONTEXT"}`, introducing the `Hardener-NEEDS_CONTEXT` label alongside `Hardener-BLOCKED`.
- [ ] In `codex/skills/ywc-parallel-executor/references/wave-integration-branch.md`'s Promotion section (step `4e.6`), change "promote it into the base branch only when the aggregate outcome under an `enforced` contract is not `BLOCKED`" to "...is neither `BLOCKED` nor `NEEDS_CONTEXT`".
- [ ] In `codex/skills/ywc-parallel-executor/references/checkpoint-resume.md`'s State File Format section, update the `hardener_verdict` description to list all four values.
- [ ] In the same file's `### Resume with wave-int/<N>` section, insert case 4 immediately after case 3 (`:85`): title it "Fully-merged-not-promoted, `hardener_verdict == NEEDS_CONTEXT`" `(pending empty, status != completed)`. Word it mirroring case 3's existing phrasing convention ("requires explicit user confirmation before re-running the gate") but requiring the missing context to be *supplied* rather than a bare confirmation — per spec FR-4's codex-specific note, do not attempt to reconcile this with the file's own `--resume-disposition` non-interactive framing at `:13`/`:22-25`.
- [ ] In `codex/skills/ywc-parallel-executor/scripts/resume-state.py`'s `in_progress` branch (after the existing `pending = in_progress.get("pending", [])` / worktree-validation block, before the shared result construction around `:213`), add the same `hardener_verdict` inspection as `yw-000038-010`'s claude-code edit: when `pending` is empty, `verdict = in_progress.get("hardener_verdict")`; `verdict in ("BLOCKED", "NEEDS_CONTEXT")` short-circuits to a non-`"valid"` result (`status: "blocked"` / `"needs_context"`) via a new sibling function to `fail()` (not `fail()` itself), carrying `resume_wave`, `mode`, `tasks_dir`, `reason`/`blocked_detail` (absent-key omission, never `null`), exit 1.
- [ ] Add type annotations to every new/modified function signature per PEP 8 / `~/.claude/rules/python/coding-style.md` — matches this file's existing fully-typed style.
- [ ] Run `bash scripts/sync-codex-plugin.sh` (or the repo's documented plugin-sync step) to update `plugins/ywc-agent-toolkit/skills/ywc-parallel-executor` and stage the result — do not hand-edit the plugin mirror directly.

## Task Verify
- [ ] `python3 codex/skills/scripts/update-state.py hardener-verdict 1 NEEDS_CONTEXT` — exit 0, field written.
- [ ] `python3 codex/skills/scripts/update-state.py hardener-verdict 1 BOGUS` — non-zero exit, sorted 4-value `die()` message.
- [ ] Hand-built fixtures against `resume-state.py --json` — `needs_context` / `blocked` / `valid` / `valid`.
- [ ] `diff <(python3 codex/skills/scripts/update-state.py --help) <(python3 claude-code/skills/scripts/update-state.py --help)` — identical.
- [ ] `grep -n "NEEDS_CONTEXT" codex/skills/ywc-parallel-executor/SKILL.md` — 4+ matches.
- [ ] `grep -n "NEEDS_CONTEXT" codex/skills/ywc-parallel-executor/references/checkpoint-resume.md` — non-empty.
- [ ] `diff -r codex/skills/ywc-parallel-executor plugins/ywc-agent-toolkit/skills/ywc-parallel-executor` — exits 0 after sync.

## Verification
- [ ] `bash scripts/validate.sh` passes.
- [ ] `python3 -c "import ast; ast.parse(open('codex/skills/ywc-parallel-executor/scripts/resume-state.py').read())"` — no syntax error.

## Implementation Notes
(Populated during execution — not authored at generation time.)
