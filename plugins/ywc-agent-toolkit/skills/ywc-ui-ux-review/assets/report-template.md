# UI/UX Review — {{TARGET_NAME}}

> **Reviewer**: Codex (`ywc-ui-ux-review`)
> **Date**: {{YYYY-MM-DD}}
> **Stack**: {{e.g., Next.js 15 + Tailwind CSS 4}}
> **Scope**: {{pages / features in scope}}
> **Live URL**: {{URL or "not available — code-only review"}}
> **Frameworks applied**: Nielsen 10 Heuristics · WCAG 2.2 AA · {{Material 3 / Apple HIG / "(none — generic platform")}} · {{Internal Design System or "(none detected)"}}

## Executive Summary

| Tier | Count |
|---|---|
| 🔴 Critical | {{N}} |
| 🟠 High | {{N}} |
| 🟡 Medium | {{N}} |
| 🟢 Low | {{N}} |
| **Total** | **{{N}}** |

### Top 3 Systemic Patterns

1. {{Most pervasive root cause, with count of related findings}}
2. {{Second pattern}}
3. {{Third pattern}}

### Recommended Top 5 Actions

1. {{Highest-leverage fix}}
2. {{...}}
3. {{...}}
4. {{...}}
5. {{...}}

---

## 🔴 Critical

> Issues that block usage, violate WCAG 2.2 AA, or risk data / security harm. **Fix before next release.**

### C-01 · {{Concise issue title}}

- **Location**: `{{file/path:line}}` and screen `{{route or selector}}`
- **Breakpoint(s)**: {{360 / 768 / 1280 / 1920 / all}}
- **Heuristic**: {{WCAG SC X.X.X / Nielsen #N / Material 3 — topic / Design System — token}}
- **Observed**: {{what is happening, with evidence reference}}
- **Expected**: {{what the heuristic requires}}
- **User-facing impact**: {{one sentence}}
- **Evidence**:
  - Screenshot: `{{path or marker}}`
  - Snapshot excerpt:
    ```
    {{accessibility tree fragment}}
    ```
- **Recommendation**:
  ```{{lang}}
  {{concrete code or design change}}
  ```

### C-02 · {{...}}

(repeat the structure above)

---

## 🟠 High

> Major usability degradation. **Fix in the current cycle.**

### H-01 · {{title}}

(same structure as Critical)

---

## 🟡 Medium

> Friction or inconsistency. **Schedule into the backlog.**

### M-01 · {{title}}

(same structure as Critical)

---

## 🟢 Low

> Polish opportunities. **Address opportunistically.**

### L-01 · {{title}}

(same structure as Critical)

---

## Appendix A — Methodology

This review followed the six-phase workflow defined in `ywc-ui-ux-review/SKILL.md`:

`Scope → Code Reconnaissance → Live UI Exploration → Per-Domain Review → Severity Triage → Report`

Live UI evidence was gathered via available browser tooling (`take_snapshot`, `take_screenshot`, `lighthouse_audit`, `resize_page`, `list_console_messages`, `evaluate_script`).

## Appendix B — Out of Scope

- {{Items the user explicitly excluded — e.g., onboarding flow, marketing site}}
- {{Areas where evidence could not be gathered — e.g., authenticated-only pages without test account}}

## Appendix C — Open Questions

- {{Questions for the team that arose during review}}
