# Codex Evaluation S5 Hardening

> Status: Draft
> Scale: Medium
> Created: 2026-08-12
> Author: Codex
> Spec Reference: [Codex evaluation report](../skill-agent-eval/codex/2026-08-12-full-sweep.md)

## Global Constraints

- Codex distributable skills live under `codex/skills/`; the evaluator remains local under `.codex/skills/`.
- Codex `SKILL.md` frontmatter contains only `name` and `description`.
- Required pre-PR verification is `bash scripts/validate.sh`; targeted evaluator checks must also pass.
- Do not add a dependency when the existing Python standard-library evaluator harness is sufficient.
- No mechanical baseline update is allowed unless explicitly reviewed and requested.

## Purpose

Raise the weakest Codex evaluation dimensions from the 2026-08-12 full sweep by adding deterministic behavioral evidence for the architecture and infrastructure skill family. Preserve the existing evaluator boundary and make the backlog measurable on the next scorecard run.

## Scope

- Add focused evaluator fixtures or equivalent deterministic contract coverage for:
  - `ywc-architecture-invariants`
  - `ywc-iac-author`
  - `ywc-infra-design`
  - `ywc-infra-optimize`
  - `ywc-infra-review`
- Reuse the existing evaluator fixture schema, verifier registry, fake runner, inventory gate, and score script.
- Cover the high-value safety boundaries already stated by those skills: no arbitrary execution, design-before-authoring, no auto-apply, three-lens review, and SAFE/CAUTION/DANGER routing.
- Re-run the full Codex evaluation and update the judgment report/scoreboard with evidence-backed deltas.

## Out of Scope

- Rewriting the five skills' workflows unless a fixture exposes a real contract defect.
- Adding a new test framework, external package, live model/API evaluation, or cloud credentials.
- Implementing infrastructure changes or running Terraform against live infrastructure.
- Changing `evals/history.mechanical.json` without explicit baseline review.
- Raising the three existing S8 watch items (`ywc-agentic`, `ywc-finish-branch`, `ywc-project-docs`); keep that as a separate low-priority pass.

## Existing Constraints Touched

| Existing artifact | Behavior verified from the file | New work's interaction |
|---|---|---|
| `.codex/skills/ywc-codex-toolkit-eval/evals/evals.json:1-61` | The local evaluator's current V1 contract tests mechanical mode, full-cycle backlog behavior, and CI regression behavior. | Preserve these cases; add coverage in the existing fixture surface rather than replacing them. |
| `.codex/skills/ywc-codex-toolkit-eval/scripts/fixture_validator.py:1-215` | V2 fixtures are JSON-only, reject execution fields, and support bounded stdout/stderr/file/JSON/verifier checks. | Use only supported fixture fields and extend the validator only if a required assertion cannot be expressed safely. |
| `.codex/skills/ywc-codex-toolkit-eval/scripts/runner.py:1-210` | The fake runner isolates workspaces, installs target/dependency skills, detects undeclared writes, and runs registry-owned verifiers only. | Reuse isolation and write-boundary checks; do not add an ad-hoc executor. |
| `codex/skills/ywc-architecture-invariants/SKILL.md:15-27` | Architecture validation is bounded, validation-only in v1, and never executes verifier data from the skill input. | Add valid/invalid/no-manifest evidence proving these boundaries. |
| `codex/skills/ywc-iac-author/SKILL.md:41-87` | IaC authoring requires design input or explicit clarification, stops at validate/plan, and recommends review before apply. | Add missing-input, no-apply, and review-handoff assertions. |
| `codex/skills/ywc-infra-design/SKILL.md:18-33,77-85` | Design precedes IaC and records reliability/cost/security checks in `infra-design.md`. | Add design-only and handoff assertions. |
| `codex/skills/ywc-infra-optimize/SKILL.md:18,72-90` | Optimization classifies findings and routes remediation to authoring; it does not apply changes. | Add SAFE/CAUTION/DANGER and no-apply assertions. |
| `codex/skills/ywc-infra-review/SKILL.md:18,63-93` | Review always runs security, cost, and reliability lenses and blocks on Critical/High findings. | Add three-lens and blocking recommendation assertions. |

## Acceptance Criteria

- [ ] **AC1 — Architecture evidence:** At least one valid, one malformed/unsafe, and one no-manifest case for `ywc-architecture-invariants` validate through the existing fixture contract; unsafe verifier input never executes.
- [ ] **AC2 — IaC author safety:** A fixture with missing design evidence produces clarification/`NEEDS_CONTEXT`; a successful-path fixture proves `terraform apply` is not invoked and the review handoff is present.
- [ ] **AC3 — Infrastructure design boundary:** A fixture proves `ywc-infra-design` produces a design artifact/handoff and does not author Terraform in the same pass.
- [ ] **AC4 — Optimization routing:** Fixtures cover at least one SAFE, CAUTION, and DANGER classification and prove that remediation routes to `ywc-iac-author` without auto-execution.
- [ ] **AC5 — Review completeness:** A review fixture proves all three lenses are required and a Critical/High finding yields an explicit BLOCK recommendation.
- [ ] **AC6 — Schema and safety:** All new fixtures pass `fixture_validator.py`; no fixture contains forbidden execution fields, secrets, live credentials, or paths outside its fixture root.
- [ ] **AC7 — Regression:** `test_workflow_contract.py`, targeted fixture tests, `runner.py --adapter fake --suite mocked`, `scripts/validate.sh`, and the full mechanical scorer pass.
- [ ] **AC8 — Score movement:** The next scorecard reports `ywc-architecture-invariants` at S5 ≥ 3 and each infrastructure skill at S5 ≥ 4, or records a concrete reason why the existing fixture model cannot prove the remaining behavior.

