# ywc-code-gen

A Skill for generating code across multiple layers simultaneously. Runs Backend + Frontend + QA Agents in parallel.

## Test-first, Deep Module, Critical Module Review

The default path gates the headlights: the QA lane writes failing (RED) tests before Backend/Frontend implementation is finalized. `--tdd` opts into the stronger full RED → GREEN → REFACTOR ritual and supersedes the default minimal gate. Public interfaces are designed before bodies (deep module). When generated files touch a critical path (auth, payment, crypto, PII, external input), the run requires internal review and flags `/ywc-security-audit` as a required next step. The Verification Gate checks `git diff --stat` so only spec-named files changed (diff scope), and the Confidence Gate's Minimalism dimension fails overcomplicated code (working ≠ minimal). See `references/tdd-deep-module-gray-box.md` for details.

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
