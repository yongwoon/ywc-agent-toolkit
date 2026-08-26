# 000016-050-docs-custom-agent-bounded-evidence — Implementation Checklist

## Prerequisites
Verify these before starting:
- [ ] `000016-010-docs-principles-guideline-gap` is completed (merged).

## Allowed Edit Scope
- [ ] Stay within `codex/agents/*.toml`.
- [ ] Edit `codex/agents/README.md` only if it is needed to keep custom agent docs accurate.
- [ ] If the task requires model/tooling changes, stop and report.

## Stop Conditions
- [ ] Stop if a change would alter agent models, sandbox behavior, or tool permissions.
- [ ] Stop if a language/security/performance/root-cause specialization would be weakened.
- [ ] Stop if broad reformatting is needed; use minimal TOML prompt edits instead.

## Implementation Steps
- [ ] Add or normalize bounded-evidence wording in all seven `codex/agents/*.toml` files.
  - Related AC/FR: AC7, FR-5
  - Contract / Behavior Change: agents stay within supplied evidence packet and repository context.
  - Verification Command / Evidence: `rg -n "bounded evidence|evidence packet|repository context" codex/agents/*.toml`
- [ ] Add or normalize no-invention wording for files, APIs, runtime behavior, metrics, exploit paths, and code owner intent.
  - Related AC/FR: AC7, FR-5
  - Contract / Behavior Change: agents do not invent facts outside provided evidence.
  - Verification Command / Evidence: `rg -n "invent|do not infer|do not assume|missing evidence" codex/agents/*.toml`
- [ ] Add or normalize `NEEDS_CONTEXT` behavior when correctness depends on missing evidence.
  - Related AC/FR: AC7, FR-5
  - Contract / Behavior Change: agents ask for missing context instead of producing false certainty.
  - Verification Command / Evidence: `rg -n "NEEDS_CONTEXT" codex/agents/*.toml`
- [ ] Confirm role specializations remain intact.
  - Related AC/FR: AC8, FR-5
  - Contract / Behavior Change: each reviewer/analyst still focuses on its assigned domain.
  - Verification Command / Evidence: review `git diff -- codex/agents`
- [ ] Run the Codex agent list command.
  - Related AC/FR: AC11, FR-7
  - Contract / Behavior Change: edited TOML files remain install/list compatible.
  - Verification Command / Evidence: `bash scripts/install.sh --list --codex-agents`

## Task Verify
- [ ] Run `rg -n "bounded evidence|NEEDS_CONTEXT|invent|adjacent|evidence packet" codex/agents/*.toml`.
- [ ] Run `bash scripts/install.sh --list --codex-agents`.

## Verification
- [ ] Targeted grep checks pass for all seven agents.
- [ ] Agent list command exits 0.
- [ ] Full repository validation is deferred to `000017-010-infra-codex-karpathy-validation`.
