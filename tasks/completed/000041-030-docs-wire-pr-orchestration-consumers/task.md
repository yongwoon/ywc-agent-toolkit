# Task: 000041-030-docs-wire-pr-orchestration-consumers

## Prerequisites

- [ ] `000040-010-docs-codex-language-resolution-reference` is completed.

## Allowed Edit Scope

- [ ] Stay within:
  - `codex/skills/ywc-create-pr/**`
  - `codex/skills/ywc-agentic/**`
  - `codex/skills/ywc-finish-branch/**`
  - `codex/skills/ywc-sequential-executor/**`
  - `codex/skills/ywc-parallel-executor/**`
- [ ] Do not edit artifact-generation skills or root docs.

## Stop Conditions

- [ ] Stop if `--title` verbatim behavior would be broken.
- [ ] Stop if a caller/callee pair would resolve language twice with conflicting results.
- [ ] Stop if executor PR language policy cannot preserve explicit `--pr-lang`.

## Hardening Gate

- [ ] Classify this task as docs-only behavior-contract update.
- [ ] Record named exception: no RED-first test; use targeted grep and validation.
- [ ] Record interface contract: generated PR/orchestrated prose follows shared language resolution unless explicit flag/content wins.
- [ ] Data Integrity fields are N/A.
- [ ] Critical surface review is N/A.

## Implementation Steps

- [ ] Update `ywc-create-pr`.
  - [ ] Link shared `language-resolution.md`.
  - [ ] Keep explicit `--lang` and `--language` first.
  - [ ] Resolve omitted language from project/user config before asking.
  - [ ] Preserve explicit `--title` verbatim; use resolved language for generated body prose.
  - [ ] Remove any generated-title/body English default.
- [ ] Update `ywc-agentic`.
  - [ ] Clarify `--pr-lang auto` uses shared resolution before recent PR heuristics.
  - [ ] Clarify task/spec `--lang` forwarding uses explicit user request or shared config.
  - [ ] Preserve forwarding of explicit `en|ja|ko|zh|es` unchanged.
- [ ] Update PR-language executor chain.
  - [ ] `ywc-finish-branch`: omitted/auto `--pr-lang` uses shared resolution before heuristic sources.
  - [ ] `ywc-sequential-executor`: omitted/auto `--pr-lang` uses shared resolution before heuristic sources.
  - [ ] `ywc-parallel-executor`: omitted/auto `--pr-lang` uses shared resolution before heuristic sources.
  - [ ] Keep branch names, task IDs, commands, labels, code blocks, and machine identifiers unchanged.
- [ ] Update README locale files in touched skill directories when they document old language defaults.

## Task Verify

- [ ] `grep -q "language-resolution.md" codex/skills/ywc-create-pr/SKILL.md`
- [ ] `grep -q "language-resolution.md" codex/skills/ywc-agentic/SKILL.md`
- [ ] `grep -q "language-resolution.md" codex/skills/ywc-finish-branch/SKILL.md`
- [ ] `grep -q "language-resolution.md" codex/skills/ywc-sequential-executor/SKILL.md`
- [ ] `grep -q "language-resolution.md" codex/skills/ywc-parallel-executor/SKILL.md`
- [ ] `rg -n "recent PR|dominant language|auto-detect" codex/skills/ywc-agentic codex/skills/ywc-finish-branch codex/skills/ywc-sequential-executor codex/skills/ywc-parallel-executor`

## Verification

- [ ] `bash scripts/validate.sh`
