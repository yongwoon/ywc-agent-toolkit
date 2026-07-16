---
name: ywc-auth-implement
description: >-
  (ywc) Use when planning a secure application authentication feature, choosing
  an auth library/service from project evidence, or gating auth implementation
  through policy, security audit, and E2E. Triggers: "auth implementation",
  "implement authentication", "로그인 구현", "인증 구현", "OAuth 설정",
  "ywc-auth-implement". Do not use to hand-roll JWT/password/secret crypto,
  implement an application without approved auth policy, or replace a security audit.
---

# ywc-auth-implement

**Announce at start:** "I'm using the ywc-auth-implement skill to turn the authentication intent into a policy-backed, security-gated implementation route."

This skill orchestrates authentication work; it does not write application auth code, prescribe a fixed stack, or expose secrets. Prefer an established library or managed service based on project evidence.

## Rationalization Defense

| Excuse | Reality |
|---|---|
| "It is OAuth-only, so the policy interview can be skipped" | OAuth still has consent, callback, session, recovery, deletion, and abuse decisions. Complete the interview with only selected-method fields. |
| "A short JWT helper is faster" | Do not recommend direct JWT signing, password hashing, or secret crypto. Use an established library/service selected from evidence. |
| "Existing login is close enough to extend" | Existing auth requires the user's explicit `new`, `extend`, or `migrate` choice before dispatch. |
| "The audit has findings, but E2E can run anyway" | Any Critical or High finding ends this route as `DONE_WITH_CONCERNS`; skip E2E, PR proposal, and caching. |
| "This privacy wording is standard" | Legal pages are drafts only and must say `법적 검토 전 임시본`. |

See [rationalization evidence](references/rationalization-evidence.md) for the baseline failures and forward checks behind these rules.

## Scope and Inputs

Accept an auth intent, project path, and any approved policy decisions. Do not assume a framework, provider, database, or credential family. Target-project output follows its language convention; use Korean only when no convention exists.

## Step 1: Read-only Preflight

Inspect project guidance, manifests, framework/database evidence, current branch, `.env.example`, and `.gitignore`. Report only:

- whether `feature/<auth-slug>` exists for reuse and whether a long-lived branch is needed;
- missing placeholder key *names* only—never values—and no change to `.env.example`;
- existing-auth evidence; require `new`, `extend`, or `migrate` if found;
- missing stack evidence, which routes to `$ywc-tech-research`;
- a legal-draft warning: `법적 검토 전 임시본`.

This phase is read-only and rerunnable. Detached HEAD, no establishable Git/base branch, or no clean-tree transition returns `NEEDS_CONTEXT` before mutation. A separately user-authorized branch or placeholder change must be reviewable and leave a clean tree before `$ywc-code-gen`; this skill does not make that change during preflight.

## Step 2: Policy Interview

Run one focused policy round using [policy-interview.md](references/policy-interview.md). It has nine mandatory sections, including for OAuth-only work. For each selected method record the question, response/default, and approved/deferred state. Record unselected methods as approved-policy exclusions; do not request their readiness fields or produce their E2E flows. Never record or output a client secret, access token, or real credential.

Required unresolved policy returns `NEEDS_CONTEXT`.

## Step 3: Evidence-Based Recommendation

Use stack evidence plus approved or explicitly deferred-with-risk decisions to recommend an established library or managed service. There are no fixed stack playbooks or allowlists. When evidence is insufficient, follow [generic-fallback.md](references/generic-fallback.md), invoke `$ywc-tech-research`, and resume only after a decision. A future recommendation cache is eligible only after zero Critical/High audit findings and applicable E2E success.

## Step 4: Plan and Implementation Route

Pass the approved policy and recommendation to `$ywc-plan`. Medium and large work must reach `DONE` in `$ywc-spec-ready`. Then print, but never automatically invoke, this required route:

```text
$ywc-plan → $ywc-spec-ready → $ywc-task-generator → $ywc-code-gen --spec <path> --feature <auth feature> --tdd --review
```

Do not print `$ywc-task-generator` until `$ywc-spec-ready` is `DONE`; never skip decomposition. `$ywc-code-gen` owns application implementation and its critical-path security review. Documentation-only work may use one bounded general subagent with target, oracle, stop condition, evidence required, legal warning when relevant, and [the shared status actions](../references/subagent-status-actions.md). Do not copy that shared contract.

## Step 5: Security Gate

Follow [security-checklist.md](references/security-checklist.md). For application code, consume `$ywc-code-gen --review`'s authoritative `$ywc-security-audit` evidence; do not run a duplicate audit. For documentation-only delegation, run `$ywc-security-audit --code <changed-auth-path>` exactly once.

| Audit result | Transition |
|---|---|
| Zero Critical and High | Continue to applicable E2E. |
| Any Critical or High | `DONE_WITH_CONCERNS`; skip E2E, PR proposal, and cache. Remediate or replan, then re-audit. |
| Command cannot run | `BLOCKED` with command and error evidence. |
| Scope or trust boundary missing | `NEEDS_CONTEXT` with the missing input. |

## Step 6: Policy-Conditioned E2E Gate

After only a clean security gate, run exactly one `$ywc-e2e-test-strategy --init --ci` if Playwright is absent, otherwise exactly one `$ywc-e2e-test-strategy --audit`. Then run one `$ywc-e2e-test-strategy --flow <name>` per approved capability: email/password only if selected, deletion only if enabled, and one per selected OAuth provider. Record excluded flows.

After setup/audit and after every flow, run the configured Playwright package-manager script; if none exists, use `npx playwright test` only when Playwright is installed. Record command, exit code, and result summary. A nonzero test exits `DONE_WITH_CONCERNS` with no cache or PR proposal. An absent server, provider credential, or test environment is `BLOCKED`, except an explicitly deferred non-security item is `DONE_WITH_CONCERNS`.

## Step 7: Optional PR and Completion

Offer `$ywc-create-pr` only after all applicable E2E flows pass and the user opts in. A declined PR is not a failure. Use [workflow transitions](references/workflow-transitions.md) to normalize every stage to one status.

## Output Format

```text
Authentication Implementation Route
Preflight: branch/env/auth/stack evidence
Policy: nine decisions; selected methods and approved exclusions
Recommendation: evidence, library/service, deferred risks
Delegated work: plan/spec/task handoff and worker evidence
Security: command or reused audit evidence; Critical/High counts
E2E: setup/audit, applicable/excluded flows, commands, exit codes
Cache: eligible | not eligible and reason
Next handoff: task-generator printout, remediation, or optional PR
Completion Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
```

Emit exactly one literal completion status. `DONE` requires every applicable non-optional gate. `DONE_WITH_CONCERNS` is only for an explicitly declared non-security deferral or unresolved Critical/High findings with the mandatory skips above.

## References

| Reference | Use |
|---|---|
| [policy-interview.md](references/policy-interview.md) | Nine decision sections and selected-method recording fields. |
| [generic-fallback.md](references/generic-fallback.md) | Evidence is insufficient for a library/service recommendation. |
| [security-checklist.md](references/security-checklist.md) | Auth-boundary review and audit/E2E transition. |
| [legal-pages-template.md](references/legal-pages-template.md) | Draft privacy/terms language is requested. |
| [workflow-transitions.md](references/workflow-transitions.md) | Status and E2E/PR transition detail. |
| [rationalization-evidence.md](references/rationalization-evidence.md) | Routing behavior evidence for downstream evals. |
