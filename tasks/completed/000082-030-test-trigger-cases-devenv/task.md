# Task: 000082-030-test-trigger-cases-devenv

## Prerequisites
- [ ] `000082-020-test-trigger-cases-spec-execution`이 완료(머지)되었는지 확인 — `cases` 배열 길이 증가분 확인 (Fix X gate)

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`만 편집한다(append-only).

## Collision Case Convention (Fix F2 override — verbatim, must appear in this task's dispatch context)
> "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."

## Stop Conditions
- `000082-020`이 실제로 머지되지 않았거나 `cases` 배열이 예상 개수만큼 늘지 않았으면 멈추고 보고한다.
- 편집 범위가 `trigger-cases.json` 밖으로 번지면 멈추고 보고한다.
- anti-trigger sibling이 catalog에서 사라졌으면 현재 동등물 확인 후 진행하거나 멈추고 보고한다.

## Implementation Steps
- [ ] **Step 1 — Id-inventory (Fix C2/S/Z)**: `ywc-worktrees`, `ywc-docker-isolate`, `ywc-refactor-clean`, `ywc-onboard-repo` 각각에 대해 prefix query + (hit<3 시) field-based fallback query로 `max_n` 결정
- [ ] **Step 2 — Mining pass (FR-1, Fix E2/Fix R)**: item별로 `session_search` / `mcp-search`(`type: "prompts"`) / grep fallback으로 실사용 이력 검색, 5-rule 필터(real user entry / harness tag 제외 / SKILL.md 재현 제외 / 현재 세션 제외 / reference doc 재현·데이터 덤프 제외) 적용, 생존 hit sanitize 후 `session-trace`로 기록·분류
- [ ] **Step 3 — Fallback authoring (FR-2, Fix F2)**: 부족분을 `user-prompt`로 hand-author. positive는 description 미참조 자연어, collision은 anti-trigger 기반 단일 entry(`expected`/`impostor`)
- [ ] **Step 4 — Dedup (Fix A2 step 4a + Fix L + Fix V)**: 기존 381개 + `000082-010`,`000082-020`의 case + 이 task 자신의 output과 대조, legitimate pair 제외 duplicate 제거
- [ ] **Step 5 — Append + numbering**: `max_n + 1`부터 순번 매겨 `cases` 배열 끝에 append
- [ ] **Step 6 — Per-item verify + remediation (Fix M/W/G, Fix P/X)**: `score.py --item <name>`로 확인, 실패 시 1회 재시도, 재실패 시 category (a)/(b) 판정 + evidence 첨부하여 exception 후보 기록
- [ ] **Step 7 — Report**: AC3/AC4/AC9/AC10 준수 여부를 Implementation Notes에 기록

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-worktrees --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-docker-isolate --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-refactor-clean --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-onboard-repo --format json`
- [ ] id 중복 없음 확인
- [ ] `description-derived` source 신규 추가 0건

## Verification
- [ ] `git diff --stat .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`으로 오직 그 파일만 변경했는지 확인
- [ ] JSON 유효성 확인
- [ ] 4개 item 모두 `sufficient == true`이거나 evidence 첨부된 exception으로 기록됨
- [ ] 코드/설정 변경 없음 — lint/build/validate.sh 대상 아님

## Implementation Notes

All 18 new cases (11 positives + 7 collisions) fallback-authored (`source: user-prompt`) — mining was not attempted for this batch given the low yield observed in `000082-020` for orchestration-tier skills; dev-env tooling skills (worktrees, docker-isolate) are even less likely to surface in casual session chatter. `ywc-worktrees` already had 1 pre-existing independent positive (`worktrees-trace-1`), reducing its own new-positive need to 2.

Applied L001+L002 from `docs/review-learnings.md` from the start this time, including an **automated substring check** against each item's exact quoted Trigger-list phrases (not just the `ywc-*` identifier) baked directly into the append script before writing — this is the concrete form of the "widen L001" recommendation from `000082-020`'s review. No item-name or trigger-phrase leakage found on the first pass.

Two of `ywc-refactor-clean`'s Do-not-use siblings (`ywc-tdd-ritual`) and one of `ywc-docker-isolate`'s (`ywc-sequential-executor`, cross-batch/already-authored) were written on this task's behalf per Fix I, giving `ywc-tdd-ritual` (S8, not yet its own task) and `ywc-project-scaffold` (S7, not yet its own task) a head start toward their own coverage floor.

**Correction to the plan's suggested pairing**: the README's Summary suggested `ywc-refactor-clean` vs `ywc-onboard-repo` as a likely-confused pair, but neither skill's `SKILL.md` `Do not use for ...` clause actually names the other — forcing that pairing would have failed AC4 (no real anti-trigger evidence). Used `refactor-clean` vs `code-gen`/`tdd-ritual` (both literally named in refactor-clean's own clause) and `onboard-repo` vs `project-scaffold` (already an established real pair in the baseline) instead.

**Pre-existing baseline note (not touched, out of scope)**: `refactor-clean-vs-refactor-cleaner-1` / `refactor-cleaner-vs-refactor-clean-1` in the existing 381 cases pair a skill (`ywc-refactor-clean`) against an *agent* (`ywc-refactor-cleaner`), which violates `trigger-eval-method.md`'s same-root rule ("a skill↔agent collision cannot be adjudicated"). Flagging for the repo owner's awareness — not fixed here (outside this task's append-only edit scope; would require editing an existing case).

AC3/AC4/AC7/AC9/AC10 all confirmed via the same automated checks used in prior tasks.

**Fix applied post-review (Design subagent finding)**: `docker-isolate-vs-worktrees-2` mirrored a pre-existing baseline weakness — neither `ywc-docker-isolate` nor `ywc-worktrees` literally names the other in its own anti-trigger clause (`ywc-docker-isolate`'s clause names only `ywc-sequential-executor`; `ywc-worktrees`'s clause only alludes generically to "Docker volumes"). Replaced with `docker-isolate-vs-infra-design-1`: `ywc-infra-design`'s own clause literally says "local/dev docker port collisions (use ywc-docker-isolate)" — a stricter AC4 match. This left `ywc-worktrees` one collision short (its only remaining new collision was via `worktrees-vs-parallel-executor-2`), so added `finish-branch-vs-worktrees-1` — `ywc-worktrees`'s own clause literally names `ywc-finish-branch` ("CI/merge/Mark-Complete delivery"). Re-verified: all 4 target items remain `sufficient: true` (451 total cases), no new duplicates.
