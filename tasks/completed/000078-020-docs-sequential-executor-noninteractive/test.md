# 000078-020-docs-sequential-executor-noninteractive — Manual Test Plan

spec의 NFR Verification/Testability가 요구하는 수동 transcript 확인 2건 중 sequential executor 측을 담당한다.

## T1 — `--non-interactive` 에서 질문 없이 `deny` 적용, persist 없음 (AC9)

**Steps**

1. `.claude/settings.local.json` 에 `taskExecutor` key가 **없는** 상태를 만든다 (있으면 백업 후 제거).
2. `--dry-run --non-interactive` 조합으로 `ywc-sequential-executor` 를 1회 실행한다.
3. transcript에서 `AskUserQuestion` 호출 횟수를 센다.
4. Completion Report(또는 계획 출력)의 External URL 라인을 확인한다.
5. `.claude/settings.local.json` 을 다시 확인한다.

**Expected Result**

- `AskUserQuestion` 호출 **0회**.
- 출력에 `External URL policy: deny (assumed — non-interactive, not persisted)` 가 존재한다.
- `.claude/settings.local.json` 에 `taskExecutor` key가 **생성되지 않는다**.
- skip된 external URL이 있다면 skip 목록이 log된다.

## T2 — flag 없는 기존 경로가 유지된다 (AC10)

**Steps**

1. `taskExecutor` key가 없는 상태에서 `--non-interactive` **없이** `--dry-run` 으로 1회 실행한다.

**Expected Result**

- 기존대로 `deny` / `allow` / `allowlist` 중 하나를 묻는 질문이 **1회** 열린다.
- 응답 후 값이 `.claude/settings.local.json` 에 persist된다.
- key가 이미 존재하는 상태에서는 mode와 무관하게 질문 없이 그 값을 사용한다.

## T3 — malformed 값 처리 (FR-4c 신규 규칙)

**Steps**

1. `.claude/settings.local.json` 의 `taskExecutor.externalSpecUrls` 에 `"maybe"` 같은 무효 값을 넣는다.
2. `--non-interactive` 로 1회, flag 없이 1회 `--dry-run` 실행한다.

**Expected Result**

- 두 실행 모두 Completion Report에 `External URL policy: malformed value "maybe" — treated as absent for this run` 이 기록된다.
- `--non-interactive` 실행: 질문 없이 `deny` 적용, 파일의 `"maybe"` 값은 **변경되지 않는다**.
- flag 없는 실행: 기존 값이 무효라 교체됨을 **먼저 알린 뒤** 질문한다.

## T4 — delivery mode 조합에서 flag conflict가 발생하지 않는다 (FR-4 orthogonality)

**Steps**

1. `--non-interactive --local-merge --dry-run` 으로 1회 실행한다.
2. `--non-interactive --worktree --review --dry-run` 으로 1회 실행한다.

**Expected Result**

- 두 경우 모두 `flag conflict detected (Pre-flight)` 로 중단되지 않는다.
- `--non-interactive` 가 delivery mode 선택에 영향을 주지 않는다.

## T5 — `allowlist` 가 비어 있는 기존 값 (Edge Case)

**Steps**

1. `taskExecutor.externalSpecUrls` 를 `allowlist` 로 두고 allowlist를 비운다.
2. `--non-interactive --dry-run` 으로 실행한다.

**Expected Result**

- 기존 파일 값이 존재하므로 그 값을 사용한다 (빈 allowlist = 전부 skip).
- `deny` default로 덮어쓰지 않는다.
