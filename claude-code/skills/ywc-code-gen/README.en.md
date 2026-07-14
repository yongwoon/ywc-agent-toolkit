# ywc-code-gen

A Skill for generating code across multiple layers simultaneously. Runs Backend + Frontend + QA Agents in parallel.

## Test-first, Deep Module, Critical Module Review

The default path gates the headlights: the QA lane writes failing (RED) tests before Backend/Frontend implementation is finalized. `--tdd` opts into the stronger full RED → GREEN → REFACTOR ritual and supersedes the default minimal gate. Public interfaces are designed before bodies (deep module). With `--review`, Step 8 runs `/ywc-impl-review` on the generated code and fixes Critical/High findings through **one** bounded cycle — anything surviving that cycle is reported as `DONE_WITH_CONCERNS`. When generated files touch a critical path (auth, payment, crypto, PII, external input), `/ywc-impl-review` and `/ywc-security-audit` run **even without `--review`** (the same forced contract `ywc-sequential-executor` applies). Since this skill does not merge, the gate is advisory rather than blocking. The Verification Gate checks `git diff --stat` so only spec-named files changed (diff scope), and the Confidence Gate's Minimalism dimension fails overcomplicated code (working ≠ minimal). Step 6.5 also logs any spec↔reality divergences encountered during generation to `implementation-notes.md`, recommending `ywc-plan --update-spec` when a divergence is material. See `references/tdd-deep-module-gray-box.md` for details.

## Usage

```text
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API"

# Also run /ywc-impl-review in Step 8, with one bounded fix cycle
/ywc-code-gen --spec docs/outline/02-backend-api-design.md --feature "auto-target-registry API" --review
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
