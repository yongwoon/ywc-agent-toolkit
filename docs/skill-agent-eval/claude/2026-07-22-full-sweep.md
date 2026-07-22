# Toolkit Scorecard — 2026-07-22 (full sweep)

Mode: full · Advisor escalations used: 0/5 · Activation judge runs: 3 (majority)

- `claude-code/skills` — 47 items, mean **93.8/100**, below 70: 0
- `claude-code/agents` — 13 items, mean **96.3/100**, below 70: 0

## Measurement warning — read before using these numbers

**S1/A2 scored 5 for all 60 items and the 3 judge runs disagreed on 0 of 353 cases.** That is not
evidence of a healthy catalogue; it is evidence that the axis has no discriminating power as
currently measured. The entire fixture corpus is authored *from the descriptions*, and the judge
reads those same descriptions — a closed loop. S1 carries the heaviest weight (30), so every total
below is inflated by an axis that cannot currently fail.

The mechanical axes are saturated for the same reason: all 47 skills score S2=S4=S5=5.

**Only S3, S6, A1 and A6 discriminated.** Treat those as the real signal.

## Where the variance actually is

| Axis | Weight | Distribution | Discriminating? |
|---|---|---|---|
| S1 / A2 activation | 30 / 25 | all 5 | no — circular fixture |
| S2 / S4 / S5 mechanical | 40 | all 5 | no — saturated |
| **S3 behavioural** | 20 | 5:3 · 4:36 · 3:6 · 2:2 | **yes** |
| **S6 catalog fit** | 10 | 5:16 · 4:24 · 3:7 | **yes** |
| **A1 role boundary** | 20 | 5:8 · 4:5 | yes (mild) |
| **A6 prompt quality** | 10 | 5:3 · 4:6 · 3:4 | **yes** |

## Prioritized backlog

Ranked by total ascending. Ties broken by the heaviest failing axis.

### 1. `ywc-release-pr-list` — 86.0/100  (S3=2 S6=4)

- **S3** SKILL.md:166 — The Rationalization Defense table (line 27) promises "fetch latest and re-apply, do not overwrite" on concurrent PR-description edits, but Step 7's actual procedure only ever does gh pr view once (line 118) then gh pr edit --body-file (line 166) with no re-fetch-and-reapply logic — the documented failure mode (concurrent edit) is asserted as handled but never implemented in the steps.
- **S6** nearest sibling `ywc-changelog-release-notes` — Both operate on merged PRs for a release, but one produces a PR-number list and the other prose release notes, separated by explicit anti-trigger.

### 2. `ywc-spec-validate` — 86.0/100  (S3=2 S6=4)

- **S3** SKILL.md:156 — The base "Completion Status rules" table (DONE = no Critical findings) directly contradicts the later Confidence Gate "Band-to-status mapping" (SKILL.md:270), which routes a zero-Critical spec scoring 70-89 to NEEDS_CONTEXT instead of DONE, with no stated precedence between the two tables.
- **S6** nearest sibling `ywc-spec-ready` — Single-shot spec review vs spec-ready's auto-driven convergence loop; anti-trigger cleanly names the distinction.

### 3. `ywc-changelog-release-notes` — 88.0/100  (S3=3 S6=3)

- **S3** SKILL.md:65 — Step 2 groups commits strictly by conventional-commit type (feat/fix/refactor/security) with no fallback procedure described for repositories that do not use conventional commits, a common real-world case left unhandled.
- **S6** nearest sibling `ywc-release-pr-list` — Both produce release-related summaries from merged PR/git history; changelog targets user-facing notes while release-pr-list targets a PR table, but a user request like "release summary" could plausibly route to either.

### 4. `ywc-design-renew` — 90.0/100  (S3=3 S6=4)

- **S3** SKILL.md:100 — Phase 3 step 1 says to "commit to a bold direction" and "choose one clear aesthetic point of view" from a list of examples with no criteria connecting the Phase 0 context to a specific choice - pure unguided judgment.
- **S6** nearest sibling `ywc-ui-ux-review` — Both touch existing frontend surfaces, but design-renew is visual/AI-slop specific while ui-ux-review covers usability/accessibility, with an explicit anti-trigger separating them.

### 5. `ywc-incident-postmortem` — 90.0/100  (S3=3 S6=4)

- **S3** SKILL.md:97 — Multiple workflow steps (Step 2 "Reconstruct timeline", Step 5 "Actions taken", Step 7 "Lessons learned") are one-line prompts with no procedure, source, or threshold for how to gather/verify the content, unlike the more rigorous Step 4/4.5.
- **S6** nearest sibling `ywc-debug-rootcause` — Both perform root-cause style investigation (5 Whys), but incident-postmortem is post-hoc production-incident reporting while debug-rootcause is pre-fix bug investigation, with anti-triggers cross-referencing each other.

