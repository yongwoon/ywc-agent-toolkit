# Workflow Transitions

| Stage | Success transition | Stop or concern transition |
|---|---|---|
| Preflight | Policy interview | Existing-auth choice or Git state missing → `NEEDS_CONTEXT` |
| Policy | Recommendation | Required decision unresolved → `NEEDS_CONTEXT` |
| Recommendation | Plan → spec-ready → printed task-generator | Research inconclusive → `BLOCKED` or `NEEDS_CONTEXT` |
| Delegation | Security audit | Worker result follows shared `../references/subagent-status-actions.md` |
| Security audit | Applicable E2E | Critical/High → `DONE_WITH_CONCERNS`, skip E2E/PR/cache |
| E2E | Optional PR | Missing security prerequisite → `BLOCKED`; test failure → `DONE_WITH_CONCERNS` |
| PR proposal | Completion | User decline is not a failure |

Only `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, and `NEEDS_CONTEXT` are terminal status values. Emit one.
