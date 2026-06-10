---
name: ywc-task-generator
version: 1.0.0
description: (ywc) Use when converting a specification into implementation tasks. Triggers: "task 생성", "タスク生成", "spec to tasks", "task breakdown", "작업 분해", "仕様からタスク生成", "implementation tasks", "스펙 분해", "ywc-task-generator", or any spec-to-task decomposition request. Do not use for direct code implementation, spec review (use ywc-spec-validate), or planning without a written specification.
category: spec
phase: planning
requires: [ywc-spec-validate]
advisor_budget: 1
---

# Task Generator

**Announce at start:** "I'm using the ywc-task-generator skill to decompose the specification into dependency-safe tasks."

> **Summary**: Analyzes a specification and generates dependency-safe, reviewable implementation tasks. Each task is output as a structured directory (`README.md`, `task.md`, `test.md`), along with a top-level dependency graph.

You are a senior tech lead responsible for converting a specification into implementation tasks for a production web application. Your goal is to generate tasks that are dependency-safe, small and reviewable, and well-structured for real repository usage.

## Rationalization Defense

When tempted to bend a rule, check this table first:

| Excuse | Reality |
|---|---|
| "DB migration is small, I'll bundle it with the API task" | DB migration must be its own task — in **every** mode. Safety invariant. |
| "User did not specify granularity, `human` is the safe default" | Always ask. Wrong mode cascades into every task's size and bundling. |
| "Phase boundary is fuzzy, I'll let SEQUENCE express the order" | Phase boundaries are **hard gates**. If only some Phase N tasks must finish before a Phase N+1 task starts, that task belongs in Phase N. |
| "Ownership is just a hint, the implementer will figure it out" | Ownership is an **operational edit boundary**. Vague Ownership = parallel-execution conflicts later. |
| "Spec Reference is empty for this task, I'll skip the section" | Never omit. Use `N/A — housekeeping/refactor only` when there is no spec. Empty section = ambiguity. |
| "Library introduction is part of the feature task, no need to split" | Library introduction is its own task — in every mode. Safety invariant. |
| "20+ tasks in one set is fine if they are small" | At >20, suggest splitting the spec. A task set that does not fit in human review will not be reviewed. |

**Violating the letter of these rules is violating the spirit.** Safety invariants (DB migration separation, library introduction separation, phase hard gates) have no exceptions.

## Arguments

| Argument | Default | Description |
|---|---|---|
| `--lang <language>` | _(inferred or asked)_ | Output language for task documents: `korean` \| `japanese` \| `english`. |
| `--tasks-dir <path>` | `tasks/` | Root directory where task directories are written. Override to support re-plan iteration in a separate directory (e.g., `--tasks-dir tasks-v2/`). |

## Language Option

When `--lang` is not specified, this skill first attempts to infer the language from the project's CLAUDE.md (Language Policy section or Documentation Writing Guidelines). Only if inference fails does it ask the user.

This skill supports `korean` | `japanese` | `english` (default: `english`) for task document output. When `--lang` is omitted, follow the inference-first behavior above — only ask the user for confirmation if inference from CLAUDE.md fails.

For the full language detection examples, language-specific writing rules (technical-term policy, Korean/Japanese examples), and the shared technical-term whitelist, **read [references/language-policy.md](references/language-policy.md)** when the user requests Korean or Japanese output. English output does not require reading this reference.

---

## Task Design Principles

### 1. Reviewability
- Each task should be small enough for the intended executor to hold the full context in one session
- Size guideline depends on the selected **Granularity Mode** (see Step 5):
  - `human` mode: ~10 files / ~300 LOC (optimized for single-reviewer PR)
  - `llm` mode: ~25 files / ~800 LOC (optimized for an LLM agent completing a vertical slice in one run)
- See [references/granularity-modes.md](references/granularity-modes.md) for the full rule set
- Split tasks that significantly exceed the mode's guideline
- Do not bundle more than one major concern in a single task
- Prefer self-contained change units that leave the codebase buildable on completion

### 2. Dependency Safety
- Tasks must be strictly ordered by dependency
- Earlier tasks must not depend on later tasks
- Every task must be independently implementable at its position
- If Task B depends on Task A, Task A must fully enable Task B
- After each task completes, the codebase must remain consistent and buildable

