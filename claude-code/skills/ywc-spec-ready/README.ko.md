# ywc-spec-ready (Spec Readiness Loop)

`ywc-plan` 이 만든 spec 을 `ywc-spec-validate` `DONE` 상태까지 자동으로 수렴시키는 Skill 입니다. 매 iteration 마다 `ywc-spec-validate` 를 실행하고, `DONE_WITH_CONCERNS` 면 `ywc-plan --update-spec` 으로 amendment 를 추가한 뒤 재검증합니다. `DONE` 도달 시 `ywc-task-generator` handoff 안내만 출력하고 **정지**합니다 (task-generator 자동 실행 안 함).

```text
spec ──> [ywc-spec-validate ──DONE_WITH_CONCERNS──> ywc-plan --update-spec]* ──DONE──> handoff
```

기존 `ywc-agentic` 의 loop 은 `ywc-impl-review`(코드 평가) 중심으로 돌며 `ywc-spec-validate` 를 **단 1회**만 실행합니다. 이 Skill 은 그 빠진 inner loop — **다회 spec 수렴** — 을 담당합니다.

## 사용 방법

```text
/ywc-spec-ready --spec docs/ywc-plans/feature.md                       # 기본 (max 5 iteration)
/ywc-spec-ready --spec docs/ywc-plans/feature.md --max-iterations 8    # 반복 한도 지정
/ywc-spec-ready --spec docs/ywc-plans/feature.md --max-advisor-calls 2 # advisor 비용 가드
/ywc-spec-ready --spec docs/ywc-plans/feature.md --dry-run             # 명령 시퀀스만 출력
```

## Option

| Option                   | 설명                                                              |
| ------------------------ | --------------------------------------------------------------- |
| `--spec <path>`          | 수렴 대상 spec 파일 (필수, `ywc-plan` 산출물). 부재 시 `NEEDS_CONTEXT` |
| `--max-iterations <n>`   | Validation loop 한도 (default: 5, 자동 증가하지 않는 안전 밸브)     |
| `--max-advisor-calls <n>`| 전체 iteration 누적 Opus advisor budget (default: 4, cost guard)  |
| `--log <path>`           | append-only loop 로그 (default: `<spec-dir>/<slug>.spec-ready-log.md`) |
| `--dry-run`              | 계획된 명령 시퀀스만 출력, sibling skill 미호출                    |
| `--lang <lang>`          | Report/handoff 언어 (default: auto, CLAUDE.md 에서 추론)          |
| `--focus <area>`         | `ywc-spec-validate` 로 전달                                       |
| `--format <fmt>`         | `ywc-spec-validate` 로 전달 (markdown / html)                     |
| `--terse`                | 최소 출력 (phase header 와 최종 report 만)                        |

## 실행 흐름

1. Pre-flight — `--spec` 존재 검증, `<slug>` 도출, `--dry-run` 분기
2. Iteration Loop — `ywc-spec-validate` → Status Routing → (DONE_WITH_CONCERNS 시) guard 평가 → `ywc-plan --update-spec` → 로그 → 반복
3. Hard Stop — `BLOCKED` / `NEEDS_CONTEXT` / `SOCRATIC` / 파싱불가 시 즉시 정지
4. Handoff — `DONE` 도달 시 `ywc-task-generator` 안내 출력 후 정지
5. Completion Report — 단일 보고 (마지막 줄 Completion Status)

## 무한 loop 방지 가드

| 가드 | 정지 조건 |
| --- | --- |
| Iteration cap | `iteration >= --max-iterations` 이고 status ≠ DONE |
| 비감소 Critical | Critical 증가 또는 2 연속 iteration 비감소(signature overlap) |
| 동일 signature 재출현 | 동일 Critical signature 가 re-plan 후 연속 출현 |
| 동일 amendment scope | 새 amendment scope 가 직전과 동일 (recursion guard) |

자세한 규칙은 [references/convergence.md](references/convergence.md), 로그 schema 는 [references/loop-log.md](references/loop-log.md) 참조.

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
