---
name: ywc-setup-language
version: 1.0.0
description: (ywc) Use when the user wants to set or inspect the persistent output language for ywc-generated documents, PRs, and commit messages so they stop passing --lang on every call. Triggers: "set output language", "set project language", "ywc-setup-language", "언어 설정", "언어 정책 설정", "言語設定", "出力言語を設定". Do not use for a one-off per-call override (pass --lang to the consuming skill instead), the session/chat language (never config-governed), editing consumer skills, or defining the resolution rules themselves (owned by references/language-resolution.md).
category: config
phase: setup
requires: []
advisor_budget: 0
allowed tools: Read, Edit, Write, Bash, Grep, Glob
---

# Setup Language Skill

**Announce at start:** "I'm using the ywc-setup-language skill to persist the output language into the appropriate CLAUDE.md."

Persist a project- or user-level **output language** into a canonical `## Language Policy`
section of the appropriate `CLAUDE.md`, so every language-aware `ywc-*` skill produces
documents, PR text, and commit messages in that language with no per-call `--lang` flag and
no per-call prompt. Reading the policy back is a separate `--show` mode.

This skill only **writes** the policy. How consuming skills **read and resolve** it (the
precedence chain, code list, and section format) is defined once elsewhere:

> **Action required**: Read [../references/language-resolution.md] before writing or
> inspecting a policy — it is the single source of truth for the canonical `## Language
> Policy` section format, the supported code list, full-name normalization, and the
> precedence chain. Do not restate that content in this skill body.

## Rationalization Defense

When tempted to skip a rule, check this table first:

| Excuse | Reality |
|---|---|
| "The file already has some language note, I'll just append a new section" | Appending creates a duplicate `## Language Policy` heading (AC3 violation). Setup is a create-or-**replace** on the delimited section — exactly one such heading must exist afterward. |
| "There's an ad-hoc language sentence elsewhere in CLAUDE.md, I'll rewrite it to match" | Out of scope. Setup writes only the canonical delimited section; it never migrates or rewrites pre-existing prose. |
| "`--user` target `~/.claude/CLAUDE.md` doesn't exist, so this is an error" | Not an error. Create the file with **only** the delimited section (EC5) — do not fabricate other global instructions. |
| "The user typed `korean`, that's not a valid code, stop" | Normalize full names to codes (`korean`→`ko`, EC3) before writing. Reject only inputs that map to none of `ko\|ja\|en\|es\|zh`. |
| "`--show` found no policy, I should write a default so future calls work" | `--show` is read-only (AC4). Report "no policy configured" and the fallback source — never write during show. |
| "I'll add a forced global default so absence resolves cleanly" | No. The no-block invariant (NFR1) requires absence to fall through to each consuming skill's own fallback. Setup never introduces a global default. |

## Arguments

| Argument | Form | Example | Description |
|---|---|---|---|
| Language | positional | `ko`, `japanese` | Output language code (`ko\|ja\|en\|es\|zh`) or full name (`korean`, `japanese`, `english`, `spanish`, `chinese`). Normalized to a code before writing. Required unless `--show`. |
| `--user` | flag | | Target the user-global `~/.claude/CLAUDE.md` instead of the project `CLAUDE.md` (the default target). |
| `--show` | flag | | Read-only: report the resolved language and its source rung (project / user / none). No write. |

## Procedure

### Write mode (default — positional language given)

1. **Normalize** the positional argument to a code using the mapping in
   `references/language-resolution.md`. If it maps to none of `ko|ja|en|es|zh`, stop and
   report the accepted values — do not write.
2. **Select the target file**: project `CLAUDE.md` (repo root) by default, or
   `~/.claude/CLAUDE.md` when `--user` is set.
3. **Create-or-replace the `## Language Policy` section** (idempotent):
   - If the target file has a `## Language Policy` section, replace that delimited section in
     place — its heading through the line before the next `## ` heading (or EOF). Exactly one
     `## Language Policy` heading must remain afterward (AC3, EC6).
   - If the section is absent, append the canonical section.
   - If the **target file itself is absent** (common on `--user`), create it containing only
     the canonical section (EC5) — no other global instructions.
   - The section body is the canonical format from `references/language-resolution.md` with
     the resolved code filled into `**Output language**`.
4. **Confirm** with a one-line message naming the written file path and code (no
   `@`-activation prompt — user-global `~/.claude/CLAUDE.md` is already auto-loaded).

### Show mode (`--show`)

1. Resolve per the precedence chain in `references/language-resolution.md` (project policy →
   user policy → none), reading each `CLAUDE.md`'s `## Language Policy` section.
2. Report the resolved code and the winning source rung, or "no policy configured" with the
   fallback source when neither file has a valid section. A malformed section is reported as
   invalid (EC2), not silently ignored.
3. Never write in show mode.

## Notes

- The canonical `## Language Policy` section supersedes older CLAUDE.md language cues; when
  it is absent, consuming skills still honor their own prior fallback (see the reference).
  This preserves no-regression behavior for projects that have not yet run this skill.
- Keep-in-English tokens (conventional-commit `type:` prefix, PR-title `[task-id]`/prefix,
  technical terms) are unaffected by the configured language — they stay English by policy.
