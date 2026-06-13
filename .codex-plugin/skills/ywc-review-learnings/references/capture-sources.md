# Capture Sources — Detailed Procedures

How `--mode update` derives a candidate learning from each `--source`. The SKILL.md body summarizes these; this file is the operational detail.

## `--source feedback` (default)

The user is correcting a review finding in conversation. The correction *is* the why.

1. Identify the finding being corrected and the user's stated reason.
2. Classify polarity from the correction:
   - "that was a false positive / that's fine here because…" → `FALSE-POSITIVE`
   - "you should always flag…" / "we require…" → `DO`
   - "never do…" / "don't allow…" → `DO-NOT`
3. Take the user's reason **verbatim** as the seed for `Why` — do not substitute your own rationalization. The user knows the project context the reviewer lacks.
4. Generalize the rule from the specific line to the class, then confirm scope.

## `--source review`

A `ywc-impl-review` run just finished. Promote findings worth catching earlier.

1. Take only **confirmed** findings (Phase 1 confident, or Phase 2 advisor-confirmed) — never a dropped or low-confidence candidate.
2. Prefer findings that **recur** (the same class appeared in more than one file or more than one recent review) — those are the highest-value learnings.
3. For each, derive `DO` / `DO-NOT` and write the why from the finding's root-cause line (the reviewer already identified it; the Confidence Gate requires root cause).
4. Skip a finding that is already captured as an active learning.

## `--source pr` (bot-comment harvest)

Distill an existing bot review (CodeRabbit / Codex Review) on a PR into learnings. Optional convenience — the skill works with no bot present.

### Fetch

```bash
# Inline (line-anchored) review comments from review bots on the PR
gh api --paginate "repos/{owner}/{repo}/pulls/<PR>/comments" \
  --jq '.[] | select(.user.login | test("coderabbitai|chatgpt-codex|github-actions"; "i"))
            | {id, path, line, body, in_reply_to_id}'
```

Line-anchored comments are the useful ones — they carry the file/line context that makes a precise learning (CodeRabbit's own best-practice guidance favors line-anchored feedback for exactly this reason).

### Classify (accept vs dismiss)

A bot comment only becomes a learning once a human has *reacted* to it. The reaction is the signal:

| Outcome signal | Polarity | Why source |
|---|---|---|
| Comment's thread is **resolved** and the fix appears in a later commit | `DO` | the comment's own rationale |
| A reply explains the comment was **wrong / not applicable here** | `FALSE-POSITIVE` | the reply's stated reason — this is the most valuable kind, since it teaches the reviewer to *stop* raising it |
| Comment is open, no resolution, no reply | — (skip) | not yet a learning |

This mirrors CodeRabbit's own loop: it records a learning from an accepted suggestion or a dismissed comment, and critically remembers *why* a comment was rejected — not merely that it was.

### Generalize

Bot comments are line-specific. Lift each to its class before writing (a `users.ts:42` SQL-injection comment becomes a `**/*.ts` or `**/*.sql` `DO` learning about parameterized queries), then run the same user-confirmation CHANGESET as every other source — never write harvested learnings without confirmation.
