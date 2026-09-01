# yw-000011-010-refactor-skill-author-activation-router — Implementation Checklist

## Prerequisites

- [ ] Confirm `docs/ywc-plans/20260901-small_codex-skill-creator-token-efficiency.md` remains the source of truth and the working tree has no conflicting `ywc-skill-author` edits.

## Allowed Edit Scope

- [ ] Stay within the `README.md` Ownership paths, including the generated plugin mirror only through `bash scripts/sync-codex-plugin.sh`.
- [ ] Stop and report before any `claude-code/**`, installed-skill, or unrelated skill edit.

## Stop Conditions

- [ ] Stop if `tiktoken` or `o200k_base` is unavailable; record the missing reproducibility prerequisite rather than substituting a tokenizer.
- [ ] Stop if retaining A1–A16, Rationalization Defense, RED → GREEN → REFACTOR, audit safety, validation, and completion checks cannot meet the threshold without changing required behavior.
- [ ] Stop if a fresh-context audit response routes to `authoring-rules.md`, edits a target, or authorizes deletion.
- [ ] Stop if an interface metadata change would alter the user-facing purpose without a spec-backed reason.

## Hardening Gate

- [ ] Classify as behavior-changing documentation/skill-router refactor with generated output.
- [ ] Before edits, record the immutable baseline metrics and existing authoring/audit response contract in the evidence artifact.
- [ ] Treat the inline rule/audit index plus explicit authoring-route behavior as the contract; return `NEEDS_CONTEXT` if the spec and current skill disagree on a mandatory rule.
- [ ] Data Integrity Hardening is N/A; use `bash scripts/sync-codex-plugin.sh` as the sole generated-output path.
- [ ] Critical-surface full review is N/A; preserve the focused structural and fresh-context behavior evidence.

## Implementation Steps

- [ ] Measure and record the exact baseline for `codex/skills/ywc-skill-author/SKILL.md` (lines, words, bytes, and `o200k_base` tokens) in `docs/ywc-plans/evidence/20260901-small_codex-skill-creator-token-efficiency.md`.
- [ ] Build the A1–A16 and audit-invariant ledger in that evidence file, assigning every rule one canonical final location, applicable modes, and a structural, behavioral, or manual witness.
- [ ] Add `codex/skills/ywc-skill-author/references/authoring-rules.md` with only create/restructure rationale, decision detail, and worked guidance; keep it substantive (at least 30 lines).
- [ ] Rewrite `codex/skills/ywc-skill-author/SKILL.md` as the compact always-loaded router: retain the announcement, Rationalization Defense, inline canonical rule/audit index, RED → GREEN → REFACTOR, report-only audit boundary, validation command, and completion checks; route only create/restructure work to `references/authoring-rules.md` before edits.
- [ ] Update `codex/skills/ywc-skill-author/evals/evals.json` with the compact-routing structural scenario, and review all `interface` fields in `agents/openai.yaml`; edit metadata only if it no longer describes the final router.
- [ ] Run the four required fresh-context scenarios (new-skill, restructure, audit, compact-routing), save unedited responses and pass/fail checklists in the evidence artifact, then run the exact local-Markdown-link check that excludes bundle-level prose references.
- [ ] Run focused validation, synchronize `plugins/ywc-agent-toolkit/skills/ywc-skill-author/**` from source, and run the repository validation without changing `claude-code/**`.

## Task Verify

- [ ] `wc -l -w -c codex/skills/ywc-skill-author/SKILL.md`
- [ ] `python3 -c 'import tiktoken; print(len(tiktoken.get_encoding("o200k_base").encode(open("codex/skills/ywc-skill-author/SKILL.md").read())))'` reports at most `4251` and the word count is below `3045`.
- [ ] `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-skill-author`
- [ ] Run the spec's fail-fast local-reference check after correcting it to enumerate direct Markdown links only.
- [ ] `bash scripts/run-codex-skill-contract-evals.sh`
- [ ] `bash scripts/sync-codex-plugin.sh && bash scripts/validate.sh`
- [ ] `git diff --check && git diff --exit-code -- claude-code/`

## Verification

- [ ] Targeted structural validation passes with `bash codex/skills/ywc-skill-author/scripts/validate-skill.sh codex/skills/ywc-skill-author`.
- [ ] Contract JSON validation passes with `bash scripts/run-codex-skill-contract-evals.sh`.
- [ ] Repository validation and generated-package freshness pass with `bash scripts/sync-codex-plugin.sh && bash scripts/validate.sh`.
- [ ] Manual forward-test evidence covers all four required scenarios and does not claim that the structural eval script executed them.

## Implementation Notes (optional)
