# ywc-code-gen

A Skill for generating code across multiple layers simultaneously. Runs Backend + Frontend + QA Agents in parallel.

## Usage

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API" --review
```

## Execution Agents

| Agent                   | Output                                     |
| ----------------------- | ------------------------------------------ |
| Backend Agent (sonnet)  | API Route, Service, DB Migration           |
| Frontend Agent (sonnet) | UI Component, Query Hook, State Management |
| QA Agent (sonnet)       | Unit Test, Integration Test, E2E Scenario  |

## Contract and TDD baseline

Before workers run, the skill prepares a shared Contract Snapshot so Backend, Frontend, and QA use the same public contracts. Behavior-changing generation is test-first by default; `--tdd` enables stricter RED/GREEN/REFACTOR checkpoint commits.
Final reports keep `Implementation Notes` only for non-obvious decisions that materially affect the generated code shape.

## Optional implementation review

Use `--review` to run `ywc-impl-review` after generation passes verification and its Confidence Gate. It reviews the staged, unstaged, untracked, and deleted generated changes without a review-only commit (under `--tdd`, which commits each checkpoint and leaves the tree clean, the review target becomes `--git-range <pre-generation-sha>..HEAD` instead). Start with a clean working tree; Critical or High findings get one fix-and-re-review pass, while unresolved concerns remain in the result.

**Even without `--review`**, generated files landing on a critical path (auth, payment, crypto, PII, external input) force both `ywc-impl-review` and `ywc-security-audit` — the same contract `ywc-sequential-executor` applies. Critical/High findings from **both** reviews enter the single bounded fix cycle, and a `BLOCKED` or `NEEDS_CONTEXT` from either propagates rather than reporting success. Since this skill does not merge, the gate is advisory: surviving findings downgrade the status to `DONE_WITH_CONCERNS`, they do not discard the generated code.

## Relationship with sequential-executor

- **sequential-executor**: Sequential execution (suitable for tasks with dependencies)
- **/ywc-code-gen**: Independent layer parallel generation (when SDK/API/Web are needed simultaneously)
- Used complementarily

## Triggering

Trigger conditions for this Skill are defined in the `description` field of [SKILL.md](./SKILL.md).

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
