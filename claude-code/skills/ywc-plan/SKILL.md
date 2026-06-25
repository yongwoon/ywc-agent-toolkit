---
name: ywc-plan
description: >-
  (ywc) Use when the user has a rough feature idea or change request and needs a concrete plan before implementation, including scale assessment and routing to the right downstream skill. Triggers: "plan 세워줘", "계획 세워", "어떻게 진행할지", "plan this", "make a plan", "계획", "プラン作成", "計画立てて", "ywc-plan", "task 만들기 전 plan", "before task generator". Do not use for spec quality validation on an existing spec (use ywc-spec-validate), task decomposition from a finalized spec (use ywc-task-generator), product/business reasoning (use ywc-product-review), pre-intent idea clarification when the goal is not yet pinned down (use ywc-brainstorm), authoring a full specification document (use ywc-spec-writer), or architecture-only design without implementation intent (use ywc-tech-research).
---

# ywc-plan

**Announce at start:** "I'm using the ywc-plan skill to clarify the request, assess scale, and route to the appropriate downstream path."

This skill converts a rough idea, vague request, or partially-formed change description into one of two artifacts: (1) a **direct execution plan** for Small changes that can be implemented in a single PR without task decomposition, or (2) a **spec document** for Medium/Large changes that will be handed off to `ywc-spec-validate` and then `ywc-task-generator`. Input: natural-language request from the user. Output: either a `plan.md` (Small path) or a `docs/ywc-plans/<feature>.md` (Medium/Large path), plus an explicit handoff instruction.

## Arguments

| Flag | Type | Description |
|---|---|---|
| `--non-interactive` | flag | Skip `AskUserQuestion` calls in Step 1. If any anchor is missing, fill with defaults: Out of Scope = `"nothing explicitly excluded"`, Done When = `"all tasks merged and ywc-impl-review returns DONE"`. |
| `--update-spec <path>` | string | Path to an existing spec file. Activates Re-plan Mode (Step 4c). Must be used with `--failure-context`. Mutually exclusive with normal spec generation. |
| `--failure-context <text>` | string | The "Fix Priority" section text from `ywc-impl-review`. Used together with `--update-spec` to identify which parts of the spec need amendment. |
| `--output <path>` | string | Explicit output path for the generated spec or plan (e.g., `--output docs/ywc-plans/agentic-iteration-1.md`). When omitted, defaults to `./plan.md` (Small) or `docs/ywc-plans/<slug>.md` (Medium/Large). |

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "User said 'just plan it', I'll skip the codebase investigation" | Codebase investigation is mandatory before drafting either artifact. Plans written without reading existing code, `CLAUDE.md`, or `docs/architecture/` produce conflicts that surface during implementation. The agent always feels confident; the user still suffers the rework. |
| "Scale looks ambiguous, I'll default to Small to keep things light" | Default to **Medium** when ambiguous, not Small. Small path skips spec review and task decomposition — wrong scale call cascades into untracked scope creep. The cost of writing a spec for an actually-Small change is one wasted hour; the cost of skipping a spec for an actually-Medium change is rework across multiple sessions. |
| "The request has two plausible readings, I'll pick the likelier one" | When two interpretations materially change scope, data model, or the meaning of the change, present **both** to the user with the consequence of each — do not silently choose. The default-to-Medium rule resolves **scale** ambiguity only; it is not licence to resolve **intent** ambiguity by guessing. A silently-chosen interpretation is the most expensive rework source because it stays invisible until implementation contradicts it. |
| "DB migration is part of the change, I'll bundle it into the Small plan" | Any change touching `migrations/`, `prisma/schema.prisma`, `*.sql`, or equivalent is **never Small**. DB migration must be its own task — escalate to Medium path so `ywc-task-generator` can split it. Safety invariant — same rule as `ywc-task-generator`. |
| "User wants to start coding now, I'll skip ywc-spec-validate on the Medium spec" | The Medium/Large path **must** route through `ywc-spec-validate` before `ywc-task-generator`. Skipping spec review is the failure mode `ywc-task-generator`'s `requires: [ywc-spec-validate]` exists to prevent. Run review even when the user is impatient. |
| "Out of Scope is obvious, I'll leave it implicit" | Always write Out of Scope explicitly — both in the Small `plan.md` and the Medium spec. The implicit version is the one the agent silently expands during implementation. Empty Out of Scope = guaranteed scope drift. |
| "Library introduction is small, I'll bundle it" | Any new library/framework introduction is **never Small**. Same Safety Invariant as DB migration — escalate to Medium path. |
| "User mentioned 'auto-execute', I'll skip the spec for Medium too" | Auto-execute via `ywc-parallel-executor` or `ywc-sequential-executor` does not remove the spec requirement — those executors consume task directories produced by `ywc-task-generator`, which itself requires a reviewed spec. The shortcut does not exist. |
| "The idea is clear enough, I'll write the spec directly" | For Medium/Large changes, unverified design assumptions are the most expensive rework source. Before drafting the spec, surface at least the key branching decisions: data model shape, API boundary, error handling strategy, and any third-party integration scope. Assumptions that seem obvious now become the reason the spec is rewritten during implementation. |
| "The spec-writing process is overhead — let's get to the tasks faster" | Design investment is not overhead — it IS the task. Every hour spent clarifying scope and surfacing assumptions prevents 3–5 hours of rework during implementation. Kent Beck: "Invest in the design of the system every day." The spec is today's investment. |
| "The spec says it follows existing component X, that's good enough — no need to read X" | "Follows X" is a *claim*, not a *spec*. Code Compatibility findings are the largest single category of spec-validate Critical findings, and the majority trace to a "follows X" claim where the author never opened X. Read X end-to-end and transcribe its behavior into **Existing Constraints Touched** with `file:line` citations. The reviewer cannot verify what was never written down. |
| "I grepped and found the one writer/reader, so that's the only one" | A forward grep that confirms **one** instance is not evidence of a **closed set**. Closure claims ("only / sole / 唯一 / no other / all / exhaustive") and liveness claims ("dead / @deprecated / 呼び出し元ゼロ / still active") are the single largest source of *false-but-confident* spec assertions: the planner confirms the instance it already had in mind and never runs the *complement* grep that enumerates the rest. The most expensive Critical in the LP column-drop plan was exactly this — "injectAndSaveGtmSnippet is the 唯一の generatedHtml writer", but `markDone` also wrote it, and dropping the column would have broken the build. Before writing any closure or liveness word, run the complement grep (`grep -rn "<identifier>" <module>`, classify every hit live/dead) and transcribe the full set. |
| "While I'm reading this code anyway, I'll fold in the adjacent cleanup/refactor" | Thoroughness in *investigation* must not become expansion of the *change scope*. A plan that enumerates a related site (a parameter, a sibling method, a rename opportunity) and then proposes changing it — when the request did not ask for it — adds surface that becomes new Critical findings. The measured regression: a `generatedHtml`-drop plan proactively proposed a `composeHtml` refactor and shipped a build-break Critical the narrower plan never risked. Enumerate everything; change only what the request requires; record the rest as "no change needed" under Existing Constraints Touched. |
| "AC and the API Contract probably agree, I won't cross-check" | Cross-section drift between AC, FR, Data Model, and API Contract is the #2 source of Critical findings (after Code Compatibility). Step 4b.5 is mandatory for Medium/Large precisely because authors trust their own consistency and reviewers find it broken. Run the cross-check; the cost is ~5 minutes, the cost of skipping it is one full re-plan iteration. |
| "Validation came back DONE_WITH_CONCERNS, I'll rewrite the spec from scratch and re-run" | Use **Re-plan Mode** (`--update-spec <path> --failure-context "<findings>"`) instead. Re-plan appends an `## Iteration N Amendments` section that addresses only the failing items, preserving the rest of the spec verbatim. Rewriting from scratch loses the validated portions and produces cosmetic diffs that reviewers must re-validate. |

