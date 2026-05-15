---
name: ywc-plan
description: (ywc) Use when the user has a rough feature idea or change request and needs a concrete plan before implementation, including scale assessment and routing to the right downstream skill. Triggers: "plan 세워줘", "계획 세워", "어떻게 진행할지", "plan this", "make a plan", "계획", "プラン作成", "計画立てて", "ywc-plan", "task 만들기 전 plan", "before task generator". Do not use for spec quality validation on an existing spec (use ywc-spec-validate), task decomposition from a finalized spec (use ywc-task-generator), product/business reasoning (use ywc-product-review), or architecture-only design without implementation intent (use ywc-tech-research).
category: planning
phase: pre-implementation
requires: []
advisor_budget: 1
---

# ywc-plan

**Announce at start:** "I'm using the ywc-plan skill to clarify the request, assess scale, and route to the appropriate downstream path."

This skill converts a rough idea, vague request, or partially-formed change description into one of two artifacts: (1) a **direct execution plan** for Small changes that can be implemented in a single PR without task decomposition, or (2) a **spec document** for Medium/Large changes that will be handed off to `ywc-spec-validate` and then `ywc-task-generator`. Input: natural-language request from the user. Output: either a `plan.md` (Small path) or a `docs/ywc-plans/<feature>.md` (Medium/Large path), plus an explicit handoff instruction.

## Arguments

| Flag | Type | Description |
|---|---|---|
| `--non-interactive` | flag | Skip `AskUserQuestion` calls in Step 1. If **What** is absent from the user's initial message, stop immediately with `NEEDS_CONTEXT` — planning is impossible without a concrete change description. Fill missing anchors with defaults: Why = `"not specified"`, Out of Scope = `"nothing explicitly excluded"`, Done When = `"all tasks merged and ywc-impl-review returns DONE"`. |
| `--update-spec <path>` | string | Path to an existing spec file. Activates Re-plan Mode (Step 4c). Must be used together with `--failure-context`. If provided without `--failure-context`, stop immediately with `BLOCKED` and report the missing flag. Mutually exclusive with normal spec generation. |
| `--failure-context <text>` | string | The "Fix Priority" section text from `ywc-impl-review`. Used together with `--update-spec`. If provided without `--update-spec`, stop immediately with `BLOCKED` and report the missing flag. |
| `--output <path>` | string | Explicit output path for the generated spec or plan (e.g., `--output docs/ywc-plans/agentic-iteration-1.md`). When omitted, defaults to `./plan.md` (Small) or `docs/ywc-plans/<slug>.md` (Medium/Large). |

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "User said 'just plan it', I'll skip the codebase investigation" | Codebase investigation is mandatory before drafting either artifact. Plans written without reading existing code, `CLAUDE.md`, or `docs/architecture/` produce conflicts that surface during implementation. The agent always feels confident; the user still suffers the rework. |
| "Scale looks ambiguous, I'll default to Small to keep things light" | Default to **Medium** when ambiguous, not Small. Small path skips spec review and task decomposition — wrong scale call cascades into untracked scope creep. The cost of writing a spec for an actually-Small change is one wasted hour; the cost of skipping a spec for an actually-Medium change is rework across multiple sessions. |
| "DB migration is part of the change, I'll bundle it into the Small plan" | Any change touching `migrations/`, `prisma/schema.prisma`, `*.sql`, or equivalent is **never Small**. DB migration must be its own task — escalate to Medium path so `ywc-task-generator` can split it. Safety invariant — same rule as `ywc-task-generator`. |
| "User wants to start coding now, I'll skip ywc-spec-validate on the Medium spec" | The Medium/Large path **must** route through `ywc-spec-validate` before `ywc-task-generator`. Skipping spec review is the failure mode `ywc-task-generator`'s `requires: [ywc-spec-validate]` exists to prevent. Run review even when the user is impatient. |
| "Out of Scope is obvious, I'll leave it implicit" | Always write Out of Scope explicitly — both in the Small `plan.md` and the Medium spec. The implicit version is the one the agent silently expands during implementation. Empty Out of Scope = guaranteed scope drift. |
| "Library introduction is small, I'll bundle it" | Any new library/framework introduction is **never Small**. Same Safety Invariant as DB migration — escalate to Medium path. |
| "User mentioned 'auto-execute', I'll skip the spec for Medium too" | Auto-execute via `ywc-parallel-executor` or `ywc-sequential-executor` does not remove the spec requirement — those executors consume task directories produced by `ywc-task-generator`, which itself requires a reviewed spec. The shortcut does not exist. |
| "The idea is clear enough, I'll write the spec directly" | For Medium/Large changes, unverified design assumptions are the most expensive rework source. Before drafting the spec, surface at least the key branching decisions: data model shape, API boundary, error handling strategy, and any third-party integration scope. Assumptions that seem obvious now become the reason the spec is rewritten during implementation. |
| "The spec-writing process is overhead — let's get to the tasks faster" | Design investment is not overhead — it IS the task. Every hour spent clarifying scope and surfacing assumptions prevents 3–5 hours of rework during implementation. Kent Beck: "Invest in the design of the system every day." The spec is today's investment. |

