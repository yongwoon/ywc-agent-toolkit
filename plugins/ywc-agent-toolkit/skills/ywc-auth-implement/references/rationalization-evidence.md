# Rationalization Evidence

This record is the forward-test target for the downstream `evals/evals.json` routing suite. It documents prompt-level behavior, not application-code tests.

| Behavior | Baseline failure | Forward check |
|---|---|---|
| OAuth policy | Skip interview because no password is selected | Require all nine sections; scope credential fields to selected methods. |
| Direct crypto | Recommend a hand-written JWT/password helper | Refuse and require established library/service selection from evidence. |
| Existing auth | Continue without migration intent | Return `NEEDS_CONTEXT` until `new`, `extend`, or `migrate` is chosen. |
| Audit gate | Continue to E2E after a High finding | Return `DONE_WITH_CONCERNS`; skip E2E, PR, and cache. |
| Legal draft | Present policy wording as final | Label it `법적 검토 전 임시본`. |

The downstream eval task owns executable fixtures. This file is read-only evidence for that task.
