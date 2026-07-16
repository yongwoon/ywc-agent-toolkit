# Legal Pages Template — ToS / Privacy Policy Draft Structure

Structure for the `Task(subagent_type: ywc-doc-writer)` dispatch (FR-7). This is a template for the draft's section shape, not a substitute for legal review — every output carries the "draft pending legal review" label defined below.

## Mandatory Label

Every generated draft starts with, and this label survives every downstream hand-off:

```text
> **DRAFT PENDING LEGAL REVIEW** — this document has not been reviewed by
> qualified legal counsel and must not be published or relied upon as final.
```

## Terms of Service — Section Shape

1. **Acceptance of Terms** — effective date, consent mechanism (checkbox at sign-up).
2. **Service Description** — what the product does, in plain language.
3. **Account Responsibilities** — credential security, age/eligibility requirements from the policy interview.
4. **Acceptable Use** — abuse-prevention controls referenced from the policy interview (rate limits, prohibited behavior).
5. **Termination** — self-service deletion terms if account deletion was approved in the interview.
6. **Liability and Disclaimers** — placeholder language flagged for legal counsel, not asserted as final.
7. **Governing Law** — placeholder, jurisdiction to be confirmed by legal counsel.
8. **Changes to Terms** — versioning approach matching the consent-versioning answer from the policy interview.

## Privacy Policy — Section Shape

1. **Data Collected** — profile fields from the policy interview, OAuth-provided data if applicable.
2. **How Data Is Used** — authentication, session management, abuse prevention.
3. **Third-Party Sharing** — OAuth provider data flow only if OAuth providers were approved; otherwise `N/A — no third-party sharing`.
4. **Retention and Deletion** — retention policy from the account-deletion policy interview answer.
5. **User Rights** — access, correction, deletion, consent withdrawal (matching the consent-versioning answer).
6. **Security Measures** — high-level statement referencing the recommended library/managed service, without exposing implementation detail that could aid an attacker.
7. **Contact** — placeholder for the project's actual contact channel.
8. **Changes to Policy** — versioning approach matching the consent-versioning answer.

## Sign-Up Consent Checkbox UI Requirements

- A single checkbox (not pre-checked) linking to both the ToS and Privacy Policy drafts.
- Checkbox state and the consent document version are recorded together at sign-up time — this is what makes withdrawal/versioning auditable later.
- The checkbox label text must not imply the linked documents are final — use neutral phrasing ("I agree to the Terms of Service and Privacy Policy") since the "draft pending legal review" label lives in the documents themselves, not the UI copy.

## Handoff Note for the Dispatch Prompt

The `ywc-doc-writer` dispatch prompt in `SKILL.md` references this file implicitly through the section shapes above — the dispatched agent should structure its draft output to match these two section lists and always open with the mandatory label.
