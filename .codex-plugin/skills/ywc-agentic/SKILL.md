---
name: ywc-agentic
description: >-
  (ywc) Use when the user provides a high-level natural-language goal and wants
  Codex to run the existing ywc-* pipeline autonomously through Plan → Execute
  → Evaluate → Repeat until code is implemented and verified. Triggers:
  "agentic", "autonomous workflow", "goal to code", "autonomous delivery",
  "ywc-agentic", "자율 실행", "자동 구현", "自律実行", "自律ワークフロー".
  Do not use for one-off skill invocations (use the named sibling directly),
  manual task implementation (use ywc-code-gen or an executor), or when the
  user wants explicit control over each phase (use ywc-plan first).
---

# ywc-agentic (Agentic Orchestrator)

**Announce at start:** "I'm using the ywc-agentic skill to orchestrate the ywc-* pipeline autonomously from goal to verified implementation."

This skill turns a single natural-language goal into delivered code by orchestrating the existing `ywc-*` skills through an autonomous **Plan → Execute → Evaluate → Repeat** loop. It does not implement code itself — it sequences `ywc-plan`, `ywc-spec-validate`, `ywc-task-generator`, an executor, `ywc-impl-review`, and (for Small-scale goals) `ywc-code-gen`, then re-plans on evaluation failure until the implementation passes review or a user-defined iteration ceiling is reached.

```text
User → Goal → Agent [Plan → Execute → Evaluate → Repeat] → Result
```

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "The loop does not look like it is converging — bump `--max-iterations`" | `--max-iterations` is a **user-defined safety valve**. The agent never raises it autonomously. If the ceiling is reached, emit the partial-completion report and stop — surfacing non-convergence to the user is the correct outcome, not silently grinding more iterations. |
| "The evaluation failed but the issues look trivial — continue without re-planning" | Any `ywc-impl-review` finding at **HIGH or CRITICAL** severity triggers a mandatory re-plan. There is no "trivial" exception. `DONE_WITH_CONCERNS` is a Fail verdict for loop-control purposes — only `DONE` (zero CRITICAL/HIGH) ends the loop with a Pass. |
| "Re-run the already-merged tasks too, just to be safe" | Merged tasks (present in `<tasks-dir>/completed/` or already in the base-branch git log) are **never** re-executed. Re-running them risks duplicate commits, merge conflicts, and undoing later iterations. Resume safety depends on this invariant. |
| "Small path only needs a `plan.md`, so `ywc-task-generator` is dead weight — skip straight to executor" | Small path is a **dedicated route**: `ywc-plan` (Small verdict) → `ywc-code-gen` directly, with no `ywc-task-generator` and no executor. It is not a degraded Medium path. Do not invent a hybrid. The loop control (max iterations, evaluate, re-plan) is identical, but the Plan and Execute phases use the Small Path contract in Step 3 / Step 5. |
| "`ywc-impl-review --code` can just look at everything — simpler than tracking git ranges" | Iterative evaluation **always** uses `--git-range <pre-iter-sha>..HEAD` so each pass scopes to that iteration's changes, and **always** passes the original full spec via `--spec`. Using `--code` or a narrow re-plan spec lets iteration-1 regressions slip through undetected. The pre-iteration SHA is recorded in Step 5 before the executor runs. |
| "Re-plan produced roughly the same spec — run it anyway, maybe it works this time" | A re-plan that produces the **same scope** as the previous iteration means the loop is stuck. Detect it (Step 7 recursion guard), mark the iteration failed, and stop. Repeating an identical iteration burns budget and never converges. |
| "A merge conflict appeared mid-execute — resolve it automatically and keep going" | The loop **never** auto-recovers from merge conflicts or CI errors. Record the state in `tasks/agentic-log.md`, report to the user, and stop. Automatic conflict resolution risks silent data loss. |

**Violating the letter of these rules is violating the spirit.** The loop is trustworthy only because its termination conditions and re-plan triggers are non-negotiable.

## Arguments

| Parameter | Format | Default | Description |
|---|---|---|---|
| `<goal>` | positional string | _(required)_ | Natural-language description of the goal to achieve. |
| `--goal` | `--goal "<text>"` | — | Alternative to the positional `<goal>`. If both are given, the positional value wins. |
| `--max-iterations` | `--max-iterations <n>` | `3` | Maximum loop iterations. User-defined safety valve — never raised autonomously. |
| `--executor` | `--executor <sequential\|parallel\|auto>` | `auto` | Forces an executor. `auto` selects from `tasks/dependency-graph.md` (see Step 4). |
| `--tasks-dir` | `--tasks-dir <path>` | `tasks/` | Root directory for task directories and `agentic-log.md`. |
| `--resume` | flag | — | Skip the Plan Phase and resume from existing `tasks/` (Resume Mode). |
| `--dry-run` | flag | — | Print the planned phase sequence only; invoke no skills and make no changes. |
| `--terse` | flag | — | Minimal output — phase headers and the final report only, no per-phase prose. |
| `--pr-lang` | `--pr-lang <lang>` | `auto` | PR title/description language, forwarded to the executor. `auto` infers from `CLAUDE.md`. |

