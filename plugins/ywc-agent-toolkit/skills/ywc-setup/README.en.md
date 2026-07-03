# ywc-setup

Configure the default output language for Codex `ywc-*` skills at project or
user scope.

## Examples

```bash
$ywc-setup --scope project --lang ko
$ywc-setup --scope user --lang ja
```

## Behavior

- `--scope project`: writes `{ "lang": "<code>" }` to `.codex/ywc.json`.
- `--scope user`: writes `{ "lang": "<code>" }` to `~/.codex/ywc.json`.
- `--scope session`: rejected; `.codex/tmp/ywc-session.json` is not created.

Supported codes are `ko`, `ja`, `en`, `zh`, and `es`. Aliases such as
`korean`, `japanese`, `english`, `chinese`, `spanish`, `한국어`, `日本語`, `中文`,
`espanol`, and `español` are normalized to canonical codes.

Language resolution is `--lang` > `.codex/ywc.json` > `AGENTS.md` / `CODEX.md` /
`CLAUDE.md` > `~/.codex/ywc.json` > ask user. There is no skill-level default.
