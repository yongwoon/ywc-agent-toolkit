# ywc-setup

Configure the default output language and optional collaborator initials for
Codex `ywc-*` skills at project or user scope.

## Examples

```bash
$ywc-setup --scope project --lang ko
$ywc-setup --scope user --lang ja
$ywc-setup --scope project --initials yk
$ywc-setup --scope project --lang en --initials yk
```

## Behavior

- `--scope project`: updates `.codex/ywc.json`.
- `--scope user`: updates `~/.codex/ywc.json`.
- `--initials <value>`: accepts exactly 2–4 lowercase letters or digits
  (`^[a-z0-9]{2,4}$`) and preserves the value unchanged.
- At least one of `--lang` and `--initials` is required. Updating either field
  preserves the other field and any unknown JSON keys.
- `--scope session`: rejected; `.codex/tmp/ywc-session.json` is not created.

Writes use an adjacent exclusive lock, a unique same-directory temporary file,
fsync, atomic replacement, and final JSON validation. Invalid existing JSON is
rejected without replacement.

Supported codes are `ko`, `ja`, `en`, `zh`, and `es`. Aliases such as
`korean`, `japanese`, `english`, `chinese`, `spanish`, `한국어`, `日本語`, `中文`,
`espanol`, and `español` are normalized to canonical codes.

Language resolution is `--lang` > `.codex/ywc.json` > `AGENTS.md` / `CODEX.md` /
`CLAUDE.md` > `~/.codex/ywc.json` > ask user. There is no skill-level default.
