# Dispatch artifact: ywc-setup-language (deleted body, run 3)

**Key**: claude-code/skills/ywc-setup-language/SKILL.md:36-36
**Scenario**: I need help with the following: the user wants to set or inspect the persistent output language for ywc-generated documents, PRs, and commit messages so they stop passing --lang on every call.
**Variant**: deleted
**Refused/escalated**: True
**Refusal reason**: The user's request describes the general intent ('set or inspect the persistent output language ... so they stop passing --lang on every call') but supplies neither a concrete language code/name nor a --show flag, and does not specify --user vs. the default project scope. Per the skill's Arguments table, the Language argument is required unless --show is given, and the Rationalization Defense explicitly forbids guessing a default or writing during an ambiguous/show-like request. Rather than assume a language, assume show mode, or assume project vs. user scope, I would ask a clarifying question before performing any Read/Edit/Write action against a CLAUDE.md file.

## Actions
- Read the skill's mandatory reference doc at <skill-dir>/references/language-resolution.md before doing anything else, since the procedure explicitly requires this ('Action required: Read ../references/language-resolution.md before writing or inspecting a policy') to get the canonical ## Language Policy section format, the supported code list (ko|ja|en|es|zh), full-name normalization rules, and the precedence chain
- Announce skill use verbatim per the skill's required announce line: 'I'm using the ywc-setup-language skill to persist the output language into the appropriate CLAUDE.md.'
- Parse the user's request against the Arguments table: Language is a positional argument required unless --show is passed; the request as given supplies neither a language code/name, nor --show, nor --user
- Because the required argument is missing and it is ambiguous whether the user wants write mode or --show (inspect) mode, stop before performing any Read/Edit/Write/Bash/Grep/Glob action and ask a clarifying question rather than guessing a default language or mode
- Clarifying question to send the user: (1) Do you want me to SET the persistent output language, or just SHOW/inspect what is currently configured? (2) If setting, which language — ko, ja, en, es, or zh (or the full name, e.g. 'korean', 'japanese')? (3) Should this target the project-level CLAUDE.md (default, repo root) or your user-global ~/.claude/CLAUDE.md (pass --user)?
- If the user answers with --show: Read the project CLAUDE.md and Read ~/.claude/CLAUDE.md, Grep each for a '## Language Policy' heading, resolve per precedence (project policy > user policy > none) per language-resolution.md, report the resolved code and winning source rung, flag a malformed section as invalid rather than ignoring it, and perform no writes
- If the user answers with a language code/name and target: normalize the input to one of ko|ja|en|es|zh using the mapping in language-resolution.md (stop and report accepted values without writing if it maps to none of them); Read the target CLAUDE.md (project root by default, or ~/.claude/CLAUDE.md if --user) to check for an existing '## Language Policy' section
- If a '## Language Policy' section already exists in the target file: Edit that file to replace the delimited section in place (from the heading through the line before the next '## ' heading or EOF) with the canonical section body from language-resolution.md, filling in the resolved code — never append a second heading
- If no '## Language Policy' section exists but the file exists: Edit the file to append the canonical section at the end
- If the target file itself does not exist (expected case for a fresh ~/.claude/CLAUDE.md with --user): Write a new file containing only the canonical '## Language Policy' section — do not fabricate any other global instructions
- After the write, re-Read the target file and Grep-count occurrences of '## Language Policy' to confirm exactly one heading remains (AC3/EC6 invariant)
- Emit a one-line confirmation naming the written file path and the resolved language code, with no @-activation prompt since ~/.claude/CLAUDE.md is auto-loaded
- Explicitly do not introduce a forced global default language on my own initiative, and do not write anything during a --show request (read-only invariant)

