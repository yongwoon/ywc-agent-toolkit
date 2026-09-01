# Task: 000082-010-test-trigger-cases-planning-core

## Prerequisites
- [ ] (None — root task; no predecessor to verify)

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`만 편집한다(append-only). 다른 파일은 건드리지 않는다.

## Collision Case Convention (Fix F2 override — verbatim, must appear in this task's dispatch context)
> "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."

## Stop Conditions
- 편집 범위가 `trigger-cases.json` 밖으로 번지면(예: `score.py` 수정이 필요해 보이면) 멈추고 보고한다.
- 어떤 item의 anti-trigger sibling이 catalog에서 더 이상 존재하지 않으면(rename/merge, Edge Cases) 현재 동등물을 확인 후 진행하거나, 확인 불가하면 멈추고 보고한다.
- mining/fallback을 모두 거쳐도 어떤 item이 3 positive를 채울 수 없고 그 원인이 category (b) process failure로 의심되면, exception으로 넘기지 말고 멈춰서 보고한다.

## Implementation Steps
- [ ] **Step 1 — Id-inventory (Fix C2/S/Z)**: `ywc-plan`, `ywc-brainstorm`, `ywc-tech-research`, `ywc-confidence-gate`, `ywc-spec-writer`, `ywc-spec-validate` 각각에 대해
  - [ ] `<slug>` = item 이름에서 `ywc-` 접두어 제거(예: `ywc-plan` → `plan`)로 prefix query 실행: `python3 -c "import json; d=json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json')); print(sorted(c['id'] for c in d['cases'] if c['id'].startswith('<slug>-')))"`
  - [ ] prefix query hit이 3개 미만이면 Fix S/Z field-based fallback 실행: `python3 -c "import json; d=json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json')); item='ywc-plan'; print(sorted(c['id'] for c in d['cases'] if c.get('expected')==item or c.get('impostor')==item))"`
  - [ ] 두 query의 합집합에서 `-pos-N`/`-vs-*-N`/`-trace-N` 최고 suffix를 `max_n`으로 결정 (없으면 0)
- [ ] **Step 2 — Mining pass (FR-1, Fix E2/Fix R) + Open Question 2 dry-run**: item별로
  - [ ] `mcp__plugin_oh-my-claudecode_t__session_search`, `mcp__plugin_claude-mem_mcp-search__search`(`type: "prompts"`), 필요 시 `grep` over `~/.claude/projects/**/*.jsonl`로 실사용 이력 검색
  - [ ] 필터 적용: 실제 user 발화만(role/type 필드는 tool마다 다름), harness-injected tag 제외, skill-catalog/SKILL.md 재현 제외, 현재 mining session 자신의 hit 제외, 이 plan 문서/`trigger-eval-method.md` 등 reference doc을 논의/재현하는 hit 제외(Fix E2 rule 5), tool-output/데이터 덤프성 hit 제외(Fix R)
  - [ ] 생존한 hit은 sanitize(hostname/절대경로/credential/내부 식별자 제거, 오타·구어체는 유지) 후 `"source": "session-trace"`로 기록하고, 해당 item이 실제로 이겼는지(positive) 아니면 sibling이 이겼어야 했는지(collision, `impostor`에 이 item, `expected`에 실제 winner)를 분류
  - [ ] mining만으로 확보된 positive/collision 개수와 필요 개수(3/2) 대비 비율을 계산해 Implementation Notes 최상단에 요약(예: "mined 4/6 item positive-sufficient, 2/6 collision-sufficient — fallback 부하 ~N%") — 이후 8개 task가 참고할 dry-run 데이터
- [ ] **Step 3 — Fallback authoring (FR-2, Fix F2)**: mining으로 3 positive / 2 collision을 못 채운 item에 대해
  - [ ] `positive`: item의 description을 읽지 않고 사용자가 실제로 말할 법한 자연어 요청을 `"source": "user-prompt"`로 작성 (item의 own 다국어 trigger 스타일 반영)
  - [ ] `collision`: item 자신의 `Do not use for ...` anti-trigger clause에 literal하게 이름 붙은 진짜 경쟁 sibling을 골라, **단일 entry**로 작성(`expected`=승자, `impostor`=패자) — 위 Fix F2 override 적용, paired positive 별도 작성 금지
- [ ] **Step 4 — Dedup (Fix A2 step 4a + Fix L + Fix V)**: 신규 case 전체를
  - [ ] 기존 381개 case와 prompt 텍스트로 대조 (root task이므로 predecessor batch 없음)
  - [ ] 이 task 자신의 output 내부에서도 상호 대조
  - [ ] 완전/near-duplicate는 제거하되, 같은 prompt·다른 kind이고 `expected`/`impostor`가 서로를 지칭하는 legitimate positive+collision pair는 유지
- [ ] **Step 5 — Append + numbering**: `max_n + 1`부터 순번을 매겨 `evals/trigger-cases.json`의 `cases` 배열 끝에 append한다 (파일 구조 재구성 금지, 배열만 확장)
- [ ] **Step 6 — Per-item verify + remediation (Fix M/W/G, Fix P/X)**: item별로
  - [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item <name> --format json`로 `signals.coverage.sufficient == true` 확인
  - [ ] 실패하면 해당 item만 Step 2–5를 1회 재시도(Fix H/J)
  - [ ] 재시도도 실패하면 category (a) genuine content gap(evidence: mining query 결과 + FR-2 시도 로그) 또는 category (b) process failure(evidence: 실패한 단계 trace)를 판정해 Implementation Notes에 기록하고 Fix G exception list 후보로 남긴다(category (b)는 이 task 안에서 버그로 재수정, exception 대상 아님)
