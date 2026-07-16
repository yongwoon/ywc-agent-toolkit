# Policy Interview — 9 Categories

Ask all 9 categories in a single focused round (not one round-trip per category). For each category, record three things: the question asked, the response default offered when the user has no strong preference, and whether the answer is approved or explicitly deferred (with the stated risk).

## Sign-in Method and OAuth Provider Readiness

- Question: which sign-in methods are needed — email/password, OAuth (which providers), or both?
- Response default: email/password only, added OAuth providers on explicit request.
- For each OAuth provider requested, confirm the provider is registered (client ID/secret available) and the redirect URI is ready. An unregistered provider blocks that provider's dispatch, not the whole flow.
- Edge case: a provider outside the interview's candidate list is accepted via free-text response ("other") — no special branch needed.

## MFA Enrollment and Recovery

- Question: is MFA required at launch, optional/opt-in, or deferred?
- Response default: optional/opt-in (TOTP-based) unless the project's compliance posture requires mandatory MFA.
- If deferred, record the explicit risk stated back to the user (accounts are single-factor until a follow-up task).
- Recovery: confirm backup-code or recovery-email flow before marking MFA "approved".

## Session Storage, TTL, Rotation, Revocation, Device Management

- Question: server-side session store or stateless token (JWT)? What TTL? Rotation on privilege change? Explicit revocation (logout-everywhere)? Device/session listing needed?
- Response default: server-side session with short-lived access token + rotating refresh token, revocable per-session.
- Record the TTL values and rotation trigger explicitly — these feed the backend dispatch prompt.

## Password Reset and Hashing Library Boundary

- Question: which password hashing library/managed service handles password storage? What is the reset-token TTL and single-use behavior?
- Response default: a battle-tested library appropriate to the detected stack (never hand-rolled) with a single-use, short-TTL reset token.
- This category never lets the user request a custom hashing scheme — redirect to library selection instead (Rationalization Defense row 2).

## Profile Fields

- Question: which profile fields are collected at sign-up vs. later (name, avatar, locale, marketing opt-in, etc.)?
- Response default: minimal at sign-up (email + password/OAuth identity only), everything else deferred to a post-sign-up profile step.

## Account Deletion and Re-authentication

- Question: is self-service account deletion in scope? If so, is re-authentication required immediately before deletion? What is the data retention policy after deletion?
- Response default: self-service deletion enabled, re-authentication required, retention per the project's existing data-retention policy (or a stated default if none exists).

## Shallow RBAC — Roles, Defaults, Claims

- Question: what roles exist (e.g., `user`, `admin`)? What is the default role on sign-up? Are roles carried as session/JWT claims?
- Response default: two roles (`user` default, `admin` manually promoted), role carried as a session/JWT claim.
- Reminder: this is shallow RBAC only — a `role` column plus default plus claim propagation. A full policy-matrix engine is out of scope (spec Out of Scope).

## Consent Versioning, Collection, Withdrawal

- Question: what consent is collected at sign-up (ToS, Privacy Policy, marketing)? Is consent versioned? Can it be withdrawn later?
- Response default: ToS + Privacy Policy consent required at sign-up, versioned by document date, withdrawal handled via account settings (marketing consent only — ToS/Privacy Policy withdrawal implies account closure).
- This category's output feeds the `ywc-doc-writer` dispatch (FR-7) directly.

## Abuse Prevention — Rate Limiting, Verification, Recovery Controls

- Question: what rate limits apply to sign-up/sign-in/reset attempts? Is email verification required before first sign-in? What account-recovery controls exist (lockout, CAPTCHA, alerting)?
- Response default: per-IP and per-account rate limiting on sign-in/reset attempts, email verification required before first sign-in, temporary lockout after repeated failures (no CAPTCHA unless the project already uses one).

## Recording Format

Record every category as:

```text
### <category>
- Question: <what was asked>
- Response: <what the user answered, or "default accepted">
- State: approved | deferred (risk: <stated risk>)
```

This record is what the SKILL.md "Policy Interview Summary" output section condenses to one line per category, and what the implementation dispatch prompts (FR-6/FR-7) reference as "the approved auth policy".