**Violating the letter of these rules is violating the spirit.** Safety Invariants (DB migration separation, library introduction separation, mandatory spec review for Medium/Large) have no exceptions, regardless of urgency.

## Workflow

The skill executes five steps. Steps 1–2 are mandatory; Steps 3–5 branch on the scale assessment.

### Step 1.0: Brainstorm Gate

Before extracting anchors, evaluate whether the request is concrete enough for direct planning. Some requests arrive as design conversations rather than plan inputs; those must run through `ywc-brainstorm` first.

| Signal | Route |
|---|---|
| Request includes a concrete change description, files / surfaces touched, and an observable Done condition | Proceed to Step 1 — anchors will extract cleanly. |
| Request is conversational ("I'm thinking about X", "wouldn't it be nice if…", "let's explore Y", "어떻게 만들지", "アイディアがある") | **Delegate to `ywc-brainstorm`** — it surfaces the four anchors via Socratic dialogue and presents 2–3 approaches; resume `ywc-plan` from Step 1 with the brainstorm handoff as input. |
| Request describes multiple independent subsystems (e.g., "a platform with auth, chat, billing, analytics") | **Delegate to `ywc-brainstorm`** for decomposition before any anchor extraction. Each subsystem gets its own brainstorm → plan cycle. |
| Two or more of (What / Why / Out of Scope / Done When) are completely missing from the request | **Delegate to `ywc-brainstorm`** — extracting two missing anchors at once produces shallow answers; ywc-brainstorm collects them one at a time with explicit approach trade-offs. |

When delegating, surface this verbatim before transferring control:

> "This request needs intent clarification before planning. Switching to `ywc-brainstorm` to surface the four anchors and approach choice. After the design is approved, returning to `ywc-plan` Step 1 with the brainstorm handoff as input."

