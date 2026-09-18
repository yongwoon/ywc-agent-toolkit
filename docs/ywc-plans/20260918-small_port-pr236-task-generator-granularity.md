# Port PR #236 (develop-with-llm) — task-generator granularity size guideline & mode-aware Advisor fix (Claude Code only)

## What

Port `develop-with-llm` PR #236 ("task-generator: granularity size guideline
확장 및 mode-aware 검증 강화") into this repo's `ywc-task-generator` skill,
**Claude Code root only** (`claude-code/skills/`) — `codex/skills/` is
explicitly out of scope for this port. Three changes:

1. **Size guideline expansion** — `human` mode from ~10 files/~300 LOC to
   ~12-15 files/~400-500 LOC (~1 hour review budget); `llm` mode from
   ~25 files/~800 LOC to ~30 files/~1,000 LOC (baseline: Sonnet 5). Applied
   consistently across `README.md`, `SKILL.md`, and
   `references/granularity-modes.md`.
2. **Mode-aware Planning Advisor fix** — the Planning Advisor payload
   (`SKILL.md` §Planning Advisor, "How to invoke") gains an explicit
   "Selected Granularity Mode and size guideline" payload item carrying only
   the confirmed mode's single applicable guideline. The advisor's task-size
   verification instruction changes from a hardcoded "~10 files or ~300 LOC"
   (always the `human`-mode number, regardless of the mode actually
   selected) to "the selected Granularity Mode's size guideline (passed
   above)".
3. **Guideline-is-not-a-hard-cap note** — `references/granularity-modes.md`
   gains a short paragraph clarifying the numbers approximate a fixed
   qualitative criterion (reviewable-in-one-PR / vertical-slice-in-one-session)
   and that a future model upgrade is not by itself grounds to re-raise them.
   Adapted from upstream: upstream's note points at that project's
   `ROADMAP.md` "usage-data readiness checklist" for re-evaluation criteria —
   this repo has no `ROADMAP.md`, so the ported note states the
   no-automatic-re-raise principle without pointing at any specific document.

## Why

This repo's `ywc-task-generator/SKILL.md` §Planning Advisor (`How to invoke`,
"Task size verification") hardcodes "~10 files or ~300 LOC" as the advisor's
size-check threshold regardless of which Granularity Mode was actually
selected — confirmed by reading the current file
(`claude-code/skills/ywc-task-generator/SKILL.md:218`). When `llm` mode is
selected (~25-30 files budget), the advisor is instructed with the `human`
mode's much smaller number, causing it to flag correctly-sized `llm`-mode
tasks as oversized. This is the exact bug upstream PR #236 fixed. The size
guideline expansion (upstream's stated motivation: `human` ~1 hour review
budget observed to fit more than ~10 files/~300 LOC in practice; `llm` sized
against the Sonnet 5 baseline) is adopted alongside the fix since the
Advisor's corrected instruction directly references these numbers.

## Out of Scope

- `codex/skills/ywc-task-generator/` — user explicitly scoped this port to
  Claude Code only (`skill, agent` for Claude Code). Codex's granularity
  numbers, evals, and example-decomposition changes from PR #236 are not
  ported in this pass.
- The "cross-feature bundling" wording changes upstream made to its
  `llm` mode vertical-bundling rules — verified
  (`grep -n "cross-feature reuse" claude-code/skills/ywc-task-generator/references/granularity-modes.md:59`)
  this repo's file already carries equivalent unchanged language ("no
  cross-feature reuse"). Nothing to port there.
- Upstream's `.coderabbit.yaml`, `.ywc-learnings.jsonl`, `TODO.md`,
  `docs/ywc-plans/20260902-*-task-generator-granularity-expansion.md`,
  `tasks/completed/yw-00001{7,8,9}-*`, `tasks/dependency-graph.md`, and
  `tools/scripts/run_task_generator_evals.py` changes — those are
  upstream-repo-specific execution artifacts (that project's own task batch,
  learnings log, and eval runner), not portable content.
- Any change to `evals/evals.json` under this repo's
  `claude-code/skills/ywc-task-generator/` — upstream's 4 new evals were
  added to the codex-skill bundle only (out of scope per above); no
  equivalent Claude Code eval file exists to extend.
