# 000032-010-infra-codex-plugin-sync-validation — Implementation Checklist

## Prerequisites

- [ ] `000031-010-docs-spec-writer-codex-zh-es` is completed.
- [ ] `000031-020-docs-task-generator-codex-zh-es` is completed.
- [ ] `000031-030-docs-gen-testcase-codex-zh-es` is completed.
- [ ] `000031-040-docs-pr-creation-language-zh-es` is completed.
- [ ] `000031-050-docs-executor-pr-lang-zh-es` is completed.
- [ ] `000031-060-docs-pr-review-reply-zh-es` is completed.

## Allowed Edit Scope

- [ ] Generated plugin/package files only:
  - `plugins/ywc-agent-toolkit/skills/**`
  - `plugins/ywc-agent-toolkit/.codex-plugin/plugin.json`
  - `plugins/ywc-agent-toolkit/README.md`
- [ ] If source fixes are needed, stop and route back to the owning `000031-*` task.

## Stop Conditions

- [ ] `bash scripts/sync-codex-plugin.sh` fails.
- [ ] `bash scripts/validate.sh` fails for a source issue that cannot be fixed within generated output.
- [ ] `git diff --name-only` includes `claude-code/**`.
- [ ] Generated plugin output appears to diverge from `codex/skills/**` beyond known sync path rewrites.

## Hardening Gate

- [ ] Classify this task: generated-file-only / validation gate.
- [ ] Existing coverage: `bash scripts/validate.sh`.
- [ ] Interface contract: Codex source to plugin mirror sync.
- [ ] Critical surface 없음.

## Implementation Steps

- [ ] Run `bash scripts/sync-codex-plugin.sh`.
- [ ] Validate touched eval JSON files.
  - [ ] `python3 -m json.tool codex/skills/ywc-spec-writer/evals/evals.json >/dev/null`
  - [ ] `python3 -m json.tool codex/skills/ywc-task-generator/evals/evals.json >/dev/null`
  - [ ] `python3 -m json.tool codex/skills/ywc-gen-testcase/evals/evals.json >/dev/null`
  - [ ] Run the same command for workflow skill evals touched by Phase `000031`.
- [ ] Run targeted skill validation for primary content-output skills.
  - [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-spec-writer`
  - [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-task-generator`
  - [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-gen-testcase`
- [ ] Run full repository validation: `bash scripts/validate.sh`.
- [ ] Run final scope check: `git diff --name-only | rg '^claude-code/' && exit 1 || true`.
- [ ] Review `git diff --stat` and confirm all plugin changes correspond to Codex source changes.

## Task Verify

- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `git diff --name-only | rg '^claude-code/' && exit 1 || true`
- [ ] `git diff --name-only | rg '^(codex/skills|plugins/ywc-agent-toolkit/skills|tasks/)'` shows only expected paths.

## Verification

- [ ] Full repository validation passes.
- [ ] Plugin mirror is synced.
- [ ] No `claude-code/**` files are changed.
