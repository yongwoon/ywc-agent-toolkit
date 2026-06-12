# Severity Rubric

Use this rubric in Phase 5 of `ywc-ui-ux-review`. Every finding gets exactly one tier. Tiers are mutually exclusive.

## Decision Order

Evaluate in this order; stop at the first match:

1. Does it block usage OR violate WCAG 2.2 AA? → **Critical**
2. Does it cause major usability degradation OR block a primary task? → **High**
3. Does it cause friction without blocking? → **Medium**
4. Is it polish that does not affect comprehension or completion? → **Low**

## 🔴 Critical

A finding is Critical when **any** of:

- The user is blocked from completing a primary task
- WCAG 2.2 AA violation (contrast, keyboard, focus, target size, alt text on functional images)
- Data loss or destructive action without undo / confirmation
- Security or privacy implication visible in the UI (password in plaintext, PII overexposed)
- Catastrophic IA failure (a primary destination has no path)

**Examples**:

- Body text contrast 3.2:1 against background (fails WCAG SC 1.4.3)
- Submit button reachable only by mouse (fails WCAG SC 2.1.1)
- Modal can be opened but not closed via keyboard
- "Delete account" with no confirmation step

## 🟠 High

A finding is High when **any** of:

- A primary user task is significantly slower or error-prone, but not blocked
- Inconsistency that breaks the user's mental model on a critical path
- Visual hierarchy that misleads about which action is primary
- Missing feedback on critical actions (success / failure not shown)

**Examples**:

- Two competing primary CTAs above the fold
- Form validation only at submit, on a 12-field form
- Search results page with no result count and no empty-state guidance
- A top-level navigation label uses internal jargon

## 🟡 Medium

A finding is Medium when **any** of:

- Causes friction or confusion but the user recovers within seconds
- Inconsistency on non-critical paths
- Visual rhythm / spacing / type issues that look unprofessional but readable
- Missing affordance that has a workaround

**Examples**:

- Spacing scale violated (`padding: 13px` instead of token)
- Tertiary action visually weighted equal to a secondary action
- Icon-only button with an ambiguous metaphor (recoverable via tooltip)
- Body line-length 95+ characters on wide screens

## 🟢 Low

A finding is Low when **all** of:

- The user does not consciously notice it
- Comprehension and completion are unaffected
- It is a polish opportunity, not a correctness issue

**Examples**:

- Slight optical alignment off (1–2px) on a non-critical icon
- Inconsistent corner radius between two surface variants
- Loading shimmer animation slightly off-rhythm
- Focus ring color is correct but could be more distinctive

## Tie-breakers

- If user impact is unclear, **escalate one tier higher**. Over-reporting Critical is worse than under-reporting; over-reporting High is acceptable.
- If a finding spans multiple tiers across breakpoints (e.g., Critical on mobile, Medium on desktop), use the **highest applicable tier** and note the affected breakpoints.
- Internal Design System violations default to **Medium** unless they cause a higher-tier symptom (then escalate).

## Reporting Quotas

There is no fixed quota per tier. Report what is found. If a category has zero findings, the section in the report still appears with `(no findings)`.
