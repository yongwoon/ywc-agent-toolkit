# 000078-020-docs-sequential-executor-noninteractive

## Purpose

`ywc-sequential-executor`에 `--non-interactive` flag를 신설해 Pre-flight의 유일한 사용자 응답 대기 지점인 External URL Policy 질문을 문서화된 `deny` default로 대체하고(영속화하지 않음), 이 skill이 자동으로 호출하는 `ywc-impl-review` 2개 지점에 flag를 전파한다.

## Scope

- FR-3(부분): `:337` Step 4.5(`--review`)와 `:341` critical-path 강제 호출 2곳에 `--non-interactive` 부착.
- FR-4: Arguments 표에 flag 추가, External URL Policy를 3분기 + malformed 분기로 확장, Completion Report 라인 신설, delivery-mode 그룹과의 orthogonality 명시.
- FR-7(부분): `ywc-sequential-executor` README 6 locale에 신설 flag 반영 및 기존 External URL 문구와의 정합.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#fr-3-자동-호출-caller-7곳의-flag-전파` — sequential 2행
- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#fr-4-ywc-sequential-executor---non-interactive-external-url-policy`
- `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md#iteration-1-amendments` — FR-4 flag-orthogonality 수정본이 authoritative
- `claude-code/skills/ywc-sequential-executor/references/external-url-policy.md` — `deny` default의 출처 (읽기 전용)

### Summary

현재 `SKILL.md:119`는 `taskExecutor.externalSpecUrls` key가 없으면 사용자에게 `deny`(default) / `allow` / `allowlist` 중 하나를 **1회 묻고 persist**한다. 이것이 sequential executor의 유일한 Pre-flight 질문이며 unattended run을 멈춘다. `--non-interactive`일 때는 질문 없이 `deny`를 적용하되 **파일에 persist하지 않는다** — 가정은 이번 run 한정이고, 사용자가 나중에 interactive 실행에서 진짜 결정을 내릴 수 있어야 하기 때문이다. 여기에 더해 key가 존재하지만 세 값 중 어느 것도 아닐 때의 malformed 분기를 신규 규칙으로 도입한다(이 spec이 도입하는 유일한 신규 규칙). Iteration 1 Amendments에 따라 `--non-interactive`는 `:64`의 4개 delivery mode 상호배타 그룹과 **직교**하며 — `--worktree`와 동일하게 "not a fifth member" — 그 그룹에 추가되지 않는다. 따라서 Pre-flight flag-conflict 검사와 `:196` Allowed Stop Reasons는 무변경이다.

### Out of Scope (from spec)

- `:196` Allowed Stop Reasons 목록 — 이 변경은 stop을 제거하기만 하므로 무변경.
- `/ywc-security-audit` 호출 — 해당 skill에 이 flag가 없으므로 부착하지 않는다.
- `claude-code/skills/references/non-stop-execution.md` — 파일 무수정.
- `:155` compaction 문단 — 이미 존재하며 무변경 (FR-6은 parallel-executor 대상, `000078-030`).
- caller status routing 문단(`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`) — 무변경.
- `ywc-agentic` Step 5의 forward — `000078-040`이 담당.

## Criticality

`normal` — skill의 prompt 문서만 수정한다. `--non-interactive`가 적용하는 `deny`는 기존 default 중 **가장 제한적인** 값이며, 결정을 영속화하지 않으므로 권한을 확대하지 않는다 (spec §Critical Surfaces).

## Dependencies

### Depends On

- `000078-010-docs-impl-review-bounded-payload-noninteractive` — `ywc-impl-review --non-interactive` flag가 실재해야 이 skill의 2개 호출 지점이 유효한 명령을 가리킨다

### Depended By

- `000078-040-docs-code-gen-agentic-propagation` — `ywc-agentic` Step 5가 sequential 선택 시 forward할 flag가 이 task에서 정의된다
- `000079-010-infra-context-safety-validation` — AC7(2/7건), AC9, AC10, AC15 검증 대상

## Key Files

