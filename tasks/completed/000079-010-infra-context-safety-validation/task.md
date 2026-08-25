# 000079-010-infra-context-safety-validation — Implementation Checklist

## Prerequisites

- [ ] `000078-010-docs-impl-review-bounded-payload-noninteractive` 가 완료(merge)되었다
- [ ] `000078-020-docs-sequential-executor-noninteractive` 가 완료(merge)되었다
- [ ] `000078-030-docs-parallel-executor-flag-compaction` 가 완료(merge)되었다
- [ ] `000078-040-docs-code-gen-agentic-propagation` 가 완료(merge)되었다
- [ ] `000078-050-docs-refactor-cleaner-write-scope` 가 완료(merge)되었다
- [ ] `000078-010/test.md` 와 `000078-020/test.md` 의 수동 transcript 확인 결과가 기록되었다 (AC4 / AC9)

## Allowed Edit Scope

- [ ] 검증 전용이다 — 소스 파일을 편집하지 않는다
- [ ] `score.py --ci` 실패 시에만 `.claude/skills/ywc-toolkit-eval/scripts/history.mechanical.json` 을 재생성한다
- [ ] 검증이 실패하면 고치지 말고 해당 Phase `000078` task로 되돌려 보고한다

## Stop Conditions

- [ ] Phase `000078` task 중 하나라도 merge되지 않았으면 중단 (불완전 baseline 방지)
- [ ] AC7 grep 결과가 7이 아니면 중단하고 초과/누락 지점을 보고
- [ ] `ywc-plan --non-interactive` guard 값이 변경 전과 다르면 중단
- [ ] `score.py --ci` 실패가 정당한 변경으로 설명되지 않으면 baseline을 재생성하지 말고 중단
- [ ] `git diff` 에 `codex/` 경로가 1건이라도 있으면 중단 (AC17)

## Implementation Steps

- [ ] **AC7 — call-site-scoped grep (정확히 7건)**
  - [ ] `grep -rnE "ywc-impl-review[^|]*--non-interactive" claude-code/skills/ywc-sequential-executor/SKILL.md claude-code/skills/ywc-parallel-executor/SKILL.md claude-code/skills/ywc-code-gen/SKILL.md claude-code/skills/ywc-agentic/SKILL.md | wc -l` 이 **7** 인지 확인한다
  - [ ] 7건의 내역이 sequential 2 / parallel 2 / code-gen 2 / agentic 1 로 분포하는지 출력에서 확인한다
  - [ ] guard: `grep -c "ywc-plan --non-interactive" claude-code/skills/ywc-agentic/SKILL.md` 가 변경 전과 동일한지 확인한다
- [ ] **AC2 — impl-review directive 인용**
  - [ ] `grep -c "Return-payload contract" claude-code/skills/ywc-impl-review/SKILL.md` ≥ 1
  - [ ] `grep -c "subagent-status-actions" claude-code/skills/ywc-impl-review/SKILL.md` ≥ 2
- [ ] **AC14 / AC12 — compaction 및 agent 범위**
  - [ ] `grep -ci "compaction" claude-code/skills/ywc-parallel-executor/SKILL.md` ≥ 1
  - [ ] `grep -c "DONE_WITH_CONCERNS" claude-code/agents/ywc-refactor-cleaner.md` 가 batch 이전보다 증가했는지 확인한다
  - [ ] `git diff main...HEAD -- claude-code/agents/ywc-refactor-cleaner.md | grep -c "^[+-]tools:"` 가 **0** 인지 확인한다
- [ ] **AC15 — README locale 정합 (12개)**
  - [ ] `grep -l -- "--non-interactive" claude-code/skills/ywc-impl-review/README*.md claude-code/skills/ywc-sequential-executor/README*.md | wc -l` 이 **12** 인지 확인한다
  - [ ] 12개 파일이 동일한 flag semantics를 서술하는지 육안 대조한다
- [ ] **AC17 — codex root 무변경**
  - [ ] `git diff --name-only main...HEAD | grep -c '^codex/'` 가 **0** 인지 확인한다
- [ ] **AC16 — CI 3종 gate**
  - [ ] `bash scripts/validate.sh` 를 실행해 exit 0 을 확인한다
  - [ ] markdownlint 를 `.github/workflows/markdownlint.yml:19` 의 실제 invocation 형태(unpinned + 생성된 config)로 재현해 통과를 확인한다. 로컬 임의 버전 pin / 다른 glob 사용 금지
  - [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` 를 실행한다
  - [ ] 실패 시: diff를 archive → 정당한 변경임을 확인 → baseline 재생성 → **같은 PR에 commit**

## Task Verify

- [ ] AC7 grep = **7**, guard grep 불변
- [ ] `grep -c "Return-payload contract" …/ywc-impl-review/SKILL.md` ≥ 1
- [ ] `grep -c "subagent-status-actions" …/ywc-impl-review/SKILL.md` ≥ 2
- [ ] `grep -ci "compaction" …/ywc-parallel-executor/SKILL.md` ≥ 1
- [ ] README locale hit = **12**
- [ ] `git diff --name-only main...HEAD | grep -c '^codex/'` = **0**

## Verification

- [ ] `bash scripts/validate.sh` — exit 0
- [ ] markdownlint (workflow invocation 재현) — 통과
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --ci` — exit 0 (필요 시 baseline 재생성 commit 포함)
- [ ] Traceability 표의 AC1–AC17 전 항목이 이 task 또는 선행 task의 evidence로 커버되었음을 확인

## Implementation Notes
