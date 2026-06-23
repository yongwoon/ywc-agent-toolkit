# Tier 2 — Harness-Improvement Feedback Loop & Stateful Mission Persistence

> Scale: **Medium** · Path: ywc-spec-validate → ywc-task-generator
> Source: LLM agentic-workflow review (STRATEGIC_ENGINEERING §4.3 "review the harness, not just code" + §③ stateful skills; LOOP_ENGINEERING).
> Tier 1 (Grill-Me clarify + complexity routing) shipped in commit `475c81c`. This is Tier 2.
>
> **Operative Sections (read after Iteration 1 Amendments):** `## Iteration 1 Amendments` is authoritative where it supersedes an original line — specifically AC4 (provenance grammar), AC5 (Change Log exemption), AC11 (four edges, not "two"), FR1 (§6 insertion after §3, not §5), FR3 (update-mode reuse), FR4 (four-mode template = `ywc-review-learnings`), the Data Model Success Criteria table (date column + skill-provenance Source), and OQ1/OQ2 (resolved). `ywc-task-generator` MUST treat the amendment as final for these.

## Purpose

Close two gaps the toolkit currently leaves open, both named directly by the source documents:

- **③ Harness-improvement feedback loop** — Today a fixed bug or resolved incident stops at the *code* fix. STRATEGIC_ENGINEERING §4.3 / §4.4 argue the engineer must improve the *system that produced the bug* so the bug class cannot recur. The toolkit has the project-level harness memory (`docs/review-learnings.md`, loaded into every review) but **no path that promotes a confirmed root cause / prevention item into it**.
- **④ Stateful mission/success-criteria persistence** — STRATEGIC_ENGINEERING §③ calls for skills that persist mission and success criteria locally for cross-session continuity. `ywc-brainstorm`'s "Done When" anchors and `ywc-plan`'s acceptance criteria are produced every session but **never persisted to a durable, auto-loaded project file**, so each session re-derives the project's north-star from scratch.

## Why

- The toolkit already proves the value of the stateful-file pattern twice (`ywc-review-learnings`, `ywc-ubiquitous-language`): a committed, `@`-autoloaded Markdown file that a skill reads/updates under user confirmation. Both gaps are best closed by **reusing that proven pattern**, not by inventing new infrastructure.
- Without ③, the same defect class is re-flagged PR after PR; the "why this happened" lesson evaporates. With ③, a confirmed root cause becomes a durable review learning that catches the next instance earlier.
- Without ④, a new session has no machine-readable statement of what "done" means for the project, so `ywc-plan` clarification and `ywc-confidence-gate` scope scoring start cold each time.

## Scope

Decisions confirmed with the requester (all recommended options):

- **③ shape:** extend existing skills + route into `ywc-review-learnings` (no new promotion skill).
- **④ shape:** new dedicated skill `ywc-project-mission` + dedicated file `docs/project-mission.md` (mirrors the `ywc-review-learnings` / `ywc-ubiquitous-language` architecture); `ywc-brainstorm` / `ywc-plan` only read/write that file.
- **Distribution:** `claude-code` bundle only. Codex mirroring deferred to a follow-up.
- **Apply mode:** propose a CHANGESET, then write only after **one** user confirmation (identical to `ywc-review-learnings`).

### In scope

1. `ywc-debug-rootcause` — add a Systemic-Prevention emit after a confirmed fix.
2. `ywc-incident-postmortem` — route Prevention Action Items into the same emit path.
3. `ywc-review-learnings` — accept a new capture source for systemic-prevention items.
4. New skill `ywc-project-mission` (read / update / list / curate) over `docs/project-mission.md`.
5. `ywc-brainstorm` — optional write of the four anchors (esp. Done When → Success Criteria) to the mission file on handoff.
6. `ywc-plan` — optional read of the mission file in Step 1 to frame clarification + align Acceptance Criteria.
7. Full README locale set + `evals/` for the new skill; catalog (`claude-code/skills/README.md`) and `claude-code/skills/CLAUDE.md` updates.

## Out of Scope

