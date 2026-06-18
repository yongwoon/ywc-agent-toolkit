# TDD, Deep Module, Gray Box — Shared Reference for Codex/Plugins Executors

> Shared operational reference for Codex and Plugins `ywc-*` generation and execution skills. Use this with [readable-code.md](./readable-code.md), [principles.md](./principles.md), and [confidence-gate.md](./confidence-gate.md). This file keeps the Matt Pocock pitfall 3/4/5 disciplines consistent across `ywc-code-gen`, `ywc-sequential-executor`, and `ywc-parallel-executor`.

## When This Applies

Apply this reference to behavior-changing work: new features, bug fixes, changed public contracts, cross-layer generation, and task execution that alters observable behavior.

Docs-only edits, pure formatting, metadata updates, generated README locale updates, and mechanical/config-only validation changes may use the exception path in [Allowed Exceptions](#allowed-exceptions). Do not invent fake tests for changes with no executable behavior.

## Contract Snapshot

Before implementation, write or confirm the public contract that will be changed.

Include:

- **Changed Public Contracts**: exported functions, endpoints, DTOs, schemas, CLI flags, component props/hooks, event payloads, task worker protocols, or service interfaces.
- **Critical Internals**: auth, authn, authz, session, oauth, jwt, token, password, credential, secret, crypto, encrypt, decrypt, sign/verify, payment, billing, invoice, checkout, finance, ledger, wallet, PII/personal-data handlers, migrations/data-loss, concurrency, external side effects, and external-input boundaries such as webhooks/uploads/deserialization. A project may extend this set via an additive `critical_paths` list in `CLAUDE.md`, for example `critical_paths: ["packages/auth/**", "billing/**"]`.
- **Cross-Module Impact**: callers, workers, tests, generated clients, README/user-facing behavior, or sibling tasks that rely on the same public surface.

Use `N/A` explicitly for layers that are not involved. Missing contracts on a changed public surface are a `NEEDS_CONTEXT` signal, not an invitation to let workers invent incompatible shapes.

## TDD Baseline

For behavior-changing work, create or identify the failing feedback point before finalizing implementation.

- Bug fixes require a regression test that fails for the intended bug before the fix.
- New behavior requires a failing unit, integration, contract, or component behavior test before implementation where the project has a practical test harness. First identify whether an existing regression or behavior test already fails for the intended reason; if it does, record that test and use it as the RED state instead of authoring a duplicate test.
- Implement the smallest change that turns the relevant test green, then refactor after green.
- Never skip, weaken, comment out, or rewrite assertions simply to make the suite pass.

Strict `--tdd` modes may add RED/GREEN/REFACTOR checkpoint commits. The baseline rule still applies when strict mode is not enabled.

## Allowed Exceptions

You may skip the RED state only when the task is:

- docs-only;
- pure formatting;
- metadata or locale README regeneration;
- mechanical rename or validation-only work;
- config-only with no executable behavior;
- blocked by the absence of any practical local test harness;
- explicitly overridden by the user.

Every exception must be reported as `TDD Exception: <reason>`. Prefer real validation commands over fake tests.

## Deep Module Boundary

Design the stable interface before the implementation body.

- Keep the public surface small, explicit, and easy to test.
- Hide implementation details behind the interface; do not expose internal helper shape to callers that do not need it.
- Do not split cohesive behavior into shallow single-use wrappers just to make code look smaller.
- Add abstractions only for real boundaries, meaningful reuse, or complexity reduction. Follow the anti-dogma guidance in [readable-code.md](./readable-code.md).
- When a public contract changes, record it in the Contract Snapshot and verify it with a contract or behavior test where feasible.

## Gray Box Reporting

Use gray-box verification by default: read enough internals to understand risk, but anchor tests and reports on public behavior and stable contracts.

Completion reports should include:

- **Changed Public Contracts**: added/changed interfaces or `N/A`.
- **Contract Tests**: contract/behavior tests authored, touched, or executed.
- **Critical Internals Reviewed**: critical files/modules inspected internally, or `N/A`.
- **Cross-Module Impact**: callers/sibling tasks affected, or `N/A`.
- **TDD Exceptions**: any allowed exception with the reason.

Critical modules are not gray-box-only. Auth, authn/authz, oauth, jwt, token, password, credential, secret/crypto, encrypt/decrypt, sign/verify, payment, billing, invoice, checkout, finance, ledger, wallet, PII/personal-data handlers, migrations/data-loss, concurrency, and external-input boundaries require direct internal review, and should be routed through `ywc-impl-review` or `ywc-security-audit` when the executor's scope requires it. Project-specific `CLAUDE.md` `critical_paths` entries are additive.
