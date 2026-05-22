# Claude Code Agent Catalog

이 디렉토리는 `claude-code/agents/` Catalog 의 한국어 entry point 입니다.
Agent file 작성 규칙은 [CLAUDE.md](./CLAUDE.md) 를 참조하십시오.

## Catalog Overview

이 Catalog 는 Claude Code 의 **Task tool subagent dispatch** 또는
**Claude Agent SDK** 를 통해 호출 가능한 명명된 (named) Worker Agent 집합을
보관합니다. 각 Agent 는 독립된 Context window 에서 실행되는 single-responsibility
worker 이며, Skill 의 fan-out parallel/sequential dispatch 대상으로 설계되었습니다.

**현재 시점 정책**

- Tier 1 (worker) — Backend / Frontend / QA Engineer / Doc Writer 4종 운영
- Tier 2 (language reviewer) — TypeScript (Sonnet) / Python (Sonnet) / Go (Sonnet) 3종 운영, Swift / Rust 등은 추후 follow-up PR
- Tier 3 (specialist) — Architect (Opus) / Security Engineer (Sonnet) / Refactor Cleaner (Sonnet) / Root-cause Analyst (Opus) / Performance Engineer (Sonnet) 5종 운영, 추가 specialist 는 추후 follow-up PR
- Catalog 동기 범위 — `claude-code/` 한정 (Codex / pi-skills 에는 적용 불가)

Tier 정의와 dispatch 흐름은 spec 문서
[`docs/superpowers/specs/2026-05-21-ywc-agent-toolkit-design.md`](../../../docs/superpowers/specs/2026-05-21-ywc-agent-toolkit-design.md)
의 Iteration 0 §2 (Persona Definitions) 와 Iteration 4 §P3 (Built-in vs Custom)
을 참조합니다.

## Per-Agent Summary

> 아래 표는 본 Catalog 에 실제로 land 된 Agent 들입니다 (Tier 1 worker 4종 + Tier 2 language reviewer 3종 + Tier 3 specialist 5종). 각 Agent body
> 의 정식 frontmatter, Mission, Boundaries, Return Contract 는 해당 `<agent-name>.md`
> 파일에서 확인할 수 있습니다.

