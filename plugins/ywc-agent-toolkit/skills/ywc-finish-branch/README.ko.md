# ywc-finish-branch

Feature Branch를 Base Branch에 전달(deliver)하는 Codex Skill입니다. Mark-PR-ready, CI Wait + Bot Review Polling, Merge (PR 또는 Local), Post-Merge Verification, Mark Task Complete, Local Branch Cleanup을 한 번의 호출로 처리합니다.

## 개요

`ywc-sequential-executor`와 `ywc-parallel-executor`가 각자 inline으로 가지고 있던 delivery 로직을 분리한 단일 책임 Skill입니다. 하나의 Feature Branch, 하나의 Task에 대해 verification이 끝난 시점부터 "done" 상태까지의 전체 흐름을 담당합니다.

### 주요 특징

- **Mode 분기 1곳에서 처리**: `normal-pr` / `local-merge` / `draft` / `skip-ci-wait` / `per-task-pr`
- **Post-merge Hard Gate**: `git log -1 --format="%s"`로 merge 실제 실행 여부 검증
- **Mark Task Complete의 Definition of Done 강제**: `<tasks-dir>/completed/`로의 이동을 verification까지 수행
- **Bot Review Polling 호환**: `--bot-action sequential|parallel`로 caller 환경에 맞는 polling 동작 선택
- **Worktree-path mode**: `--worktree-path <path>` 로 sequential run-level worktree 안에서 `git -C <path>` 기준 delivery를 수행하고, 생성/삭제는 caller가 유지

## 사용 방법

### 기본 사용 (PR-based)

```
/ywc-finish-branch --mode normal-pr --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch develop
```

### Local Merge

```
/ywc-finish-branch --mode local-merge --branch feature/000001-010-db-create-users \
  --task-name 000001-010-db-create-users --base-branch main
```

### Range 모드에서 push 지연

```
/ywc-finish-branch --mode normal-pr --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --defer-push
```

### Worktree path mode

```
/ywc-finish-branch --mode local-merge --branch feature/<task-name> \
  --task-name <task-name> --base-branch develop --worktree-path ../worktree-run
```

### 자연어 호출

```
"finish branch"
"deliver this branch"
"branch 마무리"
"ブランチ完了"
```

## Mode 비교

| Mode | PR | CI 대기 | Merge | Mark Complete | Cleanup |
| --- | --- | --- | --- | --- | --- |
| `normal-pr` | yes (`ywc-create-pr` 위임) | yes | `gh pr merge --delete-branch` | yes | `git branch -d` |
| `local-merge` | no | no | `git merge --no-ff` + push | yes | yes |
| `draft` | yes | no | no | no | no |
| `skip-ci-wait` | yes (mark ready) | no | no | no | no |
| `per-task-pr` | yes | no | no | no | no |

## 전제 조건

- `gh` CLI 설치 및 인증 완료 (PR-based 모드)
- Working tree clean
- 호출자가 verification gate (lint / typecheck / test)를 이미 통과했음
- Pre-authorization 설정 완료 (`Codex approval settings or the project-local policy file` — `references/local-merge-permissions.md` 참고)

## 사용 Tool

`Bash`, `Read`, `Grep`, Task (`ywc-create-pr` / `ywc-handle-pr-reviews` 위임)

## 호출 관계

- **Upstream**: `ywc-sequential-executor` (Steps 5–8 위임), `ywc-parallel-executor` (Step 4e–4f 일부 위임)
- **Internal delegation**: `ywc-create-pr` (Step 2), `ywc-handle-pr-reviews` (Step 4 bot polling 내부)
