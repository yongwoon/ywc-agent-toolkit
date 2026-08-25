# 000073-010-domain-architecture-invariants-contract — Implementation Checklist

## Prerequisites
- [ ] Confirm the working tree contains the approved specification at `docs/ywc-plans/20260812-codex-architecture-invariants.md`

## Allowed Edit Scope
- [ ] Modify only `codex/skills/ywc-architecture-invariants/**` and `codex/skills/scripts/architecture-invariants.py`
- [ ] Stop before editing consumer skills, tests, generated plugin output, or release metadata

## Stop Conditions
- [ ] Stop if v1 requires a third-party dependency or subprocess execution.
- [ ] Stop if a contract shape cannot remain closed and repository-relative.
- [ ] Stop if consumer-specific behavior must be decided inside the shared helper.

## Hardening Gate
- RED-first evidence: add contract-level failing cases or an explicit fixture plan before finalizing behavior-changing helper code.
- Public interface contract: record the exact CLI modes, JSON shapes, verdict precedence, and no-manifest fallback in `references/contracts.md`.
- Data Integrity Hardening: N/A — documentation/tooling contract only.
- Critical review: inspect all process-launch and executable-field paths; v1 must launch zero child processes.

## Implementation Steps
- [ ] Create `codex/skills/ywc-architecture-invariants/SKILL.md`, `README.md`, `README.en.md`, `README.ja.md`, `README.ko.md`, `README.zh.md`, `README.es.md`, `agents/openai.yaml`, and `evals/evals.json` with the v1 validation-only interface.
  - Related AC/FR: AC1, AC2, AC3, AC4, AC6, AC8 / FR-1, FR-3, FR-6
  - Contract / Behavior Change: adds an optional architecture-contract skill without changing no-manifest workflows.
  - Verification Command / Evidence: frontmatter, locale, metadata, and eval-shape checks pass.
- [ ] Add `codex/skills/ywc-architecture-invariants/references/contracts.md` with closed manifest, evidence, and audit-result schemas, including unknown-key rejection and deterministic path/glob rules.
  - Related AC/FR: AC1, AC3, AC4, AC6 / Iteration 2 B–C
  - Contract / Behavior Change: defines the source-of-truth JSON contracts consumed by all later tasks.
  - Verification Command / Evidence: schema examples and invalid-shape cases are reviewable and project-relative.
- [ ] Implement `codex/skills/scripts/architecture-invariants.py` using only `json`, `hashlib`, `pathlib`, and standard-library parsing/control helpers.
  - Related AC/FR: AC1–AC4, AC6 / Iteration 2 B–C
  - Contract / Behavior Change: validates draft/validate/audit inputs, maps bounded paths, verifies scope digests, and applies aggregate precedence without launching processes.
  - Verification Command / Evidence: `python3 -m py_compile codex/skills/scripts/architecture-invariants.py`; targeted CLI checks.
- [ ] Implement explicit-manifest handling, root-only discovery, no-manifest fallback, and draft approval/output safety exactly as amended.
  - Related AC/FR: AC4, AC6 / Iteration 2 B–C
  - Contract / Behavior Change: invalid explicit manifests return `NEEDS_CONTEXT` and never fall back; absent discovered manifests return `N/A`.
  - Verification Command / Evidence: command-level negative cases and no-manifest compatibility review.

## Task Verify
- [ ] `python3 -m py_compile codex/skills/scripts/architecture-invariants.py`
  - Expected Passing Signal: exit code 0.
  - Pre-change Failing Evidence / Exception: N/A — new helper; verify syntax and contract implementation together.
  - Contract/Test Evidence: CLI shape review plus subsequent fixture task.
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
  - Expected Passing Signal: structural contract eval runner passes.
  - Pre-change Failing Evidence / Exception: N/A — new skill.
  - Contract/Test Evidence: new skill has valid `evals/evals.json`.

## Verification
- [ ] lint passes (`bash scripts/validate.sh`)
- [ ] typecheck passes (N/A — Python standard library script; `py_compile` is the type/syntax check)
- [ ] unit tests pass (deferred to `000073-020`)
- [ ] integration tests pass (deferred to consumer task)
- [ ] app builds without error (N/A — skills bundle; run install validation in `000074-010`)
