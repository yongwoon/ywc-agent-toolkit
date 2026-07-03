# Output Language Resolution — Shared Reference

The single canonical definition of how every language-aware `ywc-*` skill resolves the
**output language** of the documents, PR text, and commit messages it produces. Consuming
skills reference this file with an explicit `> **Action required**: Read
[references/language-resolution.md]` directive and MUST NOT restate the precedence chain,
code list, or section format inline (single-source-of-truth rule).

Used by `ywc-task-generator`, `ywc-spec-writer`, `ywc-plan`, `ywc-create-pr`, and
`ywc-commit`. Adding a new consumer means adding one pointer in that skill's body and one
row to the consuming-skill list in `claude-code/skills/CLAUDE.md` — nothing here changes.

## Scope

This governs **output language only** — the language of ywc-generated artifacts. It never
governs the session / conversational language (the user chats in whatever language they
want, always). Absence of any policy is a no-op: it never blocks, delays, or errors a
consuming skill.

## Precedence Chain

Resolve in this order; the first rung that yields a valid language code wins:

1. **`--lang` flag** — an explicit per-call flag on the consuming skill (normalized, see
   [Code List](#code-list--full-name-normalization)).
2. **Project policy** — a `## Language Policy` section in the project `CLAUDE.md`.
3. **User policy** — a `## Language Policy` section in the user-global `~/.claude/CLAUDE.md`.
4. **Each consuming skill's existing fallback** — the skill's own pre-canonical behavior
   (e.g. `ywc-task-generator` infers-then-asks and defaults `en`; `ywc-spec-writer` defaults
   `ko`; `ywc-create-pr` prompts). This terminal rung is deliberately **NOT** a hardcoded
   `en` — routing through each skill's own fallback is what preserves no-regression behavior
   when no policy is configured.

```
resolve(lang_flag, project_claude_md, user_claude_md, skill_fallback):
  if lang_flag present            -> normalize(lang_flag)
  elif project ## Language Policy -> its code   # project beats user
  elif user ## Language Policy    -> its code
  else                            -> skill_fallback   # NOT a forced 'en'
```

## Canonical `## Language Policy` Section Format

Written by `ywc-setup-language`, read by this resolution. A file has at most one such
section (setup replaces in place, never appends a duplicate):

```markdown
## Language Policy

- **Output language**: <code>   <!-- one of: ko | ja | en | es | zh -->
- Applies to: ywc-generated documents (plan / spec / task), PR title & body, commit message description.
- Keep in English regardless of language: conventional-commit type prefix, PR-title task-id/prefix, technical terms.
```

## Code List & Full-Name Normalization

Supported output-language codes: `ko | ja | en | es | zh`.

`normalize()` accepts either the code or its full name (case-insensitive) and returns the code:

| Input | Code |
|---|---|
| `ko`, `korean` | `ko` |
| `ja`, `japanese` | `ja` |
| `en`, `english` | `en` |
| `es`, `spanish` | `es` |
| `zh`, `chinese` | `zh` |

A `## Language Policy` whose `Output language` value is missing or not one of the five codes
is **malformed**: treat that rung as absent and fall through to the next rung. `--show`
reports a malformed policy as invalid rather than silently ignoring it.

## English-Preserved Tokens

Regardless of the resolved language, the following always stay English:

- Conventional-commit `type:` prefix (`feat:`, `fix:`, `docs:`, …).
- PR-title `[task-id]` / conventional prefix (only the PR **body** follows the resolved
  language; a caller-provided `--title` stays verbatim).
- Technical terms — per the "keep technical terms in English" policy already in
  `claude-code/skills/CLAUDE.md`.

## Where Resolution Runs (main context vs subagents)

Resolution is performed in the **main skill context**, where both `~/.claude/CLAUDE.md` and
the project `CLAUDE.md` are auto-loaded. A dispatched subagent receives a fresh context that
does **not** include the user-global `~/.claude/CLAUDE.md`, so a subagent that re-resolves on
its own can silently miss the user rung (breaking project-over-user precedence and the
user-global default).

- **Recommended pattern**: the main-context orchestrator resolves the language **once** and
  passes the resolved code to its subagents as an explicit payload field. Subagents do not
  re-resolve.
- **If a subagent must resolve independently**, it MUST explicitly `Read` both
  `~/.claude/CLAUDE.md` and the project `CLAUDE.md` rather than relying on auto-load.

## Back-Compat With Older CLAUDE.md Cues

Before this canonical section existed, some skills read looser cues — `ywc-task-generator`
read a "Language Policy section **or** Documentation Writing Guidelines" cue; `ywc-spec-writer`
read a "declared primary documentation language" note. The canonical `## Language Policy`
section **coexists with and takes precedence over** those:

- When a canonical `## Language Policy` is present, it is the authoritative project/user rung
  and wins.
- When it is **absent**, a consuming skill MAY still honor its own pre-existing looser cue as
  a fallback **before** its hardcoded default. This preserves no-regression behavior for
  projects that configured language the old way and have not yet run `ywc-setup-language`.

## Edge Cases

- Both project and user policy present → **project wins**.
- Policy present but malformed / code unrecognized → treat that rung as absent, fall through.
- `--lang korean` (full name) → normalized to `ko` before use.
- `ywc-create-pr --title "…"` with a policy but no `--lang` → policy governs the **body**
  language; the provided `--title` is used verbatim.
- User-global `~/.claude/CLAUDE.md` absent on `--user` setup → it is created with only the
  delimited section (no other global instructions fabricated).
- A consuming skill resolves language inside a fan-out subagent → the main-context
  orchestrator resolves once and passes the resolved code in the subagent payload; the
  subagent never relies on an auto-loaded user-global `CLAUDE.md` (absent in its context).
