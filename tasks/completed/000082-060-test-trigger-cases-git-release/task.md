# Task: 000082-060-test-trigger-cases-git-release

## Prerequisites
- [ ] `000082-050-test-trigger-cases-review-quality`가 완료(머지)되었는지 확인 — `cases` 배열 길이 증가분 확인 (Fix X gate)

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`만 편집한다(append-only). `ywc-commit`/`ywc-create-pr`/`ywc-debug-rootcause`/`ywc-handle-pr-reviews`의 기존 case는 읽기 전용으로만 참고하고 수정/추가하지 않는다.

## Collision Case Convention (Fix F2 override — verbatim, must appear in this task's dispatch context)
> "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."

## Stop Conditions
- `000082-050`이 실제로 머지되지 않았거나 `cases` 배열이 예상 개수만큼 늘지 않았으면 멈추고 보고한다.
- 편집 범위가 `trigger-cases.json` 밖으로 번지면 멈추고 보고한다.
- 이미 충분한 4개 skill의 기존 case를 수정하려는 상황이 생기면 멈추고 보고한다(AC6 위반 위험).

## Implementation Steps
- [ ] **Step 1 — Id-inventory (Fix C2/S/Z)**: `ywc-finish-branch`, `ywc-merge-dependabot`, `ywc-changelog-release-notes`, `ywc-release-pr-list`, `ywc-receive-review` 각각에 대해 prefix query + (hit<3 시) field-based fallback query로 `max_n` 결정
- [ ] **Step 2 — Mining pass (FR-1, Fix E2/Fix R)**: item별로 `session_search` / `mcp-search`(`type: "prompts"`) / grep fallback으로 실사용 이력 검색, 5-rule 필터 적용, 생존 hit sanitize 후 `session-trace`로 기록·분류
- [ ] **Step 3 — Fallback authoring (FR-2, Fix F2)**: 부족분을 `user-prompt`로 hand-author. `ywc-commit`/`ywc-create-pr`/`ywc-handle-pr-reviews`를 collision sibling(`expected` 또는 `impostor`)으로 인용하는 것은 허용하되, 그 4개 skill 자체의 새 positive/collision case는 만들지 않는다
- [ ] **Step 4 — Dedup (Fix A2 step 4a + Fix L + Fix V)**: 기존 381개(기존 `commit-trace-*` 등 legitimate cross-citation은 읽기 참고만, 수정 금지) + `000082-010/020/030/040/050`의 case + 이 task 자신의 output과 대조, legitimate pair 제외 duplicate 제거
- [ ] **Step 5 — Append + numbering**: `max_n + 1`부터 순번 매겨 `cases` 배열 끝에 append
- [ ] **Step 6 — Per-item verify + remediation (Fix M/W/G, Fix P/X)**: `score.py --item <name>`로 확인, 실패 시 1회 재시도, 재실패 시 category (a)/(b) 판정 + evidence 첨부하여 exception 후보 기록. 부수적으로 `ywc-commit` S1 점수가 여전히 5인지 조기 확인(AC6)
- [ ] **Step 7 — Report**: AC3/AC4/AC6(조기)/AC9/AC10 준수 여부를 Implementation Notes에 기록

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-finish-branch --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-merge-dependabot --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-changelog-release-notes --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-release-pr-list --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-receive-review --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-commit --format json` — S1 5점 유지 확인(AC6 조기 체크)
- [ ] id 중복 없음 확인
- [ ] `description-derived` source 신규 추가 0건

## Verification
- [ ] `git diff --stat .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`으로 오직 그 파일만 변경했는지 확인
- [ ] JSON 유효성 확인
- [ ] 5개 item 모두 `sufficient == true`이거나 evidence 첨부된 exception으로 기록됨
- [ ] 이미 충분한 4개 skill의 case가 그대로임을 `git diff`에서 육안 확인(AC6)
- [ ] 코드/설정 변경 없음 — lint/build/validate.sh 대상 아님

## Implementation Notes

All 23 new cases (15 positives + 8 collisions) fallback-authored (`source: user-prompt`). `ywc-changelog-release-notes` vs `ywc-release-pr-list` is a real mutual in-batch pair (both directions), giving both items their full 2-collision floor from just 2 cases. The other 3 items (`finish-branch`, `merge-dependabot`, `receive-review`) had no real in-batch sibling, so per the README's explicit exception, their collisions cite the already-sufficient `ywc-create-pr`/`ywc-handle-pr-reviews`/`ywc-impl-review` as `impostor` only — no new case was created with `expected` set to any of the 4 restricted skills (`ywc-commit`, `ywc-create-pr`, `ywc-debug-rootcause`, `ywc-handle-pr-reviews`).

**AC6 early check**: confirmed via `git diff` that zero new cases have `"expected"` set to any of the 4 restricted skills — they appear only as `"impostor"` in 5 collision cases (`ywc-create-pr` ×3, `ywc-handle-pr-reviews` ×2), which the task README explicitly permits. `ywc-commit`'s case count in the file is unchanged by this diff. Final AC6 confirmation (full re-score) is `000083-010`'s responsibility.

`ywc-merge-dependabot` had only one real anti-trigger sibling available (`ywc-create-pr`, per its own clause) — used it twice with different prompt framings (batch dependency-update processing vs. bot-opened-PR framing) rather than forcing a second, less-grounded sibling relationship.

Applied L001/L002/L003/L004 with the automated trigger-phrase substring check from the start. AC3/AC4/AC7/AC9/AC10 all confirmed.
