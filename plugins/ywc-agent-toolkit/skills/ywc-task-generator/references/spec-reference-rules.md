# Spec Reference Rules

Every task's `README.md` must include a `## Spec Reference` section. This section specifies the source-of-truth documents that the agent or developer executing the task must read **before implementation**.

Since LLMs do not retain full project context when executing tasks, explicitly linking specs here significantly reduces hallucination and scope creep.

## Required Structure

### 1. Primary Sources

List of links to source-of-truth documents. Each entry should include the specific section/anchor.

- **Default: project-relative paths only** (e.g., `docs/prd/auth.md#token-rotation`). This works in offline environments and allows drift tracking via version control.
- **External URLs** (Notion, Confluence, Figma, etc.) should only be used when the project explicitly allows it. See the sequential-executor policy for the project-level rule.
- **For tasks with no spec** (e.g., pure lint setup, housekeeping), mark as `N/A — no external spec (housekeeping / refactor / config only)`.

### 2. Summary

A 2–5 sentence summary. The purpose is to "provide enough orientation for the implementer to start without opening every link."

- The linked sources above are the source of truth; this summary is for quick understanding.
- If the two diverge, **trust the link and flag the drift**.

### 3. Out of Scope (from spec)

Items mentioned in the spec that are intentionally not addressed in this task. This is a guardrail against scope creep, preventing implementers from expanding scope just because something "seems natural."

- When handled by another task, specify that task's name.

## Hard Rule

**Never leave Spec Reference as an empty section or omit it** — use `N/A` when there is no spec. An empty section makes it impossible for the implementer to tell whether it was forgotten or genuinely absent.