**Violating the letter of these rules is violating the spirit.** Safety Invariants (DB migration separation, library introduction separation, mandatory spec review for Medium/Large) have no exceptions, regardless of urgency.

## Workflow

The skill executes five steps. Steps 1–2 are mandatory; Steps 3–5 branch on the scale assessment.

### Step 1: Clarify the Request

**Prerequisite:** If `docs/ubiquitous-language.md` exists, read it before asking any questions. The vocabulary defined there must frame the clarification dialogue itself — use canonical terms in your questions and note any "Synonyms to Avoid" so the user's answers are captured in the right terms from the start.

Ask focused questions to extract four anchors. Use one round of consolidated questions (not back-and-forth) unless the user's initial input already covers some anchors.

| Anchor | What to ask | Why it matters |
|---|---|---|
| **What** | "What concrete change are we making? Which user-facing behavior or system capability is added/changed/removed?" | Without a concrete What, scale cannot be assessed. |
| **Why** | "What problem does this solve? What signal motivated it (user request, bug, metric, compliance)?" | Why grounds priority and scope decisions during implementation. |
| **Out of Scope** | "What is explicitly not part of this change? What might look related but is being deferred?" | Out of Scope is the scope-creep guardrail. Always write it. |
| **Done When** | "How will we know it's complete? What observable outcome proves success?" | Done conditions become the Acceptance Criteria in the artifact. |

If the user's initial message already answers all four anchors, skip the questions and confirm understanding in one sentence.

**`--non-interactive` mode:** When this flag is present, do not call `AskUserQuestion` at any point in Step 1. Handle missing anchors as follows: if **What** is absent, stop immediately with `NEEDS_CONTEXT` (planning is impossible without a concrete change description); fill **Why** with `"not specified"`, **Out of Scope** with `"nothing explicitly excluded"`, and **Done When** with `"all tasks merged and ywc-impl-review returns DONE"` when those anchors are missing. Proceed directly to Step 2 without waiting for user input.

### Step 2: Investigate the Codebase

Read targeted files to ground the plan in actual project state. **Mandatory minimum:**

- `CLAUDE.md` and `AGENTS.md` (or `CODEX.md`) at repo root — language policy, conventions, CI commands
- `package.json`, `pyproject.toml`, `Makefile`, `go.mod` etc. — actual lint/test/build commands
- Project tree (top 2 levels of `src/`, `apps/`, or equivalent) — module placement and existing patterns
- Existing `tasks/` directory if present — phase numbering and dependency context
- Relevant `docs/ywc-plans/`, `docs/architecture/`, `docs/product/` if the project uses the LLM development guide layout
- `docs/ubiquitous-language.md` (if it exists) — canonical domain terms and their "Synonyms to Avoid"; spec text and Out of Scope items must use canonical terms and never use synonym identifiers

