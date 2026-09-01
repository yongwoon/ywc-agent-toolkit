# Task: 000082-080-test-trigger-cases-testing-misc

## Prerequisites
- [ ] `000082-070-test-trigger-cases-durable-memory`가 완료(머지)되었는지 확인 — `cases` 배열 길이 증가분 확인 (Fix X gate)

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`만 편집한다(append-only).

## Collision Case Convention (Fix F2 override — verbatim, must appear in this task's dispatch context)
> "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."

## Stop Conditions
- `000082-070`이 실제로 머지되지 않았거나 `cases` 배열이 예상 개수만큼 늘지 않았으면 멈추고 보고한다.
- 편집 범위가 `trigger-cases.json` 밖으로 번지면 멈추고 보고한다.
- anti-trigger sibling이 catalog에서 사라졌으면 현재 동등물 확인 후 진행하거나 멈추고 보고한다.

## Implementation Steps
- [ ] **Step 1 — Id-inventory (Fix C2/S/Z)**: `ywc-gen-testcase`, `ywc-e2e-test-strategy`, `ywc-tdd-ritual`, `ywc-verify-done`, `ywc-auth-implement`, `ywc-setup-language`, `ywc-skill-author`, `ywc-incident-postmortem` 각각에 대해 prefix query + (hit<3 시) field-based fallback query로 `max_n` 결정 (`ywc-gen-testcase`는 기존 `gen-testcase-vs-e2e-test-strategy-1` 같은 hyphen-heavy sibling id가 있으므로 Fix Y의 `[a-z0-9-]+` regex로 확인)
- [ ] **Step 2 — Mining pass (FR-1, Fix E2/Fix R)**: item별로 `session_search` / `mcp-search`(`type: "prompts"`) / grep fallback으로 실사용 이력 검색, 5-rule 필터 적용, 생존 hit sanitize 후 `session-trace`로 기록·분류
- [ ] **Step 3 — Fallback authoring (FR-2, Fix F2)**: 부족분을 `user-prompt`로 hand-author. 테스트 계열 4개(`gen-testcase`/`e2e-test-strategy`/`tdd-ritual`/`verify-done`)는 서로를 collision sibling으로 우선 검토
- [ ] **Step 4 — Dedup (Fix A2 step 4a + Fix L + Fix V)**: 기존 381개 + `000082-010/020/030/040/050/060/070`의 case + 이 task 자신의 output(8개 item, 상대적으로 큰 배치이므로 특히 꼼꼼히)과 대조, legitimate pair 제외 duplicate 제거
- [ ] **Step 5 — Append + numbering**: `max_n + 1`부터 순번 매겨 `cases` 배열 끝에 append
- [ ] **Step 6 — Per-item verify + remediation (Fix M/W/G, Fix P/X)**: `score.py --item <name>`로 확인, 실패 시 1회 재시도, 재실패 시 category (a)/(b) 판정 + evidence 첨부하여 exception 후보 기록
- [ ] **Step 7 — Report**: AC3/AC4/AC9/AC10 준수 여부를 Implementation Notes에 기록

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-gen-testcase --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-e2e-test-strategy --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-tdd-ritual --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-verify-done --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-auth-implement --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-setup-language --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-skill-author --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-incident-postmortem --format json`
- [ ] id 중복 없음 확인
- [ ] `description-derived` source 신규 추가 0건

## Verification
- [ ] `git diff --stat .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`으로 오직 그 파일만 변경했는지 확인
- [ ] JSON 유효성 확인
- [ ] 8개 item 모두 `sufficient == true`이거나 evidence 첨부된 exception으로 기록됨
- [ ] 코드/설정 변경 없음 — lint/build/validate.sh 대상 아님

## Implementation Notes

