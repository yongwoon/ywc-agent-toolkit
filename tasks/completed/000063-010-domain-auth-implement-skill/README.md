# 000063-010-domain-auth-implement-skill

## Purpose

Build the Claude Code-native `ywc-auth-implement` skill source contract. It orchestrates a policy interview, dynamic battle-tested library recommendation, and TDD-disciplined implementation dispatch to existing Claude Code named agents (`ywc-backend-coder`, `ywc-frontend-coder`, `ywc-doc-writer`) — without implementing any application auth code itself.

## Scope

- Create `claude-code/skills/ywc-auth-implement/SKILL.md` with frontmatter (`name: ywc-auth-implement`, `description` ≤80 words per A15 with `(ywc) Use when...` / `Do not use for ...`, `category: spec`, `phase: planning`, `requires: []`, `advisor_budget: 2`).
- Write inline: Rationalization Defense table (≥5 rows), 5-item idempotent Preflight Gate, 9-category policy interview summary, dynamic recommendation logic, FR-6/FR-7 direct-dispatch prompts (each with the `references/subagent-status-actions.md` link and the §3.5 Return-payload contract quoted verbatim), FR-8 security/E2E/PR gate table, and the `## Output Format` 4-value Completion Status enum.
- Create 5 `references/*.md` files: `policy-interview.md`, `security-checklist.md`, `generic-fallback.md`, `legal-pages-template.md`, `rationalization-evidence.md`.
- Create the 4 Tier 1 README locale files (`README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`).

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude_auth_implement_skill.md#functional-requirements` — FR-1 through FR-9, the source of truth for this task's content
- `docs/ywc-plans/claude_auth_implement_skill.md#acceptance-criteria` — AC1–AC8, AC10 (AC9 belongs to `000063-020`)
- `docs/ywc-plans/claude_auth_implement_skill.md#edge-cases` — missing agent catalog, unknown-stack escalation, out-of-candidate OAuth provider, description length risk
- `claude-code/skills/CLAUDE.md` (§ "Subagent Return Payload Contract and Structured Surface-to-User") — defines the §3.5 contract this task must quote verbatim
- `claude-code/skills/references/subagent-status-actions.md` — the exact contract text to quote
- `claude-code/skills/ywc-skill-author/SKILL.md:48` (rule A15) — the 80-word description boundary rule
- `claude-code/skills/CLAUDE.md` (§ "Language Policy for Localized Documentation") — README locale writing rules

### Summary

The new skill is a Claude Code orchestration document set, not application auth code. It must prefer battle-tested libraries or managed services and never recommend hand-rolled password/token/secret crypto, gate on an existing-auth `new`/`extend`/`migrate` selection before any scaffolding or dispatch, dispatch implementation to `ywc-backend-coder`/`ywc-frontend-coder` under explicit `ywc-tdd-ritual` cycle instructions, dispatch legal-page drafts to `ywc-doc-writer` with a "draft pending legal review" notice, and gate E2E execution, PR suggestion, and recommendation caching behind a Critical/High-free `ywc-security-audit` result. No fixed or "supported" stack list may appear anywhere in the output.

### Out of Scope (from spec)

- `evals/evals.json` authoring (5 routing/safety scenarios) — handled by `000063-020-test-auth-implement-evals`
- Repository-wide `bash scripts/validate.sh` execution and the §3.5 verbatim-contract grep verification — handled by `000063-030-docs-auth-implement-verification`
- `claude-code/skills/README.md` catalog registration — the file does not exist in this repository; FR-9's "if it exists" condition is not triggered by this batch
- Actual application auth implementation, new Claude Code agent creation, stack-playbook seeding, legal approval, Codex bundle changes, manual `VERSION`/`CHANGELOG.md` edits — out of this feature entirely

## Criticality

`critical` — Ownership path `claude-code/skills/ywc-auth-implement/**` matches the security-sensitive keyword heuristic (`auth`); no spec "Critical Surfaces" section exists to declare this authoritatively, so this is a heuristic inference. This task authors the security-sensitive orchestration prompts themselves (FR-6/FR-7/FR-8: direct dispatch instructions, security-gate routing, legal-draft handling). Logged here per the fallback rule — downgrade to `normal` if review judges the authored content to be non-sensitive documentation only.

## Dependencies

### Depends On

- (None — root task)

### Depended By

