# Task Completion Checkout Preflight

> Status: Draft
> Scale: Medium
> Created: 2026-11-05
> Author: Codex
> Spec Reference: N/A — standalone improvement based on the task completion investigation

## Global Constraints

- Codex skills under `codex/skills/` are the source of truth; the marketplace package under `plugins/ywc-agent-toolkit/skills/` is generated from them. (`codex/AGENTS.md:12`)
- Local bundle validation is `bash scripts/validate.sh`; Codex plugin synchronization uses `bash scripts/sync-codex-plugin.sh`. (`AGENTS.md:14-19`, `CLAUDE.md:31`)
- Codex `SKILL.md` frontmatter contains only `name` and `description`. (`AGENTS.md:22`)
- Task completion must be reported only after the documented move and post-move verification succeed. (`codex/skills/ywc-finish-branch/SKILL.md:99,289`)

## Purpose

Task completion moves were present in successful executor history, while the repository root used during investigation was a bare Git repository and could not provide normal worktree status. A separate session then acted on stale root-level task copies, creating confusion about whether the executor had completed the move. This change makes the parallel executor establish and validate its task-owning checkout before it inspects or mutates task files, and stop when that context cannot be proven.

## Scope

- Specify a fail-closed invocation preflight for `ywc-parallel-executor` that requires execution from a non-bare Git worktree containing the selected task directory before any task reads, task moves, or completion reporting.
- Require successful Git command exit status and validate the reported repository root and `core.bare` state; an empty or missing `git status` result from a failed command is not evidence of a clean checkout.
- Define deterministic selection: use the current invocation checkout only; do not guess among linked worktrees or redirect execution to another path. If the current checkout is bare, invalid, or does not contain the selected task directory, stop with `NEEDS_CONTEXT` and report the evidence needed to continue from the correct checkout.
- Bind task discovery, completion `ywc-finish-branch` invocation, and post-move checks to that same validated checkout.
- Add focused regression coverage for a bare controller despite an available linked worktree, a valid current task-owning checkout, and Git command failure. Keep source-contract assertions clearly distinguished from executable runtime evidence.
- Synchronize the generated Codex plugin package from `codex/skills/` and verify parity.

## Success Oracle

- **Target:** Parallel task execution cannot inspect or mark tasks complete from a bare or non-owning checkout.
- **Quality threshold:** A valid task-owning invocation proceeds; a bare/non-owning context or failed Git probe stops before task mutation; completion retains the existing finish-branch move and postcondition checks.
- **Evidence required:** Isolated temporary Git fixtures for valid and rejected contexts, a failed-probe fixture asserting no task/index mutation, executor contract evidence, and source/generated package validation.
- **Stop condition:** Handoff is complete only when all ACs pass, the task-move contract remains unchanged, and source/package validation succeeds. If the current checkout cannot be identified safely, the executor returns `NEEDS_CONTEXT` without mutation.

## Out of Scope

- Changing `core.bare`, converting the repository root to a worktree, or automatically checking out branches.
- Repairing or moving existing task directories, resetting the index, or reconciling stale task copies.
- Changing `ywc-finish-branch` completion semantics, task lifecycle states, delivery modes, or the explicit gitignored `tasks/` move handling.
- Redesigning general executor routing, sequential executor behavior, Claude Code behavior, or worktree cleanup behavior.
- Claiming that the initial missing-move symptom was caused by a failure in the completion move itself; the observed history contains successful archive commits.

## Existing Constraints Touched

| Existing artifact | Behavior (verified by reading the file) | New code's interaction |
|---|---|---|
| `codex/skills/ywc-parallel-executor/SKILL.md:103-107` | Preflight requires a clean working tree and audits stale worktrees before creation. | Extend this preflight to validate that the current invocation checkout is non-bare and owns the selected tasks; preserve existing cleanliness and audit checks. |
| `codex/skills/ywc-parallel-executor/SKILL.md:220-229` | Worktree creation is delegated to `ywc-worktrees`; resolved task worktree paths and roots are recorded for resume. | Keep creation/resume destination resolution distinct from selecting the checkout that owns task metadata. |
| `codex/skills/ywc-parallel-executor/SKILL.md:360` | Completion marker flow requires the move, marker commit, push, and post-move checks; nonzero means BLOCKED. | Invoke this flow only in the validated task-owning checkout and propagate any context or command failure as blocked/needs-context. |
| `codex/skills/ywc-finish-branch/SKILL.md:99,289` | Tracked task directories use `git mv`; gitignored task directories use its explicit plain-move exception; both require marker commit and postcondition verification. | Preserve this contract unchanged; do not add a second filesystem-only move path to the executor. |
| `codex/skills/ywc-worktrees/SKILL.md:58-72` | `resolve` selects a destination root according to `.worktrees/`, `CLAUDE.md` `worktree_root`, and fallback configuration. | Do not treat destination-root resolution as proof of the current/task-owning checkout. |
| `scripts/validate.sh:142,331-345` | Validation invokes contract checks and verifies generated Codex package freshness. | Extend/add focused checks and retain the documented sync/validation workflow. |

## Quality Gate Contract

N/A — no quality gate contract. Existing planning, verification, review, and delivery workflow remains in effect.

## Module Boundaries

| Module | Owner | Consumers | Responsibility |
|---|---|---|---|
| `codex/skills/ywc-parallel-executor/` | Codex skill maintainers | Parallel task-range execution | Define checkout selection, validation, and fail-closed behavior before task access/mutation. |
| `tests/` focused executor contract coverage | Repository maintainers | `scripts/validate.sh` and contributors | Verify expected selection and failure behavior without mutating the developer repository. |
| `plugins/ywc-agent-toolkit/skills/` | Generated artifact | Marketplace plugin users | Mirror source skill changes; no direct-first edits. |

