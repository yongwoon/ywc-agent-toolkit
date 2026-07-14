# ywc-impl-review

A Skill that performs comprehensive implementation conformance verification before creating a PR after implementation is complete. It runs 5 Phase 1 workers (Architecture / Design / Devex / Security / QA — 4 on Sonnet, 1 on Haiku) in parallel, then escalates ambiguous findings to a Phase 2 Opus advisor.

## Usage

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --working-tree
```

`--working-tree` reviews staged, unstaged, and untracked source changes without requiring a commit. Do not combine it with `--code` or `--git-range`.

## Execution Agents

| Agent                  | Verification Scope                                                              |
| ----------------------- | --------------------------------------------------------------------------------- |
| Architecture (sonnet)  | Module boundaries, layering, dependency direction, structural spec conformance   |
| Design (sonnet)        | API/interface design, naming, signatures, error models, contract spec conformance |
| Devex (sonnet)         | Readability, error messages, logging, documentation, debuggability              |
| Security (sonnet)      | OWASP Top 10 analysis                                                            |
| QA (haiku)             | Test coverage gaps, missing test cases                                          |

Phase 2 (opus) — escalates only ambiguous findings from the five workers above (default budget: 5 calls, adjustable via `--advisor-budget`, shared).

## Output Format

Integrated Report — Aggregator merges Phase 1 findings with Phase 2 advisor verdicts, classified by severity with prioritized fix recommendations. Each finding carries a `[P1]`/`[P2]` marker indicating its Phase 1/Phase 2 provenance.

## Triggering

Trigger conditions for this Skill are defined in the `description` field of [SKILL.md](./SKILL.md).

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
- [Chinese](./README.zh.md)
- [Spanish](./README.es.md)