When `ywc-brainstorm` completes, its handoff message includes the four anchors and the chosen approach. Re-enter `ywc-plan` Step 1 with that handoff as the effective user input — the anchors should already be filled, so Step 1 typically reduces to a one-sentence confirmation.

`--non-interactive` mode skips the delegation: when the flag is present, treat ambiguity as Medium scale (Step 3) and fill missing anchors with defaults rather than routing to `ywc-brainstorm`.

After Scale assessment in Step 2 and before any downstream handoff (`ywc-spec-writer`, `ywc-task-generator`, `ywc-code-gen`, executor), invoke `ywc-confidence-gate` with the chosen approach as input. The gate's PROCEED / REVIEW / STOP band determines whether the plan is ready for handoff; a REVIEW band surfaces alternatives to the user, a STOP band routes back here for additional investigation before re-attempting handoff. The 5-dimension score becomes part of the plan's completion summary so downstream skills inherit a comparable confidence number.

### Step 1: Clarify the Request

**Prerequisite:** If `docs/ubiquitous-language.md` exists, read it before asking any questions. The vocabulary defined there must frame the clarification dialogue itself — use canonical terms in your questions and note any "Synonyms to Avoid" so the user's answers are captured in the right terms from the start.

**Prerequisite (mission framing):** If `docs/project-mission.md` exists, read it before asking any questions (best-effort, alongside the ubiquitous-language read above). Use its Mission / North-Star and active Success Criteria to **frame** the clarification dialogue — anchor questions to the stated mission, and seed the artifact's Acceptance Criteria from any Success Criterion this request advances. This is purely additive framing: the mission file's **absence is a clean no-op** (NFR2) — never block, delay, or re-derive planning because it is missing, and never treat its presence as overriding the user's stated intent for *this* request.

Ask focused questions to extract four anchors. Use one round of consolidated questions (not back-and-forth) unless the user's initial input already covers some anchors.

| Anchor | What to ask | Why it matters |
|---|---|---|
| **What** | "What concrete change are we making? Which user-facing behavior or system capability is added/changed/removed?" | Without a concrete What, scale cannot be assessed. |
| **Why** | "What problem does this solve? What signal motivated it (user request, bug, metric, compliance)?" | Why grounds priority and scope decisions during implementation. |
| **Out of Scope** | "What is explicitly not part of this change? What might look related but is being deferred?" | Out of Scope is the scope-creep guardrail. Always write it. |
| **Done When** | "How will we know it's complete? What observable outcome proves success?" | Done conditions become the Acceptance Criteria in the artifact. |

If the user's initial message already answers all four anchors, skip the questions and confirm understanding in one sentence.

If an anchor answer contradicts another anchor or the codebase evidence gathered in Step 2, **STOP** — name the contradiction explicitly and ask before proceeding. Do not silently reconcile it by picking one side.

**`--non-interactive` mode:** When this flag is present, do not call `AskUserQuestion` at any point in Step 1. If the user's initial message leaves any anchor unanswered, fill it with the following defaults automatically: Out of Scope = `"nothing explicitly excluded"`, Done When = `"all tasks merged and ywc-impl-review returns DONE"`. Proceed directly to Step 2 without waiting for user input.

### Step 2: Investigate the Codebase

Read targeted files to ground the plan in actual project state. Step 2 is organized into four parts: what to **always** read, what to read **conditionally**, what triggers a **deeper** read, and **when to stop**.

#### Always read

- `CLAUDE.md` and `AGENTS.md` (or `CODEX.md`) at repo root — language policy, conventions, CI commands
- `package.json`, `pyproject.toml`, `Makefile`, `go.mod` etc. — actual lint/test/build commands
- Project tree (top 2 levels of `src/`, `apps/`, or equivalent) — module placement and existing patterns
- Existing `tasks/` directory if present — phase numbering and dependency context
- Relevant `docs/ywc-plans/`, `docs/architecture/`, `docs/product/` if the project uses the LLM development guide layout
- `docs/ubiquitous-language.md` (if it exists) — canonical domain terms and their "Synonyms to Avoid"; spec text and Out of Scope items must use canonical terms and never use synonym identifiers
- `docs/project-mission.md` (if it exists) — Mission / North-Star + active Success Criteria; frame the plan's scope and seed Acceptance Criteria from criteria this request advances. Absence is a clean no-op (NFR2)
- **Parent spec / design doc** named in the plan's own header (`Parent spec:`, `親 spec:`, `Spec Reference:`) — when the request is a follow-up or amendment to an existing plan, read the parent end-to-end. A follow-up that silently narrows the parent's explicit removal/scope list is a cross-document Consistency finding: in the LP column-drop follow-up, the parent said "delete `markDone`/`markFailed`" but the follow-up's removal list dropped `markDone`, which would have left a dangling write against the dropped column.

#### Conditional reads (only when relevant to the request)

- DB-touching requests: existing schema/migration files
- API-touching requests: existing route definitions and OpenAPI/contract files
- UI-touching requests: existing component patterns