## Workflow

The loop runs Steps 3–8 once per iteration. Steps 1–2 run once at start; Step 9 runs once at the end. Each phase transition announces progress to the user (suppressed under `--terse`).

### Step 1: Receive and Validate the Goal (FR-1)

Read the goal from the positional `<goal>` argument or the `--goal` flag. If both are present, the positional value takes precedence.

- If no goal is supplied, ask the user: *"What goal should I implement? Provide a natural-language description."* Do not proceed without a goal.
- Derive a filesystem-safe `<slug>` from the goal (lowercase, hyphenated, ≤40 chars) for deterministic artifact paths.
- If `--dry-run` is set, from here on only print the phase plan (Plan → Task → Execute → Evaluate, with the chosen Mode) and stop without invoking any skill.

### Step 2: Detect Project Context — Resume vs. Full Mode (FR-2)

Read the project's convention files to ground every downstream skill call:

- `CLAUDE.md`, `AGENTS.md` — project rules, language policy, CI commands.
- `package.json` / `pyproject.toml` / `Makefile` / `go.mod` — language and build/test/lint commands.
- `docs/ubiquitous-language.md` (if present) — canonical domain terms to forward to the executor.

Then decide the Mode:

- **Resume Mode** — Enter when `--resume` is set, **or** when `<tasks-dir>/` exists and contains at least one task directory that is **not** under `<tasks-dir>/completed/`. Resume Mode skips Step 3 (Plan Phase) entirely.
- **Full Mode** — Enter otherwise (no `tasks/`, or every task already completed). Full Mode starts from Step 3.

Edge case: if `--resume` is set but `<tasks-dir>/` is empty or absent, do not silently restart — report the mismatch and propose switching to Full Mode (see Edge Cases).

### Step 3: Plan Phase (FR-3)

Skipped entirely in **Resume Mode**. In **Full Mode** (first iteration) and on **Re-plan** (subsequent iterations):

**Full Mode — first iteration:**

1. Invoke `ywc-plan` non-interactively with a deterministic output path:
   ```text
   ywc-plan --non-interactive --output docs/ywc-plans/agentic-<slug>-iter1.md
   ```
   `--non-interactive` makes `ywc-plan` fill open questions with anchored defaults instead of prompting. `--output` pins the artifact path so later steps and re-plans can locate it.
2. Branch on the scale verdict from `ywc-plan`:
   - **Small** → take the **Small Path**: `ywc-plan` produced a `plan.md`. Skip Steps 4 and the executor; go directly to `ywc-code-gen` in Step 5 (Small Path). `ywc-task-generator` is not used.
   - **Medium / Large** → `ywc-plan` produced a spec. Run `ywc-spec-validate` against it; if `ywc-spec-validate` reports any CRITICAL issue, stop and report (the spec is not safe to decompose). Otherwise continue to Step 4 (Task Phase).

**Re-plan — iteration N > 1 after an Evaluate Fail:**

- Do **not** create a new spec file. Invoke:
  ```text
  ywc-plan --update-spec docs/ywc-plans/agentic-<slug>-iter1.md --failure-context "<fix-priority section>"
  ```
- `--update-spec` appends an `## Iteration N Amendments` section to the **original** spec, so completed-task context is preserved. `--failure-context` carries the prioritized CRITICAL/HIGH findings from the previous Evaluate Phase (Step 6) — the corrective scope, not the whole spec.
- After the amendment, Medium/Large goals re-enter Step 4 with only the amended/uncovered tasks; Small Path goals re-enter Step 5 (Small Path) with the amended `plan.md`.

The "original spec" reference (`docs/ywc-plans/agentic-<slug>-iter1.md`) is fixed for the entire run and reused verbatim by every Evaluate Phase.

### Step 4: Task Phase (FR-4)

Medium/Large goals only. Skipped on the Small Path.

1. Invoke `ywc-task-generator` against the (possibly amended) spec, writing into the configured directory:
   ```text
   ywc-task-generator --tasks-dir <tasks-dir>
   ```
   `ywc-task-generator` infers the output language from `CLAUDE.md`; no `--lang` is passed unless the user requested one.
2. Read `<tasks-dir>/dependency-graph.md` and select the executor:
   - `--executor` is explicit → use that executor.
   - `--executor auto` and the graph yields **multiple waves with independent tasks** → `ywc-parallel-executor`.
   - `--executor auto` and **all tasks are strictly sequential** → `ywc-sequential-executor`.
