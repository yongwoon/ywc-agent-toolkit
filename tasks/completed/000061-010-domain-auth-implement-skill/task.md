# Implementation Task — 000061-010-domain-auth-implement-skill

## Prerequisites

- [ ] No predecessor task is required.
- [ ] Read `docs/ywc-plans/codex_auth_implement_skill.md` and `codex/AGENTS.md`.

## Allowed Edit Scope

Only `codex/skills/ywc-auth-implement/{SKILL.md,agents/**,README*.md,references/**}`. Do not create `evals/**`, update catalogs, edit root READMEs, or alter generated plugin files.

## Stop Conditions

- [ ] The workflow requires a Claude-only agent or unavailable Codex skill.
- [ ] The body cannot fit below 500 lines without moving static material to a directly linked reference.
- [ ] A requirement needs a fixed stack allowlist, application auth implementation, or secret example.

## Hardening Gate

- [ ] Record `evals/evals.json` as the downstream RED-first feedback target before drafting prompt text.
- [ ] Define the status-output interface and audit/E2E transition contract before routing prose.
- [ ] Treat authentication orchestration as a critical surface and complete full manual review; Data Integrity is N/A.

## Implementation Steps

- [ ] Create `SKILL.md` with strict Codex frontmatter and Rationalization Defense.
  - [ ] Include triggers/anti-triggers, read-only preflight, nine policy sections, selected-method scoping, and dynamic research fallback.
  - [ ] Specify `$ywc-plan → $ywc-spec-ready → $ywc-task-generator → $ywc-code-gen --spec ... --feature ... --tdd --review`; print but never auto-invoke task generation.
- [ ] Encode security and completion gates.
  - [ ] Forbid direct JWT/password/secret crypto recommendations and secret output.
  - [ ] Reuse code-gen audit evidence, skip E2E/PR/cache after Critical/High, and state one literal terminal status.
- [ ] Add focused `references/` documents and link shared `../references/subagent-status-actions.md` without copying it.
- [ ] Create `agents/openai.yaml` from the final body and six sibling README locale files; verify the same commands and scope.

## Task Verify

- [ ] `test -f codex/skills/ywc-auth-implement/agents/openai.yaml`
- [ ] `test "$(wc -l < codex/skills/ywc-auth-implement/SKILL.md)" -lt 500`
- [ ] `bash scripts/check-codex-skill-descriptions.sh --paths a-m`
- [ ] `rg -n '\$ywc-task-generator|DONE_WITH_CONCERNS|NEEDS_CONTEXT' codex/skills/ywc-auth-implement/SKILL.md`

## Verification

- [ ] Run the Task Verify checklist.
- [ ] Run `bash scripts/validate.sh` after generated package synchronization by `000062-010`.
