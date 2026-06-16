# ywc-parallel-executor

이 Skill은 Codex에서 `ywc-parallel-executor` workflow가 필요할 때 사용하는 안내 문서입니다. 정확한 trigger, anti-trigger, 실행 절차, output format은 [SKILL.md](./SKILL.md)를 기준으로 합니다.

## Localized Versions

- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어 full](./README.ko.md)
- [Español](./README.es.md)
- [中文](./README.zh.md)

## 사용 시나리오

- 사용자가 이 Skill의 trigger phrase 또는 동등한 자연어 request를 입력할 때
- Codex가 작업 전에 Skill별 workflow와 validation criteria를 맞춰야 할 때
- 다른 `ywc-*` Skill이 이 Skill을 upstream 또는 downstream step으로 참조할 때

## 사용 방법

```bash
$ywc-parallel-executor
```

지원 option과 mode는 [SKILL.md](./SKILL.md)의 Arguments 또는 Workflow section을 따릅니다.

## Docker Isolation

Docker Compose를 사용하는 task worktree에서는 executor가 `ywc-docker-isolate`에 port isolation을 위임합니다. Worktree 생성 전 selected task stack을 audit하고, 각 worktree 검증 후 task별 deterministic port를 setup하며, 성공한 task는 worktree prune 전에 stack을 teardown합니다. `BLOCKED` 또는 preserved worktree는 복구를 위해 Docker state를 유지합니다.

## Delivery Modes

| Mode | 동작 |
|---|---|
| `--local-merge` | 각 task를 base branch에 local merge하고 즉시 push합니다. PR은 만들지 않습니다. |
| `--draft` | 각 task를 local merge로 누적한 뒤, 마지막에 aggregate draft PR을 생성합니다. |
| `--per-task-pr` | 각 task마다 PR 생성, CI 대기, bot review 대응, 최신 base refresh, PR merge, base sync, Mark Complete까지 수행합니다. |
| `--aggregate-pr` | invocation 전체를 하나의 aggregate branch와 PR로 묶고, ready → CI → bot review → merge까지 완료합니다. |

`--per-task-pr`에서는 같은 wave의 앞선 task가 base branch를 전진시킬 수 있습니다. 따라서 merge 직전에 PR branch가 최신 base를 포함하는지 확인하고, 뒤처져 있으면 worktree branch에 base를 merge한 뒤 push하고 CI를 다시 확인합니다. Base refresh conflict는 `BLOCKED`로 보고하며, 오래된 head SHA의 CI 결과만으로 PR을 merge하지 않습니다.

## Group 실행

`--aggregate-pr --group-name <name>`은 많은 task를 group 단위 단일 PR로 delivery할 때 사용합니다. 여러 group을 동시에 실행하려면 worktree가 아니라 group당 독립 clone을 사용하는 것이 안전합니다. 자세한 절차와 동시성 규칙은 [references/aggregate-pr.md](./references/aggregate-pr.md)를 기준으로 합니다.

## 출력

이 Skill은 [SKILL.md](./SKILL.md)에 정의된 report, artifact, status format을 따릅니다. Completion Status를 출력하는 Skill은 `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT` 의미를 유지합니다.