- **Codex bundle (`codex/skills/`) mirroring** — deferred; `skills/CLAUDE.md` documents that the two roots are maintained independently. A separate port plan will follow if wanted.
- **Auto-editing skill / agent / CLAUDE.md *definitions*** (the "new ywc-harness-improve skill" / option B) — not chosen. ③ promotes into the project-level `docs/review-learnings.md`, not into skill source.
- **Toolkit self-evaluation** — already owned by `ywc-toolkit-eval`; this plan does not touch it.
- **Auto-apply without confirmation** — every write keeps the one-confirmation gate.
- **Migrating existing `review-learnings.md` content** — additive only.
- **New tooling/runtime/library** — none introduced (Markdown skills + optional bundled shell only).

## Acceptance Criteria

- **AC1** When `ywc-debug-rootcause` Phase 4 completes a verified fix (red-green-red passed) and the defect is a generalizable *class*, the skill surfaces a Systemic-Prevention proposal and offers to record it via `ywc-review-learnings` — observable as a printed `Systemic Prevention` block naming the candidate learning (rule + why + polarity) before any write.
- **AC2** When the defect is a one-off with no generalizable class, the skill explicitly states "no systemic learning warranted" rather than silently skipping — observable as that line in the Phase 4 output.
- **AC3** `ywc-incident-postmortem` Step 6 Prevention Action Items that are recurrence-preventing route through the same `ywc-review-learnings` capture path — observable as a `Systemic Prevention` block in the postmortem output.
- **AC4** `ywc-review-learnings` accepts the new systemic-prevention source and records the item as a `DO` / `DO-NOT` learning carrying the *why*, under one user confirmation — observable as a `Learnings added` confirmation block citing provenance `debug` / `incident`.
- **AC5** New skill `ywc-project-mission` exists with `read` / `update` / `list` / `curate` modes and manages `docs/project-mission.md` with Mission, Success Criteria, and Out-of-Scope sections, each entry dated with provenance — observable by running the skill and inspecting the file.
- **AC6** On first creation of `docs/project-mission.md`, the skill prints the `@docs/project-mission.md` CLAUDE.md activation prompt exactly once (not on subsequent updates) — mirrors `ywc-review-learnings`.
- **AC7** Every `ywc-project-mission` write presents an ADD / MODIFY / DEPRECATE CHANGESET and writes only confirmed entries — no inferred-and-written entries.
- **AC8** `ywc-brainstorm` Step 6 handoff, when `docs/project-mission.md` exists or the user opts in, offers to persist the four anchors (Done When → Success Criteria) via `ywc-project-mission update` — observable as the offer in the handoff block; declining is a clean no-op.
- **AC9** `ywc-plan` Step 1 reads `docs/project-mission.md` when present and frames clarification using its Mission + Success Criteria; absence is a clean no-op (never blocks planning) — mirrors the existing `docs/ubiquitous-language.md` read behavior.
- **AC10** `ywc-project-mission` ships the full README locale set (`.md`, `.en.md`, `.ja.md`, `.ko.md`), Claude-code-only frontmatter (`name` + `description`, no codex-only fields), and an `evals/evals.json`; `scripts/validate.sh` passes; SKILL.md body ≤500 lines.
- **AC11** `claude-code/skills/README.md` catalog and `claude-code/skills/CLAUDE.md` (stateful-file + cross-skill notes) list the new skill and the two new integration edges.
- **AC12** No regression: `scripts/validate.sh` passes (the runnable claude-code gate — structural checks on the new/edited skills; the bundled codex eval gate is a no-op for these changes per NFR4); all edited skills keep `(ywc) Use when...` description + `Do not use for...` anti-triggers + ≥5-row Rationalization Defense (per `ywc-skill-author`).

## Functional Requirements

### ③ Harness feedback loop

- **FR1** `ywc-debug-rootcause`: add **Phase 4 §6 — Systemic Prevention (emit)**. After §3–§5 (verified fix + red-green-red), classify whether the root cause is a *recurring class* (per a short rule: would the same mistake plausibly recur in a sibling file / future PR?). If yes, draft a candidate learning `{rule, why, polarity}` and offer `ywc-review-learnings --mode update --source debug`. If no, print `No systemic learning warranted — one-off cause`. Add one Rationalization Defense row ("fix is done, skip the prevention step") wired to this step (satisfies `ywc-skill-author` B9).
- **FR2** `ywc-incident-postmortem`: in **Step 6 Prevention Action Items**, tag each item recurrence-preventing vs operational. Recurrence-preventing items route through `ywc-review-learnings --mode update --source incident` using the same CHANGESET-then-confirm flow. Operational items stay in the postmortem report only.
- **FR3** `ywc-review-learnings`: extend the `--source` enum (currently `feedback|review|pr`) with `debug` and `incident`. Each maps the upstream root-cause statement to the learning *why*, classifies polarity (`DO` add-a-check / `DO-NOT` forbid-a-pattern), scopes to the narrowest glob, and records provenance (`debug <symptom>` / `incident <id>`). Update the Capture Sources table + `references/capture-sources.md`. No change to the confirmation gate.

