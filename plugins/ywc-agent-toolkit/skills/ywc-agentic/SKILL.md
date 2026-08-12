---
name: ywc-agentic
description: >-
  (ywc) Use when the user explicitly wants autonomous end-to-end delivery
  through Plan -> Execute -> Evaluate -> Repeat; supports resuming an
  existing `tasks/` run with `--resume`. Triggers: "agentic end-to-end
  lifecycle", "run the full lifecycle", "ywc-agentic", "자율 end-to-end
  실행", "自律エンドツーエンド実行". Do not use for generic planning (use
  ywc-plan), an ordinary direct change (use the implementation workflow), or
  one-off execution without autonomous orchestration (use an executor).
---

# ywc-agentic (Agentic Orchestrator)

**Announce at start:** "I'm using the ywc-agentic skill to orchestrate the ywc-* pipeline autonomously from goal to verified implementation."

This skill turns a single natural-language goal into delivered code by orchestrating the existing `ywc-*` skills through an autonomous **Plan → Execute → Evaluate → Repeat** loop. It does not implement code itself — it sequences `ywc-plan`, `ywc-spec-validate`, `ywc-task-generator`, an executor, `ywc-impl-review`, and (for Small-scale goals) `ywc-code-gen`, then re-plans on evaluation failure until the implementation passes review or a user-defined iteration ceiling is reached.

## Architecture evidence boundary

The optional `.ywc-architecture-invariants-evidence.json` file is diagnostic run evidence only. Agentic flows may pass its validated audit result to an architecture consultation, but must never treat it as authoritative checkpoint or task state. `.ywc-run-state.json`, the task directory, and executor transitions remain authoritative. The artifact is a closed result object containing only `version`, `aggregate_verdict`, and `rule_results`; do not persist or forward `raw_command`, `raw_command_output`, `transcript`, `source`, `generated_source`, `chain_of_thought`, `full_diff`, or unknown fields. Missing, malformed, or out-of-scope evidence cannot authorize execution and remains a diagnostic `NEEDS_CONTEXT` condition.

If the goal is still in a multi-session discovery state with unresolved architectural tickets and no stable plan boundary, stop before the loop and route the user to `ywc-wayfinder`. This skill assumes the goal is ready to enter an implementation-oriented planning pipeline.

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
| `--non-interactive` | flag | — | Close each callee's required inputs immediately before that callee is invoked; never leave a prompt open. Propagated to downstream callees only when the orchestrator itself received it. |
| `--mode` | `--mode <documented-task-generator-mode>` | — | Required for Medium/Large task generation and forwarded unchanged. |
| `--lang` | `--lang <en\|ja\|ko\|zh\|es>` | — | Required only when shared language resolution cannot determine task/spec language. |
| `--suggestions` | `--suggestions <apply\|defer>` | — | Required when `ywc-spec-ready` reports Suggestions. |
| `--resume-disposition` | `--resume-disposition <resume\|stop>` | — | Required only when the selected executor has an authoritative checkpoint. |
| `--dry-run` | flag | — | Print the planned phase sequence only; invoke no skills and make no changes. |
| `--terse` | flag | — | Minimal output — phase headers and the final report only, no per-phase prose. |
| `--pr-lang` | `--pr-lang <en\|ja\|ko\|zh\|es>` | `auto` | PR title/description language, forwarded unchanged to the executor. `auto` resolves through shared YWC language policy; if no tier resolves a language, ask the user before invoking the selected executor — or, under `--non-interactive`, return bounded `NEEDS_CONTEXT: --pr-lang` instead of prompting. |

## Workflow

The loop runs Steps 3–8 once per iteration. Steps 1–2 run once at start; Step 9 runs once at the end. Each phase transition announces progress to the user (suppressed under `--terse`).

### Staged preflight

Argument validation is **staged**: each argument is validated immediately before the callee that consumes it, never earlier. Validating a callee-dependent argument up front would block runs that never reach that callee — a Small-scale goal never needs `--mode`, and Scale is unknown until `ywc-plan` returns its Result.

| Argument | Validated immediately before |
|---|---|
| Planner inputs (`<goal>` / `--goal`, `--tasks-dir`, `--max-iterations`) | the first `ywc-plan` call (Step 3) |
| `--suggestions` | the `ywc-spec-ready` amendment call, once its Result has reported Suggestions (Step 3) |
| `--mode`, `--lang` | Medium/Large task generation, once Scale is known (Step 4) |
| `--resume-disposition` | executor invocation, once the executor's checkpoint has been inspected (Step 5) |
| `--pr-lang` | executor invocation, once shared language resolution has run (Step 5) |

