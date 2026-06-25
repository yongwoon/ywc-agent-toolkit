# Task: 000029-040-refactor-agent-context-compaction

## Prerequisites

- [ ] batch 단일 branch에서 작업 중인지 확인
- [ ] upstream 참조: `gh pr diff 134 --repo yongwoon/develop-with-llm` (agentic/onboard 경로만)
- [ ] es/zh 부재 확인: `ls claude-code/skills/ywc-onboard-repo/README.es.md` → 없음(신규 생성 대상)

## Allowed Edit Scope

- `claude-code/skills/ywc-agentic/SKILL.md`
- `claude-code/skills/ywc-onboard-repo/**`
- 그 외 경로 편집 금지(특히 sequential-executor — `000029-030` 담당, `codex/**`).

## Stop Conditions

- agentic README를 생성/수정하려는 충동 발생 시 중단(이 batch 범위 밖).
- onboard-repo에 이미 AGENTS.md reconcile 문구가 존재하면 중단.

## Implementation Steps

- [ ] `ywc-agentic/SKILL.md`: `### Step 9: Completion Report` 직전에 "**Compaction on long runs (context engineering).**" 문단 삽입. 요지: iteration 6+ (또는 ≥5 누적) 시 `agentic-log.md`를 source of truth로, working context에는 one-line-per-iteration digest만 유지. `[../references/subagent-status-actions.md](../references/subagent-status-actions.md)` §3.5 참조.
- [ ] `ywc-onboard-repo/SKILL.md`: Rationalization Defense에 "There's an AGENTS.md but I only Read the CLAUDE.md" 1행 추가.
- [ ] `ywc-onboard-repo/SKILL.md`: Phase 1에 "Agent-context pre-check (not a 7th pass)" 문단 추가 — `CLAUDE.md`/`AGENTS.md`/`.cursorrules`/`.cursor/rules/`/`.github/copilot-instructions.md` Glob.
- [ ] `ywc-onboard-repo/SKILL.md`: Phase 4(Output B)에 AGENTS.md reconcile 문단 추가 — 기존 AGENTS.md를 Read하여 모순 없는 CLAUDE.md 생성, AGENTS.md emit은 Codex variant 담당(의도적 divergence).
- [ ] `ywc-onboard-repo/SKILL.md`: Validation 체크리스트에 "기존 AGENTS.md/.cursorrules/copilot-instructions를 Read·reconcile" 1행 추가.
- [ ] `ywc-onboard-repo/README.{md,en,ja,ko}.md`: Output B에 reconcile 절 추가(편집).
- [ ] `ywc-onboard-repo/README.es.md`, `README.zh.md`: **신규 생성** — README.en 기준 es/zh 번역 seed + Output B reconcile 절 반영.

## Task Verify

- [ ] `rg -n "Compaction on long runs" claude-code/skills/ywc-agentic/SKILL.md` (>0)
- [ ] `rg -c "AGENTS.md" claude-code/skills/ywc-onboard-repo/SKILL.md` (≥3: Rationalization + Phase1 + Phase4)
- [ ] `rg -n "Agent-context pre-check" claude-code/skills/ywc-onboard-repo/SKILL.md` (>0)
- [ ] `ls claude-code/skills/ywc-onboard-repo/README.{es,zh}.md` (둘 다 존재)
- [ ] `rg -n "AGENTS.md" claude-code/skills/ywc-onboard-repo/README.{es,zh}.md` (>0 each)
- [ ] `wc -l claude-code/skills/ywc-onboard-repo/SKILL.md` (≤500)

## Verification

- [ ] `bash scripts/validate.sh` (4-locale set 통과 — es/zh는 추가분이라 미검출이나 frontmatter/구조는 통과)
- [ ] `npx markdownlint-cli2 --config /tmp/ml.json "claude-code/skills/ywc-onboard-repo/README*.md"` (신규 es/zh 포함 0 errors)
- [ ] `git diff --name-only` + 신규파일이 `ywc-agentic/SKILL.md`, `ywc-onboard-repo/` 내부로만 한정(특히 `codex/` 미포함)
