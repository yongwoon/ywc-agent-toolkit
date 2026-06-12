---
name: ywc-e2e-test-strategy
description: "(ywc) Use when designing an automated E2E test strategy for a web application, setting up Playwright from scratch, auditing existing E2E coverage gaps, or generating Playwright test code for a specific critical user flow with GitHub Actions CI integration. Triggers: \"E2E 테스트 전략\", \"Playwright 설정\", \"critical path 자동화\", \"E2E 테스트 작성\", \"e2e coverage 점검\", \"e2e test strategy\", \"playwright setup\", \"playwright test\", \"E2Eテスト戦略\", \"Playwright設定\", \"テスト自動化\". Do not use for generating manual verification test sheets (use ywc-gen-testcase), writing unit or integration tests at the code level, or security-focused penetration testing (use ywc-security-audit)."
---

# E2E Test Strategy

**Announce at start:** "I'm using the ywc-e2e-test-strategy skill to design an automated E2E test strategy with Playwright."

Design and implement an automated E2E test strategy for web applications using Playwright. The skill operates in three modes — `--init` (new project setup), `--audit` (coverage gap analysis), or `--flow <name>` (single flow generation) — and produces ready-to-run Playwright test files plus a GitHub Actions CI workflow.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "Unit tests already cover this, E2E is overkill" | Unit tests verify code logic in isolation. E2E tests verify the app works end-to-end from the user's perspective. A passing unit suite does not prevent login from breaking in production. |
| "We'll add E2E tests later when the product stabilizes" | The later tests are added, the harder they are to retrofit. 5 critical-path tests on week 1 cost 90% less effort than 50 tests on week 20 against a hardened codebase. |
| "Test everything to be safe" | Over-testing creates a maintenance burden that kills a solo developer. Start with 5–8 critical paths, measure flakiness, expand only where failure hurts users. |
| "CSS class selectors are fine, they're stable enough" | Class names change during refactoring and styling. Prefer `data-testid` → ARIA role → visible text. See [references/playwright-patterns.md](references/playwright-patterns.md). |
| "waitForTimeout(2000) fixes the flaky test" | Explicit timeouts mask timing problems and slow the suite. Banned outside the narrow debounce exception. Use the Reconnaissance Before Action pattern (`locator.waitFor()` → action → `waitForURL()` / `waitForResponse()`); see [references/reconnaissance-pattern.md](references/reconnaissance-pattern.md). |
| "Skip GitHub Actions integration until later" | CI integration is what turns tests from a local convenience into a production safety net. Running only locally creates false confidence. |
| "All three modes apply here, run all three" | Modes are mutually exclusive. Auto-detect: if `playwright.config.*` exists → `--audit`; if not → `--init`. When user specifies `--flow`, run only flow generation. |

**Violating the letter of these rules is violating the spirit.** A flaky or unmaintained E2E suite is worse than none — it erodes trust in CI and gets disabled.

## Arguments

Parse `$ARGUMENTS`.

| Parameter | Format | Example | Description |
|---|---|---|---|
| `--init` | flag | `--init` | Set up Playwright from scratch for the project |
| `--audit` | flag | `--audit` | Analyze existing E2E coverage and identify gaps |
| `--flow <name>` | string | `--flow user-login` | Generate a Playwright test for a specific user flow |
| `--ci` | flag | `--ci` | Include or update GitHub Actions E2E workflow |
| `--dry-run` | flag | `--dry-run` | Show plan without writing any files |

**Mode selection rule**: `--init`, `--audit`, and `--flow` are mutually exclusive. If none is given, auto-detect from filesystem (see Context). If conflict detected, stop and ask.

## Context

- Playwright config: !`ls playwright.config.* 2>/dev/null || echo "not found"`
- Existing E2E specs: !`find . -path "*/e2e/*.spec.*" -o -path "*/tests/e2e/*.spec.*" 2>/dev/null | wc -l | tr -d ' '`
- Package manager: !`ls package-lock.json yarn.lock pnpm-lock.yaml bun.lockb 2>/dev/null | head -1`
- GitHub Actions workflows: !`ls .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null | head -5 || echo "none"`

## Workflow

### Mode A — Init (New Playwright Setup)

**When**: `--init` flag, or no `playwright.config.*` found.

**Step 1: Clarify critical paths**

If the user has not listed the flows to cover, ask for the 3–5 most critical user flows. For a typical web app, suggest these defaults and confirm:

1. Authentication (login / logout / session expiry)
2. Core feature happy path (the action that delivers primary value)
3. Error state handling (failed form submission or API error)

Do not proceed to Step 2 until at least one flow is confirmed.

**Step 2: Install and configure Playwright**

```bash
npx playwright install --with-deps chromium
```

Generate `playwright.config.ts` using the config template in [references/playwright-patterns.md](references/playwright-patterns.md). Key decisions:
- `baseURL`: always `process.env.BASE_URL || 'http://localhost:3000'` — never hardcode
- `testDir`: `./e2e`
- `use.trace`: `'on-first-retry'` — not `'on'` (file size matters in CI)
- `reporter`: `['html']` locally; `['html', 'github']` in CI (detect via `process.env.CI`)

**Step 3: Generate initial test files**

For each confirmed critical path, generate one `e2e/<flow-name>.spec.ts` file following the patterns in [references/playwright-patterns.md](references/playwright-patterns.md). Selector priority: `data-testid` → ARIA role → visible text → CSS (last resort only).

**Step 4: Wire GitHub Actions**

Always generate `.github/workflows/e2e.yml` on `--init`. Use the template in [references/github-actions-e2e.md](references/github-actions-e2e.md). If a workflow file already exists, add an `e2e` job to it rather than creating a new file.

