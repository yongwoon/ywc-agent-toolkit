# Mission Format

`docs/mission.md`는 commit된 Markdown 상태 파일입니다. 현재 프로젝트 Mission, 활성 Success Criteria, 활성 Rejected Approaches, 선택적 Non-goals 및 Constraints, 폐기된 과거 항목, 간단한 변경 이력을 기록합니다.

## Required Structure

```markdown
# Mission - <Project Name>

<!-- updated: YYYY-MM-DD -->

## How this file is used
Short instruction explaining that Codex sessions should read this file before planning or implementation work.

## Mission
<Exactly one active Mission statement.>

## Success Criteria
| ID | Criterion | Rationale | Status | Provenance |
|---|---|---|---|---|
| SC001 | Observable done condition | Why this matters | active | user, YYYY-MM-DD |

## Rejected Approaches
| ID | Approach | Reason | Status | Provenance |
|---|---|---|---|---|
| RA001 | Approach considered | Why it was rejected | active | user, YYYY-MM-DD |

## Deprecated
| ID | Kind | Text | Original Reason / Rationale | Original Provenance | Deprecated | Reason / Superseded-by |
|---|---|---|---|---|---|---|

## Change log
- YYYY-MM-DD - <summary>
```

`## Non-goals`와 `## Constraints`는 선택 항목입니다. 각 섹션은 첫 항목이 확정될 때만 추가합니다. 빈 섹션을 만들지 않으며, 모든 항목이 폐기되면 해당 섹션도 제거합니다.

## Non-goals

Non-goal은 안정적인 `NG###` ID를 사용합니다. 각 활성 행에는 구체적인 Non-goal, 범위에서 제외하는 이유를 설명하는 비어 있지 않은 Reason, Status, Provenance가 필요합니다.

```markdown
## Non-goals
| ID | Non-goal | Reason | Status | Provenance |
|---|---|---|---|---|
| NG001 | Migrate every legacy project Mission file | Migration is not needed to support the optional format | active | user, YYYY-MM-DD |
```

## Constraints

Constraint는 안정적인 `CN###` ID를 사용합니다. 각 활성 행에는 구체적인 Constraint, 해당 제약이 적용되는 이유를 설명하는 비어 있지 않은 Rationale, Status, Provenance가 필요합니다.

```markdown
## Constraints
| ID | Constraint | Rationale | Status | Provenance |
|---|---|---|---|---|
| CN001 | Keep Claude Code and Codex Mission guidance independent | The two runtimes have separate activation and maintenance contracts | active | user, YYYY-MM-DD |
```

행을 폐기할 때는 기존 `NG` 또는 `CN` ID를 유지해 `## Deprecated`로 옮기며, 해당 ID를 재사용하지 않습니다. 기존 text, Reason/Rationale, Provenance도 함께 보존합니다. 선택 섹션에 활성 행이 남지 않으면 빈 상태로 두지 말고 섹션과 표를 제거합니다. 두 선택 섹션이 없는 기존 Mission 파일도 유효합니다.

## Mission

There must be exactly one active Mission. If the user supplies a replacement Mission, deprecate the prior active statement and write the replacement as the single active statement.

Example:

```markdown
## Mission
Build a repeatable onboarding path that lets construction SMB teams start job tracking without a sales-led setup call.
```

## Success Criteria

Success Criteria use stable `SC###` IDs. Active criteria require an observable Criterion and a Rationale.

Example:

```markdown
| ID | Criterion | Rationale | Status | Provenance |
|---|---|---|---|---|
| SC001 | A new account can create its first job and invite one teammate in under 10 minutes | Time-to-first-value is the mission's concrete adoption signal | active | user, 2026-06-23 |
```

## Rejected Approaches

Rejected Approaches use stable `RA###` IDs. Active entries require a non-empty Reason. The Reason should generalize beyond the exact wording of the rejected idea.

Example:

```markdown
| ID | Approach | Reason | Status | Provenance |
|---|---|---|---|---|
| RA001 | Require a sales-led onboarding workshop before first job creation | It delays self-serve activation and contradicts the under-10-minute success criterion | active | planning, 2026-06-23 |
```

## Deprecated Entries

Never hard-delete Mission history, `SC###`, `RA###`, `NG###`, or `CN###` entries. Move stale or superseded content into `## Deprecated` with dated reasons. Preserve the original text, Reason/Rationale, and Provenance in that history, extending legacy history rows with this information when available; do not invent missing provenance. Copy each original Reason/Rationale and Provenance verbatim into the corresponding Original columns; keep the deprecation reason separate. IDs are retired forever.

Example:

```markdown
| ID | Kind | Text | Original Reason / Rationale | Original Provenance | Deprecated | Reason / Superseded-by |
|---|---|---|---|---|---|---|
| SC002 | Success Criterion | ~~Five sample jobs are preloaded for every account~~ | Reduce initial setup effort | user, 2026-06-22 | 2026-06-23 | Superseded by SC004; sample jobs are optional seed data |
| NG001 | Non-goal | Migrate every legacy project Mission file | Migration is not needed to support the optional format | user, 2026-06-22 | 2026-06-23 | Superseded by a user-confirmed migration plan |
| CN001 | Constraint | Keep Claude Code and Codex Mission guidance independent | The two runtimes have separate activation and maintenance contracts | user, 2026-06-22 | 2026-06-23 | Superseded by a user-confirmed shared activation contract |
```

## Change Log

Append one compact line for confirmed writes. Empty CHANGESET no-ops must not add a change-log entry.

Example:

```markdown
## Change log
- 2026-06-23 - Mission set; +SC001; +RA001
- 2026-06-24 - SC002 deprecated; +SC004
```

## ID Rules

| Rule | Requirement |
|---|---|
| Format | `SC###`, `RA###`, `NG###`, and `CN###`, zero-padded from `001`. |
| Allocation | Use the next never-used ID in the matching series. |
| Reuse | Never reuse an ID after deprecation, including IDs moved to `## Deprecated`. |
| Active status | Active rows use `active`; deprecated rows move to `## Deprecated`. |

## Empty CHANGESET Rule

When the proposed CHANGESET has nothing to ADD, MODIFY, or DEPRECATE:

- do not write the file,
- do not update `<!-- updated: YYYY-MM-DD -->`,
- do not append `## Change log`,
- report that the Mission is unchanged without asking for confirmation.
