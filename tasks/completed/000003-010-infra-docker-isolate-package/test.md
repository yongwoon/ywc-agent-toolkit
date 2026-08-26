# 000003-010-infra-docker-isolate-package - Manual Test Plan

## Preconditions

- [ ] `codex/skills/ywc-docker-isolate/` exists with scripts and references.
- [ ] Docker may be absent; absent Docker must be handled without corrupting repository state.

## Test Scenarios

### Scenario 1: package structure is installable

**Steps:**
1. Run `find codex/skills/ywc-docker-isolate -maxdepth 3 -type f | sort`.
2. Confirm required files from AC1 are present.

**Expected Result:**
- `SKILL.md`, README locale set, `agents/openai.yaml`, references, and all four scripts are present.

### Scenario 2: shell scripts parse on local machine

**Steps:**
1. Run `bash -n codex/skills/ywc-docker-isolate/scripts/*.sh`.
2. Run `find codex/skills/ywc-docker-isolate/scripts -type f -perm -111 | sort`.

**Expected Result:**
- Shell syntax passes.
- Executable scripts are listed with executable bits.

### Scenario 3: source path leakage is absent

**Steps:**
1. Run `rg -n 'tools/codex-skill' codex/skills/ywc-docker-isolate`.

**Expected Result:**
- No matches are returned.
