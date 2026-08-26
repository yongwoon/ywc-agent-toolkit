# 000027-040-refactor-agent-context-compaction — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] Working tree changes outside this task's Ownership are reviewed and left untouched.

## Allowed Edit Scope
- [ ] Edit only `codex/skills/ywc-onboard-repo/**` and `codex/skills/ywc-agentic/**`.

## Stop Conditions
- [ ] Stop if onboarding changes require modifying root `AGENTS.md` in this repository.
- [ ] Stop if compaction guidance needs executor state changes outside `ywc-agentic`.
- [ ] Stop if existing skill text already contains a conflicting stronger rule.

## Implementation Steps
- [ ] Update `codex/skills/ywc-onboard-repo/SKILL.md`.
  - [ ] Add agent-context pre-check alongside existing Phase 1 reconnaissance passes.
  - [ ] Include `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.cursor/rules/`, and `.github/copilot-instructions.md`.
  - [ ] Expand Output B or equivalent write step to reconcile existing files before writing or enhancing `AGENTS.md`.
  - [ ] State that new guidance must not contradict existing agent-context rules.
- [ ] Update `codex/skills/ywc-agentic/SKILL.md`.
  - [ ] Add long-run compaction guidance from iteration 6 or when 5+ iterations accumulate.
  - [ ] Instruct agents to keep one-line iteration digests in working context.
  - [ ] Treat `agentic-log.md` as durable source of truth for prior details.

## Task Verify
- [ ] `rg -n "AGENTS.md|\\.cursorrules|\\.cursor/rules|copilot-instructions" codex/skills/ywc-onboard-repo/SKILL.md`
- [ ] `rg -n "iteration 6|5\\+ iterations|agentic-log.md|one-line iteration" codex/skills/ywc-agentic/SKILL.md`

## Verification
- [ ] Repository validation is deferred to `000028-010-infra-plugin-sync-validation`.
- [ ] `git diff --name-only` for this task contains only `codex/skills/ywc-onboard-repo/**` and `codex/skills/ywc-agentic/**`.
