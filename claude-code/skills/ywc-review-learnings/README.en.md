# ywc-review-learnings

A skill that accumulates per-project code-review preferences so review quality improves over time. It implements CodeRabbit's "learnings" concept in a runtime-agnostic form (no hosted bot required), stored as a committable Markdown file `docs/review-learnings.md` that `ywc-impl-review` loads before reviewing.

The key property is that every learning records not just *what* to do but **why**. The why is what lets a learning generalize to similar-but-not-identical situations instead of degrading into a brittle keyword match.

## Modes

- **read** — load the learnings whose scope matches the review-target globs and inject them into the reviewers
- **update** — capture new learnings from user feedback, a completed review, or harvested PR bot comments
- **list** — display the current learnings
- **curate** — deprecate stale or contradictory learnings (never hard-delete)

## When to use

- Teach the reviewer that a false positive is acceptable in your environment, so it stops re-raising it next review
- Accumulate recurring findings (e.g. a missing owner-key predicate on an ownership-scoped query) as durable rules caught earlier
- Absorb the CodeRabbit / Codex PR comments you accepted into your internal review
- Add `@docs/review-learnings.md` to CLAUDE.md so every LLM session shares the project's review preferences

## Usage

```bash
/ywc-review-learnings
```

Or via natural language:

> "this is a false positive, remember it"
> "load the review learnings that apply to this path"
> "turn PR #128's CodeRabbit comments into review learnings"
> "clean up the review learnings"

## Input

- (optional) `--mode read|update|list|curate` — force a mode (auto-detected if omitted)
- (optional) `--target <glob|path...>` — review-target paths
- (optional) `--source feedback|review|pr|debug|incident` — learning source for update mode (default `feedback`; `debug`/`incident` capture root-cause / incident-prevention items)
- (optional) `--pr <number>` — PR to harvest bot comments from with `--source pr`
- (optional) `--output <path>` — learnings file path (default `docs/review-learnings.md`)
- (optional) `--dry-run` — show the CHANGESET without writing

## Output

- `docs/review-learnings.md` — a table of `ID / Scope / Category / Polarity / Rule / Why / Provenance`
- on update: a `Learnings added` confirmation block stating exactly what changed
- on first file creation: an activation prompt recommending you add `@docs/review-learnings.md` to CLAUDE.md (this reference is what makes every future review and LLM session load the learnings automatically)

## Output example

```markdown
# Review Learnings — ShopBot

<!-- updated: 2026-06-13 -->

## Learnings

| ID   | Scope          | Category | Polarity       | Rule | Why | Provenance |
|------|----------------|----------|----------------|------|-----|-----------|
| L001 | `**/*.sql`     | Security | DO             | Every query on an ownership-scoped table includes the owner-key predicate | App-layer filtering fails open the moment one query forgets WHERE owner_id=? | PR#42, 2026-06-13 |
| L002 | `**/*.test.ts` | Test     | FALSE-POSITIVE | Do not flag top-level await in test setup files | The runner supports it; flagging it is noise | dismissed PR#51, 2026-06-13 |
```

## Related skills

- `ywc-impl-review` — calls this skill in read mode before reviewing and in update mode after
- `ywc-handle-pr-reviews` — a dismissed bot comment can feed `update --source pr`
- `ywc-ubiquitous-language` — same per-project knowledge-file architecture, different content domain
- `ywc-receive-review` — discipline for *responding* to review feedback; this skill *stores* the durable lesson it produced