**Step 5: Report** — see Output Format.

---

### Mode B — Audit (Coverage Gap Analysis)

**When**: `--audit` flag, or `playwright.config.*` found and no other mode flag.

**Step 1: Inventory existing tests**

```bash
find . \( -path "*/e2e/**/*.spec.*" -o -path "*/tests/e2e/**/*.spec.*" \) | sort
```

For each spec file, extract test names:

```bash
grep -E "^\s*(test|it)\(" <file> | head -20
```

**Step 2: Detect fragile patterns**

Flag any test that uses:
- `page.waitForTimeout()` — flaky risk
- CSS class selectors like `.btn-submit` — fragile
- Zero `expect()` calls — no assertion

**Step 3: Map to user flows and score gaps**

Use the Priority Matrix in [references/priority-matrix.md](references/priority-matrix.md) to score uncovered flows. Assign severity: Critical / Gap / Low.

**Step 4: Recommend next 3 tests**

For each recommended test: flow name, why it matters, estimated lines of code.

**Step 5: Check CI integration**

Verify `.github/workflows/` contains an E2E job. If not, report `CI: ❌ missing` and offer to generate with `--ci`.

---

### Mode C — Flow Generation

**When**: `--flow <name>` flag.

**Step 1: Understand the flow**

If the flow is not self-evident from the name, ask for:
- Entry URL or route
- Ordered user actions
- Expected end state (URL, visible text, element)

**Step 2: Generate test file**

Write `e2e/<flow-name>.spec.ts`. Follow [references/playwright-patterns.md](references/playwright-patterns.md):
- One `test.describe` block per flow
- `beforeEach` for shared setup (navigate to entry URL, reset state)
- Stub external API calls with `page.route()` when the flow depends on third-party services
- Include at least one negative case (error path)

**Step 3: Offer CI integration**

If `--ci` flag given, or no GitHub Actions E2E job exists, offer to generate or update `.github/workflows/e2e.yml`.

## Output Format

### Init and Flow modes

```text
E2E Strategy — Mode: init | flow: <name>

Files written:
  playwright.config.ts
  e2e/login.spec.ts            (8 test cases)
  e2e/checkout.spec.ts         (5 test cases)
  .github/workflows/e2e.yml    (--ci)

Critical paths covered: 2 of 5 identified
Selectors used: data-testid (12), ARIA role (3), visible text (1)

Next:
  1. Run `npx playwright test` to verify locally
  2. Push branch — GitHub Actions will run E2E on every PR
```

### Audit mode

```text
E2E Coverage Audit

Tests found: 12 across 4 spec files
Flaky risk:  3 tests use waitForTimeout
Fragile:     2 tests use CSS class selectors

Coverage Gaps (by priority):
  [CRITICAL] Checkout flow     — no test; primary revenue path
  [GAP]      Password reset    — no test; common support ticket source
  [LOW]      Profile avatar    — manual acceptable; low failure frequency

CI Integration: ✅ .github/workflows/e2e.yml (e2e job found)

Recommended next tests: checkout-flow, password-reset
```

## Validation

Before declaring complete:

- [ ] `playwright.config.ts` reads `baseURL` from `process.env.BASE_URL`, not hardcoded
- [ ] Every generated spec has at least one `expect()` assertion
- [ ] No `waitForTimeout()` in generated code
- [ ] GitHub Actions workflow triggers on both `push` to main and `pull_request`
- [ ] Playwright browser cache step present in CI workflow (avoids re-downloading ~300MB per run)
- [ ] `--dry-run` output confirmed by user before writing (if flag given)

## Reconnaissance Before Action

All generated Playwright code follows the three-step **Reconnaissance Before Action** pattern: snapshot the DOM state the action expects to find (reconnaissance), `waitFor({ state: 'visible' })` on the locator the next action targets (confirmation), then execute the action (`click`, `fill`, etc.). The pattern eliminates timing-class flakiness by replacing every `waitForTimeout(N)` with a named, condition-based precondition.

**Banned in generated code**: `page.waitForTimeout(N)` outside the narrow debounce exception (see the reference). Mode B audit flags `waitForTimeout` as a fragile pattern automatically.

**Required substitutions**: `locator.waitFor({ state: 'visible' \| 'hidden' \| 'attached' })` for element state · `page.waitForURL(<regex>)` after navigation · `page.waitForResponse(<predicate>)` after XHR / fetch · `page.waitForFunction(...)` for custom JS predicates. Each is a narrow, named precondition — when the test fails, the failure message points at the unmet precondition rather than a generic timeout.

Full pattern, banned-form / right-form examples, condition-primitive table, and the debounce exception live in [references/reconnaissance-pattern.md](references/reconnaissance-pattern.md). Generated tests in Mode A / Mode C and audit findings in Mode B treat this file as the authoritative pattern.

## Common Mistakes

- **Hardcoding `baseURL`** — tests must run in CI against a preview URL, not always localhost.
- **Testing implementation details** — test what the user sees and does, not internal component state or React props.
- **Generating coverage for every page** — 5 high-value critical-path tests beat 50 shallow page-load checks.
- **No state isolation** — shared state between tests creates order-dependent failures. Always `beforeEach` reset.
- **Skipping the negative case** — every critical flow has an error path (wrong password, network failure). Test it.

## Integration

- **Upstream**: none required. Run after implementation (ywc-impl-review) confirms the feature is working.
- **Downstream**: `ywc-gen-testcase` — for manual test sheets that complement automated E2E coverage.
- **Pairs with**: `ywc-impl-review` — verifies implementation correctness at code level; this skill verifies user-visible behavior end-to-end.
- **Related**: `ywc-security-audit` — security testing of authenticated and input-handling flows.
