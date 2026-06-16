# ywc-agentic (Agentic Orchestrator)

자연어 목표 하나를 입력받아 기존 `ywc-*` skill 들을 자율적으로 오케스트레이션하여 코드 구현까지 완료하는 Skill 입니다. **Plan → Execute → Evaluate → Repeat** loop 를 통해 `ywc-impl-review` 평가를 통과하거나 사용자가 정한 반복 한도에 도달할 때까지 재계획을 반복합니다.

```text
User → Goal → Agent [Plan → Execute → Evaluate → Repeat] → Result
```

## 사용 방법

```text
/ywc-agentic "사용자 인증 API 구현"                        # 자연어 목표 입력
/ywc-agentic --goal "검색 기능 추가" --max-iterations 5     # 최대 반복 횟수 지정
/ywc-agentic "결제 모듈 구현" --executor parallel           # Executor 강제 지정
/ywc-agentic "리팩토링 작업" --resume                       # 기존 tasks/ 에서 재개
/ywc-agentic "목표" --dry-run                               # 단계 계획만 출력
```

## Option

| Option                 | 설명                                                             |
| ---------------------- | ---------------------------------------------------------------- |
| `<goal>`               | 달성할 목표의 자연어 설명 (positional, 필수)                     |
| `--goal <text>`        | positional `<goal>` 의 대안 (둘 다 지정 시 positional 우선)      |
| `--max-iterations <n>` | 최대 loop 반복 횟수 (default: 3, 자동 증가하지 않는 안전 밸브)   |
| `--executor <mode>`    | Executor 강제 지정: sequential / parallel / auto (default: auto) |
| `--tasks-dir <path>`   | Task directory 및 agentic-log.md 경로 (default: tasks/)          |
| `--resume`             | Plan Phase 를 건너뛰고 기존 tasks/ 에서 재개                     |
| `--dry-run`            | 단계 계획만 출력하고 skill 은 실행하지 않음                      |
| `--terse`              | 최소 출력 (phase header 와 최종 report 만)                       |
| `--pr-lang <lang>`     | PR 제목·설명 언어 (default: auto, CLAUDE.md 에서 추론)           |

## 실행 흐름

1. Goal 수신·검증
2. 프로젝트 컨텍스트 탐지 → Resume / Full Mode 결정
3. Plan Phase — `ywc-plan` 호출 (Re-plan 시 `--update-spec`)
4. Task Phase — `ywc-task-generator` 호출 (Medium/Large 만)
5. Execute Phase — Executor `--local-merge` 실행 (Small Path 는 `ywc-code-gen`)
6. Evaluate Phase — `ywc-impl-review --git-range` 로 원본 spec 대비 평가
7. Loop Control — Pass 종료 / Fail 재계획 / 반복 한도 도달 시 부분 완료 report
8. Iteration Log — `tasks/agentic-log.md` 에 append
9. Completion Report

## Small Path 와 Medium/Large Path

| 경로              | 조건                            | 실행                                                  |
| ----------------- | ------------------------------- | ----------------------------------------------------- |
| Small Path        | `ywc-plan` 이 Small 판정        | `ywc-code-gen` 직접 호출 (Task Phase·Executor 생략)   |
| Medium/Large Path | `ywc-plan` 이 Medium/Large 판정 | `ywc-spec-validate` → `ywc-task-generator` → Executor |

## 오케스트레이션 대상 Skill

`ywc-plan` · `ywc-spec-validate` · `ywc-task-generator` · `ywc-sequential-executor` / `ywc-parallel-executor` · `ywc-impl-review` · `ywc-code-gen`

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
