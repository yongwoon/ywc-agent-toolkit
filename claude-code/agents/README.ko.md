# Claude Code Agent Catalog (요약)

`claude-code/agents/` Catalog 의 한국어 요약본입니다. Authoring rule 전체는
[CLAUDE.md](./CLAUDE.md), 사용 가이드 전체는 [README.md](./README.md) 를 참조
하십시오.

## Catalog Overview

본 Catalog 는 Claude Code 의 Task tool subagent dispatch 또는 Claude Agent SDK
에서 호출 가능한 named Worker Agent 의 집합입니다. 각 Agent 는 독립된 Context
window 에서 실행되며, Skill 의 fan-out (parallel / sequential) dispatch 대상으로
설계되었습니다.

- 동기화 범위: `claude-code/` 한정 (Codex / pi-skills 미적용)
- Tier 정의: Tier 1 (worker), Tier 2 (language reviewer), Tier 3 (specialist)
- 현재 상태: Tier 1 4종 + Tier 2 3종 (TypeScript / Python / Go) + Tier 3 5종 (Architect / Security Engineer / Refactor Cleaner / Root-cause Analyst / Performance Engineer) land 완료 (`<agent-name>.md` 각 파일에서 본문 확인)

## Per-Agent Summary

| Name | Tier | Model | Mission |
|------|------|-------|---------|
| `ywc-backend-coder` | 1 | sonnet | Server-side code generation (API / Business / DB) |
| `ywc-frontend-coder` | 1 | sonnet | Client-side code generation (UI / State / Routing) |
| `ywc-qa-engineer` | 1 | sonnet | Test code authoring (Unit / Integration / E2E) |
| `ywc-doc-writer` | 1 | haiku | 문서 / Comment / Release note (no Bash) |
| `ywc-typescript-reviewer` | 2 | sonnet | TypeScript-specific code review (read-only). Type system / async / framework idioms / tsconfig strictness / ESM-CJS interop. ywc-impl-review Phase 1 (TS-heavy diff) / Phase 2 (type-system advisor) 에서 dispatch |
| `ywc-python-reviewer` | 2 | sonnet | Python-specific code review (read-only). Type system (Protocol / TypedDict / TypeGuard / mypy strict) / asyncio / framework idioms (Django / FastAPI / Pydantic v2 / Flask) / GIL / lifecycle. ywc-impl-review Phase 1 (Python-heavy diff) / Phase 2 (type-system advisor) 에서 dispatch |
| `ywc-go-reviewer` | 2 | sonnet | Go-specific code review (read-only). Goroutine lifecycle / channel patterns / interface design / error wrapping (`%w` / `errors.Is` / `errors.As`) / pointer vs value semantics / generics 1.18+ / defer + sync 정상. ywc-impl-review Phase 1 (Go-heavy diff) / Phase 2 (concurrency / interface-design advisor) 에서 dispatch |
| `ywc-architect` | 3 | opus | Architectural decision worker (read-only). Trade-off / boundary / dependency direction verdict. ywc-plan / ywc-impl-review Phase 2 / ywc-confidence-gate 에서 dispatch |
| `ywc-security-engineer` | 3 | sonnet | Static security review worker (read-only). OWASP Top 10 + threat modeling + secret/PII scan. ywc-security-audit / ywc-impl-review Phase 1 / ywc-incident-postmortem 에서 dispatch |
| `ywc-refactor-cleaner` | 3 | sonnet | Dead-code 제거 worker (coder tier). SAFE worklist → per-item grep + 전후 test + 1-deletion-per-commit. ywc-refactor-clean Step 3 에서 dispatch |
| `ywc-root-cause-analyst` | 3 | opus | Root-cause analyst (read-only). 5 Whys + hypothesis tracking + "architecture wrong vs fix harder" gate. ywc-debug-rootcause Phase 1/3, ywc-incident-postmortem Step 4 에서 dispatch |
| `ywc-performance-engineer` | 3 | sonnet | Performance review (read-only). Backend (N+1 / index / hot loop / sync IO / allocation) + Frontend (bundle / render-block / image / CSS) + Web Vitals (LCP / INP / CLS / FCP / TBT) + Profiling recommendation (py-spy / chrome devtools / pprof). ywc-impl-review Phase 2 advisor 에서 dispatch |

Tier 1 worker file 은 `000005-010-domain-tier1-worker-agents` task 에서 land 되었으며 `ywc-code-gen` / `ywc-parallel-executor` / `ywc-sequential-executor` / `ywc-agentic` (Step 5) 에서 named dispatch 됩니다. Tier 3 specialist (architect / security-engineer) 는 advisor-style dispatch 로 별도 skill 에서 호출됩니다.
