# Auth Security Gate

Before E2E, verify the audit evidence covers identity, session, authorization, recovery, secrets, external callbacks, abuse controls, and data deletion boundaries.

- Prefer established libraries/services; do not prescribe direct password hashing, JWT signing, encryption, or secret crypto.
- Do not output secrets, values from `.env`, tokens, provider credentials, or real test identities.
- Application work reuses `$ywc-code-gen --review` audit evidence. Documentation-only work runs one `$ywc-security-audit --code <changed-auth-path>`.
- Zero Critical and zero High is mandatory before E2E, PR proposal, or recommendation caching.
- Critical or High means `DONE_WITH_CONCERNS`, with E2E/PR/cache skipped until remediation and a new audit.

This orchestration document itself creates no application data mutation, so Data Integrity hardening is not applicable to it directly. The delegated `$ywc-code-gen`/backend implementation work this skill dispatches does mutate user, session, recovery, consent, and deletion data plus schema/transaction boundaries — that work must pass Data Integrity checks before E2E, per `$ywc-code-gen --review`'s audit evidence.
