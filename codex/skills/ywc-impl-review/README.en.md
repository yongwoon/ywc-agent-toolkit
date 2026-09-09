# ywc-impl-review

A Skill that performs comprehensive implementation conformance verification before creating a PR after implementation is complete. It runs 5 Phase 1 workers (Architecture / Design / Devex / Security / QA) in parallel, then escalates ambiguous findings to a Phase 2 advisor.

Before worker fan-out, the selected target is refused when it is empty or exceeds 200 files. Diff-derived targets (`--base`, `--git-range`, and `--working-tree`) are also refused above 5,000 added-plus-removed lines; `--code` uses only the file limit because it is path-only. The exact counts and largest files are reported on refusal.

After Phase 1, every eligible Critical or High finding receives a blind independent verification using only its `file:line` and claimed severity. The report distinguishes `reproduced`, `verification-failed`, `verification-error`, and `cap-unverified` outcomes. These verifier calls do not consume the Phase 2 advisor budget, and `[P1]`/`[P2]` provenance remains separate from verification status.

## Usage

```text
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --code api/src/
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --working-tree
/ywc-impl-review --spec docs/outline/02-backend-api-design.md --base main
```

`--working-tree` reviews staged, unstaged, and untracked source changes without requiring a commit. `--base <ref>` reviews `git merge-base <ref> HEAD` through `HEAD` and reports both the supplied ref and resolved merge-base. `--git-range A..B` remains the explicit two-endpoint comparison. Exactly one of the four target modes is required; they are mutually exclusive.

## Execution Agents

| Agent                  | Verification Scope                                                              |
| ----------------------- | --------------------------------------------------------------------------------- |
| Architecture           | Module boundaries, layering, dependency direction, structural spec conformance   |
| Design                 | API/interface design, naming, signatures, error models, contract spec conformance |
| Devex                  | Readability, error messages, logging, documentation, debuggability              |
| Security               | OWASP Top 10 analysis                                                            |
| QA                     | Test coverage gaps, missing test cases                                          |

Phase 2 advisor — escalates only ambiguous findings from the five workers above (default budget: 5 calls, adjustable via `--advisor-budget`, shared). Independent verification calls are outside this budget.

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
