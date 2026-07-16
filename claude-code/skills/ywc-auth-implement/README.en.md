# ywc-auth-implement

Standardizes authentication feature implementation (email/password, OAuth, MFA, shallow RBAC). Orchestrates a policy interview, stack detection, a dynamic battle-tested library/managed-service recommendation, and dispatch to `ywc-backend-coder`/`ywc-frontend-coder`/`ywc-doc-writer`. This skill never writes application auth code itself.

## Usage Scenarios

- The user says "implement auth", "add login", or "set up authentication"
- A new project needs email/password or OAuth-based authentication for the first time
- Existing authentication needs extension or migration (requires a `new`/`extend`/`migrate` choice)

## How to Use

```bash
/ywc-auth-implement
```

Or invoke via natural language:

> "Implement authentication for this project"

## Input

- Required: the target project's Framework/Database evidence (auto-detected; routes to `ywc-tech-research` when insufficient)
- Required: user answers to the 9-category policy interview (method/MFA/session/password/profile/deletion/RBAC/consent/abuse-prevention)
- Optional: a `new`/`extend`/`migrate` choice when existing auth is detected

## Output

- Preflight results, policy interview summary, recommended library/service, dispatched subagent list, Security/E2E Gate result, and the `## Output Format` 4-value Completion Status (`DONE`/`DONE_WITH_CONCERNS`/`BLOCKED`/`NEEDS_CONTEXT`)
- Preflight stops before any interview question and returns `NEEDS_CONTEXT` when existing auth is detected (until the user picks `new`/`extend`/`migrate`) or when stack evidence is insufficient (routes to `ywc-tech-research` first)
- The Security/E2E gate maps `ywc-security-audit` severity to status: Critical/High = 0 proceeds to the policy-conditional E2E; Critical/High ≥ 1 ends the run as `DONE_WITH_CONCERNS` and skips E2E, the PR suggestion, and recommendation caching until remediation and re-audit; a failed audit command returns `BLOCKED`; an insufficient scope/trust boundary returns `NEEDS_CONTEXT`
- `DONE` requires the Security gate clean and every approved E2E flow captured with fresh evidence (command, exit code, key output); anything short of that reports the status above with the specific gate that stopped it

## Related Skills

- `ywc-backend-coder` / `ywc-frontend-coder` — implementation dispatch targets under TDD discipline
- `ywc-doc-writer` — dispatch target for ToS/Privacy Policy drafts (draft pending legal review)
- `ywc-security-audit` / `ywc-e2e-test-strategy` — post-implementation security/E2E gates
- `ywc-tech-research` — real-time research routing when stack evidence is insufficient
