---
name: ywc-auth-implement
description: >-
  (ywc) Use when implementing authentication features (email/password, OAuth, MFA, shallow RBAC) — runs a policy interview, detects the stack, recommends battle-tested libraries, then dispatches implementation to ywc-backend-coder/ywc-frontend-coder under TDD discipline and legal-page drafts to ywc-doc-writer. Triggers: "인증 구현", "로그인 기능", "OAuth 연동", "implement auth", "add login", "set up authentication", "認証実装", "ログイン機能", "ywc-auth-implement". Do not use for security code review after implementation (use ywc-security-audit), general feature planning unrelated to auth (use ywc-plan), or E2E test authoring outside auth flows (use ywc-e2e-test-strategy).
category: spec
phase: planning
requires: []
advisor_budget: 2
---

# ywc-auth-implement

**Announce at start:** "I'm using the ywc-auth-implement skill to run the auth policy interview and dispatch a battle-tested implementation."

Authentication (email/password, OAuth, MFA, shallow RBAC) is high-stakes and slow to get right, even for experienced developers. This skill standardizes the flow: a focused policy interview, stack detection, a dynamic battle-tested library/managed-service recommendation, and dispatch of the actual implementation to existing Claude Code named agents (`ywc-backend-coder`, `ywc-frontend-coder`, `ywc-doc-writer`). This skill never writes application auth code itself — it interviews, recommends, and dispatches.

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "Only OAuth is needed, skip the full interview" | Session handling, RBAC defaults, and abuse-prevention controls apply regardless of the primary sign-in method. Run all 9 interview categories; unrelated ones close fast with an explicit "not applicable" answer, but skipping them silently misses cross-cutting decisions (session TTL, rate-limiting) that OAuth-only flows still need. |
| "A hand-rolled JWT/password-hashing implementation would be faster" | Hand-rolled crypto is the single most common root cause of auth vulnerabilities (timing attacks, weak KDF parameters, algorithm confusion). Always recommend a battle-tested library or managed service — never hand-rolled password hashing, token signing, or secret handling. |
| "MFA can be added in a follow-up task" | Deferring MFA is a valid outcome only when the user explicitly defers it during the policy interview with the risk stated back to them. Silently dropping it from the plan is not deferral, it is scope loss. |
| "Security audit passed on the previous run, cache the recommendation now" | Caching eligibility is gated on E2E passing too, not audit alone (FR-5/FR-8). A Critical/High-clean audit with E2E still pending is `DONE_WITH_CONCERNS`, not cache-eligible. |
| "The legal draft reads complete, present it as final" | Every ToS/Privacy Policy draft from `ywc-doc-writer` carries a "draft pending legal review" label for its entire lifetime in this flow — there is no state where this skill presents it as final. |
| "Just list the frameworks this skill supports so recommendations are consistent" | The spec explicitly forbids a fixed or "supported" stack list (AC5) — v1 ships zero stack playbooks and grows them only from audited, E2E-passed recommendations. A hardcoded list becomes stale and blocks legitimate stacks outside it. |

**Violating the letter of these rules is violating the spirit.** An auth flow that skips interview categories, invents crypto, or caches before the security/E2E gates pass hands the user a plausible-looking but unverified implementation.

## Preflight Gate

Run before any interview question, in order, and re-runnable safely (idempotent):

1. **Branch reuse** — if `feature/<auth-slug>` already exists, reuse it; only create a new branch when starting from a long-lived branch (main/develop).
2. **`.env.example` placeholders** — add only missing secret placeholders (never overwrite existing values or expose real secrets).
3. **Stack evidence routing** — if framework/DB evidence is insufficient, route to `ywc-tech-research` before asking any policy question; resume once evidence is available.
4. **Existing-auth hard stop** — if existing auth is detected, return `NEEDS_CONTEXT` until the user picks `new` / `extend` / `migrate`; no scaffolding or subagent dispatch happens before that choice.
5. **Legal draft labeling** — any generated ToS/Privacy Policy draft is always labeled "draft pending legal review", from first generation through hand-off.

## Policy Interview (9 categories)

Ask all 9 categories in one focused round: sign-in method + OAuth provider readiness, MFA enrollment/recovery, session storage/TTL/rotation/revocation, password reset & hashing library boundary, profile fields, account-deletion re-authentication, shallow-RBAC roles/defaults/claims, consent versioning/collection/withdrawal, and abuse-prevention (rate limiting, verification, recovery controls). Record each answer as question / response-default / approval-deferral state.

