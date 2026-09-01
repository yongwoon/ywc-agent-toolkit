# Task: 000082-020-test-trigger-cases-spec-execution

## Prerequisites
- [ ] `000082-010-test-trigger-cases-planning-core`가 완료(머지)되었는지 확인 — `evals/trigger-cases.json`의 `cases` 배열 길이가 predecessor가 보고한 개수만큼 증가했는지 확인 (Fix X gate: append 성공이 gate 조건, 개별 item의 sufficient==true는 gate 조건 아님)

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`만 편집한다(append-only). 다른 파일은 건드리지 않는다.

## Collision Case Convention (Fix F2 override — verbatim, must appear in this task's dispatch context)
> "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."

## Stop Conditions
- `000082-010`이 실제로 머지되지 않았거나 `cases` 배열이 예상 개수만큼 늘지 않았으면 멈추고 보고한다.
- 편집 범위가 `trigger-cases.json` 밖으로 번지면 멈추고 보고한다.
- 어떤 item의 anti-trigger sibling이 catalog에서 더 이상 존재하지 않으면(rename/merge) 현재 동등물을 확인 후 진행하거나, 확인 불가하면 멈추고 보고한다.

## Implementation Steps
- [ ] **Step 1 — Id-inventory (Fix C2/S/Z)**: `ywc-spec-ready`, `ywc-task-generator`, `ywc-agentic`, `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-code-gen` 각각에 대해
  - [ ] prefix query: `python3 -c "import json; d=json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json')); print(sorted(c['id'] for c in d['cases'] if c['id'].startswith('<slug>-')))"` (`<slug>` = `ywc-` 접두어 제거형, 예: `ywc-spec-ready` → `spec-ready` — 단 기존 legacy id는 `specready-`처럼 하이픈 없이 축약된 경우가 있어(Fix S) 정확한 형태는 field-based query로 교차 확인)
  - [ ] hit이 3개 미만이면 Fix S/Z field-based fallback: `expected`/`impostor`가 item 전체 이름과 일치하는 case 조회
  - [ ] 합집합에서 최고 suffix를 `max_n`으로 결정 (없으면 0)
- [ ] **Step 2 — Mining pass (FR-1, Fix E2/Fix R)**: item별로
  - [ ] `mcp__plugin_oh-my-claudecode_t__session_search`, `mcp__plugin_claude-mem_mcp-search__search`(`type: "prompts"`), 필요 시 `grep` over `~/.claude/projects/**/*.jsonl`로 실사용 이력 검색
  - [ ] 필터: 실제 user 발화만, harness-injected tag 제외, skill-catalog/SKILL.md 재현 제외, 현재 mining session 자신의 hit 제외, 이 plan 문서/`trigger-eval-method.md` 등 reference doc 재현 hit 제외(Fix E2 rule 5), tool-output/데이터 덤프성 hit 제외(Fix R)
  - [ ] 생존 hit은 sanitize 후 `"source": "session-trace"`로 기록, positive/collision 분류
- [ ] **Step 3 — Fallback authoring (FR-2, Fix F2)**: mining으로 3 positive / 2 collision을 못 채운 item에 대해
  - [ ] `positive`: description을 읽지 않고 실제 사용자가 말할 법한 자연어 요청을 `"source": "user-prompt"`로 작성
  - [ ] `collision`: item의 `Do not use for ...` anti-trigger clause에 literal하게 이름 붙은 sibling으로 **단일 entry** 작성(`expected`/`impostor`), paired positive 금지
- [ ] **Step 4 — Dedup (Fix A2 step 4a + Fix L + Fix V)**: 신규 case 전체를
  - [ ] 기존 381개 + `000082-010`이 append한 case와 prompt 텍스트로 대조
  - [ ] 이 task 자신의 output 내부에서도 상호 대조
  - [ ] 완전/near-duplicate 제거, 단 legitimate positive+collision pair는 유지
- [ ] **Step 5 — Append + numbering**: `max_n + 1`부터 순번을 매겨 `cases` 배열 끝에 append (파일 구조 재구성 금지)
- [ ] **Step 6 — Per-item verify + remediation (Fix M/W/G, Fix P/X)**: item별로
  - [ ] `score.py --target claude-code/skills --item <name> --format json`으로 `sufficient == true` 확인
  - [ ] 실패하면 해당 item만 Step 2–5를 1회 재시도
  - [ ] 재시도도 실패하면 category (a)/(b) 판정 + evidence 첨부 후 Implementation Notes에 기록, exception 후보로 남긴다(category (b)는 재수정)
- [ ] **Step 7 — Report**: AC3/AC4/AC9/AC10 준수 여부를 Implementation Notes에 기록

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-spec-ready --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-task-generator --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-agentic --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-sequential-executor --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-parallel-executor --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-code-gen --format json`
- [ ] id 중복 없음 확인
- [ ] `description-derived` source 신규 추가 0건

