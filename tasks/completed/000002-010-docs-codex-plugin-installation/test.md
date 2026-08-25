# 000002-010-docs-codex-plugin-installation — Manual Test Plan

## Preconditions

- [ ] `000001-010-infra-codex-plugin-package-layout` is merged.
- [ ] `000001-020-infra-codex-plugin-validation` is merged.
- [ ] README changes are present in the working branch.

## Test Scenarios

### Scenario 1: Codex CLI install guidance is findable

**Steps:**
1. Open `README.md`.
2. Search for `Codex CLI`.
3. Read the install subsection.

**Expected Result:**
- The section mentions `/plugins`.
- The section does not claim official marketplace availability unless it is confirmed.
- Bash fallback remains available.

### Scenario 2: Codex App install guidance is findable

**Steps:**
1. Open `README.md`.
2. Search for `Codex App`.
3. Read the install subsection.

**Expected Result:**
- The section describes the Plugins sidebar flow.
- The wording matches actual package status.
- No missing asset or manifest path is referenced as a user-facing manual step.

### Scenario 3: Translation handling is explicit

**Steps:**
1. Check whether localized root README files changed.
2. Run `bash scripts/translate.sh --dry-run`.
3. Review PR notes or commit body.

**Expected Result:**
- Either localized root README files are updated consistently, or deferral is explicitly documented.
- Translation dry-run does not reveal an unacknowledged translation change.

