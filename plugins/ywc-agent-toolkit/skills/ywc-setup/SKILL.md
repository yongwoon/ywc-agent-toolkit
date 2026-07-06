---
name: ywc-setup
description: (ywc) Use when configuring the default output language for Codex ywc skills. Triggers: "ywc-setup", "setup ywc language", "ywc 언어 설정", "project language default", "user language default". Do not use for Claude Code setup, session language defaults, or generating project documentation.
---

# ywc-setup

Announce: "Using `ywc-setup` to configure the Codex YWC output-language default."

This skill writes the minimal language config used by Codex `ywc-*` skills. It
is Codex-only. The canonical language resolution policy is
[`../references/language-resolution.md`](../references/language-resolution.md).

## Anti-Triggers

Do not use this skill for:

- Claude Code skill setup or Claude-only configuration.
- Session language defaults. Session defaults are intentionally unsupported.
- Creating project documentation; use `ywc-project-docs` for that.
- Translating existing files.

## Inputs

Supported scopes:

- `--scope project` - write `.codex/ywc.json` in the current repository.
- `--scope user` - write `~/.codex/ywc.json`.

Supported canonical language codes:

- `ko`
- `ja`
- `en`
- `zh`
- `es`

Accept these aliases in user input and normalize before writing:

| Alias | Write as |
| --- | --- |
| `ko`, `kr`, `korean`, `한국어` | `ko` |
| `ja`, `japanese`, `日本語` | `ja` |
| `en`, `english` | `en` |
| `zh`, `chinese`, `中文` | `zh` |
| `es`, `spanish`, `espanol`, `español` | `es` |

## Workflow

1. Parse the user's requested scope.
   - If `--scope project`, target `.codex/ywc.json`.
   - If `--scope user`, target `~/.codex/ywc.json`.
   - If `--scope session`, reject it and do not write any file.
   - If scope is omitted, ask whether to use `project` or `user`.
2. Parse the requested language.
   - If `--lang <value>` is present, normalize it using the alias table.
   - If language is omitted, ask for one of `ko`, `ja`, `en`, `zh`, or `es`.
   - If language is unsupported, ask for a corrected value before writing.
3. Before writing, state the target path and canonical language code.
4. Create the parent directory when needed.
5. Create or update the target file with exactly this shape:

   ```json
   {
     "lang": "<canonical-code>"
   }
   ```

6. Report the completed scope, path, and language code.

Do not add extra config keys. Do not create `.codex/tmp/ywc-session.json`.

## Output Format

After a successful write, report the result in this shape:

```text
Status: DONE
Scope: <project|user>
Path: <target-path>
Language: <canonical-code>
```

If the skill needs more information or rejects the request, use the same
`Status:` line with `NEEDS_CONTEXT` or `BLOCKED`, then state the reason and the
next required input.

## Session Scope Rejection

If the user requests `--scope session`, explain:

- Session defaults are intentionally out of scope.
- Conversation language follows the user's current language naturally.
- Durable artifact language is resolved by the shared policy:
  explicit `--lang` > project `.codex/ywc.json` > project guidance
  `AGENTS.md` / `CODEX.md` / `CLAUDE.md` > user `~/.codex/ywc.json` > ask user.

Then stop without writing files.

## Validation

After writing a config file:

- Confirm the file exists at the expected path.
- Confirm it is valid JSON.
- Confirm `.lang` is one of `ko`, `ja`, `en`, `zh`, or `es`.

For project scope, do not commit `.codex/ywc.json` automatically. It is a project
policy file; let the user decide whether it belongs in version control.
