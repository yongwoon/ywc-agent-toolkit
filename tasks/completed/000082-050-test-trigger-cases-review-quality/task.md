# Task: 000082-050-test-trigger-cases-review-quality

## Prerequisites
- [ ] `000082-040-test-trigger-cases-iac-infra`가 완료(머지)되었는지 확인 — `cases` 배열 길이 증가분 확인 (Fix X gate)

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`만 편집한다(append-only).

## Collision Case Convention (Fix F2 override — verbatim, must appear in this task's dispatch context)
> "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."

## Stop Conditions
- `000082-040`이 실제로 머지되지 않았거나 `cases` 배열이 예상 개수만큼 늘지 않았으면 멈추고 보고한다.
- 편집 범위가 `trigger-cases.json` 밖으로 번지면 멈추고 보고한다.
- anti-trigger sibling이 catalog에서 사라졌으면 현재 동등물 확인 후 진행하거나 멈추고 보고한다.

## Implementation Steps
- [ ] **Step 1 — Id-inventory (Fix C2/S/Z)**: `ywc-impl-review`, `ywc-security-audit`, `ywc-ui-ux-review`, `ywc-design-renew`, `ywc-product-review` 각각에 대해 prefix query + (hit<3 시) field-based fallback query로 `max_n` 결정
- [ ] **Step 2 — Mining pass (FR-1, Fix E2/Fix R)**: item별로 `session_search` / `mcp-search`(`type: "prompts"`) / grep fallback으로 실사용 이력 검색, 5-rule 필터 적용, 생존 hit sanitize 후 `session-trace`로 기록·분류
- [ ] **Step 3 — Fallback authoring (FR-2, Fix F2)**: 부족분을 `user-prompt`로 hand-author. `ywc-impl-review`가 "generic code review" 요청에 과도하게 이길 위험이 크므로, collision case에서 `ywc-security-audit`(보안 전용), `ywc-ui-ux-review`/`ywc-design-renew`(디자인 전용)를 실제 anti-trigger 승자로 명확히 표시
- [ ] **Step 4 — Dedup (Fix A2 step 4a + Fix L + Fix V)**: 기존 381개 + `000082-010/020/030/040`의 case + 이 task 자신의 output과 대조, legitimate pair 제외 duplicate 제거
- [ ] **Step 5 — Append + numbering**: `max_n + 1`부터 순번 매겨 `cases` 배열 끝에 append
- [ ] **Step 6 — Per-item verify + remediation (Fix M/W/G, Fix P/X)**: `score.py --item <name>`로 확인, 실패 시 1회 재시도, 재실패 시 category (a)/(b) 판정 + evidence 첨부하여 exception 후보 기록
- [ ] **Step 7 — Report**: AC3/AC4/AC9/AC10 준수 여부를 Implementation Notes에 기록

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-impl-review --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-security-audit --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-ui-ux-review --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-design-renew --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-product-review --format json`
- [ ] id 중복 없음 확인
- [ ] `description-derived` source 신규 추가 0건

## Verification
- [ ] `git diff --stat .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`으로 오직 그 파일만 변경했는지 확인
- [ ] JSON 유효성 확인
- [ ] 5개 item 모두 `sufficient == true`이거나 evidence 첨부된 exception으로 기록됨
- [ ] 코드/설정 변경 없음 — lint/build/validate.sh 대상 아님

## Implementation Notes

All 21 new cases (15 positives + 6 collisions) fallback-authored (`source: user-prompt`). This S5 batch has a rich hub-and-spoke anti-trigger structure around `ywc-impl-review` (the "generic code review" hub, exactly as the README's Summary predicted) plus a clean mutual pair between `ywc-ui-ux-review`/`ywc-design-renew`: 6 collision cases covered all 5 items' 2-collision floor (`impl-review` picked up a 3rd via `product-review-vs-impl-review-2`, `ui-ux-review` a 3rd via `product-review-vs-ui-ux-review-1`, both harmless extras).

Applied L001/L002/L003 with the automated trigger-phrase substring check from the start. The automated check caught and blocked 2 draft prompts before they were ever written to the file (`security-audit-vs-impl-review-2` originally said "코드 리뷰" — impl-review's own exact trigger phrase — while trying to describe *not* wanting a code review; `design-renew-vs-ui-ux-review-2` originally said "사용성 점검" — ui-ux-review's exact trigger phrase — while trying to describe *not* wanting a usability check). Both were rephrased to convey the same "not X" framing without quoting X's literal trigger phrase, confirming L001's rule applies even when a trigger phrase is used to explicitly *reject* that item, not just to request it — the activation judge does not read polarity, only text.

AC3/AC4/AC7/AC9/AC10 all confirmed via the same automated checks used in prior tasks. All 6 collision `impostor` values verified against the literal `Do not use for ...` clause in the corresponding item's own `SKILL.md` (per L003, checked the correct direction each time).