- `claude-code/skills/ywc-sequential-executor/SKILL.md` — Arguments 표 flag 1행, `:119` External URL Policy 3분기 + malformed 분기, Completion Report 라인, `:337` / `:341` 호출에 flag 부착
- `claude-code/skills/ywc-sequential-executor/README.md` — 한국어 기본
- `claude-code/skills/ywc-sequential-executor/README.en.md` — 영어 원본
- `claude-code/skills/ywc-sequential-executor/README.ja.md`
- `claude-code/skills/ywc-sequential-executor/README.ko.md`
- `claude-code/skills/ywc-sequential-executor/README.zh.md`
- `claude-code/skills/ywc-sequential-executor/README.es.md`

## Notes

- **persist 금지가 이 FR의 핵심이다.** AC9의 관측 방법은 실행 후 `.claude/settings.local.json`에 `taskExecutor` key가 **생성되지 않음**을 확인하는 것이다.
- **malformed 값 분기는 신규 규칙이다** — `external-url-policy.md`에 없는 내용이며 이 spec이 도입한다. key 부재와 동일하게 취급하되 **이번 run 한정**이고, malformed 값을 강제 변환하거나 persist하지 않는다. 두 mode 모두 Completion Report에 기록한다. interactive 분기가 재질문할 때는 기존 값이 무효라 교체됨을 **먼저 알린 뒤** 묻는다.
- **`--non-interactive`는 delivery-mode 그룹의 다섯 번째 멤버가 아니다.** `:64`가 정의하는 `--local-merge` / `--draft` / `--skip-ci-wait` / `--aggregate-pr` 상호배타 그룹과 직교하며, `--worktree`와 같은 위치다. 모든 delivery mode 및 `--review` / `--dry-run` / `--worktree`와 조합된다.
- `:341`은 `--review` 여부와 무관하게 `/ywc-impl-review` **및** `/ywc-security-audit`을 강제 호출한다. **impl-review 호출에만** flag를 부착한다. 이 지점은 upstream spec이 누락했던 곳이다.
- `--dry-run`과 조합 시 flag는 계획 출력에 한 줄로 반영되고 별도 동작 변화는 없다.
- 본문 편집은 **영문**이다. 한국어는 `README.md` / `README.ko.md`에만 적용.

## Parallel Execution Metadata

### Ownership

- `claude-code/skills/ywc-sequential-executor/**`

### Shared Surfaces

- `--non-interactive` flag 의미 계약 — `000078-040`(agentic forward)이 소비
- `claude-code/skills/ywc-sequential-executor/references/external-url-policy.md` — **읽기 전용**. `deny` 동작 정의의 출처
- `.claude/settings.local.json` `taskExecutor.externalSpecUrls` — **읽기만** 하며 non-interactive 경로는 쓰지 않는다. schema 무변경
- CI gates: `scripts/validate.sh`, `markdownlint.yml`, `score.py --ci`

### Conflicts With

- (None identified) — `000078-030` / `-040` / `-050` 과 파일 소유가 완전히 분리됨

### Parallelizable After

- `000078-010-docs-impl-review-bounded-payload-noninteractive`

### Task Verify

- `grep -rnE "ywc-impl-review[^|]*--non-interactive" claude-code/skills/ywc-sequential-executor/SKILL.md | wc -l` — **2** (`:337`, `:341`)
- `grep -c "not persisted" claude-code/skills/ywc-sequential-executor/SKILL.md` — ≥ 1
- `grep -c "malformed" claude-code/skills/ywc-sequential-executor/SKILL.md` — ≥ 1
- `git diff -- claude-code/skills/ywc-sequential-executor/SKILL.md` 에 `:64` delivery-mode 그룹과 `:196` Allowed Stop Reasons 가 나타나지 않음
- `grep -n -- "--non-interactive" claude-code/skills/ywc-sequential-executor/README*.md` — 6개 파일 전부 hit

## Out of Scope

- `ywc-impl-review` / `ywc-parallel-executor` / `ywc-code-gen` / `ywc-agentic` 파일 수정 — 각각 다른 task 소유.
- `external-url-policy.md` 수정 — 이 task는 참조만 한다.
- `.ywc-run-state.json` schema 변경, checkpoint/resume mechanics 변경.
- `codex/**` 하위 모든 파일 (AC17).
- mechanical score baseline 재생성 — `000079-010`이 담당.