### 3. Database Migration Separation (Safety Invariant)
- Database migrations must always be separated into their own task — in every mode
- Include schema/model definitions
- Never mix migration and feature implementation

### 4. Library Introduction Separation (Safety Invariant)
- Create a dedicated task when introducing a new library/framework — in every mode
- Never mix library introduction and feature implementation

---

## Workflow

### Step 1: Verify Input Specification

Receive the specification from the user. It may come in one of these forms:

- Markdown document (file path or inline)
- PRD (Product Requirements Document)
- Feature requirements description
- Change requirements for existing code

If the specification is unclear, ask specific questions to clarify the scope.

### Step 2: Collect Project Context

Gather information about the project environment to generate realistic tasks. This information directly feeds into task.md verification commands, ownership paths, and category selection matching the tech stack.

**Targets to collect:**
- `CLAUDE.md`, `AGENTS.md`, `CODEX.md` — project rules, language policy, CI commands
- `package.json`, `Makefile`, `pyproject.toml`, etc. — actual lint/test/build commands
- Project directory structure — `src/` layout, monorepo status, existing module placement
- Existing `tasks/` directory — whether tasks already exist, numbering collision check
- Docker environment — whether commands require a `docker exec` prefix
- `docs/ubiquitous-language.md` (if it exists) — canonical domain terms and "Synonyms to Avoid"; task names, Implementation Steps, and Ownership paths must use canonical terms and never use synonym identifiers

**When existing tasks are present:**
- Determine the next starting number by scanning **both** `tasks/` and `tasks/completed/`. Completed tasks are moved out of `tasks/` into `tasks/completed/` by the executors (`ywc-sequential-executor` / `ywc-parallel-executor`), so scanning `tasks/` alone misses them and risks reusing a number that already exists. Take the highest PHASE across the union of the two directories; the new batch's first task starts at `highest PHASE + 1` with SEQUENCE reset to `010`. Example: if the highest existing number is `000016-040` — whether it currently lives in `tasks/` or in `tasks/completed/` — the new batch starts at `000017-010`. If `tasks/` is empty (every task already completed and archived), fall back to the highest number in `tasks/completed/` and apply the same `+1 phase` rule.
- Identify dependency relationships with existing tasks and reflect them in the new tasks' `Depends On`

### Step 3: Spec Review

Review the specification for completeness and verify that sufficient information exists for decomposition. The goal is not to demand a perfect spec, but to confirm that the key information needed to determine task boundaries is present.

**Checklist:**
- Are the boundaries of major features clear? (What is in scope for this spec?)
- Is the tech stack specified? (Affects category selection and dependencies)
- If there are external system integrations, is the scope defined? (Determines whether to split into separate tasks)
- Are there implicitly assumed existing infrastructure or features?

**When unclear areas are found:**
- Ask the user specific questions before starting task decomposition
- Frame questions as choices ("Is it A or B?") rather than vague observations ("This part is unclear")
- If the spec is sufficiently clear, skip this step and proceed directly

### Step 4: Confirm Language

If `--lang` is provided, skip this step. Otherwise, attempt to infer the language from the project's CLAUDE.md (Language Policy section or Documentation Writing Guidelines). Only if inference fails or is ambiguous, ask:

> "Which language should the task documents be written in? (korean / japanese / english)"

### Step 5: Confirm Granularity Mode

**Always ask** the user which granularity mode to apply. Do not silently default — the correct mode depends on who will execute the tasks.

> "Which granularity mode should the tasks be generated in?
> - `human` — small, single-PR reviewable units (~10 files / ~300 LOC)
> - `llm` — larger vertical slices optimized for a single LLM agent run (~25 files / ~800 LOC)"

**Mode selection criteria** (share with the user if they are unsure):
- Choose `human` when a person will implement and code-review each task in sequence
- Choose `llm` when tasks will be executed autonomously by an LLM agent (Claude Code, Codex, etc.) in isolated worktrees, and reviewed in aggregate after completion

Safety invariants — DB migration separation, Library introduction separation, Phase hard gate, post-task buildability — apply in **both modes**. Only size and internal bundling differ.

