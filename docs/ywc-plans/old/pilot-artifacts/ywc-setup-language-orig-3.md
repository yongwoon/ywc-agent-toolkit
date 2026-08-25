# Dispatch artifact: ywc-setup-language (original body, run 3)

**Key**: claude-code/skills/ywc-setup-language/SKILL.md:36-36
**Scenario**: I need help with the following: the user wants to set or inspect the persistent output language for ywc-generated documents, PRs, and commit messages so they stop passing --lang on every call.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The request as phrased ('set or inspect') does not specify which of the two mutually exclusive modes is wanted, nor — if it's a set/write request — which language code or full name to write, nor which scope (project CLAUDE.md vs --user ~/.claude/CLAUDE.md). The skill's Arguments table makes the Language argument required unless --show is passed, and the Rationalization Defense table explicitly forbids guessing a default or silently choosing a mode. So before performing any Read/Edit/Write against a CLAUDE.md file, I would ask the user to confirm: (1) set a new language or check the current one (--show), (2) if setting, which language, and (3) project-level or user-level (--user) target.

## Actions
- Read claude-code/skills/ywc-setup-language/SKILL.md (already done, per instructions)
- Read claude-code/skills/ywc-setup-language/references/language-resolution.md (mandatory 'Action required' directive before any write or inspect)
- Ask the user a clarifying question resolving: (a) write mode vs --show mode, (b) if write, which language code/full name, (c) if write, target scope (project CLAUDE.md vs --user for ~/.claude/CLAUDE.md)
- If write mode confirmed: normalize the supplied language to one of ko|ja|en|es|zh per the mapping in language-resolution.md; on an unmappable value, stop and report the accepted values without writing
- If write mode confirmed: Read the target CLAUDE.md (project root CLAUDE.md by default, or ~/.claude/CLAUDE.md if --user) to check for an existing '## Language Policy' section
- If write mode confirmed: Edit the file to replace the delimited '## Language Policy' section in place (heading through the line before the next '## ' heading or EOF) if present, or append the canonical section if absent, or Write a new file containing only the canonical section if the target file itself does not exist (e.g. ~/.claude/CLAUDE.md missing)
- If write mode confirmed: report a one-line confirmation naming the written file path and the resolved language code
- If --show mode confirmed instead: Read project CLAUDE.md then ~/.claude/CLAUDE.md, resolve per the precedence chain (project policy → user policy → none) from language-resolution.md, and report the resolved code and winning source rung, or 'no policy configured' plus fallback source; perform no writes

## Files touched
- claude-code/skills/ywc-setup-language/SKILL.md
- claude-code/skills/ywc-setup-language/references/language-resolution.md
- CLAUDE.md (project root, potential write target)
- ~/.claude/CLAUDE.md (potential write target if --user)

## Gates enforced
- Required-argument gate: positional Language is required unless --show is set — request as phrased supplies neither, so proceeding without clarification would mean guessing
- Normalization/validation gate: full-name or code input must map to one of ko|ja|en|es|zh before any write; unmappable input halts with accepted-values message
- Idempotent create-or-replace gate: exactly one '## Language Policy' heading must exist after a write — never append alongside an existing one (AC3)
- No-migration-of-ad-hoc-prose gate: pre-existing free-text language notes elsewhere in CLAUDE.md are left untouched, out of scope
- Missing-target-file gate: if ~/.claude/CLAUDE.md doesn't exist, create it containing only the canonical section — do not fabricate other global instructions (EC5)
- Show-mode read-only gate: --show never writes, even when no policy is found
- No-forced-global-default gate (NFR1): setup never invents an absence-covering default; consuming skills' own fallback still applies when no policy exists

## Full narrative

Having read claude-code/skills/ywc-setup-language/SKILL.md in full, here is exactly what I would do to handle this request.

First, I would announce per the skill's required opening line: "I'm using the ywc-setup-language skill to persist the output language into the appropriate CLAUDE.md."

Before writing or inspecting anything, the skill body contains a mandatory "Action required" directive telling me to read claude-code/skills/ywc-setup-language/references/language-resolution.md, since that file — not the SKILL.md body — is the single source of truth for the canonical `## Language Policy` section format, the supported code list, full-name normalization, and the precedence chain. I would read that reference file next, before touching any CLAUDE.md.

At that point I would stop and ask a clarifying question rather than proceed, because the request as given ("set or inspect") is exactly the ambiguity the skill's Arguments table is designed to reject silently guessing on. Concretely, I need the user to tell me:
1. Which action: write a new policy, or --show to inspect the currently resolved one?
2. If it's a write: which language — one of the codes `ko|ja|en|es|zh`, or an equivalent full name like "japanese" that I'd normalize per the reference file's mapping table?
3. If it's a write: which target — the project's `CLAUDE.md` at the repo root (the default), or the user-global `~/.claude/CLAUDE.md` via `--user`?

I would not default to any of these. The Rationalization Defense table explicitly calls out and rejects three temptations that are relevant here: inventing a forced global default so "absence resolves cleanly" (explicitly banned — the no-block invariant requires absence to fall through to each consuming skill's own fallback), writing a default value during `--show` just because no policy was found (banned — show is read-only), and treating an unrecognized language token as an immediate hard stop without first trying to normalize a full name to a code. None of these apply yet, though, because I don't even have a language value or a confirmed mode to evaluate.

Once the user answers, the two branches I would execute are:

**If write mode with a language supplied:**
1. Normalize the input against the mapping in language-resolution.md (e.g., "korean" → `ko`). If it doesn't map to any of `ko|ja|en|es|zh`, I stop and report the accepted values — I do not write anything.
2. Select the target file: project `CLAUDE.md` at the repo root by default, or `~/.claude/CLAUDE.md` if `--user` was requested.
3. Read the target file's current contents (Read tool) to check whether a `## Language Policy` section already exists.
   - If it exists, I Edit the file to replace that delimited section in place — from its heading through the line before the next `## ` heading, or EOF — ensuring exactly one `## Language Policy` heading remains afterward. I would not append a second heading even if there's unrelated ad-hoc language prose elsewhere in the file; that prose is explicitly out of scope and untouched.
   - If no such section exists, I append the canonical section (format taken from language-resolution.md, with the resolved code filled into `**Output language**`).
   - If the target file itself doesn't exist — the common case for `~/.claude/CLAUDE.md` — I Write a new file containing only the canonical section, nothing else (no fabricated project instructions).
4. Confirm with a single-line message naming the exact file path written and the resolved language code. No `@`-activation prompt is needed since user-global CLAUDE.md is already auto-loaded.

**If --show mode:**
1. Read the project `CLAUDE.md` and then `~/.claude/CLAUDE.md`, resolving per the precedence chain from language-resolution.md: project policy first, then user policy, then "none."
2. Report the resolved code and which rung won, or report "no policy configured" plus the fallback source if neither file has a valid section. A malformed section is reported as invalid, not silently skipped.
3. I perform no write in this mode under any circumstance.

Given the current ambiguity, though, the concrete next step is the clarifying question above — I would not guess a language, a mode, or a target scope on the user's behalf.
