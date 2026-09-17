# yw-000044-020-docs-add-readonly-exception-section — Implementation Checklist

## Prerequisites
- [ ] None — this is a root task.

## Allowed Edit Scope
- [ ] Stay within declared Ownership from `README.md` — `claude-code/skills/references/subagent-status-actions.md` only
- [ ] If the task requires edits outside Ownership, stop and report before proceeding

## Stop Conditions
- [ ] Stop if `## Return Payload Contract`'s existing table/`MUST NOT` list has drifted in structure enough that "immediately after" is ambiguous — report and ask rather than guess a position
- [ ] Stop if inserting the subsection would require renumbering or renaming any of the file's other 3 top-level headings

## Implementation Steps
- [ ] Re-`grep -n "^## " claude-code/skills/references/subagent-status-actions.md` to confirm current line numbers before editing (file may have shifted since this task was generated)
- [ ] Insert `### 3.5. Read-only review-worker exception` immediately after the existing `MUST NOT` bullet list and before the `## BLOCKED Triage` heading
- [ ] Write the subsection body: state that agents whose `tools:` omits `Write` return the full canonical payload (Status, Summary, Concerns, Blocker, Missing context) inline, never to a file, and that `Artifacts` is the only field legitimately omitted
- [ ] Add one bounded example payload inside the new subsection showing Status + Summary + a findings-or-verdict field + Concerns + Blocker + Missing-context together (e.g. a `BLOCKED` example, since that status exercises the most fields)
- [ ] Do not touch `## Status Responses`, `## BLOCKED Triage`, or `## Aggregating Status` headings or their numbering

## Task Verify
- [ ] `grep -n "^### 3.5" claude-code/skills/references/subagent-status-actions.md` shows the new heading (AC2)
- [ ] `grep -n "^## " claude-code/skills/references/subagent-status-actions.md` still shows exactly the same 4 top-level headings, unchanged and unrenumbered
- [ ] Read the new subsection back and confirm the example payload includes all of Status/Summary/Findings-or-verdict/Concerns/Blocker/Missing-context

## Verification
- [ ] `bash scripts/validate.sh` exits 0 (no separate lint/typecheck/test/build commands apply to a Markdown reference-doc edit)

## Implementation Notes (optional)
