# Dispatch artifact: ywc-setup-language (original body, run 2)

**Key**: claude-code/skills/ywc-setup-language/SKILL.md:36-36
**Scenario**: I need help with the following: the user wants to set or inspect the persistent output language for ywc-generated documents, PRs, and commit messages so they stop passing --lang on every call.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The request states the general intent ('set or inspect the persistent output language') but supplies neither a language code nor an explicit --show flag nor a target scope (project vs. --user). The skill's own Arguments table marks the Language positional as required unless --show is passed, and its Rationalization Defense table explicitly rejects inferring or fabricating a default value ('I'll add a forced global default' / picking a value on the user's behalf). Per the procedure, the correct step before any Edit/Write is to ask a clarifying question resolving which mode (set vs. show), which language code, and which target file — not to guess.

## Actions
- Read claude-code/skills/ywc-setup-language/SKILL.md (already completed, per task instruction)
- Read claude-code/skills/ywc-setup-language/references/language-resolution.md (the skill's 'Action required' directive mandates reading this before any write or show, for the canonical section format, code list, and precedence chain)
- Recognize the incoming request names only the intent ("set or inspect") and gives neither a language code nor a --show flag nor a target scope — the Arguments table marks the Language positional as 'Required unless --show'
- Ask the user a clarifying question rather than guessing: (a) set a new language now, or just inspect (--show) the current one; (b) if setting, which code (ko/ja/en/es/zh or full name); (c) if setting, target the project CLAUDE.md (default) or the user-global ~/.claude/CLAUDE.md (--user)
- [Conditional, once the user answers 'set <lang>' for the project] Normalize the supplied value to one of ko|ja|en|es|zh via the mapping in language-resolution.md; if it maps to none of those, stop and report the accepted values without writing
- [Conditional] Select target file: repo-root CLAUDE.md by default, or ~/.claude/CLAUDE.md if --user was specified
- [Conditional] Read the target CLAUDE.md and grep for an existing '^## Language Policy' heading to decide replace-in-place vs append vs create-new-file
- [Conditional] Edit the target CLAUDE.md: replace the delimited section (heading through the line before the next '## ' heading or EOF) in place if found, or append the canonical section if absent, or Write a new file containing only the canonical section if the target file itself does not exist
- [Conditional] Fill the canonical section body (from language-resolution.md) with the resolved code in **Output language**
- [Conditional] Verify via grep -c '^## Language Policy' <file> that exactly one such heading remains post-edit (AC3/EC6 gate)
- [Conditional] Emit a one-line confirmation naming the written file path and the resolved code, with no @-activation prompt
- [Conditional, once the user answers '--show'] Read the project CLAUDE.md, then the user-global ~/.claude/CLAUDE.md, applying the precedence chain project → user → none; report the resolved code and winning source rung, or 'no policy configured' plus the fallback source; perform no write
- Do not fabricate a default language or forced global default under any branch, per the Rationalization Defense table

## Files touched
- claude-code/skills/ywc-setup-language/SKILL.md
- claude-code/skills/ywc-setup-language/references/language-resolution.md
- CLAUDE.md (repo root of the target project, e.g. /Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/CLAUDE.md)
- ~/.claude/CLAUDE.md (only if --user is specified)

## Gates enforced
- Required-argument gate: Language positional is required unless --show is given — ambiguous request triggers a clarifying question instead of a guess
- Reference-read gate: references/language-resolution.md must be read before any write or show action (explicit 'Action required' directive)
- EC3 normalization gate: full-name inputs (e.g. 'korean') are mapped to codes; anything outside ko|ja|en|es|zh is rejected with no write
- AC3/EC6 idempotency gate: exactly one '## Language Policy' heading must exist after a write — verified via grep -c count check, never appended alongside a pre-existing one
- EC5 file-absence gate: if the target CLAUDE.md itself does not exist, create it containing only the canonical section, no fabricated extra content
- AC4 read-only gate: --show mode never writes, even when no policy is found
- EC2 malformed-section gate: a malformed '## Language Policy' section is reported as invalid in --show, never silently ignored
- NFR1 no-block / no-forced-default invariant: absence of a policy is never resolved by inventing a global default

## Full narrative

Here is how I would proceed with this request.

The message describes the overall goal well — persisting an output language so it stops being passed as `--lang` on every call to language-aware ywc-* skills — but it does not give me the two or three concrete inputs the skill actually needs to act: (1) whether this is a **set** call or an **inspect (`--show`)** call, (2) if setting, which language code, and (3) if setting, whether the target is the project's `CLAUDE.md` (the default) or the user-global `~/.claude/CLAUDE.md` (`--user`). The skill's Arguments table marks the Language positional as "Required unless `--show`," and its Rationalization Defense table specifically warns against inventing a default in this situation ("I'll add a forced global default so absence resolves cleanly" → rejected). So before touching any file, I would ask:

"Would you like me to set a new output language now, or just show you the one currently configured? If setting, which language — Korean (ko), Japanese (ja), English (en), Spanish (es), or Chinese (zh)? And should this apply to this project's `CLAUDE.md`, or to your user-global `~/.claude/CLAUDE.md` (`--user`)?"

Before that question even goes out, I would first read `references/language-resolution.md` (the skill's SKILL.md contains an explicit "Action required" pointer to it) because it — not the skill body — is the single source of truth for the canonical `## Language Policy` section format, the supported code list with full-name normalization, and the precedence chain. I need that content regardless of which branch the user picks.

Once the user answers, the two branches look like this:

**If the user says "set it to Korean for this project":**
1. Normalize the input against the mapping in `language-resolution.md` (e.g., `korean` → `ko`); if it doesn't map to one of `ko|ja|en|es|zh`, I would stop and report the accepted values without writing anything.
2. Select the target file — the repo-root `CLAUDE.md` (here, `/Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/CLAUDE.md`, since that is the git repository root) unless `--user` was specified, in which case the target becomes `~/.claude/CLAUDE.md`.
3. Read that file and check for an existing `## Language Policy` heading (e.g., `grep -n "^## Language Policy"` on the target).
4. If the section exists, edit it in place — replacing everything from that heading through the line before the next `## ` heading (or EOF) — so exactly one `## Language Policy` heading remains afterward. If it's absent, append the canonical section. If the target file itself doesn't exist (the common case for a fresh `~/.claude/CLAUDE.md`), create it containing only the canonical section — no fabricated extra global instructions.
5. Fill the canonical section body with the resolved code in `**Output language**`.
6. Verify with a count check (`grep -c "^## Language Policy" <file>` should equal 1) to guard against accidentally leaving a duplicate heading — this is the AC3/EC6 gate.
7. Confirm with a single line naming the file path and the resolved code. No `@`-activation prompt is needed for `~/.claude/CLAUDE.md` since it's already auto-loaded.

**If the user says "just show me what's configured":**
1. Read the project `CLAUDE.md`'s `## Language Policy` section first; if absent or malformed, read the user-global `~/.claude/CLAUDE.md`'s section next — following the precedence chain project → user → none.
2. Report the resolved code and the winning rung, or explicitly state "no policy configured" together with the fallback source if neither file has a valid section. A malformed section would be reported as invalid, not silently skipped.
3. Perform no write under any circumstance in this mode.

Two things I would not do under any branch: I would not silently pick a "reasonable" default language on the user's behalf, and I would not write a policy during a `--show` inspection just because none exists — both are explicitly called out as rejected rationalizations in the skill. I would also keep the "keep-in-English" tokens (conventional-commit `type:` prefixes, PR-title `[task-id]` prefixes, technical terms) untouched by whatever language gets configured, since the skill notes those stay English by policy regardless.

So, in short: rather than proceeding on an assumption, I would first ask which action (set vs. inspect), which language, and which scope, and only then carry out the concrete read/edit/verify sequence above.
