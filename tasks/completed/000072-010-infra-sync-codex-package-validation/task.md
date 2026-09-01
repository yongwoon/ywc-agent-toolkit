# 000072-010-infra-sync-codex-package-validation — Implementation Checklist

## Prerequisites
- [ ] `000071-010-refactor-direct-lane-handoffs` is completed and merged.

## Allowed Edit Scope
- [ ] Run sync into the repository's generated package path.
- [ ] Use only disposable paths for installation checks.
- [ ] Do not hand-edit generated files or source skills.

## Stop Conditions
- [ ] Stop if sync produces unexpected source changes or deletes unrelated generated assets.
- [ ] Stop if validation fails for a predecessor task's source contract; report the failing path.
- [ ] Stop if targeted install writes outside the disposable `CODEX_HOME`.

## Hardening Gate
- [ ] Classify as generated-file and distribution validation work.
- [ ] Existing repository checks are the named verification path; no production behavior is authored here.
- [ ] Confirm generated package and source package are the interface contract.
- [ ] Require full final review of the generated diff before completion.

## Implementation Steps
- [ ] Run `bash scripts/sync-codex-plugin.sh` from the repository root.
- [ ] Run `bash scripts/validate.sh` and resolve only failures caused by this batch.
- [ ] Run `bash scripts/install.sh --list --codex` and confirm `ywc-implement` is listed.
- [ ] Create a disposable `CODEX_HOME`, install only `ywc-implement`, and verify its `SKILL.md`, Tier 1 READMEs, and `agents/openai.yaml` exist.
- [ ] Inspect `git diff --check` and the generated package diff; confirm no manual source edits or unrelated output changed.

## Task Verify
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `bash scripts/install.sh --list --codex`
- [ ] `tmp_codex_home="$(mktemp -d)"; CODEX_HOME="$tmp_codex_home" bash scripts/install.sh --codex ywc-implement; test -f "$tmp_codex_home/skills/ywc-implement/SKILL.md"`
- [ ] `git diff --check`

## Verification
- [ ] All commands above pass with exit status 0.
- [ ] Generated marketplace package contains the final source skill set.

## Implementation Notes
