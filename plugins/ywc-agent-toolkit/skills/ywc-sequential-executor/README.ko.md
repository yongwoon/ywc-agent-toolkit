# ywc-sequential-executor

이 문서는 Codex `ywc-sequential-executor` workflow 안내입니다. 정확한 trigger, anti-trigger, 실행 절차, output format은 [SKILL.md](./SKILL.md)를 기준으로 합니다.

## Localized Versions

- [한국어](./README.md)
- [English](./README.en.md)
- [日本語](./README.ja.md)

## 사용 시나리오

- 사용자가 이 Skill의 trigger phrase 또는 동등한 자연어 request를 입력할 때
- Codex가 작업 전에 Skill별 workflow와 validation criteria를 맞춰야 할 때
- 다른 `ywc-*` Skill이 이 Skill을 upstream 또는 downstream step으로 참조할 때

## 사용 방법

```bash
$ywc-sequential-executor
```

지원 option과 mode는 [SKILL.md](./SKILL.md)의 Arguments 또는 Workflow section을 따릅니다.

### 주요 Mode

- `--aggregate-pr`: range의 각 task를 별도 feature branch에서 실행하되 하나의 work branch에 local merge로 누적하고, 마지막에 work -> base PR 하나로 delivery합니다.
- `--group-name <name>`: `--aggregate-pr`에서 work branch 이름을 `work/<name>`으로 고정합니다.
- `--worktree`: 전체 sequential invocation을 main checkout 밖의 단일 run worktree에서 실행합니다. Delivery mode가 아니므로 다른 mode flag와 조합할 수 있습니다.
- Stale `.ywc-run-state.json` guard: 저장된 run-state가 현재 명시 range와 맞지 않으면 자동 resume하지 않고, 저장된 run-state를 이어갈지 삭제 후 새 run으로 시작할지 선택을 요구합니다.

## Contract / TDD baseline

동작 변경 task는 구현 전에 changed public contracts와 critical internals를 기록하고, failing test 또는 contract assertion을 먼저 확인합니다. docs-only, config-only, mechanical, no-harness 경우는 명시적인 TDD exception으로 보고합니다. Completion report에는 changed contracts, contract tests, critical internals, exceptions가 포함됩니다.

```bash
$ywc-sequential-executor 001010..003020 --aggregate-pr --group-name billing-rollout
```

```bash
$ywc-sequential-executor 001010..003020 --worktree --pr-lang ko
```

## 출력

이 Skill은 [SKILL.md](./SKILL.md)에 정의된 report, artifact, status format을 따릅니다. Completion Status를 출력하는 Skill은 `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT` 의미를 유지합니다.
