# ywc-setup

Codex `ywc-*` Skill の default output language を project scope または user scope
で設定します。

## 使用例

```bash
$ywc-setup --scope project --lang ko
$ywc-setup --scope user --lang ja
```

## 動作

- `--scope project`: `.codex/ywc.json` に `{ "lang": "<code>" }` を書きます。
- `--scope user`: `~/.codex/ywc.json` に `{ "lang": "<code>" }` を書きます。
- `--scope session`: unsupported です。`.codex/tmp/ywc-session.json` は作成しません。

対応 code は `ko`, `ja`, `en`, `zh`, `es` です。`korean`, `japanese`, `english`,
`chinese`, `spanish`, `한국어`, `日本語`, `中文`, `espanol`, `español` などの alias は
canonical code に normalize します。

Language resolution は `--lang` > `.codex/ywc.json` > `AGENTS.md` / `CODEX.md` /
`CLAUDE.md` > `~/.codex/ywc.json` > user に質問、の順序です。Skill-level default はありません。
