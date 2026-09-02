# Port PR #221 (develop-with-llm) — close 3 CodeRabbit catalog gaps in ywc-impl-review

## What

Port `develop-with-llm` PR #221 ("fix: ywc-impl-review CodeRabbit 코멘트량 격차
3건 해소") into this repo's `ywc-impl-review` skill. Three content additions,
none of which reference the `A-002`/`isDeliverySelected` pattern that made the
earlier PR #218 investigation inapplicable here:

1. **Large-diff enumeration procedure** (`recurring-defects.md`) — when a diff
   touches 3+ schema/component files of the same structural shape, require a
   per-file pass/fail record against the catalog instead of one aggregate
   judgment over the whole diff.
2. **New catalog entry**: reactive-effect / watcher (React `useEffect`, Vue
   `watch`, Svelte reactive statement, RxJS, or any framework's equivalent)
   keyed on a route/entity id applies a stale async response after the id
   changes before the request resolves.
3. **New Devex review dimension**: "Convention & Language-Policy Consistency"
   — exhaustively (not sampled) check every new/changed comment and
   user-facing string against the project's stated language policy.

## Why

These three gaps were found by sampling real CodeRabbit bot comments across
5 repositories and cross-checking them against `ywc-impl-review`'s current
catalog/lanes (see PR #221 body and its linked
`docs/ywc-plans/20260819-small_impl-review-coderabbit-catalog-gaps.md` in
`develop-with-llm`). Unlike PR #218 (A-002, blocked because the `A-002` code
and `isDeliverySelected` field name do not exist in this repo's catalog), this
content is stack-agnostic procedure and pattern text with no repo-specific
identifiers — it ports cleanly.

## Out of Scope

- Reconciling the pre-existing content drift between `claude-code/skills/ywc-impl-review/references/recurring-defects.md`
  and `codex/skills/ywc-impl-review/references/recurring-defects.md` in the
  concurrency-safety bullets under §1 (that drift predates this change and is
  a separate cleanup — not touched here).
- Adopting `develop-with-llm`'s alphanumeric `A-00N` provenance-code scheme
  for this repo's catalog. This repo's `recurring-defects.md` uses plain
  numbered `## N.` sections with no per-entry code; the new catalog entry
  follows that existing convention instead (see Files to Touch below).
- Any change to `plugins/ywc-agent-toolkit/skills/ywc-impl-review/` — that
  tree is **generated** from `codex/skills/` by
  `scripts/sync-codex-plugin.sh` (enforced by `.githooks/pre-commit` and
  `.githooks/pre-push`); it must never be hand-edited.
- `tools/codex-skill/` changes from the upstream PR — that path does not
  exist in this repo (this repo's Codex tree lives at `codex/skills/`, not
  `tools/codex-skill/skills/`).
- Any SKILL.md frontmatter change (matches upstream PR's own scope note: no
  frontmatter change, no new dependency).

## Existing Constraints Touched

- `claude-code/skills/CLAUDE.md` states `codex/skills/` and
  `claude-code/skills/` are "no longer auto-synced" — each root is edited
  independently and deliberately when a change applies to both. This plan
  edits both roots by hand, matching that convention (not a copy-paste
  script).
- `.githooks/pre-commit:24-35` — staging any file under
  `plugins/ywc-agent-toolkit/skills/` without a corresponding `codex/skills/`
  change is an error; the hook additionally auto-regenerates
  `plugins/ywc-agent-toolkit` via `sync-codex-plugin.sh` and re-stages it.
  Confirms: never hand-edit `plugins/`, always let the hook (or a manual
  `bash scripts/sync-codex-plugin.sh` run) regenerate it after the
  `codex/skills/` edit is committed.
- `claude-code/skills/ywc-impl-review/references/recurring-defects.md:27-33`
  — Table of contents lists exactly 5 sections (`## 1.` … `## 5.`), no
  `A-00N` codes anywhere in the file. `codex/skills/ywc-impl-review/references/recurring-defects.md`
  has the identical TOC and section structure (verified `diff` of headers —
  only the §1 concurrency-bullet body differs, which is Out of Scope).
- `claude-code/skills/ywc-impl-review/references/devex-agent.md:13-66` and
  the codex counterpart both currently number sections `### 1.` … `### 7.
  Surgical Changes — Devex Aspect` identically to upstream `develop-with-llm`
  pre-PR-221 state, so PR #221's insert-as-7-and-renumber-old-7-to-8 diff
  applies verbatim to both roots.
- `architecture-agent.md` in both roots contains the identical pointer
  sentence to `recurring-defects.md` §1 (verified by diff) — PR #221's new
  pointer sentence (to the large-diff enumeration section) is inserted
  right after it, verbatim, in both roots.

## Files to Touch

Six files, two independent source roots (`claude-code/skills/`, `codex/skills/`);
`plugins/ywc-agent-toolkit/skills/` is regenerated, not edited:

1. `claude-code/skills/ywc-impl-review/references/architecture-agent.md`
2. `claude-code/skills/ywc-impl-review/references/devex-agent.md`
3. `claude-code/skills/ywc-impl-review/references/recurring-defects.md`
4. `codex/skills/ywc-impl-review/references/architecture-agent.md`
5. `codex/skills/ywc-impl-review/references/devex-agent.md`
6. `codex/skills/ywc-impl-review/references/recurring-defects.md`

## Implementation Steps

Apply the same edit to both roots (claude-code, then codex) — the content is
identical in both since neither root currently diverges at these exact
insertion points.

### 1. `architecture-agent.md` (both roots)

- [ ] Immediately after the existing paragraph that links to
      `recurring-defects.md#1-data-layer-access-boundary--integrity` (the
      "Before finalizing, run the structural items…" paragraph), insert one
      new paragraph pointing to the large-diff enumeration procedure added in
      step 3 below:

  ```markdown
  When the diff meets the large-diff trigger, run the enumeration procedure in [`recurring-defects.md`'s "Applying this catalog to large diffs"](./recurring-defects.md#applying-this-catalog-to-large-diffs) — a per-file pass/fail against §1 for every changed schema/model file, not a single aggregate judgment across the diff.
  ```

### 2. `devex-agent.md` (both roots)

- [ ] Insert a new `### 7. Convention & Language-Policy Consistency` section
      immediately before the current `### 7. Surgical Changes — Devex
      Aspect`, and renumber that section (and only that section — `###
      Devex Findings` and everything after it keeps its own heading text,
      only the numbered items shift) to `### 8.`. New section body (verbatim
      from PR #221, already generic — no repo-specific names):

  ```markdown
  ### 7. Convention & Language-Policy Consistency

  Verify every newly-added or changed code comment and every newly-added or
  changed user-facing string complies with the project's language policy (read
  from `CLAUDE.md` / `AGENTS.md` in SKILL.md Step 1 — typically "code comments =
  English" and "user-facing strings = i18n-externalized", but always defer to the
  project's own stated policy).

  - Is every newly-added or changed code comment in the policy's designated
    language (commonly English)?
  - Is every newly-added or changed user-facing string externalized to the
    project's i18n mechanism, not a hardcoded literal?

  **Report every violation found in the diff, not a sampled subset.** This
  dimension exists specifically because the same convention violation
  historically recurs several times within one PR (a comment translated in one
  file but not its sibling, a string externalized in one component but not the
  next) — a partial or sampled report defeats the purpose; each occurrence is
  its own finding.

  Scope is limited to newly-added or changed lines in this diff — pre-existing
  violations outside the diff are out of scope for this dimension.
  ```

- [ ] In the Severity Criteria table, append to the **Warning** row:
      `; Convention/Language-Policy violation on a newly-added or changed
      comment/string`
- [ ] In the `### Devex Findings` output-format `Category:` line, insert
      `Convention & Language-Policy Consistency` before `Surgical Changes`.
- [ ] In the "Before finalizing, run the resilience items…" checklist near
      the end of the file, add one bullet after the existing "Resource
      lifecycle" bullet:

  ```markdown
  - **Convention & Language-Policy exhaustiveness** — run dimension 7 (above) against every newly-added or changed comment and user-facing string in the diff and report every violation found, not a sample. This is the recurring bot-review pattern this check exists to catch before the PR opens: the identical convention violation (e.g. a non-English comment, or a hardcoded string that should be externalized) recurring across several sibling files within one PR, each flagged separately by a bot reviewer instead of caught once locally.
  ```

### 3. `recurring-defects.md` (both roots)

- [ ] Insert a new `## Applying this catalog to large diffs` section
      immediately after the "Why this catalog exists" section's closing
      paragraph (the "**A finding from this catalog still obeys…**"
      paragraph) and before `## Table of contents`. Body verbatim from
      PR #221 (already generic):

  ```markdown
  ## Applying this catalog to large diffs

  When a diff touches **3 or more** schema / component / model files of the
  same structural shape (e.g. several ORM/DDL model definitions in one
  migration, several sibling UI components implementing the same pattern), do
  not "consider the catalog generally" against the diff as a whole — that
  produces a single aggregate judgment that silently skips some of the changed
  files. Instead, **enumerate every changed file of that shape and record a
  per-file pass/fail against the applicable catalog item(s)**, the same way the
  Step 2 trigger #4 complement-grep works in `ywc-plan`: list the full candidate
  set, then classify each one, rather than confirming the pattern once and
  generalizing.

  This is not a hypothetical failure mode: a checklist item from this catalog
  (most often an ownership/access-boundary item from §1) gets correctly applied
  to one changed file in a large diff and silently skipped on a structurally
  identical sibling file in the very same diff — same reviewer, same PR, same
  catalog item, applied to one file and not the other. Per-file enumeration is
  what catches it; a single pass over the diff as a whole does not.
  ```

- [ ] Add `6. [Frontend reactive-effect & stale-response hygiene](#6-frontend-reactive-effect--stale-response-hygiene) — Architecture + Devex`
      as a new line to the existing `## Table of contents` list (after item
      5).
- [ ] Append a new `## 6. Frontend reactive-effect & stale-response hygiene`
      section at the end of the file (after the existing `## 5. Test
      fidelity` section), adapted from PR #221's `A-003` entry — same
      content, but dropped into this repo's plain-numbered-section
      convention (no `A-00N` code, no `> Provenance —` line, since this
      repo's catalog does not carry per-entry provenance metadata anywhere
      else in the file):

  ```markdown
  ## 6. Frontend reactive-effect & stale-response hygiene

  Any UI layer with a reactive-effect or watcher mechanism (React's `useEffect`,
  Vue's `watch`, Svelte's reactive statement, or a manually re-triggered fetch on
  route/param change) can key an async fetch off an id read from
  props/route/context — a stand-in for whatever identifying value the system
  under review uses (an entity id, a resource slug, a selected-record key). If
  the id changes again before the in-flight request resolves — a fast user
  switching between entities, a rapid navigation — the resolved response is
  applied to state (component state, a store, a ref) without first checking that
  the response still corresponds to the *current* id. The UI then renders, or
  acts on, the previous id's data as if it were the current id's data. The class
  recurs because the happy-path test always waits for one fetch to settle before
  switching ids, so the missing "is this still current?" guard is never
  exercised. Apply the *why* — any reactive effect whose identity depends on a
  value that can change before its async work resolves needs to re-validate that
  identity before committing the result — not just the specific
  framework/hook shown here; skip this item entirely for stacks with no
  reactive-effect/watcher layer (note the skip).

  **Scan cue:** grep for the stack's reactive-effect/watcher construct (whatever
  it is — `useEffect`, `watch`, an RxJS subscription, a manually re-triggered
  fetch) whose trigger includes an id-like value, and confirm the resolved
  response is compared against the *current* id (read fresh at resolution time,
  not the id captured in the closure at fetch-start) before being applied to
  state. A trigger keyed on an id with no such comparison at the point the async
  result is applied is a finding.

  **Severity guide:** the stale response drives a user-facing data-corruption or
  wrong-target action (e.g. provisioning, deploying, or submitting against the
  wrong entity) → High; display-only stale render with no side effect → Medium.
  ```

### 4. Regenerate the Codex plugin package

- [ ] After both roots are edited, run
      `bash scripts/sync-codex-plugin.sh` to regenerate
      `plugins/ywc-agent-toolkit/skills/ywc-impl-review/` from the updated
      `codex/skills/`. Do not hand-edit anything under `plugins/`.

## Verification

Run from repo root (commands confirmed from `CLAUDE.md` and
`.github/workflows/`):

- [ ] `bash scripts/validate.sh` — structural skill validation (frontmatter,
      required READMEs, Codex `agents/openai.yaml`); this change touches no
      frontmatter or README, so it should pass unchanged.
- [ ] `bash scripts/sync-codex-plugin.sh` then `git status` — confirms
      `plugins/ywc-agent-toolkit/skills/ywc-impl-review/` is regenerated with
      no leftover diff (this is also what `.githooks/pre-push` enforces).
- [ ] `npx markdownlint-cli2@0.22.1 claude-code/skills/ywc-impl-review/references/*.md codex/skills/ywc-impl-review/references/*.md`
      — the repo's `markdownlint.yml` workflow only lints README files by
      glob, so this is a stricter local-only check; fix only violations
      introduced by this diff (existing files may already carry
      pre-existing rule exceptions).
- [ ] Manual read-through: confirm the `recurring-defects.md` TOC anchor
      `#6-frontend-reactive-effect--stale-response-hygiene` matches the
      heading exactly (GitHub-style slug: lowercase, spaces → `-`, `&` and
      `/` stripped) in both roots.
- [ ] Manual read-through: confirm `devex-agent.md`'s renumbered `### 8.
      Surgical Changes` heading and every reference to "item 7" / "dimension
      7" elsewhere in the file (the new checklist bullet added in Step 2)
      still points at the *new* Convention & Language-Policy section, not
      the renumbered Surgical Changes section.

## Risks / Rollback

- **Risk**: renumbering `devex-agent.md`'s `### 7.` → `### 8.` could break an
  external cross-reference to `#7-surgical-changes--devex-aspect` if any
  other file in the repo links to that anchor by number.
  - Mitigation: `grep -rn "surgical-changes--devex-aspect" claude-code/ codex/`
    before editing; update any hit found. (Not found in the Step 2
    investigation so far — re-verify at implementation time.)
- **Risk**: hand-editing `codex/skills/` and `claude-code/skills/`
  independently (per this repo's explicit "no longer auto-synced" policy)
  risks a future silent re-divergence if only one root is touched.
  - Mitigation: this plan's Implementation Steps apply every edit to both
    roots in the same pass; no step is root-specific.
- **Rollback**: pure markdown reference-file edits with no code/schema/API
  surface — `git revert` the commit(s) if the new catalog entry or Devex
  dimension produces false positives in practice.
