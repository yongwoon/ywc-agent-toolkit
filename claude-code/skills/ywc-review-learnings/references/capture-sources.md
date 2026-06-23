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

## `--source debug` (root-cause harvest)

A `ywc-debug-rootcause` session has confirmed a root cause and the user wants that lesson to make future reviews catch the same class of defect earlier. This is the harness-feedback loop: a bug found in production tightens the review that should have caught it.

1. Take only a **confirmed** root cause — the symptom reproduced, the fix verified. A speculative or still-open hypothesis is not yet a learning.
2. Map the root-cause statement to the `Why` **verbatim from the investigation** (the reviewer needs the causal reason, not the symptom). The symptom becomes the provenance, not the why.
3. Classify polarity from the root cause:
   - the bug came from *doing* something that should be forbidden → `DO-NOT` (the most common debug polarity)
   - the bug came from *omitting* a guard/check that review should require → `DO`
4. Generalize from the one defective line to the defect **class**, then scope to the narrowest glob covering that class (e.g. a missing-null-check that crashed one handler → `**/*.handler.ts` `DO`, not `repo`).
5. Record provenance as `debug <symptom>` — the short symptom string identifies the originating investigation.
6. Run the same CHANGESET confirmation as every other source.

## `--source incident` (postmortem prevention harvest)

A `ywc-incident-postmortem` produced a recurrence-prevention action item whose *review-enforceable* part should become a durable learning. Only the part a code reviewer can actually check belongs here — runbook or alerting actions do not.

1. Take a prevention item from the postmortem's action list whose enforcement point is **a code-review check** (not an infra or process change).
2. Map the item to the `Why` (the failure mode it stops from recurring — the postmortem already states it).
3. Classify polarity: a required safeguard → `DO`; a forbidden pattern that triggered the incident → `DO-NOT`.
4. Scope to the affected paths identified in the postmortem; generalize to the class, not the single file that failed.
5. Record provenance as `incident <id>` — the incident identifier links the learning back to its postmortem.
6. Run the same CHANGESET confirmation as every other source.
