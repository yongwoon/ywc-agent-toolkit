# 000028-010-infra-plugin-sync-validation — Manual Test Plan

## Preconditions
- [ ] All Phase `000027` tasks are merged.
- [ ] Local shell has `bash`, `rg`, `jq`, `python3`, and `gh` available.

## Test Scenarios

### Scenario 1: Plugin package is generated from source
**Steps:**
1. Run `bash scripts/sync-codex-plugin.sh`.
2. Run `git diff --name-only plugins/ywc-agent-toolkit/skills`.

**Expected Result:**
- Plugin package changes reflect source `codex/skills/**` changes.
- No generated files require hand edits before validation.

### Scenario 2: Repository validation passes
**Steps:**
1. Run `bash scripts/validate.sh`.
2. Review any validation output.

**Expected Result:**
- Validation exits `0`.
- No stale plugin package error remains.

### Scenario 3: Codex-only boundary is preserved
**Steps:**
1. Run `git diff --name-only | rg '^(claude-code/|tools/codex-skill/)' && exit 1 || true`.

**Expected Result:**
- Command exits `0`.
- No implementation diff touches `claude-code/**` or `tools/codex-skill/**`.