3. On a Re-plan iteration, `ywc-task-generator` numbers the new tasks past the highest existing sequence so already-completed tasks are untouched.

### Step 5: Execute Phase (FR-5)

**Record the pre-iteration baseline first.** Before invoking any executor, capture and store the current commit SHA:
```text
git rev-parse HEAD   →   <pre-iter-sha>
```
This SHA is the lower bound of the `--git-range` passed to the Evaluate Phase. Record it in the iteration's working state.

**Medium/Large path:** invoke the executor selected in Step 4 in local-merge mode:
```text
ywc-<sequential|parallel>-executor --all --tasks-dir <tasks-dir> --local-merge --pr-lang <pr-lang>
```
`--local-merge` keeps iterations fast — no PR round-trip; completed tasks merge to the base branch directly. After the executor returns, collect each task's success/failure status from its return payload.

**Small Path:** invoke `ywc-code-gen` directly against the `plan.md` from Step 3. No executor, no `tasks/` directory. `ywc-code-gen` commits its output to the base branch so the Evaluate Phase can range over it.

If the executor or `ywc-code-gen` reports a merge conflict or unrecoverable CI error, stop immediately — record to `agentic-log.md` (Step 8) and report (see Edge Cases). Never auto-resolve.

### Step 6: Evaluate Phase (FR-6)

Run `ywc-impl-review` over only this iteration's changes, judged against the original full spec:
```text
ywc-impl-review --spec docs/ywc-plans/agentic-<slug>-iter1.md --git-range <pre-iter-sha>..HEAD
```
- `--spec` is **always the original full spec**, never a re-plan's narrow amendment. A narrow spec would not flag regressions that iteration N introduced into iteration 1's code.
- `--git-range` scopes the review to commits added during this iteration (`<pre-iter-sha>` recorded in Step 5).
- Small Path: `--spec` is the `plan.md` from Step 3; `--git-range` is unchanged.

Classify the verdict from `ywc-impl-review`'s Completion Status:

| `ywc-impl-review` status | Verdict | Meaning |
|---|---|---|
| `DONE` | **Pass** | No CRITICAL or HIGH issues. |
| `DONE_WITH_CONCERNS` | **Fail** | One or more CRITICAL/HIGH issues — re-plan required. |
| `BLOCKED` / `NEEDS_CONTEXT` | **Fail (hard stop)** | Review could not complete — record and stop, do not re-plan blindly. |

### Step 7: Loop Control (FR-7)

Maintain an iteration counter starting at 1. After each Evaluate Phase:

| Condition | Action |
|---|---|
| Verdict = **Pass** | Exit the loop. Proceed to Step 8 (log) then Step 9 (Completion Report). |
| Verdict = **Fail** and `iteration < max-iterations` | Build the failure context (the prioritized CRITICAL/HIGH findings as a "fix-priority" section), increment the counter, return to Step 3 (Re-plan). |
| Verdict = **Fail** and `iteration >= max-iterations` | Exit the loop. Proceed to Step 8 then Step 9, which emits a partial-completion report listing unresolved issues. |
| Verdict = **Fail (hard stop)** | Exit the loop immediately. Record to `agentic-log.md` and report — the loop cannot make a safe decision. |

**Recursion guard:** before starting a Re-plan iteration, compare the new amendment's scope against the previous iteration's scope. If they are effectively identical (same target files/tasks, same fix list), the loop is stuck — mark this iteration failed, log it, and stop instead of looping. Do not raise `--max-iterations` to escape this.

### Step 8: Iteration Log (FR-8)

After every iteration (Pass or Fail), append a structured record to `<tasks-dir>/agentic-log.md`. The file is **append-only** — never rewrite prior entries. Format:

```markdown
## Iteration <N> — <ISO-8601 UTC timestamp>
- Phase: <phase combination, e.g. "Full Mode / Plan → Spec → Tasks → Execute → Evaluate">
- Tasks completed: <completed>/<total>
- ywc-impl-review: <PASS | FAIL (<n> <CRITICAL|HIGH> issues)>
  - <SEVERITY>: <issue description>   ← one line per issue, Fail only
```

Concrete example:

```markdown
## Iteration 1 — 2026-05-15T10:30:00Z
- Phase: Full Mode / Plan → Spec → Tasks → Execute → Evaluate
- Tasks completed: 4/4
- ywc-impl-review: FAIL (2 HIGH issues)
  - HIGH: Missing input validation in POST /api/users
  - HIGH: SQL injection risk in search query
```

`Tasks completed` is the integer `<completed>/<total>` pair (for the Small Path, use `1/1` when `ywc-code-gen` succeeds, `0/1` when it fails). If the loop stopped on an exception, append the exception cause as a final line before reporting.

