# yw-000021-030-docs-impl-review-localized-flow — Implementation Checklist

## Prerequisites

- [ ] `yw-000021-010-domain-impl-review-verification-contract` is completed and merged.

## Allowed Edit Scope

- [ ] Modify only the six README files listed in `README.md` Ownership.
- [ ] Stop and report if the work needs a SKILL, eval, plugin, or custom-agent edit.

## Stop Conditions

- [ ] Stop if the source skill has no settled user-facing wording for verification states or report counts.
- [ ] Stop if a locale cannot preserve its language while keeping identifiers and commands exact.
- [ ] Stop if documentation would promise a specific Claude-only model assignment.

## Hardening Gate

- [ ] Classify this task as docs-only.
- [ ] Record the named exception and replacement verification in `README.md` before edits.
- [ ] Consume the User-facing implementation-review flow contract; return `NEEDS_CONTEXT` on a terminology or consumer mismatch.
- [ ] Data Integrity Hardening is N/A because this is documentation-only.
- [ ] Critical surface review is N/A because this task changes no production behavior.

## Implementation Steps

- [ ] Update `README.en.md` first as the English source description.
  - [ ] Describe pre-dispatch empty/oversized-scope refusal and the unchanged five-axis review model.
  - [ ] Describe independent verification provenance and aggregate counts without claiming Sonnet, Haiku, or Opus assignments.
- [ ] Align `README.md`, `README.ko.md`, `README.ja.md`, `README.zh.md`, and `README.es.md` to the same contract.
  - [ ] Preserve locale prose and code examples while using generic Codex worker and Phase 2 advisor language.
  - [ ] Keep `[P1]`/`[P2]` provenance and verification status as separate user-visible dimensions.
- [ ] Inspect all six surfaces together.
  - [ ] Remove every Claude-only model claim.
  - [ ] Ensure scope and verification descriptions do not contradict `SKILL.md`.

## Task Verify

- [ ] `rg -n 'Sonnet|Haiku|Opus' codex/skills/ywc-impl-review/README*.md` returns no matches.
- [ ] `git diff --check -- codex/skills/ywc-impl-review/README*.md`

## Verification

- [ ] All six maintained locale files remain present.
- [ ] Source/package parity and structural validation are deferred to `yw-000022-010-infra-impl-review-package-validation`.

## Implementation Notes (optional)

