# Review Learnings — ywc-agent-toolkit

<!-- updated: 2026-08-13 -->

## How this file is used
Loaded by ywc-impl-review before review; each entry records what + WHY + polarity.

## Learnings
| ID | Scope | Category | Polarity | Rule | Why | Provenance |
|----|-------|----------|----------|------|-----|-----------|
| L001 | `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` | Design | DO-NOT | When authoring a `positive` (or `collision`) trigger case from mined or fallback-authored prompt text, do not include (a) the target item's own identifier (`ywc-<name>` or `/ywc-<name>`) or (b) a verbatim official Trigger phrase from that item's own `SKILL.md` description (e.g. "코드 생성" for `ywc-code-gen`) in the `prompt` string. | `trigger-eval-method.md`'s independence rule: a prompt that names its own target skill, or literally quotes its description's own listed trigger phrase, is trivially winnable by the activation judge (description-only) — both are the same `description-derived` circularity the coverage-floor mechanism exists to prevent, just at the identifier level vs. the phrase level. Bare colloquial words that merely overlap in *topic* with a trigger phrase (e.g. "plan", "brainstorming", "동시에 실행" as a paraphrase of "동시 실행") are fine — the rule targets literal identifier/phrase reuse, not natural vocabulary overlap. | ywc-impl-review findings, tasks 000082-010 and 000082-020, 2026-08-13 |
| L002 | `.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json` | Design | DO | When authoring a new collision id, id-inventory (task.md Step 1) must use each item's *dominant* (majority) slug form — found via the field-based (`expected`/`impostor`) fallback query, not a mechanically `ywc-`-stripped slug — and continue that family's real `max_n`. | Several items in this catalog carry one or two legacy unhyphenated outlier ids (e.g. `taskgenerator-trace-1` alongside 8 `task-generator-*` ids); treating the outlier as authoritative produces an id that both breaks AC9's per-item pattern and would misdirect a later task's own id-inventory into re-using the wrong family. | ywc-impl-review finding, task 000082-020-test-trigger-cases-spec-execution, 2026-08-13 |

## Change Log
- 2026-08-13: L001 added (source: review, task 000082-010).
- 2026-08-13: L001 widened to cover verbatim trigger-phrase reuse (not just the identifier); L002 added (source: review, task 000082-020).
