# Plan: Preserve the source heading kind in Codex `ywc-create-pr`

> Status: Implemented
> Scale: Small
> Created: 2026-09-02
> Upstream reference: [develop-with-llm PR #225](https://github.com/yongwoon/develop-with-llm/pull/225)
> Scope: Codex only

## Goal

Port the full Codex behavior from upstream PR #225: when a matched plan document is used as PR design context, optionally extract its `## Alternatives Considered` or `## Trade-offs` section and render it as a localized sub-block. Preserve which source heading was found so `Trade-offs` remains `Trade-offs` and `Alternatives Considered` remains `Alternatives Considered`, without changing the Claude Code bundle or unrelated PR-creation behavior.

## Out of Scope

- Any `claude-code/**` change — this plan is Codex-only.
- Changes to PR creation, CI, bot-review, merge-readiness, language resolution, or plan matching beyond the bounded optional design-context excerpt and heading-kind propagation.
- Changes to README files, `agents/openai.yaml`, or `evals/evals.json`; the invocation contract and existing eval coverage are unchanged.
- Refactoring the generated plugin independently from the Codex source; the plugin copy is updated only through the repository sync script.

## Files to Touch

| File | Change Type | Reason |
|---|---|---|
| `codex/skills/ywc-create-pr/SKILL.md` | Modify | Carry `alternatives_heading_kind` from Step 6.6 into Step 7 and select the matching localized sub-heading. |
| `plugins/ywc-agent-toolkit/skills/ywc-create-pr/SKILL.md` | Regenerate | Keep the marketplace Codex package synchronized with the source of truth. |

## Implementation Steps

- [x] In `codex/skills/ywc-create-pr/SKILL.md` Step 6.6 sub-step 6, search the same bounded plan excerpt window for the first `## Alternatives Considered` or `## Trade-offs` section, capture its capped verbatim excerpt, and extend the held result with `alternatives_heading_kind` (`alternatives` or `trade-offs`); retain the no-section behavior when neither heading exists.
      → verify: the extraction contract records the optional excerpt and source heading kind without performing a second unbounded read.
- [x] In the Step 7 Design Background instructions, append the optional excerpt as a `source: "plan"`-only sub-block and select its localized label from `alternatives_heading_kind` for all supported languages.
      → verify: `## Trade-offs` maps to the `Trade-offs` row, `## Alternatives Considered` maps to the existing alternatives row, and absent headings produce no sub-block.
- [x] Run `bash scripts/sync-codex-plugin.sh` to regenerate `plugins/ywc-agent-toolkit/skills/ywc-create-pr/SKILL.md` from the Codex source.
      → verify: the source and generated skill files contain the same behavior, and no `claude-code/**` file is changed by this plan.
- [x] Run the repository validation and targeted Codex install/list checks.
      → verify: all commands in the Verification section exit 0.

## Verification

```bash
python3 -m json.tool codex/skills/ywc-create-pr/evals/evals.json >/dev/null
bash scripts/install.sh --list --codex
bash scripts/validate.sh
cmp codex/skills/ywc-create-pr/SKILL.md plugins/ywc-agent-toolkit/skills/ywc-create-pr/SKILL.md
```

Expected outcome: all commands exit 0; the source/package copy is synchronized; no Claude Code files or unrelated Codex skill files are changed.

## Risks and Rollback

| Risk | Likelihood | Mitigation / Rollback |
|---|---|---|
| The new metadata is captured but the output label still defaults to `Alternatives Considered`. | Low | Review both Step 6.6 and Step 7 together and verify both heading kinds by targeted text inspection; revert the single-file source change and re-run the sync if needed. |
| The generated plugin copy drifts from the source. | Low | Run `bash scripts/sync-codex-plugin.sh` and `cmp`; rollback by reverting the source change and regenerating the package. |

## Acceptance Criteria

- [x] Codex `ywc-create-pr` extracts and renders the optional plan `Alternatives Considered` / `Trade-offs` excerpt in the Design Background section.
- [x] Codex `ywc-create-pr` preserves `Trade-offs` versus `Alternatives Considered` when rendering that sub-block.
- [x] All five supported PR prose languages retain the matching localized label for both heading kinds.
- [x] The optional block remains omitted when no source alternatives/trade-offs heading is found.
- [x] The generated Codex plugin copy matches the updated source.
- [x] Verification commands above pass without changes outside the Codex `ywc-create-pr` source/package pair.

## Confidence Gate

Confidence: 98/100 — PROCEED

| Dimension | Score |
|---|---:|
| Scope clarity | 98 |
| Architecture compliance | 98 |
| Evidence quality | 100 |
| Reuse verified | 95 |
| Root cause identified | 100 |

## Handoff

Implemented according to this plan. The Codex source and generated plugin mirror are synchronized and verified.
