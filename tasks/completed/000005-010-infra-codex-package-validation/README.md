# 000005-010-infra-codex-package-validation

## Purpose

모든 Codex skill port가 끝난 뒤 catalog, metadata, `.codex-plugin/skills` package copy, install smoke, validation gate를 정리한다. 이 task는 implementation batch의 final hard gate이며 release metadata policy를 지킨다.

## Scope

- `codex/skills/README.md` catalog와 routing sections update
- 필요한 README locale alignment 확인
- 신규 skill `agents/openai.yaml` 존재 확인
- `bash scripts/sync-codex-plugin.sh` 실행 후 `.codex-plugin/skills/**` generated copy 반영
- install smoke와 local validation 실행
- `translations.json`만 translation tooling이 요구할 때 update
- `VERSION`, `CHANGELOG.md`, root `plugin.json`은 hand-edit 금지

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-pr110-120-129-port.md#fr-6-metadata-plugin-copy-and-validation` - metadata, plugin copy, validation policy
- `docs/ywc-plans/codex-pr110-120-129-port.md#verification` - final command set
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac13---readme-locale-files-reflect-changed-behavior` - README locale acceptance criteria
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac14---catalogs-include-new-skills` - catalog acceptance criteria
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac15---plugin-package-is-synced` - plugin sync acceptance criteria
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac16---codex-only-boundary-holds` - Codex-only boundary
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac17---install-smoke-passes` - install smoke
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac18---local-validation-passes` - local validation

### Summary

This task makes the completed Codex source changes distributable. It updates the source catalog, syncs generated plugin package files, verifies no Claude Code files were touched, and runs the repository's install and validation gates. Release files controlled by Release Please must not be edited manually.

### Out of Scope (from spec)

- Implementing new skill behavior - handled by predecessor tasks
- Claude Code files under `claude-code/**` - out of scope entirely
- Root `VERSION`, `CHANGELOG.md`, and root `plugin.json` manual edits - out of scope by policy

## Dependencies

### Depends On

- `000003-010-infra-docker-isolate-package` - provides Docker isolate package
- `000003-020-docs-spec-ready-contract` - provides spec-ready package and validate contract
- `000004-010-infra-parallel-docker-hooks` - integrates Docker hooks
- `000004-020-infra-worktree-rollout` - completes worktree rollout

### Depended By

- (None - final task)

## Key Files

- `codex/skills/README.md`
- `.codex-plugin/skills/**`
- `translations.json` - only if translation tooling requires an update

## Notes

- `scripts/sync-codex-plugin.sh` rewrites some `bash codex/skills/...`, `python codex/skills/...`, and `cp codex/skills/...` command text in `.codex-plugin/skills`; do not require byte-identical source and package copies.
- The global leakage check is for `tools/codex-skill`, not for every existing `/ywc-*` example.
- Existing Codex READMEs and evals intentionally contain slash-command examples.

## Parallel Execution Metadata

### Ownership

- `codex/skills/README.md`
- `.codex-plugin/skills/**`
- `translations.json`

### Shared Surfaces

- Codex skill distribution catalog
- Codex plugin packaged skill copy
- Repository validation and install smoke gates

### Conflicts With

- (None identified after all dependencies merge)

### Parallelizable After

- `000003-010-infra-docker-isolate-package`
- `000003-020-docs-spec-ready-contract`
- `000004-010-infra-parallel-docker-hooks`
- `000004-020-infra-worktree-rollout`

### Task Verify

- `bash scripts/sync-codex-plugin.sh`
- `bash scripts/install.sh --list --codex`
- `CODEX_HOME="$(mktemp -d)" bash scripts/install.sh --codex ywc-docker-isolate ywc-spec-ready`
- `bash scripts/validate.sh`
- `if git diff --name-only | rg '^(claude-code/|\.claude/)'; then exit 1; fi`
- `if rg -n 'tools/codex-skill' codex/skills .codex-plugin/skills; then exit 1; fi`
- `if rg -n '/ywc-(spec-validate|task-generator|code-gen|sequential-executor|parallel-executor)' codex/skills/ywc-plan/SKILL.md .codex-plugin/skills/ywc-plan/SKILL.md; then exit 1; fi`

## Out of Scope

- Adding new behavior beyond validating and packaging completed predecessor outputs
- Running release publication
- Manual release version or changelog changes
