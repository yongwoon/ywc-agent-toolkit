# 000063-030-docs-auth-implement-verification

## Purpose

Run the full repository validation gate over the finished `ywc-auth-implement` skill package and verify the §3.5 verbatim Return-payload contract, catalog conditions, and the spec's own Verification script all pass before the feature is considered done.

## Scope

- Run `bash scripts/validate.sh` (repository-wide) and confirm it exits 0 with `claude-code/skills/ywc-auth-implement/` included.
- Confirm the §3.5 verbatim Return-payload contract is present for exactly the three direct-dispatch prompts (`ywc-backend-coder`, `ywc-frontend-coder`, `ywc-doc-writer`) — `ywc-security-audit` (FR-8) is a skill call, not a §3.5 target, and is excluded from this grep per AC10.
- Confirm no Codex-only command syntax (`$ywc-code-gen`, `$ywc-*`) leaked into the new skill directory.
- Confirm `claude-code/skills/README.md` still does not require registration (file absent) or, if it now exists because another concurrent task created it, register `ywc-auth-implement` there.
- Run the spec's own `## Verification` shell block verbatim.

## Spec Reference

### Primary Sources

- `docs/ywc-plans/claude_auth_implement_skill.md#verification` — the exact shell block this task executes
- `docs/ywc-plans/claude_auth_implement_skill.md#acceptance-criteria` — AC1, AC9, AC10 (package/deploy/validation criteria)
- `scripts/validate.sh` — the repository-wide gate this task runs

### Summary

This task performs no new authoring — it is the final read-only gate confirming `000063-010` and `000063-020`'s combined output satisfies the spec's package, contract, and safety acceptance criteria. Any failure here means returning to the owning task (`000063-010` or `000063-020`), not patching around the gate.

### Out of Scope (from spec)

- Skill body, references, README authoring — `000063-010-domain-auth-implement-skill`
- Eval scenario authoring — `000063-020-test-auth-implement-evals`
- Creating `claude-code/skills/README.md` if it does not exist — FR-9's registration step is conditional and this task must not originate that file

## Criticality

`normal` — this task is validation-only; it does not author or modify the security-sensitive orchestration content itself (that ownership sits with `000063-010`/`000063-020`). No write ownership over `claude-code/skills/ywc-auth-implement/**` content is granted here beyond the conditional catalog-registration case.

## Dependencies

### Depends On

- `000063-010-domain-auth-implement-skill` — provides the finished `SKILL.md`, references, and READMEs to validate.
- `000063-020-test-auth-implement-evals` — provides the finished `evals.json` required by `scripts/validate.sh` and the spec's JSON-parse check.

### Depended By

- (None — terminal task in this batch)

## Key Files

- No new files expected, unless `claude-code/skills/README.md` already exists at execution time, in which case add a one-line entry for `ywc-auth-implement` there.

## Notes

- If `bash scripts/validate.sh` fails, identify whether the failure belongs to `000063-010`'s output (skill body/README) or `000063-020`'s output (evals) and report back to that task rather than editing outside this task's Ownership.
- The spec's Verification block includes `git diff --check` — run it only after this task's own (if any) catalog-registration edit, so it reflects the true final diff.

## Parallel Execution Metadata

### Ownership

None (read-only validation) — conditionally `claude-code/skills/README.md` (single-line addition) only if that file already exists.

### Shared Surfaces

Entire `claude-code/skills/ywc-auth-implement/**` tree (read-only), `scripts/validate.sh` (read-only), `claude-code/skills/README.md` (conditional single-line write).

### Conflicts With

`000063-010-domain-auth-implement-skill` and `000063-020-test-auth-implement-evals` until both merge — this task must run against their final, merged output.

### Parallelizable After

`000063-010-domain-auth-implement-skill`, `000063-020-test-auth-implement-evals`

### Task Verify

- `bash scripts/validate.sh`
- `python3 -m json.tool claude-code/skills/ywc-auth-implement/evals/evals.json >/dev/null`
- `for file in policy-interview.md security-checklist.md generic-fallback.md legal-pages-template.md rationalization-evidence.md; do test -f "claude-code/skills/ywc-auth-implement/references/$file"; done`
- `for file in README.md README.en.md README.ja.md README.ko.md; do test -f "claude-code/skills/ywc-auth-implement/$file"; done`
- `! rg -n '\$ywc-code-gen|\$ywc-' claude-code/skills/ywc-auth-implement`
- `for agent in ywc-backend-coder ywc-frontend-coder ywc-doc-writer; do rg -U -q "(?s)Task\(subagent_type: ${agent}\).*Return-payload contract" claude-code/skills/ywc-auth-implement/SKILL.md; done`
- `rg -q 'ywc-verify-done' claude-code/skills/ywc-auth-implement/SKILL.md`
- `git diff --check`

## Out of Scope

Authoring or modifying `SKILL.md`, `references/**`, `README*.md`, or `evals/**` content; creating `claude-code/skills/README.md` if absent.
