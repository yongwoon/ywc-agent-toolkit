# Reconnaissance Before Action Pattern

Adopted from the anthropic/webapp-testing skill. The pattern transforms
the standard "act-then-hope" Playwright shape (`click → expect`) into a
deterministic three-step "see → confirm → act" sequence that eliminates
the timing-class flakiness category entirely.

## The Three Steps

Every meaningful interaction in an E2E test goes through this sequence:

1. **Reconnaissance** — snapshot the DOM state the action expects to find.
   The reconnaissance call is the proof that the precondition holds: if
   the snapshot does not contain the expected element, the action will
   not run.
2. **Confirmation** — `waitFor({ state: 'visible' })` on the locator the
   next action targets. This is the deterministic wait that replaces all
   `waitForTimeout(N)` calls — Playwright polls the DOM until the
   condition holds or the configured timeout elapses, at which point the
   test fails fast with a meaningful error instead of hanging or moving
   on to a doomed action.
3. **Action** — only after steps 1 and 2 pass does the action (`click`,
   `fill`, `selectOption`, etc.) run. The action's failure mode at this
   point is genuinely behavioral (the app did the wrong thing), not
   timing (the action raced the page).

## Banned Patterns

These patterns are **never** acceptable in generated test code under this
skill. Each is replaced by the equivalent condition-based primitive.

### `page.waitForTimeout(N)`

A flat sleep that ignores DOM state. Banned because:

- It slows the test suite linearly with the number of waits.
- It hides timing bugs — a 2000ms wait that "fixes" flakiness today
  becomes a 2001ms race condition tomorrow as the app gets slower.
- It produces no diagnostic value on failure ("test failed after 2
  seconds" tells you nothing about which element was missing).

```ts
//  WRONG
await page.click('[data-testid="submit"]');
await page.waitForTimeout(2000);
await expect(page.locator('h1')).toHaveText('Success');

//  RIGHT — reconnaissance → confirmation → action
const submit = page.locator('[data-testid="submit"]');
await submit.waitFor({ state: 'visible' });
await submit.click();
await page.waitForURL(/\/success/);
await expect(page.locator('h1')).toHaveText('Success');
```

### Implicit-wait `expect()` without DOM precondition

The bare `expect(locator).toBeVisible()` form polls until timeout, but
when paired with `click` immediately before, it masks "the click did not
trigger the expected effect" as a generic timeout. Always reconnoiter the
target before acting on it.

### Click on a locator that has not been confirmed visible

```ts
//  WRONG — locator may not exist yet
await page.locator('button.submit').click();

//  RIGHT — wait for the element to be ready
const submit = page.locator('[data-testid="submit"]');
await submit.waitFor({ state: 'visible' });
await submit.click();
```

## Condition-Based Waiting Primitives

Use these instead of `waitForTimeout`. Each names a real condition the
test depends on, which means the test's failure mode is informative.

| Primitive | When to use |
|---|---|
| `locator.waitFor({ state: 'visible' \| 'hidden' \| 'attached' })` | The most common case: wait for a specific element to enter or leave the DOM in a specific state. |
| `page.waitForURL(<regex \| string>)` | After a navigation or `page.goto`, wait for the URL to match. Replaces `waitForTimeout` after `click` on a navigation link. |
| `page.waitForResponse(<regex \| predicate>)` | After triggering an action that fires an XHR / fetch, wait for the specific response. Replaces `waitForTimeout` after form submit when you need the server roundtrip to complete. |
| `page.waitForLoadState('domcontentloaded' \| 'load' \| 'networkidle')` | Page-level lifecycle waiting. `networkidle` is fragile on apps with long-polling or analytics — prefer `domcontentloaded` and explicit per-element waits. |
| `page.waitForFunction(() => ...)` | Custom JS predicate against the page. Use when no built-in primitive captures the condition (e.g. wait until a React hook flips a flag exposed on `window`). |

## Sequence Template

The canonical shape every action in a generated test follows:

```ts
test('user can submit feedback', async ({ page }) => {
  // Reconnaissance — confirm we landed on the right page
  await page.goto('/feedback');
  await page.waitForURL(/\/feedback$/);
  const heading = page.locator('h1');
  await heading.waitFor({ state: 'visible' });
  await expect(heading).toHaveText('Send feedback');

  // Confirmation — locate the form input and confirm visibility
  const subject = page.locator('[data-testid="feedback-subject"]');
  await subject.waitFor({ state: 'visible' });

  // Action — fill, then advance through the next step
  await subject.fill('Login button is too small');

  const submit = page.locator('[data-testid="feedback-submit"]');
  await submit.waitFor({ state: 'visible' });
  await submit.click();

  // Reconnaissance for the next state
  await page.waitForURL(/\/feedback\/thanks$/);
  await expect(page.locator('h1')).toHaveText('Thanks');
});
```

Every `waitFor` / `waitForURL` / `waitForResponse` call is a narrow,
named precondition. If the test fails, the failure message points
directly at the unmet precondition rather than a generic timeout.

## Exceptions

`waitForTimeout` has **one** legitimate use: when the test deliberately
waits for a debounce or throttle window to elapse and there is no
observable DOM change to wait for (e.g. confirming that a search input
debounces 300ms before firing). In that case:

- Pair the timeout with a comment naming the specific debounce / throttle
  it waits for (`// 300ms search debounce, see SearchBox.tsx`).
- Use the smallest interval that demonstrates the behavior (300ms, not
  2000ms "to be safe").
- Add a `waitForResponse` immediately after to confirm the debounced call
  actually fired — the timeout alone is not a sufficient assertion.

Outside that narrow case, `waitForTimeout` is banned and audit Mode B
flags it as a fragile pattern.

## Cross-References

- `playwright-patterns.md` — selector priority (`data-testid` → ARIA →
  text → CSS) and the broader Playwright authoring conventions. The
  reconnaissance pattern uses those same selectors; this file is the
  timing-discipline complement to that file's locator-discipline
  guidance.
- `priority-matrix.md` — Mode B audit scoring. A test that uses
  `waitForTimeout(N)` outside the debounce exception is automatically a
  **Gap** finding regardless of which user flow it covers.
- anthropic/webapp-testing skill — source pattern. The
  "reconnaissance-before-action" wording originates there; this
  reference adapts the pattern to the ywc-e2e-test-strategy skill's
  three-mode workflow.
