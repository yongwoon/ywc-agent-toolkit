# Product Review Skill

## Overview

**ywc-product-review** is a Claude Code Skill that analyzes a project from 5 business and service perspectives to deliver a prioritized improvement feedback report.

It analyzes both the codebase and documentation (README, specs, product docs) to surface improvement opportunities from a **user value, growth, risk, and market** perspective — not a technical code quality perspective.

**Key Features:**

- Analysis across 5 business perspectives
- Integrated analysis of codebase + documentation
- Automatically generates a 🔴 High / 🟡 Medium / 🟢 Low priority report
- Includes actionable improvement suggestions for each finding
- Executive Summary distills the most important insights

**Target Users:**

- Product Managers and developers looking for service improvement direction
- Teams wanting to review a project from a business perspective
- Anyone asking "what should we build next?"

---

## How to Use

### Invoking the Skill

In Claude Code:

```
# Full analysis (all 5 perspectives)
/ywc-product-review

# Specific perspectives only
/ywc-product-review user-value growth

# With explicit document references
/ywc-product-review @README.md @docs/spec.md
```

Or in natural language:

```
User: Review this project from a business perspective
User: Find service improvement opportunities
User: What should we improve for growth?
User: Analyze gaps in user value
```

### Prerequisites

- The target project codebase is available in the current directory, or
- Documentation such as README or product specs can be referenced

---

## Analysis Perspectives

### 5 Core Perspectives

| Tag | Analysis Content | Reference File |
|---|---|---|
| `[User Value]` | Job-to-be-Done, Value Proposition, unmet user needs | `references/user-value.md` |
| `[UX Flow]` | Onboarding, drop-off points, core user journey | `references/ux-flow.md` |
| `[Growth]` | Retention, viral loops, activation, engagement | `references/growth.md` |
| `[Risk]` | User pain points, churn drivers, unsolved problems | `references/risk.md` |
| `[Market]` | Feature prioritization, market trends, competitive gaps | `references/market-timing.md` |

### Analysis Flow

```
Gather context (README + codebase)
    ↓
Phase 1: 5 perspective subagents run in parallel (each Sonnet)
├── User Value  ├── UX Flow  ├── Growth  ├── Risk  └── Market
    ↓
Phase 2: Opus Advisor (cross-perspective conflicts, max 2 calls)
    ↓
Classify by priority (High / Medium / Low)
    ↓
Generate report + Executive summary
```

---

## Output Report Format

After analysis, results are reported in this format:

```markdown
## Product Review Report: [Project Name]

**Analysis Date**: [Date]
**Perspectives Reviewed**: User Value · UX Flow · Growth · Risk · Market Timing

---

### 🔴 High Priority — Immediate Action Recommended

| # | Perspective   | Problem        | Evidence        | Suggestion      |
|---|---------------|----------------|-----------------|-----------------|
| 1 | [User Value]  | [Problem desc] | [Code/doc ref]  | [Improvement]   |

---

### 🟡 Medium Priority — Review for Near-Term Roadmap

...

---

### 🟢 Low Priority — Long-Term Consideration

...

---

### Executive Summary

- **Biggest opportunity**: [Highest-leverage improvement]
- **Most urgent issue**: [Most critical problem to fix]
- **Long-term direction**: [Strategic direction for next phase]
```

---

## File Structure

```
ywc-product-review/
├── SKILL.md                        # Skill definition and workflow
├── README.md                       # Korean guide
├── README.en.md                    # This file (English guide)
├── README.ja.md                    # Japanese guide
├── README.ko.md                    # Korean guide (same as README.md)
└── references/
    ├── user-value.md               # User value checklist
    ├── ux-flow.md                  # UX flow checklist
    ├── growth.md                   # Growth mechanics checklist
    ├── risk.md                     # Risk & pain points checklist
    ├── market-timing.md            # Market timing checklist
    └── report-template.md          # Report output template
```

---

## Usage Examples

### Example 1: Full Analysis

```
User: Review this project from a business perspective

Claude: Reading project structure and README...

[Codebase and documentation analysis]

Phase 1: Running 5 subagents in parallel...
[User Value Subagent] Reviewing Job-to-be-Done clarity
[UX Flow Subagent] Analyzing onboarding and core flows
[Growth Subagent] Reviewing retention and viral mechanisms
[Risk Subagent] Identifying unresolved pain points
[Market Subagent] Analyzing competitive gaps and timing
Phase 2: Opus Advisor reviewing cross-perspective conflicts...

## Product Review Report: My Project

### 🔴 High Priority

| # | Perspective | Problem | Evidence | Suggestion |
|---|---|---|---|---|
| 1 | [UX Flow] | Onboarding requires 5+ steps | README Quick Start is complex | Simplify to reach core value within 2 steps |
| 2 | [Growth] | No retention mechanism | No re-engagement features found | Add weekly summary or progress dashboard |

...

### Executive Summary
- **Biggest opportunity**: Simplify onboarding to improve activation rate
- **Most urgent issue**: No mechanism to bring users back
- **Long-term direction**: Introduce collaboration features with network effects
```

### Example 2: Single Perspective Analysis

```
User: Analyze from a Growth perspective only

Claude: Focusing on Growth Mechanics perspective.

[Load and apply references/growth.md]

## Product Review Report: My Project
**Perspectives Reviewed**: Growth

### 🔴 High Priority
...
```

---

## Best Practices

### 1. Provide Both Docs and Code

Providing README, specs, or user interview notes alongside the codebase enables deeper analysis:

```
User: Review this with @README.md @docs/product-spec.md
```

### 2. Use Repeatedly to Track Evolution

Re-run after adding features or improvements to compare before/after:

```
# Before improvement
/ywc-product-review

# Re-analyze after feature work (3 months later)
/ywc-product-review
```

### 3. Use Executive Summary as Roadmap Input

Feed High Priority items directly into Sprint planning or Milestone definitions.

---

## Related Documents

### Internal References

- [UI/UX Review Skill](../ywc-ui-ux-review/README.en.md) — Detailed UI/UX review (visual design, information architecture)

### External References

- [Jobs-to-be-Done Theory](https://hbr.org/2016/09/know-your-customers-jobs-to-be-done) — Clayton Christensen
- [Hooked: How to Build Habit-Forming Products](https://www.nirandfar.com/hooked/) — Nir Eyal

---

## Version

- **Last Updated**: 2026-04-25
- **Skill Version**: 1.0
- **Compatible With**: Claude Code

---

## License

This Skill is part of the `develop-with-llm` project, provided for learning and reference purposes.
