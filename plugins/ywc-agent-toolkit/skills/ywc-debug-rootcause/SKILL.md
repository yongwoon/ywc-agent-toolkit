---
name: ywc-debug-rootcause
description: >-
  (ywc) Use when a bug, test/build failure, or other unexpected behavior
  appears before any fix is proposed. Forces root-cause investigation and
  blocks symptom patching. Triggers: "디버그", "버그", "debug", "デバッグ",
  "ywc-debug-rootcause". Do not use for implementation drafting (use
  ywc-code-gen), incident postmortems (use ywc-incident-postmortem), security
  triage (use ywc-security-audit), or pre-implementation confidence checks
  (use ywc-confidence-gate).
---

# ywc-debug-rootcause

**Announce at start:** "I'm using the ywc-debug-rootcause skill to identify root cause through 4-phase investigation before any fix is proposed."

This skill enforces the discipline of finding the **why** before touching the **what**. It exists because guess-and-fix loops produce three failure modes that ywc workflows must avoid: (1) symptom fixes that mask the real defect and surface elsewhere later; (2) compounding edits that make the next investigation harder; (3) "architecture wrong" cases mistaken for "fix harder" cases, wasting 3–10× the rework. Adapted from `superpowers:systematic-debugging`.

## The Iron Law

```text
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If Phase 1 has not been completed, fixes cannot be proposed. "Try X and see" is a guess, not an investigation.

## Rationalization Defense

When tempted to skip a phase, check this table first:

| Excuse | Reality |
|---|---|
| "I see the problem, let me just fix it" | Seeing a *symptom* is not understanding the *cause*. The first reproducible defect-on-line-X is almost always a downstream effect of an upstream bad value. Trace the data flow at least one hop upstream before editing. |
| "Emergency, no time for the 4 phases" | The 4 phases take 15–30 minutes for a typical bug; guess-and-check takes 2–3 hours of thrashing with a 40% first-time-fix rate. Pressure makes the systematic path **faster**, not slower. |
| "I'll try one quick fix, then investigate if it doesn't work" | The first fix sets the pattern for the session. After the first symptom-fix, every subsequent attempt becomes "fix something else", not "investigate". Do the investigation first. |
| "I've already tried 3 fixes, one more should do it" | Three failed fixes require the architecture-suspicion gate (Phase 4 §5). Stop by default; one fourth attempt requires both separate evidence-linked debug-mode analyst fields. A failed fourth attempt ends the loop. |
| "Test fails locally, I'll skip Phase 2 (pattern analysis) since I know the code" | Familiarity is the failure mode. The "I know this code" agent skips reading the *working* sibling implementation and reinvents a bug the sibling already solved. Always read a working reference end-to-end before fixing the broken one. |
| "Logging at boundaries is overkill, I'll just read the source" | Multi-component systems (CI → build → sign; API → service → DB; controller → middleware → handler) fail at boundaries, not inside components. Source-reading without boundary logging produces false hypotheses about which component is at fault. |
| "Symptom is intermittent, must be flakiness" | "Flakiness" is the label agents give to bugs they did not investigate. ≥95% of "flaky test" diagnoses turn out to be reproducible race conditions or environment leaks once instrumented. Skip the flakiness label and investigate. |
| "I'll fix this AND clean up the surrounding code while I'm here" | Bundled changes mean you cannot tell which change fixed the bug, and the cleanup may *cause* a new bug. One investigation → one fix → one verification. Refactor in a separate session. |

**Violating the letter of these rules is violating the spirit.** The 4 phases exist because each one catches a class of failure the others miss.

## When to Use

Use for **any** technical defect, including:

- Test failure (unit, integration, E2E)
- Production bug
- Build failure / compilation error
- Type-check error that resists obvious fix
- Performance regression
- Integration / cross-component failure
- Unexpected behavior in code that "used to work"

Use this **especially** when:

- Under time pressure (the temptation to guess peaks here)
- A previous fix attempt did not work
- The symptom is intermittent or environment-dependent
- "Just one quick fix" feels obvious

Do **not** skip when:

- The bug looks "simple" — simple bugs have causes too
- The user is impatient — systematic is still faster than thrashing
- You are tired — exhaustion is not a justification

## Analyst contract

Every analyst packet carries `Caller: ywc-debug-rootcause` and `analysis_mode=debug_hypotheses` plus bounded evidence. Missing, unknown, or mismatched caller/mode returns `NEEDS_CONTEXT` without inferring another mode. Validate the returned Status/Summary/Finding counts envelope and matching Analysis mode before consuming advice; owner/input/output/status mismatch returns `NEEDS_CONTEXT`. An analyst refusal consumes the existing dispatch budget; preserve the caller's original gate and surface the missing evidence instead of re-dispatching or falling through. The analyst returns inline advice and never writes the caller's report or runs probes. Unavailable delegation uses the documented inline path; unavailable live runtime evidence is `UNVERIFIED — instruction contract only`.

## The Four Phases

Complete each phase before proceeding to the next.

### Phase 1: Root-Cause Investigation

Before proposing **any** fix:

0. **Establish the smallest feedback loop first.** Use a focused test, build check, script or bounded manual reproduction. Record `Feedback loop`, `Catches`, `Misses`, and the observed failure before any fix. If automated reproduction is unavailable, record manual evidence and constraints; do not fabricate RED or claim execution PASS. Read-only analyst advice is not a reproduced failure.
1. **Read error messages carefully.** Read the full stack trace, every line. Note file paths, line numbers, error codes. Errors often contain the exact name of the missing thing.
2. **Reproduce consistently.** Run the minimal feedback loop until its result is predictable. If reproduction is unavailable, retain the manual evidence and constraints from step 0, gather the missing data and do not propose a speculative fix.
3. **Check recent changes.** Run `git log --oneline -20`, `git diff HEAD~1`, check dependency bumps, environment changes, config changes since the last known-good state.
4. **Add diagnostic instrumentation at component boundaries.** For multi-component systems, the failure is almost always at a boundary, not inside a component. Log what each component receives and what it emits. Run once to gather evidence. **Read the evidence before forming a hypothesis.**
5. **Trace data flow upstream.** Where does the bad value originate? What called the failing function with that value? Keep tracing until the *origin* is found; fix at the origin, not at the symptom.

Phase 1 exit condition: you can answer in one sentence **what** is wrong and **why** it is happening. If either answer is fuzzy, continue Phase 1.

When local evidence cannot produce a confident initial hypothesis and the current Codex session has an available subagent/delegation tool, request at most one independent `ywc-root-cause-analyst` pass. Send `Caller: ywc-debug-rootcause`, `analysis_mode=debug_hypotheses`, and only a bounded packet: failure symptom, timeline, stack trace or logs, recent diff, rejected hypotheses, relevant code snippet, and current candidate cause. Ask for `Status: <DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT>` plus 3–5 ranked, falsifiable hypotheses with evidence-for / evidence-against and confidence per item. Validate the analyst contract before consuming advice. If no delegation tool is available, rank the same 3–5 falsifiable candidates inline; do not attempt tool-specific named-agent syntax from another runtime.

### Phase 2: Pattern Analysis

Find the pattern before fixing.

1. **Find a working example in the same codebase.** What similar code works? Read it end-to-end (not just the location, not just nearby patterns).
2. **Compare against the reference.** List every difference between the broken and the working version — including ones you think "cannot matter". Most root causes hide in the "cannot matter" set.
3. **Understand dependencies.** What other components, settings, env vars, and assumptions does the working pattern rely on? Verify the broken version satisfies each.

Phase 2 exit condition: a concrete diff between the broken and working version, with each row marked "matters" / "neutral".

### Phase 3: Hypothesis and Testing

Apply the scientific method.

1. **Rank 3–5 falsifiable candidate hypotheses** after reproduction and pattern analysis, each with evidence for and against. If evidence cannot support the candidates, return `NEEDS_CONTEXT` with the highest-information probe rather than padding the list. Show the ranking before testing; non-interactive execution selects the highest-ranked candidate without waiting.
2. **Test one hypothesis at a time.** State "X is the root cause because Y; minimal change Z should fix it." Change one variable per experiment. Do not layer a new fix on a failed one.
3. **Update the ranking from evidence.** Pass → Phase 4; fail → reject or refine the hypothesis and record the result. After two rejected hypotheses, re-investigate before testing a third. A reverted falsification experiment is not a failed fix; count an attempted fix when it fails to resolve the confirmed reproduction or introduces a regression.
4. **Stop after three failed fixes on the same surface.** The architecture-suspicion gate may request one independent analyst pass, when delegation is available, using `Caller: ywc-debug-rootcause`, `analysis_mode=debug_hypotheses`, the bounded packet, ranked hypotheses and failed-fix log. Require `Fix #4 signal: fix harder` and `Next fix worth attempting: <one concrete minimal change>`. Allow exactly one final fourth fix only when both fields are present, separate, evidence-linked, and returned for the valid debug pair. One missing or unlinked field, a different mode, malformed output or unavailable analyst keeps the stop in force. After a failed fourth fix, stop; do not reset the counter or attempt a fifth fix. Route architectural concerns to `ywc-architect`; the analyst recommends review and never makes the final architecture decision.

