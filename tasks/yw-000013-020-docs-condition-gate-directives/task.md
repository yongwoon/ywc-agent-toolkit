# yw-000013-020-docs-condition-gate-directives — Implementation Checklist

## Prerequisites

- [ ] `yw-000012-020` is completed (merged)
- [ ] `yw-000012-030` is completed (merged)

## Allowed Edit Scope

- [ ] Stay within the 8 `SKILL.md` files listed in README.md Key Files
- [ ] Do not touch the language/initials directives in `ywc-auth-implement` or `ywc-create-pr` — those are `yw-000013-010`'s scope even though both tasks touch these two files

## Stop Conditions

- [ ] Stop if a directive is reachable by an entry path this task's enumeration missed (E10) — report the missed path rather than shipping a partial gate
- [ ] Stop if gating a directive would change observable behavior (e.g. a branch that's supposed to always read the reference stops reading it) — NFR5 requires every directive's content stay reachable at the branch that needs it

## Implementation Steps

- [ ] Verify `ywc-sequential-executor/SKILL.md:78` against the amended AC7 regex (should already pass, no edit) — use as the shape template for the rest
- [ ] Condition-gate `ywc-auth-implement/SKILL.md:46,56,62,142` — for each, add the branch/step condition (e.g. "when running the policy interview", "when the generic fallback path is taken")
- [ ] Condition-gate `ywc-docker-isolate/SKILL.md:103,105`
- [ ] Condition-gate `ywc-create-pr/SKILL.md:351,369` (bot polling / PR conflict — only fires once CI has passed and a merge is attempted)
- [ ] Condition-gate `ywc-handle-pr-reviews/SKILL.md:224`, `ywc-merge-dependabot/SKILL.md:185`
- [ ] Verify `ywc-finish-branch/SKILL.md:156,196` and `ywc-parallel-executor/SKILL.md:88` and `ywc-sequential-executor/SKILL.md:203` already satisfy the amended AC7 regex (likely no edit — confirm, don't assume)
- [ ] Condition-gate `ywc-parallel-executor/SKILL.md:419` with an explicit "when `--draft` or `--aggregate-pr` is set" prefix — this one is currently unconditioned
- [ ] Condition-gate `ywc-sequential-executor/SKILL.md:126`
- [ ] For every directive touched, enumerate all entry paths into its consuming branch (E10) and confirm the gate holds on each path, not just the one being edited

## Task Verify

- [ ] `grep -rh 'Action required' claude-code/skills/*/SKILL.md | grep -vcE '\b(when|before|if|only)\b'` returns `0`

## Verification

- [ ] `bash scripts/validate.sh` exits 0
- [ ] `bash claude-code/skills/ywc-skill-author/scripts/validate-skill.sh claude-code/skills/<each of the 8 dirs>` exits 0 for each

## Implementation Notes (optional)

Line numbers in the README/task spec were off by +1 from the actual current
file state for `ywc-auth-implement` and `ywc-create-pr` (yw-000013-010 already
merged in, shifting lines by one). Re-ran the AC7 grep against the live tree
first; it reported only 7 lines actually failing, not all 16 listed. Edited
only those 7, plus `ywc-parallel-executor:419` per the task's explicit
semantic instruction (it mechanically contained the word "before" via its
line-wrapped continuation, so the regex alone would have missed that it
never actually named its real gating condition — `--draft`/`--aggregate-pr`).

Lines verified compliant with no edit needed (already state an explicit
condition per the amended AC7, confirmed by grep, not assumed):
- `ywc-auth-implement:46` — "before running the interview" (single entry:
  Policy Interview section, reached only past the Preflight Gate).
- `ywc-create-pr:352,370` and `ywc-handle-pr-reviews:224` — "before
  proceeding", same shape as the explicitly pre-approved
  `ywc-finish-branch:156` precedent.
- `ywc-merge-dependabot:185` — "before merging" appears later in the line.
- `ywc-finish-branch:156` — "now before proceeding" (canonical precedent
  cited in the task).
- `ywc-parallel-executor:88` — "before creating any worktree".
- `ywc-sequential-executor:78,203` — "when `--non-interactive` is set" /
  "before any range task begins".

E10 (multi-entry-path) check per edited directive — all had exactly one
entry path into the branch they gate, so a single condition phrase was
sufficient:
- `ywc-auth-implement:57` (generic-fallback.md) — only entered when stack
  evidence is insufficient (confirmed against the skill's own References
  table at SKILL.md:175, which already documented this same condition).
- `ywc-auth-implement:63` (subagent-status-actions.md) — Implementation
  Dispatch is reached by exactly one path (sequential document flow after
  the Preflight/interview/recommendation gates); gated "before dispatching
  any subagent below".
- `ywc-auth-implement:143` (security-checklist.md) — Security/E2E/PR Gates
  section has one entry, reached after Implementation Dispatch resolves;
  gated "before running the security audit".
- `ywc-docker-isolate:103,105` (port-allocation.md, preconditions.md) — both
  reference files are explicitly `setup`-mode-only per
  `preconditions.md`'s own header ("`--mode setup` 이 격리를 적용하기 전에
  확인하는 precondition"); `teardown`/`audit` never need them. Integration
  section confirms `setup` has one call site (Step 4a). Gated "before
  running `setup`".
- `ywc-finish-branch:196` (pr-conflict-resolution.md) — inside "Step 4
  final: Merge-Readiness Gate (normal-pr only)", explicitly skipped for
  `--mode local-merge/draft/skip-ci-wait/per-task-pr` (line 209). Single
  entry from the normal-pr Step 4 CI loop. Gated "before Step 5's
  `gh pr merge`".
- `ywc-sequential-executor:126` (external-url-policy.md) — only reached via
  Pre-flight step 5, which itself is skipped on a confirmed resume (Resume
  Detection runs before Pre-flight); no other invocation path reaches this
  reference outside step 5. Gated "before Pre-flight step 5".
- `ywc-parallel-executor:419` (aggregate-pr.md) — the "`--draft` and
  `--aggregate-pr` modes: Aggregate PR" subsection under Step 5 has exactly
  two entry flags, both of which the added condition covers. No behavior
  change: `--local-merge`/`--per-task-pr` never reached this text before
  either (NFR5 preserved).

No file outside the 8 owned `SKILL.md` files was touched; no referenced
file (`pr-bot-polling.md`, etc.) was reworded.

`bash scripts/validate.sh` reproduces exactly the one KNOWN pre-existing,
unrelated failure named in the task brief (`codex/skills/ywc-skill-author
S5: 4 -> 2`) — confirmed unrelated by design (this task never touches
`codex/`). Separately, `validate-skill.sh claude-code/skills/ywc-sequential-executor`
reports the file is 502 lines (> 500 cap); confirmed via `git stash` that
this was already true before this task's edit (net line delta from this
task's change to that file is 0 — a same-line text substitution). Left
unfixed as out of scope for a condition-phrase-only task.
