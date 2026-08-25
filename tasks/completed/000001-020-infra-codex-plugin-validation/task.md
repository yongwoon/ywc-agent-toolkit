# 000001-020-infra-codex-plugin-validation — Implementation Checklist

## Prerequisites

Verify these before starting:
- [ ] `000001-010-infra-codex-plugin-package-layout` is completed (merged).
- [ ] `.codex-plugin/plugin.json` exists.
- [ ] `.codex-plugin/skills/ywc-plan/SKILL.md` exists.

## Allowed Edit Scope

- [ ] Stay within `scripts/validate.sh` and validation-related references to `.codex-plugin/**`.
- [ ] If this task needs to change package layout, stop and report back to `000001-010` output.

## Stop Conditions

- [ ] Stop if `jq` is unavailable in CI and no existing project requirement covers it.
- [ ] Stop if freshness comparison cannot be deterministic.
- [ ] Stop if validation needs to mutate files rather than report stale state.
- [ ] Stop if validating `.codex-plugin/skills/**` requires changing source skill files.

## Implementation Steps

- [ ] Add `check_codex_plugin_manifest` to `scripts/validate.sh`.
  - [ ] Validate `.codex-plugin/plugin.json` exists.
  - [ ] Validate JSON parseability.
  - [ ] Validate top-level required fields: `name`, `version`, `description`, `author`, `repository`, `license`, `keywords`, `skills`, `interface`.
  - [ ] Validate `.skills == "./skills/"`.
- [ ] Add `interface` field checks.
  - [ ] Validate display fields needed by the spec: display name, short description, long description, developer name, category, capabilities, default prompts, website URL, brand color.
  - [ ] Validate optional asset references only when present.
- [ ] Add plugin-local skills checks.
  - [ ] Validate `.codex-plugin/skills/` exists.
  - [ ] Validate `.codex-plugin/skills/ywc-plan/SKILL.md` exists.
  - [ ] Compare source and plugin-local copy freshness using a deterministic method.
  - [ ] Print the exact refresh command when stale copy is detected.
- [ ] Integrate the new check into the existing validation flow.
  - [ ] Run it after Codex skill structure checks and before install-script dry run.
  - [ ] Preserve existing `ERRORS` accumulation pattern.

## Task Verify

- [ ] `bash scripts/validate.sh`
- [ ] `bash scripts/install.sh --list`
- [ ] `test "$(jq -r '.skills' .codex-plugin/plugin.json)" = "./skills/"`
- [ ] Temporarily alter one copied skill in `.codex-plugin/skills/` and confirm validation reports stale copy, then restore it.

## Verification

- [ ] Structure validation passes: `bash scripts/validate.sh`
- [ ] Install listing works: `bash scripts/install.sh --list`
- [ ] Targeted Codex install still works: `bash scripts/install.sh --codex ywc-plan`

