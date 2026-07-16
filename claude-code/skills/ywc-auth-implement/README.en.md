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

## Related Skills

- `ywc-backend-coder` / `ywc-frontend-coder` — implementation dispatch targets under TDD discipline
- `ywc-doc-writer` — dispatch target for ToS/Privacy Policy drafts (draft pending legal review)
- `ywc-security-audit` / `ywc-e2e-test-strategy` — post-implementation security/E2E gates
- `ywc-tech-research` — real-time research routing when stack evidence is insufficient
