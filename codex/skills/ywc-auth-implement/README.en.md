# ywc-auth-implement

A Codex orchestration skill for turning authentication intent into a policy-backed, security-gated implementation route. It does not expose secrets or recommend hand-rolled JWT, password, or secret crypto.

## Localized Versions

- [한국어 (entry)](./README.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)
- [中文](./README.zh.md)
- [Español](./README.es.md)

## When to Use

- Planning login, OAuth, sessions, or account deletion
- Deciding whether existing authentication is `new`, `extend`, or `migrate`
- Selecting an established auth library or managed service from project evidence

## Invocation

```text
$ywc-auth-implement
```

The skill performs a read-only preflight, a nine-section policy interview, and an evidence-based recommendation. It only prints the route below — never invokes it — and only after `$ywc-spec-ready` reaches `DONE` for medium/large work:

```text
$ywc-plan → $ywc-spec-ready → $ywc-task-generator → $ywc-code-gen --spec <path> --feature <auth feature> --tdd --review
```

Critical/High audit findings skip E2E, PR proposal, and caching, and the route ends as `DONE_WITH_CONCERNS` until remediation and a fresh audit clear it. Legal wording is always marked `법적 검토 전 임시본`.
