# yw-000007-010-infra-validation-gate

## Purpose
Prove the whole change set regresses nothing, using the exact CI configuration plus the two checks CI does not cover.

## Scope
Run the five AC9 gates: `validate.sh`, `install.sh --list`, the toolkit-eval mechanical regression gate with justified baseline regeneration, markdownlint under the CI config and scope, and local `shellcheck` on the three changed shell scripts.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#a8--ci-검증-수단-정정-suggestion-2-대응-ac9-개정` — the revised AC9 and the two CI coverage gaps
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#acceptance-criteria` — AC9

### Summary
Two CI gaps make a dedicated gate task necessary. First, `.github/workflows/validate.yml:22` scopes shellcheck to `scandir: ./scripts`, so the three scripts this change set touches under `claude-code/skills/**/scripts/` are never linted by CI — NFR2 portability must be proven locally. Second, `validate.yml:37` runs a toolkit-eval mechanical regression gate that compares per-axis scores against a committed baseline and fails on any drop; this change set edits five SKILL.md files, so a score shift is plausible and a legitimate shift requires regenerating and committing the baseline. Markdownlint must run with the CI's own rule disables and glob scope, because the default configuration produces false positives from rules CI turns off, and `docs/ywc-plans/**` is outside the linted scope entirely.

### Out of Scope (from spec)
- Any behavioral change — this task fixes only what the gates surface, and escalates anything larger back to the owning task.
- `docs/ywc-plans/**` lint findings — outside the CI markdownlint scope and explicitly not a gate.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000006-010-docs-task-generator-artifacts-sync` — templates, locales, and evals must be final.
- `yw-000006-020-docs-executor-consumer-sync` — executor-family docs must be final.
- `yw-000006-030-docs-branch-testcase-consumer-sync` — remaining consumer docs must be final.

### Depended By
- (None — terminal task of this batch)

## Key Files
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json` (regenerated only if a score shift is justified)
- `.claude/skills/ywc-toolkit-eval/evals/scorecard.md` (regenerated alongside)

## Notes
- Baseline regeneration command: `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`. Regenerate only when the score movement is explained by the SKILL.md edits in this batch; an unexplained drop is a defect in the owning task, not a baseline to overwrite.
- Markdownlint must be run with the CI rule disables (`MD013`, `MD031`, `MD033`, `MD037`, `MD040`, `MD060`, `MD041` all off) and the CI globs (`README*.md`, `CONTRIBUTING*.md`, `claude-code/skills/*/README*.md`, `codex/skills/*/README*.md`).
- Three shell scripts need local shellcheck: `next-task-number.sh`, `scaffold-task-dir.sh`, and — if the batch touched it — any other changed `.sh` under `claude-code/skills/**/scripts/`.
- The pre-commit hook syncs `plugins/ywc-agent-toolkit` when `codex/skills` changes. This batch touches only `claude-code/`, so no plugin sync is expected; confirm the hook stayed quiet rather than assuming it.

## Hardening Evidence
### Test Feedback Path
- The five gate commands are themselves the feedback path. Each must be run and its output recorded, not summarized from memory.

### Interface Contract
- Contract: the repository's CI gate set as of this change.
- Inputs: the merged Phase `yw-000004` through `yw-000006` work.
- Outputs: pass/fail evidence plus, if justified, a regenerated eval baseline.
- Error model: any failing gate blocks; the fix is routed to the owning task rather than patched here.
- Impacted tests: all of them.

### Critical Surface Review
- Review requirement: N/A — spec declares no Critical Surfaces.

### Data Integrity Hardening
- Trigger surface: the committed toolkit-eval baseline is shared state consumed by CI.
- Atomic / locking strategy: N/A — single-writer file.
- Transaction boundary: regenerate baseline and scorecard together in one commit.
- Idempotency guard: re-running `score.py --ci` on an already-regenerated baseline must produce no diff.
- Required tests: post-regeneration re-run produces a clean tree.

## Parallel Execution Metadata
### Ownership
- `.claude/skills/ywc-toolkit-eval/evals/history.mechanical.json`
- `.claude/skills/ywc-toolkit-eval/evals/scorecard.md`

### Shared Surfaces
- Toolkit-eval baseline consumed by the CI regression gate
- CI workflow expectations

### Conflicts With
- (None identified — terminal task; every other task in this batch is already merged)

### Parallelizable After
- `yw-000006-010-docs-task-generator-artifacts-sync`, `yw-000006-020-docs-executor-consumer-sync`, `yw-000006-030-docs-branch-testcase-consumer-sync`

### Task Verify
- `bash scripts/validate.sh`
- `bash scripts/install.sh --list`
- `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci`
- markdownlint with the CI config and globs
- `shellcheck` on each changed `.sh` under `claude-code/skills/**/scripts/`

## Out of Scope
- Fixing findings that belong to an earlier task's scope — report and route them instead.
- Adding new CI workflows or widening the CI shellcheck scandir.
