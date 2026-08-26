# 000003-010-infra-docker-isolate-package

## Purpose

PR #110의 Codex `ywc-docker-isolate` skill package를 이 repository 구조에 맞게 추가한다. 이 task는 Docker port isolation 자체의 독립 package와 script 검증까지 담당하며, executor 연결은 후속 task가 처리한다.

## Scope

- `codex/skills/ywc-docker-isolate/` 신규 생성
- `SKILL.md`, README locale set, `agents/openai.yaml`, references, shell scripts 추가
- source path `tools/codex-skill/skills/...`를 이 repository의 `codex/skills/...` 또는 installed `${CODEX_HOME}` path로 조정
- shell script syntax와 executable mode 검증

## Spec Reference

### Primary Sources

- `docs/ywc-plans/codex-pr110-120-129-port.md#fr-1-add-ywc-docker-isolate` - 신규 Docker isolate skill package 요구사항
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac1---docker-isolate-package-exists` - package file acceptance criteria
- `docs/ywc-plans/codex-pr110-120-129-port.md#ac2---docker-scripts-validate` - script syntax와 executable mode acceptance criteria

### Summary

이 task는 source PR #110의 Codex package를 현재 repository의 `codex/skills/` layout으로 port한다. Codex skill은 `agents/openai.yaml`과 README locale set을 반드시 포함해야 하며, source repo의 `tools/codex-skill` path는 runtime text에 남기면 안 된다. Parallel executor hook 연결은 이 task의 output을 사용하는 별도 task에서 수행한다.

### Out of Scope (from spec)

- `codex/skills/ywc-parallel-executor/SKILL.md` hook 연결 - handled by `000004-010-infra-parallel-docker-hooks`
- `codex/skills/README.md` catalog update와 `.codex-plugin/skills` sync - handled by `000005-010-infra-codex-package-validation`
- Claude Code files under `claude-code/**` - out of scope entirely

## Dependencies

### Depends On

- (None - root task)

### Depended By

- `000004-010-infra-parallel-docker-hooks` - Docker audit/setup/teardown hooks call this skill
- `000005-010-infra-codex-package-validation` - final package validation installs and syncs this skill

## Key Files

- `codex/skills/ywc-docker-isolate/SKILL.md` - Codex skill instructions
- `codex/skills/ywc-docker-isolate/README.md` - Korean usage guide
- `codex/skills/ywc-docker-isolate/README.en.md` - English source usage guide
- `codex/skills/ywc-docker-isolate/README.ja.md` - Japanese usage guide
- `codex/skills/ywc-docker-isolate/README.ko.md` - Korean locale usage guide
- `codex/skills/ywc-docker-isolate/agents/openai.yaml` - Codex UI metadata
- `codex/skills/ywc-docker-isolate/references/port-allocation.md` - port allocation reference
- `codex/skills/ywc-docker-isolate/references/preconditions.md` - precondition reference
- `codex/skills/ywc-docker-isolate/scripts/_lib.sh` - shared script helpers
- `codex/skills/ywc-docker-isolate/scripts/audit-docker-stacks.sh` - stale Docker stack audit
- `codex/skills/ywc-docker-isolate/scripts/setup-docker-ports.sh` - per-task port setup
- `codex/skills/ywc-docker-isolate/scripts/teardown-docker.sh` - per-task teardown

## Notes

- Preserve source PR behavior, but adapt paths to this repository.
- Keep Codex `SKILL.md` frontmatter limited to `name` and `description`.
- Do not run `.codex-plugin` sync in this task unless needed for local verification; the generated package copy is owned by the final validation task.

## Parallel Execution Metadata

### Ownership

- `codex/skills/ywc-docker-isolate/**`

### Shared Surfaces

- Codex skill install contract: `codex/skills/<skill-name>/SKILL.md`, README locale set, `agents/openai.yaml`
- Shell executable mode validation for `codex/skills/**/*.sh`

### Conflicts With

- (None identified)

### Parallelizable After

- (Root task - no predecessor required)

### Task Verify

- `find codex/skills/ywc-docker-isolate -maxdepth 3 -type f | sort`
- `bash -n codex/skills/ywc-docker-isolate/scripts/*.sh`
- `find codex/skills/ywc-docker-isolate/scripts -type f -perm -111 | sort`
- `rg -n 'tools/codex-skill|requires:|version:|category:' codex/skills/ywc-docker-isolate && exit 1 || true`

## Out of Scope

- Changing any existing executor behavior
- Updating root release files
- Adding Codex custom agent TOML files
