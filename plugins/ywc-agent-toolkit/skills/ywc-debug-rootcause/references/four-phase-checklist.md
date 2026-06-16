# Four-Phase Debugging Checklist

Concrete per-phase checklist to walk through during a debugging session. Each phase has an explicit **exit condition** — do not advance until satisfied.

## Phase 1: Root-Cause Investigation

### Pre-flight

- [ ] Symptom is captured verbatim (exact error message, exact failing assertion)
- [ ] Reproduction is consistent — running it 3 times produces the same failure each time
- [ ] If not reproducible, gather data (logs, traces, env dump) — do not advance until reproducible

### Investigation

- [ ] Full error / stack trace read top-to-bottom (not just the last line)
- [ ] File paths, line numbers, error codes noted
- [ ] `git log --oneline -20` reviewed for recent changes on the failing surface
- [ ] `git diff HEAD~1 -- <failing files>` examined when the issue appeared recently
- [ ] Dependency / config / env changes since last-known-good identified

### Multi-component boundary check (when applicable)

When the system has multiple layers (CI → build → sign; controller → service → repository; API → middleware → handler), instrument **every boundary** before reading source.

- [ ] For each boundary: log inputs received + outputs emitted
- [ ] Run once to gather evidence
- [ ] Identify the layer where the bad value first appears
- [ ] Investigate that layer specifically — do not read other layers' source until the boundary evidence points there

### Data-flow trace

- [ ] Bad value identified (concrete value, not "something wrong")
- [ ] One hop upstream: who called this with that value?
- [ ] Continue tracing until the *origin* is located
- [ ] Fix candidate = origin, not symptom site

### Exit condition

You can write the following sentence with no fuzziness:

> "The defect is **<one sentence what>** caused by **<one sentence why>** at `<file:line>`."

If "why" reads as "I think it's because…" — Phase 1 is not done.

## Phase 2: Pattern Analysis

### Find the reference

- [ ] At least one working sibling located in the same codebase (similar component, similar pattern)
- [ ] If no sibling exists in this codebase, record `N/A — no sibling pattern exists` and skip to Phase 3

### Read the reference

- [ ] Working reference read **end-to-end** (not skimmed, not partial)
- [ ] Pattern's dependencies enumerated (other modules, config, env vars, assumptions)

### Compare

| Difference | Matters? | Notes |
|---|---|---|
| <field A vs field B> | yes/neutral | <why this difference might matter> |
| ... | ... | ... |

- [ ] Every difference between broken and working listed, including ones marked "neutral"
- [ ] Each difference rated; pay extra attention to ones initially marked "neutral" — they are the most common hiding spot for root causes

### Exit condition

The diff list has at least one row marked "matters" with a hypothesis attached, OR every row is "neutral" and Phase 2 explicitly concludes that the broken version diverged in a way the reference does not cover (which itself becomes Phase 3's hypothesis).

## Phase 3: Hypothesis and Testing

### Form a single hypothesis

- [ ] Hypothesis written in the shape: **"X is the root cause because Y; the minimal change Z should fix it."**
- [ ] X names a specific identifier (file, function, variable), not a vague area
- [ ] Y explains the causal chain in one sentence
- [ ] Z is a single-variable change (one edit site, not "refactor module Q")

### Test minimally

- [ ] Z applied; no other edits in the same diff
- [ ] The failing test (or reproduction command) re-run fresh

### Verify

- [ ] Pass → advance to Phase 4
- [ ] Fail → **form a new hypothesis**; do NOT add another fix on top of the failed one
- [ ] After 2 failed hypotheses, stop and read more before forming a 3rd

### Exit condition

A passing test confirming the hypothesis, with exactly one variable changed from the previous state.

## Phase 4: Implementation

### Regression test first

- [ ] Simplest possible reproduction expressed as an automated test (or one-off script if no framework)
- [ ] Test added **before** the fix
- [ ] Test verified FAILING before the fix

### Single fix

- [ ] Edit addresses the root cause identified in Phase 1, not the symptom
- [ ] Exactly one edit site; no bundled "while I'm here" cleanup
- [ ] Edit matches the minimal change Z from Phase 3

### Red-green-red verification

- [ ] With fix applied → regression test PASSES (green)
- [ ] Revert fix → regression test FAILS (red)
- [ ] Restore fix → regression test PASSES (green)
- [ ] Broader test suite passes

### Completion gate

- [ ] `ywc-verify-done` block surfaced for the regression test pass
- [ ] `ywc-verify-done` block surfaced for the broader suite pass
- [ ] No `should`, `probably`, `seems` language in the completion claim

### 3+ failure escape hatch

- [ ] If three fixes on the same surface have failed, do NOT attempt fix #4
- [ ] Surface the situation to the user with: (a) summary of attempted fixes, (b) why each failed, (c) architectural concern, (d) proposed redesign
- [ ] Transfer the decision to the user — this is not a Phase 4 outcome but a Phase 4 escape

### Exit condition

Regression test passes, red-green-red cycle verified, `ywc-verify-done` block surfaced, OR — in the escape-hatch case — architectural concern surfaced and user has been asked to decide.
