# 000070-020-refactor-impl-review-merge-base — Implementation Checklist

## Prerequisites
- [ ] `000070-010-domain-ywc-implement-skill` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-impl-review/**`.
- [ ] Do not edit callers or generated package output.

## Stop Conditions
- [ ] Stop if existing target modes cannot remain behaviorally compatible.
- [ ] Stop if the Phase 1 worker prompt path does not expose one consistent three-dot boundary.
- [ ] Stop if the report cannot distinguish supplied ref from resolved merge-base.

## Hardening Gate
- [ ] Classify as a public review-contract refactor.
- [ ] Add failing structural eval cases before changing the contract.
- [ ] Record target inputs, outputs, and `NEEDS_CONTEXT` errors in the interface contract.
- [ ] Require full review because this changes a shared review boundary.

## Implementation Steps
- [ ] Extend the argument table with mutually exclusive `--base <ref>` and reject missing or mixed target modes before reading files.
- [ ] Specify `git rev-parse --verify <ref>^{commit}` and `git merge-base <ref> HEAD` failure handling.
- [ ] Require non-empty `git diff --name-only <merge-base>...HEAD` and use the same three-dot range for patch and final contents sent to every Phase 1 worker.
- [ ] Add supplied-ref and resolved-merge-base fields to the report header.
- [ ] Preserve explicit `--git-range A..B`, `--code`, and `--working-tree` behavior and document the distinction.
- [ ] Add eval cases for valid base, unresolved ref, no merge-base, empty diff, mixed modes, worker propagation, and explicit-range compatibility.
- [ ] Regenerate `agents/openai.yaml` only if the final `SKILL.md` description changes.

## Task Verify
- [ ] `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-impl-review`
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`

## Verification
- [ ] Lint/structure checks pass through `bash scripts/run-codex-skill-contract-evals.sh`.
- [ ] No unrelated review references or worker rubrics change.

## Implementation Notes
