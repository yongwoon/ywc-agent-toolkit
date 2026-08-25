# Task: 000023-040-docs-codex-skill-contracts

## Prerequisites
- [ ] `000023-030-test-skill-eval-fixtures` is completed and merged.
- [ ] Read `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-7-tighten-remaining-s5-output-contracts`.
- [ ] Read `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-8-scope-progressive-disclosure-cleanup`.

## Allowed Edit Scope
- `codex/skills/ywc-agentic/**`
- `codex/skills/ywc-finish-branch/**`
- `codex/skills/ywc-sequential-executor/**`
- `codex/skills/ywc-parallel-executor/**`
- `codex/skills/ywc-gen-testcase/**`
- `codex/skills/ywc-task-generator/**`
- `codex/skills/ywc-plan/**`
- Generated plugin counterparts for the listed skill directories after `bash scripts/sync-codex-plugin.sh`

## Stop Conditions
- [ ] Stop if a proposed S5 fix requires changing the intended user workflow rather than clarifying the output/validation contract.
- [ ] Stop if a reference extraction would make the core workflow harder to follow or would require force-loading another skill.
- [ ] Stop if `bash scripts/sync-codex-plugin.sh` produces generated diffs outside the allowed skill directories.
- [ ] Stop if mechanical score drops on any previously passing axis.

## Implementation Steps

### Tighten S5 contract candidates
- [ ] Review `codex/skills/ywc-agentic/SKILL.md` for `## Output Format`, `## Validation`, `Status:`, and concrete template coverage.
- [ ] Review `codex/skills/ywc-finish-branch/SKILL.md` for the same S5 criteria.
- [ ] Add the smallest SKILL.md or eval fixture update needed if either contract remains too implicit.
- [ ] If no change is needed, capture the exact evidence lines for the final report.

### Reduce progressive-disclosure bloat
- [ ] Inspect `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-gen-testcase`, `ywc-task-generator`, and `ywc-plan` for duplicated static prompt material or long examples.
- [ ] Extract only low-risk leaf/static material to `references/` files.
- [ ] Replace extracted sections with direct Markdown links from `SKILL.md`.
- [ ] Preserve trigger descriptions, output contracts, validation checklists, and core workflow order.

### Sync and rescore
- [ ] Run `bash scripts/sync-codex-plugin.sh`.
- [ ] Run the internal scorer CI command and inspect any changed score details.
- [ ] Record S5 and progressive-disclosure decisions for the final report task.

## Task Verify
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --ci`
- [ ] `bash scripts/validate.sh`
- [ ] `bash scripts/install.sh --list --codex`
- [ ] `git diff --name-only`

## Verification
- [ ] S5 candidates either have concrete contract updates or documented no-change evidence.
- [ ] Extracted references are directly linked from their source `SKILL.md`.
- [ ] Generated plugin diffs mirror source skill edits only.
- [ ] `bash scripts/validate.sh` passes.
