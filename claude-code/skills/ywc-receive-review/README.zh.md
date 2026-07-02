<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-receive-review

一个态度层的纪律 skill，在接收 code-review 反馈时**阻止表演性的附和并强制进行技术验证**。

## 它做什么

强制执行 Iron Law：

> **VERIFY BEFORE IMPLEMENTING. NO PERFORMATIVE AGREEMENT, EVER.**

一个 6 步 Response Pattern 适用于每一条 reviewer 评论：

1. **READ**——阅读完整反馈而不作反应（暂不附和、不反对、不调用工具）。
2. **UNDERSTAND**——用你自己的话重述技术需求；在推进之前询问任何不清楚的条目。
3. **VERIFY**——打开文件、运行 test、grep 符号——对照当前 codebase 核对 reviewer 的主张。
4. **EVALUATE**——判断该建议在当前状态下是否适用于此 codebase（兼容性、先前的决策、YAGNI、平台约束）。
5. **RESPOND**——用一句修复说明来确认，或用技术推理来反驳。**禁止**："You're absolutely right!"、"Great point!"、"Thanks!"
6. **IMPLEMENT**——一次一个条目，逐个 test，按 `ywc-verify-done` 呈现一个验证块。

**禁用词汇**（完整列表见 references/forbidden-acknowledgments.md）：

| Forbidden | Replace with |
|---|---|
| "You're absolutely right!" | 陈述修复："Fixed — `<file:line>` now <behavior>" |
| "Great point!" / "Excellent feedback!" | 陈述行动或提出问题 |
| "Thanks for catching that!" / "Thanks for the review!" | 完全删除；修复本身就是感谢 |
| "Let me implement that right now"（在 Step 3 之前） | "Verifying before implementing: <check>" |

## 何时触发

- 用户说 "리뷰 받았어"、"review feedback"、"コメント返信"。
- `ywc-handle-pr-reviews` 在 inline-comment 迭代期间委托态度层。
- `ywc-finish-branch` 呈现一个需要响应的 post-CI bot review。
- 即将响应 CodeRabbit / Codex Review / Claude Review。

## 何时不要使用

- 你自己执行 review → `ywc-impl-review`
- 创建 PR → `ywc-create-pr`
- 自动化获取 / 线程化 / 回复 PR 评论 → `ywc-handle-pr-reviews`（此 skill 是其态度层）
- 完成声明验证 → `ywc-verify-done`

## References

完整的 Response Pattern、禁用附和列表、pushback 条件以及特定来源的处理（human partner / external reviewer / bot）都在 [SKILL.md](./SKILL.md) 中。改编自 `superpowers:receiving-code-review`，为与 `ywc-handle-pr-reviews` 的关注点分离而调整（态度 vs. 自动化）。

## 本地化版本

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
