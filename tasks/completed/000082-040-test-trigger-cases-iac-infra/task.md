# Task: 000082-040-test-trigger-cases-iac-infra

## Prerequisites
- [ ] `000082-030-test-trigger-cases-devenv`가 완료(머지)되었는지 확인 — `cases` 배열 길이 증가분 확인 (Fix X gate)

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`만 편집한다(append-only).

## Collision Case Convention (Fix F2 override — verbatim, must appear in this task's dispatch context)
> "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."

## Stop Conditions
- `000082-030`이 실제로 머지되지 않았거나 `cases` 배열이 예상 개수만큼 늘지 않았으면 멈추고 보고한다.
- 편집 범위가 `trigger-cases.json` 밖으로 번지면 멈추고 보고한다.
- anti-trigger sibling이 catalog에서 사라졌으면 현재 동등물 확인 후 진행하거나 멈추고 보고한다.

## Implementation Steps
- [ ] **Step 1 — Id-inventory (Fix C2/S/Z)**: `ywc-infra-design`, `ywc-iac-author`, `ywc-infra-review`, `ywc-infra-optimize` 각각에 대해 prefix query + (hit<3 시) field-based fallback query로 `max_n` 결정
- [ ] **Step 2 — Mining pass (FR-1, Fix E2/Fix R)**: item별로 `session_search` / `mcp-search`(`type: "prompts"`) / grep fallback으로 실사용 이력 검색, 5-rule 필터 적용, 생존 hit sanitize 후 `session-trace`로 기록·분류
- [ ] **Step 3 — Fallback authoring (FR-2, Fix F2)**: 부족분을 `user-prompt`로 hand-author. positive는 description 미참조 자연어, collision은 anti-trigger 기반 단일 entry
- [ ] **Step 4 — Dedup (Fix A2 step 4a + Fix L + Fix V)**: 기존 381개 + `000082-010/020/030`의 case + 이 task 자신의 output과 대조, legitimate pair 제외 duplicate 제거
- [ ] **Step 5 — Append + numbering**: `max_n + 1`부터 순번 매겨 `cases` 배열 끝에 append
- [ ] **Step 6 — Per-item verify + remediation (Fix M/W/G, Fix P/X)**: `score.py --item <name>`로 확인, 실패 시 1회 재시도, 재실패 시 category (a)/(b) 판정 + evidence 첨부하여 exception 후보 기록
- [ ] **Step 7 — Report**: AC3/AC4/AC9/AC10 준수 여부를 Implementation Notes에 기록

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-infra-design --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-iac-author --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-infra-review --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-infra-optimize --format json`
- [ ] id 중복 없음 확인
- [ ] `description-derived` source 신규 추가 0건

## Verification
- [ ] `git diff --stat .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`으로 오직 그 파일만 변경했는지 확인
- [ ] JSON 유효성 확인
- [ ] 4개 item 모두 `sufficient == true`이거나 evidence 첨부된 exception으로 기록됨
- [ ] 코드/설정 변경 없음 — lint/build/validate.sh 대상 아님

## Implementation Notes

All 16 new cases (12 positives + 4 collisions) fallback-authored (`source: user-prompt`). This S4 batch forms a clean closed-loop lifecycle chain (design → author → review → optimize) with real, literal, MUTUAL anti-trigger clauses between every adjacent pair (and even the non-adjacent design↔optimize pair, via infra-optimize's own "greenfield infrastructure design (use ywc-infra-design)" clause) — the most efficient collision set of any task so far: exactly 4 collision cases cover all 4 items' 2-collision floor, vs. 6-8 in prior batches.

Applied L001/L002 with the automated trigger-phrase substring check from the start (per-item exact Trigger list extracted and checked against every new prompt for both `expected` and `impostor` sides). No item-name or trigger-phrase leakage found.

Two of the four new collisions (`iac-author-vs-infra-design-2`, `infra-review-vs-iac-author-2`, `infra-optimize-vs-infra-review-2`) continue existing baseline families in the same winner direction; `infra-design-vs-infra-optimize-1` is a genuinely new family (the existing baseline only had the reverse `infra-optimize-vs-infra-design-1`).

AC3/AC4/AC7/AC9/AC10 all confirmed via the same automated checks used in prior tasks.

**Fix applied post-review (Design subagent finding)**: `infra-design-vs-infra-optimize-1` incorrectly assumed the design↔optimize anti-trigger was mutual — it is actually one-directional (`ywc-infra-optimize`'s clause names `ywc-infra-design` for "greenfield infrastructure design", but `ywc-infra-design`'s own clause never reciprocally names `ywc-infra-optimize`). Removed and replaced with `infra-review-vs-infra-design-1` (`ywc-infra-design`'s own clause literally names `ywc-infra-review` for "reviewing existing infrastructure"), which also removed `ywc-infra-optimize`'s only remaining new-collision credit — restored it with `iac-author-vs-infra-optimize-1` (`ywc-infra-optimize`'s own clause literally names `ywc-iac-author` for "first-time IaC authoring"). Re-verified: all 4 items `sufficient: true` (468 total cases), no new duplicates, 60/60 unit tests pass.