See [references/granularity-modes.md](references/granularity-modes.md) for the full mode specification.

**Persist the decision.** After confirmation, record the selected mode in a re-checkable location (e.g., a top-line scratchpad note, or `write_memory("granularity_mode", <value>)` when Serena MCP is available) and apply it consistently through Steps 6–9 (size, bundling, Ownership scope, Implementation Steps depth, test.md inclusion). Mode drift mid-generation produces inconsistent task directories.

### Step 6: Task Decomposition

Analyze the specification and decompose it into tasks following the Task Design Principles and the selected Granularity Mode.

**Scale guidelines** (task counts scale down in `llm` mode due to vertical bundling):
- **Small** (1–3 tasks expected): A single phase is sufficient. Do not force multiple phases.
- **Medium** (4–15 tasks in `human` mode, ~3–8 in `llm` mode): Organize into 2–3 phases. This is the typical case.
- **Large** (15+ tasks in `human` mode, 8+ in `llm` mode): Suggest to the user that the spec itself be split into multiple features. A single task set exceeding 20 tasks becomes difficult to manage.

#### Planning Advisor (optional, Pattern C)

For **Medium** and **Large** specs, phase boundary decisions and task size splits benefit from frontier judgment. A wrong Phase boundary cascades into every subsequent dependency declaration and is expensive to undo once the task directories are generated.

This skill applies **Pattern C** from [advisor-pattern.md](../references/advisor-pattern.md): a **single** upfront Opus advisor call before writing any task directories. The executor handles everything else — Task Naming, Directory Generation, Dependency Graph, and Final Validation.

**When to invoke**:
- Scale is Medium (4–15 tasks) or Large (15+ tasks), AND
- At least one of: phase boundary is non-obvious, multiple DB migrations or library introductions compete for Phase 1, or the spec touches more than two concurrent feature areas.
- **Skip for Small specs** (1–3 tasks) — a single-phase decomposition is obvious and does not benefit from frontier reasoning. Adding an Opus call here wastes budget.

**How to invoke**: Use the Task tool with `model: opus`. Pass the following as context payload:

- **Spec summary** — ≤20 lines distilled from your Spec Review in Step 3 (not the full spec).
- **First-pass task list** — task name + one-line description for each candidate task from your Step 6 decomposition.
- **Known conflicts / shared surfaces** — any Ownership overlaps or Shared Surfaces you identified.
- **Project context essentials** — monorepo structure, existing phases in `tasks/`, tech-stack constraints affecting dependency order.

Ask the advisor for three things:

1. **Phase boundary recommendations** — which tasks belong to which phase, and why each boundary is a hard gate.
2. **Task size verification** — any task likely to exceed ~10 files or ~300 LOC that should be split further.
3. **Dependency cycle risk** — any tasks with circular implicit dependencies the first-pass missed.

**Budget**: exactly **1** Opus call per invocation of this skill. Pattern C explicitly rules out re-invocation during execution — if the initial plan proves wrong, re-run the whole skill with refined input rather than calling Opus mid-generation. This rule exists because mid-generation re-planning leads to inconsistent task directories; a fresh start is cleaner and more auditable.

**Payload rules**: the summary and task list together must not exceed ~200 lines of payload. If the first-pass decomposition is already larger, narrow it before the advisor call (split the spec into sub-specs and plan each separately). Never forward the full spec verbatim.

**Advisor output format** (≤300 words):
- Phase boundary plan with one-line rationale per boundary
- Task size concerns (if any)
- Cycle/ordering warnings (if any)
- Single "proceed" or "reconsider with refinements" verdict

After receiving the verdict, the executor either continues to Step 7 (Task Naming) with the adjusted plan, or surfaces the "reconsider" verdict to the user for refinement before proceeding.

### Step 7: Task Naming

Each task name follows this format:

```
[PHASE]-[SEQUENCE]-[CATEGORY]-[SHORT-DESCRIPTION]
```
> Example: `000001-010-db-create-user-table` = PHASE `000001` + SEQUENCE `010` + category + description.