Phase 3 exit condition: a passing test that confirms the hypothesis, with one and only one variable changed.

### Phase 4: Implementation

Fix the root cause, not the symptom.

1. **Create a failing test that captures the bug.** Simplest possible reproduction. The test must fail before the fix and pass after. This is the regression guard.
2. **Implement a single fix.** Address the root cause only. No "while I'm here" cleanup, no preemptive refactoring of adjacent code.
3. **Verify the fix.** Run the regression test plus the broader suite. Use `ywc-verify-done` to gate the completion claim.
4. **Verify the regression test.** Revert the fix → test must FAIL. Restore the fix → test must PASS. (Red-green-red cycle. Without this, the test may be passing for reasons unrelated to the fix.)
5. **If 3+ fixes failed on the same surface, STOP and question architecture.**

   Signals of architectural problem:
   - Each fix moves the defect to a new location.
   - Each fix requires "massive refactoring" to implement cleanly.
   - The pattern itself does not match the requirement.

   Without both validated debug-mode analyst fields from Phase 3 step 4, **do not attempt fix #4**. Surface the situation to the user with: (a) the three attempted fixes and why each failed, (b) the architectural concern, (c) a proposed redesign or pattern change. The exception permits one minimal attempt only, followed by the original verification gate. See [references/architectural-stop-signals.md](references/architectural-stop-signals.md) for the surface format.

