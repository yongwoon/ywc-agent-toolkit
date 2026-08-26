---
name: ywc-setup
description: (ywc) Use when configuring the default output language or collaborator initials for Codex ywc skills. Triggers: "ywc-setup", "setup ywc language", "setup collaborator initials", "ywc 언어 설정", "project language default", "user language default". Do not use for Claude Code setup, session language defaults, or generating project documentation.
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

Optional fields:

- `--lang <value>` - normalize and write a supported language code.
- `--initials <value>` - write unchanged when it matches `^[a-z0-9]{2,4}$`.
- At least one of `--lang` or `--initials` is required. Values are never
  silently normalized for initials; uppercase input is rejected.

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
2. Parse the requested fields.
   - If `--lang <value>` is present, normalize it using the alias table.
   - If both fields are omitted, ask for the requested field values.
   - If `--lang` is omitted but `--initials` is supplied, do not ask for a
     language; preserve the existing language value.
   - If language is unsupported, ask for a corrected value before writing.
   - If `--initials` is present, reject values outside `^[a-z0-9]{2,4}$`.
   - If only `--initials` is present, preserve the existing language value.
   - If only `--lang` is present, preserve the existing initials value.
3. Before writing, state the target path and canonical language code.
4. Create the parent directory when needed.
5. Under an exclusive adjacent lock, read the existing JSON object, merge only
   the requested fields, and preserve unknown keys. Write through a unique
   same-directory temporary file, flush and fsync it, atomically replace the
   target, fsync the directory, and validate the replaced JSON.

The resulting object may contain either or both optional fields:

   ```json
   {
     "lang": "<canonical-code>",
     "initials": "<lowercase-alphanumeric>"
   }
   ```

6. Report the completed scope, path, and language code.

Existing unknown keys are retained. Do not create `.codex/tmp/ywc-session.json`.

## Output Format

After a successful write, report the result in this shape:

```text
Status: DONE
Scope: <project|user>
Path: <target-path>
Language: <canonical-code>
Initials: <lowercase-alphanumeric>
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
- When present, confirm `.initials` matches `^[a-z0-9]{2,4}$`.

For project scope, do not commit `.codex/ywc.json` automatically. It is a project
policy file; let the user decide whether it belongs in version control.
