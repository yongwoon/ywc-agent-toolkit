---
name: ywc-spec-ready
description: >-
  (ywc) Use when a spec produced by ywc-plan still has Critical/Warning findings
  and you want it driven to ywc-spec-validate DONE automatically — recursively
  looping ywc-plan --update-spec and ywc-spec-validate until the spec is ready for
  ywc-task-generator, then stopping at the handoff. Triggers: "spec 수렴", "spec
  ready loop", "ywc-spec-ready", "plan validate 반복", "사양 수렴 자동화",
  "spec を DONE まで". Do not use for the full goal-to-code pipeline (use
  ywc-agentic), for a one-shot spec review without re-planning (use
  ywc-spec-validate), for initial spec authoring from a goal (use ywc-plan), or
  for decomposing an already-DONE spec into tasks (use ywc-task-generator).
---

# ywc-spec-ready (Spec Readiness Loop)

**Announce at start:** "I'm using the ywc-spec-ready skill to drive the spec to ywc-spec-validate DONE by looping ywc-plan and ywc-spec-validate, then stop at the ywc-task-generator handoff."

This skill takes a spec file that `ywc-plan` already produced and recursively converges it to a task-ready state. Each iteration runs `ywc-spec-validate`; on `DONE_WITH_CONCERNS` it calls `ywc-plan --update-spec` with a fix-priority summary and re-validates. The loop ends on `DONE` (handoff printed, **stop** — never auto-invoke `ywc-task-generator`), on the iteration cap, or on a convergence-stall guard.

```text
spec ──> [ywc-spec-validate ──DONE_WITH_CONCERNS──> ywc-plan --update-spec]* ──DONE──> handoff
```

It is **not** the full pipeline: `ywc-agentic` orchestrates goal→code with an impl-review loop and runs `ywc-spec-validate` only once. This skill fills the missing inner loop — multi-iteration spec convergence — that neither `ywc-agentic` Step 3 nor `ywc-spec-validate`'s single-retry Programmatic Consumer Policy provides.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "spec-validate returned DONE_WITH_CONCERNS but the findings look trivial — just go to task-generator" | Only `DONE` ends the loop with a handoff. `DONE_WITH_CONCERNS` always triggers a re-plan iteration (or a guard stop). There is no "trivial" exception — task-generator consumes DONE specs only. |
| "The loop is not converging — bump `--max-iterations`" | `--max-iterations` is a user-defined safety valve, never raised autonomously. At the cap, emit the partial report and stop. Surfacing non-convergence is the correct outcome. |
| "DONE reached — chain straight into `ywc-task-generator` to finish the job" | **Never invoke `ywc-task-generator`.** This skill is a converger, not an executor. It prints the handoff and stops; the user decides when to decompose. |
| "User gave a goal, not a spec — I'll run ywc-plan from scratch first" | This skill takes `--spec <path>` only (an existing spec). Goal→spec is `ywc-plan`'s job; goal→code is `ywc-agentic`'s. If `--spec` is absent, return `NEEDS_CONTEXT`. |
| "Critical count went up after a re-plan — stop immediately, it's diverging" | A re-plan amendment may legitimately open new surface (one transient increase). Stop only after **two consecutive** non-decreasing iterations, or an identical finding signature / amendment scope (see references/convergence.md). |
| "advisor budget is annoying — let spec-validate escalate freely every iteration" | Track `--max-advisor-calls` across iterations and pass only the remaining budget. Unbounded per-iteration escalation is the cost blow-up this skill exists to prevent. |
| "spec-validate returned SOCRATIC — re-plan from its questions" | `SOCRATIC` is not a gate verdict. Detect it and stop as misuse (`stop-misuse`); never feed it into the convergence loop. |

**Violating the letter of these rules is violating the spirit.** The loop is trustworthy only because its termination conditions (DONE, cap, stall) and its no-auto-decompose boundary are non-negotiable.

## Arguments

