---
name: ywc-implement
description: >-
  (ywc) Use when the user asks to implement exactly one approved repository
  specification or ticket through a focused, review-gated change. Triggers:
  "implement approved spec", "implement ticket", "direct implementation",
  "승인된 명세 구현", "チケットを実装". Do not use for vague ideas (use
  ywc-brainstorm or ywc-plan), parallel multi-layer generation (use
  ywc-code-gen), or generated task directories (use ywc-sequential-executor).
---

# ywc-implement

**Announce at start:** "I'm using the ywc-implement skill to implement one approved specification or ticket."

Implement one approved item with a small, auditable change. This is the direct
single-item lane; it does not replace planning, generation, or task execution.

## Rationalization Defense

| Excuse | Reality |
|---|---|
| "The request sounds useful, so approval evidence is implied." | Missing approval or acceptance criteria is `NEEDS_CONTEXT`; route the request to `ywc-brainstorm` or `ywc-plan`. |
| "A task range is just several direct items." | Ranges belong to `ywc-sequential-executor`; accept exactly one `--spec` or `--ticket`. |
| "I can edit before capturing the baseline." | Capture a clean-tree check and `git rev-parse HEAD` before edits so the review boundary is provable. |
| "The neighboring module needs cleanup too." | Inspect existing patterns, but edit only the approved scope; unrelated cleanup changes the contract. |
| "The change is small enough to skip RED or review." | Behavior changes use `ywc-tdd-ritual` at the narrowest seam and every delivery runs `ywc-impl-review`. |
| "Review found a concern, but the commit is ready anyway." | `BLOCKED`, `NEEDS_CONTEXT`, or unresolved Critical/High findings prohibit delivery. |
| "A PR or force-push will make delivery easier." | This lane never creates PRs, force-pushes, or amends published commits without an explicit user request. |

## Input Gate

Accept exactly one input:

- `--spec <repo-relative-path>` — a readable approved specification containing
  an explicit marker such as `Status: Ready for implementation` or
  `Approved: yes`, plus acceptance criteria.
- `--ticket <reference>` — a readable ticket resolved before editing to a local
  immutable snapshot with the same marker and criteria.

Reject missing, duplicated, absolute, inaccessible, ambiguous, unapproved,
contradictory, or acceptance-criteria-free inputs with `NEEDS_CONTEXT`. A
resolved ticket must expose its repository-readable snapshot path and that path
become the `--spec` path passed to `ywc-impl-review`. Also reject raw ideas,
multiple specs/tickets, task ranges, and broad multi-layer generation; name the
appropriate sibling skill in the response.

## Execution

1. Read repository guidance, the approved input, and only relevant existing
   implementation and tests. Confirm the requested scope and out-of-scope work.
2. Require a clean working tree. Record `git rev-parse HEAD` as
   `baseline_sha`. Work on a feature branch; preserve any user work and stop if
   the baseline or branch requirement cannot be satisfied.
3. Inspect existing patterns and public boundaries. For behavior changes, run
   `ywc-tdd-ritual` RED → GREEN at the selected seam. Use focused checks while
   editing and keep tests with the behavior they cover.
4. Run the project's configured full verification once after focused checks.
   Fix implementation issues, never weaken assertions or hide failures.
5. Run `ywc-impl-review --spec <resolved-spec>` against the complete direct-lane
   change. If no TDD checkpoint commit exists, use `--working-tree`; after
   local TDD or correction checkpoints, use `--git-range <baseline_sha>..HEAD`.
   Resolve confirmed Critical/High findings in one bounded correction cycle,
   rerun affected checks and full verification, then re-review the same
   boundary. A range-mode correction may be a local unpublished checkpoint;
   after a `--working-tree` review, keep the correction uncommitted so that
   `--working-tree` sees it.
6. Only after review is clean may the lane create a conventional commit. No
   push, merge, PR, or final `DONE` status is allowed before that clean review
   gate; the lane never force-pushes or amends a published commit.

## Review and Status Gate

Use this status vocabulary:

- `NEEDS_CONTEXT` — input, baseline, branch, or required evidence is missing.
- `BLOCKED` — verification or review prevents safe delivery.
- `DONE_WITH_CONCERNS` — a re-review still has Critical/High findings after the
  bounded correction cycle, or only non-blocking observation concerns remain.
- `DONE` — verification passed, review passed, and the conventional commit was
  created.

One correction cycle means one implementation-and-verification pass for
confirmed Critical/High findings. Do not continue delivery after that cycle if
the findings remain unresolved.

## Output Format

```text
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Input: --spec <path> | --ticket <reference>
Changed files: <paths>
Verification: <command> (exit 0), ...
Implementation review: PASS | CONCERNS | BLOCKED | NEEDS_CONTEXT — <summary>
Commit: <sha> | N/A
Unresolved concerns: <items> | N/A
```

## Integration

- `ywc-tdd-ritual` supplies RED → GREEN discipline for behavior changes.
- `ywc-impl-review` is mandatory before delivery.
- `ywc-verify-done` may verify the final evidence but does not replace review.
- `ywc-code-gen` owns parallel Backend/Frontend/QA generation.
- `ywc-sequential-executor` owns generated task-directory lifecycles.

## Validation

The skill is complete only when its contract fixture covers approved and
rejected inputs, baseline/branch protection, review routing, and no-push
boundaries, and the repository's skill contract checks pass.
