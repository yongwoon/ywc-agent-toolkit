# yk-000010-030-domain-retro-readonly-lenses — Manual Test Plan

## Preconditions
- [ ] The task's changes are applied on the working branch

## Test Scenarios

### Scenario 1: Lens tools
**Steps:**
1. Run `/ywc-retro` on a short session and inspect each lens dispatch

**Expected Result:**
- no lens or synthesizer dispatch has Bash/WebFetch/MCP

### Scenario 2: Output files
**Steps:**
1. After the run, list `<run>/`

**Expected Result:**
- the three lens files and `synthesis.md` exist and are non-empty
