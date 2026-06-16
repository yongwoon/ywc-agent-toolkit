# GitHub Actions E2E Workflow Templates

Templates for integrating Playwright E2E tests into GitHub Actions CI pipelines.

## Standard E2E Workflow

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    name: Playwright E2E
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'          # Change to 'yarn' or 'pnpm' as needed

      - name: Install dependencies
        run: npm ci

      - name: Cache Playwright browsers
        uses: actions/cache@v4
        id: playwright-cache
        with:
          path: ~/.cache/ms-playwright
          key: playwright-${{ runner.os }}-${{ hashFiles('package-lock.json') }}

      - name: Install Playwright browsers
        if: steps.playwright-cache.outputs.cache-hit != 'true'
        run: npx playwright install --with-deps chromium

      - name: Start dev server
        run: npm run dev &
        env:
          BASE_URL: http://localhost:3000

      - name: Wait for server
        run: npx wait-on http://localhost:3000 --timeout 30000

      - name: Run E2E tests
        run: npx playwright test
        env:
          BASE_URL: http://localhost:3000
          CI: true

      - name: Upload test report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

## Against Staging / Preview URL

When tests should run against a deployed preview (e.g., Vercel preview deployments):

```yaml
jobs:
  e2e:
    name: Playwright E2E (Staging)
    runs-on: ubuntu-latest
    environment: staging

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Run E2E tests against staging
        run: npx playwright test
        env:
          BASE_URL: ${{ vars.STAGING_URL }}   # Set in GitHub Environments
          CI: true

      - name: Upload report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

## Package Manager Variants

### pnpm

```yaml
- uses: pnpm/action-setup@v4
  with:
    version: 9
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'pnpm'
- run: pnpm install --frozen-lockfile
```

### Bun

```yaml
- uses: oven-sh/setup-bun@v2
- run: bun install --frozen-lockfile
```

## Key Decisions

| Decision | Recommended | Why |
|---|---|---|
| Browser | Chromium only (in CI) | Covers 65%+ of users; Safari/Firefox add cost and flakiness |
| Retries in CI | `retries: 2` | Absorbs transient flakiness without hiding real failures |
| `workers` in CI | `1` | Avoids race conditions on shared dev server |
| Artifacts | Always upload on failure | Trace + screenshots are essential for CI debugging |
| Cache key | `hashFiles('package-lock.json')` | Invalidates only when dependencies change (~300MB download) |
| Timeout | `30` minutes | Prevent hung jobs from blocking the queue |
