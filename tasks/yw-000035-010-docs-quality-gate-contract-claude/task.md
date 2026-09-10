# yw-000035-010-docs-quality-gate-contract-claude — Implementation Checklist

## Prerequisites
- [ ] None — root task.

## Allowed Edit Scope
- [ ] Stay within declared Ownership: `claude-code/skills/references/quality-gates.md` only.
- [ ] If any other file needs to change, stop and report before proceeding.

## Stop Conditions
- [ ] Stop if `claude-code/skills/references/quality-gates.md` already exists with conflicting content at task start.
- [ ] Stop if the codex `quality-gates.md` at `codex/skills/references/quality-gates.md` cannot be located for structural cross-reference.

## Implementation Steps
- [ ] Read `codex/skills/references/quality-gates.md` (existing, from the prior codex batch) once for structural awareness only — do not copy or translate its content; the claude-code contract is a structurally different, canonical-first document per FR-1.
- [ ] Create `claude-code/skills/references/quality-gates.md` with these sections, in order:
  - [ ] `## 1. Purpose` — states the gate exists to enforce complexity/testability on new or changed code, opt-in per project via the spec's `## Quality Gate Contract` declaration.
  - [ ] `## 2. Roles` — Cleaner (CRAP/complexity gate, dispatches to `ywc-refactor-cleaner`) and Hardener (Mutation/test-effectiveness gate, dispatches to `ywc-qa-engineer`).
  - [ ] `## 3. Thresholds` — CRAP Complexity 6–8 with rationale, Mutation Score ≥90%.
  - [ ] `## 4. Diff-only principle` — gates apply only to the diff introduced by the current task, never retroactively to the full codebase.
  - [ ] `## 5. Mutation loop cap` — at most 3 rounds of Hardener dispatch per task/wave; remaining survivors after round 3 are forwarded to review, never silently dropped.
  - [ ] `## 6. Equivalent-mutant policy` — a surviving mutant believed equivalent is still forwarded to review as a survivor; equivalence is a human/reviewer call, never adjudicated by the executor or dispatched agent.
  - [ ] `## 7. Contract-absent fallback` — `N/A — no quality gate contract` skips every gate step cleanly; the sentinel every consuming SKILL.md section must check for.
  - [ ] `## 8. Baseline convention` — `Baseline` is a per-adopting-project artifact; this toolkit never creates, seeds, or writes to that file under any condition.
  - [ ] `## 9. gate_state sentinel vocabulary` — enumerate exact strings: `"not run — contract absent"`, `"not run — tool unavailable"`, `"not run — dispatch failed"`, plus the normal pass/fail states.
  - [ ] `## 10. Tooling exclusion` — this document defines no CRAP/Mutation tool installation steps, CLI flags, or per-language tool names; deferred to each adopting project's own contract.
- [ ] Add a one-line framing note (matching `pr-bot-polling.md` / `subagent-async-monitoring.md`) that this is a shared reference, linked-not-restated by consuming SKILL.md files.

## Task Verify
- [ ] `test -f claude-code/skills/references/quality-gates.md`
- [ ] `grep -q "CRAP" claude-code/skills/references/quality-gates.md && grep -q "Mutation" claude-code/skills/references/quality-gates.md`
- [ ] `grep -q "gate_state" claude-code/skills/references/quality-gates.md`
- [ ] `grep -c "^## " claude-code/skills/references/quality-gates.md` shows at least 10 top-level sections

## Verification
- [ ] `bash scripts/validate.sh` exits 0
- [ ] No lint/typecheck/build/test toolchain applies — this repository is a skill/prompt distribution toolkit; `scripts/validate.sh` is the only verification gate.