#### Trigger-based deep reads

Five triggers force a deeper read than the lists above. Each fires independently — if more than one applies, do all of them.

1. **Explicit "follows existing X" claim.** When the user's request — or your own draft of Scope / Functional Requirements / Data Model — uses phrases like *"踏襲 / follows / based on / extends / 同じパターンで / similar to / mirrors / 参考に"* and names a specific component, you **must read that component end-to-end** (not just its location, not just nearby patterns). The new spec inherits not only the pattern but every actual behavior — response headers, status codes, timeout values, parser limits, cascade rules. Capture each inherited behavior under **Existing Constraints Touched** with a `file:line` citation. This rule exists because Code Compatibility findings dominate spec-validate Critical counts — and the majority trace back to a "踏襲" claim whose author never opened the referenced file.

2. **Implicit reference to existing types/models.** The "follows X" rule fires on prose claims, but the more common failure is the *implicit* reference — the spec never says "follows X", it just uses an identifier or shape that already exists. Trigger a deep read whenever the spec:
   - **Uses a property accessor on an existing domain type by name** not declared in your own Data Model (e.g., `tenantSlug`, `userEmail`, `orderId.short`, `submission.actor.user_id`) — every such accessor is a claim that the property exists with the expected shape
   - **Names an existing audit log, event, DTO, or error type by category** without inlining its shape (e.g., "writes an audit log", "emits a `UserCreated` event", "returns a `ConflictError`") — the spec must either inline the shape with a `file:line` citation or explicitly reference the existing type, never invent a parallel shape
   - **Introduces a new column whose name or semantics overlap a field already present elsewhere** — either reuse the existing field/enum or justify the divergence

   For each implicit reference, grep the existing schema/types (`grep -n "<identifier>" backend/prisma/schema.prisma`, `grep -rn "<TypeName>" backend/src/lib/`) and either capture the verified shape under **Existing Constraints Touched** or declare the schema change explicitly. This rule exists because findings like "field absent on existing model" and "shape mismatch with existing type" arise from variable-name use, not from any prose claim of "踏襲".

3. **Stack-primitive section about to be written.** Before drafting Data Model, API Contract, or any section that touches DB / middleware / framework primitives, skim [references/common-pitfalls.md](references/common-pitfalls.md). It enumerates the recurring traps spec-validate flags (global vs route-scoped middleware, `@HttpCode` vs documented status, error-handling discipline, etc.). The schema-side rules live in the shared [../references/schema/core.md](../references/schema/core.md) — read core for the rules, then the one stack file matching the project (`prisma.md`, `sql-ddl.md`, `drizzle.md`, `typeorm.md`). Skimming both at Step 2 is cheaper than discovering each trap individually in validation.
4. **Schema invariants summary needed.** When the user needs the planner's compact checklist instead of full stack syntax, read [references/schema-invariants.md](references/schema-invariants.md) before writing Data Model acceptance criteria.

5. **Closure or liveness claim about code.** The first three triggers fire on a *positive identity* claim ("this follows / uses X"). This one fires on the inverse — *set-closure* and *liveness* claims — which are just as failure-prone and far easier to assert from memory. When your draft asserts that a set is complete — *"only / sole / 唯一 / the single / no other / all / exhaustive / 全て / 唯一の … 経路"* — or that a symbol is dead or alive — *"@deprecated / unused / 呼び出し元ゼロ / dead write / still active / 現に write"* — you must run the **complement grep**: enumerate the entire candidate set, not just re-confirm the one instance already in hand. For "C is the only writer of column X", run `grep -rn "X" <module>` and classify every write site live/dead; for "method M is dead", grep M's callers repo-wide and transcribe the zero (or the non-zero hit you would otherwise have missed). Capture the enumerated set under **Existing Constraints Touched**. This rule exists because a forward grep that confirms one writer is silently mistaken for proof that no other writer exists — the failure mode behind both the largest Critical and a Warning in the LP column-drop plan (`markDone` was a second `generatedHtml` writer the "唯一の write 経路" claim never enumerated; `markFailed` was dead despite an "active" claim).

   Two disciplines when transcribing the enumerated set:
   - **Attribute each hit to its own `file:line`.** Never fold one file's line numbers under another file's header — mixing `lp.service.ts` lines into an `lp.repository.ts` proof is itself a Consistency finding the reviewer will flag.
   - **Enumeration is for comprehension, not scope expansion.** Classify each enumerated site as *must-change for this request* or *no change needed* (record the latter under **Existing Constraints Touched**, not in the change list). Never fold an adjacent refactor — a rename, a signature change on a site that merely looks related — into the plan unless the request requires it. "While I'm here I'll also refactor X" over-reach expands the plan's surface and is its own Critical source; the measured failure was a plan that proactively proposed a `composeHtml` refactor and introduced a build break the narrower plan never risked.

#### When to stop

