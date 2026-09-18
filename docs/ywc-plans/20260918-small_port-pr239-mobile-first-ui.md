# Port PR #239: Mobile-First UI default (Claude Code skills only)

## Goal

Port `develop-with-llm` PR #239's mobile-first UI responsive default into this
repo's Claude Code skill set (`claude-code/skills/`) only. Add a new shared
reference `claude-code/skills/references/mobile-first-ui.md` and wire it into
the same 5 skills the source PR wired: `ywc-project-scaffold`,
`ywc-task-generator`, `ywc-plan` (`spec-template.md`), `ywc-sequential-executor`,
`ywc-parallel-executor`. Document the new shared reference in
`claude-code/skills/CLAUDE.md` following this repo's existing
"referenced-not-inlined" convention (same pattern as `pr-bot-polling.md`,
`schema/core.md`, `language-resolution.md`).

## Scale judgment

Touches 7 files but every edit is a short, mechanical, single-concern doc
addition (no DB migration, no new library, no executable-code behavior
change) — same category as the prior `PR #238` monorepo-reference port
(commit `3ed491dc`), which was likewise treated as Small despite exceeding
the raw file-count heuristic. Direct execution plan chosen over the
spec/task-decomposition path.

## Out of Scope

- Codex skill set (`tools/codex-skill/` equivalent does not exist in this
  repo's layout — `codex/skills/` is a separate, independently maintained
  tree per this session's explicit instruction: "claude code 용 skill, agent").
- Retrofitting any existing UI code in this repo to mobile-first (none
  exists — this repo ships skills/agents, not application UI).
- Any change to `ywc-code-gen`, `ywc-frontend-coder`, or other skills/agents
  not named in the source PR's wiring list.

## Files to touch

1. `claude-code/skills/references/mobile-first-ui.md` (new)
2. `claude-code/skills/ywc-project-scaffold/SKILL.md`
3. `claude-code/skills/ywc-task-generator/SKILL.md`
4. `claude-code/skills/ywc-plan/references/spec-template.md`
5. `claude-code/skills/ywc-sequential-executor/SKILL.md`
6. `claude-code/skills/ywc-parallel-executor/SKILL.md`
7. `claude-code/skills/CLAUDE.md`

## Existing Constraints Touched

- `claude-code/skills/CLAUDE.md` documents every top-level shared reference
  with a dedicated section (Bot Review Polling, PR Conflict Resolution, HTML
  Output Mode, Schema Guide, Language Resolution, Task Initials Resolution).
  New shared references must follow the same "no inline, referenced only"
  discipline — this plan adds one more such section rather than inlining the
  rule text in any consuming `SKILL.md`.
- `ywc-parallel-executor/SKILL.md:216` already centralizes its six universal
  subagent directives in `references/subagent-directives.md` (verbatim-append
  contract) — unlike the source PR's inline `SKILL.md` bullet, this repo's
  category-conditional Mobile-First directive is added as a **new bullet in
  Step 4b** (not inside `subagent-directives.md`, since that file's own
  preamble states its six directives are "shared across every task category" —
  a `ui`-only directive does not belong there).
- `ywc-task-generator/SKILL.md:258` already defines `ui` as an existing task
  category — no taxonomy change needed, only a new Implementation Steps
  sub-bullet (`SKILL.md:366-368` region).
- `ywc-sequential-executor/SKILL.md:285` already has a "Schema-aware
  implementation" callout in Step 3 with the exact structure to mirror
  ("Mobile-first UI implementation" callout, same paragraph shape).
- `ywc-plan/references/spec-template.md:127-131` NFR table — add one row,
  same shape as the source PR's addition.
- `ywc-project-scaffold/SKILL.md:151-158` Section 5 "Extras" — add the note
  before Section 6 begins (`SKILL.md:159`), same insertion point as source PR.

## Implementation Steps

- [ ] Create `claude-code/skills/references/mobile-first-ui.md` — port the
      source PR's `tools/claude-code/skills/references/mobile-first-ui.md`
      content verbatim, with one adjustment: replace the sentence "the same
      convention as [`criticality.md`](./criticality.md)" (no `criticality.md`
      exists in this repo) with a reference to this repo's actual
      referenced-not-inlined convention, e.g. "the same convention as
      [`pr-bot-polling.md`](./pr-bot-polling.md)". List all 5 consuming skills
      by name in the header sentence, matching source structure (Rule /
      Trigger / Escape hatch / Backward compatibility sections unchanged).
