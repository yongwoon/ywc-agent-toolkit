# Toolkit Eval — Trigger-Case Coverage Backfill

> Status: Draft
> Scale: Medium
> Created: 2026-08-12
> Author: Claude (ywc-plan)
> Spec Reference: `.claude/skills/ywc-toolkit-eval/evals/scorecard.md` (2026-08-12 full-cycle run), `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md`

> **Operative Sections:** The original specification applies except where
> `## Iteration 1 Amendments`, `## Iteration 2 Amendments`,
> `## Iteration 3 Amendments`, or `## Iteration 4 Amendments` refines it.
> Sections marked `> ⚠️ SUPERSEDED by Iteration N` are superseded on the
> specific point the marker names — everything else in those sections
> still applies. Resolve conflicts in order
> **Iteration 4 > Iteration 3 > Iteration 2 > Iteration 1 > original**.
> Chained supersessions (final fix in each chain is authoritative):
> Fix A → A2 → Fix X (step 4c only; Fix L/step 4a chain below is separate);
> Fix A2 step 4a → Fix L → Fix V; Fix A2 step 4c → Fix P → Fix X;
> Fix C → C2 → Fix S → Fix Z; Fix E → E2 → Fix R; Fix F → F2 (final);
> Fix B, Fix H → Fix J → (Fix M → Fix W, Fix Q); AC1 → Fix G (final);
> AC2 → Fix T; AC4 → Fix U; AC9 → Fix N → Fix Y; AC10 → Fix O (final);
> AC11 → (informed by Fix W); Fix D, Fix I (final, untouched since their
> iteration).

## Global Constraints

- Case authoring rules are canonical in `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md` — do not restate or reinterpret them here; every task below points back to that file.
- The coverage floor is defined in code, not prose: `COVERAGE_MIN_POSITIVES = 3`, `COVERAGE_MIN_COLLISIONS = 2` (`.claude/skills/ywc-toolkit-eval/scripts/score.py:73-74`), counted only over independently-sourced cases (`source: session-trace` or `user-prompt`).
- `evals/trigger-cases.json` lives under `.claude/skills/ywc-toolkit-eval/evals/` and is git-tracked (unlike `scorecard.md`/`history.json`, which are gitignored generated artifacts) — changes here are real, reviewable diffs.
- Codex-side skill/agent evaluation (`.codex/skills/ywc-codex-toolkit-eval`) is a separate root with its own trigger-case file; this plan does not touch it.

## Purpose

The 2026-08-12 full `ywc-toolkit-eval` run scored 48 skills and 13 agents. Only 4 skills (`ywc-commit`, `ywc-create-pr`, `ywc-debug-rootcause`, `ywc-handle-pr-reviews`) met the independently-sourced trigger-case floor needed to measure S1 (skill activation accuracy, weight 30/100); 0 of 13 agents met the floor for A2 (agent dispatch accuracy, weight 25/100). S1/A2 is the single heaviest-weighted axis in both rubrics. Until coverage exists, `score.py`'s `item_total()` returns `None` for these 57 items by design — they cannot report a real `/100` total no matter how good every other axis scores. This plan backfills `evals/trigger-cases.json` so every item in the catalog can be measured, then re-runs the eval cycle to confirm.

## Scope

