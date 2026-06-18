# ywc-parallel-executor (Parallel Executor)

task-generator 가 생성한 Task 를 Agent 가 병렬로 실행하는 Skill 입니다. dependency-graph.md 를 분석하여 Wave 기반 병렬 실행 + Git Worktree 격리를 수행합니다.

## Test-first, Deep Module, Critical Module Review

worker payload 에 interface-first directive 와 test-first-where-feasible directive 를 주입합니다: behavior change task 는 구현 전에 실패하는 test 를 먼저 작성하고(docs/config/mechanical 은 예외), public surface 는 body 보다 먼저 설계합니다(deep module). Task 의 Ownership 이 critical path(auth, payment, crypto, PII, external input)에 해당하면 `--review` 없이도 4d 에서 `/ywc-impl-review` 와 `/ywc-security-audit` 를 강제합니다. 자세한 내용은 `../references/tdd-deep-module-gray-box.md` 를 참고하세요.

## 사용 방법

```text
/ywc-parallel-executor 000001-010-db-create-events           # 단일 Task
/ywc-parallel-executor 000001-010..000002-040                     # 범위 지정 (병렬)
/ywc-parallel-executor --all                              # 전체 실행
/ywc-parallel-executor 000001-010..000002-040 --review            # 병렬 + 자동 Review
/ywc-parallel-executor 000001-010..000002-040 --local-merge       # PR 없이 Local merge
/ywc-parallel-executor 000001-010..000002-040 --draft             # Draft PR 생성 (사람이 나중에 merge)
/ywc-parallel-executor 000001-010..000002-040 --per-task-pr       # Task 마다 PR 생성·CI·review·merge
/ywc-parallel-executor 000026-010..000026-030 --aggregate-pr --group-name payments --pr-lang ko  # Group 단위 단일 PR
```

## Option

| Option | 설명 |
|--------|------|
| `--tasks-dir <path>` | Tasks directory 경로 (default: tasks/) |
| `--pr-lang <lang>` | 최종 PR (`--aggregate-pr`) title/description 언어 (default: auto-detect) |
| `--review` | 각 Task 완료 후 /ywc-impl-review 자동 실행 (조합 가능) |
| `--local-merge` | PR 없음, base-branch 로 직접 merge + push |
| `--draft` | 전체 완료 후 단일 Draft PR 생성 (open 상태로 두고 사람이 merge) |
| `--per-task-pr` | Task 마다 PR 생성 → CI 대기 → bot review 대응 → merge 까지 수행 (sequential-executor default 와 동일한 full lifecycle) |
| `--aggregate-pr` | Invocation 전체 → branch 1개 + PR 1개. Task 는 여전히 병렬(Wave)로 실행되어 단일 aggregate branch 에 누적되고, 마지막에 ready → CI → bot review → **merge** 까지 수행 (`--draft` 의 full-lifecycle 판본) |
| `--group-name <name>` | aggregate branch 이름(`aggregate/<name>`) 지정 + 동시 group 구분. `--aggregate-pr` 전용, 생략 시 `aggregate/<base-branch>-<timestamp>` |

> Mode 미지정 시 기본값은 없습니다. `--local-merge` / `--draft` / `--per-task-pr` / `--aggregate-pr` 중 하나를 사용자가 명시적으로 선택해야 합니다. 4종은 상호 배타적입니다.

## Group 단위 실행 (`--aggregate-pr`)

많은 Task 를 **group 으로 묶어 group 당 PR 1개**로 delivery 하고, 필요하면 **group 간 병렬**로 진행하려는 경우 `--aggregate-pr` 를 사용합니다.

**핵심 개념**: 한 invocation = 한 group = 한 PR. Group **내부**의 Task 들은 Wave 기반으로 병렬 실행되며, 각 Task 의 변경과 `chore: mark ... as completed` marker commit 이 단일 aggregate branch 에 누적됩니다. 모든 Wave 가 끝나면 그 branch 로 단일 PR 을 열어 ready → CI → bot review → merge-readiness gate → merge → base sync 까지 한 번에 수행합니다. marker commit 이 이미 branch 에 있으므로 merge 후 별도 Mark Complete 는 없습니다.

### 단일 Group

```text
/ywc-parallel-executor 000026-010..000026-030 --aggregate-pr --group-name payments --review --pr-lang ko
```

- `--review`: 각 Task 의 worktree branch 가 aggregate 에 합류하기 전 `/ywc-impl-review` 로 gate
- `--pr-lang ko`: PR title/description 언어 고정
- 실행 전 `--dry-run` 으로 Wave 계획(Task 순서·의존성·mode)을 미리 확인하는 것을 권장합니다.

### Group 간 병렬 (동시 실행)

동시에 여러 group 을 돌리려면 **group 당 1 clone**(독립 `.git`)으로 격리해야 합니다. `--aggregate-pr` 는 local `<base>` branch 에 직접 누적(`git reset --hard origin/<base>` + per-task merge)하므로, 두 group 이 같은 `<base>` 를 동시에 건드리면 서로의 누적을 덮어씁니다. **git worktree 로 나눠도** working tree 와 untracked `.ywc-run-state.json` 만 분리될 뿐 `.git` 의 refs(특히 local `<base>` branch)는 worktree 간 공유되어 ref layer 에서 여전히 충돌하므로, worktree 는 격리 경계가 되지 못합니다.

```bash
git clone <repo-url> ../grp-payments && \
  ( cd ../grp-payments && /ywc-parallel-executor 000026-010..000026-030 \
      --aggregate-pr --group-name payments --review --pr-lang ko ) &

git clone <repo-url> ../grp-search && \
  ( cd ../grp-search && /ywc-parallel-executor 000027-010..000027-040 \
      --aggregate-pr --group-name search --review --pr-lang ko ) &

wait
```

추가 clone 없이 한 repo 에서 처리하려면 group 을 **순차로 back-to-back** 실행합니다 (각 group 내부는 여전히 병렬):

```bash
/ywc-parallel-executor 000026-010..000026-030 --aggregate-pr --group-name payments --pr-lang ko
/ywc-parallel-executor 000027-010..000027-040 --aggregate-pr --group-name search   --pr-lang ko
```

자세한 절차·동시성 안전 규칙은 [references/aggregate-pr.md](./references/aggregate-pr.md) 를 참고하십시오.

## 실행 흐름

1. dependency-graph.md 파싱
2. Wave 계획 수립 (Topological Sort)
3. Wave 단위 실행: Worktree 생성 → Agent 병렬 실행 → 검증(Task Verify + 전체/영향범위 회귀 suite + Ownership scope gate) → Merge → Worktree 삭제

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
