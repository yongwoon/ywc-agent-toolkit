# Shared Engineering Principles for ywc-* Skills

> Shared reference document. Linked from any `ywc-*` skill that needs to ground a decision in a cross-skill principle rather than restate the principle in its own SKILL.md.

## 1. Purpose

This document captures the engineering principles that recur across multiple `ywc-*` skills. Centralizing them here serves three goals:

- **Reduce duplication** — a principle stated once is updated once.
- **Make principle violations easier to flag** — review skills can cite this file by section instead of restating the rule.
- **Preserve cross-skill consistency** — every skill makes the same trade-off the same way when the same principle applies.

This file complements the existing `advisor-pattern.md` (when to escalate) and `confidence-gate.md` (whether to escalate). Together the three documents form the shared reasoning layer for the `ywc-*` collection.

## 2. Principle Hierarchy

When two principles conflict, resolve in this order. Lower-numbered principles override higher-numbered ones.

1. **Safety** — Do not introduce security risk, data loss risk, or production breakage.
2. **Evidence** — Claims must be verifiable from primary sources (code, official docs, test output).
3. **Scope** — Build only what was asked. Defer adjacent improvements.
4. **Reuse** — Prefer existing utilities, libraries, and patterns over new code.
5. **Clarity** — Prefer the simplest expression that preserves correctness. The operational rubric for what "readable" means — naming, function/control-flow, comments, complexity thresholds, and the anti-dogma guardrails that bound them — lives in [readable-code.md](./readable-code.md).
6. **Efficiency** — Optimize tokens, time, and tool calls only after the above are satisfied.

A skill that proceeds in violation of a higher principle to honor a lower one is misordering the hierarchy. For example: "I skipped reading the existing util because it would have used more tokens" inverts §6 over §4 and is incorrect.

## 3. Evidence Discipline

Every claim a skill makes in its output must fall into one of three categories. The category must be implicit from the way the claim is phrased.

| Category | Source | Phrasing pattern |
|----------|--------|------------------|
| **Verified** | Read directly from code, doc, or test output during this run | "The function at `src/x.ts:42` returns ..." |
| **Inferred** | Derived from verified facts plus a stated assumption | "Assuming the caller still uses the old signature, ..." |
| **Recalled** | Pulled from training data or prior session memory | "Typically, libraries of this kind ..." |

A claim presented as Verified that is actually Inferred or Recalled is a defect. Review skills (`ywc-impl-review`, `ywc-spec-validate`) treat this as a High-severity finding.

When the cost of verification is high, prefer to mark a claim Inferred or Recalled rather than skip it. Honest uncertainty beats false confidence.

## 4. Reuse Discipline

Before writing new code, a skill must check three sources in order:

1. **Project utilities** — `src/utils/`, `lib/`, or the local equivalent.
2. **Project dependencies** — already-installed packages in `package.json`, `requirements.txt`, `go.mod`, etc.
3. **Standard library** — language runtime built-ins.

Only after all three are checked may a skill recommend a new dependency or write a new utility. The check must be reported in the completion summary as a one-line note ("Searched utils/, no match; using lodash.debounce already in deps").

This rule applies to `ywc-code-gen`, `ywc-tech-research`, and any skill that produces source code as output. It does not apply to `ywc-impl-review`, `ywc-security-audit`, or other read-only skills.

## 5. Scope Discipline

When a skill discovers an adjacent improvement opportunity that is outside the requested scope, it must:

1. **Not implement it** — even if the change is small.
2. **Note it in the completion summary** — under a "Discovered, deferred" section.
3. **Suggest the appropriate next skill** — usually `ywc-spec-validate` or `ywc-task-generator` to scope it properly.

This applies even when the adjacent improvement looks "obviously correct". The cost of an unrequested change exceeds the cost of a deferred note, because the reviewer must now evaluate two changes instead of one.

Exception: if the adjacent change is required for the requested change to succeed (e.g., a missing import the requested code depends on), implement it and call it out explicitly.

## 6. Failure Discipline

When a skill encounters an unexpected failure (test failure, build error, tool error), it must:

1. **Investigate before working around.** The first response is to read the error and form a hypothesis about cause.
2. **Not disable the failing check.** Skipping a test, suppressing a lint rule, or removing a guard is not a fix.
3. **Report root cause, not symptom.** "The test failed because the database fixture was reset between cases" is a finding. "I made the test pass" is not.

If root cause cannot be identified within a reasonable budget, the skill must STOP (per [confidence-gate.md](./confidence-gate.md)) and report what it learned, not paper over the failure.

## 7. Output Discipline

Skill output is read by a person who did not run the skill. It must therefore:

- **State the outcome first.** Lead with DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT.
- **Then state evidence.** What was checked, what was found.
- **Then state next steps.** What the reader should do with this output.
- **Avoid restating the request.** The reader knows what they asked for.
- **Avoid marketing language.** No "successfully", "comprehensive", "robust" — these add length without information.

Output formatting conventions live in [symbols.md](./symbols.md). This section governs only structure and tone.

## 8. Trust Boundaries

Skills run inside the user's session and trust boundary. They have access to local files, project secrets, and shell execution. Therefore:

- **Treat all skill outputs as user-visible.** Do not embed credentials, tokens, or PII in reports.
- **Treat external data as untrusted.** API responses, web fetches, and third-party tool output require validation before use as a basis for action.
- **Treat user instructions as authoritative within their scope.** A user instruction overrides a default principle. A user instruction does not override a Safety (§2.1) constraint.

The Advisor Pattern's "bounded snippet" rule (see [advisor-pattern.md](./advisor-pattern.md) §3) is a focus mechanism, not a redaction mechanism. Redaction, when needed, must happen at the boundary where data first enters the skill — not at handoff to an advisor.

## 9. Cross-Skill Consistency

When two skills produce overlapping outputs (e.g., both `ywc-impl-review` and `ywc-security-audit` flag the same SQL injection), the rules are:

- **Each skill reports its own finding independently.** No skill suppresses a finding because another skill might also report it.
- **Severity vocabulary is shared** ([symbols.md](./symbols.md) §3). Two skills must not assign different severity tiers to the same defect.
- **The downstream merger (typically `ywc-create-pr` or a human) deduplicates.** Skills do not coordinate at runtime.

This keeps individual skills simple and audit-friendly at the cost of some duplication in the merged report. The trade-off favors auditability.

## 10. Scope and Limits

This document covers principles that apply to **two or more** `ywc-*` skills. Principles specific to a single skill belong in that skill's SKILL.md, not here.

When proposing an addition to this file, the test is: does this principle govern decisions in at least two skills, or is it specific to one workflow? If specific, it stays in the SKILL.md.
