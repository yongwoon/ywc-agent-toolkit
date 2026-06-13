---
name: ywc-review-learnings
description: >-
  (ywc) Use when capturing, reading, or curating a project's accumulated
  code-review learnings — durable natural-language review preferences that raise
  review quality per repository over time (the CodeRabbit "learnings" pattern,
  runtime-agnostic, no bot dependency). Triggers: "리뷰 학습 누적", "review learnings",
  "리뷰 피드백 축적", "이 지적 학습해둬", "이건 false positive 야 학습해줘", "리뷰 규칙 누적",
  "review 학습 갱신", "레뷰 학습", "レビュー学習", "review memory", "accumulate review feedback",
  "remember this review preference". Do not use for running an implementation
  review itself (use ywc-impl-review), for handling open PR review comments
  (use ywc-handle-pr-reviews), for responding to received review feedback in the
  moment with verify-before-agree discipline (use ywc-receive-review), for domain
  vocabulary (use ywc-ubiquitous-language), or for spec-level review (use
  ywc-spec-validate).
---

# ywc-review-learnings

**Announce at start:** "I'm using the ywc-review-learnings skill to read or update the project's accumulated review learnings."

This skill produces or maintains `docs/review-learnings.md` — a per-project, accumulating memory of code-review preferences that makes every future review sharper. It is the runtime-agnostic version of the CodeRabbit "learnings" idea: instead of relying on a hosted bot's internal database, the learnings live as a committed, human-editable Markdown file that `ywc-impl-review` loads before reviewing. Each learning records not just *what* to do but *why*, so it generalizes to similar-but-not-identical situations rather than degrading into a brittle keyword match.

It operates in four modes: **read** (load learnings applicable to a review target), **update** (capture new learnings from feedback, recurring findings, or harvested bot comments), **list** (display current learnings), and **curate** (deprecate stale or contradictory learnings).

## Rationalization Defense

When tempted to bypass a rule, check this table first:

| Excuse | Reality |
|---|---|
| "Record the rule, the WHY is obvious — skip it" | The *why* is the whole value. Without it the learning cannot be applied to a similar-but-different case, and a future reader (or LLM) cannot tell a real rule from an overfit one. A learning with no rationale is a keyword match waiting to misfire. |
| "This finding was rejected as a false positive — just delete the learning" | Deleting loses the lesson; the reviewer will re-flag it next PR. Record it as a `FALSE-POSITIVE` polarity learning **with the reason it was wrong**, so the reviewer stops raising it. CodeRabbit's precision comes from remembering *why* a comment was rejected, not just that it was. |
| "Append the new learning without reading the file" | Appending blind creates duplicate and contradictory entries. Always read the full `docs/review-learnings.md` before any write, and check whether the pattern is already captured. |
| "One learning per individual finding is most precise" | One-per-finding overfits to a single line and floods the file. Generalize to the *class* of issue (the pattern + the why), scoped to the narrowest glob that captures it. |
| "This contradicts an old learning — keep both, let the reviewer decide" | Two contradictory learnings make the reviewer's behavior non-deterministic. Newest-wins: deprecate the old entry with a pointer to the new one (`~~strikethrough~~` + note), never silently delete. |
| "Write the learnings without user confirmation, I inferred the intent" | An unconfirmed learning pollutes *every* future review on the matching glob. Always present the proposed ADD / MODIFY / DEPRECATE set for one confirmation round before writing. |
| "Scope it `repo`-wide so it always applies" | Over-broad scope is the main source of review noise — a TypeScript naming rule applied to `*.sql` is pure friction. Scope to the narrowest file glob that captures the real pattern; reserve `repo` for genuinely universal conventions. |

**Violating the letter of these rules is violating the spirit.** A learnings file full of unconfirmed, why-less, or over-scoped entries degrades review quality on every PR that touches a matching path — the opposite of its purpose.

## Arguments

| Parameter | Format | Default | Description |
|-----------|--------|---------|-------------|
| `--mode` | `--mode read\|update\|list\|curate` | auto-detect | Force a specific mode (see Mode Detection below) |
| `--target` | `--target <glob\|path...>` | changed files | Review-target paths/globs whose applicable learnings should be loaded (`read`) or attributed (`update`) |
| `--source` | `--source feedback\|review\|pr` | `feedback` | Where a new learning comes from in `update` mode (see Capture Sources) |
| `--pr` | `--pr <number>` | — | With `--source pr`, harvest bot (CodeRabbit / Codex) review comments from this PR via `gh` and distill them into learnings. Optional convenience — never required |
| `--output` | `--output <path>` | `docs/review-learnings.md` | Learnings file path |
| `--dry-run` | flag | off | Show the proposed CHANGESET without writing to disk |