Staging changes only **when** each check runs — no check is removed. At every stage the bounded `NEEDS_CONTEXT` behavior is unchanged: under `--non-interactive` a missing required input for that stage returns a bounded `NEEDS_CONTEXT` naming the exact argument/config key, invokes no callee, and never asks a question or invents a default. A callee is never invoked while its own required input for that stage is missing.

### `--non-interactive` propagation

Forward `--non-interactive` to a downstream callee **if and only if the orchestrator itself received it**. Never force it onto a callee during an interactive run, and never drop it during a non-interactive run. The `--approve-preview` consume call in Step 4 is the sole exception: it is non-interactive by contract, because approval consumption must never prompt.

### Step 1: Receive and Validate the Goal (FR-1)

Read the goal from the positional `<goal>` argument or the `--goal` flag. If both are present, the positional value takes precedence.

- If no goal is supplied, ask the user: *"What goal should I implement? Provide a natural-language description."* Do not proceed without a goal.
- Derive a filesystem-safe `<slug>` from the goal (lowercase, hyphenated, ≤40 chars) for deterministic artifact paths.
- If `--dry-run` is set, from here on only print the phase plan (Plan → Task → Execute → Evaluate, with the chosen Mode) and stop without invoking any skill.

### Step 2: Detect Project Context — Resume vs. Full Mode (FR-2)

Read the project's convention files to ground every downstream skill call:

- `AGENTS.md`, `CODEX.md`, `CLAUDE.md` — project rules, language policy, CI commands.
- `package.json` / `pyproject.toml` / `Makefile` / `go.mod` — language and build/test/lint commands.
- `docs/ubiquitous-language.md` (if present) — canonical domain terms to forward to the executor.

Then decide the Mode:

- **Resume Mode** — Enter when `--resume` is set, **or** when `<tasks-dir>/` exists and contains at least one task directory that is **not** under `<tasks-dir>/completed/`. Resume Mode skips Step 3 (Plan Phase) entirely.
- **Full Mode** — Enter otherwise (no `tasks/`, or every task already completed). Full Mode starts from Step 3.

Edge case: if `--resume` is set but `<tasks-dir>/` is empty or absent, do not silently restart — report the mismatch and propose switching to Full Mode (see Edge Cases).

### Step 3: Plan Phase (FR-3)

Skipped entirely in **Resume Mode**. In **Full Mode** (first iteration) and on **Re-plan** (subsequent iterations):

**Full Mode — first iteration:**

1. Run the planner preflight immediately before the `ywc-plan` call. It validates **only planner-required inputs** — the goal and the run-level arguments the planner itself consumes. Do **not** validate `--mode`, `--lang`, `--suggestions`, or `--resume-disposition` here: Scale is unknown until `ywc-plan` returns, so those arguments belong to their own callees' preflights (see Staged preflight; a Small-scale `--non-interactive` goal must not be blocked on a `--mode` it will never use). In `--non-interactive` mode a missing planner-required input returns a bounded `NEEDS_CONTEXT` naming the exact argument/config key and invokes no callee. Never ask a question or invent a default.
2. Invoke `ywc-plan` using its agentic-owned artifact profile, forwarding `--non-interactive` only when the orchestrator received it:
   ```text
   ywc-plan [--non-interactive] --artifact-profile agentic
   ```
   Agentic accepts authority only from exactly one complete producer Result block:
   ```text
   ## Result
   Status: DONE
   Scale: Small | Medium | Large
   Artifact: <repository-relative regular Markdown file>
   ```
   Parse `Scale` and `Artifact` atomically. Resolve the labelled Artifact against the repository root; require an existing regular Markdown file under `docs/ywc-plans/`, and for Small require `docs/ywc-plans/YYYYMMDD-small_<slug>.md`. Reject duplicate/missing/conflicting fields, absolute or escaping paths, non-Markdown files, unlabelled prose, basenames, requested output paths, and raw-response recovery. A parseable non-`DONE` terminal status is propagated; missing or invalid status/result is `BLOCKED`. The bounded diagnostic may contain only producer, failed field, candidate count, path digest, and reason; never store response text or tool output.
