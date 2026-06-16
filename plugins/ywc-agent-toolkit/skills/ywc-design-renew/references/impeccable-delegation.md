# impeccable Delegation (Graceful Enhancement)

`ywc-design-renew` is **self-contained** — it never *requires* the external
`impeccable` skill. But when `impeccable` is present, it is a more capable
design engine (23 commands, 41 deterministic detectors, project context system),
so delegate to it and let this skill act as the ywc-workflow orchestrator
(context gate → delegate → verify → capture learnings).

This file defines how to detect `impeccable` and map this skill's modes onto it.
When `impeccable` is absent, ignore this file and use
[anti-slop-ruleset.md](anti-slop-ruleset.md) directly.

## Detection (run once, in Phase 0)

`impeccable` is a user-/project-installed skill, not a guaranteed dependency.
Detect it cheaply and record a single boolean `IMPECCABLE_AVAILABLE`:

```bash
# Skill install (any of these locations) OR standalone CLI present?
( ls -d "${CODEX_HOME:-$HOME/.codex}/skills/impeccable" .codex/skills/impeccable \
       ~/.codex/skills/impeccable .agents/skills/impeccable 2>/dev/null | head -1 ) \
  || command -v impeccable 2>/dev/null \
  || npx --no-install impeccable --version 2>/dev/null
```

- If a skill directory exists → delegate via Codex skill invocation
  (`Use $impeccable to ...`), the richest path.
- Else if only the CLI resolves → use `npx impeccable detect <path>` for check
  mode; fall back to the self-contained ruleset for renew (the CLI detects but
  does not rewrite).
- Else → `IMPECCABLE_AVAILABLE=false`; use the self-contained ruleset for both
  modes.

Do not install impeccable automatically. If the user would benefit from it,
mention it once as an optional enhancement and proceed with the fallback.

## Design-context handshake

impeccable refuses to produce non-generic output without confirmed design
context (audience / use-cases / brand tone), stored in `.impeccable.md` or
`PRODUCT.md` + `DESIGN.md`. `ywc-design-renew` has the **same** requirement.
Reconcile them so context is gathered once:

1. If `.impeccable.md` / `PRODUCT.md` / `DESIGN.md` exists → read it; context is
   satisfied for both this skill and any impeccable delegation.
2. Else if `IMPECCABLE_AVAILABLE` → invoke the `impeccable` skill's teach mode to gather and persist
   context, then continue.
3. Else → gather context inline with the three required questions (audience,
   use-cases, brand tone) and proceed without writing impeccable's files.

## Mode mapping

| ywc-design-renew | impeccable skill call | impeccable CLI | Self-contained fallback |
|---|---|---|---|
| `--mode check` (audit, no edits) | `Use $impeccable to audit <scope>` | `npx impeccable detect <path>` | Grep Part B/C signals + AI Slop Test (anti-slop-ruleset.md) |
| `--mode renew`, new surface | `Use $impeccable to craft <feature>` | — (no rewrite) | Apply Part D DO rules from scratch toward a bold direction |
| `--mode renew`, existing surface | `Use $impeccable to polish <scope>` | — (no rewrite) | Apply Part D fixes to existing code, removing Part B/C tells |
| Component/token extraction | `Use $impeccable to extract <target>` | — | Out of scope — note and skip |

When delegating, still run this skill's **Phase 4 verification** afterward
(re-check + before/after screenshots): impeccable produces the design, but
ywc-design-renew owns the evidence that slop findings are actually gone and that
behavior/IA did not regress.

## Attribution note

`impeccable` is Apache-2.0, based on Anthropic's `frontend-design` skill. This
skill does not vendor impeccable's files — it distills the *principles* into a
portable ruleset and delegates to the installed copy when present. Keep the
self-contained ruleset principle-level (not a verbatim copy) so the two evolve
independently.