- [ ] `ywc-project-scaffold/SKILL.md` — insert the "Mobile-first UI note
      (frontend frameworks only)" paragraph after line 157 (end of Section 5
      bullets), before `### 6. Reference Refresh` at line 159. Link
      `../references/mobile-first-ui.md`.
- [ ] `ywc-task-generator/SKILL.md` — insert a new Implementation Steps
      sub-bullet after the "Example:" line (~line 368): "For a `ui` category
      task, order the base-layout step to target the mobile viewport first,
      with a later step expanding to tablet/desktop via `min-width`
      breakpoints — per [../references/mobile-first-ui.md](../references/mobile-first-ui.md),
      unless that file's escape hatch applies (state the exception in the
      step instead)".
- [ ] `ywc-plan/references/spec-template.md` — insert one row into the NFR
      table (after the `Scalability` row, ~line 131): `| Responsive
      (UI-touching only) | <e.g., "Mobile-first, \`min-width\` breakpoints"
      per [../references/mobile-first-ui.md](../../references/mobile-first-ui.md),
      or the stated PC/tablet-only exception> |`. Verify the relative path
      resolves correctly from `ywc-plan/references/` up to
      `claude-code/skills/references/` (two `../` levels, matching the
      existing `schema-invariants.md` link one line above at line 137, which
      also uses `../references/`).
- [ ] `ywc-sequential-executor/SKILL.md` — insert a new paragraph immediately
      after the "Schema-aware implementation" paragraph (~line 285), mirroring
      its exact shape: "**Mobile-first UI implementation (when the task
      touches frontend/UI code):** Read
      [../references/mobile-first-ui.md](../references/mobile-first-ui.md)
      before writing layout/styling code. Author the base layout and styles
      for the narrowest viewport first, then expand outward with `min-width`
      breakpoints — never a `max-width` override that claws back mobile
      styles from a desktop-first base. Skip this only when the task README
      already states the surface is PC/tablet-only per that file's escape
      hatch."
- [ ] `ywc-parallel-executor/SKILL.md` — insert a new bullet in Step 4b
      (immediately after the "All six prompt directives..." bullet at
      ~line 216): "- **Mobile-first UI directive (append verbatim to
      `ui`-category subagent prompts only):** Read
      [../references/mobile-first-ui.md](../references/mobile-first-ui.md)
      before writing layout/styling code. Author the base layout and styles
      for the narrowest viewport first, then expand outward with `min-width`
      breakpoints — never a `max-width` override that claws back mobile
      styles from a desktop-first base. Skip this only when the task README
      already states the surface is PC/tablet-only per that file's escape
      hatch." Do not add it to `references/subagent-directives.md` — that
      file's own preamble scopes it to all-category-shared directives only.
- [ ] `claude-code/skills/CLAUDE.md` — add a new `## Mobile-First UI Default`
      section following the existing shared-reference documentation pattern
      (mirror the "Shared Schema Guide" or "HTML Output Mode" section shape):
      name the reference file, the 5 consuming skills, the referenced-not-
      inlined discipline, and the escape-hatch/no-block invariant (a UI task
      predating this rule, or one covered by the escape hatch, behaves
      unchanged).

## Verification

```bash
bash scripts/validate.sh
```

Additionally spot-check that every new/edited relative markdown link
(`../references/mobile-first-ui.md` from each skill root,
`../../references/mobile-first-ui.md` from `ywc-plan/references/`) resolves
to an existing file.

## Risks / Rollback

Low risk — pure documentation/skill-prompt-text addition, no executable code,
no schema/API/library changes. Rollback is `git revert` of the single commit
this plan produces; no migration or state to unwind.
