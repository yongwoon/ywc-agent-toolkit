# Port PR #225: Alternatives Considered / Trade-offs excerpt in ywc-create-pr (Claude Code only)

## Goal

Port the "Alternatives Considered" / "Trade-offs" opportunistic excerpt feature from
`develop-with-llm` PR #225 into this repo's **Claude Code** `ywc-create-pr` skill
(`claude-code/skills/ywc-create-pr/SKILL.md`). When Step 6.6 matches a plan document
(`source: "plan"`), it should also look for a `## Alternatives Considered` or
`## Trade-offs` heading in the same already-bounded read and, when found, Step 7 renders
it as a further localized sub-block appended after the existing Goal/Purpose excerpt in
the Design Background section — never inventing content when the heading is absent.

## Out of Scope

- `codex/skills/ywc-create-pr/` — explicitly excluded per user instruction ("claude code 만 대상"). Codex is maintained independently per `claude-code/skills/CLAUDE.md` ("Codex-skill: Maintained Independently") and is not touched by this change.
- Any other skill.
- Changing the existing byte-cap extraction mechanism (`head -c 8192 <plan_path>`) — the new extraction reuses the same bounded window, it does not introduce a second read.
- `source: "task"` path — task `README.md`'s `## Spec Reference` has no equivalent Alternatives/Trade-offs section; sub-step 6 is already skipped for `source: "task"` and stays skipped.
- Upstream's own file (`tools/claude-code/skills/ywc-create-pr/SKILL.md` in `develop-with-llm`) — this repo's path is `claude-code/skills/ywc-create-pr/SKILL.md`; no changes are pushed upstream.

## Existing Constraints Touched

- `claude-code/skills/ywc-create-pr/SKILL.md:237` (Step 6.6 sub-step 6) already diverges from upstream at PR #225's time: it bounds the plan-file read to `head -c 8192 <plan_path>` (never a full-file `Read`) before extracting the Goal/Purpose excerpt. This constraint must carry over unchanged — the new Alternatives/Trade-offs lookup happens **within the same 8 KB window**, not a second unbounded read.
- `claude-code/skills/ywc-create-pr/SKILL.md:265-297` (Step 7 Design Background block) already has a 5-language localized table (en/ko/ja/zh/es) for the heading + intro line, and a `source: "plan"` render template ending in `<excerpt text, verbatim>`. The new sub-block must follow the same table-driven localization pattern and append after this existing block, not replace it.
- `claude-code/skills/ywc-create-pr/SKILL.md:301` — body is written to a temp file and passed via `--body-file "$body_file"` specifically to avoid an embedded literal `EOF` in quoted plan text closing a heredoc early. This is unrelated to the new feature and must not be disturbed (no change needed here beyond ensuring the new quoted text follows the same "verbatim, not translated" rule already stated on this line's neighbor at line 297).

## Files to Touch

- `claude-code/skills/ywc-create-pr/SKILL.md` — only file touched.

## Implementation Steps

- [ ] **Step 6.6 sub-step 6 (line 237)**: extend the existing sentence to also look for a `## Alternatives Considered` or `## Trade-offs` heading (whichever appears first) within the same `head -c 8192` window already used for the Goal/Purpose excerpt, same 5-line/~500-character cap. Mark it explicitly opportunistic: no plan template guarantees the section exists, so absence is the normal case, not a gap to fill by inventing content. Update the "Hold" sentence to: `Hold {source: "plan", plan_path, excerpt, alternatives_excerpt?, alternatives_heading_kind?}` — `alternatives_excerpt` and `alternatives_heading_kind` (`"alternatives"` | `"trade-offs"`, recording which of the two source headings was actually found) present only when found. State that Step 7 uses `alternatives_heading_kind` to pick the matching localized sub-heading — never hardcode "Alternatives Considered" regardless of which heading the source file used.
- [ ] **Step 7 Design Background block (after line 295's `<excerpt text, verbatim>` code fence, before line 297's closing sentence)**: insert a new paragraph describing the optional Alternatives/Trade-offs sub-block — appended after the existing excerpt block, `source: "plan"` only, present only when `alternatives_excerpt` was held. Include the 5-language sub-heading table (en/ko/ja/zh/es), each row split into the `"alternatives"` column (`### Alternatives Considered` / `### 검토했던 대안 (Alternatives Considered)` / `### 検討した代替案 (Alternatives Considered)` / `### 已考虑的替代方案 (Alternatives Considered)` / `### Alternativas consideradas (Alternatives Considered)`) and the `"trade-offs"` column (`### Trade-offs` / `### 트레이드오프 (Trade-offs)` / `### トレードオフ (Trade-offs)` / `### 权衡取舍 (Trade-offs)` / `### Compensaciones (Trade-offs)`), followed by the render template (localized sub-heading + `<alternatives_excerpt text, verbatim>`). State explicitly: never default to the `"alternatives"` row when `alternatives_heading_kind` is `"trade-offs"`; omit the whole sub-block when `alternatives_excerpt` is absent.
- [ ] **Line 297 closing sentence**: extend `The quoted \`summary\`/\`excerpt\` text itself stays verbatim` to `The quoted \`summary\`/\`excerpt\`/\`alternatives_excerpt\` text itself stays verbatim` so the "not translated" rule explicitly covers the new field.
- [ ] Re-read the full Step 6.6 → Step 7 region after editing to confirm the `{source: "plan", ...}` payload shape mentioned in sub-step 8 ("Hold the final result") stays consistent with the extended shape from sub-step 6 (no separate edit needed there since it already says `{source: "plan", ...}` generically, but verify no contradiction was introduced).

## Interfaces

N/A — single file, no cross-file signature shared.

## Verification

- `python3 tools/scripts/validate_ywc_skills.py --skill-root claude-code/skills` if present in this repo — otherwise run this repo's equivalent: `bash scripts/validate.sh` (mirrors CI: skill structure + shellcheck + `--list` dry run).
- Manual read-through: confirm Step 6.6 sub-step 6 and Step 7's Design Background block read consistently end-to-end (no orphan reference to `alternatives_excerpt`/`alternatives_heading_kind` without a corresponding definition), matching this repo's existing self-consistency bar for `ywc-*` skill edits.
- `git diff --stat` shows exactly one file changed: `claude-code/skills/ywc-create-pr/SKILL.md`.
- Confirm no edits landed in `codex/skills/ywc-create-pr/` (Out of Scope guard).

## Risks / Rollback

- **Risk**: table-formatting drift (misaligned columns, wrong language row) could silently corrupt an unrelated language's rendering. Mitigation: copy the exact 5-language cell text from upstream PR #225's diff (already captured in this plan's Implementation Steps) rather than re-deriving translations.
- **Risk**: forgetting the `alternatives_heading_kind` selection logic could cause the skill to always render "Alternatives Considered" even when the source used "Trade-offs" — this was itself the subject of a follow-up fix commit in the upstream PR (`d4f1c91a`). Mitigation: the plan explicitly carries that distinction into sub-step 6 and Step 7 from the start, rather than requiring a second fix pass.
- **Rollback**: single-file, additive-only change (no deletions of existing behavior) — revert via `git checkout <prior-commit> -- claude-code/skills/ywc-create-pr/SKILL.md` if the rendered PR body regresses.