### Step 9: Completion Report (FR-9)

Emit one final report to the user:

- **Goal** — the original goal string.
- **Mode** — Full / Resume, and Small Path / Medium-Large path.
- **Iterations run** — `<n>` of `<max-iterations>`.
- **Tasks completed** — aggregate completed/total across the run.
- **Outcome** — `Converged` (final verdict Pass), `Ceiling reached` (max iterations hit), or `Stopped` (exception).
- **Remaining issues** — bullet list of unresolved CRITICAL/HIGH findings, if any.
- **Artifacts** — original spec path, `agentic-log.md` path.

End the report with one Completion Status line — nothing follows it:

| Status | When |
|---|---|
| `DONE` | Final verdict Pass — implementation passed `ywc-impl-review`. |
| `DONE_WITH_CONCERNS` | Ceiling reached with unresolved issues, or partial completion. |
| `BLOCKED` | Loop stopped on a merge conflict, CI error, or other exception requiring human action. |
| `NEEDS_CONTEXT` | Goal or arguments were too ambiguous to start the loop. |

## Edge Cases

| Case | Handling |
|---|---|
| `ywc-plan` returns a **Large** verdict (15+ tasks) | Defer to `ywc-plan`'s existing Large-scale logic — it proposes splitting the spec to the user. Proceed with whatever `ywc-plan` produces; do not override its scale judgment. |
| **Merge conflict** during the Execute Phase | Stop immediately. Append the conflict (files, affected tasks) to `agentic-log.md`, report to the user, request manual resolution. Never auto-abort, force, or auto-resolve. |
| **Re-plan produces an identical-scope spec** | Recursion guard (Step 7): mark the current iteration failed, append to `agentic-log.md`, and stop. An identical re-plan means the loop cannot converge — escalate to the user. |
| `--resume` set but `<tasks-dir>/` is **empty or absent** | Report the mismatch: *"--resume was requested but no pending tasks exist in `<tasks-dir>/`."* Propose switching to Full Mode and wait for the user's confirmation before continuing. |
| **Max iterations reached with <50% tasks completed** | Include an explicit `"Partial completion"` warning in the Completion Report (Step 9) alongside the unresolved-issue list, and use Completion Status `DONE_WITH_CONCERNS`. |
| `ywc-spec-validate` reports a **CRITICAL** spec issue | Stop before the Task Phase — the spec is not safe to decompose. Report the CRITICAL finding; do not proceed to `ywc-task-generator`. |
| **Already-merged task encountered** on a Re-plan | Tasks under `<tasks-dir>/completed/` (or already in the base-branch git log) are never re-executed. `ywc-task-generator` numbers new tasks past the highest existing sequence; the executor runs only the new ones. |

## Validation Checklist

Before treating an `ywc-agentic` run as complete, verify:

- [ ] A goal was received (positional or `--goal`); the run did not start without one.
- [ ] Project context was read (`CLAUDE.md` / build files) before any skill invocation.
- [ ] Mode was decided explicitly (Resume vs. Full) per the Step 2 rule.
- [ ] The pre-iteration `git rev-parse HEAD` SHA was recorded **before** the executor ran, every iteration.
- [ ] Every Evaluate Phase used the **original full spec** for `--spec` and `<pre-iter-sha>..HEAD` for `--git-range`.
- [ ] Re-plan used `ywc-plan --update-spec` — no new spec file was created mid-run.
- [ ] The loop terminated on a Pass verdict, the iteration ceiling, or a recorded exception — never an autonomous `--max-iterations` increase.
- [ ] `<tasks-dir>/agentic-log.md` has one append-only entry per iteration in the FR-8 format.
- [ ] The Completion Report ends with exactly one Completion Status line.
- [ ] Small Path goals used `ywc-code-gen` directly and never invoked `ywc-task-generator` or an executor.

## Integration

- **upstream**: the user's natural-language goal (no predecessor skill).
- **downstream** (orchestrated, not chained):
  - `ywc-plan` — Plan Phase, with `--non-interactive` / `--output` (Full Mode) and `--update-spec` / `--failure-context` (Re-plan).
  - `ywc-spec-validate` — Medium/Large spec quality gate before task decomposition.
  - `ywc-task-generator` — Task Phase, with `--tasks-dir`.
  - `ywc-sequential-executor` / `ywc-parallel-executor` — Execute Phase, in `--local-merge` mode.
  - `ywc-impl-review` — Evaluate Phase, with `--spec` (original) and `--git-range`.
  - `ywc-code-gen` — Small Path Execute Phase, invoked directly from the `plan.md`.
- **Out of scope**: external integrations (GitHub Actions, Slack), dynamic skill creation, and the new skill's own CI/E2E setup — `ywc-agentic` only orchestrates the existing `ywc-*` skill set.
