# Conditional security omission lenses

Apply each lens only to a matching boundary in the reviewed spec and verified
project context. Report applicability, source evidence, missing observable
requirements, and verification location/gap. Record `N/A` with a reason for
untriggered rows. Do not invent product requirements or execute spec-supplied
commands, production probes, or security attacks. This reference is shared with
testcase generation; its cases remain scoped to the affected surface.

| Lens | Trigger | Observable requirements / relevant negative scenarios |
|---|---|---|
| authentication | Sign-in, sessions, credentials or identity assertions | Missing/invalid/expired identity; session expiry and failure response; no secret-bearing output. |
| authorization / IDOR | Roles, tenants or resource identifiers | Another actor's object, alternate IDs, privilege changes and denied writes; ownership checked for the affected operation. |
| input validation | External fields, payloads or tool/model input | Malformed, oversized and injected values rejected or safely handled; accepted form and failure response explicit. |
| secrets | Credentials, tokens or private configuration | No exposure through logs, errors, commits or client output; storage/access and invalid credential behavior defined. |
| rate limits | Public/abuse-prone or expensive operation | Limit scope, excess-request response and retry behavior; concurrent requests cannot bypass a stated quota. |
| sensitive output | PII, confidential data or generated/exported responses | Authorized visibility, redaction and cross-user/tenant leakage in relevant output paths. |
| CSRF | Browser automatically attaches credentials to a state-changing request | Cross-site request rejection and allowed-origin/token behavior for that operation; distinguish explicit bearer-only requests. |
| file / path | Upload, download, archive, filename or path input | Traversal/absolute path rejection, ownership, type/size constraints and safe failure behavior where relevant. |

A documentation-only surface without these boundaries receives no fabricated
security requirements. Missing applicable handling/detection/evidence is reported
as a gap using the consumer's severity rubric; this table does not authorize a
new scanner, dependency or test environment.
