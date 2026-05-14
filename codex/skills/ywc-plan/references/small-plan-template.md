# Small Path — `plan.md` Template

Use this template when `ywc-plan` Step 3 selects **Small** scale. The output is a single file at the user-specified path (default `./plan.md`).

## Structure

```markdown
# Plan: <one-line title>

> Status: Ready for implementation
> Scale: Small
> Created: YYYY-MM-DD

## Goal

<2-3 sentences answering: What concrete change are we making, and why?>

## Out of Scope

<Bulleted list of adjacent features explicitly excluded from this change. Use `N/A — none identified` only if you have actively considered and ruled out adjacent scope.>

- <Excluded item 1, with reason>
- <Excluded item 2, with reason>

## Files to Touch

| File | Change Type | Reason |
|---|---|---|
| `src/path/to/file.ts` | Modify | <one-line reason> |
| `src/path/to/test.spec.ts` | Add | Test coverage for the new behavior |

(List all files. Do not write `several files in src/` — write the actual paths.)

## Implementation Steps

- [ ] Step 1: <Concrete action — reference specific file, function, or behavior>
      → verify: <concrete check — e.g., `npm test passes`, unit test for X returns Y>
- [ ] Step 2: <Concrete action>
      → verify: <concrete check>
- [ ] Step 3: <Concrete action>
      → verify: <concrete check>
- [ ] Step 4: Add or update tests in `<test path>`
      → verify: new tests pass; no existing tests regress
- [ ] Step 5: Run verification (see below)
      → verify: all commands in the Verification section exit 0

(Each step must be small enough to execute in one focused edit. Include a concrete `→ verify:` check per step so success criteria are unambiguous.)

## Verification

Run the project's actual commands (collected from Step 2 of the `ywc-plan` workflow):

```bash
<lint command>
<typecheck command>
<test command>
<build command>
```

Expected outcome: all commands exit 0, no new warnings introduced.

## Risks and Rollback

| Risk | Likelihood | Mitigation / Rollback |
|---|---|---|
| <Risk 1> | Low / Medium / High | <How to detect, how to revert> |

(Use `N/A — no operational risk` only when the change is purely additive and self-contained.)

## Acceptance Criteria

- [ ] <Observable outcome 1>
- [ ] <Observable outcome 2>
- [ ] Verification commands above all pass
```

## Worked Example

For a request like *"Fix the 500 error in the export endpoint when CSV has UTF-8 BOM"*:

```markdown
# Plan: Strip UTF-8 BOM from CSV export input before parsing

> Status: Ready for implementation
> Scale: Small
> Created: 2026-05-01

## Goal

The CSV export endpoint returns 500 when the user-uploaded CSV contains a UTF-8 BOM. Strip the BOM defensively before parsing so the endpoint returns 200 with correct rows.

## Out of Scope

- Other character-encoding issues (e.g., UTF-16, latin-1) — defer to a separate ticket
- General CSV parser replacement — current parser is fine, only BOM is broken
- `N/A — frontend changes` (this is server-side only)

## Files to Touch

| File | Change Type | Reason |
|---|---|---|
| `api/src/routes/export/csv-import.ts` | Modify | Strip BOM in the request handler before passing to parser |
| `api/src/routes/export/__tests__/csv-import.test.ts` | Modify | Add a test case for BOM input |
| `api/src/routes/export/fixtures/with-bom.csv` | Add | Fixture file containing a UTF-8 BOM |

## Implementation Steps

- [ ] Add `with-bom.csv` fixture under `api/src/routes/export/fixtures/`
- [ ] In `csv-import.ts`, after reading the request body and before parsing, strip a leading `﻿` if present
- [ ] Add a unit test in `csv-import.test.ts` that loads `with-bom.csv` and asserts a 200 response with parsed rows
- [ ] Run verification

## Verification

```bash
pnpm lint api/src/routes/export
pnpm typecheck
pnpm test api/src/routes/export
pnpm build
```

Expected: all pass, no new warnings.

## Risks and Rollback

| Risk | Likelihood | Mitigation / Rollback |
|---|---|---|
| Stripping BOM could affect non-CSV content types | Low | Conditional on `Content-Type: text/csv` — revert by removing the strip line |

## Acceptance Criteria

- [ ] BOM-prefixed CSV uploads return 200 with all rows parsed
- [ ] Non-BOM CSV uploads still return 200 (no regression)
- [ ] Verification commands all pass
```
