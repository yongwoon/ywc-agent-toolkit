# yw-000005-020-docs-task-generator-skill-initials

## Purpose
Wire the initials contract into `ywc-task-generator`'s own skill body so every generated task ID carries an `INITIALS` segment, without restating rules that already live in the shared reference.

## Scope
Add the `--initials` argument, the Step 2 resolution step, one Rationalization Defense row, the `[INITIALS]` naming-convention definition, and two Final Validation rows to `ywc-task-generator/SKILL.md`, staying inside the ~500-line budget.

## Spec Reference
### Primary Sources
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#fr2--ywc-task-generator-step-2에-initials-해석-삽입-ac1-ac2` — SKILL.md edit contract
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#a5---initials-precedence-ac-추가-warning-2-대응` — AC10 precedence observability
- `docs/ywc-plans/20260826-task-id-collaborator-initials.md#non-functional-requirements` — NFR3 single-source, NFR4 length budget

### Summary
Initials must be resolved on **every** run, not only when tasks already exist, because Step 7 naming always requires the segment. The skill body cites `references/initials-resolution.md` through an `> **Action required**: Read [...]` directive and does not inline the precedence chain, derivation algorithm, or section format. Caching writes the `## Task Initials` section with create-or-replace semantics, mirroring the duplicate-heading guard already used for the language policy section. Precedence must be observable in three distinct states: flag wins over cached section, cached section suppresses derivation and the question, and absence of both triggers derivation plus exactly one confirmation.

### Out of Scope (from spec)
- The reference file itself — `yw-000004-010-docs-initials-resolution-reference`.
- Script behavior — `yw-000005-010-infra-next-task-number-initials-scan`.
- Templates, execution convention, READMEs, and evals — the `yw-000006` phase.

## Criticality
normal

## Dependencies
### Depends On
- `yw-000005-010-infra-next-task-number-initials-scan` — the SKILL.md text quotes this script's final `[tasks-dir] [initials]` signature and its seed/reservation behavior.

### Depended By
- `yw-000006-010-docs-task-generator-artifacts-sync` — templates and evals follow the wording settled here.
- `yw-000006-020-docs-executor-consumer-sync` — downstream examples mirror this canonical wording.
- `yw-000006-030-docs-branch-testcase-consumer-sync` — same.
- `yw-000007-010-infra-validation-gate` — final no-regression gate.

## Key Files
- `claude-code/skills/ywc-task-generator/SKILL.md`

## Notes
- SKILL.md is currently 434 lines against a ~500-line guideline. Roughly 66 lines of headroom exist; anything longer must be pushed into `references/initials-resolution.md` rather than inlined (NFR4).
- Do not use `@skill-name` force-load references anywhere in the edit — repository rule.
- The Rationalization Defense row to add: *"This repository has one user, so initials are overkill"* → *"The moment a second worktree exists, the collision happens silently with no merge conflict. A one-time question costs nothing; skipping it costs unrecoverable numbering ambiguity."*

## Hardening Evidence
### Test Feedback Path
- No executable surface. Verification is structural: line budget, single `## Task Initials` heading produced on a scratch fixture, and the three AC10 precedence states each observed once.

### Interface Contract
- Contract: the `--initials` argument and the Step 2 resolution step of the skill.
- Inputs: `--initials <value>`, project `CLAUDE.md`, git identity.
- Outputs: task directory names carrying the resolved prefix; a cached `## Task Initials` section.
- Error model: no-block — absence of every source falls through to derivation plus one question, never an error.
- Impacted tests: the eval scenario added by `yw-000006-010`.

### Critical Surface Review
- Review requirement: N/A — spec declares no Critical Surfaces.

### Data Integrity Hardening
- Trigger surface: the cached `## Task Initials` section in `CLAUDE.md`.
- Atomic / locking strategy: N/A — the PHASE reservation lives in `yw-000005-010`.
- Transaction boundary: N/A
- Idempotency guard: create-or-replace, leaving exactly one section across any number of re-runs.
- Required tests: AC1 — `grep -c '^## Task Initials' CLAUDE.md` equals 1 after two consecutive runs.

## Parallel Execution Metadata
### Ownership
- `claude-code/skills/ywc-task-generator/SKILL.md`

### Shared Surfaces
- Task-generator skill contract
- `CLAUDE.md ## Task Initials` canonical section

### Conflicts With
- `yw-000005-010-infra-next-task-number-initials-scan` — the script signature quoted here must be final first.

### Parallelizable After
- `yw-000005-010-infra-next-task-number-initials-scan`

### Task Verify
- `test "$(wc -l < claude-code/skills/ywc-task-generator/SKILL.md)" -le 500`
- `grep -q 'initials-resolution.md' claude-code/skills/ywc-task-generator/SKILL.md`
- `grep -q '\[INITIALS\]' claude-code/skills/ywc-task-generator/SKILL.md`
- AC1: two consecutive scratch runs leave exactly one `## Task Initials` section
- AC10: the three precedence states each produce the expected directory prefix
- `bash scripts/validate.sh`

## Out of Scope
- Changing PHASE width, SEQUENCE stepping, or the category vocabulary.
- Editing any other skill's SKILL.md.
