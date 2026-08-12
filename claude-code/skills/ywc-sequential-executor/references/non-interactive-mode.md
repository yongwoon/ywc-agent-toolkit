# Non-Interactive Mode (`--non-interactive`)

> Referenced from: SKILL.md → Arguments (`--non-interactive`), Pre-flight, Error Handling
> Read this when: the invocation carries `--non-interactive`, or when adding any
> new decision point to this skill.

`--non-interactive` is a **total** rule, not a best-effort one: this skill has no
decision point that still prompts when it is set. Every prompt has exactly one
deterministic replacement, listed below. No prompt outside this table exists — if
a new decision point is added to the skill, it needs a row here before it may ask
anything.

## Prompt map

| Prompt (interactive behavior) | Where | With `--non-interactive` |
|---|---|---|
| "Which mode did you want?" on conflicting delivery flags | Arguments → Flag conflicts | `NEEDS_CONTEXT` naming the conflicting flags — arguments are ambiguous and the run cannot start |
| "Continue on this feature branch?" when not on a base branch | Pre-flight 2 | `BLOCKED` reporting the current branch and the detected base branch |
| "Resume? [Y/n]" on a found checkpoint | Pre-flight resume check | `NEEDS_CONTEXT` reporting the saved run's scope, task, and step |
| Stale-run scope-divergence choice `[1] resume / [2] discard` | Resume intent-match guard | `NEEDS_CONTEXT` with both the saved and the requested scope |
| "How should I handle external URLs?" | External URL Policy | Apply `deny` for this run and do **not** persist it |
| "Continue waiting?" on CI timeout | Error Handling | `DONE_WITH_CONCERNS` with the elapsed wait |
| Merge conflict during pull; PR-vs-base textual conflict; `gh` not authenticated | Error Handling | `BLOCKED` |
| Task not found; ambiguous task specifier | Error Handling | `NEEDS_CONTEXT` with the available task list |
| Dirty working tree | Pre-flight 1 / Error Handling | `BLOCKED` with the changed files |

## Rules the table encodes

1. **Deterministic outcomes are terminal.** `NEEDS_CONTEXT` and `BLOCKED` both
   mean "stop and report", never "pick a default and continue".
2. **Only one row assumes a value.** The External URL Policy row applies `deny`,
   and only because `deny` is the documented safe default that changes no state
   and is never persisted (see [external-url-policy.md](./external-url-policy.md) §3b).
3. **Nothing is auto-repaired.** No auto-commit, auto-stash, auto-clean,
   auto-delete of `.ywc-run-state.json`, and no auto-resume.
4. **Forwarding.** `--non-interactive` is forwarded to the Step 4.5
   `/ywc-impl-review` invocation. `/ywc-security-audit` has no equivalent flag
   and does not receive it — a known gap, not something to paper over here.

## Why prompts become statuses rather than defaults

Each prompt in the table guards a decision whose wrong answer is expensive and
silent: continuing on an unexpected branch bases the whole range on unrelated
work, auto-resuming a checkpoint re-runs or skips finished tasks, and picking a
delivery mode changes whether a PR exists at all. A default would hide the
mistake inside a run that reports success. A terminal status surfaces it at the
one moment it is still cheap to fix.