> **Action required**: Read [references/policy-interview.md](references/policy-interview.md) for the full per-category question set and recording format before running the interview.

Application-facing question and output language follows the target project's resolved language, not a hardcoded assumption.

> **Action required**: Read [../references/language-resolution.md](../references/language-resolution.md) for the resolution chain.

## Dynamic Recommendation

Recommend battle-tested libraries or managed services using only stack evidence plus approved (or explicitly risk-accepted) policy answers — never a fixed "supported stack" list. When evidence is insufficient, fall back to real-time research (GitHub search, Context7/vendor docs, package registries) and route to `ywc-tech-research`. A new stack playbook becomes cache-eligible only after this skill's own `ywc-security-audit` pass finds zero Critical/High and the policy-conditional E2E in FR-8 below passes.

> **Action required**: Read [references/generic-fallback.md](references/generic-fallback.md) for the fallback research procedure and playbook-caching mechanics.

## Implementation Dispatch

Dispatch, do not implement. Each direct-dispatch prompt below instructs the agent to follow the `ywc-tdd-ritual` cycle and to run `ywc-verify-done` before claiming completion. `ywc-tdd-ritual` is a discipline the dispatched agent follows, not a nested dispatcher this skill calls.

> **Action required**: Read [../references/subagent-status-actions.md](../references/subagent-status-actions.md) — every dispatch below must apply its §3.5 Return-payload contract verbatim.

### Backend implementation — `Task(subagent_type: ywc-backend-coder)`

```text
Task(subagent_type: ywc-backend-coder)

Implement the backend half of the approved auth policy and recommendation (see
attached policy interview summary and library/service recommendation). Follow
the ywc-tdd-ritual discipline: write a failing test first (RED), verify it
fails for the right reason, implement the minimal code to make it pass
(GREEN), verify it passes, then refactor while keeping tests green (REFACTOR),
verifying again after the refactor. Never hand-roll password hashing, token
signing, or secret crypto — use the recommended library/service exactly as
specified. Before claiming completion, run ywc-verify-done and attach its
evidence trail (command, exit code, key output) for each behavior implemented.

Return-payload contract: Reply with `Status | 1-line summary | artifact paths
| (Concerns ≤ 10 lines | Blocker ≤ 5 lines | Missing-context bullets)`. Do not
return generated code, full findings, full diffs, restated prompt content, or
chain-of-thought. Write those to files and return the paths. The orchestrator
will read the files only when it needs to.
```

### Frontend implementation — `Task(subagent_type: ywc-frontend-coder)`

```text
Task(subagent_type: ywc-frontend-coder)

Implement the frontend half of the approved auth policy and recommendation
(sign-in/sign-up forms, MFA enrollment UI, session-aware routing, consent
checkbox per the FR-7 legal draft). Follow the ywc-tdd-ritual discipline: RED
(failing test first) -> Verify RED -> GREEN (minimal implementation) -> Verify
GREEN -> REFACTOR -> Verify GREEN. Never implement client-side secret
handling or bypass the backend's session/token contract. Before claiming
completion, run ywc-verify-done and attach its evidence trail for each
behavior implemented.

Return-payload contract: Reply with `Status | 1-line summary | artifact paths
| (Concerns ≤ 10 lines | Blocker ≤ 5 lines | Missing-context bullets)`. Do not
return generated code, full findings, full diffs, restated prompt content, or
chain-of-thought. Write those to files and return the paths. The orchestrator
will read the files only when it needs to.
```

### Legal page drafting — `Task(subagent_type: ywc-doc-writer)`

```text
Task(subagent_type: ywc-doc-writer)

Draft a Terms of Service and Privacy Policy covering the approved auth policy
(data collected, consent version, retention on account deletion, third-party
OAuth data sharing where applicable), plus the sign-up screen's consent
checkbox UI requirements. Label the ToS/Privacy Policy draft "draft pending
legal review" in its title and at the top of the document body — this label
must survive into every downstream hand-off; never present the draft as
final or legally reviewed.

Return-payload contract: Reply with `Status | 1-line summary | artifact paths
| (Concerns ≤ 10 lines | Blocker ≤ 5 lines | Missing-context bullets)`. Do not
return generated code, full findings, full diffs, restated prompt content, or
chain-of-thought. Write those to files and return the paths. The orchestrator
will read the files only when it needs to.
```