**Correction mid-task**: initial positive-numbering draft wrongly assumed `pos=0` (independent count) meant no pre-existing `pos-N` ids existed for `ywc-e2e-test-strategy`/`ywc-tdd-ritual`/`ywc-verify-done`/`ywc-skill-author`/`ywc-incident-postmortem` — the automated append script's own `dup_ids` assertion caught this before any write (all 5 already had 4 pre-existing `description-derived` positives occupying `pos-1..4`; `pos=0` only meant zero of those counted toward the *independent* floor). Corrected id-inventory properly this time: `gen-testcase`/`e2e-test-strategy`/`tdd-ritual`/`verify-done`/`skill-author`/`incident-postmortem` all continue at `pos-5..7` (max_n=4); `auth-implement`/`setup-language` continue at `pos-4..6` (max_n=3).

**Fix applied post-review (Design subagent finding — the most substantial correction in this task series)**: the first draft's collision strategy ("continue an existing baseline pairing's direction") propagated 6 of 9 cases into an invalid grounding direction — `expected`'s own clause did not name `impostor` in `e2e-test-strategy-vs-auth-implement-2`, `gen-testcase-vs-e2e-test-strategy-2/3`, `verify-done-vs-tdd-ritual-2`, and `skill-author-vs-project-docs-2/3` (only the *reverse* direction was grounded — the impostor's own clause named the expected side). This is precisely the class of mistake L003 was written to prevent; the pre-existing baseline pairings I copied the direction from were themselves ungrounded in that direction. All 6 were removed and replaced with 8 freshly-authored cases where `expected`'s own clause literally names `impostor` (verified programmatically post-fix, see below): `e2e-test-strategy-vs-gen-testcase-1/2`, `e2e-test-strategy-vs-security-audit-1`, `tdd-ritual-vs-verify-done-1`, `verify-done-vs-code-gen-1`, `project-docs-vs-skill-author-1/2`, `auth-implement-vs-e2e-test-strategy-1`. `ywc-gen-testcase` and `ywc-skill-author` — whose own clauses name no `ywc-*` sibling in either direction — reach their collision floor entirely via the `impostor` role (score.py credits both `expected` and `impostor` toward each name's total), never as `expected`, since no strictly-grounded case can ever cast either of them as the winner.

**L003 clarification**: this task's review made explicit what earlier tasks left implicit — AC4 grounding must come from `expected`'s own clause naming `impostor`, not the reverse. A prior task (`000082-040`) had a fix accepted where the grounding evidence came from the `impostor`'s own clause instead; that direction is not reliable and should not be treated as precedent going forward.

**Avoided a skill↔agent violation**: `skill-author-vs-doc-writer-1` (pre-existing baseline) pairs a skill (`ywc-skill-author`) against an *agent* (`ywc-doc-writer` exists only under `claude-code/agents/`, not `claude-code/skills/`), violating `trigger-eval-method.md`'s same-root rule. Not fixed (pre-existing, out of this task's append-only scope) and not reused for a new case.

**Fix G exception — `ywc-setup-language` has zero collisions and cannot reach the 2-collision floor.** Evidence: (1) `grep -rl "ywc-setup-language" claude-code/skills/*/SKILL.md` across the entire catalog returns nothing outside `ywc-setup-language`'s own file — no skill's `Do not use for ...` clause names it. (2) `ywc-setup-language`'s own clause names no `ywc-*` skill either. (3) The one pre-existing baseline pairing (`setup-language-vs-project-mission-1/2`, `description-derived`) is itself ungrounded by the same literal-naming check in either direction, independently confirmed by the Design reviewer. Category: **(a) genuine content gap**, not (b) process failure. Per `trigger-eval-method.md`: *"If an item genuinely has no competitor, the eval owner approves a documented exception — never substitute a negative for a missing collision."* `ywc-setup-language` has `positives: 3` (floor met) and `collisions: 0` (floor not met, exception granted). Final catalog-wide exception-list confirmation is `000083-010`'s responsibility.

AC3/AC7/AC9/AC10 all confirmed via the same automated checks used in prior tasks. AC4 re-verified for all 11 final collision cases (8 replacements + 3 originally-valid) via a programmatic check that `expected`'s own `Do not use for ...` clause literally contains `impostor`'s identifier.
