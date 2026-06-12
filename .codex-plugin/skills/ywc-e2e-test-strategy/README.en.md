# ywc-e2e-test-strategy

A skill for designing and implementing an automated E2E test strategy using Playwright. Handles new project Playwright setup, existing coverage gap analysis, single user flow test generation, and GitHub Actions CI integration.

## Use Scenarios

- **New project**: "Set up Playwright", "Add E2E tests for the first time"
- **Existing project audit**: "Find missing critical path coverage", "Check E2E gaps"
- **Single flow**: "Write a Playwright test for the login flow", "Generate a checkout E2E test"
- **CI integration**: "Wire Playwright into GitHub Actions"

## Usage

```bash
/ywc-e2e-test-strategy --init           # Set up Playwright from scratch
/ywc-e2e-test-strategy --audit          # Audit existing E2E coverage
/ywc-e2e-test-strategy --flow login     # Generate test for a specific flow
/ywc-e2e-test-strategy --init --ci      # Init + GitHub Actions workflow
```

Or invoke with natural language:

> "Design an E2E test strategy with Playwright"
> "Automate the critical user paths"
> "Audit my E2E coverage"

## Modes

| Mode | Flag | When to use |
|------|------|-------------|
| Init | `--init` | No `playwright.config.*` found |
| Audit | `--audit` | Existing E2E tests present |
| Flow | `--flow <name>` | Adding a single user flow test |

Without a flag, the skill auto-detects mode from the filesystem.

## Output

- `playwright.config.ts` — env-var-based baseURL configuration
- `e2e/*.spec.ts` — test files per critical path
- `.github/workflows/e2e.yml` — CI workflow (`--ci` or `--init`)
- Audit report — coverage gaps and flaky test risk analysis

## Related Skills

- `ywc-gen-testcase` — manual verification test sheets (human-verified, not automated)
- `ywc-impl-review` — code-level implementation review
- `ywc-security-audit` — security audit for auth and input-handling flows
