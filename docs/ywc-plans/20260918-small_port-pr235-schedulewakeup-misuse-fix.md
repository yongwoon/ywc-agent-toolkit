# Small Plan: Port PR #235 ScheduleWakeup-misuse fix (Claude Code)

## Goal

Port the root-cause fix from `develop-with-llm` PR
[#235](https://github.com/yongwoon/develop-with-llm/pull/235) into this
repository's `claude-code/skills/references/subagent-async-monitoring.md`:
replace the `## Mandatory Fallback Wakeup` section — which instructs the
orchestrator to actively arm a "scheduled-recheck" after every subagent batch
dispatch — with a `## Waiting for Completion` section that waits passively on
the turn boundary and the harness `<task-notification>` signal instead. Add a
mechanical gate to `scripts/validate.sh` that rejects `ScheduleWakeup(` call
syntax anywhere under a skill root, so the same defect cannot be
reintroduced silently.

## Why

`ScheduleWakeup` is a `/loop`-dynamic-pacing-only tool (confirmed by reading
its own tool description in this session: it explicitly warns "Do NOT
schedule a short-interval wakeup to poll for background work you started —
when harness-tracked work finishes, you are re-invoked automatically"). This
repository's `subagent-async-monitoring.md` currently instructs, as a
**mandatory** step after every concurrent subagent dispatch, that the
orchestrator "sets an explicit bounded wait/check point — the orchestrating
session's scheduled-recheck capability, where the runtime provides one" —
i.e. call `ScheduleWakeup` — rather than simply ending the turn and letting
the harness notification arrive. `ywc-parallel-executor`,
`ywc-sequential-executor`, and `ywc-impl-review` all cite this reference for
their monitoring contract (confirmed via grep — one citation each, two in
`ywc-impl-review`).

`develop-with-llm` hit this exact defect in production (`marketing-ecosystem`
project, 2026-08-30): the mandated `ScheduleWakeup` call injected a spurious
"Autonomous loop check" prompt into an ordinary `ywc-sequential-executor` run,
twice in twelve minutes, and PR #235 fixed it by (a) rewriting the section to
describe turn-boundary waiting instead of active scheduling, and (b) adding a
CI-enforced regression gate rejecting the call syntax anywhere under a skill
root — because the defect had shipped in a *shared reference* that no
per-skill check reached.

This repository's own prior session summary (top of this conversation, dated
2026-09-17) shows `ScheduleWakeup` among the tools actually invoked in a
session working on this repo's skills — consistent with the current wording
being followed literally. The fix is directly applicable and low-risk.

## Out of Scope

- **`codex/skills/references/subagent-async-monitoring.md`** — read in full
  during investigation. It is a structurally different, Codex-CLI-native
  contract (`spawn_agent`/`list_agents`/`wait_agent`/`interrupt_agent`
  primitives) that does not mention `ScheduleWakeup` or any Claude-Code-only
  tool at all — confirmed via `grep -rn "ScheduleWakeup" codex/` (zero
  matches). It does not carry this defect, so no edit is needed there. Per
  `claude-code/skills/CLAUDE.md` §"Codex-skill: Maintained Independently",
  the two roots are edited independently by design.
- **`plugins/ywc-agent-toolkit/skills/`** — confirmed via `.githooks/pre-commit`
  that this tree is generated **from `codex/skills/`**, not from
  `claude-code/skills/`, via `scripts/sync-codex-plugin.sh`. Since this plan
  makes no `codex/skills/` edit, no plugin regeneration is triggered or
  required.
- **`claude-code/skills/CLAUDE.md`'s "Subagent Async Monitoring Contract"
  summary section** — re-read during investigation; it restates the
  threshold table's numbers and the stall consequence but does not name
  `ScheduleWakeup` or describe the wakeup mechanism, so it is already
  consistent with the fixed reference file. No edit needed.
- **`ywc-parallel-executor/SKILL.md`, `ywc-sequential-executor/SKILL.md`,
  `ywc-impl-review/SKILL.md`** — each contains exactly one (two for
  `ywc-impl-review`) pointer-only citation to
  `../references/subagent-async-monitoring.md`, with no inlined wakeup
  mechanics or threshold numbers (confirmed via grep across all three).
  Nothing in them needs to change.
- **Historical/changelog-style additions from upstream** (a new
  `docs/bug-reports/...` retrospective file, `TODO.md` checklist item,
  `.coderabbit.yaml` path instruction) — this repository has no equivalent
  `docs/bug-reports/` convention and no incident to retroactively document
  (the defect here was caught before causing a production incident in this
  repo). Not ported.
- **Python gate port** — upstream added `check_loop_only_tool_calls` to
  `tools/scripts/validate_ywc_skills.py`. This repository has no Python
  skill validator; its equivalent is the Bash `scripts/validate.sh`. The gate
  is reimplemented natively in Bash (see Implementation Steps), not ported
  as a Python file.

## Existing Constraints Touched

- `claude-code/skills/references/subagent-async-monitoring.md:15-25` — exact
  text of the `## Mandatory Fallback Wakeup` section to be replaced (verified
  via `Read`).
- `claude-code/skills/references/subagent-async-monitoring.md:27-29` — the
  `## Bounded Escalation on Stall` section that immediately follows and reads
  "If the hard escalation threshold is reached..." — this depends on the
  Threshold table (Batch size / Soft-check interval / Hard escalation
  threshold) that lives inside the section being replaced. The table must be
  **preserved**, not deleted, since it is this file's only definition of the
  480s/900s/300s/600s numbers `## Bounded Escalation on Stall` and
  `claude-code/skills/CLAUDE.md`'s summary both depend on.
- `scripts/validate.sh:700-749` (`check_cc_support_dirs`) — existing sibling
  function immediately above the insertion point; confirms the file's
  established style (`local` var declarations, `ERRORS=$((ERRORS + 1))`
  accumulation, one `echo "ERROR: ..."` per finding, no early `exit`).
- `scripts/validate.sh:805-833` — the main-flow call list where every
  `check_*` function is invoked in sequence; the new function's call must be
  added here for the gate to actually run.
- `.github/workflows/validate.yml` — the "Validate skills" CI step already
  runs `bash scripts/validate.sh` unconditionally, so no separate CI wiring
  is needed once the new check is called from within that script (unlike
  upstream, which needed a new standalone CI step because its Python gate had
  its own unit-test file run before the validator).

## Files to Touch

- `claude-code/skills/references/subagent-async-monitoring.md`
- `scripts/validate.sh`

## Implementation Steps

- [ ] **Rewrite `## Mandatory Fallback Wakeup` → `## Waiting for Completion`**
  in `claude-code/skills/references/subagent-async-monitoring.md` (replacing
  lines 15-25 in place, section order otherwise unchanged):
  - New prose describes the turn boundary as the waiting primitive: after
    dispatching a batch, the orchestrator ends its turn; the harness
    re-invokes the session with a `<task-notification>` when a dispatched
    agent finishes; **do not** call `ScheduleWakeup`, `Monitor`, a foreground
    `sleep`, or any other active polling/scheduling mechanism to wait on a
    dispatched subagent — name `ScheduleWakeup` explicitly as the wrong tool
    for this (it is `/loop`-dynamic-pacing only) since the prior "scheduled-
    recheck capability" wording was vague enough to be read as an
    instruction to use it.
  - **Preserve the Threshold table verbatim** (Batch size / Soft-check
    interval / Hard escalation threshold rows, 480s/900s/300s/600s) — it is
    still needed by the following `## Bounded Escalation on Stall` section.
    Reframe its purpose from "when to fire a scheduled wakeup" to "the
    elapsed-time bands `## Bounded Escalation on Stall` measures against
    when a signal arrives" — elapsed time is computed from the dispatch's
    wall-clock time to the current signal's (`<task-notification>` or the
    user resuming the session) wall-clock time, not from a timer.
  - State explicitly what happens when no signal ever arrives: the turn
    stays ended and control sits with the user — a visible, recoverable
    state — rather than a synthetic timer manufacturing activity.
  - Do not touch `## Unique Dispatch Labeling`, `## Full-Roster
    Reconciliation`, `## Bounded Escalation on Stall`, or `## Known
    Limitations` beyond what this section's rewrite requires for internal
    consistency (e.g. "Cancel the fallback..." sentence at the old line 25
    is replaced by "no fallback exists to cancel" framing, since there is no
    longer an armed timer to cancel).