- Mine and author independently-sourced (`session-trace` or `user-prompt`) `positive` and `collision` cases in `evals/trigger-cases.json` for the 44 skills and 13 agents currently below the floor.
- Collision cases pair each item with a real sibling named in its own `Do not use for ...` anti-trigger clause, per the authoring rule in `trigger-eval-method.md` ("the strongest evidence is the item's own anti-trigger").
- Batch the 57 items into parallelizable authoring tasks grouped by sibling cluster (so one task's collision research covers items that already reference each other).
- Re-run `ywc-toolkit-eval --mode full --target all` after backfill and diff the resulting `history.json` entry against the 2026-08-12 baseline to confirm coverage closed and no S1/A2 score regressed.

## Out of Scope

- Any further content-defect fixes beyond the 7 already applied this cycle (confidence-gate threshold, project-scaffold defaults, tech-research staleness, handle-pr-reviews script path, project-docs/spec-writer boundary, merge-dependabot wait steps, cloud-engineer security-engineer boundary) — those are closed, not reopened here.
- The broader stale `tools/claude-code/...` path-reference cleanup noted as a follow-up during this cycle (found in `ywc-impl-review`, `ywc-code-gen`, `ywc-plan`, `claude-code/skills/CLAUDE.md`) — separate, unscoped cleanup; track it as its own small plan.
- Changing `score.py`'s coverage-floor constants, the S1/A2 banding formula, or the mechanical scorer itself.
- Codex-side (`.codex/skills/ywc-codex-toolkit-eval`) trigger-case coverage — separate root, separate plan if needed.
- Re-litigating the 4 already-sufficient skills' existing cases.

## Existing Constraints Touched

| Existing artifact | Verified behavior | New content's interaction |
|---|---|---|
| `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md:7-21` | Three case kinds (`positive`/`negative`/`collision`); collision must name a genuinely competing sibling, preferably from the item's own anti-trigger; negatives must be in-domain but off-catalog | Every new case is one of the two kinds this plan authors (positive, collision); no new negatives are required (10 shared negatives already exist and are reused, see Data Model) |
| `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md:55-80` | `source` field decides floor eligibility: `session-trace` / `user-prompt` count, `description-derived` does not; a missing `source` is read as `description-derived` | Every new case **must** set `"source": "session-trace"` or `"source": "user-prompt"` explicitly — never omit the field and never let an LLM author a case by paraphrasing the item's own description |
| `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md:78-80` | "Do not mine prompts that name the item" — a prompt containing the skill's own name in text is trivially winnable | Mined/authored prompts describe intent, not the `ywc-*` name, matching the existing 4 items' case style (e.g. `"수정내용만 commit 해줘."`, not `"ywc-commit 실행해줘"`) |
| `.claude/skills/ywc-toolkit-eval/scripts/score.py:73-74,340-360` | `sufficient = positives >= 3 and collisions >= 2`, computed only over independent sources; duplicate case ids counted once | Each item's authored batch is checked against this exact function (via `--item <name> --format json`, reading `signals.coverage`) before the task is marked done |
| `evals/trigger-cases.json` (existing 381 cases) | Flat `{"schema", "description", "cases": [...]}` shape; each case is `{id, prompt, expected, kind, source, [impostor], [note]}` | New cases are appended to the same `cases` array — the file is never restructured, only extended |

## Acceptance Criteria

- [ ] **AC1 — Coverage floor met for every skill** `> ⚠️ SUPERSEDED by Iteration 1 — see Fix G (documented-exception carve-out)`: When `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target claude-code/skills --item <name> --format json` is run for each of the 44 currently-insufficient skills, system reports `signals.coverage.sufficient == true`, observable as `positives >= 3` and `collisions >= 2` in the same JSON output.
- [ ] **AC2 — Coverage floor met for every agent** `> ⚠️ SUPERSEDED by Iteration 4 — see Fix T (same exception carve-out as AC1)`: Same check via `--target claude-code/agents --item <name>` for all 13 agents, same `sufficient == true` observable.
- [ ] **AC3 — No description-derived cases counted toward the floor**: When `evals/trigger-cases.json` is inspected, every newly-added case has `"source"` explicitly set to `"session-trace"` or `"user-prompt"` — grep `grep -c '"source": "description-derived"'` against the diff shows `0` new occurrences.
- [ ] **AC4 — Collision cases name a real anti-trigger sibling** `> ⚠️ SUPERSEDED by Iteration 4 — see Fix U (stale "paired side" language removed per Fix F2)`: For each newly-added `collision` case, the `impostor` (or `expected`, on the paired side) value matches a skill/agent literally named in the item's own `Do not use for ...` frontmatter clause — observable by cross-referencing the case's sibling name against the item's `description` text.
- [ ] **AC5 — Full-catalog re-run reports real totals** `> ⚠️ SUPERSEDED by Iteration 1 — see Fix B ("61" corrected to "57")`: When `ywc-toolkit-eval --mode full --target all` is re-run after backfill, the resulting `scorecard.md` shows a numeric (not `?`) S1/A2 score for all 61 previously-unmeasured items, and the new `history.json` entry's `roots.<root>.measured` count rises from `4` (skills) / `0` (agents) to `48` / `13`.
- [ ] **AC6 — No regression on the 4 already-measured skills**: The re-run's S1 score for `ywc-commit`, `ywc-create-pr`, `ywc-debug-rootcause`, `ywc-handle-pr-reviews` does not drop below their 2026-08-12 baseline (5, 5, 4, 5 respectively), since their cases are untouched by this plan.

## Functional Requirements

### FR-1: Mining Pass — Recover Real Prompts Before Authoring Any New Ones

> ⚠️ SUPERSEDED by Iteration 1 — see §Iteration 1 Amendments, Fix E. The first bullet's tool naming and lack of a noise filter is replaced by the concrete procedure there.

Before any case is written, search for genuinely independently-sourced prompt candidates — do not default straight to hand-authoring `user-prompt` cases, because a case an LLM writes while reading the item's own description is `description-derived` by definition, and the whole point of this backfill is escaping that trap.

- Search available session/observation history (this environment's session-memory/observation tooling, e.g. `mem-search` / `session_search` style lookups, plus any local session transcript files under `~/.claude/projects/**/*.jsonl`) for prior real invocations of each of the 57 items — the same mechanism that plausibly produced the existing 12 `*-trace-*` cases already in the file (e.g. `commit-trace-1` "commit and push").
- For each hit, sanitize per the existing rule (strip hostnames/paths/credentials/internal identifiers; keep typos, mixed-language phrasing, terse fragments as-is) and record it with `"source": "session-trace"`.
- Classify each mined prompt: does the transcript show this item was the one that actually fired (→ `positive` for this item), or did a sibling fire instead / should have (→ `collision`, naming the real winner as `expected` and this item as `impostor`, or vice versa)?
- Items with zero mined history (expected for less-used or newer skills, and likely for most agents, which are usually dispatched programmatically rather than typed by a user) fall through to FR-2.

### FR-2: Fallback Authoring — Hand-Written `user-prompt` Cases

> ⚠️ SUPERSEDED by Iteration 1 — see §Iteration 1 Amendments, Fix F. The `collision` bullet below contradicts the dominant real convention (single-entry collision, not a positive+collision pair) and risks prompt-duplication inflation; follow the amendment instead.

For items where mining yields fewer than 3 positives or 2 collisions, hand-author the remainder as `"source": "user-prompt"` — a prompt written as if by a real user, in their own words, **without consulting the item's own `description` field while writing it**. Practically: read the item's *role* one level up (what a user asking for this would actually say) rather than transcribing its trigger phrases back at it. Reuse the item's own stated anti-triggers only to pick the *collision sibling*, never to phrase the *prompt itself*.

Each authored case:
- `positive`: a natural-language request (Korean, English, or Japanese, matching the item's own multilingual trigger mix) that a real user would type, whose only reasonable owner is this item.
- `collision`: authored in a pair — the same prompt is `positive` for the true owner and `collision` (with `impostor` set) for the item whose anti-trigger names that owner, per the pairing convention already used by the 4 existing sufficient items (e.g. `commit-vs-create-pr-1`).

### FR-3: Batch Plan (Skills — 8 batches, 44 items)

> ⚠️ SUPERSEDED by Iteration 2 — see Iteration 2 Fix I. The claim below that clustering keeps anti-trigger research within-batch is false for several batches (verified: 4 of S1's 6 items name real anti-trigger siblings in S2/S5) — the batch structure itself is unchanged, but the rationale sentence and the research instruction are corrected.

Group by sibling cluster so one task's anti-trigger research covers multiple related items:

| Batch | Items |
|---|---|
| S1 — Planning core (6) | `ywc-plan`, `ywc-brainstorm`, `ywc-tech-research`, `ywc-confidence-gate`, `ywc-spec-writer`, `ywc-spec-validate` |
| S2 — Spec convergence & execution orchestration (6) | `ywc-spec-ready`, `ywc-task-generator`, `ywc-agentic`, `ywc-sequential-executor`, `ywc-parallel-executor`, `ywc-code-gen` |
| S3 — Worktree / dev-env (4) | `ywc-worktrees`, `ywc-docker-isolate`, `ywc-refactor-clean`, `ywc-onboard-repo` |
| S4 — IaC / infra lifecycle (4) | `ywc-infra-design`, `ywc-iac-author`, `ywc-infra-review`, `ywc-infra-optimize` |
| S5 — Review / quality / security (5) | `ywc-impl-review`, `ywc-security-audit`, `ywc-ui-ux-review`, `ywc-design-renew`, `ywc-product-review` |
| S6 — Git / PR / release lifecycle (5) | `ywc-finish-branch`, `ywc-merge-dependabot`, `ywc-changelog-release-notes`, `ywc-release-pr-list`, `ywc-receive-review` |
| S7 — Durable-memory family (6) | `ywc-adr`, `ywc-project-mission`, `ywc-review-learnings`, `ywc-ubiquitous-language`, `ywc-project-docs`, `ywc-project-scaffold` |
| S8 — Testing / verification / misc (8) | `ywc-gen-testcase`, `ywc-e2e-test-strategy`, `ywc-tdd-ritual`, `ywc-verify-done`, `ywc-auth-implement`, `ywc-setup-language`, `ywc-skill-author`, `ywc-incident-postmortem` |

### FR-4: Batch Plan (Agents — 2 batches, 13 items)

> ⚠️ SUPERSEDED by Iteration 1 — see §Iteration 1 Amendments, Fix D. The 2-batch split below creates a cross-batch coverage dependency that FR-5 step 3's per-batch gate cannot satisfy; agents are authored as a single batch instead.

| Batch | Items |
|---|---|
| A1 — Implementer / author agents (7) | `ywc-architect`, `ywc-backend-coder`, `ywc-frontend-coder`, `ywc-qa-engineer`, `ywc-doc-writer`, `ywc-cloud-engineer`, `ywc-refactor-cleaner` |
| A2 — Reviewer / analyst agents (6) | `ywc-go-reviewer`, `ywc-python-reviewer`, `ywc-typescript-reviewer`, `ywc-performance-engineer`, `ywc-root-cause-analyst`, `ywc-security-engineer` |

Note: since collision cases must stay within one root (skills collide only with skills, agents only with agents — `trigger-eval-method.md:20`, "Collision siblings must share a root"), an agent batch's collision authoring may need to look across both agent batches (13 agents total) even though authoring itself is split into 2 tasks for parallelism.

### FR-5: Per-Batch Task Shape

> ⚠️ SUPERSEDED by Iteration 1 — see §Iteration 1 Amendments, Fix A (concurrency mechanism) and Fix C (id allocation). The "serialize... or merge sequentially" clause below is ambiguous and the "reuse existing id naming convention" step (point 2) causes silent case loss for 54/57 items; do not follow points 1-2 literally.

Each of the 10 batch tasks (independent, run in parallel — worktree isolation not required since all edit the same single JSON file; serialize the actual file writes or merge sequentially to avoid conflicting edits):

1. For each item in the batch, run FR-1 mining; fall back to FR-2 for any shortfall.
2. Author cases directly as new entries appended to `evals/trigger-cases.json`'s `cases` array (reuse existing `id` naming convention: `<slug>-pos-N`, `<slug>-vs-<sibling>-N`, or `<slug>-trace-N` for mined ones).
3. Run `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target <root> --item <name> --format json` per item in the batch; confirm `signals.coverage.sufficient == true` for every one before marking the batch done.
4. Report back per AC3/AC4 — no `description-derived` sources added, every collision traces to a real anti-trigger sibling.

### FR-6: Verification Cycle (1 task, after all batches land)

> ⚠️ SUPERSEDED by Iteration 1 — see Fix B ("61" corrected to "57" in step 2) and Fix H (remediation step added).

1. Run `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target all --format json` and confirm `[coverage]` stderr line reports `0 items below minimum` (or names only genuinely-exempted items, if any remain per Open Questions).
2. Re-invoke `ywc-toolkit-eval --mode full --target all` (the full judgment-tier cycle, same as the 2026-08-12 baseline run) to get real S1/A2 scores for all 61 items.
3. Diff the new `history.json` entry against the 2026-08-12 baseline entry: confirm `measured` rose to 48/13, `mean_total` is now computed over the full catalog (not just 4 items), and no previously-measured item's total dropped (AC6).
4. Regenerate `scorecard.md` and produce a fresh prioritized backlog — this becomes the input to the *next* improvement cycle, not this plan's own scope.

## Non-Functional Requirements

| Category | Requirement |
|---|---|
| Authoring quality | Every new case must survive the same "would this case be circular" check applied in `trigger-eval-method.md`'s Determinism Note — a case an LLM could win purely by re-reading the item's own description is invalid regardless of its declared `source` label. |
| Privacy | Mined session-trace prompts (FR-1) must be sanitized (no hostnames, absolute paths, credentials, or internal identifiers) before being written into a git-tracked file, per the existing "Sanitize, do not paraphrase" rule. |
| Idempotency | Re-running score.py's coverage check after a batch must be side-effect-free (read-only) so batches can be verified repeatedly without corrupting state. |

## Critical Surfaces

N/A — this is toolkit self-maintenance data (trigger-case prompts), not application code, auth, payment, or PII-handling surface.

## Data Model

N/A — no database change. The relevant "schema" is the existing case-object JSON shape already defined in `evals/trigger-cases.json` and documented in `trigger-eval-method.md`:

```json
{
  "id": "<slug>-pos-N | <slug>-vs-<sibling>-N | <slug>-trace-N",
  "prompt": "<natural-language request>",
  "expected": "<owner item name, or null for negative>",
  "kind": "positive | collision | negative",
  "source": "session-trace | user-prompt",
  "impostor": "<competing sibling name, collision only>",
  "note": "<optional: which item is likely to over-trigger, collision only>"
}
```

## API Contract

N/A — no API change.

## Edge Cases

- **Item has genuinely zero real usage history and no plausible hand-authored `user-prompt` case reads as non-circular** (e.g., a very narrow internal-orchestration-only skill a user would never type directly, like a step delegated only by another skill): flag as an Open Question rather than force a case that would just be `description-derived` in disguise. `trigger-eval-method.md:19` allows a documented exception for a missing *collision* only, never a substitute for a missing *positive*.
- **An item's only real sibling collision has since been renamed or merged**: verify the sibling name still resolves in the current catalog (`claude-code/skills/<name>/SKILL.md` or `claude-code/agents/<name>.md` exists) before authoring the pair; if not, pick the anti-trigger's current equivalent.
- **Two batches independently mine the same session transcript for the same prompt**: dedupe by prompt text before merging batches into the file — `score.py` counts duplicate case ids once, but a duplicated *prompt* under two different ids would silently inflate the count.
- **A mined prompt turns out to already exist in the file** (already covered by one of the 4 sufficient items' 12 existing traces, e.g. a prompt that mentions both `commit` and `create-pr` intent): do not re-add it under a new id; cross-reference by prompt text first.

## Dependencies

- `.claude/skills/ywc-toolkit-eval/scripts/score.py` (coverage-check tool, read-only use)
- `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md` (canonical authoring rules)
- Session/observation search tooling available in this environment, for the FR-1 mining pass (best-effort — absence of mined history for an item is not a blocker, see FR-2 fallback)

## Open Questions

- [ ] `> ⚠️ SUPERSEDED by Iteration 2 — see Iteration 2 Fix J.` For agents specifically, most dispatches are programmatic (`Task(subagent_type=...)` from another skill) rather than typed by a human — does a "prompt a user would type" framing even make sense for A2, or should agent positive/collision cases instead be phrased as the **calling skill's dispatch trigger text** (still a real, independently-sourced string, just not literally a chat message)? `trigger-eval-method.md` is written skill-first; this plan assumes the same case shape applies to agents via A2 but the mining source will differ in practice (dispatch-trigger prose in caller skills' bodies, not user chat prompts). Needs a decision from the eval owner before Batch A1/A2 authoring starts.
- [ ] How many of the 44 skills will genuinely have zero mineable history (FR-1 turns up nothing)? If it's a large fraction, the fallback-authoring load (FR-2) on this plan is much heavier than the batch sizing above assumes — worth a quick mining-only dry run on 2-3 batches before committing to the full 10-task plan.

## References

- `.claude/skills/ywc-toolkit-eval/evals/scorecard.md` — 2026-08-12 baseline scorecard (source of the 44/13 unmeasured list)
- `.claude/skills/ywc-toolkit-eval/evals/history.json` — baseline run entry this plan's re-run will diff against
- `.claude/skills/ywc-toolkit-eval/references/trigger-eval-method.md` — canonical case-authoring method
- `.claude/skills/ywc-toolkit-eval/references/skill-rubric.md`, `agent-rubric.md` — S1/A2 band tables

## Iteration 1 Amendments

`ywc-spec-validate` returned `DONE_WITH_CONCERNS` (Critical: 3, Warning: 4, Suggestion: 3) against the original draft. This section fixes every Critical and Warning; Suggestions are folded in as small corrections since they overlap directly with the Critical/Warning fixes below. Original sections carrying a `> ⚠️ SUPERSEDED by Iteration 1` marker are superseded on the specific point named there — everything else in those sections is unchanged.

### Fix A — Concurrency mechanism for the shared `evals/trigger-cases.json` file (Critical 1)

> ⚠️ SUPERSEDED by Iteration 2 — see Iteration 2 Fix A2. This fix's step list is missing a cross-batch prompt-dedup check and a transport-format contract for the returned case list; use Fix A2's restated FR-5 instead.

Supersedes FR-5's "run in parallel... serialize the actual file writes or merge sequentially" clause.

**Corrected mechanism**: batch tasks never write `evals/trigger-cases.json` directly. Each batch's mining (FR-1) and authoring (FR-2) happens independently and in parallel, but the batch task's *output* is a list of new case objects (not a file write) returned to the orchestrating session. The orchestrating session appends each batch's case list to `evals/trigger-cases.json` **one batch at a time, in the order batches complete**, running the FR-5 step 3 coverage check immediately after each append before starting the next batch's file write. This makes the file-mutation step single-writer by construction — parallelism is preserved for the expensive part (mining/authoring), and the cheap part (JSON append) is trivially serial.

Updated FR-5 (supersedes the original step list):

1. For each item in the batch, run FR-1 mining; fall back to FR-2 for any shortfall.
2. Return the batch's authored case objects (not a file write) to the orchestrating session, tagged with the batch name.
3. Orchestrating session appends the batch's cases to `evals/trigger-cases.json` (see Fix C for id allocation) and runs `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target <root> --item <name> --format json` per item in the batch, confirming `signals.coverage.sufficient == true` before appending the next batch.
4. Report back per AC3/AC4 — no `description-derived` sources added, every collision traces to a real anti-trigger sibling.

### Fix B — "61" corrected to "57" (Critical 2)

> ⚠️ SUPERSEDED by Iteration 2 — see Iteration 2 Fix J for a one-clause addition reconciling AC5's hard "57" with Fix G's exception carve-out.

Supersedes AC5 and FR-6 step 2's item count.

**AC5 (corrected)**: When `ywc-toolkit-eval --mode full --target all` is re-run after backfill, the resulting `scorecard.md` shows a numeric (not `?`) S1/A2 score for all **57 previously-unmeasured items** (44 skills + 13 agents), and the new `history.json` entry's `roots.<root>.measured` count rises from `4` (skills) / `0` (agents) to `48` / `13` — 61 items measurable catalog-wide in total, counting the 4 pre-existing.

**FR-6 step 2 (corrected)**: Re-invoke `ywc-toolkit-eval --mode full --target all` to get real S1/A2 scores for the 57 newly-covered items (61 total catalog items now measurable, including the 4 pre-existing).

### Fix C — Id-allocation step prevents silent case loss (Critical 3)

> ⚠️ SUPERSEDED by Iteration 2 — see Iteration 2 Fix C2 (corrected in Iteration 3 — this marker originally misnamed Fix A2). `<slug>` was never defined; verified live that substituting the item's full catalog name (`ywc-plan`) instead of the prefix-stripped form (`plan`) makes the inventory query return empty and reproduces the exact silent-drop bug this fix exists to close. Fix C2 defines `<slug>` explicitly.

Supersedes FR-5 point 2 ("reuse existing id naming convention").

54 of the 57 target items already have `description-derived` cases under ids like `<slug>-pos-1`/`<slug>-pos-2`/`<slug>-pos-3` (verified: e.g. `plan-pos-1`, `worktrees-pos-1`, `worktrees-trace-1` already exist). `score.py` dedupes by literal id with no warning — a new case authored under a colliding id is silently dropped and never counted. Add this as an explicit step, run **before** authoring any case for an item:

- Inventory existing ids for the item: `python3 -c "import json; d=json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json')); print(sorted(c['id'] for c in d['cases'] if c['id'].startswith('<slug>-')))"` (substitute the item's slug).
- Determine `max_n` — the highest existing `-pos-N`/`-vs-*-N`/`-trace-N` suffix for that slug (0 if none exist).
- Number every newly-authored case for that item starting at `max_n + 1`, regardless of kind (`-pos-`, `-vs-<sibling>-`, `-trace-`) — i.e. do not restart numbering at 1.

### Fix D — Agents authored as a single batch (Warning 1)

Supersedes FR-4's 2-batch agent split.

**Corrected FR-4**: all 13 agents are authored as **one batch** (A1, 13 items: `ywc-architect`, `ywc-backend-coder`, `ywc-frontend-coder`, `ywc-qa-engineer`, `ywc-doc-writer`, `ywc-cloud-engineer`, `ywc-refactor-cleaner`, `ywc-go-reviewer`, `ywc-python-reviewer`, `ywc-typescript-reviewer`, `ywc-performance-engineer`, `ywc-root-cause-analyst`, `ywc-security-engineer`). This removes the cross-batch dependency where one batch's collision case could be required to satisfy a sibling item owned by a different, independently-scheduled batch. Total task count is now **9 skill/agent-authoring batches + 1 verification task = 10 tasks** (8 skill batches unchanged from FR-3, 1 merged agent batch, 1 verification), still within the Medium-scale "4–15 expected tasks" range.

### Fix E — Concrete mining tools and noise filter (Warning 3)

> ⚠️ SUPERSEDED by Iteration 2 — see Iteration 2 Fix E2. This filter's exclusion list is too narrow (only catches skill-catalog/SKILL.md reproductions, not reproductions of this plan or `trigger-eval-method.md` itself — verified live: `session_search("commit")`'s top hits were this very drafting session's own tool calls and reference-doc excerpts, none of which match the two named categories) and its field names (`type`) don't match the MCP tool wrapper's actual schema (`role`/`entryType`).

Supersedes FR-1's first bullet.

**Corrected FR-1 first bullet**: Search available session/observation history using the concrete tools verified available in this environment — `session_search` (`mcp__plugin_oh-my-claudecode_t__session_search`) and `mcp__plugin_claude-mem_mcp-search__search` (with `type: "prompts"`) — plus, as a fallback, `grep` over local session transcript files under `~/.claude/projects/**/*.jsonl`. For each candidate hit, before treating it as a real mined case, apply this filter:

- Restrict to `type == "user"` entries only (assistant/system/tool-result entries are not user prompts).
- Exclude entries wrapped in `<local-command-caveat>`, `<command-name>`, or `<command-message>` tags — these are harness-injected, not typed by a human.
- Exclude entries that reproduce a skill-catalog listing (the `available-skills` system-reminder block) or an entire `SKILL.md` body verbatim — these are context injections, not usage evidence.
- Exclude hits whose session/timestamp is the current mining session itself (a mining pass searching for its own just-issued tool calls is self-contaminating, not historical evidence).

Items with zero surviving hits after this filter fall through to FR-2, unchanged.

### Fix F — Collision cases are a single entry, not a pair (Warning 4)

> ⚠️ SUPERSEDED by Iteration 2 — see Iteration 2 Fix F2. This fix changes the convention inside this plan but leaves `trigger-eval-method.md:15,101` (which this plan's own Global Constraints declare canonical) still saying "authored in pairs" — a batch task reading that file fresh could legitimately follow the stale instruction. Fix F2 makes the override explicit instead of silent.

Supersedes FR-2's `collision` bullet.

**Corrected FR-2 collision bullet**: `collision`: authored as a **single** case entry — the item that should win goes in `expected`, the competing sibling goes in `impostor`, both drawn from the pair's actual anti-trigger relationship. Do **not** also author a separate `positive`-kind entry sharing the same prompt text — `score.py`'s collision-counting already credits both `expected` and `impostor` from one entry (verified: 102 of 107 existing collision cases in the file follow this single-entry shape), and a duplicate same-prompt `positive` entry under a different id would inflate that item's positive count beyond what the evidence actually supports (the exact hazard the spec's own Edge Cases section warns against).

### Fix G — Documented-exception carve-out for AC1 (Warning 2)

Refines AC1 (additive — does not contradict the original criterion, only adds an exception path).

**AC1 (refined)**: ...as originally stated, **except** for any item where FR-1 mining and FR-2 fallback authoring both genuinely cannot produce 3 non-circular positives (see Edge Cases, first bullet) — such an item is tracked in an explicit exception list at the top of FR-3/FR-4's batch tables, requires the eval owner's documented sign-off per `trigger-eval-method.md`'s existing exception mechanism (extended here to cover missing positives, not just missing collisions — a repo-local extension of that rule, scoped to this plan only), and is excluded from AC1's `sufficient == true` requirement and from AC5's coverage-rise count. Expected size of this exception list: zero, pending the mining-only dry run in Open Questions item 2.

### Fix H — Remediation step for a failed post-merge check (Suggestion)

> ⚠️ SUPERSEDED by Iteration 2 — see Iteration 2 Fix J. This fix has no terminal condition if the single retry also fails; Fix J adds one.

Adds to FR-6 step 1 (additive).

If the FR-6 step 1 catalog-wide coverage check finds an item still `sufficient == false` after all batches land (a Fix A process failure, or a mining/authoring gap), do not re-run the full batch — identify the specific affected item(s), re-run FR-1/FR-2 for just that item, append via the Fix A mechanism, and re-check before proceeding to FR-6 step 2's full judgment-tier re-run.

### Minor correction

FR-1's "existing 12 `*-trace-*` cases" is corrected to **27** (verified count in `evals/trigger-cases.json`).

### Iteration 1 Acceptance Criteria (supplement to the original AC1–AC6)

- [ ] **AC7 — No file-write collision**: When `evals/trigger-cases.json` is inspected after all batches land, `len(cases) == len(set(c['id'] for c in cases))` (no duplicate ids), and the total case count equals the pre-backfill count (381) plus the sum of every batch's reported case count exactly (no batch's contribution is missing).
- [ ] **AC8 — Agents authored as one batch**: The task list shows exactly one agent-authoring task covering all 13 agents, not two.

## Iteration 2 Amendments

`ywc-spec-validate` returned `DONE_WITH_CONCERNS` again against the Iteration-1-amended spec (Critical: 1, Warning: 6, Suggestion: 5). One Critical from Iteration 1 (id-collision) was not actually closed — Fix C's `<slug>` placeholder was undefined, and live testing found the plausible literal reading (full catalog name, e.g. `ywc-plan`) reproduces the exact silent-drop bug Fix C exists to prevent. This section fixes that plus five Warnings surfaced during re-validation; Suggestions are folded in below since they're one-clause additions to the same fixes.

### Fix A2 — Corrected FR-5: batch count, transport format, and cross-batch dedup (supersedes Fix A)

> ⚠️ SUPERSEDED by Iteration 3 — see Iteration 3 Fix L (step 4a dedup scope) and Fix P (step 4c failure path). Step 4(a)'s dedup only checks against prior state, not against other cases in the same batch's own return; step 4(c)'s per-batch gate has no defined failure path.

**Fully restated FR-5** (this text is now authoritative in place of both the original FR-5 and Iteration 1's Fix A):

Each of the **9** batch tasks (8 skill batches per FR-3 + 1 merged agent batch per Fix D) mines/authors independently and in parallel. No batch writes `evals/trigger-cases.json` directly.

1. For each item in the batch, run FR-1 mining (per Fix E2); fall back to FR-2 (per Fix F2) for any shortfall.
2. Run the Fix C2 id-inventory step for every item in the batch before authoring, to determine each item's starting case number.
3. Return the batch's authored case objects to the orchestrating session as a single fenced ` ```json ` block, one array matching the §Data Model case-object shape exactly (`id`/`prompt`/`expected`/`kind`/`source`/`impostor`/`note`). A batch whose return does not parse as valid JSON matching that shape is treated as **not landed** — re-dispatch that batch, never partially merge it.
4. Orchestrating session, upon receiving a valid batch return: (a) cross-reference every new case's `prompt` text against every case already in the file (pre-existing 381 plus every previously-merged batch this run) — an exact or near-duplicate prompt under a new id is dropped and logged, not appended (closes the Edge Cases duplicate-prompt hazard); (b) append the surviving cases; (c) run `python3 .claude/skills/ywc-toolkit-eval/scripts/score.py --target <root> --item <name> --format json` per item in the batch, confirming `signals.coverage.sufficient == true`, before merging the next batch.
5. Report back per AC3/AC4 — no `description-derived` sources added, every collision traces to a real anti-trigger sibling.

### Fix C2 — `<slug>` defined explicitly (supersedes Fix C)

> ⚠️ SUPERSEDED by Iteration 3 — see Iteration 3 Fix S. The "0 of 381 ids start with `ywc-`" claim is still true, but the simple prefix-strip rule computes the wrong slug for at least `ywc-spec-ready` (existing ids use `specready-`, no hyphen) and `ywc-changelog-release-notes` (existing ids use `changelog-`, not the full name) — the id-prefix inventory query returns empty for these items even though real prior cases exist, understating `max_n`. This does not cause an id collision (the new author's ids use a different string than the legacy ones), but it does miss real existing evidence and produces an inconsistent second naming convention for the same item. Fix S adds an `expected`/`impostor` field-based cross-check.

**`<slug>` = the item's catalog name with the `ywc-` prefix stripped** (e.g. `ywc-plan` → `plan`, `ywc-worktrees` → `worktrees`). Verified: 0 of the 381 existing case ids in `evals/trigger-cases.json` start with the `ywc-` prefix — every existing id already uses the stripped form, so this is not a new convention, only a now-explicit statement of the existing one.

Corrected inventory command (fixes the ambiguity, otherwise identical to Fix C):

```bash
python3 -c "
import json
d = json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json'))
slug = '<item-name-without-ywc-prefix>'  # e.g. 'plan' for ywc-plan
print(sorted(c['id'] for c in d['cases'] if c['id'].startswith(slug + '-')))
"
```

Determine `max_n` (highest existing `-pos-N`/`-vs-*-N`/`-trace-N` suffix for that slug, 0 if none) and number new cases starting at `max_n + 1`, exactly as Fix C stated. Verified live: for `plan` this returns `max_n=4` (existing `plan-pos-1..4`); appending a case at `plan-pos-5` was correctly counted by `score.py` (`positives_total: 4→5`). For a genuinely new item like `adr`, this returns `max_n=0` and numbering starts at 1, as originally intended.

### Fix E2 — Widened mining filter and tool field-name note (supersedes Fix E)

> ⚠️ SUPERSEDED by Iteration 3 — see Iteration 3 Fix R. Rule 1 ("restrict to real user entries") is insufficient on its own: tool-result content can be stored under a `role`/`type` value of "user" while still not being a real typed prompt.

Extend Fix E's exclusion list with a fifth rule and a tool-specific note:

- (Rules 1-4 from Fix E unchanged: restrict to real user entries, exclude harness-injected tag wrappers, exclude skill-catalog/SKILL.md reproductions, exclude current-mining-session hits.)
- **Rule 5 (new)**: Exclude any hit that is discussion of, or reproduction of content from, this plan document, `trigger-eval-method.md`, or any other `ywc-toolkit-eval` reference doc — not just `SKILL.md` bodies. A session where someone is *talking about* the eval methodology is not evidence that a *user asked for* the skill/agent in question.
- **Tool field-name note**: `mcp__plugin_oh-my-claudecode_t__session_search` and `mcp__plugin_claude-mem_mcp-search__search` expose `role`/`entryType`-style fields, not a field literally named `type` — that raw `"type":"user"` name applies to the underlying `~/.claude/projects/**/*.jsonl` schema (the grep fallback), not the MCP tools' wrapper output. Apply "restrict to real user entries" using whichever field name the specific tool actually returns.

### Fix F2 — Explicit local override of `trigger-eval-method.md`'s "paired" language (supersedes Fix F)

Fix F's single-entry collision convention stands **as an explicit, stated local override** for this plan's authoring tasks only — not a change to the canonical reference doc, which stays out of scope per Global Constraints ("do not restate or reinterpret them here... every task below points back to that file") and per this plan's Out of Scope (no further content-defect fixes beyond the 7 already applied this cycle). Add this sentence verbatim to every batch task's dispatch prompt, immediately after the pointer to `trigger-eval-method.md`:

> "Note: `trigger-eval-method.md:15,101` describes collision cases as an authored *pair* (a positive + a collision sharing one prompt). For this backfill specifically, author collisions as a **single** entry instead (owner in `expected`, sibling in `impostor`, no paired positive) — `score.py` already credits both sides from one entry, and 102 of 107 existing collision cases in the file already use this single-entry shape. This overrides the reference doc's 'pairs' language for new cases authored under this plan only."

(If a future cycle decides `trigger-eval-method.md` itself should be corrected to describe single-entry collisions as the norm, that is new-content-defect-fix work for a separate plan, per this plan's Out of Scope.)

### Fix I — FR-3's clustering rationale corrected, not restructured (Warning, Completeness)

FR-3's 8 skill batches remain unchanged in composition — reshuffling them is out of scope for this iteration and was flagged only as an advisor candidate, not a blocking finding. What's corrected is the claim and the instruction:

**Corrected rationale**: batches are grouped by *rough* conceptual proximity for reading convenience, not because anti-trigger siblings are guaranteed to stay within a batch — verified false for at least S1 (4 of 6 items name real siblings in S2/S5). **Add to FR-5 (Fix A2) step 1**: when mining/authoring a collision case, the competing sibling named in the item's own anti-trigger clause may belong to a *different* batch than this one — author the collision case regardless of which batch owns the sibling; the sibling's own batch does not need to independently re-derive the same pairing. Fix A2 step 4's post-batch dedup check (by prompt text) is what prevents two batches from redundantly authoring the same cross-batch pair.

### Fix J — Bounded retry, AC5 reconciliation, and stale-reference cleanup (Suggestions)

> ⚠️ SUPERSEDED by Iteration 3 — see Iteration 3 Fix M (root-cause attribution) and Fix Q (FR-6 step 2 reconciliation, applying the same adjustment Fix J gave AC5).

Three small additions:

- **FR-6 step 1 (extends Fix H)**: if the single re-authoring retry Fix H describes also fails to reach `sufficient == true` for an item, do not retry again — route that item into Fix G's documented-exception list (with the eval owner's sign-off) rather than looping indefinitely.
- **AC5 (extends Fix B)**: append to the corrected AC5 text — "...(57, or fewer if any item is carved out under Fix G's documented-exception path; the target adjusts to `57 − |exceptions|`)."
- **Open Questions item 1**: this question is resolved by Fix D (agents authored as a single batch, eliminating the "before Batch A1/A2 authoring starts" framing) — the underlying question (does "user prompt" framing fit agent A2 cases, or should dispatch-trigger text from caller skills count as an equivalent independent source) is still open and still worth an eval-owner decision before the merged agent batch starts, just not gated on a since-eliminated batch split.

### Iteration 2 Acceptance Criteria (supplement to AC1–AC8)

> ⚠️ SUPERSEDED by Iteration 3 — see Iteration 3 Fix N (AC9) and Fix O (AC10). AC9 as stated duplicates AC7 without testing convention-adherence; AC10's post-hoc claim is false against the current baseline (5 pre-existing duplicate-prompt groups already exist) and is never scheduled as a required step.

- [ ] **AC9 — Slug convention verified**: Every id inventory command run during batch authoring uses the `ywc-`-prefix-stripped slug form, observable as zero newly-authored ids reusing an existing id already present in `evals/trigger-cases.json` before that batch's merge.
- [ ] **AC10 — No cross-batch prompt duplication**: After all batches land, no two cases in `evals/trigger-cases.json` share identical `prompt` text under different ids (checked by Fix A2 step 4 at merge time, verifiable post-hoc by grouping all cases by `prompt` and confirming every group has exactly one id).

## Iteration 3 Amendments

`ywc-spec-validate` returned `DONE_WITH_CONCERNS` a third time (Critical: 1, Warning: 9, folded Suggestions). The one Critical was a cross-reference bug introduced by Iteration 2 itself (a `SUPERSEDED` marker pointed to the wrong fix name) — corrected directly in place above, since it was a pure citation error with no technical content, following the same convention as Iteration 1's "Minor correction." The Warnings below are genuine residual gaps, none of which reproduce the original id-collision/data-loss defect.

### Minor correction (in place, no marker needed)

The `⚠️ SUPERSEDED by Iteration 2` marker under the original **Fix C** section named "Fix A2" as the fix defining `<slug>`; corrected in place to name **Fix C2** (the section that actually defines it), matching the top-of-file Operative Sections precedence table, which was already correct.

### Fix L — Intra-batch dedup (extends Fix A2 step 4a)

> ⚠️ SUPERSEDED by Iteration 4 — see Fix V. Missing the kind-based exception (a legitimate positive+collision pair sharing one real mined prompt, per Fix O, must not be dropped by self-dedup).

**Fix A2 step 4(a), extended**: cross-reference every new case's `prompt` text against (i) every case already in the file (pre-existing 381 plus every previously-merged batch this run) **and (ii) every other case in this same batch's own return** — a batch that authors two cases sharing prompt text (e.g., reusing one mined trace for two items) must dedup against itself before the orchestrator ever sees it, not just against prior state.

### Fix M — Root-cause attribution before the exception path (extends Fix J bullet 1)

> ⚠️ SUPERSEDED by Iteration 4 — see Fix W. The category (a)/(b) attribution was self-reported with no evidence requirement; Fix W requires attaching supporting evidence.

**FR-6 step 1, extended**: before routing a still-insufficient item into Fix G's exception list, the retry must record which of two categories caused the failure: (a) a genuine content gap — FR-1 mining and FR-2 fallback authoring both could not produce enough non-circular cases, matching the Edge Cases scenario Fix G was designed for, or (b) a process failure — a Fix A2 mechanism (transport parse, dedup, id allocation) malfunctioned and cases were lost or misattributed. Only category (a) is eligible for Fix G's exception list; category (b) is a bug in this plan's own execution and must be fixed and retried, not excused. The eval owner's sign-off on an exception-list entry must state which category applies.

### Fix N — AC9 corrected to test convention-adherence, not id-uniqueness (supersedes AC9)

> ⚠️ SUPERSEDED by Iteration 4 — see Fix Y. The regex's `[a-z-]+` sibling-name class excludes digits, failing on real in-scope items like `ywc-e2e-test-strategy`.

**AC9 (corrected)**: Every newly-authored case id for a given item matches the pattern `^<stripped-slug>-(pos|vs-[a-z-]+|trace)-\d+$` (per Fix C2 §Fix S's slug rule), observable by regex-matching every id added during this backfill against its item's expected slug. (AC7 already covers id-uniqueness catalog-wide; AC9's distinct job is verifying the *naming convention* was followed, not re-testing collision absence.)

### Fix O — AC10 corrected scope, and scheduled as a required FR-6 step (supersedes AC10)

**AC10 (corrected)**: After all batches land, no two **newly-authored** cases share identical `prompt` text with each other or with any pre-existing case — checked against the new cases only, not an absolute claim about the full file. (Verified: the pre-backfill baseline already has 5 duplicate-prompt groups — e.g. `commit-trace-4` / `commit-vs-createpr-trace-1` — where one real mined prompt is deliberately cited as both a positive for one item and a collision for another; this is a legitimate, intentional pattern per Fix I, not a defect, and AC10 must not flag it.)

**FR-6, new step 1a**: immediately after step 1's coverage check, group all cases by `prompt` text and confirm every group containing at least one newly-authored case has no duplicate beyond the legitimate positive/collision cross-citation pattern (same prompt, different `kind`, naming each other via `expected`/`impostor` — allowed; same prompt, same `kind`, unrelated items — not allowed). This is the check Fix A2 step 4(a)/Fix L perform per-batch; step 1a is the final catalog-wide confirmation.

### Fix P — Per-batch gate failure path (extends Fix A2 step 4c)

> ⚠️ SUPERSEDED by Iteration 4 — see Fix X. "Do not block the remaining batches" never restated what the new merge gate actually is; Fix X names it explicitly.

**Fix A2 step 4(c), extended**: if the per-batch `sufficient == true` confirmation fails for an item mid-run (not all 9 batches landed yet), apply the identical Fix M/Fix J remediation immediately for that item (re-run FR-1/FR-2 for just it, re-append, re-check) rather than deferring to FR-6 step 1's final pass — do not block the remaining batches from merging while one item's remediation is in flight, since batches are independent by item.

### Fix Q — FR-6 step 2 gets the same exception-count adjustment as AC5 (extends Fix J bullet 2)

**FR-6 step 2 (further corrected)**: get real S1/A2 scores for the 57 newly-covered items **minus any items carved out under Fix G's exception path** (61 total catalog items now measurable, minus `|exceptions|`, including the 4 pre-existing) — matching the same `57 − |exceptions|` adjustment Fix J already applied to AC5, so the acceptance criterion and the step that satisfies it never diverge.

### Fix R — Mining filter closes the tool-result-under-role-user gap (extends Fix E2)

**Fix E2 rule 1, extended**: "restrict to real user entries" is necessary but not sufficient — a tool-result or tool-output block can be stored under the same `role`/`type` value as a genuine user message. Add: exclude any "user"-labeled entry whose content is structured tool-output (JSON, stack trace, command output, file listing) rather than natural-language prose — a real typed prompt is prose:, an entry that is substantially a data dump is not evidence of what a user asked for, regardless of its role label.

### Fix S — Id-inventory falls back to field-based lookup when the prefix query is empty (extends Fix C2)

**Fix C2, extended**: the `<slug>`-prefix inventory (id-prefix matching) is the first check, but is not authoritative when it returns few or zero hits for an item with a real prior history — the file's legacy ids do not consistently follow the "full name minus `ywc-`" convention (verified: `ywc-spec-ready`'s existing ids use `specready-`, no hyphen; `ywc-changelog-release-notes`'s existing ids use `changelog-`, not the full name). Before treating `max_n = 0` as ground truth, also run a field-based check:

```bash
python3 -c "
import json
d = json.load(open('.claude/skills/ywc-toolkit-eval/evals/trigger-cases.json'))
item = 'ywc-spec-ready'  # full catalog name
matches = [c['id'] for c in d['cases'] if c.get('expected') == item or c.get('impostor') == item]
print(sorted(matches))
"
```

> ⚠️ SUPERSEDED by Iteration 4 — see Fix Z. The trigger condition below ("zero hits") is narrower than this fix's own stated rationale ("few or zero"); Fix Z widens it.

If this field-based check finds existing cases the id-prefix check missed, author new cases using the **id-prefix-derived slug going forward** (do not retroactively rename legacy ids — that would violate the append-only discipline this whole plan depends on) but record the item's true existing case count from the field-based check, not the id-prefix check, when deciding whether FR-1/FR-2 need to close a 3-positive/2-collision gap or a smaller one.

### Iteration 3 Acceptance Criteria (supplement to AC1–AC10)

- [ ] **AC11 — No process-failure items in the exception list** `> ⚠️ SUPERSEDED by Iteration 4 — see Fix W (evidence requirement makes this independently checkable, not self-reported)`: When the exception list (Fix G) is inspected after FR-6 completes, every entry's eval-owner sign-off states category (a) genuine content gap — no entry is present solely because of an unresolved Fix A2/Fix M category (b) process failure.

## Iteration 4 Amendments

`ywc-spec-validate` returned **zero Critical findings** for the first time this pass (Warning: 6, Suggestion: 3) — Critical count across iterations: 3 → 1 → 1 → 0. The remaining Warnings are refinement-tier: an unenforced attribution rule, an incomplete dedup exception, an unnamed gate state, a regex character-class gap, and one structural gap present since the original draft (AC2 never got AC1's exception carve-out). Fixed below; no Critical, no data-loss-class defect in any of them.

### Fix T — AC2 gets the same exception carve-out as AC1 (extends Fix G)

**AC2 (corrected)**: ...as originally stated, **except** for any agent where FR-1 mining and FR-2 fallback authoring both genuinely cannot produce 3 non-circular positives — tracked in the same exception list Fix G defines for skills, at the top of FR-4's batch table, with the same eval-owner sign-off requirement (extended by Fix W below to require evidence). This closes a gap present since the original draft: Fix G's own mechanism already scoped itself to cover FR-4 ("at the top of FR-3/FR-4's batch tables"), but AC2 was never given the parallel exception clause, and the document itself flags agents as the *more* likely case to need it (FR-1: agent dispatches are usually programmatic, not user-typed).

### Fix U — AC4's stale "paired side" language removed (supersedes AC4)

**AC4 (corrected)**: For each newly-added `collision` case, the `impostor` value matches a skill/agent literally named in the item's own `Do not use for ...` frontmatter clause — observable by cross-referencing the case's `impostor` field against the item's `description` text. (The original "or `expected`, on the paired side" clause described the pre-Fix-F2 paired-collision convention; Fix F2 makes every collision a single entry, so there is no separate paired case to check.)

### Fix V — Fix L's dedup exception for legitimate positive/collision pairs (extends Fix L)

**Fix L, extended**: the intra-batch (and cross-batch, per Fix A2 step 4a) dedup check drops an exact/near-duplicate prompt **unless** the two cases are a legitimate positive+collision pair — same prompt, different `kind` (one `positive`, one `collision`), the collision's `impostor` naming the item the positive's `expected` names (or vice versa) — matching the pattern Fix O already documents as valid for the pre-existing baseline (e.g. `commit-trace-4` / `commit-vs-createpr-trace-1`). Any other same-prompt duplicate (same `kind`, or unrelated items) is dropped as before.

### Fix W — Evidence requirement for exception-list attribution (extends Fix M)

**Fix M, extended**: the retry's category (a)/(b) determination must attach concrete evidence to the exception-list entry, not just a stated conclusion — for category (a) (genuine content gap), the FR-1 mining query/tool results showing zero surviving hits after the Fix E2/Fix R filter, and the FR-2 fallback attempt showing why no non-circular prompt could be authored; for category (b) (process failure), the specific Fix A2 step (transport parse, dedup, id allocation) that malfunctioned and its error output. The eval owner's sign-off confirms the attached evidence supports the claimed category, rather than confirming an unsupported assertion. This is what makes AC11 (below) actually independently checkable instead of a self-report rubber stamp.

### Fix X — Fix P's per-batch gate stated explicitly (extends Fix P)

**Fix A2 step 4(c), fully restated** (this is now the authoritative gate, replacing all three prior phrasings in the original, Fix A2, and Fix P): merging batch N+1 is gated on batch N's **append succeeding** — the batch's return parsed as valid JSON (step 4b) and the dedup pass (step 4a/Fix L/Fix V) completed without error. It is **not** gated on every item in batch N reaching `sufficient == true`. An item that fails its post-append coverage check is flagged and routed to Fix W's remediation (immediately, per Fix P, without blocking batch N+1's merge) — coverage sufficiency for all items is confirmed catalog-wide at FR-6 step 1, not per-batch.

### Fix Y — AC9 regex includes digits (supersedes Fix N)

**AC9 pattern (corrected)**: `^<stripped-slug>-(pos|vs-[a-z0-9-]+|trace)-\d+$` — widened from `[a-z-]+` to `[a-z0-9-]+` so sibling names containing digits (e.g. `ywc-e2e-test-strategy` → `e2e-test-strategy`) are matched. Verified: the real existing id `gen-testcase-vs-e2e-test-strategy-1` matches the corrected pattern and failed the original.

### Fix Z — Fix S's fallback trigger widened to match its own rationale (extends Fix S)

**Fix S, extended**: run the field-based check whenever the id-prefix check returns **fewer than 3 hits** for an item expected to have prior history (not only when it returns exactly zero). Verified this is the common case, not a 2-item exception: at least `ywc-finish-branch`/`finishbranch-trace-1`, `ywc-task-generator`/`taskgenerator-trace-1`, and one agent case (`agent-tsreviewer-vs-pyreviewer-1`) show the same split-slug pattern in the real file, beyond the two examples Fix S originally named. (No collision or data-loss risk regardless — `score.py` counts by `expected`/`impostor` field, not id shape — this fix improves inventory accuracy for authoring efficiency, not correctness.)

### Iteration 4 Acceptance Criteria (supplement to AC1–AC11)

- [ ] **AC12 — Agent exception parity**: If any agent is carved out under Fix T's exception path, AC2's `sufficient == true` target adjusts the same way AC1's does under Fix G (target = `13 − |agent exceptions|`).
- [ ] **AC13 — Exception evidence present**: Every entry in the exception list (Fix G/Fix T) carries the evidence Fix W requires, verifiable by reading the entry and confirming a mining-query result or an FR-2 attempt log (category a) or a specific Fix A2 step failure trace (category b) is attached — not just a category label.
