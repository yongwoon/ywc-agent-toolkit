<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-debug-rootcause

一个流程纪律性 skill，针对 bugs、test 失败、build 失败和意外行为，强制**在任何修复之前先识别 root cause**。

## 它做什么

强制执行 Iron Law：

> **在没有先进行 ROOT CAUSE 调查之前，不得修复**

在 Phase 1（Investigation）完成之前，不得提出任何修复。这是一个 4 阶段流程：

1. **Phase 1 — Root-cause 调查** — 完整阅读错误信息，可靠地复现，检查最近的改动，在多组件边界处插桩，沿数据流向上游追溯至源头。
2. **Phase 2 — 模式分析** — 在同一 codebase 中定位一个正常工作的同类实现，端到端阅读它，列出损坏版本与正常版本之间的每一处差异（包括那些"不可能有影响"的差异）。
3. **Phase 3 — 假设与测试** — 形成单一假设，形如"X 是 root cause；最小改动 Z 可修复它"；通过一次只改一个变量来测试。
4. **Phase 4 — 实现** — 编写一个 regression test，应用单一修复，验证 red-green-red，通过 `ywc-verify-done` 对完成主张进行 gate，然后输出系统性预防（§6）：反复出现的类别会被提交给 `ywc-review-learnings --source debug`，一次性的原因则被显式声明。

**如果同一处出现 3 次以上的修复失败**，那么情况是"architecture is wrong"，而非"fix harder"。停止，并将设计问题呈现给用户 —— 不要尝试第 4 次修复。

## 何时触发

- 用户提到 "bug"、"debug"、"왜 안돼"、"落ちる"、"通らない" 或类似表达。
- 一个 test、build 或 type-check 失败。
- 同一处已经有两次或更多的修复尝试失败。
- `ywc-verify-done` 的 failure-routing 表将调查发送到此处。

## 何时不使用

- 正在进行的实现起草 → `ywc-code-gen`
- 事故后回顾 → `ywc-incident-postmortem`
- 安全漏洞分诊 → `ywc-security-audit`
- 实现前置信度检查 → `ywc-confidence-gate`（planned）

## 参考

逐阶段的检查清单、Rationalization Defense 和 architectural-stop 信号见 [SKILL.md](./SKILL.md)。底层准则改编自 `superpowers:systematic-debugging`。

## 本地化版本

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
