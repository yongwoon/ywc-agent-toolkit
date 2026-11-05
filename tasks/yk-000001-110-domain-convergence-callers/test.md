# Single owner spec convergence — scenarios

## AC-10 — automatic readiness boundaries
1. Invoke a new Medium and Large spec with default options; invoke with `--no-converge`, noninteractive mode, Small scale, and Re-plan.
2. Exercise auth and agentic as readiness-owning callers, with a spy on planner and spec-ready invocations.
3. Test both interactive and noninteractive agentic paths.

Expected: default new Medium/Large runs spec-ready exactly once; exclusions run it zero times automatically; auth/agentic planner passes `--no-converge` and owns exactly one readiness pass. Agentic preserves `--artifact-profile agentic` and producer-owned Result/Status/Scale/Artifact sections. Spec-ready goal and Re-plan termination boundaries remain intact; no recursive planner call occurs.

## Failure-mode coverage
Steps: inspect every existing caller, including auth and agentic, and include a duplicate-call negative control; inspect the cross-skill graph ownership entry.

Expected: no caller double-runs convergence. Static expected-call traces are not live invocation evidence; report unavailable runtime as UNVERIFIED.