- [ ] **Add `check_loop_only_tool_calls` to `scripts/validate.sh`**,
  inserted immediately after `check_cc_support_dirs` (after line 749) and
  before `check_agent_readonly_return_contract`:
  ```bash
  check_loop_only_tool_calls() {
    local root="$1"
    local file
    while IFS= read -r file; do
      [ -n "$file" ] || continue
      if grep -nE 'ScheduleWakeup[[:space:]]*\(' "$file" >/dev/null 2>&1; then
        while IFS= read -r hit; do
          echo "ERROR: ${file#./}:${hit%%:*}: \`ScheduleWakeup(\` call syntax — that tool is /loop-only. To wait on a dispatched subagent, end the turn and let the harness <task-notification> arrive (references/subagent-async-monitoring.md)"
          ERRORS=$((ERRORS + 1))
        done < <(grep -nE 'ScheduleWakeup[[:space:]]*\(' "$file" | cut -d: -f1)
      fi
    done < <(find "$root" -name '*.md' -type f)
  }
  ```
  Rejects call syntax (`ScheduleWakeup(`) only — bare prose mentioning the
  tool name (as the rewritten reference file now does, to name it as
  forbidden) passes untouched, matching upstream's gate design.

- [ ] **Call the new function from the main flow** in `scripts/validate.sh`,
  added to the call sequence after `check_cc_support_dirs` (near line 806)
  and again after `check_codex_support_dirs` (near line 814), passing
  `claude-code/skills` and `codex/skills` respectively as `root` — scanning
  both roots even though only claude-code currently carries the defect,
  matching upstream's "scan the whole skill root, not just the file known to
  be broken today" rationale.

