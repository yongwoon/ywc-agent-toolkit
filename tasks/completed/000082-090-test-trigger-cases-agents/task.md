# Task: 000082-090-test-trigger-cases-agents

## Prerequisites
- [ ] `000082-080-test-trigger-cases-testing-misc`가 완료(머지)되었는지 확인 — `cases` 배열 길이 증가분 확인 (Fix X gate)

## Allowed Edit Scope
- `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`만 편집한다(append-only).

## Collision Case Convention (Fix F2 override — verbatim, must appear in this task's dispatch context)
> "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."

## Stop Conditions
- `000082-080`이 실제로 머지되지 않았거나 `cases` 배열이 예상 개수만큼 늘지 않았으면 멈추고 보고한다.
- 편집 범위가 `trigger-cases.json` 밖으로 번지면 멈추고 보고한다.
- skill을 collision sibling으로 사용하려는 시도가 생기면(root mismatch) 멈추고 보고한다.
- 13개 agent를 2개 이상의 task로 나누려는 유혹이 생기면 멈춘다 — AC8은 단일 task를 요구한다.

## Implementation Steps
- [ ] **Step 1 — Id-inventory (Fix C2/S/Z)**: 13개 agent 각각에 대해 `<slug>-` prefix query와 `agent-<slug>-` prefix query를 모두 실행(Fix Z, agent 계열은 `agent-` 접두어 legacy id가 존재), hit<3이면 field-based(`expected`/`impostor`) fallback query 병행해 `max_n` 결정
- [ ] **Step 2 — Mining pass, 확장(FR-1 + Open Question 1, Fix E2/Fix R)**: agent별로
  - [ ] 표준 mining(`session_search` / `mcp-search`(`type: "prompts"`) / grep fallback) 실행, 5-rule 필터 적용
  - [ ] **확장**: `claude-code/skills/**/SKILL.md`를 grep해 `Task(subagent_type=<agent>)` 호출을 실제로 유발하는 caller skill의 자연어 trigger 문장을 찾는다. agent 자신의 `.md` 정의를 재서술한 것이 아니라 caller skill 쪽 실제 조건/트리거 문구여야 한다. 발견 시 `"source": "session-trace"`로 기록하고 `note`에 caller skill 이름을 남긴다
  - [ ] 생존 hit sanitize 후 positive/collision 분류 (collision sibling은 다른 12개 agent 중에서만)
- [ ] **Step 3 — Fallback authoring (FR-2, Fix F2)**: mining+확장으로도 3 positive / 2 collision을 못 채운 agent에 대해 `user-prompt`로 hand-author. agent 요청은 "이 코드 Go 리뷰해줘" 같은 사용자 문장 또는 caller skill이 실제로 dispatch할 법한 상황 서술 중 하나를 자연스럽게 선택
- [ ] **Step 4 — Dedup (Fix A2 step 4a + Fix L + Fix V)**: 기존 381개 + `000082-010`~`000082-080`의 case + 이 task 자신의 output(13개 item)과 대조, legitimate pair 제외 duplicate 제거
- [ ] **Step 5 — Append + numbering**: `max_n + 1`부터 순번 매겨 `cases` 배열 끝에 append
- [ ] **Step 6 — Per-item verify + remediation (Fix M/W/T, Fix P/X)**: `score.py --target claude-code/agents --item <name>`로 확인, 실패 시 1회 재시도, 재실패 시 category (a)/(b) 판정 + evidence 첨부하여 Fix T exception 후보로 기록(AC12: agent exception이 있으면 AC2 목표를 `13 − |agent exceptions|`로 조정한다고 명시)
- [ ] **Step 7 — Report**: AC3/AC4/AC8(13개 단일 batch)/AC9/AC10/AC12 준수 여부를 Implementation Notes에 기록

## Task Verify
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-architect --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-backend-coder --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-frontend-coder --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-qa-engineer --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-doc-writer --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-cloud-engineer --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-refactor-cleaner --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-go-reviewer --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-python-reviewer --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-typescript-reviewer --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-performance-engineer --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-root-cause-analyst --format json`
- [ ] `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/agents --item ywc-security-engineer --format json`
- [ ] id 중복 없음 확인
- [ ] `description-derived` source 신규 추가 0건

## Verification
- [ ] `git diff --stat .claude/skills/ywc-toolkit-eval/evals/trigger-cases.json`으로 오직 그 파일만 변경했는지 확인
- [ ] JSON 유효성 확인
- [ ] 13개 agent 모두 `sufficient == true`이거나 evidence 첨부된 exception(Fix T)으로 기록됨
- [ ] 코드/설정 변경 없음 — lint/build/validate.sh 대상 아님

## Implementation Notes

All 58 new cases (39 positives + 19 collisions) fallback-authored (`source: user-prompt`) covering all 13 agents in this single task (AC8 satisfied — no 2-batch split). Did not pursue the Open Question 1 dispatch-trigger-mining extension (grepping `claude-code/skills/**/SKILL.md` for caller-side natural-language trigger phrases that would count as `session-trace`-equivalent) given the batch's already-large scope (13 items); all positives are plain FR-2 fallback-authored user requests instead, which is an explicitly valid path per the task's own Step 3.

**AC4/L003 applied strictly from the start** (per the correction from `000082-080`): every one of the 19 new collision cases was verified programmatically — `expected`'s own `.md` `Do not use for ...` clause must literally contain `impostor`'s identifier — before being written, using the exact same automated check pattern that caught `000082-080`'s regression. Zero violations on the first pass this time.

**Root constraint (agent↔agent only) enforced programmatically**: every collision case asserts both `expected` and `impostor` are in the 13-agent set before being written — no skill↔agent pairing was attempted. Several **pre-existing baseline** entries for these 13 agents (not part of this diff, not fixed — out of append-only scope) are skill↔agent violations discovered during id-inventory: `go-reviewer-vs-impl-review-1`, `python-reviewer-vs-impl-review-1`, `typescript-reviewer-vs-impl-review-1`/`impl-review-vs-typescript-reviewer-1`, `doc-writer-vs-project-docs-1`/`project-docs-vs-doc-writer-1`, `doc-writer-vs-ubiquitous-language-1`, `skill-author-vs-doc-writer-1` (already known from `000082-080`), `qa-engineer-vs-tdd-ritual-1`/`tdd-ritual-vs-qa-engineer-1`, `e2e-test-strategy-vs-qa-engineer-1`/`gen-testcase-vs-qa-engineer-1`, `refactor-clean-vs-refactor-cleaner-1`/`refactor-cleaner-vs-refactor-clean-1` (already known from `000082-030`), `security-engineer-vs-security-audit-1`/`security-audit-vs-security-engineer-1`, `debug-rootcause-vs-root-cause-analyst-1`, `incident-postmortem-vs-root-cause-analyst-1`. All `description-derived`, so none count toward any floor — flagging for the repo owner's awareness only.

Some real agent↔agent anti-triggers are **asymmetric even where both sides mention the same language-reviewer family**: e.g. `ywc-python-reviewer`'s own clause lists "TypeScript / Go / Swift / Rust have their own Tier 2 reviewers" without the `ywc-` prefix, so it does not literally name `ywc-go-reviewer`/`ywc-typescript-reviewer` — those two directions were sourced from `ywc-go-reviewer`'s and `ywc-typescript-reviewer`'s own clauses instead (which do use the full `ywc-*` identifier), never from `python-reviewer`'s side.

No exceptions needed — all 13 agents reached `sufficient: true` (`positives: 3` each, `collisions` ranging 2–6). AC3/AC7/AC9/AC10 confirmed via the same automated checks used in prior tasks.
