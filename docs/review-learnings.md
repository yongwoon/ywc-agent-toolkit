# Review Learnings — ywc-agent-toolkit

<!-- updated: 2026-08-13 -->

## How this file is used
Loaded by ywc-impl-review before review; each entry records what + WHY + polarity.

## Learnings
| ID | Scope | Category | Polarity | Rule | Why | Provenance |
|----|-------|----------|----------|------|-----|-----------|
| L001 | `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` | Design | DO-NOT | When authoring a `positive` (or `collision`) trigger case from mined or fallback-authored prompt text, do not include the target item's own identifier (`ywc-<name>` or `/ywc-<name>`) in the `prompt` string. | `trigger-eval-method.md`'s independence rule: a prompt that names its own target skill is trivially winnable by the activation judge (description-only), mirroring the exact `description-derived` circularity the coverage-floor mechanism exists to prevent. Bare colloquial trigger words (e.g. "plan", "brainstorming") that already appear in the skill's own official Triggers list are fine — the rule targets the full `ywc-*` identifier / slash-command form specifically. | ywc-impl-review finding, task 000082-010-test-trigger-cases-planning-core, 2026-08-13 |

## Change Log
- 2026-08-13: L001 added (source: review, task 000082-010).