## Verification

- [ ] `bash scripts/validate.sh` exits 0 with no new `ERROR` lines (confirms
  both the rewritten reference file's structural links are intact and the
  new gate finds zero `ScheduleWakeup(` call-syntax hits post-fix).
- [ ] Red-green-red check on the new gate: temporarily reinsert a literal
  `ScheduleWakeup({` block into a scratch copy of the reference file (or a
  throwaway `*.md` under `claude-code/skills/`) and confirm
  `bash scripts/validate.sh` reports exactly one new `ERROR` line naming that
  file; remove the scratch content and confirm the error disappears.
- [ ] `grep -n "## Mandatory Fallback Wakeup"
  claude-code/skills/references/subagent-async-monitoring.md` returns no
  match (old section name fully replaced).
- [ ] `grep -n "## Waiting for Completion\|Batch size | Soft-check interval"
  claude-code/skills/references/subagent-async-monitoring.md` confirms both
  the new section heading and the preserved Threshold table are present.
- [ ] `grep -c "ScheduleWakeup" claude-code/skills/references/subagent-async-monitoring.md`
  is non-zero (the tool is still *named*, in prose, as the thing not to call)
  while `grep -c "ScheduleWakeup(" claude-code/skills/references/subagent-async-monitoring.md`
  is zero (no call syntax survives in the fixed file itself).
- [ ] Re-read `## Bounded Escalation on Stall` and `## Known Limitations`
  once after the edit to confirm they still read coherently against the
  rewritten `## Waiting for Completion` section (no dangling reference to a
  "fallback" that no longer exists).

## Risks / Rollback

- **Risk**: the rewritten section could under-specify what "the user resuming
  the session" means as a reconciliation trigger, leaving a gap versus the
  removed active-wakeup mechanism. Mitigated by keeping the existing
  `## Full-Roster Reconciliation` section's "On receiving *any* signal" rule
  as the actual reconciliation trigger — `## Waiting for Completion` only
  changes *how the orchestrator waits*, not *what happens when a signal
  arrives*, which that other section already governs unchanged.
- **Risk**: the new Bash gate's `find ... -name '*.md'` could be slow on a
  very large tree. Bounded — both scanned roots (`claude-code/skills`,
  `codex/skills`) are a few hundred files at most, consistent with every
  other `find`/`grep -r` already used elsewhere in `validate.sh`.
- **Rollback**: two-file, single-commit change — revert the commit if the
  new wording causes confusion or the gate produces a false positive.

## Interfaces

N/A — no shared function/type signature crosses a file boundary; the new
`check_loop_only_tool_calls` function is called only from within
`scripts/validate.sh`'s own main flow.

## Confidence Gate

Not run as a separate step — this plan's scale (2 files, ~60 LOC net change
including the new Bash function and its two call sites, no DB/library/API-
contract impact, no cross-module change, direct upstream precedent already
reviewed and merged in `develop-with-llm`) is unambiguously Small per
`ywc-plan` Step 3's rubric (≤3 files, ≤300 LOC, single concern, no
hard-disqualifiers). Architectural Advisor Gate (Step 3.5) and Confidence
Gate (Step 3.6) apply to Medium/Large paths only.
