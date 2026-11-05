# yk-000005-050-domain-handoff-retro-skills — Manual Test Plan

## Preconditions
- [ ] Previous dependency tasks are merged
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Secret in session text
**Steps:**
1. Follow the handoff steps for a session containing `API_KEY=abc123` in prose, a log and a URL query

**Expected Result:**
- All occurrences become `<REDACTED>` before any file is written

### Scenario 2: Save location
**Steps:**
1. Set `TMPDIR` inside the repository and follow the save step

**Expected Result:**
- Refuses to write (canonical path is inside the repository)

### Scenario 3: File safety
**Steps:**
1. Follow the save step normally and inspect the file

**Expected Result:**
- Created via `mktemp` with mode 0600; unverifiable State fields tagged `[unverified]`

### Scenario 4: Retro dispatch
**Steps:**
1. Run `bash scripts/validate.sh`

**Expected Result:**
- `named_agent_release_test.py` passes with `ywc-retro` present
