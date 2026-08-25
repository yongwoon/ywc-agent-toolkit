# Dispatch artifact: ywc-setup-language (original body, run 1)

**Key**: claude-code/skills/ywc-setup-language/SKILL.md:36-36
**Scenario**: I need help with the following: the user wants to set or inspect the persistent output language for ywc-generated documents, PRs, and commit messages so they stop passing --lang on every call.
**Variant**: original
**Refused/escalated**: True
**Refusal reason**: The incoming request describes intent ("set or inspect") but does not supply the concrete arguments the skill's procedure requires before it can act: whether this is Write mode or Show mode, which language code (or full name) to persist if writing, and whether the target should be the project's CLAUDE.md (default) or the user-global ~/.claude/CLAUDE.md (--user flag). Per the skill's own Arguments table, the Language argument is required unless --show is explicitly passed, and per the Rationalization Defense table, guessing or defaulting here is exactly the kind of shortcut the skill is designed to prevent (e.g. inventing a default, or misreading intent as a request that doesn't map to a valid code). Rather than assume which of the two modes was meant, or pick a language/scope on the user's behalf, the appropriate step is to ask a short clarifying question before touching any file, since a wrong write would silently change output language behavior across every language-aware ywc-* skill going forward.

## Actions
- Announce skill invocation: "I'm using the ywc-setup-language skill to persist the output language into the appropriate CLAUDE.md."
- Read claude-code/skills/ywc-setup-language/references/language-resolution.md (mandatory per the skill's 'Action required' directive, before any write or inspect)
- Recognize the request under-specifies mode (write vs --show), language code, and target scope (project vs --user) and ask a clarifying question instead of guessing
- [If clarified as Show mode] Read project CLAUDE.md at repo root for a '## Language Policy' section
- [If clarified as Show mode] Read ~/.claude/CLAUDE.md for a '## Language Policy' section
- [If clarified as Show mode] Resolve via precedence chain (project -> user -> none) and report resolved code + winning source rung; no writes
- [If clarified as Write mode] Normalize supplied language token (e.g. 'korean'->'ko') against the ko|ja|en|es|zh list; abort without writing if unmapped
- [If clarified as Write mode] Select target file: repo-root CLAUDE.md by default, or ~/.claude/CLAUDE.md if --user given
- [If clarified as Write mode] Read the target file to check for an existing '## Language Policy' section and its boundaries
- [If clarified as Write mode, section exists] Edit the target file to replace the delimited section in place (heading through line before next '## ' heading or EOF)
- [If clarified as Write mode, section absent but file exists] Edit/append the canonical '## Language Policy' section to the target file
- [If clarified as Write mode, target file absent] Write a new file containing only the canonical section (no fabricated extra content)
- [If clarified as Write mode] Re-read the target file to verify exactly one '## Language Policy' heading remains
- [If clarified as Write mode] Confirm to the user with a one-line message naming the written file path and resolved code

## Files touched
- claude-code/skills/ywc-setup-language/SKILL.md (read)
- claude-code/skills/ywc-setup-language/references/language-resolution.md (would read)
- /Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/CLAUDE.md (would read/edit, project-level target)
- ~/.claude/CLAUDE.md (would read/write, user-level target if --user)

## Gates enforced
- Required-argument gate: Language is required unless --show is set; request supplies neither, so proceeding to write would be guessing
- Normalize-before-write gate: reject any language token that doesn't map to ko|ja|en|es|zh, do not write
- Create-or-replace idempotency gate (AC3/EC6): exactly one '## Language Policy' heading must remain after write, verified by re-read
- No-append-duplicate rule: never append a second Language Policy section when one already exists
- Out-of-scope rule: never rewrite pre-existing ad-hoc language prose elsewhere in CLAUDE.md
- EC5: on missing target file (typically --user), create it containing only the canonical section, no fabricated content
- AC4: --show is strictly read-only, never writes a default policy even when none is found
- EC2: a malformed existing section is reported as invalid, not silently ignored
- NFR1 no-block invariant: never introduce a forced global default; absence must fall through to each consumer's own fallback
- Keep-in-English exception: conventional-commit type: prefix, PR-title task-id/prefix, and technical terms stay English regardless of configured language

## Full narrative

Before taking any action, it would be advisable to clarify two points with you, as the skill's own procedure treats them as required inputs rather than assumptions I should make on your behalf.

First, upon invoking this skill I would announce: "I'm using the ywc-setup-language skill to persist the output language into the appropriate CLAUDE.md." I would then read `claude-code/skills/ywc-setup-language/references/language-resolution.md`, since the skill body explicitly marks this as an "Action required" step before any write or inspect operation — it is the single source of truth for the canonical `## Language Policy` section format, the supported code list, full-name normalization, and the precedence chain, and the skill body instructs me not to restate or approximate that content myself.

At that point, however, I would find that your request — wanting to "set or inspect" the persistent output language — does not resolve to one unambiguous action under this skill's Arguments contract. Two things are unspecified:

1. **Mode.** The skill supports a Write mode (positional language argument, default) and a Show mode (`--show` flag, read-only). Your phrasing covers both possibilities without indicating which one applies right now.
2. **If Write mode: language and scope.** The Language argument is positional and required unless `--show` is passed — no code or full name (e.g. `ko`, `ja`, `korean`, `japanese`) was supplied. Separately, the target file defaults to the project's `CLAUDE.md` at the repository root, but can instead target the user-global `~/.claude/CLAUDE.md` via `--user`; this determines whether the policy applies to this repository only or to all of your projects.

Given this, I would ask you directly: "Would you like me to report the currently effective output language (read-only), or set a new one? If setting, which language — Korean, Japanese, English, Spanish, or Chinese — and should it apply to this project only, or to all your projects via your user-global CLAUDE.md?"

Once that is confirmed, the concrete execution would proceed as follows, depending on your answer:

**If Show mode is intended:** I would read the project `CLAUDE.md` at `/Users/yongwoon.kim/Desktop/yongwoon/source/private/ywc-agent-toolkit/CLAUDE.md` looking for a `## Language Policy` section, then read `~/.claude/CLAUDE.md` for the same section. I would apply the precedence chain from the reference (project policy → user policy → none configured), and report back the resolved code and which rung it came from — or "no policy configured" plus the fallback source if neither file has a valid section. A malformed section (missing or unrecognized `**Output language**` value) would be reported as invalid rather than silently skipped. No file would be modified in this branch.

**If Write mode is intended (e.g., "set project language to Korean"):** I would first normalize the given token against the reference's mapping (`korean` → `ko`), and if it did not map to one of `ko|ja|en|es|zh`, I would stop and report the accepted values without writing anything. I would then select the target file — project `CLAUDE.md` by default, or `~/.claude/CLAUDE.md` if you asked for the user-level scope — and read it to check whether a `## Language Policy` section already exists. If it does, I would use the Edit tool to replace that delimited section in place, from its heading through the line before the next `## ` heading (or end of file), so that exactly one such heading remains afterward — never appending a second one alongside an existing section, and never touching any unrelated ad-hoc language sentence elsewhere in the file, since that is explicitly out of scope. If the section is absent but the file exists, I would append the canonical section using Edit. If the target file itself does not exist (most likely for the `--user` case), I would use Write to create it containing only the canonical `## Language Policy` section, without fabricating any other global instructions. After writing, I would re-read the file to confirm exactly one `## Language Policy` heading is present, and then confirm to you in one line which file was written and which code was set — no additional activation prompt is needed, since `~/.claude/CLAUDE.md` is already auto-loaded.

Throughout, I would not introduce a forced default language when none exists, and I would leave the "keep in English" tokens (conventional-commit `type:` prefixes, PR-title task-id prefixes, technical terms) unaffected by whatever language is configured, per the skill's closing notes. Only the tools permitted by the skill's frontmatter — Read, Edit, Write, Bash, Grep, Glob — would be used, and Bash would only be reached for a trivial existence check if needed, since Read itself reveals file absence.
