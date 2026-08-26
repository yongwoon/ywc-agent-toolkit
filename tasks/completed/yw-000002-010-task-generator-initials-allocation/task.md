# yw-000002-010-task-generator-initials-allocation — Implementation Checklist

## Prerequisites
- [ ] `yw-000001-010-config-initials-writer` is completed and merged.
- [ ] `yw-000001-030-parser-prefixed-task-ids` is completed and merged.

## Allowed Edit Scope
- [ ] Stay within `codex/skills/ywc-task-generator/**` and its task-allocation contract.

## Stop Conditions
- [ ] Stop if linked-worktree scanning would inspect an absolute or escaping tasks path.
- [ ] Stop if legacy IDs would be renamed or counted as another collaborator's namespace.
- [ ] Stop if a reservation cannot be shared through the repository common Git directory.

## Hardening Gate
- [ ] Record RED-first generator contract evidence before changing allocation behavior.
- [ ] Record the task ID and `NEEDS_CONTEXT` interface contract.
- [ ] Apply Data Integrity Hardening for the serialized allocation and durable reservation.
- [ ] Require full implementation review before completion.

## Implementation Steps
- [ ] Add `references/collaborator-initials.md` documenting validation, config precedence, interactive derivation, and non-interactive blocking behavior.
- [ ] Update `SKILL.md` to resolve initials before scans, lock the common Git directory, and scope numbering to `^<initials>-<phase>-<sequence>-` candidates.
- [ ] Implement corresponding-path discovery from `git worktree list --porcelain`, including inaccessible/mismatched source reporting and repository-relative tasks-dir validation.
- [ ] Add compare-and-create reservation attempts under `refs/ywc/task-phase/<initials>/<phase>`, retrying collisions with the next candidate and preserving consumed reservations.
- [ ] Update naming, ledger, preview, and task-directory rules so new output is prefixed while legacy references remain accepted.
- [ ] Add fixtures for config precedence, malformed tiers, linked worktrees, scoped max selection, empty graphs, and concurrent reservations.

## Task Verify
- [ ] Run focused task-generator contract evals.
- [ ] Run temporary linked-worktree scan fixtures for active/completed/graph sources.
- [ ] Run the concurrent reservation fixture and verify distinct PHASEs.
- [ ] Verify missing initials returns `NEEDS_CONTEXT` before any task artifact write.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — Markdown/Python/Bash skill tooling)
- [ ] unit tests pass (focused generator fixtures)
- [ ] integration tests pass (temporary Git/worktree reservation fixtures)
- [ ] app builds without error (N/A — documentation/tooling repository)
