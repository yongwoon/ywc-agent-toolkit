# Dispatch artifact: ywc-commit (original body, run 3)

**Key**: claude-code/skills/ywc-commit/SKILL.md:26-26
**Scenario**: 지금 작업한 내용을 커밋해줘
**Variant**: original
**Refused/escalated**: False


## Actions
- Announce: "I'm using the ywc-commit skill to stage and commit the current work."
- Step 0: inspect $ARGUMENTS for --skip-ubiquitous-update (none present in a direct user request) -> proceed to Step 0.5
- Step 0.5: run `test -f docs/ubiquitous-language.md`; if it exists, invoke `ywc-ubiquitous-language --mode update` and let any resulting diff to docs/ubiquitous-language.md flow into Step 2 as IN; if absent, skip silently without prompting the user
- Step 1: run `git status --short`, `git diff --stat`, `git log --oneline -15`, `git branch --show-current` to assess current state and learn commit-message conventions
- Check current branch name against main/master (Rule 5) - if on main/master, stop and ask for explicit confirmation before any commit; otherwise continue
- Step 2: classify every file shown in git status into IN (created/modified/discussed this session), UNKNOWN (unclear origin), or OUT (clearly unrelated) - cross-referencing against what was actually touched in this conversation
- Exclude secrets/build artifacts per Rule 7 (.env*, *.log, dist/, build/, node_modules/, .DS_Store, large binaries) and report any found rather than staging them
- If any file is UNKNOWN or OUT, present the classification table to the user and get explicit approval before staging anything (blocking step, not skippable)
- Step 3: group IN files into logically distinct commits (e.g., refactor separate from feat); use `git add -p <path>` for hunk-level splitting when one file mixes unrelated changes; show the user the planned commit(s) with draft messages and get approval unless it's a trivial 1-2 file single-purpose change
- Step 4: read `git log --oneline -30` to match the repo's exact type(scope): summary style; resolve commit-message language via the language-resolution reference chain (--lang flag -> project CLAUDE.md Language Policy -> user CLAUDE.md Language Policy -> existing fallback of matching recent commit style); keep type/scope/whitelisted technical terms in English regardless; do not add a co-author trailer unless the repo's recent commits already use one or the user explicitly asked
- Step 5: stage only by explicit path with `git add <path1> <path2> ...` (never `git add .` or `git add -A`); verify with `git diff --cached --stat`; commit via `git commit -m "$(cat <<'EOF' ... EOF)"` heredoc, one commit per logical unit, running `git status` after each to confirm remaining state - never pass --no-verify even if a pre-commit hook fails (fix root cause or report it)
- Step 6: run `git log --oneline -<N>` and `git status` to verify the commit(s) landed as expected and the working tree matches intent
- Step 7 (push): check the user's message '지금 작업한 내용을 커밋해줘' for push-intent words (푸쉬/올려줘/push) - none present, so skip `git push` entirely per Rule 3 (commit only, no push)
- Report result in the fixed format: '✅ N commit(s) created' with hash/type(scope)/summary per commit, plus an 'Excluded files' line only if Step 2 excluded anything

## Files touched
- claude-code/skills/ywc-commit/SKILL.md (read only, per task constraint)

## Gates enforced
- Rule 1: only stage files verifiably touched/discussed this session (IN/UNKNOWN/OUT classification, ask before staging UNKNOWN or OUT)
- Rule 2: split logically distinct changes into separate commits
- Rule 3: never push without explicit push-intent wording in the user's message - this request has none, so no push
- Rule 4: never use --no-verify on hook failure; fix root cause or report it
- Rule 5: confirm before committing directly to main/master
- Rule 6: never git add . or git add -A; always explicit paths
- Rule 7: exclude secrets/build artifacts (.env*, *.log, dist/, build/, node_modules/, .DS_Store) unless user explicitly added them
- Rule 8: no fabricated AI co-author trailer unless repo convention or explicit user request
- Step 0.5 UL-glossary sync gate (test -f docs/ubiquitous-language.md before commit)
- Step 2 blocking approval gate for UNKNOWN/OUT files before any staging

## Full narrative

Per the ywc-commit SKILL.md procedure, the phrase "지금 작업한 내용을 커밋해줘" is a direct-invocation trigger for this skill (matches "커밋 해줘" / "지금까지 한 작업 커밋" in the description) with no push-intent wording and no flags, so I would proceed as follows.

First, I would announce: "I'm using the ywc-commit skill to stage and commit the current work."