Stop investigating once you can confidently (a) pick a scale using Step 3's rubric, (b) name concrete files in the plan or spec, and (c) state the project's actual lint/test/build commands. Going beyond this is `gstack-investigate`'s job — defer to that skill if the user explicitly wants deep investigation.

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

### Step 3.5: Architectural Advisor Gate (Medium/Large only)

Run this gate **only when both conditions hold**:

- Scale assessed as **Medium** or **Large** (Small path skips this gate)
- Step 2 codebase investigation surfaced an architectural ambiguity that the spec / `docs/architecture/` / project convention cannot resolve on its own (examples: monolith vs split, sync vs async boundary, ORM vs raw SQL, domain boundary placement, abstraction-vs-duplication trade-off for a soon-to-be-replicated pattern)

If both conditions fail, skip to Step 4 directly. The gate exists to head off the failure mode where a Medium/Large plan locks in a structural choice that subsequent implementation cannot walk back without a re-plan.

**Procedure**:

1. **Frame the decision** in one sentence with the two (occasionally three) reasonable options the codebase / spec admit. Avoid hypothetical options the project would not actually pick.
2. **Assemble the bounded payload** — the spec excerpt that touches the decision (≤30 lines), the most relevant existing code reference (file path + 1-paragraph summary, not the full file), and the project convention or prior-art entry if one applies. Do not forward the whole spec.
3. **Dispatch the advisor**. When the Claude Code runtime is in use and the named-agent catalog at `tools/claude-code/agents/` is installed, dispatch `Task(subagent_type: ywc-architect)` with the bounded payload. When the runtime does not support named agents, dispatch a `model: opus` subagent with the same payload and the canonical persona prompt copied from `tools/claude-code/agents/ywc-architect.md` Mission section.
4. **Record the verdict** in `docs/ywc-plans/<plan-slug>/architecture-verdict.md` (or alongside the spec when the spec path is provided). The file captures: the framed decision, the trade-off table the advisor returned, the chosen direction, and the file / type / structural shape recommendation. Subsequent steps cite this file rather than re-litigating the decision.
5. **Handle non-DONE statuses** per the standard contract:
   - `DONE_WITH_CONCERNS` → cite the concerns explicitly in the spec's Constraints section so reviewers see the caveat
   - `NEEDS_CONTEXT` → run the additional Read / Grep the advisor names, then re-dispatch with the enriched payload
   - `BLOCKED` → surface to the user with the advisor's blocker summary; do not proceed to Step 4 until the prerequisite is resolved

**Budget**: at most **1** ywc-architect dispatch per ywc-plan invocation. If a second architectural decision surfaces, defer it to `ywc-confidence-gate` STOP-band routing or to a follow-up plan rather than burning another Opus call inside the same plan run.

Skip the gate entirely (with a one-line note in the plan / spec) when the architectural choice is unambiguous from the spec or already adjudicated by a prior `architecture-verdict.md` in the same project.

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

When the spec names module boundaries, key types, and interfaces, ground those design choices in the shared readable-code rubric — especially §G (structural smells) and its anti-dogma guardrails (do not specify speculative generality or premature abstraction the requirement does not yet need). See [../references/readable-code.md](../references/readable-code.md).

For **Large** scale, also surface this advisory before writing the spec:

> "This change is Large (15+ expected tasks). Consider splitting into multiple smaller specs by feature boundary. Splitting now is cheaper than splitting after `ywc-task-generator` produces 20+ task directories. Proceed with single spec, or split first?"

### Step 4c: Re-plan Mode

Activated when `--update-spec <path>` and `--failure-context <text>` are both provided. This mode is mutually exclusive with normal spec generation (Steps 4a and 4b).

**Behavior:**

1. Read the existing spec at `<path>`. If the file does not exist, report an error and stop — do not create a new file.
2. Determine the current iteration number by counting existing `## Iteration N Amendments` sections in the file. The new section number is N + 1 (starting at 1 if none exist).
3. Using `--failure-context` as the input (the "Fix Priority" section text from `ywc-impl-review`), draft amendment content that addresses only the failing areas.
4. **Append** `## Iteration N Amendments` to the end of the existing spec file. Do NOT create a new file, do NOT rewrite any completed section's body above the new section.
4.5. **Mark superseded originals (the one permitted in-place edit).** When the amendment scopes out or changes an instruction that an original section still states literally — e.g., an original migration SQL block that drops a column the amendment now defers — prepend a single inline marker line at the head of that original section: `> ⚠️ SUPERSEDED by Iteration N — see §<amendment-anchor>`. Do not edit the section's body, only prepend the marker. Then ensure a top-of-file **Operative Sections** pointer names which sections `ywc-task-generator` should treat as authoritative. This removes the precedence-only resolution that otherwise leaves a copy-faithful implementer acting on the superseded original — the exact residual Warning in the LP column-drop re-validation, where the original §1 SQL still dropped `errorMessage` after the amendment deferred it.
5. The appended section must include: which requirements failed (from `--failure-context`), the amended approach, and updated Acceptance Criteria for the affected items only.
6. **Re-run Step 4b.5 on the whole spec** (original sections + the new amendment) before printing the handoff. An amendment frequently introduces fresh drift — a new status code that conflicts with an original AC, a new field absent from the original API Contract, a new state value without a write site. Without the re-run, that drift surfaces as a *fresh* Critical at the next `ywc-spec-validate` pass and forces yet another iteration. Re-running 4b.5 here is what makes Re-plan Mode actually converge.

