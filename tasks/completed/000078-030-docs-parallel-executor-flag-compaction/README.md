# 000078-030-docs-parallel-executor-flag-compaction

## Purpose

`ywc-parallel-executor`가 자동으로 호출하는 `ywc-impl-review` 2개 지점에 `--non-interactive`를 전파하고, 이 repo의 executor 중 fan-out 폭이 가장 넓음에도 유일하게 부재한 compaction 문단을 신설한다.

## Scope

- FR-3(부분): `:264` Step 4d 코드블록과 `:257` critical-path 강제 호출 2곳에 `--non-interactive` 부착.
- FR-6: Checkpoint and Resume section(`:142-144`) 직후에 compaction 문단 신설.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#fr-3-자동-호출-caller-7곳의-flag-전파` — parallel 2행
- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#fr-6-ywc-parallel-executor-compaction-문단-신설`
- `claude-code/skills/ywc-sequential-executor/SKILL.md` `:155` — 재사용할 compaction 문형의 출처 (읽기 전용)

### Summary

`ywc-parallel-executor`는 `.ywc-run-state.json`을 durable record로 규정하지만 compaction 문단이 없다(grep 확인). 반면 `ywc-sequential-executor:155`와 `ywc-agentic:208`에는 이미 존재한다. 새 mechanism을 발명하지 않고 sequential의 문형을 그대로 재사용해, `.ywc-run-state.json`과 각 task의 `tasks/completed/<id>/` artifact를 source of truth로 삼고 완료 wave당 1줄 digest만 작업 context에 유지하도록 규정한다. 문단은 **advisory**이며 새 stop condition을 도입하지 않는다. 동시에 이 skill이 자동 호출하는 impl-review 2개 지점 — `--review` 시의 Step 4d와 `--review` 여부와 무관한 critical-path 강제 호출(upstream spec 누락 지점) — 에 flag를 부착한다.

### Out of Scope (from spec)

- chars/4 크기 신호 병기 — 근거로 삼을 `ywc-agent-legibility-audit` skill이 본 repo의 48개 `ywc-*` skill 중 **부재**하므로 재사용할 표기 관례가 없다. 새 heuristic을 발명하지 않는다.
- `.ywc-run-state.json` schema 변경, checkpoint/resume mechanics 변경.
- delivery-mode 선택 질문 — 유일한 unattended caller인 `ywc-agentic`이 Step 5에서 mode를 항상 명시 전달하므로 hang 경로가 성립하지 않는다.
- `/ywc-security-audit` 호출 — 해당 skill에 이 flag가 없다.
- `ywc-parallel-executor`용 `--non-interactive` flag 신설 — 이 skill은 이 flag를 **갖지 않는다**. 전파만 한다.

## Criticality

`normal` — skill의 prompt 문서만 수정한다. compaction 문단은 advisory이며 실행 권한이나 stop condition을 변경하지 않는다 (spec §Critical Surfaces).

## Dependencies

### Depends On

- `000078-010-docs-impl-review-bounded-payload-noninteractive` — `ywc-impl-review --non-interactive` flag가 실재해야 이 skill의 2개 호출 지점이 유효한 명령을 가리킨다

### Depended By

- `000079-010-infra-context-safety-validation` — AC7(2/7건), AC14 검증 대상

## Key Files

- `claude-code/skills/ywc-parallel-executor/SKILL.md` — `:142-144` 직후 compaction 문단 신설, `:264` / `:257` 호출에 flag 부착

## Notes

- **`ywc-parallel-executor`에는 `--non-interactive` flag를 만들지 않는다.** 이 skill은 impl-review 호출에 flag를 **전파**만 한다 (FR-4는 sequential 전용).
- `:257`은 `--review` 여부와 무관하게 `/ywc-impl-review` **및** `/ywc-security-audit`을 강제 호출한다. **impl-review 호출에만** flag를 부착한다. upstream spec이 누락했던 지점이다.
- `:264`는 코드블록이므로 리터럴 `--non-interactive`를 명령 끝에 추가한다.
- compaction 문단은 `ywc-sequential-executor:155`의 **문형을 재사용**한다 — 새 mechanism·새 표기·새 임계값을 만들지 않는다. sequential은 `~30+ tasks` trigger를 쓰지만, parallel의 단위는 task가 아니라 **완료 wave**다.
- 문단에 **advisory**이며 새 stop condition을 도입하지 않음을 문장으로 명시해야 한다 (AC14).
- 이 skill은 README 갱신 대상이 아니다 — 신설 flag가 없으므로 FR-7 범위 밖.
- 본문 편집은 **영문**이다.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-parallel-executor/SKILL.md`

### Shared Surfaces

- `--non-interactive` flag 의미 계약 — `000078-010`이 정의, 이 task는 소비만 한다
- `claude-code/skills/ywc-sequential-executor/SKILL.md:155` — **읽기 전용**. compaction 문형의 출처이며 이 task는 수정하지 않는다
- `.ywc-run-state.json` — 문서 참조만. schema 무변경
- CI gates: `scripts/validate.sh`, `markdownlint.yml`, `score.py --ci`

### Conflicts With

- (None identified) — `000078-020` 이 소유하는 `ywc-sequential-executor/**` 를 읽기만 하므로 편집 충돌 없음

### Parallelizable After

- `000078-010-docs-impl-review-bounded-payload-noninteractive`

### Task Verify

- `grep -rnE "ywc-impl-review[^|]*--non-interactive" claude-code/skills/ywc-parallel-executor/SKILL.md | wc -l` — **2** (`:264`, `:257`)
- `grep -ci "compaction" claude-code/skills/ywc-parallel-executor/SKILL.md` — ≥ 1 (현재 0)
- `grep -ci "advisory" claude-code/skills/ywc-parallel-executor/SKILL.md` — 신설 문단에서 ≥ 1
- `git diff -- claude-code/skills/ywc-parallel-executor/SKILL.md` 에 새 stop condition 이 추가되지 않았음을 육안 확인
- `git diff --name-only | grep -c 'ywc-sequential-executor'` — 0 (이 task는 sequential 파일을 수정하지 않는다)

## Out of Scope

- `ywc-sequential-executor` / `ywc-impl-review` / `ywc-code-gen` / `ywc-agentic` 파일 수정 — 각각 다른 task 소유.
- `ywc-parallel-executor` README 갱신 — 신설 flag가 없으므로 FR-7 범위 밖.
- chars/4 등 새 크기 신호 도입.
- `codex/**` 하위 모든 파일 (AC17).
- mechanical score baseline 재생성 — `000079-010`이 담당.
