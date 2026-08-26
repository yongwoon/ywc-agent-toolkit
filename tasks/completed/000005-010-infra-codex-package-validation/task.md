# 000005-010-infra-codex-package-validation - Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] `000003-010-infra-docker-isolate-package` is completed and merged.
- [ ] `000003-020-docs-spec-ready-contract` is completed and merged.
- [ ] `000004-010-infra-parallel-docker-hooks` is completed and merged.
- [ ] `000004-020-infra-worktree-rollout` is completed and merged.

## Allowed Edit Scope

- [ ] Stay within `codex/skills/README.md`, `.codex-plugin/skills/**`, and `translations.json` only when required by tooling.
- [ ] Do not edit `VERSION`, `CHANGELOG.md`, root `plugin.json`, `claude-code/**`, or `.claude/**`.

## Stop Conditions

- [ ] Stop if `bash scripts/sync-codex-plugin.sh` changes unexpected non-Codex package paths.
- [ ] Stop if validation requires hand-editing Release Please managed files.
- [ ] Stop if source-path leakage remains in `codex/skills` after predecessor tasks.

## Implementation Steps

- [ ] Update source Codex catalog.
  - [ ] Add `ywc-docker-isolate` to `codex/skills/README.md`.
  - [ ] Add `ywc-spec-ready` to `codex/skills/README.md`.
  - [ ] Keep `ywc-parallel-executor`, `ywc-spec-validate`, `ywc-agentic`, and `ywc-worktrees` routing identities consistent with the spec.
- [ ] Check README locale behavior across touched skills.
  - [ ] Verify Docker isolate README locale set exists.
  - [ ] Verify spec-ready and spec-validate README locale changes mention readiness and advisor budget behavior.
  - [ ] Verify worktree-related README locale changes mention `--worktree`, `--keep-branch`, and `--worktree-path` where relevant.
- [ ] Sync plugin package.
  - [ ] Run `bash scripts/sync-codex-plugin.sh`.
  - [ ] Review `.codex-plugin/skills/**` generated changes for expected skill additions and command path rewrites.
  - [ ] Confirm executable file modes match source package.
- [ ] Run install smoke and validation.
  - [ ] Run `bash scripts/install.sh --list --codex`.
  - [ ] Run `CODEX_HOME="$(mktemp -d)" bash scripts/install.sh --codex ywc-docker-isolate ywc-spec-ready`.
  - [ ] Run `bash scripts/validate.sh`.
- [ ] Enforce Codex-only and source-path boundaries.
  - [ ] Confirm no `claude-code/**` or `.claude/**` path is in the implementation diff.
  - [ ] Confirm no `tools/codex-skill` text appears in `codex/skills` or `.codex-plugin/skills`.
  - [ ] Run scoped slash-command leakage check only against `ywc-plan` source and plugin copies.

## Task Verify

- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `bash scripts/install.sh --list --codex`
- [ ] `CODEX_HOME="$(mktemp -d)" bash scripts/install.sh --codex ywc-docker-isolate ywc-spec-ready`
- [ ] `bash scripts/validate.sh`
- [ ] `if git diff --name-only | rg '^(claude-code/|\.claude/)'; then exit 1; fi`
- [ ] `if rg -n 'tools/codex-skill' codex/skills .codex-plugin/skills; then exit 1; fi`
- [ ] `if rg -n '/ywc-(spec-validate|task-generator|code-gen|sequential-executor|parallel-executor)' codex/skills/ywc-plan/SKILL.md .codex-plugin/skills/ywc-plan/SKILL.md; then exit 1; fi`

## Verification

- [ ] `git diff --check`
- [ ] Final implementation diff contains no hand-edits to `VERSION`, `CHANGELOG.md`, or root `plugin.json`.