| Name | Tier | Model | Mission |
|------|------|-------|---------|
| `ywc-backend-coder` | 1 (worker) | sonnet | Server-side code: API / Business logic / Database integration |
| `ywc-frontend-coder` | 1 (worker) | sonnet | Client-side code: UI / State / Routing / a11y |
| `ywc-qa-engineer` | 1 (worker) | sonnet | Test code: Unit / Integration / E2E, edge case authoring. tests/ 외부 수정 금지 |
| `ywc-doc-writer` | 1 (worker) | haiku | 문서 / Comment / Release note 작성. Bash tool 제외 |
| `ywc-typescript-reviewer` | 2 (language reviewer) | sonnet | TypeScript-specific code review (read-only). Type system depth (generics, conditional types, satisfies), async correctness, framework idioms (React hooks / Vue / Svelte), tsconfig strictness, ESM/CJS interop. ywc-impl-review Phase 1 (TS-heavy diff) / Phase 2 (Design 또는 type-system advisor) 에서 dispatch |
| `ywc-python-reviewer` | 2 (language reviewer) | sonnet | Python-specific code review (read-only). Type system depth (Protocol / TypedDict / TypeGuard / Self / ParamSpec, mypy strict mode), asyncio correctness (gather / create_task / cancellation), framework idioms (Django ORM / FastAPI / Pydantic v2 / Flask), GIL implications (ProcessPoolExecutor vs threadpool), lifecycle patterns (context manager / generator / `__init__.py`). ywc-impl-review Phase 1 (Python-heavy diff) / Phase 2 (Design 또는 type-system advisor) 에서 dispatch |
| `ywc-go-reviewer` | 2 (language reviewer) | sonnet | Go-specific code review (read-only). Goroutine lifecycle (leak / context cancellation / errgroup), channel patterns (close ownership / select / chan struct{}), interface design (accept interfaces return concrete / small interface), error wrapping (`fmt.Errorf %w` / `errors.Is` / `errors.As`), pointer vs value semantics (method set / escape analysis), generics post 1.18, lifecycle (defer / sync primitives / race detection). ywc-impl-review Phase 1 (Go-heavy diff) / Phase 2 (concurrency 또는 interface-design advisor) 에서 dispatch |
| `ywc-architect` | 3 (specialist) | opus | Architectural decision worker (read-only). Trade-off 분석 + 모듈 boundary / dependency direction / 추상화 판단 verdict 반환. ywc-plan / ywc-impl-review Phase 2 / ywc-confidence-gate 에서 dispatch |
| `ywc-security-engineer` | 3 (specialist) | sonnet | Static security review worker (read-only). OWASP Top 10 + threat modeling + secret/PII scan, severity-rated findings + 구체 remediation. ywc-security-audit / ywc-impl-review Phase 1 Security subagent / ywc-incident-postmortem 에서 dispatch |
| `ywc-refactor-cleaner` | 3 (specialist) | sonnet | Dead-code 제거 worker (coder tier — writes). SAFE 분류된 worklist 를 받아 per-item grep 검증 + 전후 test 실행 + 1-deletion-per-commit 으로 정리. ywc-refactor-clean Step 3 에서 dispatch |
| `ywc-root-cause-analyst` | 3 (specialist) | opus | Root-cause analyst (read-only). 5 Whys + hypothesis tracking + primary cause vs contributing factor 분리 + "architecture wrong vs fix harder" gate. ywc-debug-rootcause Phase 1 / Phase 3 (3+ failed fixes), ywc-incident-postmortem Step 4 에서 dispatch |
| `ywc-performance-engineer` | 3 (specialist) | sonnet | Performance review worker (read-only). 4 axes: Backend (N+1 / index / hot loop / sync IO / allocation / lock), Frontend (bundle / render-block / image / hydration / CSS specificity), Web Vitals (LCP / INP / CLS / FCP / TBT vs project targets), Profiling recommendations (py-spy / chrome devtools / node --prof / pprof / perf / JFR / dotnet-trace — recommend invocation, do not execute). ywc-impl-review Phase 2 advisor pass 의 Performance-related Architecture / Devex candidate 에서 dispatch |

각 Agent body 의 정확한 frontmatter, Mission 문구, Boundaries, Return Contract 는
`claude-code/agents/<agent-name>.md` 에서 직접 확인할 수 있습니다. 본
Catalog 의 Agent 들은 [`ywc-code-gen`](../skills/ywc-code-gen/),
[`ywc-parallel-executor`](../skills/ywc-parallel-executor/),
[`ywc-sequential-executor`](../skills/ywc-sequential-executor/),
[`ywc-agentic`](../skills/ywc-agentic/) (Step 5) 에서 named dispatch
(`subagent_type: ywc-<name>`) 됩니다.

## Frontmatter Rule

Agent file 의 frontmatter 는 strict YAML parser 에서 valid 해야 하며, canonical
form 은 다음과 같습니다:

```yaml
---
name: <agent-name>
description: >-
  <mission summary>. Triggers: "<dispatch entry points>". Do not use for:
  "<anti-triggers>".
model: sonnet
tools: [Read, Write, Edit, Bash, Grep, Glob]
---
```

**camelCase warning** — `permissionMode`, `maxTurns`, `initialPrompt`,
`mcpServers` 네 개 key 만 camelCase 이며, 나머지는 모두 lowercase 입니다. 자세한
규칙은 [CLAUDE.md](./CLAUDE.md) 의 "camelCase Warning" section 을 참조하십시오.

**Return Contract** — Agent 의 응답 형식은
[`claude-code/skills/references/subagent-status-actions.md`](../skills/references/subagent-status-actions.md)
§3.5 의 4-state payload (`DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` /
`NEEDS_CONTEXT`) 를 따르며, Agent body 안에서 새 format 을 invent 하지 않습니다
(Iteration 6 §R1).

## Install Commands

