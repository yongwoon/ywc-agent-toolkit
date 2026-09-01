# Plan: Port Load-bearing Premises gate into ywc-brainstorm

> Scale: Small
> Confidence Gate: 92/100 — PROCEED (weakest: reuse verified 85)
> Source: yongwoon/develop-with-llm PR #215 (`ywc-brainstorm` SKILL.md, merged 2026-08-14)

## Goal

Add a **Load-bearing premises** gate to `claude-code/skills/ywc-brainstorm`'s
Step 5 approval flow: any design-critical fact the design assumes but does not
establish must be tabled with `file:line` + quoted-snippet evidence and marked
`VERIFIED`/`UNVERIFIED`. The Step 5 handoff question ("Should I hand this off
to `ywc-plan`?") must not be asked while any row is `UNVERIFIED`.

Motivation (from upstream): a real session built an entire spec on an
unverified "tenant scope exists in DB" premise; the user caught it only at
turn 22, forcing a full spec rewrite. Every other error in that session was
self-caught by existing mechanical checks (grep / `git log --reverse` /
call-graph) — the only structural gap was a gate that verifies the *absence*
of evidence for a load-bearing claim. Upstream's fix (PR #215) was hardened
twice more after merge: once to require a *quoted snippet*, not just a
`file:line` citation (a bare citation lets `VERIFIED` be self-declared without
being checked), and once to constrain `Status` to exactly `{VERIFIED,
UNVERIFIED}` (an unconstrained free-text status let any string satisfy a
"zero UNVERIFIED" gate). This repo's `ywc-brainstorm` has no equivalent gate
today — confirmed via `grep -n "Load-bearing premises\|UNVERIFIED"
claude-code/skills/ywc-brainstorm/SKILL.md` (no matches).

## Out of Scope

- Porting to `codex/skills/ywc-brainstorm/` or
  `plugins/ywc-agent-toolkit/skills/ywc-brainstorm/` — this repo's skill roots
  are maintained independently by deliberate hand-porting
  (`claude-code/skills/CLAUDE.md` "Codex-skill: Maintained Independently");
  not part of this change.
- Any change to `ywc-spec-validate` or `ywc-plan`'s own gates — upstream PR
  #215 explicitly considered and rejected adding a premise-grounding axis
  there; same reasoning applies here.
- Renumbering this repo's existing Step 4/4.5/5/5.5/6 structure. Upstream's
  Step 1 (Blind Spot Pass) / Step 5 (design + approval) split maps onto this
  repo's existing **Step 4.5** (Blind-spot pass / Unknown Matrix) and **Step
  5** (Present the design and get approval) — adapt content into those
  existing steps, do not add or renumber steps.
- A new `references/*.md` file — the addition is a few lines per existing
  section, not new content deserving extraction.

## Files to Touch

| File | Change Type | Reason |
|---|---|---|
| `claude-code/skills/ywc-brainstorm/SKILL.md` | Modify | Add premises table spec + evidence rule to Step 5 (`:142-156`); add schema/scope verification sentence to Step 4.5's Unknown Matrix table (`:129-140`); add one line to Validation Checklist (`:210-224`) |
| `claude-code/skills/ywc-brainstorm/README.md` | Modify | Sync Step 5 summary bullet (item 6, `:19`) to mention the premises table + `UNVERIFIED` block condition |

(No Interfaces section — both files are prose documents with no shared
function/type signature.)

## Design

Reuse this repo's existing table conventions (the anchor table at Step 3, the
Rationalization Defense table) rather than inventing new formatting.

