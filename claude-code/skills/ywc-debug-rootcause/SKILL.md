---
name: ywc-debug-rootcause
description: >-
  (ywc) Use when encountering a bug, test failure, build failure, or any
  unexpected behavior, before proposing or applying any fix. Forces root-cause
  identification through a 4-phase investigation, blocks symptom patching, and
  questions architecture after 3+ failed fixes on the same surface. Triggers:
  "왜 안돼", "안 돼요", "디버그", "디버깅", "버그", "고장", "이상해",
  "원인 찾아줘", "debug", "debug this", "find the bug", "root cause",
  "what's wrong", "デバッグ", "原因不明", "通らない", "落ちる", "おかしい",
  "ywc-debug-rootcause". Do not use for ongoing implementation drafting
  (use ywc-code-gen), incident postmortem after the fact (use
  ywc-incident-postmortem), security vulnerability triage (use
  ywc-security-audit), or pre-implementation confidence check (use
  ywc-confidence-gate).
category: discipline
phase: investigation
requires: []
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
| "I've already tried 3 fixes, one more should do it" | 3+ failed fixes on the same surface is a signal that the **architecture is wrong**, not that the next fix is right. Stop and question the pattern (Phase 4 §5). A 4th fix on bad architecture creates a 5th bug; the loop only terminates at a refactor or a redesign. |
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

## The Four Phases

Complete each phase before proceeding to the next.

### Phase 1: Root-Cause Investigation

Before proposing **any** fix:

1. **Read error messages carefully.** Read the full stack trace, every line. Note file paths, line numbers, error codes. Errors often contain the exact name of the missing thing.
2. **Reproduce consistently.** Run the failing case until you can predict the outcome before pressing enter. If you cannot reproduce, gather more data — never propose a fix for a non-reproducible bug.
3. **Check recent changes.** Run `git log --oneline -20`, `git diff HEAD~1`, check dependency bumps, environment changes, config changes since the last known-good state.
4. **Add diagnostic instrumentation at component boundaries.** For multi-component systems, the failure is almost always at a boundary, not inside a component. Log what each component receives and what it emits. Run once to gather evidence. **Read the evidence before forming a hypothesis.**
5. **Trace data flow upstream.** Where does the bad value originate? What called the failing function with that value? Keep tracing until the *origin* is found; fix at the origin, not at the symptom.

Phase 1 exit condition: you can answer in one sentence **what** is wrong and **why** it is happening. If either answer is fuzzy, continue Phase 1.

When local evidence cannot produce a confident initial hypothesis and the Claude Code runtime is in use with the named-agent catalog at `claude-code/agents/` installed, dispatch `Task(subagent_type: ywc-root-cause-analyst)` with the bounded packet (failure symptom + stack trace + recent diff + relevant code snippet) so an Opus-tier analyst returns a ranked top-3 hypothesis list with evidence-for / evidence-against per item (`claude-code/agents/ywc-root-cause-analyst.md`). The dispatch is conditional and at most one per Phase 1; runtimes without named-agent dispatch use the inline procedure above.

### Phase 2: Pattern Analysis

Find the pattern before fixing.

1. **Find a working example in the same codebase.** What similar code works? Read it end-to-end (not just the location, not just nearby patterns).
2. **Compare against the reference.** List every difference between the broken and the working version — including ones you think "cannot matter". Most root causes hide in the "cannot matter" set.
3. **Understand dependencies.** What other components, settings, env vars, and assumptions does the working pattern rely on? Verify the broken version satisfies each.

Phase 2 exit condition: a concrete diff between the broken and working version, with each row marked "matters" / "neutral".

### Phase 3: Hypothesis and Testing

Apply the scientific method.

1. **Form a single hypothesis.** Write it down in the shape: "X is the root cause because Y; if I change Z minimally, the test should pass." Vague hypotheses do not survive Step 2.
2. **Test the smallest possible change.** Change one variable. Do not bundle "while I'm here" edits.
3. **Verify the result.**
   - Pass → proceed to Phase 4.
   - Fail → form a **new** hypothesis. Do **not** layer another fix on top of the failed one.
4. **Stop and admit when stuck.** If you have run two hypotheses and both failed, the model of the system is wrong. Read more before forming a third hypothesis. After 3+ failed fixes on the same surface, fire the **architecture-suspicion gate**: when the Claude Code runtime is in use and the named-agent catalog at `claude-code/agents/` is installed, dispatch `Task(subagent_type: ywc-root-cause-analyst)` with the bounded packet plus the failed-fix log. The analyst returns either "architecture is wrong — dispatch ywc-architect with [framed decision]" or "fix harder — next surgical attempt is [specific change]" — never an ambiguous verdict. Runtimes without named-agent dispatch read this gate as "stop and surface to the user instead of attempting a 4th fix".

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

   At this point, **do not attempt fix #4**. Surface the situation to the user with: (a) the three attempted fixes and why each failed, (b) the architectural concern, (c) a proposed redesign or pattern change. Continuing to fix is not perseverance — it is sunk-cost thrashing. See [references/architectural-stop-signals.md](references/architectural-stop-signals.md) for the surface format.

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
| "One more fix attempt" (after 2+) | 3+ attempts = architectural problem. Stop and discuss, do not fix again. |
| Each fix surfaces a new defect elsewhere | The pattern is wrong, not the latest line. |

## Output Format

Surface the investigation in this shape, in order:

````markdown
### Investigation summary

- **Symptom:** <one-line observed behavior>
- **Reproduction:** <exact command(s)>
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
- [ ] Reproduction command is concrete and deterministic (not "sometimes it fails")
- [ ] Phase 2 found at least one working reference, OR explicitly recorded `N/A — no sibling pattern exists`
- [ ] Hypothesis (Phase 3) is in the shape "X is the root cause because Y; minimal change Z fixes it"
- [ ] The fix changed exactly one variable; no bundled cleanup
- [ ] A regression test was added before the fix and verified red-green-red
- [ ] `ywc-verify-done` block was surfaced for the final passing test
- [ ] If 3+ fixes failed on the same surface, the investigation halted and surfaced an architectural concern instead of attempting a 4th fix

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