**Conditional reads (only when relevant to the request):**

- For DB-touching requests: existing schema/migration files
- For API-touching requests: existing route definitions and OpenAPI/contract files
- For UI-touching requests: existing component patterns

Stop investigating once you have enough context to assess scale and write the artifact. **Do not perform open-ended codebase exploration** — that is `gstack-investigate`'s job, not this skill's.

### Step 3: Assess Scale

Pick exactly one scale using the rubric below. **Default to Medium when ambiguous.**

| Scale | Criteria (any one matches) | Path |
|---|---|---|
| **Small** | All of: ≤3 files changed, ≤300 LOC, single concern, no DB migration, no new library, no cross-module impact | Direct execution plan (`plan.md`) |
| **Medium** | 4–15 expected tasks, OR DB migration involved, OR new library introduction, OR touches 2–3 modules | Spec document → `ywc-spec-validate` → `ywc-task-generator` |
| **Large** | 15+ expected tasks, OR cross-cutting refactor, OR new feature with multiple phases | Spec document → split suggestion to user → `ywc-spec-validate` → `ywc-task-generator` |

**Hard-disqualifiers from Small** (any of these forces Medium minimum):

- Database migration / schema change
- New library/framework introduction
- New API contract that other services consume
- Cross-cutting concern (auth, logging, error handling) modified in >1 module

For the full scale-assessment heuristics including borderline-case examples, see [references/scale-assessment.md](references/scale-assessment.md).

### Step 4a: Small Path — Direct Execution Plan

When scale is **Small**, generate `plan.md` at a user-specified path (default: `./plan.md`). If `--output <path>` is provided, write to that path instead of the default.

For the full `plan.md` structure and a worked example, see [references/small-plan-template.md](references/small-plan-template.md).

