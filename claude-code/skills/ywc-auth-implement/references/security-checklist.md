# Security Posture Checklist and E2E Policy Branching

## Pre-Audit Checklist (before calling `ywc-security-audit`)

- [ ] No hand-rolled password hashing, token signing, or secret crypto anywhere in the diff — only the recommended library/managed service.
- [ ] Secrets (API keys, OAuth client secrets, signing keys) are read from environment variables, never hardcoded.
- [ ] `.env.example` contains placeholders only, no real values.
- [ ] Session/token TTL, rotation, and revocation match the approved policy interview answers.
- [ ] Rate limiting is present on sign-in, sign-up, and password-reset endpoints.
- [ ] Password reset tokens are single-use and short-TTL.
- [ ] RBAC role/claims match the approved default and are not client-trusted (server-verified).

## Audit Invocation

```bash
ywc-security-audit --code <auth-diff-path>
```

Map the result via the FR-8 table in `SKILL.md`. This checklist is a pre-check that reduces the chance of a Critical/High finding — it does not replace the audit itself.

## E2E Policy-Branch Execution

1. **Detect config**: `ls playwright.config.* 2>/dev/null`.
   - Absent → run `ywc-e2e-test-strategy --init` once. Inspect the generated flows against the approved interview items before continuing.
   - Present → run `ywc-e2e-test-strategy --audit` to see current coverage.
2. **Fill gaps only**: for each approved item still missing a flow, run `ywc-e2e-test-strategy --flow <name>` once. Do not regenerate flows that already exist and pass.
   - Sign-up/sign-in/reset flow — only if email/password was approved.
   - Account-deletion flow — only if self-service deletion was approved.
   - One OAuth flow per configured provider.
   - MFA enrollment/verification flow — only if MFA was approved (not deferred).
3. **Flow generation is not a pass.** After flows exist, run the project's actual E2E command (discovered from `package.json` scripts, CI workflow, or CLAUDE.md) fresh.
4. **Capture evidence** in `ywc-verify-done` format: exact command, exit code, and the key pass/fail output lines — for each approved flow, not just a suite-level summary.
5. **Missing credentials/test env**: if a provider's test credentials or a required test environment is unavailable, classify as `DONE_WITH_CONCERNS` only when this is non-security and was explicitly deferred by the user during the interview; otherwise the missing-evidence state is `BLOCKED`.

## Cache Eligibility Gate

A stack recommendation becomes cache-eligible (usable as a future playbook) only when both hold:

- The `ywc-security-audit` result is Critical/High = 0.
- The policy-conditional E2E above passed with captured evidence for every approved flow.

Either condition failing means the recommendation stays session-scoped — do not write a new `references/stack-*.md` playbook file.