- Pointing the new "not a hard cap" note at a `ROADMAP.md`-style external
  document — this repo has no such document; the note states the principle
  without a dangling reference (see What §3).

## Files to touch

- `claude-code/skills/ywc-task-generator/README.md` — size guideline table
- `claude-code/skills/ywc-task-generator/SKILL.md` — size guideline bullets
  (§1 Reviewability), granularity-mode prompt text (§5), Planning Advisor
  payload + task-size-verification instruction (§6 Planning Advisor)
- `claude-code/skills/ywc-task-generator/references/granularity-modes.md` —
  Mode Comparison table row, not-a-hard-cap note, `llm` mode vertical
  bundling rule number

## Implementation Steps

- [ ] `README.md`: update the Mode / Size guideline table — `human` row to
      `~12-15 files / ~400-500 LOC`, `llm` row to `~30 files / ~1,000 LOC`,
      per `/tmp/pr236-cc.diff` lines 1-18 (table cell/column-width diff only,
      no prose change beyond the numbers and the `~1시간 review budget` /
      `baseline: Sonnet 5` additions already in upstream's cell text)
- [ ] `SKILL.md` §1 Reviewability (~line 64-65): update both bullet numbers
      and their parenthetical qualifiers to match
      `/tmp/pr236-cc.diff` lines 24-34
- [ ] `SKILL.md` §5 mode-selection prompt (~line 175-176): update both
      inline numbers to match `/tmp/pr236-cc.diff` lines 38-42
- [ ] `SKILL.md` §Planning Advisor "How to invoke" bullet list (~line 213):
      add the new "Selected Granularity Mode and size guideline" payload
      item verbatim from `/tmp/pr236-cc.diff` line 50 (numbers already
      updated to this repo's ported values)
- [ ] `SKILL.md` §Planning Advisor "Ask the advisor for three things" item 2
      (~line 218): replace the hardcoded "~10 files or ~300 LOC" with "the
      selected Granularity Mode's size guideline (passed above)" per
      `/tmp/pr236-cc.diff` line 56 — this is the mode-insensitivity bug fix
- [ ] `references/granularity-modes.md` Mode Comparison table (~line 19):
      update Size guideline row to the new numbers per
      `/tmp/pr236-cc.diff` lines 68-69
- [ ] `references/granularity-modes.md`: insert the not-a-hard-cap note
      after the Mode Comparison table (~line 27), adapted from
      `/tmp/pr236-cc.diff` line 77 — drop the `ROADMAP.md` clause, keep the
      qualitative-criterion + no-automatic-re-raise-on-model-upgrade
      statement. Suggested wording: "The numbers above are guidelines, not
      hard caps — they approximate a fixed qualitative criterion: `human`
      means \"reviewable in a single PR within a ~1 hour review budget\";
      `llm` means \"one feature vertical slice, completable and
      build+test-verified in one worktree session on the project's current
      baseline model (Sonnet 5).\" A future model upgrade is not by itself
      grounds to re-raise these numbers — re-evaluate deliberately, against
      observed task-generation outcomes, not automatically."
- [ ] `references/granularity-modes.md` `llm` mode vertical bundling rule
      (~line 58): update `~25 files / ~800 LOC` to `~30 files / ~1,000 LOC`
      per `/tmp/pr236-cc.diff` lines 86-87

## Verification

- [ ] `bash scripts/validate.sh` — mirrors CI, confirms skill structure
      (frontmatter, README locale set) still passes after the edits
- [ ] `grep -rn "~10 files\|~300 LOC\|~25 files\|~800 LOC" claude-code/skills/ywc-task-generator/` —
      expect zero remaining hits (confirms no stale number left behind)
- [ ] `grep -n "Selected Granularity Mode and size guideline" claude-code/skills/ywc-task-generator/SKILL.md` —
      confirms the Advisor payload fix landed
- [ ] Manual read-through of the three edited files to confirm no broken
      cross-reference or table formatting

## Risks / Rollback

- **Risk**: numbers referenced in more than the 7 identified locations (a
  stale copy elsewhere in the skill or in a translated `README.*.md`).
  Mitigated by the post-edit grep sweep in Verification.
- **Risk**: none of these are behavior-breaking — this is a documentation
  guideline change with no script or executable logic touched, so rollback
  is a plain `git revert` of the single commit with no data or state
  implications.
