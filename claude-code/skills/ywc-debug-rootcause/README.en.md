# ywc-debug-rootcause

A process-discipline skill that forces **root-cause identification before any fix** for bugs, test failures, build failures, and unexpected behavior.

## What It Does

Enforces the Iron Law:

> **NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

No fix may be proposed before Phase 1 (Investigation) is complete. The 4-phase process:

1. **Phase 1 — Root-cause investigation** — Read errors fully, reproduce reliably, check recent changes, instrument multi-component boundaries, trace data flow upstream to the origin.
2. **Phase 2 — Pattern analysis** — Locate a working sibling in the same codebase, read it end-to-end, list every difference between broken and working (including ones that "cannot matter").
3. **Phase 3 — Hypothesis and testing** — Form a single hypothesis in the shape "X is the root cause; minimal change Z fixes it"; test by changing one variable at a time.
4. **Phase 4 — Implementation** — Write a regression test, apply a single fix, verify red-green-red, gate the completion claim through `ywc-verify-done`, then emit systemic prevention (§6): a recurring class is offered to `ywc-review-learnings --source debug`, a one-off cause is explicitly declared.

**If 3+ fixes fail on the same surface**, the situation is "architecture is wrong", not "fix harder". Stop and surface the design concern to the user — do not attempt a 4th fix.

## When It Triggers

- The user mentions "bug", "debug", "왜 안돼", "落ちる", "通らない", or similar.
- A test, build, or type-check fails.
- Two or more fix attempts on the same surface have already failed.
- `ywc-verify-done`'s failure-routing table sends the investigation here.

## When NOT to Use

- Active implementation drafting → `ywc-code-gen`
- Post-incident retrospective → `ywc-incident-postmortem`
- Security vulnerability triage → `ywc-security-audit`
- Pre-implementation confidence check → `ywc-confidence-gate` (planned)

## References

Phase-by-phase checklists, Rationalization Defense, and the architectural-stop signals are in [SKILL.md](./SKILL.md). The underlying discipline is adapted from `superpowers:systematic-debugging`.

## Localized Versions

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
