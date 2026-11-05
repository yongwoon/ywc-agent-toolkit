# Blind independent convergence-contract verification

Status: DONE_WITH_CONCERNS
Critical: 1, Warning: 0, Suggestion: 0

## Confirmed finding

- Severity: Critical (Completeness — omitted existing owned caller)
- Spec location: docs/ywc-plans/20261105-codex-issue69-upstream-adoption.md:162
- Current producer/consumer evidence: codex/skills/ywc-agentic/SKILL.md:116–118 invokes `ywc-plan [--non-interactive] --artifact-profile agentic`, forwarding non-interactive only if supplied. Lines 128–130 independently invoke `ywc-spec-ready --spec <artifact>` for Medium/Large after parsing the planner-owned closed Result. Lines 146–157 separate planner Result authority from ready Result authority.
- Proposed FR-10 says new Medium/Large plans auto-invoke readiness and explicitly names only auth as a caller to change. Its generic '기존 다른 caller도 조사해 중복 수렴을 막는다' does not name agentic's interactive path, owned result profile, or specific required call-site change. The named files checkbox at line 161 omits ywc-agentic.
- Failure: an interactive agentic Full Mode planner invocation lacks non-interactive/opt-out, so proposed planner behavior can first invoke readiness automatically, then agentic line 130 invokes it again. That duplicates amendment/revalidation work and exposes the consumer to output/result authority ambiguity. Non-interactive path is protected by its already-forwarded flag, so it must not be used as proof that interactive agentic is safe.
- Smallest fix: explicitly add `ywc-agentic/SKILL.md` and relevant contract fixture to FR-10. Append `--no-converge` to agentic's Full Mode planner invocation while preserving `--artifact-profile agentic` and conditional non-interactive propagation. Keep readiness owned by agentic after planner Result parsing. Add AC-10 cases: interactive Medium/Large agentic = planner nested ready 0, agentic-owned ready 1; non-interactive Medium/Large = same counts; Small = 0; preserve exact closed Result and final artifact authority. Add this known integration site to the coverage table rather than leaving it as implementation-time investigation.

No other worker artifacts were read. This is independent verification of the specific convergence integration boundary, not a full second review.
