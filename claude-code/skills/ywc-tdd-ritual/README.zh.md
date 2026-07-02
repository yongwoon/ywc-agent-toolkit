<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-tdd-ritual

一个 TDD 纪律 Skill，在编写任何 production code 之前强制执行 RED → GREEN → REFACTOR，并要求一个必须的 watch-it-fail 步骤。

## What It Does

强制执行 Iron Law：

> **没有先失败的 test 就没有 production code**

一个 7 步循环把关每一次 production-code commit。

1. **RED** —— 为一个 behavior 编写一个最小的失败 test（尚无 production code）。
2. **Verify RED** —— 观察 test 因**预期的**原因失败。此步骤是必须的。
3. **GREEN** —— 编写让 test 通过的最简单 production code。
4. **Verify GREEN** —— 新 test 和更广的 suite 都通过。
5. **REFACTOR** —— 在 suite 保持绿色的同时改进命名 / 移除重复。
6. **Verify after REFACTOR** —— 所有 tests 仍然通过。
7. 用下一个 behavior 继续循环，或交接给 `ywc-verify-done`。

"code first, tests later" 模式被阻止，因为在 code 之后编写的 tests 会在首次运行时通过 —— 你从未见过它们捕获缺陷，所以你无法信任它们将来能捕获缺陷。

## When It Triggers

- 用户说 "TDD"、"test first"、"테스트 먼저"、"RED-GREEN"。
- 实现任何新 feature、bug fix 或 behavior 变更。
- `ywc-code-gen --tdd` 委托到这里。
- `ywc-debug-rootcause` Phase 4 §1 需要一个 regression test。

## When NOT to Use

- 用户已明确选择在本轮为一次性 prototype 退出。
- 调查一个已存在的 test failure → `ywc-debug-rootcause`。
- 生成的 code / config 文件。
- Completion-claim 验证 → `ywc-verify-done`（TDD 是编写纪律；verify-done 是声明纪律）。

## References

完整的循环规则、Rationalization Defense 和 output format 见 [SKILL.md](./SKILL.md)。底层纪律改编自 `superpowers:test-driven-development`，并加以收紧，使声明交接给 `ywc-verify-done`，将调查路由到 `ywc-debug-rootcause`。

## Localized Versions

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
