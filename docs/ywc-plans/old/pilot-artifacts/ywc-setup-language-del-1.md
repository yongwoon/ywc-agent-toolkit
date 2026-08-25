# Dispatch artifact: ywc-setup-language (deleted body, run 1)

**Key**: claude-code/skills/ywc-setup-language/SKILL.md:36-36
**Scenario**: I need help with the following: the user wants to set or inspect the persistent output language for ywc-generated documents, PRs, and commit messages so they stop passing --lang on every call.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: The incoming request only describes intent generically ('set or inspect') without supplying the required positional Language argument, without indicating --show, and without indicating --user vs the default project target. Per the skill's own Arguments table, Language is required unless --show is passed, so proceeding would require guessing a language code or guessing between write/show mode — instead the correct step is to ask a clarifying question before taking any write action.

## Actions
- Announce skill start with the required line: "I'm using the ywc-setup-language skill to persist the output language into the appropriate CLAUDE.md."
- Read references/language-resolution.md (the file adjacent to this skill's SKILL.md) before doing anything else, since it is the single source of truth for the canonical '## Language Policy' section format, the supported code list (ko|ja|en|es|zh), full-name normalization, and the precedence chain
- Recognize the incoming request is ambiguous: it says 'set or inspect' without giving a concrete language code/name, without indicating --show, and without indicating --user vs default project target — and the skill's own Arguments table marks the positional Language argument as required unless --show is passed
- Ask a clarifying question instead of guessing: (a) do you want to SET the policy or just INSPECT (--show) the currently resolved language, (b) if setting, which language — ko/ja/en/es/zh or a full name like 'korean'/'japanese', (c) should this target the project CLAUDE.md at the repo root (default) or the user-global ~/.claude/CLAUDE.md via --user
- If the user answers with a set request (e.g. 'set to Japanese for this project'): normalize the given value to a code per the mapping table in references/language-resolution.md (e.g. 'japanese' -> 'ja'); if it does not map to one of ko|ja|en|es|zh, stop and report the accepted values without writing
- Select the target file: default to the project CLAUDE.md at repo root (/Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/CLAUDE.md in this workspace) unless --user was requested, in which case target ~/.claude/CLAUDE.md
- Read the target CLAUDE.md file with the Read tool to check whether a '## Language Policy' section already exists and, if so, capture its exact boundaries (its heading through the line before the next '## ' heading or EOF)
- If a '## Language Policy' section exists, use Edit to replace only that delimited span in place with the canonical section body (from references/language-resolution.md) with the resolved code filled into **Output language** — never append a second heading
- If no such section exists but the file exists, use Edit to append the canonical section to the end of the existing file, leaving all other content (e.g. the user's existing ~/.claude/CLAUDE.md content, or this repo's existing CLAUDE.md content) untouched
- If the target file itself does not exist (typical for a first --user write), use Write to create it containing only the canonical '## Language Policy' section — no fabricated additional global instructions
- After writing, re-read the file (or grep-count occurrences of the '## Language Policy' heading) to verify exactly one such heading remains, satisfying AC3/EC6
- Emit a one-line confirmation naming the written file path and the resolved code, with no additional @-activation prompt since ~/.claude/CLAUDE.md is already auto-loaded
- If instead the user asks to inspect (--show): read the project CLAUDE.md's '## Language Policy' section first, then fall back to reading ~/.claude/CLAUDE.md's section if the project section is absent or invalid, per the precedence chain (project -> user -> none)
- In --show mode, report the resolved code and the winning source rung, or explicitly report 'no policy configured' plus the fallback source if neither file has a valid section — and perform no writes at all, even if no policy is found
- Throughout, keep in mind that keep-in-English tokens (conventional-commit type: prefix, PR-title [task-id]/prefix, technical terms) are unaffected by the configured language and must not be altered by this skill

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-setup-language-36-36.md (read only, per task instructions)
- references/language-resolution.md (would read, path relative to the skill's own directory, not yet resolved)
- /Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/CLAUDE.md (would read and potentially edit as the default project target)
- /Users/yongwoon.kim/.claude/CLAUDE.md (would read and potentially edit only if --user is explicitly requested)

## Gates enforced
- Required-argument gate: Language positional argument is mandatory unless --show is given, so a genuinely ambiguous request must not be silently defaulted
- Normalization/validation gate: only ko|ja|en|es|zh accepted after normalizing full names; anything else halts before any write and reports accepted values
- Single-section invariant (AC3/EC6): exactly one '## Language Policy' heading must exist after a write — replace-in-place, never append a duplicate
- Missing-file handling (EC5): an absent --user target file is not an error; create it containing only the canonical section, no fabricated content
- Read-only gate for --show (AC4): --show never writes, even when no policy is found or the found section is malformed (EC2 reported as invalid, not silently ignored)
- No-global-default invariant (NFR1): setup never introduces a forced global default to make absence resolve cleanly; absence must fall through to each consuming skill's own fallback
- Reference-first gate: references/language-resolution.md must be read before writing or inspecting any policy, since it owns the canonical section format and precedence chain

## Full narrative

Here is how I would work through this.

First, per the skill's required announcement, I would state: "I'm using the ywc-setup-language skill to persist the output language into the appropriate CLAUDE.md."

Before writing or inspecting anything, I would read `references/language-resolution.md` (the file located alongside this skill's SKILL.md), since the procedure explicitly requires that as the single source of truth for the canonical `## Language Policy` section format, the supported code list, full-name normalization, and the precedence chain — and forbids restating that content here.

At that point I would stop and ask a clarifying question rather than proceeding, because the request as given is ambiguous against this skill's own Arguments table:
- The positional Language argument (a code like `ko`/`ja`/`en`/`es`/`zh` or a full name like `korean`) is required unless `--show` is passed — and the request doesn't specify either a language or that this is a `--show` inspection.
- The target is also unspecified — default is the project `CLAUDE.md` at the repo root, but `--user` would redirect to `~/.claude/CLAUDE.md`.

So I would ask: "Would you like to set the persistent language, or just inspect what's currently configured (`--show`)? If setting, which language — `ko`/`ja`/`en`/`es`/`zh` or a full name? And should this apply to this project's `CLAUDE.md`, or your user-global `~/.claude/CLAUDE.md` via `--user`?"

Once that's answered, the concrete path splits two ways:

**If setting a language** (e.g., "set Japanese for this project"):
1. Normalize the given value against the mapping table in `references/language-resolution.md` (e.g., `japanese` → `ja`). If it maps to none of `ko|ja|en|es|zh`, I would stop and report the accepted values without writing anything.
2. Select the target file — by default the project `CLAUDE.md` at `/Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/CLAUDE.md` in this workspace, or `~/.claude/CLAUDE.md` if `--user` was requested.
3. Read that target file to check whether a `## Language Policy` section already exists and, if so, note its exact span (its heading through the line before the next `## ` heading, or EOF).
4. If the section exists, use Edit to replace only that delimited span in place with the canonical section body, filling the resolved code into `**Output language**` — never appending a second heading (this guards against the "just append a new section" rationalization the skill explicitly calls out as a violation).
5. If the section is absent but the file exists, append the canonical section via Edit, leaving the rest of the file (e.g., the substantial existing content already in this user's `~/.claude/CLAUDE.md`, or this repo's `CLAUDE.md`) completely untouched.
6. If the target file itself doesn't exist (the common case for a first `--user` write), use Write to create it containing only the canonical section — no fabricated additional global instructions.
7. After writing, re-read the file (or count occurrences of the `## Language Policy` heading) to verify exactly one such heading remains.
8. Confirm with a single-line message naming the written file path and the resolved code, with no extra activation prompt.

**If inspecting (`--show`)**:
1. Read the project `CLAUDE.md`'s `## Language Policy` section first.
2. If absent or malformed, fall back to reading `~/.claude/CLAUDE.md`'s section.
3. Report the resolved code and the winning source rung, or explicitly "no policy configured" plus the fallback source if neither file has a valid section — treating a malformed section as invalid rather than silently skipping it.
4. Perform no writes at all in this mode, even if no policy is found — I would not write a default just to make future calls resolve cleanly.

Throughout, I would keep in mind that conventional-commit `type:` prefixes, PR-title `[task-id]`/prefixes, and technical terms stay in English regardless of the configured language, since the skill notes those tokens are unaffected by this policy.

Given the actual request as phrased, though, the first and only action I would take right now is to ask the clarifying question above rather than pick a language or mode on the user's behalf.
