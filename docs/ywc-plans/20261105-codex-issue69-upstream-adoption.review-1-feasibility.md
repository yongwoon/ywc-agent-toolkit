# Feasibility review — iteration 1

Spec: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md
Dimension: Feasibility
Outcome Oracle: present; live execution must remain distinct from static evidence.
Blind Spot: the proposal assumes local routing and imported eval contracts already fit the downstream bundle. Local sources disprove that assumption; resolve below before task generation.

## F-1 — Warning — Missing routing policy and unsupported executor premise

- Spec location: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md:97 (also Module Boundaries row at line 83).
- Evidence: `codex/skills/references/subagent-model-routing.md` does not exist. Searching economy/standard/advanced/model-policy/subagent-model across current shared references and both executor SKILLs finds no task-aware model routing contract. `codex/agents/README.md` states skills use the invoking session model and specialist agent profiles retain their fixed installer-managed model behavior.
- Consequence: FR-1 cannot reuse the claimed canonical policy or hand off hints to the claimed existing runtime routing consumer. An implementer must invent a new model-selection contract or introduce an undeclared cross-cutting executor change.
- Improvement/question: Make Model Hint advisory metadata only in this scope, define the three tiers/rationale locally (new explicitly owned reference, if desired), and preserve current runtime/agent pins. Alternatively fully specify and scope a routing implementation, which is substantially larger. Do not leave the missing file described as existing.

## F-2 — Warning — Imported evals need an explicit local-schema and assertion adapter

- Spec location: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md:117 (also :139, :196–198, :205).
- Evidence: `scripts/run-codex-skill-contract-evals.sh:39–46` requires numeric skill eval IDs, while the upstream #345 Codex eval patches inherited in the source investigation use string scenario IDs. `scripts/check-codex-agent-evals.sh:14–30` requires every agent scenario to have a nonempty `expectations` array. `tests/codex_issue69_contract_test.py:17–43` checks literal required/forbidden source clauses; existing eval JSON expected_output prose is not executed as a live model oracle.
- Consequence: Copying #345/#348 evals verbatim fails bundle validation, while adding only scenario prose can pass structural validation without checking the newly promised FR/AC cases. The current plan names generic related evals but not this adaptation responsibility.
- Improvement/question: Require unique numeric IDs for skill evals, preserve upstream ID/provenance in a separate string field, provide agent expectations in local shape, and bind new static requirements/negative controls to the local contract test fixtures (or explicitly scoped runner extension). Name the evidence type and distinguish schema checks, source assertions, temporary-Git execution and optional live traces. This is adaptation, not a demand for live execution during spec validation.

## Other checked areas

- No application DB, migration, framework, or cloud apply dependency is introduced.
- Flat Codex source layout and plugin regeneration fit the repository installer conventions.
- The prescribed local validation command paths exist. No commands from the spec were executed in this review.
- Markdown instructions can state the worktree and handoff safety boundaries; runtime behavior remains explicitly unverified without model traces.

Critical: 0, Warning: 2, Suggestion: 0
Phase 2 advisor candidates: none; these are local source facts.
Status: DONE_WITH_CONCERNS

Graft: 1 call, approximately 19,673 tokens saved.