**Constraints:**

- Never overwrite or reorder existing content — **except** the single-line `> ⚠️ SUPERSEDED ...` marker permitted by Behavior step 4.5, which prepends (never rewrites the body of) a contradicted original section.
- Never create a new spec file — only append to the file at `<path>`.
- `--output` is ignored in Re-plan Mode (output path is always the `--update-spec` path).

### Step 4b.5: Pre-Handoff Self-Consistency Pass (Medium/Large only)

Before printing the handoff message in Step 5, run this mechanical check on the spec you just wrote. Step 5's `Validation` list checks **structural** items (sections exist, anchors answered); Step 4b.5 catches the **semantic drift** the author introduces between sections — which is what dominates `ywc-spec-validate` Critical findings.

The check is organized into three passes, each catching a different class of drift. Run all three. For each row, scan the spec end-to-end and answer with a concrete pointer (section heading or `file:line`). If the answer is "I'm not sure" or "probably yes", edit the spec until the answer becomes "yes, see <pointer>" before printing the handoff.

Examples below are tagged *(past session, this codebase)* — they are real failures observed during the LP form / publish spec work that motivated this skill, included because concrete examples teach better than abstract rules. The **Rule** column is the universal principle and applies to any feature family.

#### Pass A — Cross-section consistency (within this spec)

Catches drift between AC / FR / API Contract / Data Model of the same spec.

| Rule | Example failure (past session, this codebase) |
|---|---|
| Every Acceptance Criterion maps to ≥1 Functional Requirement; every Functional Requirement is motivated by ≥1 AC | Orphan ACs (tests for unspecified behavior); orphan FRs (unmotivated work) |
| Every HTTP status code mentioned anywhere (AC, FR, Edge Case, NFR) also appears in the API Contract — and the API Contract has no orphan codes | AC3 says `202`, AC6 says `200`, controller enforces `@HttpCode(202)` → silent contradiction |
| Every field name in API Contract request/response is either declared in Data Model **or** explicitly marked as "derived from X" / "server-side snapshot from Y" | `consentText` appears in DB columns but is missing from the request body — reviewer cannot tell whether the field is client-supplied (spoofable PII) or server-snapshotted |
| Every Acceptance Criterion is in the form `When <trigger>, system does <behavior>, observable as <concrete check>` — not a bare behavior name | "e2e: form submission の golden path" is a section name; becomes an AC only when it specifies request shape → expected status → DB row state |
| Every new state value (enum value, status flag, lifecycle column) declared in Data Model has ≥1 Functional Requirement writing it, **and** Edge Cases enumerate every state combination it introduces (A→B→A, delete-then-recreate, partial-then-resume) | `LandingPage.status='PUBLISHED'` added to the enum without a transaction writing it; `unpublish → delete LpFormConfig → republish` is a 3-step path the spec never enumerates |
| Every grep-based Acceptance Criterion matches the code's **actual call shape** — a single-line regex like `update\([^)]*field` does not match a multi-line `.update({ … field … })`, so use a broad identifier grep or pair the narrow regex with one | AC1's single-line `landingPage\.update\([^)]*generatedHtml` could not match `markDone`'s multi-line `.update({ … })` — the verification command shared the exact blind spot that let the Critical through, so the AC would have falsely passed |

#### Pass B — Claim ↔ reality verification (this spec vs existing code / sibling specs)

Catches the failure mode where the spec asserts something about the world that turns out to be false at implementation time.

