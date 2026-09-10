# Subagent Prompt Directives (Step 4b)

Append each of the following six directives **verbatim** to every subagent prompt spawned in Step 4b. These directives are shared across every task category (`db`/`api`/`ui`/`test`/`infra`/`refactor`) and every `subagent_type` — none of them are category-specific, so they live here once instead of being restated per dispatch path in the SKILL.md body.

Do not paraphrase or summarize a directive when appending it — the exact wording (including the escape hatches like `NEEDS_CONTEXT`, `BLOCKED`, and `[PAUSED — ...]`) is what lets the orchestrator's Status Routing table parse the subagent's eventual return correctly.

Order does not matter within the prompt; all six must be present.

**Question-First directive:**

> Before any code change: read `task.md` and the Spec Reference, then enumerate genuinely ambiguous decisions whose wrong answer would force a rewrite (interface shape, data model, naming that conflicts with existing code, library choice when more than one is installed). If the list is non-empty, return `NEEDS_CONTEXT` with the questions enumerated — do not infer from neighboring tasks. Inferring silently compounds error and is the most expensive failure mode. See [../../references/question-first-gate.md](../../references/question-first-gate.md) for what counts as genuine ambiguity and the question format.

**Completeness directive:**

> This implementation will be merged directly into the base branch — treat it as production code. Before returning output: (1) every function/method must have a complete implementation body — no `// TODO`, no `// rest of code`, no placeholder stubs; (2) all imports must be used and all referenced symbols must be defined; (3) tests must contain real assertions, not empty `it()` blocks; (4) if token budget is approaching and generation is incomplete, stop at a clean function boundary and write `[PAUSED — X of Y files complete. Continue: <file-list>]` — never truncate mid-function. A stub is a compile error; a truncated function is worse.

**Tool Error Recovery directive:**

> When a tool call returns an error, do not enter extended thinking — apply the recovery action immediately. For `Edit`/`Update` → "Error editing file": (1) re-read the full file with `Read`, (2) retry the edit with `old_string` from the fresh content. For `Bash` non-zero exit: inspect the error, fix the root cause (wrong flag, path, binary), re-run. Maximum 2 fix attempts for any tool error before returning `BLOCKED` with the file path, attempted change, and exact error text.

**Simplicity + Surgical Changes directive:**

> Implement the minimum code that satisfies this task — no speculative features, no unsolicited abstractions, no "flexibility" that wasn't asked for. When editing existing code: touch only files listed in your declared Ownership; do not improve adjacent code, comments, or formatting unless they are the direct subject of this task. If you notice unrelated issues, mention them in the PR description — do not fix them. Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify before committing.

**Interface-first (deep module) directive:**

> Before writing the body, design the public interface this task exposes or changes — function signature, endpoint, event payload, DTO, component props, CLI flag — and keep the implementation behind it. Do not split cohesive behavior into shallow single-use wrappers, and add an interface only for a real boundary (no speculative generality). A shallow-module maze is what the next reader, human or AI, gets lost in. See [../../references/tdd-deep-module-gray-box.md](../../references/tdd-deep-module-gray-box.md) §3.

**Test-first-where-feasible directive:**

> If this task changes observable behavior, author the test first and confirm it fails (RED) for the intended reason before implementing, then make it pass (GREEN) — do not weaken or delete a test to go green. Don't outrun your headlights: feedback speed is your speed limit. Docs/config/mechanical tasks may skip the RED state but must state the reason; never fabricate an empty/passing test for an untestable change. See [../../references/tdd-deep-module-gray-box.md](../../references/tdd-deep-module-gray-box.md) §2.
