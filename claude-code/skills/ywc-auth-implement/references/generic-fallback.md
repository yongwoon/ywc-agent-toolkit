# Generic Fallback — Real-Time Research When Stack Evidence Is Insufficient

This skill never ships a fixed or "supported" stack list (AC5). When stack evidence — framework, database, existing auth-adjacent dependencies — is insufficient for a direct recommendation, use this fallback instead of guessing or defaulting to a favorite library.

## Trigger

Stack evidence is insufficient when any of the following hold:

- The project's manifest (`package.json`, `pyproject.toml`, `go.mod`, etc.) does not clearly identify a web framework or the framework is unfamiliar/unversioned.
- No existing auth-adjacent dependency (session middleware, JWT library, OAuth client) is present to infer conventions from.
- The detected framework has multiple viable auth approaches with no clear project precedent (e.g., a framework with 3+ equally common auth libraries and no existing pattern in the codebase).

## Fallback Procedure

1. **Repository-internal check first** — search the existing codebase for any partial auth scaffolding, config, or comments indicating an intended library (`grep`/`rg` for `auth`, `session`, `jwt`, `oauth` near the manifest and config files).
2. **Real-time research**, in this order (mirrors the project's Research & Reuse discipline):
   - GitHub code/repo search for battle-tested implementations against the detected framework.
   - Context7 or primary vendor documentation for the leading candidate libraries.
   - Package registry search (npm/PyPI/crates.io/etc.) for maintenance signal (recent releases, download counts, open critical issues).
3. **Route to `ywc-tech-research`** for a structured comparison when more than one credible candidate remains after step 2 — do not pick a favorite unilaterally.
4. **Record the outcome** in the Output Format "Recommendation" section as `<library/service + evidence>` if resolved, or `routed to ywc-tech-research: <comparison scope>` if still pending.

## What This Fallback Never Does

- Never invents a "supported stack" allowlist as a side effect of resolving this fallback — the fallback is per-invocation research, not a growing static list.
- Never falls back to hand-rolled implementation because research is inconclusive — inconclusive research is a `NEEDS_CONTEXT` state (ask the user to pick from the researched candidates), not a license to hand-roll.

## Stack Playbook Caching

v1 ships zero `references/stack-*.md` playbooks. A playbook is written only after a specific stack + policy combination has:

1. Passed `ywc-security-audit` with Critical/High = 0, and
2. Passed the policy-conditional E2E in `SKILL.md`'s Security/E2E gate section with captured evidence.

Until both conditions are met for a given stack, every invocation re-runs this fallback procedure — there is no shortcut through an unverified cache entry.
