---
name: ywc-code-gen
description: >-
  (ywc) Use when the user wants parallel multi-layer code generation (Backend + Frontend + QA simultaneously) from a spec. Triggers: "코드 생성", "code gen", "풀스택 생성", "full-stack generation", "scaffold feature", "CRUD 생성", "API + UI 동시 생성", "コード生成". Do not use for single-file edits, refactoring an existing module, debugging, or when no specification exists.
---

# ywc-code-gen

**Announce at start:** "I'm using the ywc-code-gen skill to generate Backend + Frontend + QA layers in parallel."

Multi-layer code generation Skill. Runs Backend + Frontend + QA agents in parallel.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "Reuse Gate is overhead, the spec is clear" | Reuse Gate prevents reimplementing existing code. Skip only with `--skip-reuse-check`. |
| "Phase 1 output looks fine, no need for Phase 2" | Phase 2 is for genuinely ambiguous design decisions. Phase 1 confidence ≠ correctness. |
| "I'll use `// TODO: implement` and let the user fill it in" | Stubs are CI failures. **Never deliver a stub** — see Banned Output Patterns. |
| "Token budget is tight, truncating mid-function is OK" | Stop at a clean function boundary and write `[PAUSED — N of M files complete]`. Never mid-function. |
| "I generated test `describe` blocks, that counts as test coverage" | Empty `describe` without `it` is a stub. Tests need real assertions. |
| "Verification gate failed, but the change is small" | Run the failing layer once more after one fix attempt. Then BLOCKED if still failing. Don't ship. |
| "This generation is on `main`, branch creation is bureaucracy" | Always feature branch. Generation on main is a regression vector. |
| "The spec has multiple cases, I'll design a flexible abstraction" | Simplicity First. Build exactly what the spec describes. Unsolicited flexibility is scope creep disguised as good engineering. |
| "I'll add error handling for edge cases that might come up later" | No error handling for scenarios the spec doesn't mention. Trust the spec's boundary conditions. |
| "This helper could be reused elsewhere, I'll make it generic" | Single-use code needs no abstraction. Extract to shared only when the spec explicitly requires it or reuse is confirmed by the Reuse Gate. |
| "I improved the adjacent module's code quality while I was in the file" | Surgical Changes. Remove those improvements. They belong to a different PR and a different review boundary. |
| "I'll design the module interface as I generate the implementation" | Gray Box: design the public interface before generating the body. Write the API signatures and their contracts first — that is a design decision that belongs to you, not the AI. Generate only the implementation body. Interface decisions made under generation pressure produce shallow modules that are expensive to fix later. |
| "I'll write the implementation first, tests are easier to add after the shape is clear" | Outrunning the headlights. Without test feedback, AI-generated implementations grow unchecked until they crash at runtime. Use `--tdd` to enforce RED → GREEN → REFACTOR, or write failing test stubs before any implementation code. |

**Violating the letter of these rules is violating the spirit.** A stub committed today is a runtime crash tomorrow.

## Arguments

| Parameter | Format | Example | Description |
|-----------|--------|---------|-------------|
| `--spec` | `--spec <path>` | `--spec docs/outline/02-api.md` | Specification file path (required) |
| `--feature` | `--feature "desc"` | `--feature "auto-target API"` | Feature description to generate (required) |
| `--skip-reuse-check` | flag | | Skip the Step 0 reuse gate and proceed directly to generation |
| `--tdd` | flag | | Enable TDD checkpoint commits after each RED/GREEN/REFACTOR stage |

## Advisor Pattern