### ④ Mission persistence

- **FR4** New skill `ywc-project-mission` managing `docs/project-mission.md`:
  - Modes `read` (load mission to frame planning) / `update` (capture or revise) / `list` / `curate` (deprecate stale), mirroring `ywc-review-learnings`.
  - File sections: **Mission / North-Star** (the durable why), **Success Criteria** (measurable done conditions, sourced from Done When / acceptance criteria), **Out of Scope** (durable non-goals). Each entry dated + provenance.
  - `update` builds an ADD / MODIFY / DEPRECATE CHANGESET; writes only confirmed entries; updates `<!-- updated: DATE -->`.
  - On first file creation, print the `@docs/project-mission.md` activation prompt once.
  - Description: `(ywc) Use when ...` with KR/EN/JA triggers + `Do not use for ...` anti-triggers pointing at `ywc-ubiquitous-language` (vocabulary) and `ywc-review-learnings` (review prefs).
- **FR5** `ywc-brainstorm`: in **Step 6 Handoff**, after producing the four-anchor block, offer to persist Mission (What+Why) and Success Criteria (Done When) via `ywc-project-mission update`. Opt-in; declining is a no-op. Add `requires`/Integration note + one RD row.
- **FR6** `ywc-plan`: in **Step 1 (Clarify)**, read `docs/project-mission.md` when present (alongside the existing `docs/ubiquitous-language.md` read) and use its Mission + Success Criteria to frame questions and seed Acceptance Criteria. Absence is a clean no-op. Optionally offer a mission `update` when a plan finalizes new durable success criteria.

### Cross-cutting

- **FR7** Author `ywc-project-mission` per `ywc-skill-author` rules: `**Announce at start:**` line, ≥5-row domain-specific Rationalization Defense, body ≤500 lines (extract long format spec to `references/`), full README locale set, `evals/evals.json`. Update `claude-code/skills/README.md` and `claude-code/skills/CLAUDE.md` (add `docs/project-mission.md` to the stateful-file family description and the two new cross-skill edges).

## Non-Functional Requirements

- **NFR1 (token discipline)** The mission `read` must emit a compact block (target ≤ ~25 lines) injected into planning; a mission file that floods context degrades planning — same constraint `ywc-review-learnings` places on its applicable-learnings block.
- **NFR2 (no-block invariant)** Absence of `docs/project-mission.md` / `docs/review-learnings.md` must never block the host workflow (planning, debugging, postmortem). All new reads are best-effort.
- **NFR3 (idempotent confirmation)** Re-running an `update` with no new content produces an empty CHANGESET and no file write — no spurious date bumps.
- **NFR4 (validation parity)** All edits keep `scripts/validate.sh` green. Note: the bundled `ywc-codex-toolkit-eval` mechanical gate run by `validate.sh` scores only `codex/skills` / `codex/agents` and is therefore a **no-op for these claude-code-only changes** — claude-code regression coverage comes from `validate.sh`'s structural checks (frontmatter present, full README locale set, body present), not the eval gate.

## Data Model — `docs/project-mission.md` file format

No database. The only "schema" is the Markdown file shape (mirrors `review-learnings.md`):

```markdown
# Project Mission — [Project Name]
<!-- updated: YYYY-MM-DD -->

## Mission / North-Star
- <durable one-paragraph statement of what the project is and why>  (provenance, YYYY-MM-DD)

## Success Criteria
| ID | Criterion (measurable) | Source | Status |
|----|------------------------|--------|--------|
| S001 | <observable done condition> | brainstorm / plan <ref> | active |

## Out of Scope (durable non-goals)
- <non-goal> — <reason>  (YYYY-MM-DD)

## Change Log
| Date | Change | Source |
```

The full format spec (field rules, deprecation via `~~strikethrough~~`, provenance grammar) is extracted to `references/mission-format.md` to keep the body ≤500 lines.

## API Contract

