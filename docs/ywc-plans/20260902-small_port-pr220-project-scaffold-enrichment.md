# Port PR #220 (develop-with-llm) — enrich ywc-project-scaffold (Claude Code only)

## What

Port `develop-with-llm` PR #220 ("docs: enrich ywc-project-scaffold references
and add trend-check/reference-refresh") into this repo's `ywc-project-scaffold`
skill, **Claude Code root only** (`claude-code/skills/`) — `codex/skills/` and
`plugins/ywc-agent-toolkit/` are explicitly out of scope for this port. Three
content additions:

1. **`references/javascript.md`** — new shared `Naming Convention` section
   (Directory/Component/Utility casing table) and `Component Logic Colocation`
   section (component-private `hooks/`/`functions/` staged-promotion rule),
   plus one cross-reference bullet added to the `Key Points` of Next.js Small
   (new), Next.js Medium, Next.js Large, NestJS Large (DDD), and Astro Medium.
2. **`references/go.md`** — new `Go Large (Layered, Connect RPC)` variant
   inserted after `Go Large (DDD)` (tier-first layout: `domain/usecase/
   repository/handler/infrastructure/worker/injector/gen`), a new TOC entry,
   and 3 new rows (`injector/`, `gen/`, `converter/`) in the `Conventions`
   table.
3. **`SKILL.md`** — a conditional **Trend check** sub-step (delegate to
   `/ywc-tech-research` for large-scale or contested-Architecture requests
   before finalizing the tree) and an optional **Reference Refresh** mode
   (user asks to review/refresh/audit a `references/<language>.md` file;
   propose an additive diff, wait for approval, then edit).

## Why

