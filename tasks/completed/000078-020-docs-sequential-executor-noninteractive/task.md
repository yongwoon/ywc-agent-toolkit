# 000078-020-docs-sequential-executor-noninteractive — Implementation Checklist

## Prerequisites

- [ ] `000078-010-docs-impl-review-bounded-payload-noninteractive` 가 완료(merge)되었고 `ywc-impl-review` 의 Arguments 표에 `--non-interactive` 행이 존재한다
- [ ] `claude-code/skills/ywc-sequential-executor/references/external-url-policy.md` 의 `deny` 동작 정의를 확인했다
- [ ] `docs/ywc-plans/20260812-claude-code-agentic-context-safety.md` FR-3 / FR-4 및 `## Iteration 1 Amendments` 의 FR-4 orthogonality 절을 읽었다

## Allowed Edit Scope

- [ ] `claude-code/skills/ywc-sequential-executor/**` 안에서만 편집한다
- [ ] `references/external-url-policy.md` 는 **읽기만** 한다
- [ ] Ownership 밖 편집이 필요하면 중단하고 보고한다

## Stop Conditions

- [ ] `:119` External URL Policy 문단의 기존 두 분기 문장을 특정할 수 없으면 중단
- [ ] `--non-interactive` 를 `:64` delivery-mode 상호배타 그룹에 넣어야 한다고 판단되면 중단 (FR-4 orthogonality 위반)
- [ ] `:196` Allowed Stop Reasons 에 항목을 추가/삭제해야 한다고 판단되면 중단
- [ ] non-interactive 경로가 `.claude/settings.local.json` 에 write해야 한다고 판단되면 중단 (AC9 위반)

## Implementation Steps

- [ ] **FR-4a — Arguments 표에 flag 추가**
  - [ ] `--non-interactive` 1행 추가. 의미: Pre-flight의 External URL Policy 질문을 열지 않고 문서화된 `deny` default를 **이번 run 한정**으로 적용(영속화하지 않음)
  - [ ] `:64` 의 4개 delivery mode 상호배타 그룹과 **직교**함을 명시한다 — `--worktree` 와 동일하게 "not a fifth member"
  - [ ] 모든 delivery mode 및 `--review` / `--dry-run` / `--worktree` 와 조합됨을 기술한다
- [ ] **FR-4b — External URL Policy 3분기화** (`SKILL.md:119`)
  - [ ] 분기 1 — key가 **있으면**: mode와 무관하게 기존대로 silently 사용 (기존 문장 삭제 금지, AC10)
  - [ ] 분기 2 — **없고** `--non-interactive` 가 **없으면**: 기존대로 1회 질문 후 persist (기존 문장 삭제 금지, AC10)
  - [ ] 분기 3(신설) — **없고** `--non-interactive` 가 **있으면**: 질문 없이 `deny` 적용, **파일에 persist하지 않음**
  - [ ] 분기 3에 Step 1b의 skip된 URL 목록을 기존 `deny` 동작대로 log한다고 명시한다
- [ ] **FR-4c — malformed 값 분기 신설**
  - [ ] key가 존재하지만 `allow` / `deny` / `allowlist` 중 어느 것도 아닐 때: key 부재와 동일하게 취급하되 **이번 run 한정**
  - [ ] malformed 값을 강제 변환하거나 persist하지 않는다고 명시한다
  - [ ] 두 mode 모두 Completion Report에 `External URL policy: malformed value "<value>" — treated as absent for this run` 기록
  - [ ] interactive 분기가 재질문할 때는 기존 값이 무효라 교체됨을 **먼저 알린 뒤** 묻는다고 기술한다
  - [ ] 이 규칙이 `external-url-policy.md` 에 없는 **신규 규칙**임을 문서 내에 밝힌다
- [ ] **FR-4d — Completion Report 라인**
  - [ ] non-interactive 경로에서 `External URL policy: deny (assumed — non-interactive, not persisted)` 를 Completion Report에 출력하도록 규정한다
  - [ ] `--dry-run` 조합 시 이 가정이 계획 출력에 한 줄로 표시되고 별도 동작 변화가 없음을 기술한다
- [ ] **FR-3(부분) — impl-review 호출 2곳에 flag 부착**
  - [ ] `:337` Step 4.5 (`--review` 시): 문장 내 명령을 `/ywc-impl-review --non-interactive` 로 변경
  - [ ] `:341` critical-path 강제 호출: `/ywc-impl-review` 에만 flag 부착. `/ywc-security-audit` 에는 부착하지 않는다
  - [ ] 두 지점의 status routing 문단(`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT`)은 변경하지 않는다
- [ ] **FR-7(부분) — README 6 locale 갱신**
  - [ ] `README.en.md` 에 영어 원본으로 flag 설명을 추가한다
  - [ ] `README.md` / `README.ko.md` 에 한국어로 반영한다 (technical term은 English 유지)
  - [ ] `README.ja.md` / `README.zh.md` / `README.es.md` 에 각 언어로 반영한다
  - [ ] 기존 External URL 관련 문구(`README.md:115` 등)와 3분기 서술이 모순되지 않도록 정합한다
  - [ ] 6개 파일이 동일한 flag semantics를 서술하는지 대조한다 (AC15)

## Task Verify

- [ ] `grep -rnE "ywc-impl-review[^|]*--non-interactive" claude-code/skills/ywc-sequential-executor/SKILL.md | wc -l` — **2**
- [ ] `grep -c "not persisted" claude-code/skills/ywc-sequential-executor/SKILL.md` — ≥ 1
- [ ] `grep -c "treated as absent for this run" claude-code/skills/ywc-sequential-executor/SKILL.md` — ≥ 1
- [ ] `grep -n -- "--non-interactive" claude-code/skills/ywc-sequential-executor/README*.md` — 6개 파일 전부 hit
- [ ] `git diff -- claude-code/skills/ywc-sequential-executor/SKILL.md` 에 `:64` delivery-mode 그룹 / `:155` compaction 문단 / `:196` Allowed Stop Reasons 가 나타나지 않음을 육안 확인
- [ ] `:119` 의 기존 두 분기 문장이 삭제되지 않고 세 번째 분기만 추가되었음을 육안 확인 (AC10)

## Verification

- [ ] `bash scripts/validate.sh` 통과
- [ ] markdownlint 통과 — `.github/workflows/markdownlint.yml` 의 실제 invocation 형태를 재현한다
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --format json` 으로 read-only 확인
- [ ] `git diff --name-only | grep -c '^codex/'` — 0 (AC17)
- [ ] 수동 transcript 확인 — `test.md` 참조

## Implementation Notes