### Mode Detection (when `--mode` is omitted)

| Condition | Auto-selected mode |
|---|---|
| Invoked by a review skill with a target, file exists | `read` |
| User is describing feedback on a finding ("this was wrong because…", "always flag…") | `update` |
| File absent, user wants to start accumulating | `update` (creates the file with the first learning) |
| User asks "what review learnings exist?" | `list` |

## Workflow

### Mode: read — Load Applicable Learnings

Invoked before a review (typically by `ywc-impl-review` Step 0).

1. **Read the file.** If `docs/review-learnings.md` is absent, return an empty applicable set and say so — never block a review on a missing learnings file.
2. **Match by scope.** For each learning, include it if its `Scope` glob matches at least one path in `--target` (or any changed file when `--target` is omitted). `repo`-scoped learnings always match. Skip `deprecated` entries.
3. **Emit a compact applicable block** in the [Applicable Learnings format](#output-format) — grouped by category, each line carrying the rule, the why, and the polarity (`DO` / `DO-NOT` / `FALSE-POSITIVE`). This block is what the caller injects into each reviewer subagent prompt. Keep it tight; a reviewer that drowns in learnings reviews worse, not better.

### Mode: update — Capture a New Learning

1. **Read the existing file** in full (or note its absence to create it). Parse all current learnings.
2. **Gather the candidate** from the declared `--source` (see Capture Sources below). Every candidate must yield three things before it can be written: the **rule** (imperative), the **why** (rationale that lets it generalize), and the **polarity** (`DO` adds a check, `DO-NOT` forbids a pattern, `FALSE-POSITIVE` suppresses a known wrong flag).
3. **Generalize, then scope.** Lift the candidate from the specific line to the issue *class*. Assign the narrowest `Scope` glob that captures the class. If a similar learning already exists, treat this as a `MODIFY`, not a duplicate `ADD`.
4. **Build the CHANGESET** for user confirmation: `ADD` / `MODIFY` / `DEPRECATE` lists. Show the why for each. Do not write any entry the user has not confirmed.
5. **Apply and echo.** Write confirmed changes, update the `<!-- updated: DATE -->` header, and print a `Learnings added` confirmation block listing exactly what changed — making the behavioral change explicit (the CodeRabbit pattern). Append a one-line entry to the file's change log.

6. **CLAUDE.md Integration Prompt.** The *first* time the file is created (it did not exist before this run), print the activation reminder so the learnings actually reach future reviews:
   ```text
   ★ To activate these learnings, add the following line to your CLAUDE.md so every
     review (and every LLM session) loads them automatically:
       @docs/review-learnings.md
   ```
   Print it only on first creation, not on every incremental update — repeating it each run is noise.

### Mode: list — Display Current Learnings

Print the active learnings (optionally filtered by `--target` glob or category). Show deprecated entries only when explicitly asked. Useful before a review to sanity-check what the reviewer will apply.

### Mode: curate — Deprecate Stale / Contradictory Learnings

1. Read the file. Identify candidates: contradictory pairs, learnings whose `Scope` glob no longer matches any file, or entries the user reports as no longer wanted.
2. Present a `DEPRECATE` list with the reason for each. On confirmation, mark with `~~strikethrough~~` and a `> deprecated YYYY-MM-DD: <reason / superseded-by #ID>` note. Never hard-delete — the history of *why* a rule was abandoned is itself a learning.

## Capture Sources (`--source` in update mode)

| Source | What it harvests | How |
|---|---|---|
| `feedback` (default) | A correction the user gave on a review finding — "that was a false positive because X" / "always flag Y because Z" | Take the user's reason verbatim as the *why*; classify polarity; confirm scope |
| `review` | Confirmed recurring findings from a just-completed `ywc-impl-review` | Promote a finding the reviewer is confident about (especially one that recurs) into a `DO`/`DO-NOT` learning so it is caught earlier next time |
| `pr` | Bot review comments (CodeRabbit / Codex) on a specific PR | `--pr <n>`; fetch via `gh`, keep only **accepted / resolved-by-fix** comments as `DO` learnings and **explicitly dismissed** ones (with the dismissal reason) as `FALSE-POSITIVE` learnings. A comment that was neither accepted nor dismissed is not yet a learning |

The detailed harvest procedure for `--source pr` (the `gh` query and the accept-vs-dismiss classification) is in [references/capture-sources.md](references/capture-sources.md).

## Output Format

The full learnings-file specification is in [references/learning-format.md](references/learning-format.md).

**`docs/review-learnings.md` (file) summary:**

```markdown
# Review Learnings — [Project Name]

<!-- updated: YYYY-MM-DD -->

## How this file is used
Loaded by ywc-impl-review before review; each entry records what + WHY + polarity.

## Learnings
| ID | Scope | Category | Polarity | Rule | Why | Provenance |
|----|-------|----------|----------|------|-----|-----------|
| L001 | `**/*.sql` | Security | DO | Every query on an ownership-scoped table includes the owner-key predicate | App-layer filtering fails open the moment one query forgets WHERE owner_id=? | PR#42 finding, 2026-06-13 |
| L002 | `**/*.test.ts` | Test | FALSE-POSITIVE | Do not flag a top-level `await` in test setup as a missing-await bug | Vitest supports top-level await in setup files; flagging it is noise | dismissed PR#51, 2026-06-13 |
```

**Applicable Learnings block (read-mode emission, injected into reviewers):**

```text
## Applicable Review Learnings (3)
[Security] DO — Every query on an ownership-scoped table includes the owner-key predicate.
   why: app-layer filtering fails open if one query forgets the WHERE clause. (L001, **/*.sql)
[Test] FALSE-POSITIVE — Do NOT flag top-level await in test setup files.
   why: the runtime supports it; flagging is noise. (L002, **/*.test.ts)
```

**`Learnings added` confirmation (update-mode emission):**

```text
✦ Learnings added (1 ADD, 0 MODIFY, 1 DEPRECATE)
  + L007 [Performance/DO, src/api/**] — Batch N+1 ORM reads behind a single query.
        why: per-row queries in a request loop dominate p95 latency under load.
  ~ L003 deprecated — superseded by L007 (was scoped too narrowly to src/api/users.ts).
```

## Validation

Before declaring complete:

- [ ] Every active learning has a non-empty `Why` (rationale, not a restatement of the rule)
- [ ] Every learning has a `Polarity` of exactly `DO`, `DO-NOT`, or `FALSE-POSITIVE`
- [ ] Every `Scope` is the narrowest glob that captures the class (no gratuitous `repo`-wide scope)
- [ ] No two **active** learnings contradict each other (the older was deprecated, not left to coexist)
- [ ] The user confirmed the CHANGESET before any write (no inferred-and-written entries)
- [ ] `docs/review-learnings.md` is parseable Markdown with no broken table rows
- [ ] `<!-- updated: DATE -->` header reflects today's date
- [ ] A `Learnings added` confirmation was printed for update mode
- [ ] On first file creation, the `@docs/review-learnings.md` CLAUDE.md integration prompt was printed

## Common Mistakes

- **Recording the rule without the why** — the single most common failure. A why-less learning cannot generalize and is indistinguishable from an overfit nitpick; the reviewer either ignores it or misapplies it.
- **Deleting a dismissed finding instead of recording it as `FALSE-POSITIVE`** — the reviewer has no memory of the dismissal and re-raises the same noise every PR. Capture the dismissal *with its reason*.
- **One learning per finding** — produces an unscannable file and overfits. Generalize to the class.
- **Over-broad scope** — `repo`-wide learnings that only apply to one language create cross-language review noise. Scope tightly.
- **Writing without confirmation** — an unconfirmed learning silently changes every future review on the matching glob.

## Integration

- **Upstream**: `ywc-impl-review` (Step 0 calls this skill in `read` mode; a post-review step calls it in `update --source review`), `ywc-handle-pr-reviews` (a dismissed bot comment can feed `update --source pr`)
- **Downstream**: `ywc-impl-review` consumes the read-mode Applicable Learnings block; the file is also a natural `@docs/review-learnings.md` reference in `CLAUDE.md`
- **Pairs with**: `ywc-ubiquitous-language` — same per-project-knowledge-file architecture (read/update modes, user-confirmed writes), different content domain (review preferences vs domain vocabulary)
- **Do not confuse with**: `ywc-receive-review` (discipline for *responding* to review feedback) — this skill *stores* the durable lesson that feedback produced