N/A — no network API. The skill-to-skill contract is the `--source debug|incident` extension on `ywc-review-learnings` (FR3) and the `ywc-project-mission` mode flags (FR4); both documented in their `## Arguments` tables.

## Edge Cases

- **EC1** `docs/project-mission.md` absent at `ywc-plan`/`ywc-brainstorm` read time → no-op, planning proceeds (NFR2).
- **EC2** `docs/review-learnings.md` absent when ③ tries to promote → `ywc-review-learnings update` creates it (its existing first-creation path) and prints the activation prompt.
- **EC3** Root cause is a one-off (no recurring class) → AC2 explicit "no systemic learning warranted", no CHANGESET.
- **EC4** User declines the mission/learning CHANGESET → clean abort, no write, no partial file.
- **EC5** A new Success Criterion contradicts an active one → `curate`/MODIFY path: newest-wins, deprecate old with pointer (never silent delete) — same rule as review-learnings.
- **EC6** Mission `update` invoked with identical content → empty CHANGESET, no date bump (NFR3).
- **EC7** A postmortem Prevention Action Item is purely operational (e.g., "rotate the key") → stays in the report, not promoted to a review learning (FR2 tagging).

## Existing Constraints Touched

- `claude-code/skills/ywc-review-learnings/SKILL.md:46` — `--source` arg currently `feedback|review|pr`; FR3 extends it. Capture Sources table at `:97-105`; first-creation activation prompt at `:80-86`; CHANGESET/confirm flow at `:72-86`. The new sources MUST reuse this exact confirm gate.
- `claude-code/skills/ywc-debug-rootcause/SKILL.md:118-135` — Phase 4 (§1–§5); FR1 appends §6 after §3 verification, before the §5 architecture-stop branch. Phase 4 exit condition at `:135` must be updated to include the emit.
- `claude-code/skills/ywc-incident-postmortem/SKILL.md` — Step 6 "Prevention Action Items" (referenced at `:82`, `:122`); FR2 routes recurrence-preventing items.
- `claude-code/skills/ywc-brainstorm/SKILL.md:135-146` — Step 6 Handoff block with `Done When: <bullet list>`; FR5 adds the opt-in persist offer here.
- `claude-code/skills/ywc-plan/SKILL.md` Step 1 — already reads `docs/ubiquitous-language.md` ("**Prerequisite:** If `docs/ubiquitous-language.md` exists, read it…"); FR6 adds the mission read alongside it, same best-effort pattern.
- `claude-code/skills/ywc-ubiquitous-language/SKILL.md` — reference architecture for FR4 (read/update/list/curate + user-confirmed writes + per-project file). Clone its structure, not its content.
- `claude-code/skills/CLAUDE.md` — the stateful-file conventions and cross-skill notes live here; FR7 adds `ywc-project-mission` and the two new edges. Authoring MUST go through `ywc-skill-author` per this file's own rule.
- `scripts/validate.sh` — CI mirror; AC10/AC12 gate on it.

## Critical Surfaces

None security-sensitive. All writes target `docs/*.md` under explicit one-confirmation gates; no auth, secrets, external input, or DB. `Criticality: normal` for all tasks. (Declared so `ywc-task-generator` does not mark gray-box-blocked review.)

## Open Questions

- **OQ1** Should `ywc-plan` *auto-offer* a mission `update` on every Medium/Large finalize, or only when the user opts in? Default proposed: opt-in only (consistent with the confirmed apply-mode decision). Resolve at task time.
- **OQ2** `--source` value naming on `ywc-review-learnings`: `debug` + `incident` (proposed) vs a single `prevention`. Default proposed: two distinct values for provenance clarity. Resolve at task time.

## Notes for downstream

- Step 3.5 Architectural Advisor Gate intentionally skipped: design forks resolved by requester decisions; all four FR families clone an existing in-repo pattern, so no unresolved structural ambiguity.
- `ywc-skill-author` is the mandated authoring path for the new skill and every structural edit (per `claude-code/skills/CLAUDE.md`).

## Iteration 1 Amendments

Resolves the Iteration-1 `ywc-spec-validate` findings (1 Critical, 6 Warning, key Suggestions). The Critical (AC12/NFR4 eval-gate misattribution) was fixed in place above; the remaining resolutions are below and are authoritative where they supersede an original line.

### Terms

