# 000001-010-infra-codex-plugin-package-layout — Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] Current branch is based on the intended base branch.
- [ ] `docs/ywc-plans/codex-plugin-distribution.md#iteration-1-amendments` has been read.

## Allowed Edit Scope

- [ ] Stay within `.codex-plugin/**`, `scripts/sync-codex-plugin.sh`, and packaging copy behavior from `codex/skills/**` to `.codex-plugin/skills/**`.
- [ ] Treat `codex/skills/**` as source input; do not edit skill source content for this task.
- [ ] If implementation requires edits outside Ownership, stop and report before proceeding.

## Stop Conditions

- [ ] Stop if Codex plugin loader documentation or a real install test proves `"skills": "./skills/"` is wrong.
- [ ] Stop if symlinks appear necessary; the spec forbids them for plugin packaging.
- [ ] Stop if copying all `codex/skills/**` creates a PR too large to review without a generation-only release artifact decision.
- [ ] Stop if manifest fields require private marketplace data that is not present in the repo.

## Implementation Steps

- [ ] Add `.codex-plugin/plugin.json`.
  - [ ] Set `name`, `version`, `description`, `author`, `repository`, `license`, and `keywords` from current repository metadata.
  - [ ] Set `"skills": "./skills/"`.
  - [ ] Add `interface` metadata for Codex App display.
- [ ] Establish plugin-local skill package output.
  - [ ] Add `.codex-plugin/skills/` as a real file tree copied from `codex/skills/`, or add `scripts/sync-codex-plugin.sh` that deterministically creates it.
  - [ ] Ensure `.codex-plugin/skills/ywc-plan/SKILL.md` exists after sync/generation.
  - [ ] Ensure copied files preserve required Codex skill structure and executable bits for scripts.
- [ ] Handle assets deliberately.
  - [ ] If `composerIcon` or `logo` is present in the manifest, add the referenced file under `.codex-plugin/assets/`.
  - [ ] If assets are omitted, ensure manifest does not reference missing asset paths.
- [ ] Preserve existing install behavior.
  - [ ] Do not modify `scripts/install.sh --codex` behavior.
  - [ ] Do not modify `.claude-plugin/plugin.json`.

## Task Verify

- [ ] `jq empty .codex-plugin/plugin.json`
- [ ] `test "$(jq -r '.skills' .codex-plugin/plugin.json)" = "./skills/"`
- [ ] `test -f .codex-plugin/skills/ywc-plan/SKILL.md`
- [ ] `test -f codex/skills/ywc-plan/SKILL.md`
- [ ] `bash scripts/install.sh --list`

## Verification

- [ ] Structure validation passes: `bash scripts/validate.sh` (may require `000001-020` if validation is intentionally updated there)
- [ ] Install listing works: `bash scripts/install.sh --list`
- [ ] Targeted Codex install still works: `bash scripts/install.sh --codex ywc-plan`