- [ ] **Step 7 — Report**: AC3(신규 case 모두 `source` explicit, `description-derived` 0건), AC4(모든 collision의 `impostor`가 실제 anti-trigger clause와 일치), AC9(id가 `^<slug>-(pos|vs-[a-z0-9-]+|trace)-\d+$` 패턴 준수), AC10(신규 case가 기존/자기 자신과 legitimate 아닌 duplicate prompt 없음) 준수 여부와 dry-run 요약(Step 2)을 Implementation Notes에 기록

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-plan --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-brainstorm --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-tech-research --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-confidence-gate --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-spec-writer --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item ywc-spec-validate --format json`
- [ ] id 중복 없음: `python3 -c "import json; d=json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json')); ids=[c['id'] for c in d['cases']]; assert len(ids)==len(set(ids))"`
- [ ] `description-derived` source 신규 추가 0건

## Verification
- [ ] `git diff --stat .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`으로 이 task가 오직 그 파일만 변경했는지 확인
- [ ] JSON 유효성: `python3 -c "import json; json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json'))"`
- [ ] 위 6개 item 모두 `sufficient == true`이거나 evidence 첨부된 exception으로 기록됨
- [ ] 이 task는 코드/설정 변경이 아니므로 `bash scripts/validate.sh` / lint / build 대상 없음 — 위 JSON 유효성 + score.py 검증이 이 task의 완전한 검증

## Implementation Notes

**Open Question 2 dry-run summary (mining vs fallback yield)**: mining via `mcp__plugin_claude-mem_mcp-search__search` (`type: "prompts"`) over prior session history yielded clean, unambiguous hits for only 2 of 6 items (`ywc-plan`, `ywc-spec-validate` — both had genuine explicit `/ywc-<name>`-style invocations in transcript), plus partial/ambiguous hits for `ywc-brainstorm` that needed cross-referencing. `ywc-tech-research`, `ywc-confidence-gate`, `ywc-spec-writer` had no clean mined hits (unrelated project chatter dominated the search results) and were filled entirely by FR-2 fallback authoring. Final tally: **2/18 positives (11%) mined (`session-trace`), 16/18 (89%) fallback-authored (`user-prompt`)**. All 7 collisions are fallback-authored (`user-prompt`) since mining for a specific sibling-vs-sibling framing was not productive within this task's time budget; each collision's `impostor` was picked to trace a real `Do not use for ...` clause (AC4), and 6 of the 7 target items reach their 2-collision floor via cross-crediting (one collision entry credits both the `expected` and `impostor` name), so only 7 new collision cases were needed instead of 12. **Recommendation for the remaining 8 Phase 000082 tasks**: budget for a majority-fallback-authored mix (roughly 1 mined : 4-5 fallback-authored) rather than expecting mining to carry most of the floor.

**Fix applied post-review (Design subagent finding, `ywc-impl-review --git-range`)**: the first draft included 5 positives (`plan-pos-5`, `plan-pos-6`, `brainstorm-pos-5`, `spec-validate-pos-5`, `spec-validate-pos-6`) whose prompt text literally contained the target item's own identifier (`ywc-plan`, `/ywc-brainstorm`, `ywc-spec-validate`) — a direct violation of `trigger-eval-method.md`'s "Do not mine prompts that name the item" rule (a second way to build a case that cannot fail, parallel to the `description-derived` circularity problem this whole coverage-floor mechanism exists to prevent). Per "Sanitize, do not paraphrase," these were not edited in place (that would silently turn a real mined quote into a paraphrase while still claiming `session-trace` provenance) — instead all 5 were replaced with freshly authored intent-only prompts (`source: user-prompt`) that describe the request without naming the skill. Re-verified after the fix: no item drops below its coverage floor, no new id/prompt duplicates introduced, id-pattern (AC9) and collision-impostor (AC4) conformance unaffected.

**AC conformance**: AC3 (no `description-derived` among the 25 new cases) — confirmed, `git diff | grep -c '"source": "description-derived"'` → 0. AC4 (every collision `impostor` traces to a real anti-trigger clause) — confirmed by reading each of the 6 items' `SKILL.md` `Do not use for ...` text directly (see per-case `note` fields). AC7 (no duplicate ids across the file) — confirmed, 406 unique ids. AC9 (id pattern `^<slug>-(pos|vs-[a-z0-9-]+|trace)-\d+$`) — confirmed via regex scan. AC10 (no new-vs-existing or new-vs-new duplicate prompts) — confirmed; the only duplicate `prompt` values in the file are pre-existing legitimate positive+collision pairs from the original 381 cases (e.g. `commit-trace-4` / `commit-vs-createpr-trace-1` sharing one prompt) and do not involve any of this task's 25 new cases.

**`scripts/validate.sh` note**: this task's own Verification section declares `validate.sh`/lint/build out of scope (pure JSON data change). Ran it anyway as a sanity check; it reports one pre-existing, unrelated failure (`plugins/ywc-agent-toolkit/skills is stale` — a compiled `.pyc` byte-diff under `scripts/__pycache__/`) that is present identically on the base branch (`feature/eval-pr-161`, commit `208405f`) before this task's changes and touches only `plugins/ywc-agent-toolkit/skills/scripts/__pycache__/`, nothing in this task's Allowed Edit Scope. Not fixed here (out of scope; would require editing files outside `trigger-cases.json`) — flagging for the repo owner separately from this batch.
