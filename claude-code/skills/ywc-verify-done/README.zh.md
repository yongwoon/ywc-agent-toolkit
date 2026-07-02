<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-verify-done

一个流程纪律 Skill，在任何完成声明之前强制要求提供新鲜的验证 evidence。

## 它的作用

在发出任何完成声明——"work done"、"tests pass"、"build succeeds"、"bug fixed"、"requirements met"——之前立即调用此 Skill。它强制执行一个 5 步 Gate Function：

1. **IDENTIFY** — 指明能证明该声明的确切 shell 命令。
2. **RUN** — **在当前 message 中**重新执行该命令。
3. **READ** — 读取完整输出和 exit code。
4. **VERIFY** — 确认输出支持该声明的确切措辞。
5. **CLAIM** — 仅在步骤 1–4 之后，将声明**连同验证块一起**发出。

未经验证的断言词汇（"should"、"probably"、"seems"）会被阻止。

## 何时触发

- 用户示意完成（"완료"、"done"、"完了"）。
- 就在 commit、PR 创建或 merge 之前。
- 就在 executor 转入下一个 task 之前。
- 在收到 subagent 返回负载之后立即。

## 何时不使用

- 在活跃的实现草拟期间 → `ywc-code-gen`
- 对某个 bug 的 root-cause 调查 → `ywc-debug-rootcause`
- 实现前的 confidence 检查 → `ywc-confidence-gate`（计划中）
- 规划前的 codebase 探索 → `ywc-plan`

## 参考

关于完整的规则集、output format 和 Rationalization Defense，请参见 [SKILL.md](./SKILL.md)。其底层纪律改编自 `superpowers:verification-before-completion`。

## 本地化版本

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