This skill uses **Pattern B (Two-Phase)** from [advisor-pattern.md](../references/advisor-pattern.md). Code generation decisions range from mechanical (scaffold a CRUD endpoint following the project's existing pattern) to genuinely design-heavy (choose between repository pattern vs service layer vs direct query, pick a state management boundary, decide a test seam). Running every generation worker at maximum reasoning depth wastes frontier capacity on the mechanical cases; running every worker at low reasoning depth undersells the design-heavy ones. Phase 1 generates the obvious cases with normal Codex workers; Phase 2 escalates only the genuinely ambiguous design decisions to a short higher-capability advisor pass.

**Budget**: up to 5 design-advisor calls per invocation, shared across all three agents. Most generation tasks should use fewer — Phase 2 is reserved for decisions where more than one valid implementation exists and the correct choice depends on project-specific context.

## Continuous Execution Rule

Execute all steps (0 → 7) without pausing for user confirmation between steps. Do not ask "shall I proceed to Phase 2?" after Phase 1 completes — proceed immediately. Permitted stops are:

- `--spec` or `--feature` not provided (NEEDS_CONTEXT)
- Spec file unreadable or project context unreadable (BLOCKED)
- Reuse Gate: decision is Adopt/Extend/Compose and user has not confirmed full generation (stop only for this confirmation, then proceed after response)
- Verification Gate failure after 1 retry attempt (BLOCKED)

All other mid-execution pauses are not permitted. Phase transitions (Phase 1 → aggregate → Phase 2 → finalize → verify) are silent.

## Execution Steps

**Branch Setup (required before any step)** — All generation and commit work must happen on an isolated feature branch. Before proceeding to step 0, check the current branch:

```bash
git branch --show-current
```

If already on a feature branch (e.g. `feature/<something>`), proceed. If on a long-lived branch (`main`, `develop`, `master`), create and check out a feature branch now:

```bash
git checkout -b feature/<feature-slug>  # derive slug from --feature value, e.g. "auto-target-api"
```

**Post-merge cleanup:** After the generated code has been reviewed and merged (via PR or `--local-merge`), delete the local feature branch:

```bash
git branch -d feature/<feature-slug>
```

When running downstream through `ywc-sequential-executor` or `ywc-parallel-executor`, those skills handle this cleanup automatically. Only run the manual cleanup command when using `ywc-code-gen` standalone without an executor.

0. **Reuse Gate** (skip if `--skip-reuse-check`) — Before generating anything, determine whether an existing artifact can satisfy the feature requirement. Apply this decision matrix in order:

   | Decision | Condition | Action |
   |----------|-----------|--------|
   | **Adopt** | Existing internal code (same repo) covers ≥80% of the requirement | Propose reuse; confirm with user before generating |
   | **Extend** | Existing internal code covers 40–79%; extending is lower risk than generating fresh | Generate an extension patch only |
   | **Compose** | Multiple existing fragments each cover one slice; composition is cleaner than new code | Generate a thin composition layer |
   | **Build** | No existing artifact covers >40%, or existing code would require invasive changes | Proceed to Phase 1 generation |

   Search scope: (1) `Grep` for symbols related to `--feature` in the current repo; (2) scan `package.json` / `pyproject.toml` for already-installed libraries that solve the problem. If the decision is **Adopt**, **Extend**, or **Compose**, report the finding and stop unless the user confirms they want full generation anyway.

1. **Collect Project Context** — Read `AGENTS.md`, `CODEX.md`, `package.json`, and directory structure where present to identify tech stack, project structure, and conventions. If `docs/ubiquitous-language.md` exists, read it — canonical term names and "Synonyms to Avoid" entries must flow into every subagent's context payload; generated code must use canonical terms and never use synonym identifiers. This context stays with the parent; do not forward it wholesale to Phase 2.

2. **Read Specification File** — Extract feature requirements from the `--spec` file.

3. **Phase 1 — Parallel Generation** — Use Codex subagent delegation to spawn three workers in parallel when the environment supports subagents. Do not pass Claude Code-only named dispatch fields; Codex workers receive their role from the prompt and the layer reference file:
   - **Backend worker** — Generate API routes, service layer, and DB migrations. Follow the project's existing patterns (ORM, router structure, etc.). Include [references/backend-agent.md](references/backend-agent.md) and the operational base prompt at [prompts/implementer-base.md](./prompts/implementer-base.md) in the dispatch payload.
   - **Frontend worker** — Generate UI components, query hooks, and state management. Follow the project's UI framework and conventions. Include [references/frontend-agent.md](references/frontend-agent.md) and the operational base prompt at [prompts/implementer-base.md](./prompts/implementer-base.md) in the dispatch payload.
   - **QA worker** — Generate unit tests, integration tests, and E2E scenarios. Follow the project's test runner and existing test patterns. Include [references/qa-agent.md](references/qa-agent.md) and the operational base prompt at [prompts/implementer-base.md](./prompts/implementer-base.md) in the dispatch payload.

   **Subagent prompt composition**: each subagent dispatch consists of (i) the `--spec` excerpt for the layer, (ii) the project context (AGENTS.md / CODEX.md / package.json / equivalent), (iii) the canonical term table from `docs/ubiquitous-language.md` if it exists (include the "Synonyms to Avoid" column), (iv) the layer's role reference (`references/backend-agent.md`, `references/frontend-agent.md`, or `references/qa-agent.md`), and (v) the operational base prompt at [prompts/implementer-base.md](./prompts/implementer-base.md) appended verbatim. The base prompt is the single source of truth for the Question-First gate, Completeness directive, status protocol, return-artifact format, and scope boundaries; updates touch one file rather than three subagent dispatches in this skill plus the analogous sites in `ywc-sequential-executor` / `ywc-parallel-executor`.

   **Handling each Phase 1 subagent's status return**: each subagent ends its run with one of `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`. The orchestrator's response is defined by [../references/subagent-status-actions.md](../references/subagent-status-actions.md): `NEEDS_CONTEXT` → provide the missing context and re-dispatch at the same model class; `BLOCKED` → run the four-step triage (context → reasoning → scope → plan) before surfacing to the user; `DONE_WITH_CONCERNS` → read the concerns and decide whether they are correctness-level (fix and re-dispatch) or observation-level (carry into the final report). Do not silently retry on the same input.

   ## Status Routing

   Codex worker subagents return payloads per [../references/subagent-status-actions.md](../references/subagent-status-actions.md) §3.5. Apply the following routing table to every Phase 1 subagent return:

   | Returned status | Caller action |
   |---|---|
   | `DONE` | Proceed to Step 4 (aggregate Phase 2 candidates) and Phase 2 advisor pass |
   | `DONE_WITH_CONCERNS` | Continue; accumulate concerns into Phase 2 advisor input or the Completion Report depending on whether they raise correctness or observation issues |
   | `BLOCKED` | Run the four-step triage (context → reasoning → scope → plan), surface to user, halt generation for the blocked lane |
   | `NEEDS_CONTEXT` | Provide the missing context and re-dispatch the same subagent at the same model class — do not silently infer |
   | Status absent or unparseable | Treat as implicit `BLOCKED`; surface the raw payload to the user without re-dispatch |

4. **Aggregate and Select Phase 2 Candidates** — Combine candidate lists from all three subagents:
   - Deduplicate candidates that point to the same decision (for example, Backend and QA both flagging the repository interface shape).
   - Cap the total at 5 per invocation. If candidates exceed the cap, prioritize: architecture-level > shared contract > single-layer decisions.
   - Log dropped candidates in the final report so the user can see what was not escalated.

5. **Phase 2 — Design Advisor Pass** — For each surviving candidate, spawn a short higher-capability advisor subagent:
   - **Context payload**: only the decision point, the alternatives, the spec excerpt, the relevant existing-project pattern, and the tech-stack essentials. Do **not** forward the full spec, the full generated code from other agents, or Phase 1 transcripts.
   - **Expected output**: a short verdict (≤200 words) containing the recommended alternative, a one-line rationale, and any constraints the executor should apply when finalizing the code (for example, "use the existing UserRepository interface; do not add a new abstraction").
   - Advisor calls are sequential, not parallel — each is small and fast, and sequential execution keeps the budget enforcement simple and auditable.

6. **Finalize and Output** — Apply the Phase 2 verdicts to the Phase 1 generated code. Reconcile shared type/interface conflicts. Verify import path consistency and confirm file placement matches the project directory structure. Mark each file in the final report with its provenance: `[P1]` for files Phase 1 generated with confidence, `[P2]` for files whose design was adjusted by a Phase 2 advisor verdict.

7. **Verification Gate** — After writing all generated files, run these checks in order. If a check fails, attempt one fix and re-run that layer. If it still fails after the fix attempt, stop and report before declaring DONE. Do not stop at first failure without attempting a fix.

   **Surface format**: every verification result in this gate must follow `ywc-verify-done` — the verification block (command, output excerpt, exit code) appears **before** the Completion Status line, no `should` / `probably` / `seems` language in the claim, and a failing check is surfaced as `DONE_WITH_CONCERNS` (or routed to `ywc-debug-rootcause` when ≥2 fixes fail on the same layer) rather than a bare "Done" with the failure tucked below.

   | Phase | Command (adapt to project tooling) | Pass Condition |
   |-------|------------------------------------|----------------|
   | Build | `npm run build` / `cargo build` / `go build ./...` | Exit 0 |
   | Type check | `tsc --noEmit` / `mypy` / `pyright` | No new errors |
   | Lint | `eslint` / `ruff` / `golangci-lint` (project's lint command) | No new errors |
   | Tests | `npm test` / `pytest` / `go test ./...` | All tests pass |

   If no build or test command is configured in `package.json` / project config, note "No verification configured — manual check required" and set Completion Status to `DONE_WITH_CONCERNS`.

   **When `--tdd` is set**, instead of running tests only at the end, enforce checkpoint commits at each stage:
   - After generating the test file (RED state): `git commit -m "test: add tests for <feature>"` — verify tests fail before committing.
   - After implementing code that makes tests pass (GREEN state): `git commit -m "feat: implement <feature>"`.
   - After any cleanup or refactor: `git commit -m "refactor: clean up <feature>"`.
   - If tests do not fail in RED state, that is a test authoring error — stop and report `DONE_WITH_CONCERNS`.

   The canonical RED → GREEN → REFACTOR cycle (including the mandatory "watch it fail" step, anti-patterns, and per-step exit conditions) is defined in [`ywc-tdd-ritual`](../ywc-tdd-ritual/SKILL.md). When `--tdd` is set, this step delegates the cycle discipline there; the executor here only wires the three commit boundaries and reports the per-stage verification blocks per `ywc-verify-done`.

## Output Format

```text
## Code Generation Result: {feature}

### Summary
- Reuse gate decision: {Adopt|Extend|Compose|Build} — {one-line rationale}
- Phase 1 generated files: Backend N, Frontend M, QA K
- Phase 2 advisor calls: X of 5 budget used
- Phase 2 adjustments: N design decisions confirmed, M revised
- Verification gate: {PASS|FAIL|SKIPPED} — {failing phase if FAIL}

### Generated Files
- Backend: [file list, each marked [P1] or [P2]]
- Frontend: [file list, each marked [P1] or [P2]]
- QA: [file list, each marked [P1] or [P2]]

### Design Decisions (Phase 2)
1. [P2] {decision point} → {chosen alternative}
   Rationale: {one-line rationale from advisor}

### Per-Agent Summary
(Summary of what each agent generated)

### Next Steps
(Items requiring manual review or configuration)

### Advisor Budget Report
- Used: X of 5 calls
- Dropped (over budget): {list, if any}

### Completion Status
(One of: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT)
```

**Completion Status rules:**

| Status | When to use |
|--------|------------|
| `DONE` | All files generated with no banned patterns, advisor budget within limit |
| `DONE_WITH_CONCERNS` | Generation complete but with issues — banned patterns required retry, advisor budget exceeded, or stubs that need manual follow-up |
| `BLOCKED` | Generation cannot proceed — spec file missing, project context unreadable, or a critical ambiguity with no resolvable default |
| `NEEDS_CONTEXT` | `--spec` or `--feature` argument is too vague to generate useful code without clarification |

## Banned Output Patterns (Hard Failures)

Any subagent output containing the following patterns is treated as a failed generation — retry or escalate, never deliver as-is. Downstream tools (ywc-sequential-executor, CI) will compile and test whatever is generated; a stub is a runtime error, not deferred work.

Catch the high-confidence comment/marker stubs mechanically before delivering (more reliable than self-review; exits non-zero on any hit):

```bash
STUB_SCRIPT="codex/skills/scripts/scan-stubs.sh"
[ -f "$STUB_SCRIPT" ] || STUB_SCRIPT="${CODEX_HOME:-$HOME/.codex}/skills/scripts/scan-stubs.sh"
bash "$STUB_SCRIPT" <generated-file>...
```

The script gates the comment/marker forms below; the prose shortcuts and bare `...`/`pass` placeholders still need your own read, since they false-positive in real code and docs.

**Code stubs (never acceptable in generated files):**
- `// TODO: implement` / `// FIXME` / any implementation replaced by a comment only
- `// ... rest of code` / `// ...` / `/* ... */` used to omit logic
- `// similar to above` / `// same as X` / `// follows the same pattern`
- Bare `...` or `pass` as a placeholder for omitted logic
- `throw new Error("Not implemented")` or language equivalents (`raise NotImplementedError`, `todo!()`, `unimplemented!()`)

**Prose shortcuts (never acceptable in generated files):**
- "The rest follows the same pattern"
- "You can extend this with..."
- "For brevity, only showing..."
- "I'll leave X for you to implement"
- "See [other file] for the full implementation"

**Structural incompleteness:**
- Functions or methods with a signature but no real body
- Test `describe`/`context` blocks with no `it`/`test`/`spec` cases inside them
- Type definitions using `any` / `unknown` as a placeholder for real types
- Config or schema files containing `YOUR_VALUE_HERE` or `<replace_me>` tokens

**Scope creep / drive-by edits (never acceptable in generated output):**
- Reformatting or restyling files the spec did not name — adjacent imports reordered, whitespace fixed, blank lines normalized, formatter run repo-wide because "it was easier than configuring the scope"
- "While I'm here" docstring polish, comment rewording, or rename of a private symbol whose signature the spec did not touch — every such edit must wait for its own task
- Magic-number → named-constant extraction in production code from a test-only task, or any production-code refactor surfaced "for free" while authoring tests
- Bug-fix commits that bundle surrounding cleanup (dead-import removal, error-message rewording, log-level adjustment) — the fix and the cleanup ship in separate commits on separate branches
- Type-annotation tasks that also remove unused exports, mark functions `internal`, or shrink the public surface — every public-surface change is its own review boundary, not a side effect of typing

## Agent Prompt References

Read the corresponding reference file when spawning each agent and include it in the agent prompt:

- `references/backend-agent.md` — Backend generation targets, coding standards, and output checklist
- `references/frontend-agent.md` — Frontend generation targets, accessibility standards, and output checklist
- `references/qa-agent.md` — QA generation targets, test strategy, and output checklist

## Confidence Gate

This skill applies the [Confidence Gate](../references/confidence-gate.md) before emitting generated code as a final artifact. The gate is evaluated by the Phase 2 advisor when one is invoked, or by the executor itself otherwise.

**Required dimensions** (must each score ≥ 70):

- **Architecture compliance** — Generated code that introduces new patterns inconsistent with the existing structure produces costly cleanup downstream. Verify against the project's actual layout, not against generic conventions.
- **Reuse verified** — Before emitting any new utility, helper, or service, the relevant existing modules (`src/utils/`, `lib/`, project dependencies) must have been searched. Reimplementing existing functionality is a gate failure even if the new code is correct.

**Band-to-status mapping** for this skill:

| Gate band | Completion status | Action |
|-----------|-------------------|--------|
| PROCEED (≥ 90) | DONE | Code is ready for `ywc-impl-review`. |
| REVIEW (70 – 89) | DONE_WITH_CONCERNS | Emit code, but flag the weakest dimension and the rationale in the completion summary. The reviewer must see this. |
| STOP (< 70) | BLOCKED | Do not emit code. Report what evidence (architecture scan, reuse search) is missing. |

The gate score must appear in the completion summary together with the Backend / Frontend / QA file counts. The Phase 2 advisor budget (5 calls) covers gate evaluation; do not double-count.

## Integration

- **upstream**: After specification is finalized
- **downstream**: Implementation review (ywc-impl-review), PR creation
- **relationship**: Complementary to sequential-executor (independent layer parallel generation)