## Security, E2E, and PR Gates

Before running the security audit, apply the shared subagent-status contract to every dispatch result from the Implementation Dispatch step above: `DONE` integrates as-is; `DONE_WITH_CONCERNS` requires resolving the stated correctness/scope concerns before integration; `NEEDS_CONTEXT` requires re-dispatching with the missing context supplied; `BLOCKED` requires triaging the blocker before continuing. Only proceed to the audit once every dispatched subagent's result is resolved to a clean integration state.

After implementation, run `ywc-security-audit --code <auth-diff-path>`. `ywc-security-audit` is a skill call (not a §3.5 direct-dispatch target), so this skill maps its severity result to a Completion Status directly:

| Audit result | Route | Cache |
|---|---|---|
| Critical/High = 0 | Proceed to policy-conditional E2E below | Pending — eligible only after E2E passes |
| Critical/High ≥ 1 | `DONE_WITH_CONCERNS`; skip E2E, PR suggestion, and caching entirely; remediate and re-audit | Not eligible |
| Audit command fails to run | `BLOCKED` with the command and error evidence | Not eligible |
| Scope/trust boundary insufficient | `NEEDS_CONTEXT` naming the missing item | Not eligible |

E2E covers only interview-approved items (sign-up/sign-in/reset only if email/password was chosen, account deletion only if enabled, one flow per configured OAuth provider, and MFA enrollment/verification only if MFA was approved and not deferred). Check `playwright.config.*` first: absent → run `ywc-e2e-test-strategy --init` once and inspect the generated flows; present → run `--audit` for current coverage. Either way, run `--flow <name>` only for the approved flows still missing — flow generation is never itself a pass. Run the project's actual E2E command fresh and capture `ywc-verify-done`-style evidence (command, exit code, key output) before claiming a pass. Missing provider credentials or test environment is `DONE_WITH_CONCERNS` only when it is non-security and the user explicitly deferred it; otherwise `BLOCKED`. Only after these gates pass, propose `ywc-create-pr` non-blockingly — never invoke it automatically.

> **Action required**: Read [references/security-checklist.md](references/security-checklist.md) for the full security posture checklist and the detailed E2E policy-branch execution steps.

## Output Format

```text
## Preflight
<branch reuse | env placeholders | stack routing | existing-auth decision | legal draft label>

## Policy Interview Summary
<9-category recap: question / response-default / approval-deferral state>

## Recommendation
<library/service + evidence, or ywc-tech-research routing>

## Dispatched Subagents
- ywc-backend-coder: <Status | summary>
- ywc-frontend-coder: <Status | summary>
- ywc-doc-writer: <Status | summary>

## Security / E2E Gate
<ywc-security-audit result -> route taken; E2E command + evidence if run>

## Completion Status
DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
```

## References

| Reference | Use when |
|---|---|
| [references/policy-interview.md](references/policy-interview.md) | Running the 9-category policy interview |
| [references/security-checklist.md](references/security-checklist.md) | Running the FR-8 security posture checklist and E2E policy branching |
| [references/generic-fallback.md](references/generic-fallback.md) | Stack evidence is insufficient for a direct recommendation |
| [references/legal-pages-template.md](references/legal-pages-template.md) | Structuring the `ywc-doc-writer` ToS/Privacy Policy dispatch |
| [references/rationalization-evidence.md](references/rationalization-evidence.md) | Backing evidence for each Rationalization Defense row |

## Integration

- **Upstream**: direct user invocation when an auth feature is requested; `ywc-plan` / `ywc-spec-ready` consume this skill's approved policy and recommendation for Medium/Large auth features.
- **Downstream**: `Task(subagent_type: ywc-backend-coder\|ywc-frontend-coder)` for implementation, `Task(subagent_type: ywc-doc-writer)` for legal pages, `ywc-security-audit` and `ywc-e2e-test-strategy` for the delivery gates, `ywc-create-pr` for the non-blocking PR suggestion.
- **Must not be paired with**: implementing application auth code directly in this skill's own context — that always routes through the named-agent dispatches above.
