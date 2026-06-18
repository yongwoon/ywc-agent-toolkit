# Task Dependency Graph

## Batch

- Spec: `docs/ywc-plans/codex-toolkit-eval-improvements.md`
- Granularity mode: `llm`
- Starting phase: `000007`
- Rationale: existing completed tasks go through phase `000006`, so this batch starts at `000007`.

## Phase 000007 - Internal Evaluator Behavior

- `000007-010-infra-score-cli-contract` -> root
- `000007-020-test-trigger-coverage` -> depends on `000007-010-infra-score-cli-contract`

## Phase 000008 - Documentation Surface and Final Gate

- `000008-010-infra-eval-surface-validation` -> depends on `000007-010-infra-score-cli-contract`, `000007-020-test-trigger-coverage`

## Parallel Execution Notes

- Initial ready set: `000007-010-infra-score-cli-contract`
- After `000007-010-infra-score-cli-contract` merges: `000007-020-test-trigger-coverage` becomes runnable.
- After all Phase `000007` tasks merge: `000008-010-infra-eval-surface-validation` becomes runnable.
- `000007-010` and `000007-020` must not run in parallel because both may edit `tools/codex-internal/skills/ywc-codex-toolkit-eval/scripts/test_score.py`.
- `000008-010` must wait for both predecessors because it documents and validates their final behavior.

## Visual Dependency Graph

```mermaid
graph LR
  A[000007-010-infra-score-cli-contract] --> B[000007-020-test-trigger-coverage]
  A --> C[000008-010-infra-eval-surface-validation]
  B --> C
```

---

## Batch 2 — ywc-toolkit-eval (Claude Code) Quality Improvements

- Spec: `docs/ywc-plans/ywc-toolkit-eval-improvements.md`
- Granularity mode: `llm` · Language: korean
- Starting phase: `000009` (phases `000007`–`000008` are occupied by the codex batch above)
- Independent of the codex batch — no cross-dependency.

### Phase 000009 - Eval Scorer Fixes, Docs Alignment, Case Coverage

| Task | Category | Depends On |
| --- | --- | --- |
| `000009-010-domain-eval-scorer-logic` | domain | (root) |
| `000009-020-test-eval-scorer-unit-tests` | test | `000009-010` |
| `000009-030-docs-rubric-skill-alignment` | docs | `000009-010` |
| `000009-040-test-trigger-cases-authoring` | test | `000009-010` |
| `000009-050-infra-final-verification` | infra | `000009-010`, `-020`, `-030`, `-040` |

### Parallel Execution Notes (Batch 2)

- Initial ready set: `000009-010-domain-eval-scorer-logic` (solo — owns `score.py` + `history.mechanical.json`, atomic rebaseline).
- After `000009-010` merges: `000009-020`, `000009-030`, `000009-040` are parallel-safe (disjoint files: `test_score.py` / docs+rubric / `trigger-cases.json`).
- `000009-050` waits for all four; verification only (no source edits).
- **Hard gate (Spec Amendment A3):** `000009-010`'s A5/A7 logic change and the `history.mechanical.json` rebaseline must land in the **same commit**, or CI (`validate.yml --ci`) may go red.

```mermaid
graph LR
  D[000009-010-domain-eval-scorer-logic] --> E[000009-020-test-eval-scorer-unit-tests]
  D --> F[000009-030-docs-rubric-skill-alignment]
  D --> G[000009-040-test-trigger-cases-authoring]
  E --> H[000009-050-infra-final-verification]
  F --> H
  G --> H
```

---

## Batch 3 — ywc-toolkit Activation & Boundary Fixes (Claude catalog)

- Spec: `docs/ywc-plans/ywc-toolkit-activation-fixes.md` (spec-ready DONE, 2 iterations)
- Granularity mode: `llm` · Language: korean
- Starting phase: `000010` (phases `000007`–`000009` occupied by prior batches)
- Independent of prior batches — no cross-dependency. Targets `claude-code/agents` + `claude-code/skills` descriptions only (Codex mirror deferred).

### Phase 000010 — Description / Structure Edits

| Task | Category | Depends On |
| --- | --- | --- |
| `000010-010-docs-reviewer-anti-triggers` | docs | (root) |
| `000010-020-docs-agent-dispatch-boundaries` | docs | (root) |
| `000010-030-docs-skill-anti-triggers` | docs | (root) |
| `000010-040-refactor-parallel-executor-extraction` | refactor | (root) |

### Phase 000011 — Re-baseline & Re-score (hard gate)

| Task | Category | Depends On |
| --- | --- | --- |
| `000011-010-infra-rebaseline-rescore` | infra | `000010-010`, `-020`, `-030`, `-040` |

### Parallel Execution Notes (Batch 3)

- Initial ready set: `000010-010`, `000010-020`, `000010-030`, `000010-040` are **all parallel-safe** — each owns a disjoint set of files (3 reviewer agents / qa+doc agents / 4 skill SKILL.md / parallel-executor skill). No inter-task dependency within Phase 000010.
- None of the Phase 000010 tasks edit `history.mechanical.json`; each verifies read-only with `score.py --format json` (NOT `--ci`).
- **Hard gate:** `000011-010` waits for all four Phase 000010 tasks to merge, then runs the single `score.py --ci` re-baseline + full `ywc-toolkit-eval` re-score. Re-baselining before all edits land would produce an incomplete baseline.
- FR mapping: FR1→010, FR2+FR3→020, FR4–FR7→030, FR8→040, FR9→000011-010.

