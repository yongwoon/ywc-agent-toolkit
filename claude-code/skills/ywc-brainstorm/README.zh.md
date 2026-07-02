<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-brainstorm

一个采用苏格拉底式对话的 skill，在任何实现工作开始之前，将粗略的想法转化为已获批准的设计。

## 它的作用

强制执行 Hard Gate：

> **在提出设计并获得用户批准之前，不得使用任何实现 SKILL、起草 SPEC 或编写代码。**

一个 6 步对话工作流：

1. **Step 1 — 探索项目 context** — 阅读受影响区域的 `CLAUDE.md`、`docs/` 和近期 commits，以防止过时的假设。
2. **Step 2 — 检测"单一设计过大"** — 如果请求跨越多个独立的子系统，先停止并进行拆解。
3. **Step 3 — 每次只问一个澄清性问题** — 逐一浮现四个锚点（What / Why / Out of Scope / Done When），每条消息只问一个问题。
4. **Step 4 — 提出 2–3 种方案及其权衡** — 以推荐方案为先；明确展示各备选方案。
5. **Step 5 — 呈现设计并获得批准** — 分节呈现；在最终批准 gate 之前逐节确认。
6. **Step 6 — 交接给 `ywc-plan`** — 将锚点和所选方案作为明确的输入传递。

此 skill 绝不会直接分支到 `ywc-code-gen`、`ywc-spec-writer`、`ywc-task-generator` 或任何 executor — 它的终态始终是调用 `ywc-plan`。

## 何时触发

- 用户说 "idea"、"brainstorm"、"let's build"、"アイディア"、"구상" 及类似表述。
- 意图不明确，或实现方式可能有多种走向。
- 请求似乎跨越多个子系统。
- `ywc-plan` Step 1 将澄清对话委派到此处。

## 何时不使用

- 请求已指定文件路径和验收标准 → 直接使用 `ywc-plan`
- 验证现有 spec → `ywc-spec-validate`
- 在库或框架之间做选择 → 先用 `ywc-tech-research`
- 实现阶段的问题 → `ywc-code-gen`

## 参考

完整工作流和 Rationalization Defense 见 [SKILL.md](./SKILL.md)。底层原则改编自 `superpowers:brainstorming`，并收紧为交接给 `ywc-plan`。

## 本地化版本

- [한국어 (default)](./README.md)
- [日本語](./README.ja.md)
- [한국어 (full)](./README.ko.md)