```bash
# 모든 Agent 를 ~/.claude/agents/ 에 설치 (Catalog 전체)
bash claude-code/agents/scripts/install.sh

# 설치 가능한 Agent 목록 출력
bash claude-code/agents/scripts/install.sh --list

# Usage 출력
bash claude-code/agents/scripts/install.sh --help

# 실제 복사 없이 어떤 동작이 일어날지만 확인
bash claude-code/agents/scripts/install.sh --dry-run

# 목적지 override (테스트 용)
CLAUDE_AGENTS_DIR=/tmp/test-agents bash claude-code/agents/scripts/install.sh
```

설치된 Agent 는 `~/.claude/agents/<agent-name>.md` 에 위치하며, 모든 Claude Code
session 에서 즉시 dispatch 가능합니다. **Global namespace 주의**: 동일한 이름의
Agent 가 다른 source 에서 설치되면 마지막 installer 의 내용으로 덮어쓰여집니다.
프로젝트 specific Agent 는 `ywc-` prefix 를 유지하여 충돌을 줄이는 것이 권장
사항입니다.

## Related Skills

본 Catalog 의 Agent 는 다음 Skill 에서 dispatch 됩니다:

**Tier 1 worker fan-out (Phase 6 이후)**

- [`ywc-code-gen`](../skills/ywc-code-gen/) — Phase 1 parallel generation step
- [`ywc-parallel-executor`](../skills/ywc-parallel-executor/) — Wave-mode task execution
- [`ywc-sequential-executor`](../skills/ywc-sequential-executor/) — Sequential task execution
- [`ywc-agentic`](../skills/ywc-agentic/) — Step 5 Execute Phase

**Tier 2 language-specific reviewer dispatch**

- [`ywc-typescript-reviewer`](./ywc-typescript-reviewer.md) ← [`ywc-impl-review`](../skills/ywc-impl-review/) (Phase 1 Design / Devex subagent on TS-heavy diff, Phase 2 type-system advisor)
- [`ywc-python-reviewer`](./ywc-python-reviewer.md) ← [`ywc-impl-review`](../skills/ywc-impl-review/) (Phase 1 Design / Devex subagent on Python-heavy diff, Phase 2 type-system / asyncio / framework advisor)
- [`ywc-go-reviewer`](./ywc-go-reviewer.md) ← [`ywc-impl-review`](../skills/ywc-impl-review/) (Phase 1 Design / Devex subagent on Go-heavy diff, Phase 2 concurrency / interface-design / error-wrapping advisor)

**Tier 3 specialist advisory dispatch**

- [`ywc-architect`](./ywc-architect.md) ← [`ywc-plan`](../skills/ywc-plan/) (architecture-significant decision), [`ywc-impl-review`](../skills/ywc-impl-review/) (Phase 2 advisor candidate from Architecture subagent), [`ywc-confidence-gate`](../skills/ywc-confidence-gate/) (architecture dimension <70 escalation)
- [`ywc-security-engineer`](./ywc-security-engineer.md) ← [`ywc-security-audit`](../skills/ywc-security-audit/) (dedicated worker), [`ywc-impl-review`](../skills/ywc-impl-review/) (Phase 1 named Security subagent), [`ywc-incident-postmortem`](../skills/ywc-incident-postmortem/) (security boundary incident)
- [`ywc-refactor-cleaner`](./ywc-refactor-cleaner.md) ← [`ywc-refactor-clean`](../skills/ywc-refactor-clean/) (Step 3 SAFE deletion loop worker — per-item grep + test before/after + 1-deletion-per-commit)
- [`ywc-root-cause-analyst`](./ywc-root-cause-analyst.md) ← [`ywc-debug-rootcause`](../skills/ywc-debug-rootcause/) (Phase 1 hypothesis assembly, Phase 3 architecture-suspicion gate after 3+ failed fixes), [`ywc-incident-postmortem`](../skills/ywc-incident-postmortem/) (Step 4 5-Whys walk)
- [`ywc-performance-engineer`](./ywc-performance-engineer.md) ← [`ywc-impl-review`](../skills/ywc-impl-review/) (Phase 2 advisor pass on Performance-related Architecture / Devex candidate — Backend latency / Frontend bundle / Web Vitals regression / Profiling recommendation)

각 Skill 의 SKILL.md 안에서 `subagent_type: ywc-<name>` 형식으로 명명 dispatch
합니다.