**Numbering Rules:**
- PHASE: **6-digit** number (`000001`, `000002`, ...) — the wider width reserves headroom for multi-year project growth
- SEQUENCE: 3-digit number (`010`, `020`, `030`, ...)
- Sequence increments by 10 (allows inserting tasks later without renumbering)
- Always use hyphen (`-`) to separate PHASE and SEQUENCE for readability
- **Starting PHASE for a new batch**: when any tasks already exist, scan both `tasks/` and `tasks/completed/`, take the highest PHASE across the union, and start the new batch at `highest PHASE + 1` with SEQUENCE `010` (see Step 2). A freshly generated batch never reuses a number that was already used and then archived into `tasks/completed/`.

**Category:**
- `lib` — New library/framework introduction
- `db` — Database migration, schema change
- `api` — API endpoint implementation
- `domain` — Business logic, service layer
- `worker` — Background job, async processing
- `ui` — Frontend component, page
- `test` — Test-only task (e2e, load test, etc.)
- `refactor` — Code structure improvement with no behavior change
- `infra` — CI/CD, deployment, configuration
- `config` — Environment variables, feature flags, `.env` setup (distinct from infra: infra covers CI/CD pipelines and deployment, config covers application-level settings)

**Category Selection Guidelines:**
- When a task seems to fit multiple categories, choose based on the **primary nature of the change**
- If creating an API endpoint also requires a DB migration → split into separate tasks (db + api), even in `llm` mode (Safety Invariant)
- Tasks that only set environment variables use `config`; tasks modifying deployment pipelines use `infra`
- Auth/security logic is not a category on its own — choose based on implementation location: `api` (endpoint), `domain` (logic), or `lib` (library introduction)
- In `llm` mode, a single task may bundle `domain` + `api` for one feature — label it with the dominant category (usually `api` when an endpoint is exposed, otherwise `domain`)

**Naming Quality Rules:**
- Use only lowercase and hyphens
- Keep names concise, descriptive, and filesystem-friendly
- Express exactly one primary concern (in `llm` mode, "one primary concern" may cover a vertical slice of a single feature)
- Avoid vague names
- Do not use "and" in task names — use a unifying noun instead (e.g., `user-auth` rather than `registration-and-login`)

**Examples:**
- `000001-010-db-create-user-table`
- `000001-020-lib-setup-auth-library`
- `000001-030-api-user-registration`
- `000002-010-ui-login-form`

### Step 8: Phase Organization

- PHASE represents a meaningful dependency stage (e.g., `000001` = foundation, `000002` = core features, `000003` = integration)
- Do not create phases arbitrarily — a new phase means "all tasks in the previous phase must be complete before this phase can start"
- Tasks within the same phase may have internal ordering via SEQUENCE, but conceptually belong to the same stage

**Phase Boundary Rules:**
- Phase boundaries are **hard gates**. No task in Phase N+1 can start before all tasks in Phase N are complete
- Dependencies between tasks within the same phase are allowed (order expressed via SEQUENCE)
- If only some tasks in Phase N need to be complete before a specific Phase N+1 task can start, that task should be placed in Phase N instead
- Criterion for splitting phases: "Do all outputs from this stage need to be in place for the next stage's work to be meaningful?"

### Step 9: Directory and File Generation

Use the path specified by the user for output. If not specified, default to `tasks/`.

Generate the following structure for each task:

```
tasks/[TASK_NAME]/
├── README.md
├── task.md
└── test.md (optional — included when manual verification is needed)
```

Refer to templates in the `references/` directory when writing files:
- `references/README.md.template` — Task overview and dependency documentation
- `references/task.md.template` — Implementation checklist
- `references/test.md.template` — Manual test plan
- `references/dependency-graph.md.template` — Top-level dependency summary

#### README.md Core Elements

Each README.md must include the following:

- **Purpose**: What this task achieves
- **Scope**: What is included
- **Spec Reference**: Specification/design documents that must be consulted before implementation (see "Spec Reference Rules" below)
- **Dependencies**: Bidirectional dependency tracking
  - **Depends On**: Predecessor tasks this task depends on (specify what each provides)
  - **Depended By**: Successor tasks that depend on this task (specify what each needs)
