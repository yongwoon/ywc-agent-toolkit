# Auth Security Gate

Before E2E, verify the audit evidence covers identity, session, authorization, recovery, secrets, external callbacks, abuse controls, and data deletion boundaries.

- Prefer established libraries/services; do not prescribe direct password hashing, JWT signing, encryption, or secret crypto.
- Do not output secrets, values from `.env`, tokens, provider credentials, or real test identities.
- Application work reuses `$ywc-code-gen --review` audit evidence. Documentation-only work runs one `$ywc-security-audit --code <changed-auth-path>`.
- Zero Critical and zero High is mandatory before E2E, PR proposal, or recommendation caching.
- Critical or High means `DONE_WITH_CONCERNS`, with E2E/PR/cache skipped until remediation and a new audit.

This is a documentation orchestration gate. Data Integrity hardening is not applicable because it creates no application data mutation.