## Files touched
- docs/ywc-plans/pilot-artifacts/variant-ywc-setup-language-36-36.md (read only, per task instructions)
- <skill-dir>/references/language-resolution.md (would read, path not directly given, inferred from the skill's relative reference)
- CLAUDE.md at the project repo root (candidate write/read target for project-scope policy, pending clarification of which repo root)
- ~/.claude/CLAUDE.md (candidate write/read target for --user scope policy)

## Gates enforced
- Required-argument gate: Language is required unless --show — proceeding without either is not allowed, so I ask a clarifying question instead of guessing
- Exactly-one-heading invariant (AC3/EC6): after any write, the target file must contain exactly one '## Language Policy' heading — never append a duplicate
- No-fabrication gate (EC5): when creating a missing ~/.claude/CLAUDE.md for --user, write only the canonical section, no invented global instructions
- Normalization gate (EC3): full language names must be mapped to a code before validating; inputs mapping to none of ko|ja|en|es|zh are rejected without writing
- Read-only gate for --show (AC4): show mode never writes, and a malformed policy section is reported as invalid rather than silently ignored (EC2)
- No-forced-default gate (NFR1): setup must never introduce a global default on its own — absence must fall through to each consuming skill's own fallback
- Mandatory-reference-read gate: language-resolution.md must be read before any write or inspect action, since it is the single source of truth for the section format, code list, and precedence chain

## Full narrative

Here is how I would proceed under the ywc-setup-language procedure for this request.

First, before touching any file, the skill mandates reading its reference doc, so I would Read `<skill-dir>/references/language-resolution.md` to pick up the canonical `## Language Policy` section format, the supported code list (`ko|ja|en|es|zh`), the full-name-to-code normalization table, and the precedence chain (project → user → none). I would also emit the skill's required announce line: "I'm using the ywc-setup-language skill to persist the output language into the appropriate CLAUDE.md."

Next I would check the request against the Arguments contract: Language is a positional argument, required unless `--show` is passed. The message as given says the user "wants to set or inspect" the language but does not actually supply a language code/name, does not pass `--show`, and does not indicate `--user` vs. the default project-level target. That leaves three open questions I cannot safely resolve on my own: (a) set or show, (b) which language code if setting, (c) project CLAUDE.md or `~/.claude/CLAUDE.md`. The Rationalization Defense table is explicit that I must not paper over these gaps — I must not fabricate a default language, must not assume show mode just because no language was given, and must not silently pick a scope.

So instead of running any Read/Edit/Write/Grep against a CLAUDE.md file, I would ask a clarifying question along these lines: "Would you like me to set a specific output language, or show what's currently configured? If setting, which language — ko, ja, en, es, or zh (or a full name like 'korean')? And should this apply to the project's CLAUDE.md, or your user-global `~/.claude/CLAUDE.md` via `--user`?"

Once that's answered, the concrete path forks:

If the answer is `--show`: I would Read the project CLAUDE.md and Read `~/.claude/CLAUDE.md`, Grep each for a `## Language Policy` heading, apply the precedence chain from language-resolution.md, and report the resolved code plus the winning source rung (or "no policy configured" with the fallback source if neither has a valid section). A malformed section would be reported as invalid rather than ignored. No writes occur in this branch.

If the answer is a set request with a code/name and scope: I would normalize the input via the language-resolution.md mapping (stopping and reporting the accepted values without writing if it doesn't map to `ko|ja|en|es|zh`), select the target file (project CLAUDE.md at repo root by default, or `~/.claude/CLAUDE.md` if `--user`), and Read that file to check for an existing `## Language Policy` section. If one exists, I would Edit the file to replace that delimited section in place (heading through the line before the next `## ` heading, or EOF) with the canonical body carrying the resolved code — never appending a second heading. If the section is absent but the file exists, I would Edit to append the canonical section. If the file itself doesn't exist (the common `--user` case), I would Write a new file containing only the canonical section, with no fabricated additional content. After writing, I would re-Read the file and confirm via a heading count that exactly one `## Language Policy` section remains, then emit a one-line confirmation naming the file path and the resolved code, with no `@`-activation prompt since `~/.claude/CLAUDE.md` is already auto-loaded.

Throughout, I would enforce the invariants baked into the procedure: never introduce a forced global default on my own initiative (absence should still fall through to each consuming skill's own fallback), never fabricate unrelated global instructions when creating a fresh `~/.claude/CLAUDE.md`, and treat `--show` as strictly read-only. Given the ambiguity in the initial request, though, the first concrete action is the clarifying question above rather than any file operation.