3. Branch on the verified Scale:
   - **Small** → pass the resolved Artifact verbatim to `ywc-code-gen --spec <artifact> --feature <original-goal> --skip-reuse-check`. Skip task generation and executors.
   - **Medium / Large** → pass the resolved candidate Artifact verbatim to `ywc-spec-ready --spec <artifact> [--non-interactive]`, forwarding `--non-interactive` only when the orchestrator received it. Invoke it **without** `--suggestions` first — the flag is only meaningful once a `ywc-spec-ready` Result exists. Only when that Result reports Suggestions does the `--suggestions` preflight run, immediately before the amendment call; under `--non-interactive` a missing `--suggestions` there returns bounded `NEEDS_CONTEXT: --suggestions` with only the count and invokes no further callee. Continue only when its single Result is `Status: DONE`; otherwise propagate its parseable terminal status or return bounded `BLOCKED`.

**Re-plan — iteration N > 1 after an Evaluate Fail:**

- Do **not** create a new spec file or reconstruct an artifact path. Invoke against the verified candidate:
  ```text
  ywc-plan --update-spec <verified-candidate> --failure-context "<fix-priority section>" [--non-interactive] --artifact-profile agentic
  ```
  `--non-interactive` is forwarded only when the orchestrator received it.
- `--update-spec` appends an `## Iteration N Amendments` section to the verified candidate, so completed-task context is preserved. `--failure-context` carries the prioritized CRITICAL/HIGH findings from the previous Evaluate Phase (Step 6) — the corrective scope, not the whole spec.
- After the amendment, Medium/Large goals re-enter Step 4 with only the amended/uncovered tasks; Small Path goals re-enter Step 5 (Small Path) with the amended verified Artifact.

The verified final-spec Artifact is fixed for the entire run and reused verbatim by every Evaluate Phase; it is never reconstructed from a filename or log.

### Result and status boundary

The planner and ready producer have separate, closed success schemas. `ywc-plan` emits exactly one block with `Status`, `Scale`, and `Artifact`; `ywc-spec-ready` emits exactly one block with only `Status` and `Artifact`:

```text
## Result
Status: DONE
Scale: Small | Medium | Large        # ywc-plan only
Artifact: <repository-relative regular Markdown file>
```

Agentic never treats a human handoff, log entry, requested output, basename, or raw response as authority. A Result parser rejects unknown/duplicate/missing fields, out-of-root or escaping paths, stale candidates, and non-regular/non-Markdown files. It returns only bounded status, producer, failed field, candidate count, path digest, and reason. No raw response, transcript, tool output, generated source, full diff, or other sensitive diagnostic field may be persisted or forwarded. A producer `NEEDS_CONTEXT`, `BLOCKED`, or other parseable terminal status is propagated unchanged; absent or malformed status is `BLOCKED` and prevents downstream invocation.

For `ywc-spec-ready`, Suggestions are a preflight boundary: no `--suggestions` is needed when none are reported; `apply` permits exactly one amendment/re-validation and residual Suggestions return `NEEDS_CONTEXT: --suggestions` with only the count; `defer` records the deferral and permits a `DONE` handoff. `--non-interactive` never prompts.

### Step 4: Task Phase (FR-4)

Medium/Large goals only. Skipped on the Small Path.

1. Medium/Large task generation is allowed only after `ywc-spec-ready` returns one verified `DONE` Result. The ready Artifact is the sole final-spec authority; do not use the initial candidate, a log lookup, a basename, or raw response. Run the task-generation preflight here — **this is the first point at which `--mode` and `--lang` are validated**, because Scale is only known once `ywc-plan` has returned and the Small Path never reaches this step. `--mode` is mandatory for Medium/Large; `--lang` is required only when shared language policy cannot resolve a task/spec language. Under `--non-interactive`, a missing `--mode` (or an unresolved `--lang`) returns a bounded `NEEDS_CONTEXT` naming that exact argument, with zero `ywc-task-generator` and zero executor calls and no prompt.
2. Invoke `ywc-task-generator` against the verified ready Artifact, writing into the configured directory:
   ```text
   ywc-task-generator --spec <ready-artifact> --tasks-dir <tasks-dir> --mode <mode> --preview-only --preview-path <preview-path>
   ```
   This first call writes only the persisted preview artifact. Validate and capture the returned `preview_path`, `preview_revision`, and `preview_digest`, then append them to the UTC iteration log before making the second call:
   ```text
   ywc-task-generator --spec <ready-artifact> --tasks-dir <tasks-dir> --mode <mode> --approve-preview --preview-path <preview-path> --non-interactive
   ```
   The second call is consume-only. It must reuse the exact same `--spec`, `--tasks-dir`, output language, and approved preview identity. Missing preview, stale digest, mismatched identity, or a direct bypass of the first call stop the run with `NEEDS_CONTEXT`.
   `ywc-task-generator` resolves output language through
   [`../references/language-resolution.md`](../references/language-resolution.md).
   Pass `--lang en|ja|ko|zh|es` only when the user explicitly requested a
   task/spec language or a shared config tier resolves one for task/spec
   artifacts. Otherwise preserve the no-`--lang` behavior and let
   `ywc-task-generator` ask if needed.
