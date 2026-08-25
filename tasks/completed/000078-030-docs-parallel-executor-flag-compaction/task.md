# 000078-030-docs-parallel-executor-flag-compaction — Implementation Checklist

## Prerequisites

- [ ] `000078-010-docs-impl-review-bounded-payload-noninteractive` 가 완료(merge)되었고 `ywc-impl-review` 의 Arguments 표에 `--non-interactive` 행이 존재한다
- [ ] `claude-code/skills/ywc-sequential-executor/SKILL.md:155` 의 compaction 문단 원문을 읽고 문형을 파악했다
- [ ] `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md` FR-3 / FR-6 을 읽었다

## Allowed Edit Scope

- [ ] `claude-code/skills/ywc-parallel-executor/SKILL.md` 만 편집한다
- [ ] `ywc-sequential-executor/SKILL.md` 는 **읽기만** 한다 (`000078-020` 소유)
- [ ] Ownership 밖 편집이 필요하면 중단하고 보고한다

## Stop Conditions

- [ ] Checkpoint and Resume section(`:142-144`)의 위치를 특정할 수 없으면 중단
- [ ] compaction 문단이 새 stop condition을 요구한다고 판단되면 중단 (AC14 위반)
- [ ] `ywc-parallel-executor` 자체에 `--non-interactive` flag를 신설해야 한다고 판단되면 중단 (범위 밖 — 이 skill은 전파만 한다)
- [ ] chars/4 등 새 크기 신호를 도입해야 한다고 판단되면 중단 (Out of Scope)

## Implementation Steps

- [ ] **FR-3(부분) — impl-review 호출 2곳에 flag 부착**
  - [ ] `:264` Step 4d 코드블록: `/ywc-impl-review --spec <task-spec-path> --git-range <base-branch>..feature/<task-name>` 끝에 리터럴 `--non-interactive` 를 추가한다
  - [ ] `:257` critical-path 강제 호출: `/ywc-impl-review` 에만 flag를 부착한다. `/ywc-security-audit` 에는 부착하지 않는다
  - [ ] 두 지점의 status routing 문단(`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`)은 변경하지 않는다
- [ ] **FR-6 — compaction 문단 신설** (`:142-144` Checkpoint and Resume 직후)
  - [ ] `.ywc-run-state.json` 과 각 task의 `tasks/completed/<id>/` artifact 를 source of truth로 삼는다고 명시한다
  - [ ] 완료 **wave 당 1줄 digest** 만 작업 context에 유지하고 세부는 필요 시 재독한다고 규정한다 (sequential의 단위는 task, parallel의 단위는 wave)
  - [ ] `ywc-sequential-executor:155` 의 문형을 재사용한다 — 새 mechanism·새 표기·새 임계값을 만들지 않는다
  - [ ] 문단이 **advisory** 이며 **새 stop condition을 도입하지 않음**을 문장으로 명시한다
  - [ ] chars/4 크기 신호는 넣지 않는다
- [ ] **경계 확인**
  - [ ] `ywc-parallel-executor` README 는 수정하지 않는다 (신설 flag가 없으므로 FR-7 범위 밖)
  - [ ] `.ywc-run-state.json` schema 및 checkpoint/resume mechanics 서술을 변경하지 않는다

## Task Verify

- [ ] `grep -rnE "ywc-impl-review[^|]*--non-interactive" claude-code/skills/ywc-parallel-executor/SKILL.md | wc -l` — **2**
- [ ] `grep -ci "compaction" claude-code/skills/ywc-parallel-executor/SKILL.md` — ≥ 1 (현재 0)
- [ ] `grep -ci "advisory" claude-code/skills/ywc-parallel-executor/SKILL.md` — 신설 문단에서 ≥ 1
- [ ] `git diff --name-only` 에 `ywc-sequential-executor` 경로가 **없음**
- [ ] `git diff -- claude-code/skills/ywc-parallel-executor/SKILL.md` 에 새 stop condition / `.ywc-run-state.json` schema 변경 / README 변경이 없음을 육안 확인

## Verification

- [ ] `bash scripts/validate.sh` 통과
- [ ] markdownlint 통과 — `.github/workflows/markdownlint.yml` 의 실제 invocation 형태를 재현한다
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --format json` 으로 read-only 확인
- [ ] `git diff --name-only | grep -c '^codex/'` — 0 (AC17)

## Implementation Notes
