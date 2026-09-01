<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-braystorm

一种苏格拉底对话式技能，将粗略的想法转化为获得批准的设计，然后再开始任何实现工作。

## 它的功能

强制执行硬关:

> **在设计方案被提出并且用户批准之前，不允许进行任何实现工作、规范草拟或代码编写。**

一个6步对话工作流：

1. **步骤 1 — 探索项目背景** — 阅读受影响区域的 `CLAUDE.md`、`docs/` 和最近的提交，防止过时的假设。
2. **步骤 2 — 检测"一个设计无法容纳"的情况** — 如果请求跨越多个独立的子系统，停止并首先分解。
3. **步骤 3 — 逐个提出澄清问题** — 浮出四个锚点（What / Why / Out of Scope / Done When），每条消息一个问题。
4. **步骤 4 — 提出 2-3 种方法及其权衡** — 以建议开头；明确展示替代方案，并浮出值得在建议之前验证的假设。
5. **步骤 5 — 呈现设计并获得批准** — 分部分呈现；当设计依赖于存储库事实时，显示一个带有引用 `file:line` 证据的"加载承载前提"表，并且当任何行为 `UNVERIFIED` 时不要要求交接。
6. **步骤 6 — 交接给 `ywc-plan`** — 将锚点和选定的方法作为显式输入传递。

该技能永远不会直接分支到 `ywc-code-gen`、`ywc-spec-writer`、`ywc-task-generator` 或任何执行器 — 其终端状态始终是调用 `ywc-plan`。

## 何时触发

- 用户说"idea"、"brainstorm"、"let's build"、"アイディア"、"구상"等类似表述。
- 意图不明确或实现可能有多种方式。
- 请求似乎跨越多个子系统。
- `ywc-plan` 第1步将澄清对话委派到这里。

## 何时不使用

- 请求已指定文件路径和验收标准 → 直接使用 `ywc-plan`
- 验证现有规范 → `ywc-spec-validate`
- 在库或框架之间选择 → 先使用 `ywc-tech-research`
- 实现时问题 → `ywc-code-gen`

## 参考资源

完整工作流和论证防守在 [SKILL.md](./SKILL.md) 中。基础学科改编自 `superpowers:brainstorming`，更紧密地交接给 `ywc-plan`。盲点表面化在内部使用 [../references/unknown-matrix.md](../references/unknown-matrix.md)。

## 本地化版本

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
