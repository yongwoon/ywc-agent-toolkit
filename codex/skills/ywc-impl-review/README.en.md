# ywc-impl-review

A Skill that performs comprehensive implementation conformance verification before creating a PR after implementation is complete. It runs 3 Agents (Reviewer + Security + QA) in parallel.

## Usage

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
```

## Execution Agents

| Agent                 | Verification Scope                                                      |
| --------------------- | ----------------------------------------------------------------------- |
| Reviewer Agent (opus) | Implementation gaps vs specification, code quality, pattern consistency |
| Security Agent (opus) | OWASP Top 10, missing authentication/authorization, Input Validation    |
| QA Agent (sonnet)     | Test Coverage analysis, missing Test Case suggestions                   |

## Output Format

Integrated Report — Aggregator merges results from 3 Agents, classified by severity with prioritized fix recommendations.

## Triggering

Trigger conditions for this Skill are defined in the `description` field of [SKILL.md](./SKILL.md).

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