| Parameter | Format | Default | Description |
|---|---|---|---|
| `--spec` | `--spec <path>` | _(required)_ | Existing spec file (produced by `ywc-plan`) to converge. Absent/missing → `NEEDS_CONTEXT`. |
| `--max-iterations` | `--max-iterations <n>` | `5` | Validation loop ceiling. User-defined safety valve — never raised autonomously. `<= 0` → `NEEDS_CONTEXT`. |
| `--max-advisor-calls` | `--max-advisor-calls <n>` | `4` | Total Opus advisor budget across **all** iterations (cost guard). |
| `--log` | `--log <path>` | `<spec-dir>/<slug>.spec-ready-log.md` | Append-only loop log. `<slug>` = `--spec` filename stem. |
| `--dry-run` | flag | — | Print the planned command sequence only; invoke no sibling skill, write no amendment or log. |
| `--lang` | `--lang <lang>` | `auto` | Report/handoff language; inferred from `CLAUDE.md` when `auto`. |
| `--focus` | `--focus <area>` | — | Forwarded to `ywc-spec-validate` when set. |
| `--format` | `--format <markdown\|html>` | `markdown` | Forwarded to `ywc-spec-validate` when set. |
| `--terse` | flag | — | Minimal output — phase headers and the final report only. |

> **Cost-guard note**: `--max-advisor-calls` is the cumulative Opus budget across all iterations. This skill tracks spend from each `ywc-spec-validate` report header (`Phase 2 advisor calls used: X of N`) and injects the remaining budget into the next iteration via `ywc-spec-validate --advisor-budget <min(2, global_remaining)>`. When the budget reaches 0 the loop continues with escalation off (`--advisor-budget 0`) and only stops if a mandatory ambiguous Critical remains.

## Workflow

### Step 1: Pre-flight

- If `--spec` is absent, or the file does not exist, stop with `NEEDS_CONTEXT` (report the missing path). Do not create a spec.
- If `--max-iterations <= 0`, stop with `NEEDS_CONTEXT`.
- Derive `<slug>` = `--spec` filename stem (drop directory and `.md`, lowercase-hyphenate). Resolve the log path (`--log` wins when given).
- If `--dry-run`, print the planned sequence (`ywc-spec-validate --spec <path>` → conditional `ywc-plan --update-spec <path> --failure-context "…"`, up to `--max-iterations`) and stop. Write nothing.

### Step 2: Iteration Loop

Initialize `iteration = 1`, `global_remaining = --max-advisor-calls`, and an empty signature history. Repeat:

1. **Validate** — bind `iter_cap = min(2, global_remaining)` (the per-iteration advisor ceiling), then run `ywc-spec-validate --spec <path> --advisor-budget <iter_cap>` (forward `--focus` / `--format` when set). Parse the report: Critical/Warning/Suggestion counts, finding signatures, and the advisor-usage line (`Phase 2 advisor calls used: X of N`); subtract `X` from `global_remaining` (subtract the full `iter_cap` when the line is unparseable). When `global_remaining == 0`, pass `--advisor-budget 0` (escalation off); if a mandatory ambiguous Critical then remains, stop with `DONE_WITH_CONCERNS` / `stop-advisor-exhausted`.
2. **Route** on Completion Status (see Status Routing). `DONE` → Step 4. `BLOCKED`/`NEEDS_CONTEXT`/`SOCRATIC`/unparseable → Step 3 (hard stop). `DONE_WITH_CONCERNS` → continue.
3. **Guard** (see [references/convergence.md](references/convergence.md)) — compute Critical-count trend, finding-signature recurrence, and amendment-scope identity against the previous iteration. If any stall guard fires, stop with `DONE_WITH_CONCERNS` and the matching `action` (`stop-non-converging`). If `iteration >= --max-iterations`, stop with `DONE_WITH_CONCERNS` / `stop-cap`.
4. **Re-plan** — build a fix-priority summary (Critical first; Warnings only when they block DONE or signal cross-section drift) and run `ywc-plan --update-spec <path> --failure-context "<summary>"`. If this call itself fails (file vanished, non-zero, error), stop with `BLOCKED` / `stop-replan-failed`.
5. **Log + advance** — append the iteration entry to the log (see [references/loop-log.md](references/loop-log.md)), record signatures, `iteration += 1`, loop.

### Step 3: Hard Stop

