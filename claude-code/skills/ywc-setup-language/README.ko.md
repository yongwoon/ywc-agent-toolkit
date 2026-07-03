# Setup Language Skill (ywc-setup-language)

Project 또는 user 단위 **output language** 를 저장해, 모든 language-aware `ywc-*` skill 이
per-call `--lang` flag 이나 prompt 없이 해당 언어로 document, PR text, commit message 를
생성하도록 하는 Claude Code Skill.

## Overview

이 Skill 은 알맞은 `CLAUDE.md` 에 canonical `## Language Policy` 섹션을 작성한다:

- ywc-generated document(plan / spec / task), PR title & body, commit message description 의
  output language 를 설정
- Idempotent — 재실행 시 섹션을 append 하지 않고 in-place 로 replace
- Read-only `--show` mode 로 현재 resolved 언어와 그 source 를 보고
- Additive & non-blocking — policy 가 없는 project 는 이전과 동일하게 동작

이 Skill 은 policy 를 **write** 만 한다. Consuming skill 이 이를 resolve 하는 방법(precedence
chain, code list, section format)은 shared reference `references/language-resolution.md` 에 있다.

## Usage

```text
/ywc-setup-language ko
```

```text
/ywc-setup-language ja --user
```

```text
/ywc-setup-language --show
```

Full language name 도 받아 정규화한다: `korean` → `ko`, `japanese` → `ja`,
`english` → `en`, `spanish` → `es`, `chinese` → `zh`.

## Arguments

| Argument | Description |
| --- | --- |
| `<language>` | Output language code(`ko\|ja\|en\|es\|zh`) 또는 full name. `--show` 가 아니면 필수. |
| `--user` | Project `CLAUDE.md` 대신 user-global `~/.claude/CLAUDE.md` 에 write. |
| `--show` | Resolved 언어와 source rung(project / user / none) 보고. Write 없음. |

## What it writes

```markdown
## Language Policy

- **Output language**: ko
- Applies to: ywc-generated documents (plan / spec / task), PR title & body, commit message description.
- Keep in English regardless of language: conventional-commit type prefix, PR-title task-id/prefix, technical terms.
```

## Precedence

설정된 policy 는 consuming skill 이 읽는 resolution chain 의 한 rung 이다:
`--lang` flag → project `## Language Policy` → user `## Language Policy` → 각 skill 의
기존 fallback. Project policy 가 user policy 를 이긴다. 전체 규칙은
`references/language-resolution.md` 참고.

## Consuming skills

`ywc-task-generator`, `ywc-spec-writer`, `ywc-plan`, `ywc-create-pr`, `ywc-commit`.
