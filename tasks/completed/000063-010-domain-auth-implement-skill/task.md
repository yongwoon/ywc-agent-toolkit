# 000063-010-domain-auth-implement-skill — Implementation Checklist

## Prerequisites

- [ ] No predecessor task is required (root task).
- [ ] Read `docs/ywc-plans/claude_auth_implement_skill.md` in full.
- [ ] Read `claude-code/skills/CLAUDE.md` (Writing Rules, Language Policy, Subagent Return Payload Contract sections) and `claude-code/skills/references/subagent-status-actions.md`.
- [ ] Confirm `claude-code/agents/{ywc-backend-coder,ywc-frontend-coder,ywc-doc-writer,ywc-security-engineer}.md` all exist (`ls claude-code/agents/`).

## Allowed Edit Scope

- [ ] Stay within `claude-code/skills/ywc-auth-implement/{SKILL.md,README*.md,references/**}` — do not create `evals/**` (owned by `000063-020`).
- [ ] Do not create or edit `claude-code/skills/README.md` — it does not exist in this repository and FR-9's catalog step is conditional on it already existing.
- [ ] If a change is needed outside this scope, stop and report before proceeding.

## Stop Conditions

- [ ] Stop and return `BLOCKED` if any of `ywc-backend-coder`/`ywc-frontend-coder`/`ywc-doc-writer`/`ywc-security-engineer` is missing from `claude-code/agents/` — do not inline-implement a substitute (spec Edge Cases).
- [ ] Stop if `SKILL.md` cannot fit under ~500 lines without moving a spec-mandated inline section (§3.5 dispatch prompts, Preflight Gate, FR-8 table, Rationalization Defense, Output Format) out to a reference — report and ask before improvising an exception.
- [ ] Stop if a requirement would need a fixed/supported-stack list or a stack-playbook seed — the spec explicitly forbids this (AC5, FR-5).

## Implementation Steps

- [ ] Scaffold the skill directory using `ywc-skill-author` conventions.
  - [ ] Create `claude-code/skills/ywc-auth-implement/SKILL.md` with frontmatter: `name: ywc-auth-implement`, `description` (≤80 words, `(ywc) Use when...` / `Do not use for ...`, per A15), `category: spec`, `phase: planning`, `requires: []`, `advisor_budget: 2`.
  - [ ] Create `README.md` (Korean prose, English technical terms), `README.en.md`, `README.ja.md`, `README.ko.md` per `claude-code/skills/CLAUDE.md` Writing Rules.
- [ ] Write the Rationalization Defense and Preflight Gate inline in `SKILL.md` (FR-2, FR-3).
  - [ ] ≥5 Excuse/Reality rows rejecting: skipping the interview for OAuth-only, hand-rolled crypto being faster, deferring MFA, caching before security/E2E pass, presenting a legal draft as final.
  - [ ] 5-item idempotent Preflight Gate: branch reuse, non-destructive `.env.example` placeholders, `ywc-tech-research` routing on insufficient stack evidence, `new`/`extend`/`migrate` hard-stop on existing auth, "draft pending legal review" labeling.
- [ ] Write the policy interview and dynamic recommendation content (FR-4, FR-5).
  - [ ] `references/policy-interview.md` with ≥9 `## ` sections (method/OAuth, MFA, session, password/hashing boundary, profile, deactivation, shallow-RBAC, consent, abuse prevention), each recording question / response-default / approval-deferral state.
  - [ ] Inline summary in `SKILL.md` plus `references/generic-fallback.md`: dynamic recommendation from stack evidence + approved policy only, zero fixed-stack-list language, routes to `ywc-tech-research` when evidence is insufficient.
- [ ] Write the FR-6/FR-7 direct-dispatch prompts inline in `SKILL.md`.
  - [ ] `Task(subagent_type: ywc-backend-coder)` and `Task(subagent_type: ywc-frontend-coder)` prompts instructing the `ywc-tdd-ritual` RED → Verify RED → GREEN → Verify GREEN → REFACTOR → Verify GREEN cycle and a `ywc-verify-done` completion check, each immediately followed by the `references/subagent-status-actions.md` link and the §3.5 Return-payload contract quoted **verbatim**.
  - [ ] `Task(subagent_type: ywc-doc-writer)` prompt for ToS/privacy-policy drafts and consent-checkbox UI requirements, same link + verbatim contract, with an explicit "draft pending legal review" instruction (FR-3 item 5).
- [ ] Write the FR-8 gate table and the Output Format contract inline in `SKILL.md`.
  - [ ] Security/E2E/PR routing table: Critical/High 0 → proceed to policy-conditional E2E; Critical/High ≥1 → `DONE_WITH_CONCERNS`, skip E2E/PR/cache; audit command failure → `BLOCKED`; insufficient scope → `NEEDS_CONTEXT`.
  - [ ] `## Output Format` section with the literal `DONE` / `DONE_WITH_CONCERNS` / `BLOCKED` / `NEEDS_CONTEXT` enum, matching `claude-code/skills/references/subagent-status-actions.md` Status Responses structure.
- [ ] Write the remaining references: `references/security-checklist.md`, `references/legal-pages-template.md`, `references/rationalization-evidence.md` (baseline + forward-test evidence per Rationalization Defense row, no application code execution required).

## Task Verify

- [ ] `test -f claude-code/skills/ywc-auth-implement/SKILL.md`
- [ ] `test "$(wc -l < claude-code/skills/ywc-auth-implement/SKILL.md)" -lt 500`
- [ ] `test "$(grep -c '^## ' claude-code/skills/ywc-auth-implement/references/policy-interview.md)" -ge 9`
- [ ] `rg -U -q "(?s)Task\(subagent_type: ywc-backend-coder\).*Return-payload contract" claude-code/skills/ywc-auth-implement/SKILL.md`
- [ ] `rg -U -q "(?s)Task\(subagent_type: ywc-frontend-coder\).*Return-payload contract" claude-code/skills/ywc-auth-implement/SKILL.md`
- [ ] `rg -U -q "(?s)Task\(subagent_type: ywc-doc-writer\).*Return-payload contract" claude-code/skills/ywc-auth-implement/SKILL.md`
- [ ] `rg -q 'DONE_WITH_CONCERNS' claude-code/skills/ywc-auth-implement/SKILL.md && rg -q 'NEEDS_CONTEXT' claude-code/skills/ywc-auth-implement/SKILL.md`
- [ ] `! rg -n '\$ywc-code-gen|\$ywc-' claude-code/skills/ywc-auth-implement`

## Verification

- [ ] No `package.json`/lint/typecheck/test/build commands apply — this repository is a documentation/skill-authoring toolkit. The equivalent gate for this task is the Task Verify checklist above plus:
- [ ] `npx markdownlint-cli2 --config /tmp/ml.json "claude-code/skills/ywc-auth-implement/README*.md"` (using the same MD-rule disables as `.github/workflows/markdownlint.yml`)
- [ ] Full `bash scripts/validate.sh` is deferred to `000063-030` (it also requires `evals/evals.json` from `000063-020`), but confirm this task's own README/SKILL frontmatter checks would pass in isolation before handing off.