**Change 1 — `SKILL.md` Step 5 (`:144-150`, the bullet list under "Present
the design in sections sized to their complexity")**: add a new bullet after
`Failure modes` and before `Out of Scope`:

> - **Load-bearing premises** — every fact the design assumes but does not
>   itself establish (distinct from Failure modes, which are things that go
>   wrong once the design runs — a premise is a fact the design stands on), as
>   a table: `Premise | Evidence (file:line + quoted snippet) | Status`.
>   `Status` is exactly one of `VERIFIED` (the cited line was read and its
>   snippet reproduced in the table) or `UNVERIFIED` (not yet checked) — no
>   other value is valid. A bare `file:line` citation without the quoted
>   snippet does not count as `VERIFIED`. Typically 3–5 premises; skip one
>   already stated verbatim in "What we're building" or "Where it lives".

Then, after the existing `"Does that match what you have in mind?"` line and
before the "After the last section, ask explicitly" handoff line, add:

> Every row in the Load-bearing premises table must read `VERIFIED` with its
> snippet quoted before the handoff question is asked — resolve any
> `UNVERIFIED` row (read the code, or ask the user directly) first.

**Change 2 — `SKILL.md` Step 4.5 (`:129-140`, the Unknown Matrix table)**:
append one sentence directly after the Unknown Matrix table (before the "Ask
at most 1–2 confirmation questions..." paragraph), targeting the same failure
shape upstream named — a claim of the form "the system/server/DB already
knows/stores X":

> When the design depends on a claim of the form "the system / server / DB
> knows, stores, or can determine X", confirm X's storage location and scope
> (tenant / project / session / none) against the actual schema or model
> definitions before treating it as known — this shape of assumption has no
> identifier to grep because the field it depends on may not exist, so it
> survives even a thorough Step 1 codebase read unless checked explicitly.
> Carry the result into Step 5's Load-bearing premises table.

**Change 3 — `SKILL.md` Validation Checklist (`:210-224`)**: add one line
after the existing Step 5 checklist item (`"Step 5 surfaced the design in
sections and received explicit per-section confirmation"`):

> - [ ] Step 5's Load-bearing premises table was presented with every row
>   marked `VERIFIED` (no `UNVERIFIED` or other status value), each with its
>   evidence snippet quoted rather than just cited, before the handoff
>   question was asked

**Change 4 — `README.md` line 19** (Step 5 summary bullet): extend the
existing bullet to mention the premises table and the block condition,
matching the phrasing style already used for other steps in that list.

## Implementation Steps

- [ ] Step 1: Edit `SKILL.md` Step 5 — insert the Load-bearing premises
      bullet and the pre-handoff resolution sentence
      → verify: `grep -n "Load-bearing premises\|UNVERIFIED" claude-code/skills/ywc-brainstorm/SKILL.md` returns ≥2 lines
- [ ] Step 2: Edit `SKILL.md` Step 4.5 — append the schema/scope verification
      sentence after the Unknown Matrix table
      → verify: that paragraph contains the words "tenant / project / session"
- [ ] Step 3: Edit `SKILL.md` Validation Checklist — add the one new line
      → verify: checklist item count increased by exactly 1 (`grep -c "^- \[ \]" claude-code/skills/ywc-brainstorm/SKILL.md` before/after)
- [ ] Step 4: Edit `README.md` line 19 — sync the Step 5 summary bullet
      → verify: line mentions "premises" and "UNVERIFIED" (or the Korean equivalent phrasing already used in that file)
- [ ] Step 5: Run verification commands below
      → verify: all commands exit 0

## Verification

```bash
bash scripts/validate.sh
grep -n "Load-bearing premises\|UNVERIFIED" claude-code/skills/ywc-brainstorm/SKILL.md
grep -n "premises" claude-code/skills/ywc-brainstorm/README.md
wc -l claude-code/skills/ywc-brainstorm/SKILL.md
```

Expected outcome: `validate.sh` exits 0; both greps return non-empty matches;
`wc -l` shows a modest increase (current 240 lines → roughly 250–255).

## Risks and Rollback

| Risk | Likelihood | Mitigation / Rollback |
|---|---|---|
| Premises table becomes a rubber-stamp (rows marked `VERIFIED` without real verification) | Medium | Mitigated by porting the already-hardened upstream wording verbatim (quoted-snippet requirement, constrained Status enum) rather than the original, weaker draft |
| Adds dialogue overhead to `ywc-brainstorm` sessions | Low | Table is capped at "typically 3–5 premises" per upstream's own observed norm; most resolve via a quick grep |
| Drifts from upstream wording over time (independent skill roots, no auto-sync) | Low, accepted | Same accepted trade-off as every other skill in this repo's independently-maintained roots — noted, not blocking |
| `validate.sh` regression from a malformed edit | Low | Plain prose/table edits to an existing skill file; `validate.sh` checks frontmatter/structure, not prose content — re-run after edit |

## Acceptance Criteria

- [x] `ywc-brainstorm` Step 5 will not ask the handoff question while any
      Load-bearing premises row is `UNVERIFIED`
- [x] Step 4.5's Blind-spot pass explicitly requires schema/scope
      verification for "system knows X" premises
- [x] `README.md`'s Step 5 summary matches `SKILL.md` (and `README.en.md`,
      `README.ja.md`, `README.ko.md` — Tier 1 locale set fully synced;
      `README.zh.md`/`README.es.md` are Tier 2 auto-generated and were
      already stale before this change — regeneration via
      `scripts/translate.sh` is a separate, non-blocking follow-up)
- [x] `bash scripts/validate.sh` passes
