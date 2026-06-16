# Convergence and Stall Detection

This reference defines how `ywc-spec-ready` decides that a loop is no longer
making progress and must stop before the iteration cap. All three guards are
evaluated after each `DONE_WITH_CONCERNS` validation, before the next re-plan.

## Inputs computed per iteration

From each `ywc-spec-validate` report, compute and retain:

- **Critical count** — integer from the report Summary line.
- **Warning count** — integer from the report Summary line.
- **Finding signatures** — a normalized set, one entry per Critical/Warning
  finding: the tuple `(severity, pointer, first-sentence)` where:
  - `severity` = `Critical` | `Warning`
  - `pointer` = the `file:line` or section anchor the finding cites (normalized:
    strip surrounding brackets, lowercase the path)
  - `first-sentence` = the finding description up to the first `.` or `—`
  - Normalization order: match on `(severity, pointer)` first; fall back to
    `first-sentence` only when the pointer is absent. This makes "same defect,
    reworded" still count as a recurrence (pointer match is sufficient).
- **Amendment scope** — after the re-plan, the set of section/AC/FR identifiers
  named in the new `## Iteration N Amendments` block (e.g. `A1`, `AC16`, `FR-7`).

## The three stall guards

Stop the loop with Completion Status `DONE_WITH_CONCERNS` and action
`stop-non-converging` when **any** guard fires:

| Guard | Stop condition |
|---|---|
| Non-decreasing Criticals | Critical count increases, OR stays unchanged for **two consecutive** iterations whose signature sets overlap. A single transient increase after one re-plan does **not** fire — amendments may legitimately open new surface (e.g. a PERSIST fix exposing a lifecycle cluster). |
| Repeated signature | The same Critical signature appears in two consecutive validation reports after a re-plan — the re-plan failed to resolve it. Report the repeated signature. |
| Identical amendment scope | The new amendment scope equals the previous iteration's amendment scope (same identifiers) — `ywc-plan` is producing the same fix, so the loop cannot converge. This mirrors `ywc-agentic`'s recursion guard (`claude-code/skills/ywc-agentic/SKILL.md:185`). |

## Why two-consecutive, not one

The motivating case study (docker-isolate spec) converged in 4 manual iterations
where Critical counts moved 8 → 5 → 2 → mechanical. An R2 PERSIST fix opened an
R3 lifecycle cluster — a transient non-decrease that still converged. A
one-iteration guard would have aborted a healthy run. Requiring two consecutive
non-decreasing iterations with overlapping signatures distinguishes "opened new
surface, still progressing" from "genuinely stuck".

## Deterministic aid (advisory)

Signature and scope comparison is LLM judgment, consistent with the
`ywc-agentic` precedent (prose "effectively identical"). For a cheaper
cross-check, `git diff --name-only` between the pre- and post-amendment spec file
states is empty when `ywc-plan --update-spec` wrote nothing — an immediate
identical-scope signal. Use it to corroborate, not replace, the scope guard.