| Rule | Example failure (past session, this codebase) |
|---|---|
| Every "踏襲 / follows / based on / extends X" claim carries a `file:line` citation, **and** the cited code's actual behavior is transcribed into **Existing Constraints Touched** | "`LpFormCorsInterceptor` follows `BeaconSiteCorsInterceptor`" — the cited interceptor unconditionally sets `Allow-Credentials: true`, contradicting AC1 |
| Every "no change to existing X" / "§Y そのまま採用" claim is verified — replace with "based on X, with diffs: A, B, C" the moment any diff exists | Data Model header says "§5 そのまま" while silently changing `isActive` default and adding `consentText` columns |
| Every Edge Case threshold (size, time, rate) is verified against the actual enforcing code, not assumed | "body > 32kb → 413" sounds observable; `main.ts` actually enforces 6mb globally — the spec is a wish, not an assertion, until the limit is path-scoped |
| Every function signature, shared type, prerequisite, or shared constant that crosses a sibling spec in the same feature family appears identically in both — or one spec explicitly declares "owned by spec X, referenced here" with the canonical signature inlined | `injectBeaconMarkers(html, formKey)` is untyped 2-arg in form spec but `(html: string, formKey: string \| null): string` in publish spec; publish spec depends on `LpFormConfig` from form spec without naming the prerequisite in Dependencies |
| Every closure claim ("only / sole / 唯一 / no other / all / exhaustive") and every liveness claim ("dead / @deprecated / 呼び出し元ゼロ / still active") carries the **complement-grep result** enumerating the full candidate set — not a single confirming instance (Step 2 trigger #4 produced this; Pass B confirms it landed in the spec) | "injectAndSaveGtmSnippet is the 唯一の write 経路" — `markDone` (`:404`) also wrote the column → Critical; "errorMessage is active because markFailed writes it" — `markFailed` had zero callers → Warning |
| Every removal / scope item in a referenced parent spec is either carried into this follow-up or explicitly deferred with a stated reason — a follow-up never silently narrows the parent's declared scope | Parent plan §3 said "delete `markDone`/`markFailed`"; the follow-up's removal list dropped `markDone`, so the dropped column would still be referenced by a live build target |

#### Pass C — Schema invariants (Data Model mechanical rules)

Catches Data Model omissions that make the migration fail at `prisma generate`, the first delete attempt, or the first concurrent insert. The two highest-frequency Criticals are inline; the full ruleset (NOT NULL backfill, FK index, composite uniqueness, multi-tenant scope, enum domain, `timestamptz`) is in the shared [../references/schema/core.md](../references/schema/core.md) Part B, with stack-specific syntax in the matching `../references/schema/<stack>.md`.

| Rule | Example failure (past session, this codebase) |
|---|---|
| Every new DB `@relation` has the reverse-relation field declared on the other model **in this spec** (even if the other model already exists in `schema.prisma`) | `@relation` on `LpFormSubmission` pointing at `LandingPage` without adding `lpFormSubmissions LpFormSubmission[]` on `LandingPage` → `prisma generate` fails |
| Every `onDelete` rule (`Restrict / Cascade / SetNull / NoAction`) has its API consequence specified in the API Contract (typically `409 Conflict` for `Restrict`, a destructive-side-effect note for `Cascade`) | `onDelete: Restrict` on submissions, but `DELETE /api/lp-forms/:id` lacks `409 Conflict` and the operator UX for "delete submissions first" |

For the full Data Model self-check, run the [../references/schema/core.md](../references/schema/core.md) Part C checklist.

---

This step is **mandatory for the Medium/Large path** (Step 4b), **for the appended amendment in Re-plan Mode** (Step 4c), and **for any in-place append of implementation detail to an existing plan or spec** — including a free-form 追補 / follow-up block added via `Edit` rather than through `--update-spec`. The append path is the one that silently skips this pass: it is neither a fresh Step 4b generation nor a formal Step 4c invocation, so the failure that motivated these rules (a follow-up 追補 whose "唯一の write 経路" closure claim was never complement-grepped) lands exactly there. Run at minimum **Pass B and Pass C** on any such append, and Pass A as well when the append introduces or changes an Acceptance Criterion. For the Small path (Step 4a), Step 5's structural checks suffice — Small plans rarely span enough sections for cross-section drift.

If any pass surfaces ≥1 issue, fix and re-run **that pass**. The loop terminates only when every row answers "yes, see <pointer>". This investment is what prevents `ywc-spec-validate` from returning `DONE_WITH_CONCERNS` and forcing a Re-plan iteration — the cost is paid once here instead of being amplified across the spec-validate fan-out and the re-plan amendment.

### Step 5: Handoff

Always end with an explicit handoff instruction matching the path taken.

**Small path handoff:**

```text
✅ Plan ready: <path>
Next: implement directly, or run /ywc-code-gen, or /ywc-sequential-executor
```

**Medium/Large path handoff:**

Output this block first:

```text
✅ Spec drafted: <path>
```

**Optional: mission write-back (AC14).** A plan *finalizes* a durable success criterion when it reaches this Step 5 handoff carrying **≥1 new durable success criterion** — a measurable, project-level done-condition that is not already present in `docs/project-mission.md` (a feature-only, throwaway done-condition does not count). When that holds, offer **once** to persist it:

```text
This plan finalized N new durable success criterion(s). Add to docs/project-mission.md?
→ /ywc-project-mission --mode update --source plan   [y / skip]
```

On acceptance, invoke `ywc-project-mission --mode update --source plan` (its CHANGESET confirmation gate still applies). On decline or silence, it is a clean no-op — never write the mission file unasked, and never block the handoff on the answer. Skip the offer entirely when the plan introduces no new durable criterion (the common case for small/feature plans).

Then ask the user (skip when `--non-interactive` is set):

> The spec draft is complete. Run `ywc-spec-ready` to drive the validate → converge loop (validate → DONE) automatically?
> - **y** → run `/ywc-spec-ready <path>` now.
> - **n** → proceed manually with the steps below:
>   1. `/ywc-spec-validate --spec <path>`
>   2. (after review passes) `/ywc-task-generator <path>`
>   3. (after tasks are generated) `/ywc-sequential-executor` or `/ywc-parallel-executor`

If the user responds **y** (or equivalent affirmative), invoke `ywc-spec-ready <path>` immediately.
If the user responds **n**, skips the prompt, or `--non-interactive` is set, do not proceed further — the three manual steps above are the guide.

The `ywc-spec-ready` prompt is an opt-in shortcut, not automatic execution. The user decides the next action — this skill is the planner, not the executor.

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
- [ ] Step 2 deep-read **every component the spec claims to "踏襲 / follow / extend"** (not just located them)
- [ ] Step 2 grepped every **implicit reference** (property accessor on existing type, named audit/event/DTO/error type, mirrored column name) to confirm the existing schema/types match the spec's use
- [ ] Step 2 ran the **complement grep** for every **closure** ("only / 唯一 / no other / all / exhaustive") and **liveness** ("dead / @deprecated / 呼び出し元ゼロ / active") claim, enumerating and classifying the full candidate set (Step 2 trigger #4), with each hit attributed to its own `file:line`
- [ ] The plan's change list contains only sites the request **requires** changing; enumerated-but-incidental sites are recorded as "no change needed" under Existing Constraints Touched (no "while I'm here" refactors)
- [ ] If the plan names a **parent spec**, Step 2 read it and confirmed the follow-up does not silently narrow the parent's removal / scope list
- [ ] Step 3 selected exactly one scale, with the rubric criterion that matched stated explicitly
- [ ] If scale = Small, none of the hard-disqualifiers apply (re-check DB / library / API contract / cross-cutting)
- [ ] If scale = Medium/Large, the spec includes an **Existing Constraints Touched** section with `file:line` citations for every inherited behavior
- [ ] If scale = Medium/Large, **Step 4b.5 Self-Consistency Pass** ran (all three passes A/B/C) and every row resolved to a concrete pointer
- [ ] If Re-plan Mode (Step 4c) ran, **Step 4b.5 was re-run on the whole spec** (original + amendment) before handoff
- [ ] If this run was an **in-place append** (追補 / follow-up) to an existing plan/spec, Step 4b.5 (≥ Pass B + C) ran on the appended content
- [ ] If Re-plan Mode changed an instruction an original section still states literally, a `> ⚠️ SUPERSEDED ...` marker plus a top-of-file **Operative Sections** pointer was added
- [ ] Output file written at a concrete path (no `<placeholder>` slugs)
- [ ] Out of Scope is non-empty (use `N/A — none identified` if truly none)
- [ ] Handoff message printed verbatim with the file path filled in
- [ ] Did not auto-execute downstream — invoked `ywc-spec-ready` **only** on an explicit **y**; for an **n** answer, a skipped prompt, or `--non-interactive`, ran no downstream skill at all

## Common Mistakes

(Procedural failure modes specific to this skill. Behavioral / rationalization failures are in the Rationalization Defense table above — do not duplicate here.)

- **Conflating ywc-plan with ywc-tech-research** — `ywc-plan` assumes the technology choice is settled or out of scope for this request. If the user is asking *what library to use* or *what architecture to adopt*, route to `ywc-tech-research` first, then return to `ywc-plan` after.
- **Forgetting the handoff message** — without an explicit handoff, the user is left guessing which downstream skill to run. The handoff is the contract that this skill is a planner, not an executor.
- **Treating Step 4b.5 as a single pass instead of three** — Pass A, B, and C catch different classes of drift. Skipping any one of them is the most common way Step 4b.5 fails to prevent a Critical. The cost of running all three is ~5 minutes; the cost of skipping one is a full re-plan iteration.

## Integration

- **Upstream**: `ywc-tech-research` (when technology choice is unsettled before planning)
- **Downstream (Small path)**: `ywc-code-gen`, `ywc-sequential-executor`
- **Downstream (Medium/Large path)**: `ywc-spec-ready` (auto-converge shortcut) or `ywc-spec-validate` → `ywc-task-generator` → `ywc-sequential-executor` / `ywc-parallel-executor`
- **Pairs with**: `ywc-product-review` (run before `ywc-plan` when business framing is unclear), `ywc-project-docs` (run after if `docs/` set is missing)
- **Reads / writes-back**: `ywc-project-mission` — Step 1 reads `docs/project-mission.md` (best-effort) to frame clarification and seed Acceptance Criteria; Step 5 offers an opt-in `update --source plan` write-back when the plan finalizes ≥1 new durable success criterion. Both are no-ops on absence / decline (NFR2).
