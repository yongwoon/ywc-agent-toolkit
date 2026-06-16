# Review Learnings File Format

The canonical specification for `docs/review-learnings.md`. The SKILL.md body shows the summary; this file is the full contract.

## Design principles

1. **What + WHY + polarity, always.** A learning that records only *what* to flag cannot be applied to a similar-but-different case and cannot be told apart from an overfit nitpick. The `Why` is the generalization key.
2. **Polarity is first-class.** Reviews improve by *adding* checks (`DO` / `DO-NOT`) **and** by *suppressing* known false positives (`FALSE-POSITIVE`). A file that only ever adds checks grows noisier over time; the suppression half is what keeps signal high.
3. **Narrowest scope that captures the class.** Scope is a file glob (`**/*.sql`, `src/api/**`, `**/*.test.ts`) or the literal `repo` for genuinely universal conventions. Over-broad scope is the main source of cross-context review noise.
4. **Human-editable and version-controlled.** The file is committed; learning changes show up in PR diffs, so the team can review how the reviewer's behavior is evolving.
5. **Deprecate, never silently delete.** The history of why a rule was abandoned is itself a learning.

## Full document structure

```markdown
# Review Learnings — [Project Name]

<!-- updated: YYYY-MM-DD -->

## How this file is used

`ywc-impl-review` loads this file before reviewing and injects the learnings whose
`Scope` matches the changed files into each reviewer. Each entry records what to do,
**why** it matters (so it generalizes), and a polarity. Add a short AGENTS.md or
CODEX.md instruction telling agents to read this file before implementation
reviews when you want every Codex session to share the same context.

## Learnings

| ID | Scope | Category | Polarity | Rule | Why | Provenance |
|----|-------|----------|----------|------|-----|-----------|
| L001 | `**/*.sql` | Security | DO | ... | ... | PR#42, 2026-06-13 |

## Deprecated

| ID | Scope | Category | Rule | Deprecated | Reason / Superseded-by |
|----|-------|----------|------|-----------|-----------------------|
| ~~L003~~ | `src/api/users.ts` | Performance | ... | 2026-06-13 | superseded by L007 |

## Change log

- 2026-06-13 — +L007 (Performance/DO, src/api/**); ~L003 deprecated (superseded by L007)
```

## Field definitions

| Field | Rule |
|---|---|
| `ID` | Stable `L###` identifier. Never reuse a deprecated ID. Other entries may reference it (`superseded-by L007`) |
| `Scope` | A file glob matched against changed-file paths, or the literal `repo`. Narrowest glob that captures the class |
| `Category` | One of: `Correctness`, `Security`, `Performance`, `Error-handling`, `Contract`, `Test`, `Style`, `Convention`. Aligns with the `ywc-impl-review` aspects so a learning can be routed to the right reviewer |
| `Polarity` | Exactly one of: `DO` (add this check), `DO-NOT` (forbid this pattern), `FALSE-POSITIVE` (stop flagging this — it is acceptable here) |
| `Rule` | One imperative sentence. The behavior, not the incident |
| `Why` | The rationale. Must explain the underlying reason, not restate the rule. This is what lets the learning apply to similar-but-not-identical code |
| `Provenance` | Where it came from + date: `PR#<n> finding`, `dismissed PR#<n>`, `user feedback`, `review <date>` |

## Worked examples

```markdown
| L001 | `**/*.sql` | Security | DO | Every query on an ownership-scoped table includes the owner-key predicate explicitly | App-layer filtering fails open the moment one query forgets `WHERE owner_id = ?`; the DB is the last line of defense for the tenant boundary | PR#42 finding, 2026-06-13 |
| L002 | `**/*.test.ts` | Test | FALSE-POSITIVE | Do not flag top-level `await` in test setup files as a missing-await bug | The test runner supports top-level await in setup; flagging it is pure noise that the team has rejected twice | dismissed PR#51, 2026-06-13 |
| L004 | `src/components/**` | Convention | DO-NOT | Do not introduce a new color literal; use a token from `tokens.css` | The design system enforces palette via CSS custom properties; raw literals drift and break theming | user feedback, 2026-06-13 |
| L007 | `src/api/**` | Performance | DO | Batch N+1 ORM reads behind a single query or a dataloader | Per-row queries inside a request loop dominate p95 latency under production load | review 2026-06-13 |
```

## Anti-examples (do not write these)

| Bad entry | Why it is bad | Fix |
|---|---|---|
| Rule: "Fix the bug in users.ts:42" | Overfit to one line; not a class | Generalize to the pattern + scope to a glob |
| Why: "Because it is wrong" | Restates the rule, no rationale | Explain the underlying mechanism |
| Scope: `repo`, Rule about TS generics | Over-broad; fires on `*.md`, `*.sql` | Scope to `**/*.ts` |
| A `DO` learning that duplicates an existing one | File bloat, contradictory drift | `MODIFY` the existing entry instead |