The plan **must** include: Goal, Out of Scope, Files to touch (concrete paths), Implementation Steps (checkbox list with file/function references), Verification commands (using project's actual commands from Step 2), and Risks/Rollback.

After writing the plan, surface this handoff message to the user:

> "Plan ready at `<path>`. To execute, you can:
> 1. Implement directly in this session, or
> 2. Run `/ywc-code-gen` with the plan as context, or
> 3. Hand off to `/ywc-sequential-executor` if you prefer Branch + PR isolation."

### Step 4b: Medium/Large Path — Spec Document

When scale is **Medium** or **Large**, generate a spec document under `docs/ywc-plans/<feature-slug>.md` (or the project's equivalent — derive from Step 2 investigation). If `--output <path>` is provided, write to that path instead of the derived slug path.

For the full spec structure aligned with `ywc-spec-validate`'s evaluation dimensions, see [references/spec-template.md](references/spec-template.md).

The spec **must** include: Purpose, Scope, Out of Scope, Acceptance Criteria, Functional Requirements, Non-Functional Requirements (when applicable), Data Model / API Contract (when applicable), Edge Cases, and Open Questions (use `N/A — none identified` if none).

For **Large** scale, also surface this advisory before writing the spec:

> "This change is Large (15+ expected tasks). Consider splitting into multiple smaller specs by feature boundary. Splitting now is cheaper than splitting after `ywc-task-generator` produces 20+ task directories. Proceed with single spec, or split first?"

### Step 4c: Re-plan Mode

Activated when `--update-spec <path>` and `--failure-context <text>` are both provided. If exactly one is provided without the other, stop immediately with `BLOCKED` and report the missing flag. This mode is mutually exclusive with normal spec generation (Steps 4a and 4b).

**Behavior:**

1. Read the existing spec at `<path>`. If the file does not exist, report an error and stop — do not create a new file.
2. Determine the current iteration number by counting existing `## Iteration N Amendments` sections in the file. The new section number is N + 1 (starting at 1 if none exist).
3. Using `--failure-context` as the input (the "Fix Priority" section text from `ywc-impl-review`), draft amendment content that addresses only the failing areas.
4. **Append** `## Iteration N Amendments` to the end of the existing spec file. Do NOT create a new file, do NOT modify any completed sections above the new section.
5. The appended section must include: which requirements failed (from `--failure-context`), the amended approach, and updated Acceptance Criteria for the affected items only.

**Constraints:**

- Never overwrite or reorder existing content.
- Never create a new spec file — only append to the file at `<path>`.
- `--output` is ignored in Re-plan Mode (output path is always the `--update-spec` path).

### Step 5: Handoff

Always end with an explicit handoff instruction matching the path taken.

**Small path handoff:**

```text
✅ Plan ready: <path>
Next: implement directly, or run /ywc-code-gen, or /ywc-sequential-executor
```

**Medium/Large path handoff:**

```text
✅ Spec drafted: <path>
Next:
  1. /ywc-spec-validate --spec <path>
  2. (after review passes) /ywc-task-generator <path>
  3. (after tasks generated) /ywc-sequential-executor or /ywc-parallel-executor
```

Never proceed past the handoff. The user decides which downstream skill runs next — this skill is the planner, not the executor.

## Output Format

Two possible artifacts. Both are markdown files at user-specified paths. The handoff message is plain text printed to the conversation.

| Path | Artifact | When |
|---|---|---|
| `./plan.md` (or user-specified) | Small-path execution plan | Scale = Small |
| `docs/ywc-plans/<slug>.md` (or project equivalent) | Medium/Large-path spec | Scale = Medium or Large |

For the exact templates, see [references/small-plan-template.md](references/small-plan-template.md) and [references/spec-template.md](references/spec-template.md).

## Validation

Before declaring the skill's task complete, verify:

- [ ] Step 1 produced explicit answers to all four anchors (What, Why, Out of Scope, Done When)
- [ ] Step 2 read at minimum `CLAUDE.md` (or equivalent) and the project's build/test command source
- [ ] Step 3 selected exactly one scale, with the rubric criterion that matched stated explicitly
- [ ] If scale = Small, none of the hard-disqualifiers apply (re-check DB / library / API contract / cross-cutting)
- [ ] Output file written at a concrete path (no `<placeholder>` slugs)
- [ ] Out of Scope is non-empty (use `N/A — none identified` if truly none)
- [ ] Handoff message printed verbatim with the file path filled in
- [ ] Did not execute the next downstream skill — handoff stops at instruction

## Common Mistakes

- **Skipping Step 2 because the request "sounds simple"** — the request always sounds simpler than it is. Read `CLAUDE.md` and the project tree at minimum, even for one-line changes. Cost: 30 seconds. Benefit: avoiding plans that conflict with project conventions.
- **Conflating ywc-plan with ywc-tech-research** — `ywc-plan` assumes the technology choice is settled or out of scope for this request. If the user is asking *what library to use* or *what architecture to adopt*, route to `ywc-tech-research` first, then return to `ywc-plan` after.
- **Writing Out of Scope as a single line "everything else"** — that is not Out of Scope; that is laziness. List concrete adjacent features that might look related but are deferred (e.g., "User profile editing — separate spec", "Password reset flow — already covered in spec X").
- **Forgetting the handoff message** — without an explicit handoff, the user is left guessing which downstream skill to run. The handoff is the contract that this skill is a planner, not an executor.

## Integration

- **Upstream**: `ywc-tech-research` (when technology choice is unsettled before planning)
- **Downstream (Small path)**: `ywc-code-gen`, `ywc-sequential-executor`
- **Downstream (Medium/Large path)**: `ywc-spec-validate` → `ywc-task-generator` → `ywc-sequential-executor` / `ywc-parallel-executor`
- **Pairs with**: `ywc-product-review` (run before `ywc-plan` when business framing is unclear), `ywc-project-docs` (run after if `docs/` set is missing)
