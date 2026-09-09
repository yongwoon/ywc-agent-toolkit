# Small Plan: Port scope guardrail + independent verification pass into ywc-impl-review (Claude Code)

## Goal

Port two quality/UX patterns already validated and merged upstream in
`develop-with-llm` PR [#227](https://github.com/yongwoon/develop-with-llm/pull/227)
into `claude-code/skills/ywc-impl-review/SKILL.md`:

1. **Step 2.5 — Scope Guardrail**: hard-block Phase 1 dispatch when the review
   scope is empty or excessive (200 files / 5,000 changed lines), mirroring the
   cloud `/code-review ultra` diff-size pre-check.
2. **Step 4.5 — Independent Verification Pass**: for every Critical/High
   **Confirmed** finding surfaced in Phase 1 (Step 3), dispatch one
   `model: sonnet` subagent per finding to attempt blind independent
   reproduction (file:line only, no original rationale) before the finding is
   reported as fact. Distinct from the existing Sonnet→Opus Advisor Pattern —
   not counted against `--advisor-budget`.

## Why

`ywc-agent-toolkit` has a standing practice of mining `develop-with-llm`'s PRs
for skill improvements (see prior ports of PR #220, #221, #225, #226). PR #227
closes a real gap: today a Phase-1-Confirmed Critical/High finding is reported
as fact with no independent check, and a pathologically large `--git-range`
scope is not pre-screened before five subagents each independently `Read` full
file contents (5x cost multiplication on an oversized diff). Both gaps exist
verbatim in this repository's `claude-code/skills/ywc-impl-review/SKILL.md`
(confirmed via grep — zero matches for "Scope Guardrail" or "Independent
Verification" in that file, nor in the `codex/` or `plugins/` mirrors).

## Out of Scope

- **`codex/skills/ywc-impl-review/SKILL.md`** — the codex mirror is
  intentionally *not* auto-synced with claude-code (see
  `claude-code/skills/CLAUDE.md` §"Codex-skill: Maintained Independently",
  which explicitly lists `ywc-impl-review` as a file where claude-code uses
  model-explicit Task-tool dispatch and codex uses generic worker/advisor
  terminology without `model:` fields). Porting this pattern to codex is a
  deliberate follow-up decision for the user to make separately, not bundled
  here.
- **`plugins/ywc-agent-toolkit/skills/ywc-impl-review/SKILL.md`** — this copy
  already carries pre-existing content drift from `claude-code/skills/`
  unrelated to this PR (different `description` frontmatter wording observed
  during investigation). Reconciling that drift is a separate cleanup task,
  not part of this port. Only `claude-code/skills/ywc-impl-review/SKILL.md` is
  touched.
- **Agent catalog files** (`claude-code/agents/ywc-architect.md`,
  `ywc-performance-engineer.md`, `ywc-security-engineer.md`, etc.) — reviewed
  for impact (see Risks section) and found to need **no changes**. Step 4.5 is
  a new Sonnet-only dispatch path that does not touch Advisor Pattern routing
  or any named-agent persona file.
- No new symbols are introduced — reuses existing `✅`/`❌`/`⚠️` vocabulary
  from `claude-code/skills/references/symbols.md` §2, which this file already
  uses (Confidence Gate band markers).
- No renumbering of existing steps 0/1/2/3/4/5/6/7 — new steps are inserted as
  `2.5` and `4.5` exactly as upstream did, to avoid breaking the hardcoded
  `ywc-impl-review Step 0` and `ywc-impl-review Step 3` cross-references
  confirmed present in `ywc-review-learnings/SKILL.md` and the three
  Tier-2 language-reviewer agents (`ywc-typescript-reviewer.md`,
  `ywc-python-reviewer.md`, `ywc-go-reviewer.md`).

## Existing Constraints Touched

- **Step numbering contract** — confirmed via repo-wide grep that no file
  references `ywc-impl-review Step 4`, `Step 5`, `Step 6`, or `Step 7`
  (only Step 0 and Step 3 are hardcoded elsewhere), so inserting `2.5`/`4.5`
  cannot break any external reference. `ywc-sequential-executor/SKILL.md:398`
  mentions "(Step 4.5)" but that refers to **its own** internal step
  numbering for the optional `/ywc-impl-review` invocation call site, not to
  `ywc-impl-review`'s internal steps — no collision, no edit needed there.
- **This repo's Phase 1 shape differs from upstream's assumption.** Upstream
  `develop-with-llm` PR #227 was written against a Phase 1 where all five
  subagents run at Sonnet/Haiku uniformly ("Pass `model` explicitly on each
  call so the executor layer stays at Sonnet or Haiku cost"). This repo's
  `ywc-impl-review/SKILL.md:66-71` instead runs **Security at Opus already in
  Phase 1** (`references/security-agent.md`; Security returns Confirmed
  findings only, no Advisor candidates — SKILL.md:70,85). This means Step 4.5
  in this repo must apply to Critical/High Confirmed findings from **all five**
  aspects, including Security's Opus-sourced findings — not just the four
  Sonnet/Haiku aspects. The ported wording is adjusted accordingly (see
  Implementation Steps below): drop the "Sonnet→Sonnet cross-check" framing
  (accurate upstream, inaccurate here for Security) in favor of "independent
  Sonnet reproduction check," since the verifier is always Sonnet but the
  original finding's source model varies by aspect.
- **This repo has a third review target upstream doesn't**:
  `--working-tree` (SKILL.md:39,62), in addition to `--code` and
  `--git-range`. The ported Scope Guardrail must classify `--working-tree`
  the same way as `--git-range` for the changed-line threshold (a real diff
  is available — staged + unstaged + untracked full contents — so the
  5,000-line threshold applies), not lumped in with `--code`'s "no diff
  available" case.
- **`## Confidence Gate` section already defines the `✅`/`⚠️`/`❌` band
  markers** (SKILL.md:199) — Step 4.5's verification markers reuse these
  exact three symbols, consistent with the file's own established
  convention, not `symbols.md`'s `Status Markers` alone.

## Files to Touch

- `claude-code/skills/ywc-impl-review/SKILL.md` (only file changed)

## Implementation Steps

- [ ] **Rationalization Defense table** (after the existing 8th row, before
  "User wants a quick review..." row — match upstream's insertion point
  relative to the "Reviewer agents agree" row): add one row —
  `"Phase 1 already marked this Critical, no need to double-check"` →
  `"Phase 1 'Confirmed' is a single lane's self-assessment, not independent
  confirmation — the same failure mode already named for 'reviewer agents
  agree, so the finding is correct.' Skipping Step 4.5 on a Critical/High
  Confirmed finding (including a Security finding confirmed at Opus)
  reintroduces exactly the false-Confirmed-positive risk it exists to catch."`

- [ ] **Advisor Pattern section** (after the existing budget-discipline
  paragraph, SKILL.md:51): add one paragraph — `"**Boundary with Step 4.5**:
  the Independent Verification Pass (Step 4.5) is a separate mechanism — an
  independent Sonnet reproduction check on Critical/High Confirmed findings
  from any Phase 1 aspect (including Security's Opus-sourced Confirmed
  findings), not a Sonnet→Opus escalation — and is not governed by this
  section's budget or Pattern B."`

- [ ] **Insert Step 2.5** between Step 2 (SKILL.md:59-64) and Step 3
  (SKILL.md:66), title "**Scope Guardrail**":
  - Empty scope: if `--git-range`'s changed-file list is empty, or `--code`
    resolves to zero reviewable files, or `--working-tree` finds no staged/
    unstaged/untracked changes, stop — report "Nothing to review: no changed
    files found for `<target>`" and suggest checking staging/commit state or
    the `--git-range`/`--code` value. Do not dispatch Phase 1. (This
    reconciles with the existing Step 2 rule at SKILL.md:64 — "If the
    selected target has no reviewable source files, return `NEEDS_CONTEXT`" —
    so Step 2.5's empty-scope branch and Step 2's existing `NEEDS_CONTEXT`
    rule must not duplicate; word Step 2.5 to explicitly say "this restates
    Step 2's existing NEEDS_CONTEXT rule for emphasis before the Scope
    Guardrail's excessive-scope check runs" rather than introducing a second,
    conflicting rule.)
  - Excessive scope (hard block): for `--git-range` and `--working-tree`,
    refuse Phase 1 dispatch when changed-file count exceeds **200 files** or
    total changed-line count (added+removed) exceeds **5,000 lines**. For
    `--code`, apply the 200-file limit only (no changed-line count — no diff
    exists for a raw path target). Report exact file/line counts, top 5 files
    by changed-line count, and instruct the user to narrow the range or split
    the invocation. Carry forward upstream's rationale verbatim for why the
    threshold is tighter than the cloud feature's 500-file/8,000-line limit
    (each of this skill's five Phase 1 subagents independently Reads full
    file contents, multiplying cost 5x on a large diff).

- [ ] **Insert Step 4.5** between Step 4 (SKILL.md:96-99) and Step 5
  (SKILL.md:101), title "**Independent Verification Pass**":
  - For every Confirmed finding (not Advisor candidate) with severity
    Critical or High from **any** Step 3 aspect — Architecture / Design /
    Devex / QA / **Security** — spawn one `model: sonnet` subagent per
    finding to attempt independent reproduction.
  - Bounded dispatch payload: verifier prompt contains only the finding's
    `file:line` and claimed severity — never the original description or
    rationale (anchoring-bias avoidance). Inject the Step 3 return-payload
    contract verbatim (SKILL.md:77-79 directive). Verifier reads the cited
    location independently and reports its own one-line description of the
    defect found there, or "could not reproduce."
  - Dispatch cap: 20 findings per invocation (Critical + High combined),
    Critical before High, Step 3 discovery order within a tier. Findings
    beyond the cap: `⚠️ Unverified — verifier dispatch cap reached`.
  - **Reproduced** → `✅ Verified` marker (reuse `symbols.md` §2 vocabulary —
    matches this file's own existing `✅` Confidence Gate band usage), carry
    to Step 6 unchanged.
  - **Could not reproduce** → tag `verification-failed`, add to the Step 4
    candidate pool for Phase 2 (same `--advisor-budget` cap, Critical > High >
    Medium ordering; within a tier, `verification-failed` findings rank ahead
    of same-severity Advisor candidates). Cap overflow: drop and log exactly
    as Step 4 already logs over-budget drops.
  - **Verifier execution failure** (timeout / error / malformed response /
    missing artifact) → distinct tag `verification-error` (never conflated
    with `verification-failed`). Route to the same Step 4 candidate pool when
    Phase 2 enabled; under `--no-advisor`, mark
    `⚠️ Unverified — Phase 2 disabled via --no-advisor`. Report
    `verification-error` counts separately from `Reproduced`/`Could not
    reproduce` in the Step 6 report's verification summary.
  - `--no-advisor` interaction: Step 4.5 still runs (independent of the
    Advisor Pattern), but a failed reproduction cannot escalate to a
    skipped Phase 2 — mark `⚠️ Unverified — Phase 2 disabled via --no-advisor`
    instead of a flat Confirmed claim.

- [ ] **Output Format template** (SKILL.md:114-168):
  - Summary section: add a line — `"Step 4.5 verification: X of Y
    Critical/High Confirmed findings independently reproduced; Z escalated
    to Phase 2 due to failed reproduction"` (after the existing "Phase 1
    findings" line, before "Phase 2 advisor calls").
  - Every per-category finding block (Architecture / Design / Devex /
    Security / QA — all five, since Step 4.5 now covers Security too, unlike
    upstream where Security wasn't itemized in this way): add a conditional
    line under each numbered finding — `"(if Critical/High Confirmed, Step
    4.5 ran) Verification: {✅ Reproduced independently at {file}:{line} |
    ❌ Could not independently reproduce — escalated to Phase 2 | ⚠️
    Unverified — Phase 2 disabled via --no-advisor}"`.

## Verification

- [ ] `bash scripts/validate.sh` — must report `Skill is valid!` for
  `ywc-impl-review` (structural frontmatter check only; body edits do not
  affect it, but run to confirm no incidental frontmatter damage).
- [ ] Manual step-order check: confirm the file reads
  `0, 1, 2, 2.5, 3, 4, 4.5, 5, 6, 7` with no other step renumbered.
- [ ] `grep -rn "ywc-impl-review Step" claude-code/ | grep -v ywc-impl-review/SKILL.md`
  — confirm the only hardcoded external references (Step 0, Step 3) still
  resolve to the same content they did before this edit.
- [ ] Confirm no new symbol was introduced —
  `grep -n "✅\|❌\|⚠️" claude-code/skills/ywc-impl-review/SKILL.md` should
  show only symbols already defined in `references/symbols.md` §2 /
  the file's own Confidence Gate section.
- [ ] Re-read the full edited file top to bottom once to confirm the two new
  steps read coherently against the surrounding prose (in particular that
  Step 2.5's empty-scope branch doesn't contradict Step 2's existing
  `NEEDS_CONTEXT` rule at SKILL.md:64).

## Risks / Rollback

- **Risk**: Step 4.5 measurably increases invocation cost (up to 20 extra
  Sonnet calls per review). Mitigated by the 20-finding dispatch cap and by
  scoping to Critical/High only (Medium/Low findings are unaffected).
- **Risk**: Wording that assumes uniform Sonnet/Haiku Phase 1 (upstream's
  framing) would be actively wrong here since Security runs at Opus — this
  plan's Implementation Steps explicitly correct that framing before writing
  the port, rather than copy-pasting upstream prose verbatim.
- **Rollback**: single-file, single-commit change — revert the commit if the
  new steps cause confusion or false-positive `verification-error` noise in
  practice.

## Interfaces

N/A — single file, no shared function/type signature crosses a boundary.

## Confidence Gate

Not run as a separate step — this plan's scale (1 file, ~35 LOC addition
including table rows, no DB/library/API-contract impact, no cross-module
change, direct upstream precedent already reviewed and merged) is
unambiguously Small per `ywc-plan` Step 3's rubric (≤3 files, ≤300 LOC,
single concern, no hard-disqualifiers). Architectural Advisor Gate (Step 3.5)
and Confidence Gate (Step 3.6) apply to Medium/Large paths only.
