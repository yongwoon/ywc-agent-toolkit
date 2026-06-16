# ywc-tdd-ritual

A TDD-discipline skill that enforces RED → GREEN → REFACTOR with a mandatory watch-it-fail step before any production code is written.

## What It Does

Enforces the Iron Law:

> **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**

A 7-step cycle gates every production-code commit.

1. **RED** — Write a minimal failing test for one behavior (no production code yet).
2. **Verify RED** — Watch the test fail for the **expected** reason. This step is mandatory.
3. **GREEN** — Write the simplest production code that makes the test pass.
4. **Verify GREEN** — The new test and the broader suite both pass.
5. **REFACTOR** — Improve names / remove duplication while the suite stays green.
6. **Verify after REFACTOR** — All tests still pass.
7. Loop with the next behavior, or hand off to `ywc-verify-done`.

The "code first, tests later" pattern is blocked because tests written after the code pass on first run — you never see them catch a defect, so you cannot trust them to catch one in the future.

## When It Triggers

- User says "TDD", "test first", "테스트 먼저", "RED-GREEN".
- Implementing any new feature, bug fix, or behavior change.
- `ywc-code-gen --tdd` delegates here.
- `ywc-debug-rootcause` Phase 4 §1 needs a regression test.

## When NOT to Use

- The user has explicitly opted out for a throwaway prototype this turn.
- Investigating an existing test failure → `ywc-debug-rootcause`.
- Generated code / config files.
- Completion-claim verification → `ywc-verify-done` (TDD is the writing discipline; verify-done is the claiming discipline).

## References

Full cycle rules, Rationalization Defense, and output format are in [SKILL.md](./SKILL.md). Underlying discipline is adapted from `superpowers:test-driven-development`, tightened to hand off claims to `ywc-verify-done` and route investigation to `ywc-debug-rootcause`.

## Localized Versions

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
