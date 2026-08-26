# yw-000005-010-infra-next-task-number-initials-scan

## Purpose
Make PHASE allocation collision-proof: scope the scan to one collaborator's initials, union every linked worktree, and reserve the chosen number atomically before returning it.

## Scope
Extend `next-task-number.sh` to `next-task-number.sh [tasks-dir] [initials]` with initials-scoped candidate matching, worktree union with path normalization, legacy seeding, scoped drift cross-check, `git update-ref` reservation with retry, and collection of the existing-initials advisory list.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#fr3--채번-스캔의-initials-한정--worktree-union--legacy-seed-ac3-ac4-ac5` — scan contract
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#a2--fr6-신설-phase의-원자적-예약-critical-2-대응-q1-종결` — git-ref reservation, with measured `exit=0` / `exit=128` evidence
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#a3--fr3의-graph-교차검증-scope-한정-critical-3-대응` — drift-check scoping
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#a6--worktree-union-경로-정규화-warning-3-대응` — path normalization
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#a9--q2-종결-initials-충돌-감지는-디스크-스캔-목록-제시로-한정-suggestion-1-대응` — advisory list source
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#acceptance-criteria` — AC3, AC4, AC5, AC11, AC12

### Summary
Today's allocator takes "highest local PHASE + 1", which cannot detect a concurrent run: two worktrees compute the same number, produce different slugs, and collide with no merge conflict to surface it. Namespacing by initials removes the cross-person case structurally; `git update-ref <ref> HEAD ''` closes the same-person case, because the empty old-value is an atomic create-if-absent CAS shared across every linked worktree via the git common dir. A losing caller increments and retries. Reservation refs are never released — they are a local allocation ledger, and a burned number is preferred over a reused one. Two secondary corrections matter as much: the drift cross-check must be initials-scoped and skipped entirely when the graph has zero entries for those initials (otherwise this repository warns on every single run, since it already carries a measured drift of graph `000083` vs directories `000081`), and `tasks-dir` must be relativized against `git rev-parse --show-toplevel` before being joined to a worktree path.

### Out of Scope (from spec)
- Parser regexes in the other three scripts — handled by `yw-000004-020-infra-parser-optional-initials-prefix`.
- SKILL.md prose — handled by `yw-000005-020-docs-task-generator-skill-initials`.
- Migrating existing legacy IDs (spec §A7: do not migrate).

## Criticality
normal

## Dependencies
### Depends On
- `yw-000004-010-docs-initials-resolution-reference` — defines the numbering scope and validation rules this script implements.
- `yw-000004-020-infra-parser-optional-initials-prefix` — `scaffold-task-dir.sh` must already accept the prefixed names this allocator will produce.

### Depended By
- `yw-000005-020-docs-task-generator-skill-initials` — SKILL.md cites this script's new signature and behavior.
- `yw-000006-010-docs-task-generator-artifacts-sync` — templates and evals describe this allocation behavior.
- `yw-000007-010-infra-validation-gate` — final no-regression gate.

## Key Files
- `claude-code/skills/ywc-task-generator/scripts/next-task-number.sh`
- Fixture directories and a throwaway linked worktree used for AC3/AC4/AC5 verification

## Notes
- Measured current state of this repository (spec AC3): `next-task-number.sh tasks` returns `000082-010` — directory max `000081`, graph max `000083`. The first prefixed batch for a new collaborator must therefore seed from the **directory** scan, not the graph.
- Reservation refs live under `refs/ywc/task-phase/<initials>/<phase>`, outside `refs/heads/`, so they are not pushed, not fetched, and do not appear in `git branch -a`.
- Retry cap is 100; on exhaustion exit 1 and report the ref count under `refs/ywc/task-phase/<initials>/`, since reaching it implies ledger corruption.
- A separate clone does not share the git common dir and therefore cannot see reservations. That residual risk is accepted and must be stated in the script comments, not silently omitted.
- NFR1: with no `initials` argument the script must behave exactly as it does today. NFR2: macOS default tooling only — `git update-ref` is used precisely because `flock` is unavailable.

## Hardening Evidence
### Test Feedback Path
- RED-first target: fixture directories containing `ab-000050-010-x` (must be ignored when resolving `yk`), a linked-worktree-only `yk-000012-010-x` (must raise the max), and a legacy-only tree (must seed from legacy max + 1).

### Interface Contract
- Contract: `next-task-number.sh [tasks-dir] [initials]` → stdout `NNNNNN-NNN`, drift warnings on stderr.
- Inputs: optional tasks directory (relative or absolute), optional initials.
- Outputs: the allocated `PHASE-SEQUENCE` pair; unchanged when `initials` is omitted.
- Error model: exit 1 on reservation retry exhaustion; missing worktree paths are skipped silently, not errors.
- Impacted tests: fixture-based AC3/AC4/AC5/AC11 runs.

### Critical Surface Review
- Review requirement: N/A for security. The spec nonetheless mandates fixture-based before/after verification because a scan regression silently corrupts numbering.

### Data Integrity Hardening
- Trigger surface: the PHASE counter is shared mutable state across worktrees — this is exactly the concurrency case the spec exists to close.
- Atomic / locking strategy: `git update-ref "refs/ywc/task-phase/<initials>/<phase>" HEAD ''` — the empty old-value is an atomic create-if-absent CAS; the loser increments and retries.
- Transaction boundary: one ref creation per allocation attempt; no multi-ref write.
- Idempotency guard: reservations are never released, so a crashed run burns its number rather than allowing reuse.
- Required tests: AC11 — a second `update-ref` against the same ref must exit non-zero and drive the caller to `N+1`.

## Parallel Execution Metadata
### Ownership
- `claude-code/skills/ywc-task-generator/scripts/next-task-number.sh`
- Fixture directories created by this task

### Shared Surfaces
- PHASE allocation contract
- `refs/ywc/task-phase/**` reservation ledger
- `tasks/dependency-graph.md` drift-warning behavior

### Conflicts With
- `yw-000005-020-docs-task-generator-skill-initials` — SKILL.md must quote this script's final signature, so the two must not be authored concurrently.

### Parallelizable After
- `yw-000004-010-docs-initials-resolution-reference`, `yw-000004-020-infra-parser-optional-initials-prefix`

### Task Verify
- `shellcheck claude-code/skills/ywc-task-generator/scripts/next-task-number.sh`
- `bash .../next-task-number.sh tasks` (no initials) returns the same value as the pre-change build — NFR1
- Fixture with `ab-000050-010-x` only: `next-task-number.sh <fixture> yk` ignores `ab-` (AC4)
- Fixture with legacy-only IDs: seeds from legacy max + 1 (AC3)
- Linked-worktree fixture holding `yk-000012-010-x`: returns `000013-010` (AC5)
- `git update-ref refs/ywc/task-phase/yk/000099 HEAD ''` twice — second call exits non-zero (AC11)

## Out of Scope
- Garbage-collecting burned reservation refs.
- Cross-clone coordination.
