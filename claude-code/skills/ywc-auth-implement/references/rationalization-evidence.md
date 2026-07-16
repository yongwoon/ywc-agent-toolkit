# Rationalization Evidence — Baseline and Forward-Test per Row

For each `## Rationalization Defense` row in `SKILL.md`, this records the baseline failure evidence (why the excuse is tempting and what it produces if followed) and the forward-test evidence (how to recognize the correct behavior actually happened). No application code execution is required to record either — both are document-level checks against the interview record, the dispatch prompts, and the skill's own output.

## Row 1 — "Only OAuth is needed, skip the full interview"

- Baseline: skipping non-OAuth categories drops session TTL/rotation and abuse-prevention decisions silently, because those categories are framed as "password-related" when they are not.
- Forward test: the Policy Interview Summary output lists all 9 categories with a state for each (approved, deferred, or "not applicable" — never "skipped").

## Row 2 — "A hand-rolled JWT/password-hashing implementation would be faster"

- Baseline: an inline crypto suggestion in the recommendation or dispatch prompt text is the earliest signal this excuse won; it compounds into a Critical finding at the `ywc-security-audit` gate.
- Forward test: `grep`-style check that neither the Recommendation output nor the FR-6 dispatch prompts contain a hand-rolled hashing/signing suggestion — only a named library/service.

## Row 3 — "MFA can be added in a follow-up task"

- Baseline: MFA silently absent from the Policy Interview Summary with no recorded risk statement.
- Forward test: the MFA category's recorded state is either `approved` or `deferred (risk: ...)` — never simply absent from the summary.

## Row 4 — "Security audit passed on the previous run, cache the recommendation now"

- Baseline: a cache-eligible marking recorded before the E2E gate ran.
- Forward test: cross-check the Security/E2E Gate output section — cache eligibility text only appears after both the audit (Critical/High = 0) and E2E evidence lines are present together.

## Row 5 — "The legal draft reads complete, present it as final"

- Baseline: a `ywc-doc-writer` output missing the "draft pending legal review" label, or the label present only in one of the two documents.
- Forward test: both the ToS and Privacy Policy drafts open with the mandatory label from `references/legal-pages-template.md`.

## Row 6 — "Just list the frameworks this skill supports so recommendations are consistent"

- Baseline: any inline "supported stack" list appearing in `SKILL.md` or `references/`.
- Forward test: `rg` sweep across `claude-code/skills/ywc-auth-implement/` for allowlist-style phrasing (e.g., "supported frameworks:", "only works with") returns no matches — recommendations always cite evidence, never a static list.