```mermaid
graph LR
  I[000010-010-docs-reviewer-anti-triggers] --> M[000011-010-infra-rebaseline-rescore]
  J[000010-020-docs-agent-dispatch-boundaries] --> M
  K[000010-030-docs-skill-anti-triggers] --> M
  L[000010-040-refactor-parallel-executor-extraction] --> M
```

---

## Batch 4 — Codex Executor Contract-First / Test-First Skill Improvements

- Spec: `docs/ywc-plans/codex-executor-tdd-deep-module-gray-box.md`
- Granularity mode: `llm` · Language: korean
- Starting phase: `000012` (phases `000001`–`000011` occupied by existing/completed batches)
- Codex-only boundary: targets `codex/skills/**` source and generated plugin sync only; no `claude-code/**` edits.

### Phase 000012 — Shared Contract + Skill Surface Updates

| Task | Category | Depends On |
| --- | --- | --- |
| `000012-010-docs-shared-tdd-boundary-contract` | docs | (root) |
| `000012-020-docs-code-gen-contract-first` | docs | `000012-010` |
| `000012-030-docs-sequential-executor-test-first` | docs | `000012-010` |
| `000012-040-docs-parallel-executor-contract-gates` | docs | `000012-010` |

### Phase 000013 — Sync and Validation Hard Gate

| Task | Category | Depends On |
| --- | --- | --- |
| `000013-010-infra-codex-executor-contract-validation` | infra | `000012-010`, `-020`, `-030`, `-040` |

### Parallel Execution Notes (Batch 4)

- Initial ready set: `000012-010-docs-shared-tdd-boundary-contract`.
- After `000012-010` merges: `000012-020`, `000012-030`, and `000012-040` are parallel-safe because they own disjoint skill directories.
- `000013-010` waits for all Phase 000012 tasks, then runs install scan, optional generated plugin sync, and full repository validation.
- Conflict notes: the three skill tasks share only the new reference semantics and README localization expectations. They must not edit each other's skill directories.
- Hard boundary: no `claude-code/**` edits in Batch 4. Generated plugin output, if needed, belongs only to `000013-010`.
- FR mapping: FR-1→000012-010, FR-2→000012-020, FR-3→000012-030, FR-4→000012-040, FR-5→all Phase 000012 tasks, FR-6→000013-010.

```mermaid
graph LR
  N[000012-010-docs-shared-tdd-boundary-contract] --> O[000012-020-docs-code-gen-contract-first]
  N --> P[000012-030-docs-sequential-executor-test-first]
  N --> Q[000012-040-docs-parallel-executor-contract-gates]
  N --> R[000013-010-infra-codex-executor-contract-validation]
  O --> R
  P --> R
  Q --> R
```

## Batch 5 — Claude Code Executor TDD / Deep Module / Gray Box Improvements

- Spec: `docs/ywc-plans/claude-code-executor-tdd-deep-module-gray-box.md`
- Granularity mode: `llm`
- Starting phase: `000014` (phases `000001`–`000013` occupied by existing/completed batches)
- Scope: claude-code only (the codex twin is Batch 4, phases `000012`–`000013`).

### Phase 000014 — Shared Reference + Skill Surface Updates

| Task | Category | Depends On |
|---|---|---|
| `000014-010-docs-shared-tdd-boundary-contract` | docs | (root) |
| `000014-020-docs-code-gen-red-gate-deep-module` | docs | `000014-010` |
| `000014-030-docs-sequential-executor-test-first` | docs | `000014-010` |
| `000014-040-docs-parallel-executor-contract-gates` | docs | `000014-010` |

### Phase 000015 — Validation Hard Gate

| Task | Category | Depends On |
|---|---|---|
| `000015-010-infra-claude-executor-contract-validation` | infra | `000014-010`, `-020`, `-030`, `-040` |

### Parallel Execution Notes (Batch 5)

- Initial ready set: `000014-010-docs-shared-tdd-boundary-contract`.
- After `000014-010` merges: `000014-020`, `000014-030`, `000014-040` are parallel-safe — each owns a disjoint `claude-code/skills/<skill>/` directory and only read-links the shared reference.
- `000015-010` is a **hard gate**: it waits for all four Phase 000014 tasks, then runs install scan + `scripts/validate.sh` + markdownlint and asserts the claude-code-only boundary.
- Hard boundary: no `codex/**` or `plugins/**` edits in Batch 5. The TDD-default divergence from Batch 4 (codex) is intentional and recorded in the spec.
- FR mapping: FR-1→000014-010, FR-2→000014-020, FR-3→000014-030, FR-4→000014-040, FR-5→all Phase 000014 tasks, FR-6→000015-010.

```mermaid
graph LR
  S[000014-010-docs-shared-tdd-boundary-contract] --> T[000014-020-docs-code-gen-red-gate-deep-module]
  S --> U[000014-030-docs-sequential-executor-test-first]
  S --> V[000014-040-docs-parallel-executor-contract-gates]
  S --> W[000015-010-infra-claude-executor-contract-validation]
  T --> W
  U --> W
  V --> W
```