## Verification
- [ ] `git diff --stat .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`으로 이 task가 오직 그 파일만 변경했는지 확인
- [ ] JSON 유효성: `python3 -c "import json; json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json'))"`
- [ ] 위 6개 item 모두 `sufficient == true`이거나 evidence 첨부된 exception으로 기록됨
- [ ] 코드/설정 변경 없음 — lint/build/validate.sh 대상 아님

## Implementation Notes

**Mining vs fallback**: mining for this batch (S2, orchestration-layer skills) surfaced almost nothing usable — real session hits were dominated by slash-command invocations that name the item (`/ywc-sequential-executor 000082-010..000083-010 --review`, `4개를 한 번에 task-generator로 넘겨...`), which are excluded by L001. All 18 positives and all 8 collisions were FR-2 fallback-authored (`source: user-prompt`), applying L001 from `000082-010` throughout.

**Fixes applied post-review (Design subagent findings, `ywc-impl-review --git-range`)**:
1. `code-gen-pos-5` verbatim-quoted `ywc-code-gen`'s own official Trigger phrase ("코드 생성") even though it did not name the skill's identifier — the Design reviewer correctly widened L001's scope to cover verbatim trigger-phrase reuse, not just the `ywc-*` identifier, since it produces the same trivially-winnable circularity. Replaced with an intent-only phrasing containing none of the item's 8 official trigger strings.
2. 5 new collision ids used an unhyphenated/contracted slug for their own item prefix (`taskgenerator-`, `sequentialexecutor-`, `parallelexecutor-`, `codegen-` ×2), inconsistent with each item's dominant hyphenated id convention already established by 8-9 other ids for the same item — a real AC9 mechanical-pattern break, not just cosmetic (would misdirect a future task's Fix C2 prefix-query id-inventory). Renamed to `task-generator-vs-spec-ready-1`, `sequential-executor-vs-parallel-executor-2`, `parallel-executor-vs-sequential-executor-1`, `code-gen-vs-sequential-executor-2`, `code-gen-vs-parallel-executor-2` — each renumbered off the correct family's real `max_n`, not a fresh isolated counter under the wrong slug.

Re-verified after both fixes: all 6 items remain `sufficient: true`, id uniqueness holds (432 total), JSON valid, no new duplicate prompts.

**Recommendation for remaining tasks**: extend L001 in `docs/review-learnings.md` to explicitly cover verbatim official-trigger-phrase reuse (not just the `ywc-*` identifier), and to require id-inventory Step 1 to use each item's *majority* slug form (found via the field-based fallback query) rather than a mechanically-stripped `ywc-` prefix, since several items in this catalog have legacy unhyphenated outlier ids that should not be treated as the dominant convention.

**AC conformance**: AC3 (no `description-derived`) — confirmed, 0. AC4 (collision `impostor` traces to a real anti-trigger clause) — confirmed against each item's actual `SKILL.md` description text. AC7 (no duplicate ids) — confirmed, 432 unique. AC9 (id pattern, including per-item slug consistency) — confirmed after the rename fix. AC10 (no duplicate prompts) — confirmed against the full 432-case file.
