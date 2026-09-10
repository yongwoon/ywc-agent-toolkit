# Quality Gate Contract for Claude Code Skills

Used by `ywc-plan`, `ywc-sequential-executor`, `ywc-parallel-executor`, and `ywc-impl-review` to define opt-in thresholds for complexity and test-effectiveness gates applied to diff-only code changes. The gate roles (Cleaner for CRAP complexity, Hardener for mutation score), thresholds, dispatch conditions, and resolution policies are identical across these skills. This is a shared reference — consuming skills link this document and do not re-state gate rules inline.

## 1. Purpose

The Quality Gate Contract lets a project carry bounded complexity and mutation evidence through the task lifecycle. The gates exist to enforce code complexity and test-effectiveness standards on newly written or changed code, catching regressions that pass functional tests but represent hidden risk.

Gate adoption is opt-in: a task that does not declare a quality gate contract in its `spec` → `quality_gate_contract` field proceeds without complexity or mutation checks and keeps the existing verification and review workflow. A project that does not adopt quality gates does not pay the dispatch or evidence-gathering cost.

## 2. Roles

Quality gates are enforced by two specialized Cleaner and Hardener roles:

| Role | Gate type | Threshold | Dispatches to |
|---|---|---|---|
| **Cleaner** | Complexity (CRAP) | Maximum CRAP ≤ 8 (default) | `ywc-refactor-cleaner` |
| **Hardener** | Mutation score | Minimum ≥ 90% (default) | `ywc-qa-engineer` |

**Cleaner** owns production-code-only refactoring; it must not modify tests or fixtures. It attempts complexity reduction when measured CRAP exceeds the threshold, and returns a sanitized result containing status, pre/post baseline-test proof, measured maximum CRAP, and changed paths.

**Hardener** owns test-and-fixture-only hardening; it must not modify production code. It attempts to raise mutation score when survivors remain after Cleaner passes, and returns a sanitized result containing status, attempt count, mutation score or bounded survivor evidence, and changed paths.

## 3. Thresholds

The canonical defaults are as follows. A project adopting quality gates may configure these thresholds per task, but the circuit-breaker rules and dispatch conditions remain fixed.

| Gate | Default | Rationale |
|---|---|---|
| CRAP (Complexity Risk Analysis Point) | 6–8 | Captures methods/functions that combine high cyclomatic complexity (>5) with low test coverage (<80%); measures behavior-risk density. Range allows gradual escalation without false positives in test-dense code. |
| Mutation score | ≥90% | Enforces that the test suite kills 90%+ of injected defects; leaves room for equivalent mutants or tool artifacts but requires hardening when effective coverage is < 90%. |

These thresholds apply only to the diff introduced by the current task, never retroactively to the full codebase.

## 4. Diff-only Principle

Quality gates apply only to the diff introduced by the current task or execution wave, never retroactively to the full codebase. A project may never mandate that existing code pass these gates; gates only constrain new or changed production and test code.

When measuring CRAP and mutation score:

- Measure only the production-code paths touched in the diff.
- Measure test and fixture changes only for the test/fixture symbols that correspond to changed production symbols.
- Do not require pre-existing code outside the diff to meet the threshold.

## 5. Mutation Loop Cap

Hardener may make at most three approved attempts per task or execution wave. After the third attempt:

- Report every residual survivor — a mutant not killed by the test suite — with its bounded evidence reference.
- Forward all survivors to the implementation review or delivery reviewer, never silently drop them.
- Do not claim success merely because an attempt completed; a third-round attempt with survivors remaining is still evidence of incomplete mutation coverage.

Surviving mutants after round 3 are raised as concerns in the final completion report; the reviewer, not the executor or dispatch agent, decides whether survivors are acceptable.

## 6. Equivalent-Mutant Policy

A surviving mutant believed to be **equivalent** (one whose mutation produces semantically identical behavior, e.g., reordering two unrelated statements) is still reported as a survivor in the final evidence and forwarded to the reviewer.

Equivalence determination is a **human decision**, never adjudicated by:
- The Hardener agent itself (no automatic "this is equivalent, skip it" logic).
- The executor that calls Hardener (no silent filtering of survivors).
- The delivery/merge automation.

The reviewer has full context to distinguish a true equivalent from a mutant representing incomplete test coverage. All survivors, suspected equivalent or not, become part of the permanent task record.

## 7. Contract-Absent Fallback

The exact sentinel for a task or plan with no quality gate contract is:

```
N/A — no quality gate contract
```

This exact string (including capitalization, spacing, and em dash) is valid and not a failure; it signals opt-out. Every downstream skill and executor that reads a quality gate field must check for this sentinel first. When found:

- Do not emit an empty packet or placeholder.
- Do not dispatch Cleaner or Hardener workers.
- Do not require any authorized tool.
- Do not alter the established verification, review, or delivery lifecycle.

Absence of a quality gate contract is a clean no-op; the task proceeds without gate steps.

## 8. Baseline Convention

A **Baseline** is an artifact maintained by the adopting project to record baseline test results, baseline mutation scores, or other reference evidence. It is a **per-adopting-project** file, never created, seeded, or written to by this toolkit or its skills.

When a task declares a quality gate contract:

- The task may reference a project-specific `Baseline` location (e.g., `.ywc-gate-baseline`) to read baseline evidence.
- Cleaner and Hardener may read `Baseline` to compare pre/post evidence.
- **This toolkit never creates, modifies, or deletes `Baseline`.** The adopting project owns initialization, maintenance, and rotation of baseline artifacts.

If a Cleaner or Hardener dispatch depends on `Baseline` and the file is absent or corrupt, the dispatch returns `NEEDS_CONTEXT` and surfaces the missing baseline to the task maintainer for resolution.

## 9. gate_state Sentinel Vocabulary

A quality gate's state at any step must be exactly one of these values. These strings are deterministic outcomes, not free-text descriptions:

| State | Meaning |
|---|---|
| `"not run — contract absent"` | No quality gate contract was declared; all gates skipped cleanly. |
| `"not run — tool unavailable"` | A valid contract was declared and gates were eligible, but the authorized tool (e.g., a CRAP analyzer or mutation framework) could not be invoked or was not found. |
| `"not run — dispatch failed"` | A valid contract was declared and gates were eligible, but the dispatch to Cleaner or Hardener (via `ywc-refactor-cleaner` or `ywc-qa-engineer`) failed before the worker could attempt the gate. |
| `"pass"` | The measured value (CRAP or mutation score) met or exceeded the threshold; the gate did not require a worker dispatch. |
| `"fail — severity advisory"` | The measured value fell below the threshold under an `advisory` contract mode; Cleaner or Hardener was dispatched and returned `DONE_WITH_CONCERNS`. The task may proceed but records the concern. |
| `"fail — severity enforced"` | The measured value fell below the threshold under an `enforced` contract mode; Cleaner or Hardener was dispatched and returned `BLOCKED`. The task cannot proceed without human review or threshold adjustment. |
| `"skip — dispatcher decision"` | Dispatcher (e.g., `ywc-sequential-executor`) determined the task is ineligible for this gate (e.g., documentation-only, no production code). |

Every field or report that includes a gate state must use one of these exact strings, never paraphrased, free-text descriptions, or abbreviations.

**Enforcement-eligibility rule**: a delivery mode whose point-of-no-return precedes a gate may not declare `enforced` at that gate — an isolation mechanism can only protect state whose point-of-no-return sits after the gate runs. Under `--per-task-pr` (`ywc-parallel-executor`), each task's point-of-no-return (`gh pr merge --delete-branch`) lands inside the wave, before the wave-boundary check completes, so that check cannot enforce there regardless of the declared contract tier. The wave-boundary cross-task-interaction check still **runs** under `--per-task-pr` — it is reporting-only — but its result is a plain descriptive note in the wave's Completion Report and is **never** assigned to `gate_state`.

## 10. Tooling Exclusion

This document defines the **contract and routing logic only**. It does not and must not define:

- Tool installation steps, package managers, or dependency specifications (e.g., "install Pylint for Python CRAP analysis").
- Tool-specific CLI flags, configuration files, or output parsing rules.
- Per-language or per-framework CRAP analyzer names, mutation-testing frameworks, or baseline-artifact locations.

Each adopting project supplies its own:
- CRAP analyzer (e.g., Pylint, Phpmd, cloc-based heuristics, custom tooling).
- Mutation testing framework (e.g., mutmut, Stryker, pitest, custom harness).
- Baseline convention and artifact path.

These are maintained as local project conventions, not as part of this toolkit's scope. When a skill documentation or spec mentions a tool (e.g., "Hardener will run your project's mutation test framework"), it refers the reader back to this contract for the state vocabulary and result handling, not for installation or configuration guidance.
