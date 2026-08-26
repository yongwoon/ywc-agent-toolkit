# ywc-setup

Codex `ywc-*` Skill の default output language と collaborator initials を project
scope または user scope で設定します。

## 使用例

```bash
$ywc-setup --scope project --lang ko
$ywc-setup --scope user --lang ja
$ywc-setup --scope project --initials yk
$ywc-setup --scope project --lang en --initials yk
```

## 動作

- `--scope project`: `.codex/ywc.json` を更新します。
- `--scope user`: `~/.codex/ywc.json` を更新します。
- `--initials <value>`: `^[a-z0-9]{2,4}$` の lowercase alphanumeric 値をそのまま保存します。
- `--lang` または `--initials` の少なくとも一方が必要で、他の field と unknown JSON key は保持します。
- `--scope session`: unsupported です。`.codex/tmp/ywc-session.json` は作成しません。

Write は adjacent exclusive lock、unique temporary file、fsync、atomic replacement、final JSON validation を使用します。既存 JSON が malformed の場合は replacement せず拒否します。

対応 code は `ko`, `ja`, `en`, `zh`, `es` です。`korean`, `japanese`, `english`,
`chinese`, `spanish`, `한국어`, `日本語`, `中文`, `espanol`, `español` などの alias は
canonical code に normalize します。

Language resolution は `--lang` > `.codex/ywc.json` > `AGENTS.md` / `CODEX.md` /
`CLAUDE.md` > `~/.codex/ywc.json` > user に質問、の順序です。Skill-level default はありません。
