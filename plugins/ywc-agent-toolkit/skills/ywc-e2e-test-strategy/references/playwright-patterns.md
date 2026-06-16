# Playwright Patterns Reference

Selector strategy, configuration template, wait patterns, and anti-patterns for consistent E2E tests.

## Config Template

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? [['html'], ['github']] : [['html']],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
```

## Selector Priority (Most to Least Stable)

| Priority | Method | Example | Notes |
|----------|--------|---------|-------|
| 1 | `data-testid` | `page.getByTestId('submit-btn')` | Most stable; survives refactoring |
| 2 | ARIA role | `page.getByRole('button', { name: 'Submit' })` | Accessible and semantic |
| 3 | Visible text | `page.getByText('Submit order')` | Brittle on i18n but readable |
| 4 | Label | `page.getByLabel('Email address')` | Good for form fields |
| 5 | CSS selector | `page.locator('.submit-btn')` | Last resort; breaks on style changes |
| ❌ | XPath | `page.locator('//button[1]')` | Never use — breaks on DOM changes |

## Test File Template

```typescript
// e2e/user-login.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Login', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('logs in with valid credentials', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Sign in' }).click();

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByTestId('user-menu')).toBeVisible();
  });

  test('shows error on invalid credentials', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('wrong-password');
    await page.getByRole('button', { name: 'Sign in' }).click();

    await expect(page.getByRole('alert')).toContainText('Invalid credentials');
    await expect(page).toHaveURL('/login');
  });
});
```

## Wait Patterns

### Correct: Locator-based waits

```typescript
// Wait for element to appear
await expect(page.getByTestId('toast')).toBeVisible();

// Wait for navigation
await page.getByRole('button', { name: 'Submit' }).click();
await page.waitForURL('/confirmation');

// Wait for network response
const responsePromise = page.waitForResponse('/api/orders');
await page.getByRole('button', { name: 'Place order' }).click();
const response = await responsePromise;
expect(response.status()).toBe(201);
```

### Wrong: Time-based waits

```typescript
// ❌ Never do this
await page.waitForTimeout(2000);
await page.waitForTimeout(500); // "just to be safe"
```

## Stubbing External APIs

Use `page.route()` to stub third-party calls (Stripe, Sendgrid, etc.) so tests don't depend on external services:

```typescript
test('handles payment success', async ({ page }) => {
  await page.route('**/api/stripe/charge', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ id: 'ch_test_123', status: 'succeeded' }),
    });
  });

  // Continue with test...
});
```

## State Isolation

Each test must start from a clean state. Do not share state between tests.

```typescript
test.beforeEach(async ({ page, request }) => {
  // Reset via API (fastest)
  await request.post('/api/test/reset');
  // OR navigate to a known start state
  await page.goto('/');
});
```

## Common Anti-patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `waitForTimeout(n)` | Brittle, slow | Use `expect(locator).toBeVisible()` |
| CSS class selector | Breaks on styling | Use `data-testid` or ARIA role |
| No assertions | Test always passes | Add at least one `expect()` |
| Shared state between tests | Order-dependent failures | Use `beforeEach` to reset |
| Testing all pages | Maintenance burden | Focus on critical user paths |
| XPath selectors | DOM-structure coupling | Use Playwright locator methods |
