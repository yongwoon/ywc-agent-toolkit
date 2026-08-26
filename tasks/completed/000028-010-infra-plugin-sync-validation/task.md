# 000028-010-infra-plugin-sync-validation — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `000027-010-refactor-plan-pr-spec-contracts` is completed and merged.
- [ ] `000027-020-refactor-pr-health-handler` is completed and merged.
- [ ] `000027-030-refactor-executor-health-sweeps` is completed and merged.
- [ ] `000027-040-refactor-agent-context-compaction` is completed and merged.
- [ ] `000027-050-refactor-parity-doc-hygiene` is completed and merged.
- [ ] `000027-060-test-codex-parity-evals` is completed and merged.

## Allowed Edit Scope
- [ ] Edit generated `plugins/ywc-agent-toolkit/skills/**` only through `bash scripts/sync-codex-plugin.sh`.
- [ ] Edit `CHANGELOG.md` only if final user-visible behavior changes need an Unreleased entry.
- [ ] Do not edit `VERSION` or `.release-please-manifest.json` unless current release workflow explicitly requires a manual version bump.

## Stop Conditions
- [ ] Stop if `scripts/sync-codex-plugin.sh` rewrites unexpected non-plugin paths.
- [ ] Stop if `bash scripts/validate.sh` fails for a source task's Ownership and cannot be fixed within plugin sync or changelog scope.
- [ ] Stop if `git diff --name-only` includes `claude-code/**` or `tools/codex-skill/**`.

## Implementation Steps
- [ ] Run source-specific verification commands from the spec.
  - [ ] Check helper syntax and executable bit.
  - [ ] Check eval JSON validity.
  - [ ] Run stale-pattern scans and classify any historical non-active matches.
- [ ] Run `bash scripts/sync-codex-plugin.sh`.
  - [ ] Review generated `plugins/ywc-agent-toolkit/skills/**` changes.
  - [ ] Confirm installed-path rewrites are expected.
- [ ] Run `bash scripts/validate.sh`.
  - [ ] Fix plugin freshness or structure failures within allowed scope.
  - [ ] If validation points to a Phase `000027` source bug, stop and report the owning task.
- [ ] Review release metadata.
  - [ ] Add concise `CHANGELOG.md` Unreleased Codex entry only if this repository's current process expects it.
  - [ ] Leave `VERSION` and `.release-please-manifest.json` unchanged unless manually required.
- [ ] Run final boundary and summary checks.
  - [ ] Confirm no `claude-code/**` or `tools/codex-skill/**` paths in implementation diff.
  - [ ] Capture `git diff --stat` for the implementation report.

## Task Verify
- [ ] `bash -n codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`
- [ ] `test -x codex/skills/ywc-handle-pr-reviews/scripts/fetch-pr-review-artifacts.sh`
- [ ] `python3 -m json.tool codex/skills/ywc-project-docs/evals/evals.json >/dev/null`
- [ ] `python3 -m json.tool codex/skills/ywc-project-scaffold/evals/evals.json >/dev/null`
- [ ] `rg -n "fetch-unresolved-comments|ywc-project-docs-ja|ywc-project-docs-kr|legalforce/cas-marketing-on|Critical/High/Medium/Low|PROCEED \\(≥ 90\\) \\| DONE \\| Spec is ready" codex/skills`
- [ ] `rg -n "tools/codex-skill|tools/claude-code" codex/skills plugins/ywc-agent-toolkit/skills`
- [ ] `bash scripts/sync-codex-plugin.sh`
- [ ] `bash scripts/validate.sh`
- [ ] `git diff --name-only | rg '^(claude-code/|tools/codex-skill/)' && exit 1 || true`
- [ ] `git diff --stat`

## Verification
- [ ] Full repository validation passes with `bash scripts/validate.sh`.
- [ ] Generated plugin package is current after sync.
- [ ] Codex-only boundary holds.
