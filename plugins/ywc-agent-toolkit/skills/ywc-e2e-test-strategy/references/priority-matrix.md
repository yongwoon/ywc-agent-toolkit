# E2E Test Priority Matrix

Framework for deciding what to automate, what to keep manual, and in what order.

## Automation Decision Framework

Automate a flow when it scores HIGH on both axes:

| Axis | HIGH (automate) | LOW (keep manual or skip) |
|---|---|---|
| **Business impact** | Revenue path, authentication, core feature | Edge case, admin-only, rarely used |
| **Failure frequency** | Breaks after refactoring, stateful logic | Stable UI with no logic |

## Priority Scoring

Score each candidate flow from 1–3 on each dimension. Automate flows with total score ≥ 5.

| Dimension | 1 (Low) | 2 (Medium) | 3 (High) |
|---|---|---|---|
| Revenue / user impact | Nice-to-have feature | Important feature | Core revenue / login |
| Failure likelihood | Stable, rarely changes | Changes occasionally | Complex logic, stateful |
| Manual test cost | 1 min to verify | 5–10 min to verify | 15+ min or multi-step |

## Recommended Starting 5 for a Web App

For a solo developer launching a web product, these 5 flows provide the highest ROI:

| Priority | Flow | Why |
|---|---|---|
| 1 | **Authentication** (login + logout) | Everything depends on this; breaks silently after auth refactors |
| 2 | **Core feature happy path** | The action users pay for or return for; regression here is critical |
| 3 | **Form validation + error state** | Input handling breaks often after library upgrades |
| 4 | **Navigation / routing** | Broken links are invisible to developers, obvious to users |
| 5 | **API error handling** | Network failures should degrade gracefully, not show blank screens |

## What to Keep Manual

Not everything should be automated. These categories are better left to manual or `ywc-gen-testcase` test sheets:

| Category | Why skip automation |
|---|---|
| Visual design / pixel accuracy | Screenshots are fragile; better served by visual regression tools |
| Exploratory UX | Automation follows scripts; humans find unexpected issues |
| One-time migrations | Setup cost > test lifetime value |
| Third-party OAuth flows | Cannot automate real OAuth redirects reliably |
| Email / SMS verification | Requires inbox access; use mocking via `page.route()` instead |

## Coverage Gap Severity Definitions

Use these consistently in Audit mode reports:

| Severity | Definition | Example |
|---|---|---|
| **CRITICAL** | No test for a flow that directly handles money, data loss, or authentication | Checkout with no payment test |
| **GAP** | No test for a high-traffic or frequently broken flow | Search with no test |
| **LOW** | No test for a low-traffic or stable flow where manual verification is cheap | Admin settings page |

## Flaky Test Risk Signals

Flag existing tests with these patterns during Audit mode:

| Signal | Risk level | Action |
|---|---|---|
| `waitForTimeout(n)` | High | Replace with locator-based wait |
| CSS class selector `.btn-*` | Medium | Replace with `data-testid` or ARIA role |
| No `expect()` call | High | Add assertion or delete test |
| Shared state between `test()` blocks | High | Add `beforeEach` reset |
| Test depends on execution order | High | Make each test independent |
