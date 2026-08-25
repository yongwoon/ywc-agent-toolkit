# 000063-030-docs-auth-implement-verification — Implementation Checklist

## Prerequisites

- [ ] `000063-010-domain-auth-implement-skill` is merged.
- [ ] `000063-020-test-auth-implement-evals` is merged.

## Allowed Edit Scope

- [ ] No file edits expected, except a single-line entry in `claude-code/skills/README.md` **only if that file already exists** at execution time.
- [ ] Do not create `claude-code/skills/README.md` if it is absent — leave FR-9's catalog registration as a no-op in that case.
- [ ] Do not edit `SKILL.md`, `references/**`, `README*.md`, or `evals/**` — any needed fix there is out of this task's scope; stop and report to the owning task instead.

## Stop Conditions

- [ ] Stop and report to `000063-010` if `bash scripts/validate.sh` fails on `SKILL.md`, `references/**`, or `README*.md` content.
- [ ] Stop and report to `000063-020` if it fails on `evals/evals.json`.
- [ ] Stop if fixing the failure would require editing outside this task's Ownership.

## Implementation Steps

- [ ] Check catalog condition: `test -f claude-code/skills/README.md` — if it exists, add a one-line `ywc-auth-implement` entry consistent with existing entries; if it does not exist, skip (do not create it).
- [ ] Run the repository-wide gate: `bash scripts/validate.sh`.
- [ ] Run the spec's package-completeness checks: `evals.json` JSON-parse, 5 `references/*.md` files present, 4 README locale files present.
- [ ] Run the safety/contract checks: no `$ywc-code-gen`/`$ywc-*` leftover Codex syntax, §3.5 verbatim Return-payload contract present for all three named agents (`ywc-backend-coder`, `ywc-frontend-coder`, `ywc-doc-writer`), `ywc-verify-done` reference present.
- [ ] Run `git diff --check` last, after any catalog-registration edit from step 1.

## Task Verify

- [ ] `bash scripts/validate.sh`
- [ ] `python3 -m json.tool claude-code/skills/ywc-auth-implement/evals/evals.json >/dev/null`
- [ ] `for file in policy-interview.md security-checklist.md generic-fallback.md legal-pages-template.md rationalization-evidence.md; do test -f "claude-code/skills/ywc-auth-implement/references/$file"; done`
- [ ] `for file in README.md README.en.md README.ja.md README.ko.md; do test -f "claude-code/skills/ywc-auth-implement/$file"; done`
- [ ] `! rg -n '\$ywc-code-gen|\$ywc-' claude-code/skills/ywc-auth-implement`
- [ ] `for agent in ywc-backend-coder ywc-frontend-coder ywc-doc-writer; do rg -U -q "(?s)Task\(subagent_type: ${agent}\).*Return-payload contract" claude-code/skills/ywc-auth-implement/SKILL.md; done`
- [ ] `rg -q 'ywc-verify-done' claude-code/skills/ywc-auth-implement/SKILL.md`
- [ ] `git diff --check`

## Verification

- [ ] All Task Verify commands above exit 0 — this constitutes the spec's `## Verification` block in full (this repository has no separate lint/typecheck/test/build pipeline for skill-authoring changes).
