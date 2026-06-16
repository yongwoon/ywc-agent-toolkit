# ywc-spec-ready

This document introduces the Codex `ywc-spec-ready` workflow. The authoritative trigger conditions, anti-triggers, execution steps, and output format are defined in [SKILL.md](./SKILL.md).

## Localized Versions

- [한국어](./README.md)
- [日本語](./README.ja.md)
- [한국어 full](./README.ko.md)

## When To Use

- A natural-language goal must become a validated spec before task generation.
- An existing spec must reach `DONE` from `ywc-spec-validate` before `ywc-task-generator`.
- `DONE_WITH_CONCERNS` should be routed through repeated `ywc-plan --update-spec` loops within strict caps.

## Usage

```bash
$ywc-spec-ready "Design payment failure recovery UX"
$ywc-spec-ready --spec docs/ywc-plans/example.md --max-iterations 4
$ywc-spec-ready --spec docs/ywc-plans/example.md --dry-run
```

On success, this skill prints `ywc-task-generator <spec-path>` and stops. It does not generate tasks or implement code directly.

## Output

This skill follows the report, loop log, and status format defined in [SKILL.md](./SKILL.md).