`BLOCKED` / `NEEDS_CONTEXT` from `ywc-spec-validate`, an unparseable report, or `SOCRATIC` (misuse) end the loop immediately without a re-plan. Log the iteration (`stop-blocked` / `stop-context` / `stop-misuse`), surface the reason, and emit the Completion Report.

### Step 4: Handoff (DONE)

On `DONE`, print the handoff message **verbatim** and stop. Do not invoke `ywc-task-generator`.

```text
✅ Spec ready: <path> (DONE after N/<cap> iterations, <X> advisor calls)
Next:
  1. /ywc-task-generator <path>
  2. (after tasks generated) /ywc-sequential-executor or /ywc-parallel-executor
```

### Step 5: Completion Report

Emit one report: spec path, iterations run / cap, final Completion Status, remaining Critical count (if any), cumulative advisor calls used, log path, and (on DONE) the handoff. The final line is one Completion Status — nothing follows it.

## Status Routing (ywc-spec-validate response)

| spec-validate Status | ywc-spec-ready action |
|---|---|
| `DONE` | End loop → print handoff → stop (Step 4) |
| `DONE_WITH_CONCERNS` | Guards pass → fix-priority summary → `ywc-plan --update-spec` → next iteration; guard fires → stop (Step 2.3) |
| `BLOCKED` | Stop immediately, report blocker (Step 3) |
| `NEEDS_CONTEXT` | Stop immediately, report missing context (Step 3) |
| `SOCRATIC` | Misuse — stop, report (`stop-misuse`) |
| status absent / unparseable | Implicit `BLOCKED`, surface raw excerpt |

## Completion Status

| Status | When |
|---|---|
| `DONE` | Loop converged to `ywc-spec-validate` = DONE |
| `DONE_WITH_CONCERNS` | Cap reached / convergence stall / advisor budget exhausted, Critical remaining |
| `BLOCKED` | spec-validate BLOCKED, unparseable report, or `ywc-plan --update-spec` failure |
| `NEEDS_CONTEXT` | `--spec` missing/absent, bad argument, or spec-validate NEEDS_CONTEXT |

## Validation Checklist

Before treating a run as complete, verify:

- [ ] A `--spec` path was provided and the file existed (else `NEEDS_CONTEXT`).
- [ ] Each iteration ran `ywc-spec-validate` exactly once and routed strictly on its Completion Status.
- [ ] Every `DONE_WITH_CONCERNS` (that passed guards) produced exactly one `ywc-plan --update-spec` call.
- [ ] The loop terminated on `DONE`, the iteration cap, a stall guard, or a hard stop — never an autonomous `--max-iterations` increase.
- [ ] `ywc-task-generator` was **not** invoked — the run ended at the handoff.
- [ ] Each iteration appended one entry to the loop log (unless `--dry-run`).
- [ ] The Completion Report ends with exactly one Completion Status line.

## Common Mistakes

- **Auto-decomposing on DONE** — printing the handoff and then calling `ywc-task-generator` anyway. The handoff IS the stop; the user owns the decompose decision.
- **Stopping on the first Critical increase** — a single transient rise after a re-plan is allowed; only a two-consecutive non-decrease (or repeated signature / identical scope) is a stall.
- **Treating SOCRATIC as a verdict** — it is a learning-question mode, not a gate result; detect and stop as misuse.
- **Rewriting the spec from scratch on re-plan** — always `ywc-plan --update-spec` (append amendments); never regenerate, which loses validated sections.

## Integration

- **Upstream**: `ywc-plan` (produces the initial spec this skill converges).
- **Consumes**: `ywc-spec-validate` (per-iteration gate), `ywc-plan --update-spec` (per-iteration amendment).
- **Downstream (handoff only, not invoked)**: `ywc-task-generator`, then `ywc-sequential-executor` / `ywc-parallel-executor`.
- **Delegated from**: `ywc-agentic` Step 3 (Medium/Large) replaces its single `ywc-spec-validate` call with a delegation to this skill — the two skills' `--max-iterations` are independent ceilings (outer impl-review loop vs inner spec-convergence loop). Wiring lands in the integration task.
