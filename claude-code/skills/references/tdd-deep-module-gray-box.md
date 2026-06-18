# TDD, Deep Module, Gray Box — Shared SoT for ywc-* Executors

> Shared reference document. The single source of truth for the three design disciplines drawn from Matt Pocock's "AI coding pitfalls 3/4/5" across the `ywc-*` generation and execution skills. Generation/execution skills write *to* these rules; this file keeps the disciplines identical across `ywc-code-gen`, `ywc-sequential-executor`, and `ywc-parallel-executor` instead of re-explaining them in three places.
>
> Companion to [readable-code.md](./readable-code.md) (§E reuse, §G structural smells, anti-dogma guardrails), [principles.md](./principles.md) (evidence / scope / failure discipline), [confidence-gate.md](./confidence-gate.md) (readiness scoring when a contract is ambiguous), and [subagent-status-actions.md](./subagent-status-actions.md) (status vocabulary).

## How skills use this file

- **`ywc-code-gen`** — Phase 1 runs the §2 RED-first gate by default; §3 governs interface-first generation; §4 sets review depth and the critical-path escalation in the Confidence Gate / completion report.
- **`ywc-sequential-executor`** — Step 3 applies §2 (test-first for behavior changes) and §3 (interface-first); Step 4.5/5 apply §4 critical-path auto-escalation.
- **`ywc-parallel-executor`** — Step 4b worker payload carries §2 + §3 directives; Step 4d/4e apply §4 critical-path auto-escalation.

The disciplines are **language-agnostic**. Language-specific test/idiom detail belongs to the per-language reviewers, not here.

## 1. When this applies

Apply §2–§4 to **behavior-changing work**: new features, bug fixes, new public contracts, cross-layer generation, and task execution that adds or alters observable behavior. Pure docs / formatting / metadata / config-only / mechanical changes take the §"Allowed exceptions" path.

## 2. Feedback loop — don't outrun your headlights (pitfall 3)

The failure mode: an LLM generates a large body of code, then runs the type checker / tests only at the end — by which point the code is already broken in ways that are expensive to unwind. Feedback speed is the speed limit.

Rules for behavior-changing work:

- A failing test must **exist and be confirmed RED** before the implementation is finalized. RED must fail for the *intended* reason (the behavior is unimplemented) — not because the test itself throws (import error, typo, bad fixture).
- If an existing regression or behavior test already fails for the intended reason, record it and use that as the RED state instead of authoring a duplicate test.
- Implement the **minimum** that turns the test GREEN. Refactor only after green.
- Keep the loop short: prefer the smallest unit that produces real feedback over a big-bang generate-then-verify pass.

**`ywc-code-gen` default (minimal RED gate)**: the QA lane authors the tests first and the orchestrator confirms RED before Backend/Frontend implementation is finalized; Backend and Frontend still run in parallel with each other. This is **one** RED-before-implement checkpoint.

**`--tdd` (opt-in, stronger)**: the full RED → GREEN → REFACTOR cycle with per-stage checkpoint commits, delegated to [`ywc-tdd-ritual`](../ywc-tdd-ritual/SKILL.md). `--tdd` **supersedes** the default minimal gate — it is the strict superset, not an additional pass; do not run both.

Trade-off: the default gate is fastest and gates the headlights without per-stage commits; `--tdd` gives a stronger audit trail (RED/GREEN/REFACTOR commits) at the cost of more commits and time. Default off; opt in when the audit trail is worth it.

## 3. Deep module boundary — interface first (pitfall 4)

The failure mode: the LLM defaults to many shallow modules with complex interfaces — a maze it later gets lost in, mis-edits, and breaks elsewhere. Deep modules (simple interface, substantial hidden implementation) are navigable.

Rules:

- Design the **public interface before the body** — API signature, DTO, component props, service method, event payload, CLI flag. The interface is a human/strategist decision; the body is the implementation the AI fills in.
- Hide implementation behind the interface; do not expose internals callers do not need.
- Do **not** proliferate shallow single-use wrappers to satisfy a "small function" reflex. Keep cohesive behavior together.
- Honor [readable-code.md](./readable-code.md) §G and its anti-dogma guardrails: add an interface only for a **real boundary**. Never specify speculative generality or premature abstraction the requirement does not yet need.

When a public contract changes, write the new contract down (and report it) before implementing against it.

## 4. Gray-box verification + critical-module exception (pitfall 5)

The failure mode: AI raises code volume past human review capacity, so reviewing every line is infeasible. The answer is gray-box review — verify the **interface/contract** works and delegate the internals — **except** for critical modules, which still require internal review.

Default (non-critical): verify the public contract / contract tests pass and delegate internals to the worker. Do not exhaustively re-read every internal line.

**Critical-module exception — internal review required.** A change is *critical* when its Ownership/files match any of:

`auth` · `authn` · `authz` · `session` · `oauth` · `jwt` · `token` · `password` · `credential` · `secret` · `crypto` · `encrypt` · `decrypt` · `sign` / `verify` · `payment` · `billing` · `invoice` · `checkout` · `finance` · `ledger` · `wallet` · PII / personal-data handlers · external-input boundaries (`webhook`, `upload`, `deserialize`)

A project may extend this set via an additive `critical_paths` list in `CLAUDE.md`, for example `critical_paths: ["packages/auth/**", "billing/**"]`. When in doubt, treat as critical — fail safe toward more review.

**Detection timing differs by skill** (do not conflate):

- `ywc-code-gen` evaluates the match against the **generated file set after generation** (the file list does not exist before Phase 1).
- The executors evaluate the match against the **task's declared Ownership, before implementation** (pre-flight knowledge).

**Auto-escalation on a critical match:**

- `ywc-code-gen` — the Confidence Gate requires internal review of the critical modules (gray-box is insufficient), and the completion report lists them with `/ywc-security-audit` as a **REQUIRED** next step.
- `ywc-sequential-executor` / `ywc-parallel-executor` — force `/ywc-impl-review` (even if `--review` was not passed) and route to `/ywc-security-audit` before delivery (Step 5 / Step 4e). Non-critical tasks keep gray-box verification.

## Allowed exceptions

Docs-only edits, pure formatting, metadata, generated README locale updates, and mechanical/config-only changes may skip the §2 RED state — but must report `TDD Exception: <reason>` (e.g., `TDD Exception: config-only, no observable behavior`). Never fabricate empty tests to satisfy the gate; an empty `describe`/`it` with no real assertion is a stub, not a test.

## Reporting contract

When a skill governed by this file completes behavior-changing work, its report includes:

- **Changed public contracts** — interfaces/signatures/DTOs added or altered.
- **Tests RED→GREEN** — which tests first failed (RED) and now pass, or `N/A (exception: <reason>)`.
- **Critical modules** — any critical-path files touched and the internal review / `ywc-security-audit` routing applied.
- **Exceptions** — any §"Allowed exceptions" path taken, with the reason.
