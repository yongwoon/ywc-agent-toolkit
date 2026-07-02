<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-design-renew

一个 Claude Code Skill，将通用或"AI 制造"（AI-slop）的 frontend 界面翻新
为独具特色的设计，并审计 UI 中的 AI-slop 设计特征。当已安装 `impeccable`
skill 时，它会委派给该 skill 作为设计引擎；否则回退到自包含的规则集 —
因此它可在任何项目或 runtime 中工作。

## 概述

LLM 生成的 UI 会趋同于可预测的视觉套路 — cyan-on-dark 配色、
渐变文字、border-left 强调条纹、Inter 字体、统一的 card 网格 — 因为
每个 model 都在相同的模板上训练。此 skill 检测（check）并
移除（renew）这些 AI-slop 信号。

- **renew mode（默认）**：接收现有界面，将其改进为大胆的
  美学方向，并留下 before/after 证据。
- **check mode**：审计 AI-slop 而不进行编辑，应用 pass/fail gate。

锚定标准是 **AI Slop Test** — "如果你展示这个并说
'AI made this'，他们会立刻相信你吗？"

## 前置条件

- （可选）`impeccable` skill — 存在时被委派为更强的设计引擎；
  否则回退到自包含规则集。**安装（任选其一）**：在
  Claude Code 中运行 `/plugin marketplace add pbakaus/impeccable`，或
  `npx impeccable skills install`。安装后，运行一次 `/impeccable init`
  来设置项目 Design Context — 它会写入下面的 `PRODUCT.md` / `DESIGN.md`
  文件，从而跳过 context 问题。
- （可选）一个实时 URL（本地 dev server）— 由 Chrome DevTools MCP 用于
  before/after 截图。
- （可选）`.impeccable.md` / `PRODUCT.md` / `DESIGN.md` — 当 Design Context
  已存在时跳过 context 收集问题。

## 使用场景

- "This dashboard looks too generic, like an AI made it. Renew it."
- "Before release, check this screen for AI-slop design tells."
- "Redesign the hero section to feel distinctive."

## 使用方法

```bash
/ywc-design-renew --target src/components/hero --url http://localhost:3000
/ywc-design-renew --mode check --target src/app/dashboard --fail-on critical
```

或用自然语言调用：

> "This screen looks AI-generated. Please renew the design."

## 输入

- **必填**：`--target`（component / page / route）以及 Design Context
  （audience / use-cases / brand tone）
- **可选**：`--url`（实时截图）、`--mode check`、`--fail-on`、
  `--format html`

## 输出

- **renew**：翻新后的代码以及一份翻新报告（所选方向、已解决的 slop
  findings 的 before→after、更改的文件、重新审计结果、before/after
  截图）
- **check**：一份按优先级排序（Critical / High / Medium / Low）的 slop 审计报告
  以及 `--fail-on` gate 判定

## 相关 Skills

- `impeccable` — 已安装时被委派的设计引擎（craft / polish / audit）
- `ywc-ui-ux-review` — 在翻新后验证 usability / IA / WCAG 维度
  （此 skill 只负责 aesthetic / slop 维度）
- `ywc-review-learnings` — 按项目累积已确认的设计偏好