## Acceptance Criteria

- [ ] **AC-1 — Bare controller is rejected**: When invocation begins from a bare controller even if a linked worktree exists, executor stops before task access and returns `NEEDS_CONTEXT`, identifying the current path as bare and requiring invocation from the task-owning worktree.
- [ ] **AC-2 — Current checkout does not own tasks**: When the current non-bare checkout lacks the selected task directory, executor stops before moving task directories, returns `NEEDS_CONTEXT`, and identifies the missing path; it does not guess another linked worktree based on a matching folder name.
- [ ] **AC-3 — Git command failure**: When a required Git probe exits nonzero, executor does not interpret empty stdout as clean/valid, performs no task mutation, and returns a failure/`NEEDS_CONTEXT` result with the failed probe identified.
- [ ] **AC-4 — One checkout throughout completion**: When a task is completed, discovery, the `ywc-finish-branch` call, and post-move checks all use the same validated task-owning checkout; the existing marker commit and source-absent/destination-present verification remain required.
- [ ] **AC-5 — Existing completion policy preserved**: For tracked and explicitly gitignored task directories, the existing `ywc-finish-branch` move contract remains the sole move authority; the executor adds no direct rename fallback.
- [ ] **AC-6 — Bundle parity**: After synchronization, changed Codex source files match the generated plugin copies and `bash scripts/validate.sh` accepts the package.

## Functional Requirements

### FR-1: Resolve the task-owning checkout

Before task discovery or task mutation, the parallel executor must run from the non-bare Git worktree that owns the selected `tasks/` directory. It must validate the current invocation checkout and selected task path. It must not auto-select or change to a different linked worktree. Worktree destination resolution for creating worker worktrees is not a substitute for this check.

### FR-2: Validate Git evidence

Every required Git probe must check its exit code and validate required output. The executor must not treat missing output, command failure, `core.bare=true`, or a repository-root mismatch as a clean checkout. It must fail closed before task reads or writes when validation cannot complete.

### FR-3: Preserve checkout identity through completion

The validated checkout identity must be retained through task discovery, merge/delivery coordination, `ywc-finish-branch`, and post-move verification. If that checkout becomes unavailable or no longer matches before the move, completion must stop and must not be reported as DONE.

### FR-4: Regression evidence and distribution

Add isolated regression coverage for a valid current task-owning checkout, a bare/non-owning current checkout, and failed Git probes. Keep source assertions labeled as contract evidence, not live Codex execution evidence. Update only source-of-truth Codex skill files first, synchronize the marketplace package, and run repository validation during implementation.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Safety | No task directory or index mutation occurs until a unique valid task-owning checkout has been established. |
| Compatibility | Existing delivery modes, worktree destination selection, task states, and finish-branch move semantics remain unchanged. |
| Maintainability | Reuse existing worktree/Git probing facilities where their behavior matches this contract; do not introduce a general checkout-routing subsystem without evidence it is needed. |

## Data Model / API Contract

- Data Model: N/A — no persistent state schema change is intended.
- API Contract: N/A — no HTTP API. Executor diagnostics/status must distinguish valid selection from `NEEDS_CONTEXT` or failed Git probes as described in FR-1/FR-2.

## Edge Cases

- The invocation begins in a bare repository while a valid task worktree exists elsewhere; the executor must stop and explain the required invocation context.
- Multiple linked worktrees contain similarly named task folders; the current invocation checkout remains authoritative and the executor must not guess between them.
- The current checkout is valid but does not contain the selected task directory.
- A Git probe fails after another probe succeeds; partial success must not authorize mutation.
- Checkout disappears or changes identity between preflight and completion move.
- The `tasks/` directory is gitignored; only the existing `ywc-finish-branch` exception may perform its move.

## Failure Modes

| ID | New path | Realistic failure | Covered by (AC / test / error handling) | User-visible? |
|---|---|---|---|---|
| FM-1 | Checkout validation | Invocation starts from a bare or non-owning checkout | AC-1/AC-2; stop before task access and identify the required invocation context | Yes, `NEEDS_CONTEXT` |
| FM-2 | Git context probe | Git exits nonzero or returns malformed/empty evidence | AC-3; reject result and identify failed probe | Yes, failure status |
| FM-3 | Completion | Validated checkout becomes unavailable before marking complete | AC-4; stop and preserve task state without reporting DONE | Yes, blocked diagnostic |
| FM-4 | Move handling | Executor bypasses the finish-branch move authority | AC-5; contract coverage and implementation review | Yes, validation failure |
| FM-5 | Distribution | Generated plugin package is stale | AC-6; sync and validation commands | Yes, validation failure |

## Verification Strategy

- Isolated temporary Git fixture: valid current worktree containing the task directory, plus a bare invocation context even when a linked worktree exists.
- Failure fixtures: non-owning checkout and injected nonzero Git probe; assert no task path or index mutation occurs.
- Contract checks: verify the executor instructions bind task discovery and completion to one validated checkout; treat this as instruction-level evidence only.
- Distribution checks: `bash scripts/sync-codex-plugin.sh`, followed by `bash scripts/validate.sh`.

## Dependencies

- Existing `ywc-finish-branch` contract remains authoritative for task movement and completion-marker verification.
- Implementation must be coordinated with any active task that owns `codex/skills/ywc-parallel-executor/` or related regression files before editing those files.

## Open Questions

N/A — the current invocation checkout is authoritative; an invalid or non-owning checkout fails closed instead of triggering automatic worktree selection.