Phase 4 exit condition: regression test passes + red-green-red cycle verified + `ywc-verify-done` block surfaced.

## Red Flags — STOP and return to Phase 1

If you catch yourself doing any of these, stop and restart from Phase 1.

| Red flag | Why it means stop |
|---|---|
| "Quick fix for now, investigate later" | "Later" never comes; the symptom-fix becomes the de facto code. |
| "Let me try changing X and see if it works" | Trying is not testing. Form a hypothesis first. |
| "Multiple changes at once — faster" | Bundled changes cannot be isolated. If the suite passes, you do not know *which* change fixed it. |
| "Skip the test, I'll verify manually" | Manual verification does not protect against regression. |
| "Probably X, let me fix that" | "Probably" is forbidden by `ywc-verify-done`. State the hypothesis precisely or do not state it. |
| "Pattern says X but I'll adapt differently" | Partial understanding of a pattern guarantees a bug. Read it completely before adapting. |
| "Here are the main problems: [list of fixes]" | Listing fixes without investigation = guessing in bulk. |
| "One more fix attempt" (after 2+) | Three failed fixes require the architecture gate; only both validated debug-mode fields permit one final attempt. |
| Each fix surfaces a new defect elsewhere | The pattern is wrong, not the latest line. |

## Output Format

Surface the investigation in this shape, in order:

