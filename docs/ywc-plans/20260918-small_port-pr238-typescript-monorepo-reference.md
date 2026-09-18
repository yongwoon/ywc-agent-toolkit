# Plan: Port PR #238 TypeScript pnpm-workspaces monorepo reference to Codex

> Status: Ready for implementation
> Scale: Small
> Created: 2026-09-18

## Goal

Add PR #238's `TypeScript Monorepo Large (apps + packages)` variant to the
Codex `ywc-project-scaffold` JavaScript/TypeScript reference. This supplies a
concrete large-scale pnpm-workspaces layout for multi-app projects and a
single backend split into HTTP and worker entry points, including package
boundaries and dependency-direction enforcement guidance.

## Out of Scope

- `claude-code/skills/` — the requested target is Codex only; the two skill
  roots are independently maintained.
- `codex/agents/*.toml` — PR #238 changes no agent behavior, and this is
  reference content consumed by `ywc-project-scaffold`, not a custom-agent
  contract.
- Changes to `ywc-project-scaffold/SKILL.md`, its README locales, or
  `agents/openai.yaml` — its reference-loading behavior already selects
  `references/javascript.md` for JavaScript/TypeScript requests.
- Creating pnpm workspace files, architecture tests, or a project scaffold in
  this repository — this change documents a reusable structure only.
- Reworking existing Next.js, NestJS, Astro, or Express variants.

## Existing Constraints Touched

- `codex/skills/ywc-project-scaffold/SKILL.md:104-112` routes JavaScript and
  TypeScript scaffold requests to `references/javascript.md`; no skill logic
  change is required for a new variant in that file.
- `codex/skills/ywc-project-scaffold/references/javascript.md:3-23` is the
  maintained table of contents, and `:480-518` shows `Express Medium` is the
  final existing framework variant. Insert the new monorepo section after it
  and add matching nested TOC entries.
- `scripts/sync-codex-plugin.sh:5-6,47` declares `codex/skills` the source of
  truth and `plugins/ywc-agent-toolkit` the packaging output. Do not edit the
  package mirror by hand.
- `scripts/validate.sh:330-344` regenerates a temporary plugin package and
  fails when the checked-in package differs, so synchronization is required
  after the source reference changes.

## Files to Touch

| File | Change Type | Reason |
|---|---|---|
| `codex/skills/ywc-project-scaffold/references/javascript.md` | Modify | Add the Codex-only monorepo reference and its TOC links. |
| `plugins/ywc-agent-toolkit/skills/ywc-project-scaffold/references/javascript.md` | Generated update | Regenerate the marketplace package from the Codex source. |

## Implementation Steps

- [ ] In `codex/skills/ywc-project-scaffold/references/javascript.md`, add
      `TypeScript Monorepo (pnpm workspaces)` and its `TypeScript Monorepo
      Large (apps + packages)` child to the Table of Contents after the
      Express entries.
      → verify: both GitHub heading anchors resolve to the inserted headings.
- [ ] Append PR #238's Codex-oriented `TypeScript Monorepo Large (apps +
      packages)` section after `Express Medium`: the `apps/web` and
      `apps/server` deployable layout, reusable `packages/` boundaries
      (`contracts`, `core`, `db`, external SDK adapter, `connectors`), and
      root test categories/configuration files.
      → verify: the tree distinguishes deployable apps from reusable packages
      and includes no project-specific names.
- [ ] Preserve the PR's seven key constraints: process-entrypoint separation,
      zero-internal-dependency contracts boundary, SDK isolation, framework-
      free core ports, automated forbidden-dependency checks, and package
      public API/no-deep-import rules.
      → verify: every key point is present and does not claim a change to
      existing framework variants.
- [ ] Run `bash scripts/sync-codex-plugin.sh` to regenerate
      `plugins/ywc-agent-toolkit/skills/ywc-project-scaffold/references/javascript.md`.
      → verify: `cmp -s` reports the source and package copies are identical.
- [ ] Review the diff, then run the repository validation.
      → verify: only the source reference and generated package mirror change
      (besides this plan artifact), and all verification commands exit zero.

## Verification

```bash
bash scripts/sync-codex-plugin.sh
cmp -s codex/skills/ywc-project-scaffold/references/javascript.md plugins/ywc-agent-toolkit/skills/ywc-project-scaffold/references/javascript.md
git diff --check
bash scripts/validate.sh
```

Expected outcome: the generated package is in sync, Markdown introduces no
whitespace errors, and repository structural/contract validation passes.

## Risks and Rollback

| Risk | Likelihood | Mitigation / Rollback |
|---|---|---|
| The documented layout is treated as a universal TypeScript structure | Low | State its Large-scale applicability and retain all existing framework-specific variants. |
| Source and marketplace package diverge | Low | Regenerate only through `scripts/sync-codex-plugin.sh`; revert both matching reference changes together. |
| An agent is changed unnecessarily | Low | Make no `codex/agents/*.toml` or skill metadata change; this PR is reference-only. |

## Acceptance Criteria

- [ ] A Codex `ywc-project-scaffold` request for a large pnpm-workspaces
      monorepo can select a documented `apps/` + `packages/` structure with
      explicit contracts, core, infrastructure-adapter, and test boundaries.
- [ ] The new section is discoverable through matching table-of-contents links.
- [ ] No Claude Code skill or Codex custom agent changes.
- [ ] The packaged Codex skill is generated from, and matches, the canonical
      `codex/skills` reference.
- [ ] All verification commands pass.

## Planning Confidence

Confidence Gate Report

Aggregate: 97/100 — PROCEED

- Scope clarity: 98 — PR #238's exact two-file diff and the requested Codex
  skill/agent boundary make the change and exclusions explicit.
- Architecture compliance: 96 — the repository designates `codex/skills` as
  source and the plugin as generated output; no new runtime architecture is
  introduced.
- Evidence quality: 98 — current reference anchors, upstream PR diff, and
  validation/synchronization scripts were inspected directly.
- Reuse verified: 94 — the current JavaScript reference has framework variants
  only and no pnpm-workspaces monorepo variant; this is an additive sibling,
  not duplicate guidance.
- Root cause identified: 96 — the reference lacks a structure for large
  multi-app TypeScript systems with shared contracts and isolated providers.
