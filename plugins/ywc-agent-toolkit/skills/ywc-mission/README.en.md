# Mission

Maintain the project's durable Mission, Success Criteria, Rejected Approaches, and optional Non-goals/Constraints in `docs/mission.md` across Codex sessions.

## Usage

```text
Use $ywc-mission --mode read.
Use $ywc-mission --mode update --dry-run.
```

## Options

`SKILL.md` is authoritative when this summary differs.

| Option | Values | Default | Purpose |
|---|---|---|---|
| `--mode` | `read\|update\|curate` | auto-detect | Read the active anchor, propose updates, or deprecate stale state. |
| `--output` | `<path>` | `docs/mission.md` | Mission file path. |
| `--dry-run` | flag | off | Show the CHANGESET without confirmation or writing. |

## State and confirmation

- A missing read returns an empty anchor; legacy files without optional sections remain valid.
- Update/curate read the whole file and propose reasoned ADD/MODIFY/DEPRECATE changes. Only exact user confirmation of a non-empty CHANGESET permits durable writing.
- Dry-run and empty changesets make no file, updated-date, or change-log changes and request no confirmation.
- Keep one active Mission. SC requires an observable Criterion and Rationale; RA requires Reason. NG requires Non-goal/Reason; CN requires Constraint/Rationale.
- Optional sections start with their first confirmed row and disappear when no active rows remain. Preserve deprecated text, explanations, provenance and stable IDs in history; never delete or reuse retired IDs.
- Read anchors include active entries only. Re-read before writing; changed state requires fresh confirmation. Applied retries are no-ops; failed writes cannot claim success.
- First creation provides AGENTS.md/CODEX.md activation guidance only. It does not edit those files or infer user intent from a repository scan.

## Output and evidence

Read emits a compact Mission Anchor; update/curate emit the proposed CHANGESET and confirmed result. The durable format is in [mission-format.md](references/mission-format.md).

The source is frozen upstream #348 (`29068f9f690fbf09e0ace8d562e4fb846b4d1339`). Contract fixtures and evaluation expectations are source evidence; live behavior is UNVERIFIED without a separate execution trace.
