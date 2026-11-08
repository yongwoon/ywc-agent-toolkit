# P2-a: Enforce Prose-Only Guards with Claude Code Hooks

> Scale: Medium
> Parent: issue #215 (P2-a), `docs/ywc-plans/20261107-p1-hardening-before-main-pr.md:33`
> Status: first slice (G1, G2, G4, G7 secret paths) implemented for #222; G7 confinement implemented as `retro-lens-scope` in `claude-code/hooks/protect-secrets.py`; see `claude-code/hooks/test_hooks.py`. The G2 deny-vs-ask Open Question remains.

## Purpose

Several `ywc-*` safety rules exist only as SKILL.md prose. A model can skip prose; a PreToolUse hook that returns `permissionDecision: "deny"` cannot be skipped. This plan decides which guards are worth a hook, what each costs in false positives, and which slice to build first.

## Scope

- A candidate-guard inventory with source `file:line`, hook event and matcher, false-positive cost, and a verdict (hook / ask / keep prose).
- The Codex position for each guard.
- A recommended first slice for the implementation PR.

## Out of Scope

- Implementing, installing, or changing any hook in this PR.
- Codex enforcement. Codex has no equivalent hook surface; every guard stays prose there.
- Changing existing guard prose in any SKILL.md.
- Changing the user's own external hooks (for example `npx block-no-verify`), which this repository does not ship.

## Global Constraints

- "Skill names follow `ywc-<kebab-case>` for all distributed skills." (`CLAUDE.md`)
- Hooks ship from `claude-code/hooks/` and are listed in `claude-code/hooks/hooks-registry.json`; `scripts/install.sh --hooks [--global|--local] [hook-name...]` installs them (`scripts/install.sh:15`, `:520`).
- `bash scripts/validate.sh` mirrors CI and must pass.

## Existing Constraints Touched

| Existing artifact | Behavior (verified by reading the file) | Interaction |
|---|---|---|
| `claude-code/hooks/block-dangerous-commands.py:25` | `SAFETY_LEVEL = "high"`; patterns at `:36-64` | New Bash patterns extend this file instead of adding a new hook |
| `claude-code/hooks/block-dangerous-commands.py:49` | `git-force-main` (high) blocks force push to main/master unless `--force-with-lease` is present | Already enforces the force-push guard at the default level |
| `claude-code/hooks/block-dangerous-commands.py:60` | `git-force-any` (strict) blocks any force push without `--force-with-lease` | Off at the default level; `--force-with-lease` stays allowed, which the `ywc-sequential-executor --worktree` claim push needs (`claude-code/skills/ywc-sequential-executor/references/worktree-run.md`) |
| `claude-code/hooks/block-dangerous-commands.py:115-116` | Any exception prints `{}` (allow) | Fail-open: a hook bug never blocks work, but a parser crash also silently disables the guard |
| `claude-code/hooks/block-dangerous-commands.py:82-88` | Regex search over the whole command string | No tokenization, so a flag in one segment of a compound command can match a rule meant for another segment |
| `claude-code/hooks/protect-secrets.py:48-57`, `:149-154`, `:163-165` | Registered for `Read|Edit|Write|Bash`; `check` inspects `file_path` for Read/Edit/Write and the command for Bash, and every other tool returns `{}` (allow). Critical patterns block `.env*`, `~/.ssh/id_*`, `authorized_keys`, `.aws/credentials`, `*.pem`, `*.key` | Covers only `Read` of known secret paths for `ywc-retro-lens`; its `Grep` and `Glob` calls pass unchecked (see G7) |
| `scripts/install.sh:467-501` | `merge_hook_settings` adds a command to an event/matcher entry and skips duplicates | New patterns in existing hook files need no install change |
| `tests/`, `scripts/` | No test covers any file under `claude-code/hooks/` | The implementation PR must add the first hook test |
| `claude-code/skills/ywc-merge-dependabot/SKILL.md:57`, `:272` | Legitimately runs `gh pr merge --auto --merge --match-head-commit` | A blanket `--auto` deny would break this skill |
| `claude-code/skills/ywc-parallel-executor/SKILL.md:123`, `references/checkpoint-resume.md:30` | Legitimately runs `git branch -D feature/<task>` after a merged task | A blanket `branch -D` deny would break this skill |

