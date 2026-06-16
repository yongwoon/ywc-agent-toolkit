# ywc-security-audit

A Security Agent Skill for performing security audits when authentication, payment, or personal data-related code changes, or for periodic security reviews.

## Usage

```text
/ywc-security-audit --code api/src/middleware/
```

## Audit Checklist (OWASP Top 10)

1. Injection (SQL, Command, LDAP)
2. Broken Authentication (Token, Session)
3. Sensitive Data Exposure
4. XSS (Reflected, Stored, DOM)
5. Broken Access Control
6. Security Misconfiguration
7. SSRF
8. Input Validation
9. Rate Limiting
10. Timing Attacks

## Execution Agent

- **Security Agent** (claude-opus-4-20250514)

## Recommended Scenarios

- When modifying middleware/ (authentication/authorization logic)
- When adding or modifying API Endpoints that accept external input
- Periodic security reviews (e.g., monthly)

## Output Format

Classified by severity: Critical / High / Medium / Low. Each finding includes file:line, risk description, and recommended fix.

## Triggering

Trigger conditions for this Skill are defined in the `description` field of [SKILL.md](./SKILL.md).

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