- **Key Files**: List of files expected to be created or modified
- **Notes**: Important considerations, design decisions
- **Out of Scope**: What is intentionally excluded
- **Parallel Execution Metadata**:
  - **Ownership**: Files, directories, modules, contracts this task may modify
  - **Shared Surfaces**: Shared boundaries that may cause merge or design conflicts
  - **Conflicts With**: Tasks that must not run in parallel
  - **Parallelizable After**: Minimum merged baseline before isolated execution can safely start
  - **Task Verify**: Exact commands that prove this task is complete

Bidirectional dependency tracking matters because developers executing a task can immediately see which downstream tasks are affected, allowing them to consider downstream requirements when designing interfaces.

#### Spec Reference Rules

Every task's README.md must include a `## Spec Reference` section with three subsections: **Primary Sources** (links to source-of-truth docs, project-relative by default), **Summary** (2–5 sentence orientation), and **Out of Scope (from spec)** (scope-creep guardrail).

**Hard rule**: never leave Spec Reference empty or omitted — use `N/A — no external spec (housekeeping / refactor / config only)` when no spec exists.

For the full structure, the external-URL policy, the link-vs-summary drift protocol, and the cross-task scope-handoff convention, **read [references/spec-reference-rules.md](references/spec-reference-rules.md)**.

#### Parallel Execution Metadata Rules

When tasks may be executed via `git worktree`, Codex, Claude Code, or other isolated worker setups, every task's README.md must declare:

- **Ownership** — concrete edit boundary (file paths, globs, modules, contracts). Bad: `backend`, `frontend related files`. Good: `api/src/routes/metrics.ts`, `OpenAPI contract: /api/v1/metrics`.
- **Shared Surfaces** — shared boundaries (DB schema, API contracts, event payloads, workspace config, CI config) that may cause conflicts even without direct file overlap.
- **Conflicts With** — tasks that must not run in parallel even when dependencies allow. Write `(None identified)` if none.
- **Parallelizable After** — the minimum merged baseline for safely starting isolated execution (often, but not always, the same as `Depends On`).
- **Task Verify** — task-specific commands that prove completion (avoid project-wide gates only).

For the full rule set including good/bad Ownership examples, the complete shared-surfaces taxonomy, and the dependency-graph Parallel Execution Notes format, **read [references/parallel-execution-metadata.md](references/parallel-execution-metadata.md)**.

#### task.md Core Elements

Each task.md must include the following:

- **Prerequisites**: Predecessor task completion status to verify before starting (checkbox format)
- **Allowed Edit Scope**: A brief restatement of the `README.md` Ownership as an operational boundary
- **Stop Conditions**: Conditions under which the implementer should stop and report rather than continuing
- **Implementation Steps**: Specific implementation steps (checkbox format)
  - Each step must reference specific files, modules, functions, or behaviors
  - Do not use generic placeholders like "implement core logic" or "handle edge cases"
  - Example: `Create src/models/user.ts with User entity definition`
