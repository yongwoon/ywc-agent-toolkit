# Granularity Modes

This document specifies the two Granularity Modes supported by `ywc-task-generator` and the rules that differ between them. The executor **must** ask the user which mode to use before Step 6 (Task Decomposition) — there is no silent default.

## Contents

- [Mode Comparison](#mode-comparison)
- [Safety Invariants (Both Modes)](#safety-invariants-both-modes)
- [`human` Mode Detailed Rules](#human-mode-detailed-rules)
- [`llm` Mode Detailed Rules](#llm-mode-detailed-rules)
- [Choosing Between Modes](#choosing-between-modes)
- [Interaction with Other Skills](#interaction-with-other-skills)

## Mode Comparison

| Axis | `human` mode | `llm` mode |
|---|---|---|
| Primary executor | Human developer reviewing each PR | LLM agent in an isolated worktree |
| Size guideline | ~10 files / ~300 LOC | ~25 files / ~800 LOC |
| Internal bundling | One primary concern per task; strict category split | Vertical slice permitted — a single feature may bundle `domain` + `api`, provided Safety Invariants hold |
| Category splitting | `db`, `lib`, `api`, `domain`, `ui`, `worker` strictly separated | Feature-level bundling allowed for non-invariant categories; invariants remain separate |
| Ownership scope | Narrow path globs (file-level or small directory) | Feature-level module subtree |
| Implementation Steps depth | 10–20 fine-grained checkboxes | 3–7 top-level bullets, each with 2–5 sub-bullets |
| test.md inclusion | UI / external-integration / browser-dependent tasks | More inclusive — add feature-level integration scenarios alongside the same UI / external-integration criteria |
| Typical phase count | 2–3 phases for a medium spec | 1–2 phases for the same spec (tasks absorb more scope) |
| Review cadence | Per-task PR review | Post-completion aggregate review across the feature slice |

## Safety Invariants (Both Modes)

These rules apply identically in `human` and `llm` mode. Do not relax them when enlarging tasks in `llm` mode.

1. **Database migration separation** — every schema/migration change is its own task
2. **Library / framework introduction separation** — every new dependency is its own task
3. **Phase hard gate** — no task in Phase N+1 may start before all tasks in Phase N complete
4. **Post-task buildability** — after each task completes, the codebase must remain consistent and buildable
5. **Single phase per task** — a task never spans more than one phase

## `human` Mode Detailed Rules

Use `human` mode when:
- A developer will implement and review each task in sequence
- Changes must fit in a reviewable single PR (~1 hour review budget)
- Tight feedback loop per task is valued over throughput

Guidelines:
- Split tasks that cross `db` / `api` / `ui` boundaries
- Implementation Steps should be specific enough that another developer can resume mid-task
- Ownership should be a narrow path glob or a specific file

## `llm` Mode Detailed Rules

Use `llm` mode when:
- Tasks will be executed by an LLM agent (Codex, or similar)
- Tasks run in isolated `git worktree`s and are reviewed after completion
- Throughput and single-session context coherence matter more than per-PR reviewability

Vertical bundling rules:
- A task may cover one feature across `domain` + `api` if the scope stays within ~25 files / ~800 LOC
- `ui` may be bundled with its directly-coupled `api` only when the UI and API share exclusive ownership (no cross-feature reuse)
- Never bundle a Safety Invariant (DB migration, Library introduction) with other work

Implementation Steps rules:
- Use 3–7 top-level bullets, each representing a coherent sub-goal
- Each top-level bullet may contain 2–5 sub-bullets for internal steps
- Each step must still reference specific files, modules, functions, or behaviors

Ownership rules:
- Declare ownership at module or feature subtree level (e.g., `src/features/auth/**`)
- Still declare Shared Surfaces with the usual precision

test.md rules:
- Include when the feature slice has a user-visible workflow end-to-end
- Scenarios should cover the full vertical path the task implements, not just the UI surface

## Choosing Between Modes

If the user is unsure, ask:
1. "Will a person review each task in a separate PR, or will an agent execute them autonomously and be reviewed in aggregate?"
2. "Is throughput of completed work per session more valuable than per-task reviewability?"

Never silently default — require the user to confirm one of the two modes.

## Interaction with Other Skills

- `ywc-sequential-executor`: executes tasks one-by-one. Either mode works, but `human` tends to match sequential human oversight better.
- Parallel worktree execution: both modes work. `llm` mode tends to produce fewer, larger parallel units.
