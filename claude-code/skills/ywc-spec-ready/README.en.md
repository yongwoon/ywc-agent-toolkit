# ywc-spec-ready (Spec Readiness Loop)

A Skill that automatically converges a spec produced by `ywc-plan` to the `ywc-spec-validate` `DONE` state. Each iteration runs `ywc-spec-validate`; on `DONE_WITH_CONCERNS` it appends an amendment via `ywc-plan --update-spec` and re-validates. On reaching `DONE` it prints the `ywc-task-generator` handoff and **stops** (it never auto-runs task-generator).

```text
spec ──> [ywc-spec-validate ──DONE_WITH_CONCERNS──> ywc-plan --update-spec]* ──DONE──> handoff
```

The existing `ywc-agentic` loop revolves around `ywc-impl-review` (code evaluation) and runs `ywc-spec-validate` only **once**. This Skill fills the missing inner loop — **multi-iteration spec convergence**.

## Usage

```text
/ywc-spec-ready --spec docs/ywc-plans/feature.md                       # Default (max 5 iterations)
/ywc-spec-ready --spec docs/ywc-plans/feature.md --max-iterations 8    # Set iteration ceiling
/ywc-spec-ready --spec docs/ywc-plans/feature.md --max-advisor-calls 2 # Advisor cost guard
/ywc-spec-ready --spec docs/ywc-plans/feature.md --dry-run             # Print command sequence only
```

## Options

| Option                   | Description                                                       |
| ------------------------ | ---------------------------------------------------------------- |
| `--spec <path>`          | Spec file to converge (required, a `ywc-plan` output). Absent → `NEEDS_CONTEXT` |
| `--max-iterations <n>`   | Validation loop ceiling (default: 5, never raised autonomously)  |
| `--max-advisor-calls <n>`| Total Opus advisor budget across all iterations (default: 4, cost guard) |
| `--log <path>`           | Append-only loop log (default: `<spec-dir>/<slug>.spec-ready-log.md`) |
| `--dry-run`              | Print the planned command sequence only; invoke no sibling skill |
| `--lang <lang>`          | Report/handoff language (default: auto, inferred from CLAUDE.md) |
| `--focus <area>`         | Forwarded to `ywc-spec-validate`                                  |
| `--format <fmt>`         | Forwarded to `ywc-spec-validate` (markdown / html)               |
| `--terse`                | Minimal output (phase headers and the final report only)         |

## Execution Flow

1. Pre-flight — verify `--spec` exists, derive `<slug>`, handle `--dry-run`
2. Iteration Loop — `ywc-spec-validate` → Status Routing → (on DONE_WITH_CONCERNS) guard check → `ywc-plan --update-spec` → log → repeat
3. Hard Stop — stop immediately on `BLOCKED` / `NEEDS_CONTEXT` / `SOCRATIC` / unparseable
4. Handoff — on `DONE`, print the `ywc-task-generator` guidance and stop
5. Completion Report — single report (final line is the Completion Status)

## Loop-prevention Guards

| Guard | Stop condition |
| --- | --- |
| Iteration cap | `iteration >= --max-iterations` and status ≠ DONE |
| Non-decreasing Criticals | Critical count increases or stays flat for 2 consecutive iterations (signature overlap) |
| Repeated signature | Same Critical signature recurs across consecutive iterations after a re-plan |
| Identical amendment scope | New amendment scope equals the previous one (recursion guard) |

See [references/convergence.md](references/convergence.md) for the full rules and [references/loop-log.md](references/loop-log.md) for the log schema.

## Triggering

This Skill's trigger conditions are defined in the `description` field of [SKILL.md](./SKILL.md).

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
