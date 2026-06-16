# ywc-verify-done

A process-discipline skill that enforces fresh verification evidence before any completion claim.

## What It Does

Invoke this skill immediately before surfacing any completion claim — "work done", "tests pass", "build succeeds", "bug fixed", "requirements met". It enforces a 5-step Gate Function:

1. **IDENTIFY** — Name the exact shell command that proves the claim.
2. **RUN** — Execute the command fresh **in the current message**.
3. **READ** — Read the full output and exit code.
4. **VERIFY** — Confirm the output supports the exact wording of the claim.
5. **CLAIM** — Only after steps 1–4, surface the claim **together with the verification block**.

Unverified-assertion vocabulary ("should", "probably", "seems") is blocked.

## When It Triggers

- The user signals completion ("완료", "done", "完了").
- Just before a commit, PR creation, or merge.
- Just before an executor transitions to the next task.
- Immediately after a subagent return payload is received.

## When NOT to Use

- During active implementation drafting → `ywc-code-gen`
- Root-cause investigation of a bug → `ywc-debug-rootcause`
- Pre-implementation confidence assessment → the planning or spec-review skill that owns the decision
- Codebase exploration before planning → `ywc-plan`

## References

For the full ruleset, output format, and Rationalization Defense, see [SKILL.md](./SKILL.md). The underlying discipline is adapted from `superpowers:verification-before-completion`.

## Localized Versions

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
