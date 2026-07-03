# YWC Language Resolution

This reference is the source of truth for Codex `ywc-*` skills that create
language-sensitive durable artifacts: specs, task docs, plans, PR prose,
project docs, testsheets, release notes, and similar human-facing files.

## Resolution Order

Resolve the artifact output language in this exact order:

1. **Explicit request**: `--lang <code>` or an equivalent explicit user
   instruction for the current artifact.
2. **Project default**: `.codex/ywc.json` in the current repository.
3. **Project guidance**: clear language instructions in `AGENTS.md`,
   `CODEX.md`, or `CLAUDE.md`, preferring Codex-native guidance when files
   conflict.
4. **User default**: `~/.codex/ywc.json`.
5. **Ask user**: if no tier resolves a language, ask which supported language
   to use before writing the artifact.

There is no skill-level output-language default. A skill must not silently fall
back to `ko`, `en`, or any other language when all tiers are unresolved.

Session defaults are intentionally out of scope. Do not read or write
`.codex/tmp/ywc-session.json` for language resolution. Conversation language can
follow the user's current message naturally, but durable artifact language is
resolved by the order above.

## Config Files

Project and user config files use the same shape:

```json
{
  "lang": "ko"
}
```

Allowed canonical values are:

Canonical code set: `ko`, `ja`, `en`, `zh`, `es`.

- `ko` - Korean
- `ja` - Japanese
- `en` - English
- `zh` - Simplified Chinese unless explicitly stated otherwise
- `es` - Spanish

Config files should store canonical codes only. If `.codex/ywc.json` or
`~/.codex/ywc.json` is malformed JSON, omits `lang`, or contains an unsupported
value, treat that tier as unresolved and continue to the next tier. Optionally
warn the user, but do not hard-fail unrelated skill work because of a bad config
tier.

## Alias Policy

Explicit user input may use canonical codes or known aliases. Normalize aliases
before applying the language:

| Input aliases | Canonical code |
| --- | --- |
| `ko`, `kr`, `korean`, `한국어` | `ko` |
| `ja`, `japanese`, `日本語` | `ja` |
| `en`, `english` | `en` |
| `zh`, `chinese`, `中文` | `zh` |
| `es`, `spanish`, `espanol`, `español` | `es` |

`kr` is accepted only for backward compatibility with existing documented
`ywc-project-docs` usage. New config files and new documentation should prefer
`ko`.

## Writing Policy

Use the resolved language for human prose in the generated artifact.

Keep machine-facing surfaces in English regardless of the resolved language:
commands, file paths, YAML keys, JSON keys, code, task IDs, branch names, labels,
front matter keys, section contract terms, and stable workflow identifiers.

Conversation language does not override artifact language. For example, the user
may ask in Korean while project config resolves artifact output to `en`; reply to
the user naturally, but write the artifact prose in English.
