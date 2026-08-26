# 000017-010-infra-codex-karpathy-validation — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `000016-010-docs-principles-guideline-gap` is completed (merged).
- [ ] `000016-020-docs-code-gen-worker-discipline` is completed (merged).
- [ ] `000016-030-docs-task-template-goal-verification` is completed (merged).
- [ ] `000016-040-docs-skill-author-future-proofing` is completed (merged).
- [ ] `000016-050-docs-custom-agent-bounded-evidence` is completed (merged).

## Allowed Edit Scope
- [ ] Run `bash scripts/sync-codex-plugin.sh` to update generated plugin package.
- [ ] Do not manually edit `plugins/ywc-agent-toolkit/skills/**`.
- [ ] If source fixes are required, stop and route back to the owning source task.

## Stop Conditions
- [ ] Stop if any Phase `000016` task is not merged.
- [ ] Stop if `git diff --name-only` shows unexpected `claude-code/**` edits.
- [ ] Stop if generated plugin output cannot be explained by `codex/skills/**` source changes.

## Implementation Steps
- [ ] Run Codex plugin sync.
  - Related AC/FR: AC10, FR-7
  - Contract / Behavior Change: generated plugin package reflects changed `codex/skills` source.
  - Verification Command / Evidence: `bash scripts/sync-codex-plugin.sh`
- [ ] Run full repository validation.
  - Related AC/FR: AC11, FR-7
  - Contract / Behavior Change: repository structure, plugin package freshness, and mechanical eval gate pass.
  - Verification Command / Evidence: `bash scripts/validate.sh`
- [ ] Run Codex skill install list check.
  - Related AC/FR: AC11, FR-7
  - Contract / Behavior Change: changed Codex skills remain installable/listable.
  - Verification Command / Evidence: `bash scripts/install.sh --list --codex`
- [ ] Run Codex agent install list check.
  - Related AC/FR: AC11, FR-7
  - Contract / Behavior Change: changed custom agents remain installable/listable.
  - Verification Command / Evidence: `bash scripts/install.sh --list --codex-agents`
- [ ] Run targeted guideline integration grep.
  - Related AC/FR: AC1, AC3, AC4, AC5, AC6, AC7, FR-7
  - Contract / Behavior Change: expected guidance appears in source files.
  - Verification Command / Evidence: `rg -n "Assumption|Goal-Driven|NEEDS_CONTEXT|Simplicity|Surgical|success criteria|verification" codex/skills/references/principles.md codex/skills/ywc-code-gen/prompts/implementer-base.md codex/skills/ywc-task-generator/references/task.md.template codex/skills/ywc-skill-author/SKILL.md codex/agents`
- [ ] Inspect final diff scope.
  - Related AC/FR: AC2, AC8, AC10, AC12, FR-7
  - Contract / Behavior Change: no new Karpathy skill, no Claude Code edits, no manual generated package drift.
  - Verification Command / Evidence: `git diff --name-only`

## Task Verify
- [ ] Run `bash scripts/sync-codex-plugin.sh`.
- [ ] Run `bash scripts/validate.sh`.
- [ ] Run `bash scripts/install.sh --list --codex`.
- [ ] Run `bash scripts/install.sh --list --codex-agents`.
- [ ] Run the targeted `rg` command from the implementation step.
- [ ] Run `git diff --name-only` and confirm scope.

## Verification
- [ ] Sync exits 0.
- [ ] Validation exits 0.
- [ ] Install list checks exit 0.
- [ ] Targeted grep finds expected guidance across changed surfaces.
- [ ] Final diff scope matches the spec.
