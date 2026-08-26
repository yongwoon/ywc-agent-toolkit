# Codex `ywc-task-generator` Collaborator Initials Namespace

> Status: Draft
> Scale: Medium
> Created: 2026-08-26
> Author: Codex
> Spec Reference: [develop-with-llm PR #217](https://github.com/yongwoon/develop-with-llm/pull/217)

## Global Constraints

- `codex/skills/` is the source of truth; generated marketplace output must be refreshed with `bash scripts/sync-codex-plugin.sh` (`codex/AGENTS.md`).
- Codex `SKILL.md` frontmatter contains only `name:` and `description:` (`AGENTS.md`).
- Codex skills must keep machine-facing identifiers, paths, commands, JSON keys, and task IDs stable and in English; human-facing documentation follows the shared language policy (`codex/skills/references/language-resolution.md:72-82`).
- The project has no package test runner; `bash scripts/validate.sh` is the required repository validation command (`AGENTS.md`, `codex/AGENTS.md`).
- Shell scripts use portable Bash with `set -euo pipefail` (`AGENTS.md`).
- The existing Codex config path is `.codex/ywc.json` for project scope and `~/.codex/ywc.json` for user scope (`codex/skills/references/language-resolution.md:29-53`); `.ywc-config.json` from PR #217 is not applicable.

## Purpose

PR #217 prevents task-number collisions when multiple collaborators or multiple worktrees generate tasks concurrently by adding a collaborator-initials namespace and expanding the task ID format. The same risk exists in this repository: `ywc-task-generator` currently allocates the next global PHASE from `dependency-graph.md`, active tasks, and completed tasks, while Codex executors explicitly support isolated worktrees. Apply the useful Codex portion of the PR to make task allocation collision-resistant without changing the existing config location or removing legacy task compatibility.

## Scope

- Add optional collaborator initials resolution for Codex task generation.
- Persist initials in the existing project/user `.codex/ywc.json` config alongside `lang`.
- Change newly generated task names to `[INITIALS]-[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]`, for example `yk-000082-010-docs-task-generator-initials`.
- Scope PHASE allocation to the resolved initials, while scanning current, completed, dependency-graph, and linked-worktree task sources.
- Add an atomic shared reservation for a newly allocated initials/PHASE pair so concurrent worktrees cannot select the same PHASE before their task directories are visible in the current worktree.
- Keep legacy numeric IDs and current unprefixed IDs readable by task generation, dependency graph compaction, PR title construction, finish-branch flow, and existing task references.
- Update Codex source documentation, examples, eval fixtures, and generated marketplace output.

## Out of Scope

- Claude Code skill changes. This request is Codex-only.
- Renaming or migrating existing task directories, completed tasks, dependency graphs, or branch names.
- Changing the shared language-resolution order or introducing session-scoped configuration.
- Supporting multiple initials aliases, team accounts, remote coordination across separate clones, or a server-side task ledger.
- Replacing `tasks/dependency-graph.md` as the execution-order source of truth.
- Porting PR #217's `.ywc-config.json` format or the old `tools/codex-skill` directory layout.
- Refactoring unrelated executor behavior; only consumers that parse or display task IDs are updated for compatibility.

## Existing Constraints Touched

| Existing artifact | Behavior verified from the current tree | New code's interaction |
|---|---|---|
| `codex/skills/references/language-resolution.md:29-53` | Project and user config use `.codex/ywc.json`; malformed or unsupported config tiers are skipped rather than hard-failing unrelated work. | Extend the same files with optional `initials`; preserve `lang` resolution and malformed-config fallback. |
| `codex/skills/ywc-setup/SKILL.md:25-71` | `ywc-setup` currently accepts `--scope` and `--lang`, writes exactly `{ "lang": "..." }`, and rejects extra config keys. | Extend the contract to accept `--initials`, preserve existing keys, validate `[a-z0-9]{2,4}`, and document that the resulting object may contain `lang`, `initials`, or both. |
| `codex/skills/ywc-task-generator/SKILL.md:142-153` | Context collection scans the graph, active tasks, and completed tasks; next PHASE is the global maximum plus one; compaction runs before generation when the graph exceeds 300 lines. | Resolve initials before scanning, add linked-worktree sources and initials filtering, reserve the selected PHASE atomically, and retain the compaction gate and mismatch warning. |
| `codex/skills/ywc-task-generator/SKILL.md:276-305` | New task names are unprefixed `[PHASE]-[SEQUENCE]-...` with 6-digit PHASE and 3-digit SEQUENCE; legacy names are already used in evals and task history. | Define the initials-prefixed format for new output and explicitly allow both prefixed and legacy forms in dependency references and migration periods. |
| `codex/skills/ywc-task-generator/scripts/compact-dependency-graph.py:42-47` | The compactor recognizes only numeric phase/full/short IDs; exact `rest.strip().lower() == "— done"` already prevents false completion matches. | Extend ID regexes to optional initials while preserving the exact completion check and legacy parsing. Add regression coverage for headings such as `— Done prerequisites`. |
| `codex/skills/ywc-task-generator/references/execution-convention.md:7-38` | Completion moves a task under `<tasks-dir>/completed/`; the graph stays at the task root. | Use the resolved `<tasks-dir>` and prefixed task names in examples without changing move or graph ownership semantics. |
| `codex/skills/ywc-finish-branch/scripts/build-pr-title.py:17-63` | PR title parsing supports current 6-digit/3-digit, legacy 6-digit, flexible numeric, and single-prefix formats. | Add an optional initials segment before the numeric task number while keeping all existing fallbacks unchanged. |
| `codex/AGENTS.md` and `scripts/sync-codex-plugin.sh` | Source files under `codex/` are copied into generated marketplace packages; generated copies must not be edited first. | Implement and validate source changes, then sync and check parity. |

## Architecture Decision

The shared PHASE reservation uses an atomic Git ref under the repository common directory, for example `refs/ywc/task-phase/<initials>/<phase>`. For each candidate, the generator attempts a compare-and-create update: create the ref with a fixed reservation value only when its expected old value is the all-zero object ID. A failed create means another invocation owns that initials/PHASE pair, so the generator retries the next candidate. Worktrees share this common Git directory, so the reservation remains visible across them and is durable enough to survive the interval between scanning and task-directory creation. The generator releases no reservation during ordinary operation; the ref is a local allocation ledger and prevents reuse even if a generation run exits after reservation. Separate clones are intentionally outside scope.

Config updates use a short-lived exclusive `fcntl.flock` on an adjacent lock file while loading JSON, merging the requested key, flushing/fsyncing a unique same-directory temporary file, and replacing the config. The implementation may be a Python standard-library helper invoked by the portable Bash CLI wrapper; the lock must cover the complete read-modify-write operation. This preserves concurrent `lang` and `initials` updates without relying on the fixed `.tmp` path criticized in PR #217.

## Acceptance Criteria

- [ ] **AC1 — Initials resolution**: When an explicit `--initials <value>` is supplied, the generator validates it against `^[a-z0-9]{2,4}$` and uses it unchanged; uppercase and other non-matching values are rejected rather than silently normalized. Otherwise it uses cached project config, then user config, then derives a candidate from `git config user.email` or `git config user.name` and asks for one confirmation in interactive mode; unresolved non-interactive execution returns `NEEDS_CONTEXT` before writing any task artifact.
- [ ] **AC2 — Config compatibility**: `ywc-setup --scope project --initials yk` preserves an existing `lang` key, writes valid JSON to `.codex/ywc.json`, rejects values outside `[a-z0-9]{2,4}`, and does not create a session config. `--lang`-only, `--initials`-only, and combined invocations each validate and report only the requested/resolved fields.
- [ ] **AC3 — New naming**: A newly generated task uses `[INITIALS]-[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]`, with initials 2–4 lowercase alphanumeric characters, PHASE six digits, and SEQUENCE three digits incrementing by 10 within the batch.
- [ ] **AC4 — Scoped numbering**: With existing tasks for initials `yk` and `js`, a new `yk` batch ignores `js` PHASEs, but includes all matching `yk` IDs found in the resolved graph, active tasks, completed tasks, and every linked worktree's corresponding task directory.
- [ ] **AC5 — Concurrent reservation**: Two generator invocations using the same initials and shared Git repository cannot reserve the same PHASE, even when launched from separate linked worktrees before either worktree sees the other's task directory; each candidate reservation uses the compare-and-create operation in the Architecture Decision, the losing invocation retries with the next available PHASE, and a bounded retry failure reports a deterministic conflict without writing a duplicate task directory.
- [ ] **AC6 — Legacy compatibility**: Existing numeric and current unprefixed task IDs remain valid in `Depends On`, graph parsing, compaction, `ywc-sequential-executor` range selection, `ywc-parallel-executor` wave parsing, finish-branch PR title construction, and completion moves; no existing task directory is renamed.
- [ ] **AC7 — Compactor correctness**: Initials-prefixed full and short IDs compact when all owned tasks are completed, while a heading whose suffix contains `done` but is not exactly `— done` remains untouched. Existing numeric IDs continue to behave as before.
- [ ] **AC8 — Safe concurrent config writes**: Concurrent `lang` and `initials` updates to the same config retain both independent updates, never leave truncated JSON, do not share a fixed temporary filename, and validate the final JSON after replacement.
- [ ] **AC9 — Bundle parity**: After `bash scripts/sync-codex-plugin.sh`, source and generated marketplace copies of every changed Codex skill/reference/script/eval are identical, and `bash scripts/validate.sh` passes.
- [ ] **AC10 — Focused regression evidence**: Shell syntax checks, compactor fixtures, PR title parser fixtures, config smoke tests, and task-generator contract evals cover prefixed, legacy, missing-initials, malformed-config, linked-worktree, and concurrent-reservation cases.

## Functional Requirements

### FR-1: Resolve and persist collaborator initials

Add an `initials` option to `ywc-setup` and a reusable config-writing script under `codex/skills/ywc-setup/scripts/`. The script must preserve unknown existing keys during read-modify-write, validate initials against `^[a-z0-9]{2,4}$`, use a unique temporary file, and serialize the complete operation with an exclusive lock. `ywc-task-generator` must resolve initials before reading or writing task directories, graph files, or preview/task artifacts.

### FR-2: Derive initials safely

For interactive generation, derive a candidate from the local Git identity only when no explicit or cached initials exist, ask one confirmation question, and persist the confirmed value through `ywc-setup`. For non-interactive generation, never guess or write when no explicit/cached value exists; return `NEEDS_CONTEXT` with the missing value named. Derivation rules and examples belong in `codex/skills/ywc-task-generator/references/collaborator-initials.md`.

### FR-3: Allocate initials-scoped PHASEs

Scan the resolved `<tasks-dir>/dependency-graph.md`, `<tasks-dir>/`, `<tasks-dir>/completed/`, and linked worktrees obtained from `git worktree list --porcelain`. Parse both prefixed and legacy IDs. For prefixed IDs, compare the already-validated lowercase initials; legacy IDs remain visible for compatibility but do not claim another collaborator's prefixed namespace. For each candidate PHASE, attempt the compare-and-create reservation ref before creating task directories and retain the existing SEQUENCE reset to `010`. A reservation collision is retried with the next candidate, and task-directory creation occurs only after a reservation succeeds.

### FR-4: Preserve numbering and dependency semantics

Update the task naming rules, task templates, dependency graph template, execution convention, README examples, and eval expectations so new output uses initials-prefixed IDs. Dependency references may point to either format during the transition. The generator must continue to use `<tasks-dir>` rather than hardcoded `tasks/` paths.

### FR-5: Extend machine parsers without weakening completion logic

Update `compact-dependency-graph.py` regexes and `build-pr-title.py` parsing to accept initials-prefixed IDs and retain all legacy formats. Keep compactor completion detection exact (`rest.strip().lower() == "— done"`), and add a fixture proving that `— Done prerequisites` is not treated as completed.

### FR-6: Keep Codex distribution synchronized

Update only the source tree first, run the repository sync script, and validate both source and generated package. Changed Tier 1/Tier 2 README files, `agents/openai.yaml`, evals, and shared references must reflect the new convention without translating machine-facing identifiers.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Correctness | No duplicate initials/PHASE reservation is permitted within one shared Git repository, including linked worktrees. |
| Compatibility | Existing numeric IDs, current task directories, dependency graphs, and config files continue to work without migration. |
| Concurrency | Config replacement is atomic; task-phase reservation is atomic; failures do not leave a partially written JSON file. |
| Portability | Use Bash with `set -euo pipefail`, Python standard library only, and Git/POSIX facilities available on the supported macOS/Linux development environments. |
| Determinism | Contract tests do not call GitHub or require network access; worktree and Git identity fixtures are temporary and isolated. |

## Data Model

No database or external data model change. The durable local configuration shape becomes:

```json
{
  "lang": "ko",
  "initials": "yk"
}
```

Both keys are optional at the individual scope; existing files containing only `lang` remain valid. Atomic reservation refs are local Git metadata, not tracked project files.

## API Contract

N/A — no external API contract change. The internal CLI contracts are:

- `ywc-setup --scope <project|user> [--lang <value>] [--initials <value>]`
- Task generator resolution returns a validated initials value or `NEEDS_CONTEXT` before artifact writes.
- `build-pr-title.py <task-name>` emits the same `TASK_NUMBER`/`SLUG_EN` interface for prefixed and legacy task names; for a prefixed name, `TASK_NUMBER` includes `<initials>-<phase>-<sequence>` so the generated PR title remains traceable.

## Edge Cases

- **Missing `--initials` operand**: fail through the existing usage/error path without an unbound-variable error under `set -u`.
- **Uppercase or invalid initials**: reject rather than silently normalize; documentation should tell users to supply lowercase `[a-z0-9]{2,4}`.
- **Malformed config**: ignore the malformed tier for resolution, but do not overwrite it unless the user explicitly invokes setup for that scope.
- **Config contains unknown keys**: preserve them during read-modify-write; do not regress the existing language setting.
- **Only legacy tasks exist**: start the resolved collaborator's first prefixed batch at `000001-010`, while preserving legacy dependencies unchanged.
- **Legacy and prefixed IDs share a numeric phase**: treat them as distinct identifiers for parsing; do not rename either entry or infer ownership for an unprefixed legacy ID.
- **Linked worktree has a custom tasks directory**: resolve `<tasks-dir>` to a repository-relative path from the invoking worktree, apply that same relative path below each linked worktree's worktree path, inspect only those corresponding directories, and report an inaccessible/mismatched source as a concern rather than silently claiming closure. Absolute or escaping task paths return `NEEDS_CONTEXT`.
- **Reservation exists but task generation crashed**: the reserved PHASE remains consumed; a later run uses the next PHASE, preventing reuse and preserving safety over density.
- **Compactor sees `## Phase yk-000001 — Done prerequisites`**: leave the section unchanged because completion requires the exact suffix `— done`.
- **No `dependency-graph.md`**: continue with directory and reservation discovery, preserving the current no-op/creation behavior.

## Dependencies

- Git with linked-worktree support and atomic ref updates.
- Python 3 standard library for JSON atomic read-modify-write and parser/test helpers.
- Existing `scripts/sync-codex-plugin.sh` and `scripts/validate.sh`.

## Implementation Plan

1. **Config contract and writer**
   - Extend `codex/skills/ywc-setup/SKILL.md`, `README*.md`, and `evals/evals.json` for optional `initials`.
   - Add `codex/skills/ywc-setup/scripts/write-config.sh` with argument validation, scope resolution, `fcntl` lock, unique temporary file, fsync, replace, and post-write JSON validation.
   - Add focused smoke fixtures for lang-only, initials-only, combined, malformed, missing operand, and concurrent updates.
2. **Initials resolution and allocation contract**
   - Add `codex/skills/ywc-task-generator/references/collaborator-initials.md`.
   - Update `codex/skills/ywc-task-generator/SKILL.md` to resolve initials first, enumerate linked-worktree sources, filter prefixed IDs by initials, reserve PHASEs with common-Git refs, and retain legacy fallback behavior.
   - Define cleanup/inspection commands for reservations and deterministic conflict handling without deleting reservations.
3. **Parser and consumer compatibility**
   - Update `compact-dependency-graph.py`, `build-pr-title.py`, `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-finish-branch`, `references/dependency-graph.md.template`, `references/execution-convention.md`, and task README/templates as applicable.
   - Preserve exact `— done` matching and add prefixed/legacy parser fixtures.
4. **Evaluation and documentation parity**
   - Update `codex/skills/ywc-task-generator/evals/evals.json`, `agents/openai.yaml`, and all affected Tier 1/Tier 2 localized READMEs.
   - Run `bash scripts/sync-codex-plugin.sh`; do not hand-edit generated files.
5. **Verification and rollout**
   - Run targeted shell/Python smoke tests and contract evals.
   - Run `bash scripts/install.sh --list --codex` and `bash scripts/validate.sh`.
   - Inspect `git diff --stat` and verify that pre-existing user deletions under `docs/ywc-plans/` remain untouched.

## Open Questions

N/A — none identified. The scope intentionally limits coordination to linked worktrees in one shared Git repository; a multi-clone or remote ledger would require a separate design.

## References

- [PR #217 — PHASE 번호를 collaborator initials로 namespace](https://github.com/yongwoon/develop-with-llm/pull/217)
- `codex/skills/ywc-task-generator/SKILL.md`
- `codex/skills/ywc-setup/SKILL.md`
- `codex/skills/references/language-resolution.md`
- `codex/AGENTS.md`

## Outcome Oracle

- **Target**: Codex task generation and its setup, compaction, PR-title, finish-branch, executor, evaluation, and generated-marketplace consumers allocate and consume initials-prefixed IDs without same-repository linked-worktree collisions, while existing numeric and unprefixed IDs remain usable.
- **Quality threshold**: All AC1–AC10 are implemented with no unresolved Critical or Warning findings; the focused regression suite passes; `bash scripts/sync-codex-plugin.sh` produces source/generated parity; and `bash scripts/validate.sh` passes.
- **Evidence required**: Diff-backed contract tests for config resolution/write locking, prefixed and legacy parsing, linked-worktree discovery, compare-and-create reservation races, compaction, PR-title extraction, finish-branch/executor compatibility, plus parity and repository validation outputs.
- **Stop condition**: Stop and report `BLOCKED` or `NEEDS_CONTEXT` without writing task artifacts if initials cannot be resolved safely, a reservation cannot be acquired deterministically, a path/config input is unsafe, or required evidence cannot be produced. Otherwise stop at the first validation report with zero Critical and Warning findings; remaining Suggestions may be explicitly deferred.

## Blind Spot Pass

- **Action**: `proceed`
- **Checked unknowns**: The review searched all named precedent consumers and current worktree support. Remote coordination across separate clones, task-directory renames, and Claude Code behavior remain explicitly out of scope. No additional runtime path is required by this spec beyond the named Codex setup, generator, compactor, finish-branch, executor, config, evaluation, and sync/validation surfaces.
- **Evidence boundary**: The implementation must re-run the precedent-site search and include every changed consumer in the focused regression evidence; if a newly discovered consumer is outside this boundary, stop for spec amendment rather than silently omitting it.

## Confidence Gate

Inline bounded gate (no delegation tool was available):

```text
Confidence Gate Report
──────────────────────
Aggregate: 86/100 — PROCEED

  Scope clarity:           92   Codex-only scope, applicable PR ideas, exclusions, and observable ACs are explicit.
  Architecture compliance: 78   Existing config and worktree boundaries are verified; Git-ref reservation is chosen for shared-worktree atomicity.
  Evidence quality:        88   Current skill, parser, config policy, distribution, and validation paths were read and cited.
  Reuse verified:          84   Existing language config, compactor, PR-title parser, sync script, and validation commands are reused.
  Root cause identified:   88   Collision source is the global highest-PHASE scan performed before linked-worktree visibility and without a shared reservation.
```

The architecture score is below the other dimensions because Git-ref reservation is a new coordination primitive, but it is bounded to the existing shared-worktree model and is covered by AC5 and the focused concurrency tests.

## Handoff

This is a Medium spec. Before implementation, run `$ywc-spec-validate` against this file. After it returns `DONE`, run `$ywc-task-generator` with an explicit `--spec` and `--mode` to produce dependency-safe tasks. Do not invoke `$ywc-code-gen` directly from this draft.
