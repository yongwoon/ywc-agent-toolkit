# Setup Language Skill (ywc-setup-language)

A Claude Code Skill that persists a project- or user-level **output language** so every
language-aware `ywc-*` skill produces documents, PR text, and commit messages in that
language without a per-call `--lang` flag or prompt.

## Overview

This Skill writes a canonical `## Language Policy` section into the appropriate `CLAUDE.md`:

- Sets the output language for ywc-generated documents (plan / spec / task), PR title & body,
  and commit message descriptions.
- Idempotent — re-running replaces the section in place instead of appending a duplicate.
- Read-only `--show` mode reports the currently resolved language and where it comes from.
- Additive and non-blocking — projects without a policy behave exactly as before.

It only **writes** the policy. How consuming skills resolve it (precedence chain, code list,
section format) lives in the shared reference `references/language-resolution.md`.

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

Full language names are accepted and normalized: `korean` → `ko`, `japanese` → `ja`,
`english` → `en`, `spanish` → `es`, `chinese` → `zh`.

## Arguments

| Argument | Description |
| --- | --- |
| `<language>` | Output language code (`ko\|ja\|en\|es\|zh`) or full name. Required unless `--show`. |
| `--user` | Write to the user-global `~/.claude/CLAUDE.md` instead of the project `CLAUDE.md`. |
| `--show` | Report the resolved language and its source rung (project / user / none). No write. |

## What it writes

```markdown
## Language Policy

- **Output language**: ko
- Applies to: ywc-generated documents (plan / spec / task), PR title & body, commit message description.
- Keep in English regardless of language: conventional-commit type prefix, PR-title task-id/prefix, technical terms.
```

## Precedence

The configured policy is one rung in the resolution chain read by consuming skills:
`--lang` flag → project `## Language Policy` → user `## Language Policy` → each skill's
existing fallback. A project policy beats a user policy. See
`references/language-resolution.md` for the full rules.

## Consuming skills

`ywc-task-generator`, `ywc-spec-writer`, `ywc-plan`, `ywc-create-pr`, `ywc-commit`.