3. Read `<tasks-dir>/dependency-graph.md` and select the executor:
   - `--executor` is explicit → use that executor.
   - `--executor auto` and the graph yields **multiple waves with independent tasks** → `ywc-parallel-executor`.
   - `--executor auto` and **all tasks are strictly sequential** → `ywc-sequential-executor`.
4. On a Re-plan iteration, `ywc-task-generator` numbers the new tasks past the highest existing sequence so already-completed tasks are untouched.

### Step 5: Execute Phase (FR-5)

**Record the pre-iteration baseline first.** Before invoking any executor, capture and store the current commit SHA:
```text
git rev-parse HEAD   →   <pre-iter-sha>
```
This SHA is the lower bound of the `--git-range` passed to the Evaluate Phase. Record it in the iteration's working state.

**Medium/Large path:** inspect the selected executor's authoritative checkpoint **first** — `--resume-disposition` is only meaningful once a checkpoint has actually been found, so it is validated here and never earlier. If a checkpoint exists, require `--resume-disposition resume|stop`; under `--non-interactive` a missing value returns bounded `NEEDS_CONTEXT: --resume-disposition` without prompting, without mutating checkpoint state, and without invoking the executor. `stop` returns a bounded terminal status without changing checkpoint state or invoking the executor. Resume/worktree or branch conflict, CI wait/timeout, or missing external URL policy returns `NEEDS_CONTEXT`/`BLOCKED` without prompting. The sequential external URL policy is read only from `.codex/settings.local.json` key `ywDevSequentialExecutor.externalSpecUrls`; missing or invalid values are `NEEDS_CONTEXT`.

Invoke the executor selected in Step 4 in local-merge mode, forwarding the orchestrator's own `--non-interactive` and the already-validated `--resume-disposition` when each applies:
```text
ywc-<sequential|parallel>-executor --all --tasks-dir <tasks-dir> --local-merge --pr-lang <pr-lang> [--resume-disposition <resume|stop>] [--non-interactive]
```
`--resume-disposition` is passed exactly as validated above whenever a checkpoint was found; it is omitted when no checkpoint exists. `--non-interactive` is forwarded when — and only when — the orchestrator itself received it, so a non-interactive run never degrades into a prompting executor.

`--local-merge` keeps iterations fast — no PR round-trip; completed tasks merge to the base branch directly. After the executor returns, collect each task's success/failure status from its return payload.

Forward `--pr-lang` unchanged when it is one of `en|ja|ko|zh|es`; do not normalize `zh` or `es` before the selected executor receives it. When `--pr-lang auto` or no PR language is supplied, use [`../references/language-resolution.md`](../references/language-resolution.md). If no tier resolves a language:

- **Not `--non-interactive`** → ask the user before invoking the selected executor, then forward only the resolved language code.
- **`--non-interactive`** → return bounded `NEEDS_CONTEXT: --pr-lang` and invoke no executor. Never prompt during a non-interactive run.

**Small Path:** invoke `ywc-code-gen` directly against the verified planner Artifact from Step 3. No executor, no `tasks/` directory. `ywc-code-gen` commits its output to the base branch so the Evaluate Phase can range over it.

If the executor or `ywc-code-gen` reports a merge conflict or unrecoverable CI error, stop immediately — record to `agentic-log.md` (Step 8) and report (see Edge Cases). Never auto-resolve.

### Step 6: Evaluate Phase (FR-6)

Run `ywc-impl-review` over only this iteration's changes, judged against the original verified final spec Artifact:
```text
ywc-impl-review --spec <verified-final-spec-artifact> --git-range <pre-iter-sha>..HEAD
```
- `--spec` is **always the verified final-spec Artifact**, never an unverified candidate or a re-plan's guessed/narrow path. This preserves the complete contract when iteration N is evaluated.
- `--git-range` scopes the review to commits added during this iteration (`<pre-iter-sha>` recorded in Step 5).
- Small Path: `--spec` is the verified planner Artifact from Step 3; `--git-range` is unchanged.

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
- Preview Approval: <preview_path> | <preview_revision> | <preview_digest>
- ywc-impl-review: <PASS | FAIL (<n> <CRITICAL|HIGH> issues)>
  - <SEVERITY>: <issue description>   ← one line per issue, Fail only