### 6. `ywc-worktrees` — 90.0/100  (S3=3 S6=4)

- **S3** SKILL.md:66 — The skill states "--mode takes exactly one value... this skill does not infer" but never specifies the behavior when --mode is omitted or invalid, leaving that failure mode unhandled.
- **S6** nearest sibling `ywc-parallel-executor` — Worktree creation/audit/prune is a delegated subcomponent of parallel-executor and finish-branch; anti-trigger lists five siblings to route around.

### 7. `ywc-backend-coder` — 92.0/100  (A1=4 A6=3)


### 8. `ywc-code-gen` — 92.0/100  (S3=4 S6=3)

- **S3** SKILL.md:169 — Step 7's Verification Gate says "attempt one fix and re-run that layer" without bounding what a "fix" may touch, so the one-attempt discipline can't be mechanically checked against scope creep.
- **S6** nearest sibling `ywc-agentic` — Both orchestrate multi-file implementation dispatch (backend/frontend/QA in parallel) from a spec; overlap is real since code-gen is essentially agentic's execution phase, though code-gen is scoped to one-shot generation vs agentic's full autonomous loop.

### 9. `ywc-doc-writer` — 92.0/100  (A1=4 A6=3)


### 10. `ywc-frontend-coder` — 92.0/100  (A1=4 A6=3)


### 11. `ywc-handle-pr-reviews` — 92.0/100  (S3=4 S6=3)

- **S3** SKILL.md:103 — The Step 4 classification table splits "clear code change request" from "controversial or ambiguous change request" with no objective test, so an agent must guess which bucket a given comment falls into.
- **S6** nearest sibling `ywc-receive-review` — Both deal with responding to review feedback on an open PR; handle-pr-reviews is the automation/action layer while receive-review is the verify-before-agreeing discipline layer, and a vague "handle my PR review comments" request could route to either.

### 12. `ywc-impl-review` — 92.0/100  (S3=4 S6=3)

- **S3** SKILL.md:61 — The --working-tree file-list step says to "apply the repository's ignore / generated-path rules" to the combined tracked+untracked list without defining what those rules are or how to derive them beyond --exclude-standard, leaving detection of tracked-but-ignored generated files to inference.
- **S6** nearest sibling `ywc-security-audit` — Both are review-before-merge gates on implementation code; impl-review's 5-aspect review can overlap with security-audit's security-only lens, though anti-triggers point security-specific requests elsewhere.

## Two defects worth fixing first

Both scored S3=2, the lowest in the catalogue, and both are contradictions rather than vagueness.

1. **`ywc-release-pr-list`** — the Rationalization Defense promises "fetch latest and re-apply, do
   not overwrite" for concurrent PR-description edits, but Step 7 does one `gh pr view` then
   `gh pr edit --body-file`. The documented failure mode is asserted as handled and never
   implemented: a concurrent edit is silently lost.
2. **`ywc-spec-validate`** — the base Completion Status table (`DONE` = no Critical findings)
   contradicts the Confidence Gate band mapping, which routes a zero-Critical spec scoring 70–89
   to `NEEDS_CONTEXT`. No precedence is stated. This defect was hit live during the session that
   produced this sweep — the ambiguity had to be resolved by inference.

## Recurring S6 pattern

Seven skills scored S6=3, and they cluster into three contested pairs rather than seven
independent problems:

- `ywc-handle-pr-reviews` ↔ `ywc-receive-review` (both scored 3, each naming the other)
- `ywc-parallel-executor` ↔ `ywc-sequential-executor` (differentiator is execution mode, which a
  user request rarely signals)
- `ywc-spec-ready` ↔ `ywc-spec-validate`, and `ywc-changelog-release-notes` ↔ `ywc-release-pr-list`

Fixing the pairs is cheaper than fixing seven skills.

## Method

- Mechanical: `scripts/score.py --target all`
- Activation (S1/A2): 3 independent judge runs over all 353 fixture cases, description-only,
  majority verdict. 0 splits.
- S3: 4 batched judges reading each `SKILL.md` body in full; every score carries a `file:line`.
- S6: 2 batched judges over the full description catalogue.
- A1/A6: 1 judge reading all 13 agent files.
- Subagent reliability was poor at first — three judges returned nothing while consuming ~430k
  tokens. Switching the deliverable from an in-reply list to a written file fixed it.

