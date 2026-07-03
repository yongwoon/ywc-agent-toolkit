# ywc-setup

Codex `ywc-*` skill 의 기본 output language 를 project 또는 user scope 로 설정합니다.

## 사용 예

```bash
$ywc-setup --scope project --lang ko
$ywc-setup --scope user --lang ja
```

## 동작

- `--scope project`: `.codex/ywc.json` 에 `{ "lang": "<code>" }` 를 작성합니다.
- `--scope user`: `~/.codex/ywc.json` 에 `{ "lang": "<code>" }` 를 작성합니다.
- `--scope session`: 지원하지 않으며 `.codex/tmp/ywc-session.json` 을 만들지 않습니다.

지원 code 는 `ko`, `ja`, `en`, `zh`, `es` 입니다. `korean`, `japanese`, `english`,
`chinese`, `spanish`, `한국어`, `日本語`, `中文`, `espanol`, `español` 같은 alias 는
canonical code 로 normalize 됩니다.

언어 resolution 은 `--lang` > `.codex/ywc.json` > `AGENTS.md` / `CODEX.md` /
`CLAUDE.md` > `~/.codex/ywc.json` > 사용자에게 질문 순서입니다. Skill-level default 는 없습니다.