````markdown
### Investigation summary

- **Symptom:** <one-line observed behavior>
- **Reproduction:** <exact command(s), or manual evidence and constraints>
- **Feedback loop / Catches / Misses:** <minimal observation and limits>
- **Ranked candidates:** <3–5 falsifiable hypotheses, evidence for/against>
- **Root cause (Phase 1):** <one-sentence why, with file:line citation>
- **Working reference (Phase 2):** <path:line of a working sibling, if applicable; "N/A — no sibling pattern exists" otherwise>
- **Hypothesis (Phase 3):** "<X is the root cause because Y. Minimal change Z should fix it.>"
- **Fix attempted:** <commit hash or file:line of the change>
- **Regression test:** <test path:name>

### Verification

(verification block per `ywc-verify-done`, including red-green-red proof for the regression test)
````

When the investigation reveals an architectural concern (Phase 4 §5), the output instead surfaces a `### Architectural concern` block and the conversation transfers to the user for design discussion — no Phase 4 §1–4 occurs in that path.

## Integration

- **Upstream callers:** `ywc-verify-done` (when verification fails ≥2 times on the same surface), `ywc-impl-review` (when a Critical finding points to a defect with unclear root cause), `ywc-incident-postmortem` (live debugging that escalates into a postmortem still uses these 4 phases).
- **Downstream:** `ywc-verify-done` (Phase 4 §3 — gate the fix's completion claim), `ywc-plan` (when architectural redesign is required after Phase 4 §5).
- **Pairs with:** `ywc-impl-review` (when investigation reveals a class of defects, not a single one), `ywc-incident-postmortem` (post-resolution write-up).

## Validation Checklist

Before concluding the investigation, verify:

- [ ] Phase 1 produced a one-sentence root-cause statement with `file:line` citation
- [ ] Minimal feedback loop, observed failure and catches/misses recorded; manual evidence and constraints named when automation is unavailable
- [ ] Phase 2 found at least one working reference, OR explicitly recorded `N/A — no sibling pattern exists`
- [ ] Hypothesis (Phase 3) is in the shape "X is the root cause because Y; minimal change Z fixes it"
- [ ] The fix changed exactly one variable; no bundled cleanup
- [ ] A regression test was added before the fix and verified red-green-red
- [ ] `ywc-verify-done` block was surfaced for the final passing test
- [ ] After three failed fixes, stop unless both validated debug-mode fields permit one fourth fix; stop after a failed fourth fix

## Common Mistakes

- **Reading the source without first instrumenting boundaries** in multi-component systems. Source-reading produces hypotheses about which component is at fault; only boundary logs produce *evidence* of which component is at fault.
- **Treating "no root cause found" as a conclusion.** ≥95% of such conclusions are incomplete investigations. If after 30 minutes the root cause is still elusive, the investigation strategy is wrong (wrong tools, wrong layer, wrong reproduction). Change strategy; do not declare "environmental flake" and move on.
- **Reverting the fix without re-verifying the regression test** (skipping the red-green-red cycle). Without the revert step, the test may have been passing for a reason unrelated to the fix.
- **Allowing the fix to bundle adjacent improvements.** "While I'm here" turns the single-variable change into an N-variable change and destroys the bisection signal if the bug returns.

## References

| Reference | Use when |
|---|---|
| [references/four-phase-checklist.md](references/four-phase-checklist.md) | Walking through the 4 phases with concrete checklists per phase |
| [references/architectural-stop-signals.md](references/architectural-stop-signals.md) | Deciding whether the situation is "next fix is right" vs "architecture is wrong" |
| [../references/non-stop-execution.md](../references/non-stop-execution.md) | Routing the investigation result back into the executor loop without halting the workflow unnecessarily |