## Functional Requirements

### FR-1: Extend existing fixture coverage

Add the smallest number of fixtures needed to cover the acceptance criteria. Prefer one fixture per distinct safety boundary over broad prose-only fixtures. Keep target skill and dependencies explicit so inventory diagnostics can resolve them deterministically.

### FR-2: Preserve evaluator trust boundaries

All checks must run through the existing fake/isolated harness. Fixture data may describe commands or expected output only through the schema's allowed assertion fields; it must not introduce `argv`, shell, environment, network, timeout, or arbitrary executable fields.

### FR-3: Keep skill contracts authoritative

Fixtures test the current `SKILL.md` output and safety contracts. If a fixture fails because the skill contract is ambiguous or unsafe, make the smallest skill correction at the owning skill, then add the regression fixture. Do not weaken the expected assertion to make a failing behavior pass.

### FR-4: Re-score and document

Run inventory and mechanical scoring after fixture changes, then update the Codex evaluation report with per-dimension evidence and the scoreboard only after reviewing the delta. Do not update the mechanical baseline as part of the default implementation path.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Security | No live credentials, arbitrary command execution, network egress, or secret-like fixture content. |
| Determinism | Tests use the existing fake adapter, local fixtures, and registry-owned verifiers only. |
| Maintainability | Prefer existing schemas/scripts; new helper code is allowed only when multiple fixtures need the same assertion. |
| Compatibility | Existing V1 fixtures and all current Codex skill installs remain valid. |

## Data Model

No application data model or database changes. Evaluation data is JSON fixture content under `.codex/skills/ywc-codex-toolkit-eval/evals/`.

## API Contract

No runtime application API change. The evaluator-facing contract remains the existing V1/V2 fixture schema implemented by `fixture_validator.py` and the existing runner CLI.

## Edge Cases

- No architecture manifest: preserve the documented `N/A — no architecture contract` fallback; do not turn absence into failure.
- Explicit missing or unsafe architecture manifest: return the skill's context/error status; do not silently fall back.
- Missing infrastructure design: route to clarification/design; do not infer topology.
- Critical/High infrastructure review finding: assert BLOCK and remediation routing; never assert apply.
- Fixture declares an undeclared file write or forbidden execution field: validator/runner must fail the fixture, not silently accept it.
- A fixture cannot express a required behavior without broadening the evaluator schema: stop and record the gap rather than adding a general-purpose execution mechanism.

## Dependencies

- Existing `.codex/skills/ywc-codex-toolkit-eval` fixture validator, fake runner, and verifier registry.
- Existing target skills and their `agents/openai.yaml` metadata.
- Python 3 standard library and repository shell validation scripts.

## Open Questions

- [ ] Do the infrastructure skills need live-adapter behavioral evidence after offline fixtures are complete? This is deferred; the current repository policy keeps live evaluation unavailable unless explicitly approved and credentialed.
- [ ] Should S8 watch items be handled in the same release? Recommended answer: no; keep the current plan limited to S5 evidence coverage.

## Confidence Gate

**Aggregate: 93/100 — PROCEED to `ywc-spec-validate`**

| Dimension | Score | Evidence |
|---|---:|---|
| Scope clarity | 95 | Five named skills, exact evaluator surface, explicit exclusions. |
| Architecture compliance | 90 | Reuses the current fixture validator/runner/registry; no new execution architecture. |
| Evidence quality | 95 | Current scorecard, source skill lines, fixture schema, and passing commands were inspected. |
| Reuse verified | 90 | Existing V1/V2 schemas, fake runner, and test scripts are the planned implementation path. |
| Root cause identified | 95 | S5 weakness is insufficient deterministic behavioral evidence, not a structural gate failure. |

## Handoff

Run `ywc-spec-validate` against this spec before implementation. After validation,
run `ywc-task-generator` to split fixture additions, any necessary skill contract
fixes, and the re-score/report update into bounded tasks.

## References

- `docs/skill-agent-eval/codex/2026-08-12-full-sweep.md`
- `.codex/skills/ywc-codex-toolkit-eval/evals/evals.json`
- `.codex/skills/ywc-codex-toolkit-eval/scripts/fixture_validator.py`
- `.codex/skills/ywc-codex-toolkit-eval/scripts/runner.py`

## Iteration 1 Amendments

### Outcome Oracle

- **Target:** Deterministic offline evaluator evidence exists for all five named skills, and the next full scorecard shows the S5 thresholds in AC8 or documents an evidence-model limitation.
- **Quality threshold:** AC1–AC7 pass; the targeted fixture suite, full mocked runner, repository validation, and mechanical scorer all exit successfully.
- **Evidence required:** Fixture files, validator/runner output, targeted and full test output, scorecard rows with file/line evidence, and any reviewed reason for an unmet AC8 threshold.
- **Stop condition:** Stop after one complete offline fixture-and-score pass; do not add live adapters or update `history.mechanical.json` unless explicitly approved.

### Blind Spot Pass

- **Reviewed blind spot:** Offline fixtures may not prove live-adapter behavior or model-quality variance for infrastructure skills.
- **Disposition:** `proceed` with the current scope because live evaluation requires unavailable credentials and is explicitly deferred in the Open Questions section.
- **Follow-up trigger:** Reopen this scope only when live evaluation is approved and credentials are available; keep it separate from the S5 offline evidence pass.