- **Task Verify**: Task-specific verification command checklist
- **Verification**: Confirm lint, typecheck, test, and build pass (use the project's actual commands)

#### test.md (optional)

Write structured scenario-based tests (Steps + Expected Result).

**Include when:**
- UI component or screen behavior verification → always include
- External service integration (S3, Email, Payment, etc.) → always include
- Browser-dependent features → always include
- Complex user workflows (multi-step) → recommended

**May omit when:**
- Pure API endpoints (coverable by unit + integration tests)
- Database migrations (schema application verified via task.md Verification)
- Library introduction tasks (import and basic operation verified via Verification)

### Step 10: Generate Dependency Graph

After generating all tasks, create `<tasks-dir>/dependency-graph.md` at the top level (where `<tasks-dir>` is the value of `--tasks-dir`, defaulting to `tasks/`). This file serves as the single source of truth for execution order.

Refer to `references/dependency-graph.md.template` for format. List tasks by phase and express each task's dependencies using arrow notation.

This graph must be consistent with the Dependencies sections in individual README.md files.

### Step 11: Final Validation

After generating all tasks, verify the following:

**Dependency & Structure:**
- [ ] No forward dependencies (earlier tasks do not depend on later tasks)
- [ ] No circular dependencies
- [ ] Phase boundaries correctly set as hard gates
- [ ] Database migrations and library introductions separated into their own tasks (Safety Invariant in both modes)
- [ ] No numbering collisions with existing tasks (if any)

**Naming & Size:**
- [ ] Naming convention followed (`[PHASE:6]-[SEQUENCE:3]-[CATEGORY]-[SHORT-DESCRIPTION]`)
- [ ] PHASE is 6 digits, SEQUENCE is 3 digits, separated by hyphen
- [ ] No task name contains "and" (single concern check)
- [ ] Each task fits within the selected Granularity Mode's size guideline
- [ ] Selected Granularity Mode applied consistently (bundling, Implementation Steps depth, Ownership scope)

**README.md Quality:**
- [ ] Both "Depends On" and "Depended By" included
- [ ] Parallel Execution Metadata included (Ownership, Shared Surfaces, Conflicts With, Parallelizable After, Task Verify)
- [ ] Ownership is narrow enough to serve as an actual edit boundary, not just a restatement of Key Files
- [ ] **Spec Reference** section included — Primary Sources, Summary, and Out of Scope (from spec) all filled in or explicitly marked `N/A`
- [ ] If Primary Sources include external URLs, only if the project allows it (default is project-relative paths only)

**task.md Quality:**
- [ ] Specific Implementation Steps included (no generic placeholders)
- [ ] Prerequisites section included
- [ ] Allowed Edit Scope and Stop Conditions included
- [ ] Verification commands match the project's actual commands (based on context collected in Step 2)

**Consistency:**
- [ ] Dependency Graph Summary matches individual README.md files
- [ ] If the task set is intended for parallel execution, Dependency Graph includes Parallel Execution Notes
- [ ] Codebase is buildable after each task completes
- [ ] Selected language's writing rules are followed

---

## Output Format

The final output includes:

1. **Task list summary**: A table organizing all tasks by phase
2. **Directory generation**: Task directories and files created under `<tasks-dir>/` (default: `tasks/`)
3. **Dependency Graph**: `<tasks-dir>/dependency-graph.md` generated — single source of truth for execution order
4. **Parallel Execution Notes**: Included in `<tasks-dir>/dependency-graph.md` when parallel worktree execution is expected

When parallel execution is expected, verify that each task is safe for isolated worktree or agent execution.

---

## Example

User input: "Break down the user authentication spec into tasks. In Korean." (Granularity Mode: `human`)

Output task list:

| Phase   | Task Name                            | Category | Description                                       |
|---------|--------------------------------------|----------|---------------------------------------------------|
| 000001  | `000001-010-db-create-user-table`    | db       | User table migration                              |
| 000001  | `000001-020-lib-setup-bcrypt`        | lib      | Password hashing library introduction             |
| 000001  | `000001-030-domain-user-entity`      | domain   | User entity and repository implementation         |
| 000002  | `000002-010-api-user-registration`   | api      | Registration API endpoint                         |
| 000002  | `000002-020-api-user-login`          | api      | Login API endpoint                                |
| 000003  | `000003-010-ui-registration-form`    | ui       | Registration form implementation                  |
| 000003  | `000003-020-ui-login-form`           | ui       | Login form implementation                         |

Generated directory structure:

```text
tasks/
├── dependency-graph.md
├── 000001-010-db-create-user-table/
│   ├── README.md
│   └── task.md
├── 000001-020-lib-setup-bcrypt/
│   ├── README.md
│   └── task.md
├── 000001-030-domain-user-entity/
│   ├── README.md
│   └── task.md
├── 000002-010-api-user-registration/
│   ├── README.md
│   └── task.md
├── 000002-020-api-user-login/
│   ├── README.md
│   └── task.md
├── 000003-010-ui-registration-form/
│   ├── README.md
│   ├── task.md
│   └── test.md
└── 000003-020-ui-login-form/
    ├── README.md
    ├── task.md
    └── test.md
```

**In `llm` mode**, the same spec would likely collapse to ~4–5 tasks — e.g., `000001-010-db-create-user-table`, `000001-020-lib-setup-bcrypt`, `000002-010-api-user-auth` (bundled domain + api for registration and login), `000003-010-ui-user-auth-forms` (bundled registration and login forms). DB migration and library introduction remain separate per Safety Invariants.

---

## Task Execution Convention

For execution rules after task generation (completion handling, directory moves, etc.), see `references/execution-convention.md`.