- **Polarity** (used in FR1/FR3/AC1/AC4) — a learning's directional class: `DO` (add a check), `DO-NOT` (forbid a pattern), `FALSE-POSITIVE` (suppress a known wrong flag). Same vocabulary as `ywc-review-learnings`.
- **The four anchors** (used in FR5/AC8) are `ywc-brainstorm`'s handoff anchors: **What**, **Why**, **Out of Scope**, **Done When**. Persisted mapping: Mission ← What + Why; Success Criteria ← Done When; durable Out-of-Scope ← Out of Scope. ("What/Why collapse into one Mission paragraph; Out of Scope persists only when the user marks it durable.")

### Open Questions — resolved

- **OQ1 → resolved: opt-in only.** `ywc-plan` never auto-writes the mission file; FR6's write-back is an explicit offer the user must accept. "Finalizes" = the plan run reaches its Step 5 handoff with ≥1 new durable success criterion not already in `docs/project-mission.md`.
- **OQ2 → resolved: two values `debug` + `incident`.** Distinct provenance beats a single `prevention` value for audit clarity (the Feasibility reviewer's single-value alternative was considered and declined on that ground). AC4 provenance grammar is therefore `debug <symptom>` / `incident <id>`.

### Supersedes / pins

- **FR1 §6 insertion point (pins the AC1 / FR1 / Existing-Constraints contradiction):** the new step is inserted **after Phase 4 §3 (red-green-red verification), as a new §6, independent of the §5 architecture-stop branch** — not "after §5". AC1's trigger ("Phase 4 completes a verified fix") and Existing Constraints `:118-135` both read against this single insertion point. `ywc-debug-rootcause` §5 (architecture suspicion) remains a separate branch that §6 does not gate.
- **FR3 (pins the update-mode reuse):** the new `--source debug|incident` values **enter the existing `ywc-review-learnings` update-mode workflow (`SKILL.md:74-86`) unchanged** — only the `--source` enum and the Capture Sources table are extended. No parallel write path; the CHANGESET confirmation and first-creation activation-prompt gates are reused exactly (this is what makes EC2 sound).
- **FR4 / line "reference architecture" (corrects the template citation):** clone the four-mode `read / update / list / curate` shape and the user-confirmed-write pattern from **`ywc-review-learnings` (`SKILL.md:46`)**. `ywc-ubiquitous-language` is a *secondary* reference for the per-project stateful-file pattern only — its actual modes are `new / extract / update`, so it is NOT the four-mode template.
- **Data Model — Success Criteria table (satisfies AC5 "every entry dated"):** the table schema gains a date column → `| ID | Criterion (measurable) | Source | Added | Status |`, where `Added` is `YYYY-MM-DD` and `Source` is **skill-provenance** (`brainstorm` / `plan`), matching the ③ `--source` provenance convention (not artifact-type). The `## Change Log` block is **auto-maintained metadata**, not a user-facing section — AC5's "Mission, Success Criteria, Out-of-Scope" enumeration stands; Change Log is exempt.

### Added Acceptance Criteria

- **AC13** (FR2 negative branch, mirrors AC2) — a postmortem Prevention Action Item classified *operational* (not recurrence-preventing) is explicitly retained in the postmortem report and **not** promoted to a review learning — observable as the operational item appearing in the report with no corresponding `ywc-review-learnings` CHANGESET.
- **AC14** (FR6 write-back, resolves OQ1) — when `ywc-plan` reaches Step 5 with ≥1 new durable success criterion, it **offers** (opt-in) a `ywc-project-mission update`; the user accepting writes under the one-confirmation gate, declining is a clean no-op — observable as the offer line in the handoff and no write on decline.
- **AC15** (NFR3 idempotency, promotes EC6) — re-running `ywc-project-mission update` with content identical to the current file produces an empty CHANGESET and **no** file write or `<!-- updated -->` date bump.

### Enumerated integration edges (satisfies AC11)

The catalog (`claude-code/skills/README.md`) and `claude-code/skills/CLAUDE.md` must document exactly these new edges: (1) `ywc-debug-rootcause` → `ywc-review-learnings` (`--source debug`); (2) `ywc-incident-postmortem` → `ywc-review-learnings` (`--source incident`); (3) `ywc-brainstorm` → `ywc-project-mission` (handoff persist); (4) `ywc-plan` ← `ywc-project-mission` (Step 1 read). The "two new integration edges" phrasing in AC11 is superseded by this explicit four-edge list (two for ③, two for ④).
