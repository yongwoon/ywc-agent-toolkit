# ywc-parallel-executor (Parallel Executor)

task-generator 가 생성한 Task 를 Agent 가 병렬로 실행하는 Skill 입니다. dependency-graph.md 를 분석하여 Wave 기반 병렬 실행 + Git Worktree 격리를 수행합니다.

## 사용 방법

```text
/ywc-parallel-executor 000001-010-db-create-events           # 단일 Task
/ywc-parallel-executor 000001-010..000002-040                     # 범위 지정 (병렬)
/ywc-parallel-executor --all                              # 전체 실행
/ywc-parallel-executor 000001-010..000002-040 --review            # 병렬 + 자동 Review
/ywc-parallel-executor 000001-010..000002-040 --local-merge       # PR 없이 Local merge
/ywc-parallel-executor 000001-010..000002-040 --draft             # Draft PR 생성
```

## Option

| Option | 설명 |
|--------|------|
| `--tasks-dir <path>` | Tasks directory 경로 (default: tasks/) |
| `--review` | 각 Task 완료 후 /ywc-impl-review 자동 실행 (조합 가능) |
| `--local-merge` | PR 없음, base-branch push 만 (기본 동작) |
| `--draft` | 전체 완료 후 Draft PR 생성 |
| `--per-task-pr` | Task 마다 개별 PR 생성 |

## 실행 흐름

1. dependency-graph.md 파싱
2. Wave 계획 수립 (Topological Sort)
3. Wave 단위 실행: Worktree 생성 → Agent 병렬 실행 → Merge → Worktree 삭제

## Task → Agent 자동 매핑

| Category | Agent |
|----------|-------|
| db, api, domain, lib, worker | Backend Agent (sonnet) |
| ui | Frontend Agent (sonnet) |
| test | QA Agent (sonnet) |
| infra | DevOps Agent (sonnet) |
| refactor | Reviewer Agent (opus) |

Agent Hint 로 Override 가능:
```markdown
## Parallel Execution Metadata
- Agent Hint: frontend
```

## sequential-executor 와의 비교

| 상황 | 권장 도구 |
|------|----------|
| 소규모 작업 (1-3 Task) | sequential-executor |
| 순차 의존성이 강한 작업 | sequential-executor |
| 대규모 작업 (4+ Task) | /ywc-parallel-executor |
| 병렬 가능한 Task 가 많은 경우 | /ywc-parallel-executor |

## Triggering

이 Skill 의 Trigger 조건은 [SKILL.md](./SKILL.md) 의 `description` 필드에 정의되어 있습니다.

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
