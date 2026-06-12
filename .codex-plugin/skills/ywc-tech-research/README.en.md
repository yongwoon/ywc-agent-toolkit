# ywc-tech-research

A Research Agent Skill for technical investigation and library comparison.

## Usage

```text
/ywc-tech-research "How to implement Server-Sent Events in Hono"
```

## Use Cases

| Scenario                    | Example                                                                      |
| --------------------------- | ---------------------------------------------------------------------------- |
| Before writing specs        | "Compare privacy-preserving approaches for Web Analytics SDK"                |
| Library selection           | "PostgreSQL partition table aggregation performance optimization strategies" |
| Stuck during implementation | "Resolving Rollup tree-shaking polyfill issues"                              |

## Execution Agent

- **Research Agent** (claude-sonnet-4-20250514)

## Output Format

- Summary (1-2 sentences)
- Comparative analysis (table)
- Recommendation with rationale
- Project integration considerations
- References

## Triggering

Trigger conditions for this Skill are defined in the `description` field of [SKILL.md](./SKILL.md).

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
