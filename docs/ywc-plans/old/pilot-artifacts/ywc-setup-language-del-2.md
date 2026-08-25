# Dispatch artifact: ywc-setup-language (deleted body, run 2)

**Key**: claude-code/skills/ywc-setup-language/SKILL.md:36-36
**Scenario**: I need help with the following: the user wants to set or inspect the persistent output language for ywc-generated documents, PRs, and commit messages so they stop passing --lang on every call.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: Not a refusal — a targeted clarifying question is required before Write mode can proceed. The user's request describes wanting to 'set or inspect' the persistent language but supplies neither the required positional language code (ko/ja/en/es/zh or a full name) nor the target scope (project CLAUDE.md by default, or user-global via --user). Per the procedure, the Language argument is required unless --show is used, so I would run the no-input-needed Show mode immediately to report current state, then ask the user to confirm the desired language code and scope before performing any Edit/Write.

## Actions
- Announce skill start per the mandated line: "I'm using the ywc-setup-language skill to persist the output language into the appropriate CLAUDE.md."
- Read references/language-resolution.md (mandatory 'Action required' step) before writing or inspecting any policy, to get the canonical '## Language Policy' section format, the supported code list (ko|ja|en|es|zh), full-name normalization table, and the precedence chain
- Run Show mode first since it requires no additional input: resolve per precedence chain by reading the project CLAUDE.md at the git repo root (ywc-agent-toolkit/CLAUDE.md) for a '## Language Policy' section, then read ~/.claude/CLAUDE.md for the same section if project-level is absent or invalid
- Report the resolved code and winning source rung, or 'no policy configured' plus the fallback source, if no valid section exists at either rung; treat a malformed section as invalid (EC2) rather than ignoring it
- Ask the user a clarifying question before entering Write mode: which language code (ko/ja/en/es/zh or full name) to persist, and whether the target is the project CLAUDE.md (default) or the user-global ~/.claude/CLAUDE.md (--user flag)
- Once the language and target are confirmed, normalize the input to a code via the mapping in references/language-resolution.md (e.g., 'korean'->'ko'); stop and report accepted values without writing if it maps to none of ko|ja|en|es|zh
- Select the target file (project CLAUDE.md by default or ~/.claude/CLAUDE.md if --user)
- Check whether the target file already has a '## Language Policy' section; if yes, replace that delimited section in place (heading through the line before the next '## ' heading or EOF) so exactly one such heading remains; if absent, append the canonical section; if the target file itself does not exist (common for --user), create it containing only the canonical section, with no other fabricated global instructions
- Use Edit (for an existing file with or without an existing section) or Write (only if the target file does not exist yet) to persist the canonical section body with the resolved code filled into **Output language**
- Confirm with a one-line message naming the written file path and the code, without adding any @-activation prompt since user-global CLAUDE.md is already auto-loaded
- Apply the Rationalization Defense checks throughout: never append a duplicate heading, never treat an absent --user file as an error, always normalize full language names before writing, never write anything during --show, never introduce a forced global default when none exists
- Leave keep-in-English tokens (conventional-commit type prefix, PR-title task-id/prefix, technical terms) unaffected by the configured language per the Notes section

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-setup-language-36-36.md (read only, procedure source)
- ../references/language-resolution.md (read, mandatory before any write or inspect)
- CLAUDE.md at the project/repo root (read for --show; create-or-replace '## Language Policy' section for write mode)
- ~/.claude/CLAUDE.md (read for --show; create-or-replace '## Language Policy' section for write mode only if --user is specified)

## Gates enforced
- Action required: read references/language-resolution.md before writing or inspecting a policy
- Language positional argument required unless --show is set — triggers a clarifying question here since the user's request did not specify a language code or scope
- Normalization of full names to codes (EC3); reject inputs that map to none of ko|ja|en|es|zh
- Create-or-replace semantics on '## Language Policy' — exactly one such heading must remain (AC3, EC6); never append a duplicate
- Absent --user target file is not an error — create it containing only the canonical section (EC5), no fabricated content
- --show is strictly read-only (AC4) — never write during inspection, even if no policy is found
- No forced global default may be introduced by setup (NFR1 no-block invariant) — absence must fall through to each consuming skill's own fallback
- Malformed section reported as invalid (EC2), not silently ignored

## Full narrative

Here is how I would handle this.

First, I would announce the skill per its required opening line, then immediately read `references/language-resolution.md`, since the skill body explicitly marks this as an "Action required" step before any write or inspect action — that file is the single source of truth for the canonical `## Language Policy` section format, the supported code list (`ko|ja|en|es|zh`), full-name normalization (e.g., `korean` → `ko`), and the precedence chain (project → user → none).

Since the user's phrasing covers both "set" and "inspect" without picking one, and without supplying either a language code or a scope flag, I would not jump straight to a write. Instead I'd start with the half of the task that needs no extra input from the user: Show mode.

For Show mode, I would resolve the policy per the precedence chain: read the project `CLAUDE.md` at the repository root (the git root here is `ywc-agent-toolkit/`, so that's `CLAUDE.md` in that directory) and look for a `## Language Policy` section; if absent or invalid there, read `~/.claude/CLAUDE.md` and check the same. I would report either the resolved code and which rung won, or "no policy configured" together with the fallback source, per the procedure — and I would flag a malformed section as invalid rather than silently skipping it, per EC2.

Having surfaced the current state, I would then ask the user a clarifying question rather than guessing, because Write mode's positional Language argument is required and was not supplied: "Would you like me to persist a specific output language now — and if so, which one (ko, ja, en, es, or zh, or a full name like 'Japanese')? Should it apply to this project's CLAUDE.md, or to your user-global `~/.claude/CLAUDE.md` via `--user`?"

Once I have that answer, the write path would be:
1. Normalize the supplied value to one of `ko|ja|en|es|zh` using the reference's mapping table; if it doesn't map to any supported code, stop and report the accepted values without touching any file.
2. Select the target file — project `CLAUDE.md` by default, or `~/.claude/CLAUDE.md` if `--user` was requested.
3. Check for an existing `## Language Policy` section in that file:
   - If present, replace that delimited section in place (its heading through the line before the next `## ` heading, or EOF), so exactly one such heading survives — never append a second one.
   - If absent, append the canonical section to the existing file content, using `Edit`.
   - If the target file itself doesn't exist (a normal, non-error case especially for `--user`), create it with `Write`, containing only the canonical section — I would not fabricate any other global instructions into that file.
4. Fill the resolved code into the `**Output language**` field of the canonical section body exactly as defined in the reference doc.
5. Confirm with a single-line message stating the file path written and the code, without an `@`-activation prompt (unnecessary since `~/.claude/CLAUDE.md` auto-loads).

Throughout, I'd hold to the guardrails the skill calls out explicitly: never treat an absent `--user` target as an error, never write anything while in `--show`, never introduce a forced default that would make "absence" resolve to something other than each consuming skill's own prior fallback, and leave keep-in-English tokens (commit `type:` prefixes, PR `[task-id]` prefixes, technical terms) untouched regardless of the configured language.

So in short: I would not silently pick a language on the user's behalf. I'd show the current state first (no clarification needed for that half), then ask exactly one question — target language and scope — before making any edit.</narrative>

