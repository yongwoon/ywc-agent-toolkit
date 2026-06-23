# Mission File Format — `docs/project-mission.md`

The full specification for the file `ywc-project-mission` reads and writes. The SKILL.md body summarizes this; this file is the authoritative schema.

## File skeleton

```markdown
# Project Mission — [Project Name]

<!-- updated: YYYY-MM-DD -->

## Mission / North-Star
- <durable one-paragraph statement of what the project is and why>  (<source>, YYYY-MM-DD)

## Success Criteria
| ID | Criterion (measurable) | Source | Added | Status |
|----|------------------------|--------|-------|--------|
| S001 | <observable done condition> | brainstorm | 2026-06-23 | active |

## Out of Scope (durable non-goals)
- <non-goal> — <reason>  (YYYY-MM-DD)

## Change Log
| Date | Change | Source |
|------|--------|--------|
| 2026-06-23 | Created mission + S001 | brainstorm |
```

## Section rules

### Mission / North-Star

- One durable paragraph (occasionally two) describing **what the project is and why it exists**. It must outlive any single feature — if a statement would be obsolete once the current sprint ships, it does not belong here.
- Each Mission bullet carries an inline `(<source>, YYYY-MM-DD)` provenance suffix.
- There is normally exactly one active Mission statement. A revision deprecates the old one (see Deprecation) rather than appending a second active statement.

### Success Criteria (table)

Columns, in order:

| Column | Meaning | Rules |
|---|---|---|
| `ID` | Stable identifier | `S` + zero-padded sequence (`S001`, `S002`). Never renumber; a deprecated ID is retired, not reused. |
| `Criterion (measurable)` | The done-condition | Must be **observable / checkable** — a reader can decide true/false. Reject vague aspirations ("be fast"); require a measurable form ("p95 request latency under 200 ms"). |
| `Source` | Skill-provenance | One of `brainstorm` or `plan` (optionally with a `<ref>`, e.g. `plan #21`). This is the **skill** the criterion came from, matching the `--source` convention — not an artifact type. |
| `Added` | Date the entry entered the file | `YYYY-MM-DD`. Set once when the row is added; never bumped on unrelated edits. |
| `Status` | Lifecycle | `active` or `deprecated`. A deprecated row keeps its data with the strikethrough/note treatment below. |

### Out of Scope (durable non-goals)

- Each bullet names the non-goal and the **reason** it is excluded, with an inline `(YYYY-MM-DD)`.
- These are durable boundaries (what the project will deliberately never do), not the per-feature "out of scope" list a spec carries.

### Change Log

- Auto-maintained metadata, **not** a user-facing section — the skill appends one row per real write. It is exempt from the "every section is user-curated" expectation: the skill owns it.
- Columns `Date | Change | Source`. One row per `update`/`curate` that actually wrote to the file. An idempotent no-op `update` appends **no** row.

## Provenance grammar

- Mission bullet / Out-of-Scope bullet: inline suffix `(<source>, YYYY-MM-DD)` where `<source>` ∈ {`brainstorm`, `plan <ref>`}.
- Success Criterion: the `Source` and `Added` columns carry the same information in table form.
- `<ref>` is optional and free-form but should be traceable (a plan number, a brainstorm session date).

## Deprecation

Never hard-delete an entry. To retire one:

- **Success Criterion row**: set `Status` to `deprecated`, strike the `Criterion` text with `~~strikethrough~~`, and append a trailing note cell or a `> deprecated YYYY-MM-DD: <reason / superseded-by S0NN>` line beneath the table.
- **Mission / Out-of-Scope bullet**: wrap the text in `~~strikethrough~~` and add a `> deprecated YYYY-MM-DD: <reason / superseded-by …>` line.

Newest-wins: when a new entry contradicts an active one, the `update` CHANGESET pairs a `DEPRECATE` (old) with an `ADD` (new). Two contradictory **active** entries must never coexist.

## Idempotency (AC15 / NFR3)

An `update` whose confirmed CHANGESET is empty — every candidate already matches the file byte-for-byte in meaning — performs **no** write: the file is untouched, the `<!-- updated: DATE -->` header is not bumped, and no Change Log row is appended. The skill reports "mission unchanged" and stops. This keeps `git log` honest: a commit touching the mission file always reflects a real change of intent.