Step 0 (parse arguments): $ARGUMENTS is empty in a direct user request, so no --skip-ubiquitous-update flag is present, and Step 0.5 runs normally.

Step 0.5 (Ubiquitous Language check): I would run `test -f docs/ubiquitous-language.md`. If the file exists, I would invoke `ywc-ubiquitous-language --mode update` and let any resulting glossary changes flow into the file classification in Step 2. If it doesn't exist, I would skip silently without prompting the user to create one.

Step 1 (assess state): I would run `git status --short`, `git diff --stat`, `git log --oneline -15`, and `git branch --show-current`. I would check whether the current branch is main/master — per Rule 5, if so I would stop and ask for explicit confirmation before committing anything directly to it. I would also read the last 15-30 commit messages to learn the exact `type(scope): summary` conventions this repository already uses (this repo's recent log shows patterns like `chore: mark 000057-010-test-pilot-sample-frame as completed` and `feat(skill-author): add decidable 8-step Deletion Test procedure (000056-010)`, so I would match that style rather than inventing a new one).

Step 2 (classify changed files): I would sort every file surfaced by `git status` into IN (demonstrably created/modified/discussed in this session), UNKNOWN (unclear origin), or OUT (clearly unrelated — other features, IDE files, local config). I would also screen for secrets/build artifacts per Rule 7 (`.env*`, `*.log`, `dist/`, `build/`, `node_modules/`, `.DS_Store`, large binaries) and exclude those, reporting them rather than staging silently. If anything lands in UNKNOWN or OUT, I would stop and show the user the classification table, asking for explicit approval before staging — this is a non-skippable gate per the skill.

Step 3 (split into logical commits): I would group the IN files by logical purpose (e.g., a refactor and a new feature would become two separate commits, ordered refactor-then-feat; a bug fix plus its own tests would stay as one commit). Where a single file mixes unrelated hunks, I would use `git add -p <path>` for hunk-level staging. I would show the user the planned commit sequence (files + draft message per commit) and get approval, unless the whole change is only 1-2 files with an obviously single purpose.

Step 4 (write commit messages): I would follow the `<type>(<scope>): <summary>` format, deriving `type` and `scope` from the repository's own observed conventions (this repo uses `feat`, `fix`, `refactor`, `docs`, `i18n`, `ci`, `chore` per its CLAUDE.md, and for skill files uses the skill name as scope, e.g. `(ywc-commit)`). I would resolve the message language via the referenced language-resolution chain (`--lang` flag → project CLAUDE.md Language Policy → user CLAUDE.md Language Policy → fallback to matching recent commit style) while always keeping the `type:` prefix, `(scope)` token, and technical terms in English. I would not add any AI co-author trailer by default — this repo's own git-workflow rule notes attribution is disabled globally, and recent commits shown don't carry a trailer, so none would be added unless the user explicitly asked.

Step 5 (stage and commit): I would stage strictly by explicit path — `git add <path1> <path2> ...` or `git add -p <path>` — never `git add .` or `git add -A`. I would verify with `git diff --cached --stat` before committing, then commit using a heredoc (`git commit -m "$(cat <<'EOF' ... EOF)"`) to safely handle multi-line messages, repeating per logical commit and running `git status` after each to confirm the remaining tree matches expectations. If any pre-commit/pre-push hook failed, I would never bypass it with `--no-verify` — I would diagnose and fix the root cause, or report the failure to the user if I can't resolve it myself.

Step 6 (verify): I would run `git log --oneline -<N>` (N = commits just created) and `git status` to confirm the commits landed correctly and nothing unexpected remains, reporting immediately if anything is off.

Step 7 (push): The user's request "지금 작업한 내용을 커밋해줘" contains no push-intent language (no "push", "푸쉬", "올려줘"), so per Rule 3 I would not run `git push` at all — this stays a commit-only operation.

Finally, I would report in the skill's fixed format: "✅ N commit(s) created" followed by one line per commit (hash, type(scope): summary), plus an "Excluded files" line only if Step 2 excluded anything.

I would not refuse or escalate this request in the abstract — it's a standard, well-scoped commit request. The one place I would legitimately pause and ask the user rather than proceed unilaterally is Step 2, if the actual `git status` output contains files I cannot confidently attribute to this session's work (UNKNOWN) or that look unrelated (OUT); in that case I would show the classification table and wait for explicit approval before staging anything, per the skill's non-negotiable rule. Likewise, if the branch turned out to be main/master, I would pause for confirmation before committing at all. Absent either of those conditions, I would carry the workflow through to a completed, unpushed commit and the final report line.
