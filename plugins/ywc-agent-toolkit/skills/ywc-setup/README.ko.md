# ywc-setup

Codex `ywc-*` skill 의 기본 output language 와 collaborator initials 를 project 또는 user scope 로 설정합니다.

## 사용 예

```bash
$ywc-setup --scope project --lang ko
$ywc-setup --scope user --lang ja
$ywc-setup --scope project --initials yk
$ywc-setup --scope project --lang en --initials yk
```

## 동작

- `--scope project`: `.codex/ywc.json` 을 update 합니다.
- `--scope user`: `~/.codex/ywc.json` 을 update 합니다.
- `--initials <value>`: `^[a-z0-9]{2,4}$` 인 lowercase alphanumeric 값만 허용하며 그대로 저장합니다.
- `--lang` 또는 `--initials` 중 하나 이상이 필요하며, 다른 field 와 unknown JSON key 를 보존합니다.
- `--scope session`: 지원하지 않으며 `.codex/tmp/ywc-session.json` 을 만들지 않습니다.

Write 는 adjacent exclusive lock, unique temporary file, fsync, atomic replacement 및 final JSON validation 을 사용합니다. 기존 JSON 이 malformed 이면 replacement 없이 거부합니다.

지원 code 는 `ko`, `ja`, `en`, `zh`, `es` 입니다. `korean`, `japanese`, `english`,
`chinese`, `spanish`, `한국어`, `日本語`, `中文`, `espanol`, `español` 같은 alias 는
canonical code 로 normalize 됩니다.

언어 resolution 은 `--lang` > `.codex/ywc.json` > `AGENTS.md` / `CODEX.md` /
`CLAUDE.md` > `~/.codex/ywc.json` > 사용자에게 질문 순서입니다. Skill-level default 는 없습니다.