```

Concrete example:

```markdown
## Iteration 1 — 2026-05-15T10:30:00Z
- Phase: Full Mode / Plan → Spec → Tasks → Execute → Evaluate
- Tasks completed: 4/4
- Preview Approval: docs/ywc-plans/agentic-auth-iter1.task-preview.md | rev-003 | sha256:abcd1234
- ywc-impl-review: FAIL (2 HIGH issues)
  - HIGH: Missing input validation in POST /api/users
  - HIGH: SQL injection risk in search query
```

`Tasks completed` is the integer `<completed>/<total>` pair (for the Small Path, use `1/1` when `ywc-code-gen` succeeds, `0/1` when it fails). If the loop stopped on an exception, append the exception cause as a final line before reporting.

**Long-run compaction**: from iteration 6, or whenever 5+ iterations accumulate in context, keep only a one-line iteration digest per prior iteration in working context. Treat `<tasks-dir>/agentic-log.md` as the durable source of truth for prior details; re-read it before evaluating historical decisions instead of relying on transcript memory.

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

## Output Format

```text
## Agentic Result: <goal-slug>

### Iterations
- Iteration <n>: <Pass|Fail|Blocked> — <one-line evidence>

### Artifacts
- Spec: <path-or-skipped>
- Tasks: <tasks-dir-or-skipped>
- Review: <ywc-impl-review status-or-skipped>

### Completion Status
<DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>
```

**Completion Status rules:**

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
| `ywc-spec-ready` does not return a verified `DONE` Result | Stop before the Task Phase — propagate its bounded terminal status or return `BLOCKED`; do not proceed to `ywc-task-generator`. |
| **Already-merged task encountered** on a Re-plan | Tasks under `<tasks-dir>/completed/` (or already in the base-branch git log) are never re-executed. `ywc-task-generator` numbers new tasks past the highest existing sequence; the executor runs only the new ones. |

## Validation Checklist

Before treating an `ywc-agentic` run as complete, verify:

- [ ] A goal was received (positional or `--goal`); the run did not start without one.
- [ ] Project context was read (`AGENTS.md` / `CODEX.md` / `CLAUDE.md` / build files) before any skill invocation.
- [ ] Mode was decided explicitly (Resume vs. Full) per the Step 2 rule.
- [ ] The pre-iteration `git rev-parse HEAD` SHA was recorded **before** the executor ran, every iteration.
- [ ] Every Evaluate Phase used the **verified final-spec Artifact** for `--spec` and `<pre-iter-sha>..HEAD` for `--git-range`.
- [ ] Re-plan used `ywc-plan --update-spec` — no new spec file was created mid-run.
- [ ] The loop terminated on a Pass verdict, the iteration ceiling, or a recorded exception — never an autonomous `--max-iterations` increase.
- [ ] `<tasks-dir>/agentic-log.md` has one append-only entry per iteration in the FR-8 format.
- [ ] The Completion Report ends with exactly one Completion Status line.
- [ ] Small Path goals used `ywc-code-gen` directly and never invoked `ywc-task-generator` or an executor.
- [ ] Each argument was validated immediately before its consuming callee — no Small-scale run was blocked on `--mode`, and no callee ran with its own required input missing.
- [ ] `--non-interactive` was forwarded to downstream callees exactly when the orchestrator received it — never forced, never dropped (the `--approve-preview` consume call excepted).
- [ ] No prompt was issued during a `--non-interactive` run; unresolvable inputs returned bounded `NEEDS_CONTEXT` instead.

## Integration

- **upstream**: the user's natural-language goal (no predecessor skill).
- **downstream** (orchestrated, not chained):
  - `ywc-plan` — Plan Phase, with `--artifact-profile agentic` (Full Mode) and verified Artifact / `--failure-context` (Re-plan); `--non-interactive` only when the orchestrator received it.
  - `ywc-spec-ready` — Medium/Large final-spec authority before task decomposition.
  - `ywc-task-generator` — Task Phase, with `--tasks-dir`.
  - `ywc-sequential-executor` / `ywc-parallel-executor` — Execute Phase, in `--local-merge` mode.
  - `ywc-impl-review` — Evaluate Phase, with `--spec` (verified final Artifact) and `--git-range`.
  - `ywc-code-gen` — Small Path Execute Phase, invoked directly from the verified planner Artifact.
- **Out of scope**: external integrations (GitHub Actions, Slack), dynamic skill creation, and the new skill's own CI/E2E setup — `ywc-agentic` only orchestrates the existing `ywc-*` skill set.