- `000063-020-test-auth-implement-evals` — needs this task's final routing/policy/gate prose to write matching eval scenarios (happy path, existing-auth hard stop, unknown-stack routing, direct-crypto rejection, security-fail no-cache).
- `000063-030-docs-auth-implement-verification` — needs the finished skill tree for the full `bash scripts/validate.sh` run and the §3.5 verbatim-contract grep checks.

## Key Files

- `claude-code/skills/ywc-auth-implement/SKILL.md` — activation frontmatter, Rationalization Defense, Preflight, interview/recommendation summary, FR-6/FR-7 dispatch prompts, FR-8 gate table, Output Format
- `claude-code/skills/ywc-auth-implement/references/policy-interview.md` — 9-category interview detail (FR-4)
- `claude-code/skills/ywc-auth-implement/references/security-checklist.md` — security posture checklist backing FR-8
- `claude-code/skills/ywc-auth-implement/references/generic-fallback.md` — real-time research fallback when stack evidence is insufficient (FR-5)
- `claude-code/skills/ywc-auth-implement/references/legal-pages-template.md` — ToS/privacy-policy draft structure for the FR-7 dispatch
- `claude-code/skills/ywc-auth-implement/references/rationalization-evidence.md` — baseline/forward-test evidence for each Rationalization Defense row (FR-2)
- `claude-code/skills/ywc-auth-implement/README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`

## Notes

- Keep `SKILL.md` under ~500 lines; extract any section over ~30 lines to its matching reference per FR-1's extraction list — except the §3.5 dispatch prompts, Preflight Gate, FR-8 routing table, Rationalization Defense, and Output Format, which the spec requires to stay inline.
- `claude-code/skills/README.md` (root skill catalog) does not currently exist in this repository — do not create it in this task; FR-9's registration step is conditional on the file already existing.
- Do not introduce a fixed/supported-stack allowlist concept anywhere in `SKILL.md` or `references/` (AC5); route insufficient-evidence cases to `ywc-tech-research` instead.
- `ywc-tdd-ritual` is a discipline referenced inside the FR-6 dispatch prompts, not a dispatcher this skill calls "underneath" — phrase the prompts as instructing the dispatched agent to follow the cycle, not as a nested Task call.

## Parallel Execution Metadata

### Ownership

`claude-code/skills/ywc-auth-implement/{SKILL.md,README*.md,references/**}` (excludes `evals/**`, owned by `000063-020`)

### Shared Surfaces

- `claude-code/skills/references/subagent-status-actions.md` (read-only quote source — the §3.5 contract text must match verbatim)
- `claude-code/skills/ywc-skill-author/SKILL.md` A15 convention (read-only)
- `claude-code/agents/{ywc-backend-coder,ywc-frontend-coder,ywc-doc-writer,ywc-security-engineer}.md` (read-only — dispatch targets must exist and be named correctly)

### Conflicts With

- `000063-020-test-auth-implement-evals` until this task merges — eval fixtures depend on final routing/policy text.

### Parallelizable After

- (Root task — no predecessor required)

### Task Verify

- `test -f claude-code/skills/ywc-auth-implement/SKILL.md`
- `test "$(wc -l < claude-code/skills/ywc-auth-implement/SKILL.md)" -lt 500`
- `test "$(grep -c '^## ' claude-code/skills/ywc-auth-implement/references/policy-interview.md)" -ge 9`
- `rg -U -q "(?s)Task\(subagent_type: ywc-backend-coder\).*Return-payload contract" claude-code/skills/ywc-auth-implement/SKILL.md`
- `rg -U -q "(?s)Task\(subagent_type: ywc-frontend-coder\).*Return-payload contract" claude-code/skills/ywc-auth-implement/SKILL.md`
- `rg -U -q "(?s)Task\(subagent_type: ywc-doc-writer\).*Return-payload contract" claude-code/skills/ywc-auth-implement/SKILL.md`
- `rg -q 'DONE_WITH_CONCERNS' claude-code/skills/ywc-auth-implement/SKILL.md && rg -q 'NEEDS_CONTEXT' claude-code/skills/ywc-auth-implement/SKILL.md`
- `! rg -n '\$ywc-code-gen|\$ywc-' claude-code/skills/ywc-auth-implement`

## Out of Scope

`evals/evals.json` authoring, `claude-code/skills/README.md` catalog registration, repository-wide `bash scripts/validate.sh` execution, actual application auth implementation.
