# ywc-code-gen

A Skill for generating code across multiple layers simultaneously. Runs Backend + Frontend + QA Agents in parallel.

## Usage

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"
```

## Execution Agents

| Agent                   | Output                                     |
| ----------------------- | ------------------------------------------ |
| Backend Agent (sonnet)  | API Route, Service, DB Migration           |
| Frontend Agent (sonnet) | UI Component, Query Hook, State Management |
| QA Agent (sonnet)       | Unit Test, Integration Test, E2E Scenario  |

## Contract and TDD baseline

Before workers run, the skill prepares a shared Contract Snapshot so Backend, Frontend, and QA use the same public contracts. Behavior-changing generation is test-first by default; `--tdd` enables stricter RED/GREEN/REFACTOR checkpoint commits.

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