Upstream added these based on real LIMA frontend/backend project experience
(see PR #220 body): a `Naming Convention` + `Component Logic Colocation` gap
found repeatedly in JS/TS scaffolds, a `Go Large (Layered, Connect RPC)`
variant for single-deployable multi-domain Go backends that don't fit the
existing DDD/Bounded-Context variant, and two process gaps in the skill itself
— stale reference content going undetected on large/contested requests, and no
sanctioned way to update a reference file short of a silent hand-edit.

## Out of Scope

- `codex/skills/ywc-project-scaffold/` — the user explicitly scoped this port
  to Claude Code only. Codex has no `ywc-project-scaffold` skill directory at
  all in this repo (verified: `codex/skills/` contains no
  `ywc-project-scaffold/`), so there is nothing to port there in this pass
  regardless.
- `plugins/ywc-agent-toolkit/` — generated from `codex/skills/` by
  `scripts/sync-codex-plugin.sh`; since `codex/skills/` is untouched, no
  regeneration is needed and none should be run.
- Adopting upstream's `Mode` enum / `NEEDS_CONTEXT Conditions` / `Common
  Mistakes` table architecture wholesale. This repo's local `SKILL.md` never
  adopted that structure (it has no `Status:`/`Mode:` output contract, no
  `NEEDS_CONTEXT Conditions` section, no `Common Mistakes` table anywhere in
  the file) — introducing that scaffolding now, just to carry two features
  that don't strictly need it, is out of scope. Trend check and Reference
  Refresh are grafted onto the existing Behavioral Flow / Rationalization
  Defense / Boundaries sections instead (see Implementation Steps).
- `README*.md` locale files for `ywc-project-scaffold` — this port changes
  skill *behavior* text (`SKILL.md`) and *reference* content
  (`references/*.md`), neither of which the README files summarize at that
  level of detail; no README currently documents the Behavioral Flow steps or
  reference-file contents in enough depth to need updating (`grep -l
  "Trend\|reference-refresh\|Naming Convention" claude-code/skills/ywc-project-scaffold/README*.md`
  → no hits, confirms nothing there references the pre-port content this
  touches).
- Any SKILL.md frontmatter change (matches upstream PR's own scope note — no
  new trigger phrase, no version bump; `description` and `allowed tools`
  already cover this skill's existing Read/Write/Edit usage).

## Existing Constraints Touched

- `claude-code/skills/CLAUDE.md` ("Codex-skill: Maintained Independently")
  confirms `codex/skills/` and `claude-code/skills/` are edited independently
  and deliberately — this port touching only `claude-code/skills/` (because
  no Codex `ywc-project-scaffold` exists to receive it) matches that
  convention rather than violating it.
- `claude-code/skills/ywc-project-scaffold/SKILL.md:1-170` (full file read) —
  confirms the local skill's actual structure: `Rationalization Defense`
  table (6 rows), `Triggers`, `Usage`, `Input Analysis` (+ `Scale Criteria`),
  `Behavioral Flow` steps 1–5 (`Analyze` / `Load References` / `Generate` /
  `Explain` / `Extras`), `Output Rules`, `Boundaries` (`Will:` / `Will Not:`).
  No `Mode:`/`Status:` output block, no `NEEDS_CONTEXT Conditions` section, no
  `Common Mistakes` table exist anywhere in the file — the upstream PR's
  SKILL.md diff assumes all three, so it cannot be applied as a literal patch
  (see Out of Scope above); the plan below re-expresses the same two features
  against this file's actual section set.
- `claude-code/skills/ywc-project-scaffold/references/go.md:160-271` (full
  tail read) — confirms `Go Large (DDD)`'s `**Key Points:**` block ends at
  line 172, followed by `---` then `## Gin / Echo Framework` at line 176; the
  `## Conventions` table ends at line 271 (file EOF, 8 existing rows, no
  trailing blank line after the last row). Both anchors match the upstream
  PR's diff context exactly (`Go Large (DDD)` Key Points end with "Multiple
  binaries in `cmd/`" in both; `## Conventions` table both end with the
  `testdata/` row before the diff's new rows) — direct verbatim port with no
  adaptation needed.
- `claude-code/skills/ywc-project-scaffold/references/javascript.md:1-450`
  (full file read) — confirms Next.js Small (no existing `Key Points`), Next.js
  Medium (`Key Points` ends with "`lib/`: Framework-independent utilities and
  configuration"), Next.js Large (`Key Points` ends with "Only promote to
  shared when used by 2 or more features"), NestJS Large (DDD) (`Key Points`
  ends with "Inter-module communication through Domain Events"), and Astro
  Medium (`Key Points` starting at line 429) all match the upstream PR's diff
  context lines exactly, word-for-word. NestJS Medium's `Key Points` (line
  270) is present locally but was **not** touched by the upstream PR either —
  no change needed there. Direct verbatim port for the two new sections and
  all five cross-reference bullets.

## Files to Touch

Three files, one root only (`claude-code/skills/`) — no `codex/skills/`
counterpart exists for this skill, and `plugins/` is not touched:

1. `claude-code/skills/ywc-project-scaffold/references/javascript.md`
2. `claude-code/skills/ywc-project-scaffold/references/go.md`
3. `claude-code/skills/ywc-project-scaffold/SKILL.md`

## Implementation Steps

### 1. `references/go.md` — verbatim port

- [ ] In the `## Table of Contents` list, add
      `    - [Go Large (Layered, Connect RPC)](#go-large-layered-connect-rpc)`
      immediately after the existing `- [Go Large (DDD)](#go-large-ddd)` line.
- [ ] Immediately after `Go Large (DDD)`'s `**Key Points:**` block (after "-
      Multiple binaries in `cmd/`: Separate API server and background worker")
      and its trailing `---`, insert the full `### Go Large (Layered, Connect
      RPC)` section verbatim from the PR #220 diff (tree block + the 7-bullet
      `**Key Points:**` list ending with "Typical fit: gRPC/Connect-RPC
      backend..."), followed by its own trailing `---`, before `## Gin / Echo
      Framework`.
- [ ] Append 3 new rows to the end of the `## Conventions` table (after the
      existing `testdata/` row), verbatim from the PR #220 diff:
      `injector/`, `gen/`, `converter/`.

### 2. `references/javascript.md` — verbatim port

- [ ] In the `## Table of Contents` list, add two new lines
      (`- [Naming Convention](#naming-convention)` and
      `- [Component Logic Colocation](#component-logic-colocation)`)
      immediately after the `- [Table of Contents](#table-of-contents)` line
      and before `- [Next.js](#nextjs)`.
- [ ] After the TOC's closing `---` and before `## Next.js`, insert both new
      sections verbatim from the PR #220 diff, in order: `## Naming
      Convention` (casing table + framework-exception blockquote) then `##
      Component Logic Colocation` (colocation tree diagram + 3-bullet
      promotion rules), each followed by its own trailing `---`.
- [ ] Next.js Small: insert a new `**Key Points:**` block (this section has
      none today) immediately before its trailing `---`, containing exactly
      the PR's one bullet: `- See [Component Logic Colocation](#component-logic-colocation)
      — give \`header.tsx\`/\`footer.tsx\` their own \`hooks/\`/\`functions/\`
      if page-specific logic accumulates`.
- [ ] Next.js Medium: append one bullet to the existing `**Key Points:**` list
      (after "`lib/`: Framework-independent utilities and configuration"):
      `- See [Component Logic Colocation](#component-logic-colocation) — give
      any \`features/*\` component its own \`hooks/\`/\`functions/\` once it
      needs private logic`.
- [ ] Next.js Large: append one bullet to the existing `**Key Points:**` list
      (after "Only promote to shared when used by 2 or more features"):
      `- See [Component Logic Colocation](#component-logic-colocation) for the
      finer-grained, per-component version of this same rule inside
      \`features/*/components/\``.
- [ ] NestJS Large (DDD): append one bullet to the existing `**Key Points:**`
      list (after "Inter-module communication through Domain Events") — reuse
      the exact bullet upstream added, but **re-fetch and confirm the exact
      PR #220 diff hunk for this section before writing it** (this session's
      diff fetch showed hunks for Next.js Small/Medium/Large and Astro Medium
      explicitly; a distinct NestJS hunk was not directly observed in the
      captured output, and the PR body's general claim "모든 규모의 Key
      Points에서 상호 참조" is not a substitute for the actual hunk text). If
      re-fetching shows no NestJS hunk, skip this bullet and note the
      discrepancy instead of inventing wording.
- [ ] Astro Medium: append one bullet to the existing `**Key Points:**` list:
      `- See [Component Logic Colocation](#component-logic-colocation) for
      \`components/react/\` and \`components/vue/\` islands`.

### 3. `SKILL.md` — re-expressed against local structure (not a literal patch)

- [ ] **Rationalization Defense** — append 2 new rows after the existing 6:

  ```markdown
  | "Reference file is good enough, skip the trend check for a large-scale request" | `references/*.md` are hand-maintained and can lag current practice. Large scale or a contested Architecture choice warrants a lightweight `/ywc-tech-research` check before finalizing (see Trend check in step 2). |
  | "User wants a reference file updated, just edit it directly" | Reference-file review/refresh requests propose an additive diff for approval first (see Reference Refresh, step 6). Silent edits change every future scaffold call using that language. |
  ```

- [ ] **Triggers** — append one bullet after the existing 4:
      `- Reference file audit/refresh request — "review go.md", "refresh the
      python reference with current trends", "re-audit this reference against
      recent practice"`
- [ ] **Behavioral Flow, step 2 (`Load References`)** — after the existing
      "**Compound condition handling**" paragraph, insert a new
      "**Trend check (conditional)**" paragraph, adapted from the PR #220
      diff (drop the upstream cross-reference to its own `#trend-check`
      anchor and `Extras section` wording; point at this file's own step 5
      `Extras` instead):

  ```markdown
  **Trend check (conditional)**: The loaded reference is a fast, curated baseline, not a permanent verdict — it is hand-maintained and can lag current practice. When Scale is `large`, or the user explicitly contests/questions the Architecture choice, pause and delegate to `/ywc-tech-research "<language>/<framework> project structure conventions" --depth 25` before finalizing the tree. Compare its findings against the loaded reference:

  - If findings confirm the reference, proceed without comment.
  - If a material delta exists (a convention the reference is missing, or one that has since shifted), surface it as a labeled callout in step 5 (Extras) — do not silently substitute it into the tree, and do not edit the reference file from this step (that is Reference Refresh, step 6, below).

  Skip this sub-step for `small`/`medium` scale with an uncontested Architecture — the static reference is sufficient and the research overhead is not justified for a fast baseline case.
  ```

- [ ] **Behavioral Flow — new step 6** — append after the existing step 5
      (`Extras`) and before `## Output Rules`:

  ```markdown
  ### 6. Reference Refresh - Optional Mode

  Triggered when the user asks to review, refresh, or audit a `references/<language>.md` file itself, rather than generate a project plan. This mode never edits silently — it produces a proposal for the user to approve, then stops.

  1. **Identify target(s)** — the `references/<language>.md` file(s) named or implied by the request. Language is inferred from the matched file path, not asked for separately; Framework and Scale (required elsewhere in this skill) do not apply to this mode.
  2. **Gather evidence**: if the user supplies a real-world repository or documentation path to cross-check, read/grep it directly and compare its actual structure against the reference. Otherwise, delegate to `/ywc-tech-research "<language> project structure best practices"` (or `"<language>/<framework> project structure best practices"` when Framework is known), with `--depth 25`.
  3. **Diff against the current reference** — identify genuinely new or divergent patterns, not just rephrasing of what is already documented.
  4. **Propose additively** — a new variant section alongside existing ones, or new rows in an existing Conventions/Key Points table. Never delete or silently overwrite an existing documented pattern; an older pattern may still be a valid alternative for a different context (see how `Go Large (DDD)` and `Go Large (Layered, Connect RPC)` coexist as sibling variants in `references/go.md`).
  5. **Present the diff and stop** — show the proposed addition to the user and wait for approval before editing. After approval, apply the edit and run the project's Markdown lint check on the touched file(s) before reporting done.
  ```

- [ ] **Boundaries → Will:** — append one bullet:
      `- Audit/refresh a \`references/<language>.md\` file against real-world
      evidence or \`/ywc-tech-research\` findings, proposing an additive diff
      for approval (Reference Refresh, step 6)`
- [ ] **Boundaries → Will Not:** — replace the existing bare
      `- Move, rename, or edit files in an existing repository` line with:

  ```markdown
  - Move, rename, or edit files in the user's target project (this skill is plan-only there) — the sole exception is Reference Refresh (step 6) editing this skill's own `references/<language>.md` file, and only after the user approves the proposed diff
  - Auto-apply a reference-file edit without user confirmation
  - Remove or overwrite an existing documented variant during Reference Refresh — that mode stays additive-only
  ```

## Verification

Run from repo root (commands confirmed from `CLAUDE.md` and
`.github/workflows/`):

- [ ] `bash scripts/validate.sh` — structural skill validation (frontmatter,
      required READMEs); this change touches no frontmatter or README, so it
      should pass unchanged.
- [ ] `npx markdownlint-cli2@0.22.1 "claude-code/skills/ywc-project-scaffold/SKILL.md" "claude-code/skills/ywc-project-scaffold/references/go.md" "claude-code/skills/ywc-project-scaffold/references/javascript.md"`
      — the repo's `markdownlint.yml` workflow only lints README files by
      glob, so this is a stricter local-only check; fix only violations
      introduced by this diff.
- [ ] Manual read-through: confirm the new TOC anchors
      (`#go-large-layered-connect-rpc`, `#naming-convention`,
      `#component-logic-colocation`) match their headings exactly
      (GitHub-style slug: lowercase, spaces → `-`, parens/commas stripped).
- [ ] Manual read-through: confirm every new `**Key Points:**` cross-reference
      bullet lands inside the correct section (Next.js Small/Medium/Large,
      NestJS Large (DDD), Astro Medium) and not a sibling section with a
      similar name (e.g. NestJS Medium, which upstream did not touch).
- [ ] Manual read-through: confirm `SKILL.md`'s new step 6 does not
      contradict step 2's existing Input Analysis table (which still marks
      Language/Framework/Scale as "Required — always ask" for the normal
      scaffold flow) — step 6 is scoped to explicitly say Framework/Scale
      don't apply to *it*, not to change the table itself.

## Risks / Rollback

- **Risk**: the NestJS Large (DDD) `Key Points` bullet content in
  Implementation Step 2 is inferred from the PR body's general claim ("모든
  규모의 Key Points에서 상호 참조") rather than a directly transcribed diff hunk
  for that specific section — the exact PR #220 diff fetch performed during
  this planning session showed hunks for Next.js Small/Medium/Large and Astro
  Medium, but the fetched diff output did not include a distinct NestJS
  hunk in the portion captured. Re-fetch `gh pr diff 220 --repo
  yongwoon/develop-with-llm` at implementation time and confirm the exact
  NestJS Large (DDD) bullet text before writing it, rather than trusting this
  plan's inferred wording.
  - Mitigation: implementation step is flagged inline with a re-verify
    instruction; if the diff shows no NestJS hunk at all, skip that bullet
    and note the discrepancy rather than inventing text.
- **Risk**: `SKILL.md`'s re-expression (Implementation Step 3) is a redesign,
  not a literal patch — a redesign risks drifting from upstream's intent in
  ways a literal patch would not.
  - Mitigation: the plan preserves upstream's exact procedural content (Trend
    check delegation query + `--depth 25`, Reference Refresh's 5 numbered
    sub-steps, the additive-only invariant) and only changes anchor/section
    references to match this file's actual structure — no behavioral content
    is dropped, only the surrounding scaffolding (`Mode:` enum, `NEEDS_CONTEXT
    Conditions`, `Common Mistakes` table) that this file never had.
- **Rollback**: pure Markdown skill/reference-file edits with no code/schema/
  API surface — `git revert` the commit(s) if either new reference variant or
  the Reference Refresh mode produces confusing behavior in practice.
