# Codex Skill/Agent Evaluation - 2026-08-12 - full sweep

## Verdict

| Field | Value |
|---|---|
| Status | PASS_WITH_ACTIONS |
| Scope | full sweep (`--target all`) |
| Assets evaluated | 58 (50 skills, 8 agents) |
| Gate failures | 0 |
| Lowest grade | A / 3.74 |

## Evidence

- `inventory_gate.py --json`: PASS; 50 skills, 8 agents; no missing locale README, `openai.yaml`, or invalid agent TOML.
- `score.py --mode mechanical --target all --format markdown`: PASS; all judgment axes intentionally completed below.
- `test_workflow_contract.py`: 5 tests passed.
- `runner.py --adapter fake --suite mocked`: PASS.
- Local evaluator distribution-boundary negative checks: PASS.
- Existing 48 assets retain the 2026-07-01 rubric judgments; current mechanical checks show no regression. The 9 newly added skills and 1 new agent were re-read and judged in this pass.

## Scorecards

| Asset | Kind | Grade | Composite | Weakest dimension | Evidence |
|---|---|---:|---:|---|---|
| `ywc-architecture-invariants` | skill | A | 3.74 | S5=2 | Clear anti-triggers, bounded validation/audit modes, references, and Codex metadata; eval coverage is thinner than the rest. |
| `ywc-auth-implement` | skill | A | 4.00 | none | Precise multilingual triggers, explicit security/policy/E2E gates, status contract, references, and eval evidence. |
| `ywc-iac-author` | skill | A | 3.87 | S5=3 | Strong IaC boundaries and validate/plan safety workflow; mechanical fixture evidence is incomplete. |
| `ywc-implement` | skill | A | 4.00 | none | Exact one-item input gate, review/TDD workflow, refusal boundaries, status contract, and eval evidence. |
| `ywc-infra-design` | skill | A | 3.87 | S5=3 | Clear design-before-IaC boundary and downstream handoff; mechanical fixture evidence is incomplete. |
| `ywc-infra-optimize` | skill | A | 3.87 | S5=3 | Explicit SAFE/CAUTION/DANGER classification and no-auto-execute boundary; mechanical fixture evidence is incomplete. |
| `ywc-infra-review` | skill | A | 3.87 | S5=3 | Three-lens review contract, severity/blocking rules, and remediation routing; mechanical fixture evidence is incomplete. |
| `ywc-setup` | skill | A | 4.00 | none | Narrow Codex-only scope, exact JSON output, aliases, rejection rules, and validation. |
| `ywc-wayfinder` | skill | A | 4.00 | none | One-active-ticket invariant, deterministic local map, clear routing boundaries, and validation contract. |
| `ywc-cloud-engineer` | agent | A | 4.00 | none | Precise read-only IaC mission, explicit exclusions, least privilege, bounded status/output contract, and passing smoke evidence. |
| Existing 38 skills with no watch item | skill | A | 4.00 | none | Judgment inherited from 2026-07-01; current gate and mechanical checks remain green. |
| `ywc-agentic`, `ywc-finish-branch`, `ywc-project-docs` | skill | A | 3.92 | S8=3 | Judgment inherited from 2026-07-01; broad workflow/document surfaces remain bounded but warrant monitoring. |
| Existing 7 agents | agent | A | 4.00 | none | Judgment inherited from 2026-07-01; current TOML gate and smoke evidence remain green. |

All dimensions were scored 0–4 using the Codex skill and agent rubrics. The
grouped rows above account for all 58 assets: 50 skills and 8 agents.

## Priority Backlog

1. [Medium] `codex/skills/ywc-architecture-invariants` - add deterministic eval fixture coverage or document why its validation-only behavior is sufficiently covered by the shared contract.
   Evidence: S5=2; mechanical score 50.5/57.0.
   Owner: `ywc-skill-author`
   Re-score target: S5 -> 3 or 4.
2. [Low] `codex/skills/ywc-iac-author`, `ywc-infra-design`, `ywc-infra-optimize`, `ywc-infra-review` - add targeted behavioral fixtures if fixture-backed proof is required for the infrastructure suite.
   Evidence: S5=3; mechanical score 53.75/57.0 each.
   Owner: `ywc-skill-author`
   Re-score target: S5 -> 4.
3. [Low] `ywc-agentic`, `ywc-finish-branch`, `ywc-project-docs` - keep broad-scope boundaries explicit as adjacent skills evolve.
   Evidence: S8=3 from the prior judged pass.
   Owner: `ywc-skill-author`
   Re-score target: S8 -> 4.

## Decisions

- No gate cap applied; all structural gates passed.
- No Claude Code paths were scored as Codex assets.
- `ywc-codex-toolkit-eval` remains local-only under `.codex/skills/`.
- No mechanical baseline update was made.
- Final grades are complete for this sweep; mechanical evidence remains the source for deterministic dimensions.

## Scoreboard Update

- Added: 10 assets (9 skills, 1 agent).
- Improved: 0 claimed from this evaluation alone.
- Regressed: 0.
- Lowest current grade: A / 3.74.
- Next review scope: targeted S5 fixture coverage for architecture/infrastructure skills.
