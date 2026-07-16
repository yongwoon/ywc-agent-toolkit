# Generic Evidence Fallback

When manifests, project guidance, and existing code do not establish the stack or auth boundary, do not guess a library or service.

1. State the missing evidence (runtime, framework, persistence, deployment, existing identity provider, or trust boundary).
2. Invoke `$ywc-tech-research` with the evidence question and project constraints.
3. Convert its result into a recommendation only after the policy record approves it.
4. If research is inconclusive, return `BLOCKED`; if the user must choose a boundary or provider, return `NEEDS_CONTEXT`.

No stack-specific playbook or supported-stack allowlist is created by this fallback.
