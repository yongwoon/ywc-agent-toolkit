# yw-000044-020-docs-add-readonly-exception-section

## Purpose
All 12 `claude-code/agents/ywc-*.md` files (and `claude-code/agents/CLAUDE.md:126`) hardcode a pointer to "`§3.5`" of `claude-code/skills/references/subagent-status-actions.md` for the canonical return-payload format — but that file's 4 existing top-level headings carry no numbering at all, so `§3.5` resolves to nothing (a dead link). This task adds a literal `### 3.5. Read-only review-worker exception` heading, making the pointer addressable while also defining the bounded inline payload shape the 7 read-only agents (fixed in `yw-000044-010`) now reference.

## Scope
- Insert a new subsection immediately under `## Return Payload Contract`, after its existing table and `MUST NOT` list, headed literally `### 3.5. Read-only review-worker exception`.
- Content: state that agents whose `tools:` grant omits `Write` return the full canonical payload (Status, Summary, Concerns, Blocker, Missing context) inline in the response text, never to a file, and that `Artifacts` is the only canonical field legitimately omitted (no file exists to point to).
- Include one bounded example payload showing Status/Summary/Findings-or-verdict/Concerns/Blocker/Missing-context together, so a `BLOCKED` or `NEEDS_CONTEXT` return from one of these agents is not missing a field that `## BLOCKED Triage` depends on.

## Spec Reference

### Primary Sources
- `docs/ywc-plans/20260917-readonly-agent-inline-return.md` FR-2, AC2, Amendment Log Iteration 1

### Summary
The file's 4 existing headings (`## Status Responses`, `## Return Payload Contract`, `## BLOCKED Triage`, `## Aggregating Status`) carry no numbers — `§3.5` is a literal fixed label to add as a real heading, not a position in an actual numbering scheme, and the other 3 headings must not be renumbered or otherwise touched. The new subsection lives inside `## Return Payload Contract` (a `###`-level child), positioned after that section's existing table and `MUST NOT` bullet list, before the section ends. This task's fix is purely additive — the file's existing content changes only by insertion, nothing is deleted or reworded.

### Out of Scope (from spec)
- Renumbering or restructuring the file's other 3 top-level headings
- Editing any of the 12 `claude-code/agents/ywc-*.md` files or `claude-code/agents/CLAUDE.md` — their `§3.5` pointer text already resolves correctly once this heading exists; no change needed to them
- The write-to-file contradiction inside the 7 read-only agents (handled by `yw-000044-010`)

## Criticality
`normal` — documentation-only edit to a shared reference doc describing subagent return-payload conventions; no auth, payment, secret-handling, or PII-adjacent code is touched.

## Dependencies

### Depends On
- (None — root task, parallel with `yw-000044-010`)

### Depended By
- (None — leaf task for the immediate spec; the pointer text in all 12 agent files already references `§3.5` verbatim and needs no edit once this heading lands)

## Key Files
- `claude-code/skills/references/subagent-status-actions.md` — new `### 3.5. Read-only review-worker exception` subsection inserted under `## Return Payload Contract` (currently lines 14-41; the new subsection goes after line 41, before the `## BLOCKED Triage` heading at line 43)

## Notes
- Be aware that `claude-code/skills/CLAUDE.md`'s own "Subagent Return Payload Contract and Structured Surface-to-User" section already informally labels the *entire* `## Return Payload Contract` section as "`(§3.5)`" in its own prose (`**Return payload (§3.5)** — every subagent prompt must include a directive...`). This task adds a literal, narrower `### 3.5.` heading for a *different* sub-topic (the read-only exception) inside that same section. This is a pre-existing minor labeling overlap already acknowledged in the spec's Amendment Log Iteration 1 ("§3.5 is a literal fixed label... not a position to renumber into") — not something this task needs to reconcile; do not edit `claude-code/skills/CLAUDE.md` as part of this task.
- The example payload must include all 5 of Status/Summary/Findings-or-verdict/Concerns/Blocker/Missing-context together in one example so a `BLOCKED` or `NEEDS_CONTEXT` return is never missing a field `## BLOCKED Triage` depends on — do not split this into multiple smaller examples per status.
- As a side effect, this task's fix also repairs the same dead `§3.5` link for the 5 write-capable agents that reference it (`ywc-backend-coder`, `ywc-cloud-engineer`, `ywc-doc-writer`, `ywc-frontend-coder`, `ywc-refactor-cleaner`) — no change to those files is needed.

## Parallel Execution Metadata

### Ownership
- `claude-code/skills/references/subagent-status-actions.md`

### Owned Interface
- The literal heading text `### 3.5. Read-only review-worker exception` — all 12 agent files' existing `§3.5` pointer text depends on this exact addressable anchor existing; do not rename it

### Shared Surfaces
- `§3.5` pointer text referenced (read-only, not modified) by all 12 `claude-code/agents/ywc-*.md` files and `claude-code/agents/CLAUDE.md:126`

### Conflicts With
- (None identified — `yw-000044-010` and `yw-000044-030` do not touch this file)

### Parallelizable After
- (Root task — no predecessor required)

### Task Verify
- `grep -n "^### 3.5" claude-code/skills/references/subagent-status-actions.md` — confirms the heading exists (AC2)
- Manual read-through confirming the new subsection's example payload contains Status, Summary, a findings-or-verdict field, Concerns, Blocker, and Missing-context, and explicitly states `Artifacts` is the only omitted canonical field (AC2)

## Out of Scope
- Any change to the 7 read-only agents' body text (handled by `yw-000044-010`)
- Any change to `scripts/validate.sh` (handled by `yw-000044-030`)
- Renumbering the file's 4 existing top-level headings