## Candidate Guards

| ID | Guard | Prose source | Event / matcher | False-positive cost | Verdict | Codex |
|---|---|---|---|---|---|---|
| G1 | No `--no-verify` / `-n` on `git commit`, no `--no-verify` on `git push` | `claude-code/skills/ywc-commit/SKILL.md:51`, `:259` | PreToolUse / `Bash` | **High if regex-based.** An external `block-no-verify` hook blocked six legitimate commands in the issue #215 session because `grep -n`, `sed -n`, `[ -n "$x" ]`, or a quoted example inside a heredoc shared a command line with `git commit` or `git push`. **Low if tokenized**: split on `;`, `&&`, `||`, `|`, newline with `shlex`, ignore heredoc bodies, then match `-n` (alone or in a short-flag cluster such as `-nm`) only in a `git commit` segment, and `--no-verify` in a `git commit` or `git push` segment. On `git push`, `-n` means `--dry-run` and must stay allowed | Hook (deny), tokenized | Prose |
| G2 | No `git add -A` / `git add .` / `git add --all` | `ywc-commit/SKILL.md:53`, `ywc-sequential-executor/SKILL.md:316` | PreToolUse / `Bash` | **Medium.** The hook is session-wide, so it also catches a user who deliberately stages everything outside a skill | Hook (`ask`, not deny) | Prose |
| G3 | No force push | `ywc-create-pr/SKILL.md:192` | already `git-force-main` / `git-force-any` | None new | Keep the existing patterns; document that `strict` is needed for non-trunk branches | Prose |
| G4 | No `gh pr merge --admin` | `ywc-agentic` Finish Phase rule (installed bundle copy, not present in this repo's `claude-code/skills/ywc-agentic/SKILL.md`) | PreToolUse / `Bash` | **Low.** No skill in this repo runs `--admin` (`grep -rn -e '--admin' claude-code/skills` → no SKILL.md hit) | Hook (deny), tokenized | Prose |
| G5 | No `gh pr merge --auto` outside `ywc-merge-dependabot` | same as G4 | — | **High.** `ywc-merge-dependabot` needs it (see Existing Constraints) and a hook cannot tell which skill is running | Keep prose | Prose |
| G6 | No `git branch -D` to bypass the merge check | `claude-code/skills/ywc-worktrees/scripts/cleanup-worktree.sh:203` (message) | — | **High.** `ywc-parallel-executor` uses `-D` legitimately | Keep prose | Prose |
| G7 | `ywc-retro-lens` reads only the transcript and lens files | `claude-code/agents/ywc-retro-lens.md` Boundaries and "Accepted residual risk" | PreToolUse / `Read|Grep|Glob` | **Low** for a secret-path deny: extend `protect-secrets.py` so `Grep` and `Glob` check their `path` (and `Glob` its `pattern`) against the same secret patterns. Confinement uses the documented `agent_type` hook input field (Open Questions, resolved) and limits the agent to the `ywc-retro.*` run directory (ywc-retro copies the transcript there, so `~/.claude/projects` with every project's transcripts stays out of scope) and repository Owner locations; it touches no other agent | Hook (deny) for secret paths in `Grep`/`Glob`; hook (deny, fail closed) for confinement | N/A (no Codex retro-lens agent) |

## Recommended First Slice

One implementation PR, extending `block-dangerous-commands.py` and `protect-secrets.py`:

1. Add a tokenizer helper (`shlex` with a regex fallback; on a tokenize error, fall back to the current whole-string regex rather than allowing) that yields `(argv, segment_text)` per command segment.
2. Add G1 (deny) and G4 (deny) as segment-scoped rules at level `high`.
3. Add G2 as an `ask` decision at level `high`.
4. Extend `protect-secrets.py` to inspect `Grep`/`Glob` (G7): add both tools to its registry matcher and check their `path` (and `Glob` `pattern`) with the existing file patterns.
5. Add `scripts/test-hooks.sh` (or a `test_*.py` beside the hook) that feeds JSON on stdin and asserts the decision, and wire it into `scripts/validate.sh`.

G3, G5, and G6 need no code in this slice.

## Acceptance Criteria

- AC1: When this PR merges, `test -f docs/ywc-plans/20261107-p2a-hook-enforcement.md` exits 0. Baseline: 1 — file absent before this PR.
- AC2: Every row in Candidate Guards names a prose source (`file:line`, or an explicit "not present in this repo"), an event/matcher or `—`, a false-positive cost, a verdict, and a Codex position.
- AC3: The PR that adds this file links it from its body under "P2-a" so issue #215 can be updated when it merges.

The following ACs belong to the later implementation PR and are recorded so it can copy them:

- AC4: Given a PreToolUse Bash payload `git add foo && git commit -m x && grep -n y z`, the hook returns no deny. Given `git commit -n -m x`, `git commit -nm x`, or `git push --no-verify`, it returns deny with id `git-no-verify`. Given `git push -n origin x` (dry run), it returns no deny.
- AC5: Given `gh pr merge 12 --admin --merge`, the hook denies; given `gh pr merge 12 --auto --merge --match-head-commit abc`, it allows.
- AC6: Given `git add -A` or `git add .`, the hook returns `permissionDecision: "ask"`; given `git add src/a.ts`, it returns `{}`.
- AC6b: Given a `Grep` payload with `path` `~/.ssh` or a `Glob` payload with `pattern` `**/.env`, `protect-secrets.py` denies; given a `Grep` over `src/`, it allows.
- AC7: `bash scripts/validate.sh` runs the hook test and passes.

## Functional Requirements

- FR-0 (AC1, AC3): The plan lives at the dated path and the PR body links it under "P2-a".
- FR-1 (AC2): Each candidate guard is classified as hook-deny, hook-ask, or keep-prose, with the reason.
- FR-2 (AC4–AC6b, later PR): Bash guards match per command segment, not over the whole command string.
- FR-3 (AC7, later PR): The hook gets a stdin-driven test that `validate.sh` runs.

## Non-Functional Requirements

- A hook stays fail-open on an internal exception (current behavior), but a tokenize error falls back to the whole-string regex instead of allowing silently.
- Hook latency stays within one `uv run` start; no network access.

## Edge Cases

- A combined short-flag cluster (`git commit -anm x`) contains `n` and must deny; `git push -nu origin x` is a dry run and must not.
- A heredoc or quoted string that mentions a forbidden flag (a commit message, a Python script body) must not deny.
- A quoted message containing `--no-verify` (`git commit -m "drop --no-verify"`) must not deny; tokenization makes it one argv element.
- Heredoc commit messages (`git commit -F - <<'EOF'`) carry free text after the segment; only argv before the heredoc counts.
- `git -C <path> commit -n` must still match: skip `git` global options before the subcommand.

## Failure Modes

| Path | Failure | Handling | Test |
|---|---|---|---|
| Tokenizer | Unbalanced quotes raise `ValueError` | Fall back to whole-string regex | Edge-case test in AC4 suite |
| Hook process | `uv` missing or crash | Fail-open (existing); the skill prose still states the rule | Not testable in CI; documented |
| `ask` decision (G2) | Non-interactive runs cannot answer | The run stops at the prompt; documented as intended | Manual |

## Open Questions

- ~~Does the Claude Code PreToolUse input identify the subagent?~~ Resolved: yes. The hooks reference (https://code.claude.com/docs/en/hooks, "Common input fields") documents `agent_id` and `agent_type`, present when the hook fires inside a subagent. `protect-secrets.py` uses `agent_type` for the G7 confinement (`retro-lens-scope`).
- Should G2 be `deny` once skills are the main users of these hooks? Default: `ask`, revisit after a release.
