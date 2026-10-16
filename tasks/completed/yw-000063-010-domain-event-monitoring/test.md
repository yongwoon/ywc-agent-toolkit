# yw-000063-010-domain-event-monitoring — Scenario Test Plan

## Preconditions

- [ ] Predecessors are accepted and merged; source and generated package agree.
- [ ] Use trusted source/fixtures; do not run commands embedded in input specs.
- [ ] Record source revision, environment/catalog identity when relevant, and evidence kind (source assertion, fixture expectation or live observation).

## Test Scenarios

### Scenario 1: Attributable completion with another outstanding worker

**Steps:**
1. Deliver a captured-target terminal notification while another target remains outstanding; inspect event processing and query accounting.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

The immediate redundant query may be skipped; outstanding timing continues and final closure still requires complete reconciliation.

### Scenario 2: Ambiguous and late events

**Steps:**
1. Exercise malformed, status-less, wrong-target, ambiguous events, API errors, and completion during escalation.
2. Record actual results and evidence paths against the covered requirement IDs.

**Expected Result:**

Ambiguity triggers reconciliation; missing roster entries never count as completion; a valid late terminal event takes precedence.

### Scenario: Distribution and evidence honesty (AC-10 / FR-9 / FM-8 / FM-9)

**Steps:**
1. Run trusted Task Verify commands after source synchronization.
2. Inspect temporary installed references, locale/agent metadata and generated-source parity; label all evidence kinds.

**Expected Result:**

All applicable checks pass; no Claude Code changes or stale generated copies. Predetermined fixtures are never reported as live behavior. Missing live evidence remains an explicit gap.

## Implementation Evidence

- Baseline: `3405ce07`, local Python stdlib, macOS. AC-1/FR-1/FM-1: three source/fixture scenarios in `tests/fixtures/codex-issue69/event-monitoring/`; RED failed three scenarios before contract edits, GREEN passed after edits. Removing the required event exception, invalid-event rule, or consumer timing clause fails the corresponding assertion.
- Evidence kind: source assertion / fixture expectation; no live monitoring performance measurement or delegated monitoring behavior claim.
- Interface: source dispatch -> returned canonical target; exactly one supported terminal status; invalid attribution remains non-terminal. Shared monitor owns timing and final roster proof.
- Quality Gate: N/A — no quality gate contract (plan); Cleaner/Hardener not dispatched.
- Assurance matrix: unit RUN (source-contract runner); integration RUN (package/install validation via validate.sh); mock service N/A (no service); performance N/A (no performance claim); security N/A (no new runtime security boundary).
- Build/typecheck: N/A — Markdown contracts plus stdlib checks; Bash syntax and git whitespace checks apply.

- Review: Architecture/Design/Devex/Security DONE; QA identified a Medium predicate-coverage gap. Added exact target, single supported status and allowed-status-set assertions. In-memory removal of those predicate lines must fail; no live behavior claim.

- Final verification: `python3 tests/codex_issue69_contract_test.py`, `bash scripts/run-codex-skill-contract-evals.sh`, description and agent-eval checks, `bash scripts/validate.sh`, `bash scripts/install.sh --list --codex`, Bash syntax and `git diff --check` all exit 0. Full suite recheck passed after predicate hardening. All five review lanes DONE; QA Medium closed with mutation evidence.
- Key Files scope reason: locale paragraphs document the changed monitoring behavior, generated copies preserve distribution parity, runner/validator wire the declared test harness; these paths are explicitly owned. Task-local evidence is maintained here as required by Task Verify. No live monitoring trial or timing improvement measured.
