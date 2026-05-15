---
name: ywc-product-review
version: 1.0.0
description: (ywc) Use when the user wants a business/service perspective review of a project (user value, UX, growth, risk, market). Triggers: "product review", "service feedback", "비즈니스 관점 리뷰", "서비스 개선 포인트", "what should we improve", "プロダクトレビュー", "サービス改善". Do not use for code-level review (use ywc-impl-review), security review (use ywc-security-audit), or UI/UX implementation review (use ywc-ui-ux-review).
category: review
phase: quality
requires: []
advisor_budget: 2
---

# Product Review

**Announce at start:** "I'm using the ywc-product-review skill to evaluate the project from 5 business/service perspectives."

Analyze a project from 5 business and service perspectives to generate a prioritized improvement report.

## Rationalization Defense

When tempted to skip a step, check this table first:

| Excuse | Reality |
|---|---|
| "User Value perspective is obvious, skip it" | All 5 perspectives must be addressed. Missing one creates a blind spot in the prioritized report. |
| "Feature recommendations should match what the user already wants" | Honest review means surfacing tradeoffs the user did not ask about. Soften tone, never soften findings. |
| "I'll mix multiple perspectives in one finding to save space" | Tag each finding with exactly one primary perspective. Multi-tag findings become impossible to triage. |
| "Priority is roughly High, do not specify P0/P1/P2" | Always emit explicit priority. Without it, the report becomes a wishlist instead of a plan. |
| "Risks are speculative, drop them from the report" | Risk is a perspective. Speculative risks are still findings — mark `unverified`, do not drop. |
| "I have no live access, infer growth metrics from code" | If a perspective cannot be assessed (no live data), state the gap. Do not fabricate. |
| "Running 5 perspectives sequentially is fine" | Phase 1 fan-out reduces total latency; each Sonnet subagent sees only one perspective's checklist, lowering per-call context and improving analysis depth. |

**Violating the letter of these rules is violating the spirit.** A product review with cherry-picked perspectives misses the most expensive problems.

## Perspectives

| Tag | Perspective | Reference |
|---|---|---|
| `[User Value]` | Job-to-be-Done, value proposition, unmet needs | `references/user-value.md` |
| `[UX Flow]` | Onboarding, drop-off points, core user journey | `references/ux-flow.md` |
| `[Growth]` | Retention, viral loops, activation, engagement | `references/growth.md` |
| `[Risk]` | User pain points, churn drivers, unsolved problems | `references/risk.md` |
| `[Market]` | Feature prioritization, market trends, competitive gaps | `references/market-timing.md` |

## Workflow

### Step 1: Gather Context

Read the following in order:
1. `README.md` (or equivalent top-level docs) — understand what the service does and who it targets
2. Key specification or design documents if referenced
3. Directory structure — identify key feature areas from folder/file names
4. Core entrypoint files — understand main flows and features implemented
5. `docs/ubiquitous-language.md` (if it exists) — domain vocabulary that names the key entities, user roles, and business actions; this sharpens the User Value and UX Flow perspectives

Focus on: what the service **does**, who it serves, and what the main user flows are.

### Step 2: Phase 1 — Parallel Perspective Review

Use the Task tool to spawn 5 Sonnet subagents in parallel — one per perspective. Pass each subagent a brief context summary (service name, target user, main flows) and the corresponding reference file to read:

| Subagent | Model | Reference |
|---|---|---|
| User Value | sonnet | `references/user-value.md` |
| UX Flow | sonnet | `references/ux-flow.md` |
| Growth | sonnet | `references/growth.md` |
| Risk | sonnet | `references/risk.md` |
| Market | sonnet | `references/market-timing.md` |

Each subagent classifies its findings:
- **High**: Directly blocks or degrades core user value, causes churn, or represents a significant missed opportunity
- **Medium**: Meaningfully improves experience, growth, or differentiation with moderate effort
- **Low**: Incremental improvement, nice-to-have, or long-term consideration

Each subagent returns two artifacts:
- **Confirmed findings** — perspective tag, problem statement, evidence, improvement suggestion
- **Advisor candidates** — cross-perspective conflicts where two reasonable positions exist (include conflicting finding excerpts + one-sentence reason for escalation)

### Step 2b: Aggregate Phase 1 Results

Combine findings from all 5 subagents. Deduplicate by evidence source. Select up to `advisor_budget` (default: 2) advisor candidates, prioritizing High over Medium findings.

### Step 3: Phase 2 — Advisor Pass

Follow the **Advisor Escalation Policy** section below. For each surviving candidate, spawn a short Opus subagent via the Task tool. Pass only the conflicting finding excerpts (≤100 lines total). Merge Phase 2 verdicts into the confirmed findings list.

### Step 4: Generate Report

Use `references/report-template.md` as the output structure.

- Group findings by priority tier (🔴 High → 🟡 Medium → 🟢 Low)
- Each finding must include: perspective tag, problem statement, evidence from codebase/docs, improvement suggestion
- End with a 3-item executive summary: biggest opportunity, most urgent issue, long-term direction

## Advisor Escalation Policy

**Budget**: up to **2 Opus advisor calls per invocation**.

Escalate to an Opus advisor only when the executor genuinely cannot resolve ambiguity from the reference files alone. Escalation is reserved for two conditions:

| Condition | Example |
|---|---|
| **Cross-perspective priority conflict** | A finding is classified Critical under `[Risk]` but Low under `[Market]`, and the correct priority tier determines a concrete recommendation that contradicts the other perspective |
| **Architectural product trade-off** | A recommendation from one perspective (e.g., deepen a niche feature for `[User Value]`) would directly undermine another perspective (e.g., limit growth loop activation under `[Growth]`), and resolving the conflict requires product strategy judgment beyond the reference checklists |

For all other ambiguities — borderline High vs Medium severity, uncertain evidence strength, incomplete codebase — use conservative judgment (prefer the lower priority) and note the uncertainty inline in the report. Do not escalate these to Opus.

## Notes

- If the user provides specific docs or files, read those first before scanning the codebase
- If the codebase is large, focus on README, main entrypoints, and feature directories rather than implementation details
- Base all findings on observable evidence — avoid speculation without grounding in what you actually read
- Follow any additional instructions in `$ARGUMENTS`
