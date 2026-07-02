<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-confidence-gate

一个实现前的纪律性 skill，它强制给出明确的 5 维度置信度评分，并在调用任何实现工具之前呈现 PROCEED / REVIEW / STOP 决策。

## 它做什么

强制执行 Iron Law：

> **没有明确的置信度评分和 band 决策，就不得实现**

对 5 个维度评分（各 0–100），取加权和，并映射到一个 band。

| Dimension | Weight | One-sentence test |
|---|---|---|
| Scope clarity | 25% | 你能否用一句话分别陈述 in-scope 和 out-of-scope，且不使用含糊的术语？ |
| Architecture compliance | 25% | 计划中的变更是否遵循现有的结构 / 命名 / abstractions？ |
| Evidence quality | 20% | 主张是否有一手来源（code、official docs、test output）支撑？ |
| Reuse verified | 15% | 你是否搜索过现有的 utilities，并逐一给出排除的理由？ |
| Root cause identified | 15% | Bug：你说出的是原因而非症状吗？Greenfield：是底层需求而非表面请求吗？ |

| Band | Aggregate | Action |
|---|---|---|
| **PROCEED** | ≥ 90 | 开始实现；将评分带入 executor report |
| **REVIEW** | 70–89 | 提出 1–3 个备选方案或未决问题；先提出最弱的维度 |
| **STOP** | < 70 | 不要开始；揭示薄弱维度并路由回上游 skill |

**单维度 `< 50` 覆盖规则**：加权和先确定一个初步 band，然后任何单个维度评分低于 50 会将其下调一级（PROCEED → REVIEW，REVIEW → STOP）—— 始终只下调一级，绝不会直接跳到 STOP，且恰好为 50 的维度不会触发它。这可防止某个强维度掩盖致命的弱点。

## 何时触发

- 用户说 "ready to implement"、"should I proceed"、"confidence check"、"確信度チェック"、"구현 시작해도 돼"。
- `ywc-code-gen`、`ywc-sequential-executor`、`ywc-parallel-executor`、`ywc-agentic` 的边界入口。
- 在 `ywc-plan` Scale 评估之后，紧接在下游移交之前。
- 在任何具有实质性 architectural 影响的 commit 之前。

## 何时不使用

- 实现后验证 → `ywc-verify-done`（使用相同 rubric 的对称 gate）
- Spec 质量审查 → `ywc-spec-validate`
- 实现审查评分 → `ywc-impl-review`（也使用此 rubric —— 评分可比较）
- 意图澄清 → `ywc-brainstorm`

## 参考

完整工作流和 anti-patterns 见 [SKILL.md](./SKILL.md)。规范的 rubric 定义是共享参考 [../references/confidence-gate.md](../references/confidence-gate.md)。该 skill 借鉴了 ECC 的 confidence-check 模式和 SuperClaude 的 PM Agent rubric。

## 本地化版本

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
