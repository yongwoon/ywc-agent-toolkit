# 000023-040-docs-codex-skill-contracts

## Purpose

Tighten the remaining Codex skill output contracts and reduce low-value SKILL.md context bloat while preserving existing behavior and validation.

## Scope

- Review `ywc-agentic` and `ywc-finish-branch` for S5 output/validation contract gaps.
- Add the smallest deterministic SKILL.md or eval update needed for downstream consumers.
- Review long executor-adjacent skill bodies and extract low-risk static material to `references/`.
- Run Codex skill sync after source skill edits and keep generated plugin changes source-aligned.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-7-tighten-remaining-s5-output-contracts` — S5 contract candidates and criteria.
- `docs/ywc-plans/codex-agent-skill-eval-harness-improvements.md#fr-8-scope-progressive-disclosure-cleanup` — long skill bodies and extraction candidates.
- `CLAUDE.md#skill-authoring-rules` — SKILL.md line-count and reference extraction guidance.
- `codex/AGENTS.md` — generated plugin sync rule for Codex skills.

### Summary
This task focuses on small documentation and fixture changes that make Codex skill behavior more deterministic for downstream agents. It should avoid broad rewrites and only extract static or duplicated material when the pointer remains direct and validation still passes. The final report will decide score movement; this task only creates the evidence.

### Out of Scope (from spec)
- Agent smoke harness and evidence — handled by `000023-010-infra-agent-smoke-harness` and `000023-020-test-agent-smoke-evidence`.
- Missing fixture coverage for the nine FR-6 targets — handled by `000023-030-test-skill-eval-fixtures`.
- Report and scoreboard edits — handled by `000024-010-docs-eval-report-scoreboard`.

## Dependencies

### Depends On
- `000023-030-test-skill-eval-fixtures` — complete first to avoid overlapping Codex skill sync churn.

### Depended By
- `000024-010-docs-eval-report-scoreboard` — needs S5 and progressive-disclosure results.

## Key Files
- `codex/skills/ywc-agentic/SKILL.md`
- `codex/skills/ywc-agentic/evals/**`
- `codex/skills/ywc-finish-branch/SKILL.md`
- `codex/skills/ywc-finish-branch/evals/**`
- `codex/skills/ywc-sequential-executor/SKILL.md`
- `codex/skills/ywc-sequential-executor/references/**`
- `codex/skills/ywc-parallel-executor/SKILL.md`
- `codex/skills/ywc-parallel-executor/references/**`
- `codex/skills/ywc-gen-testcase/SKILL.md`
- `codex/skills/ywc-gen-testcase/references/**`
- `codex/skills/ywc-task-generator/SKILL.md`
- `codex/skills/ywc-task-generator/references/**`
- `codex/skills/ywc-plan/SKILL.md`
- `codex/skills/ywc-plan/references/**`
- `plugins/ywc-agent-toolkit/skills/**` generated counterparts after sync

## Notes

- A no-change decision is acceptable if the reviewed contract is already deterministic; record the evidence for the final report.
- Extract only leaf/static sections or duplicated prompt material. Do not force-load sibling skills or create hidden dependencies.
- Keep `SKILL.md` pointers direct so progressive disclosure remains obvious to future agents.

## Parallel Execution Metadata

### Ownership
- `codex/skills/ywc-agentic/**`
- `codex/skills/ywc-finish-branch/**`
- `codex/skills/ywc-sequential-executor/**`
- `codex/skills/ywc-parallel-executor/**`
- `codex/skills/ywc-gen-testcase/**`
- `codex/skills/ywc-task-generator/**`
- `codex/skills/ywc-plan/**`
- Generated plugin counterparts for those skill directories only

### Shared Surfaces
- Codex skill source/generated sync.
- Internal mechanical scoring for SKILL.md body size and output contract structure.

### Conflicts With
- `000023-030-test-skill-eval-fixtures` — shared Codex skill sync and generated plugin surfaces.

### Parallelizable After
- `000023-030-test-skill-eval-fixtures`

### Task Verify
- `bash scripts/sync-codex-plugin.sh`
- `python3 tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/score.py --target all --ci`
- `bash scripts/validate.sh`
- `bash scripts/install.sh --list --codex`

## Out of Scope

- Rewriting full workflows for style.
- Moving scores in `docs/skill-agent-eval/codex/scoreboard.md`.
- Editing Claude Code skills or agents.
