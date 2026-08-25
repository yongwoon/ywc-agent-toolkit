# 000074-010-infra-architecture-invariants-distribution — Manual Test Plan

## Preconditions
- [ ] All Phase `000073` tasks are merged.
- [ ] `bash scripts/sync-codex-plugin.sh` is available.

## Test Scenarios

### Scenario 1: Source/package consistency
**Steps:**
1. Run `bash scripts/sync-codex-plugin.sh`.
2. Run `bash scripts/validate.sh`.

**Expected Result:**
- The generated plugin is current and repository validation passes.

### Scenario 2: Isolated installation
**Steps:**
1. Create a temporary directory.
2. Run `CODEX_HOME=<temporary-directory> bash scripts/install.sh --codex ywc-architecture-invariants`.
3. Confirm the installed skill contains its required metadata files.

**Expected Result:**
- Installation succeeds without touching the real user Codex home.
