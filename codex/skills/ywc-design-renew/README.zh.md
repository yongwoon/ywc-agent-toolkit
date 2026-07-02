<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-design-renew

一个 Codex Skill，用于把通用或“AI 生成感”很强的 Frontend 界面更新为更有辨识度的设计，并审计 UI 中的 AI-slop 设计痕迹。安装了 `impeccable` 时会把它作为更强的 design engine；否则使用内置规则集，因此可在任何项目或 runtime 中工作。

## 概览

LLM 生成的 UI 常收敛到可预测的视觉套路：深色背景上的青色、gradient text、左侧 accent border、Inter、统一 card grid 等。本 Skill 用来检测并移除这些信号。

- **renew mode（默认）**：接收现有 surface，朝更明确的美学方向改进，并留下 before/after 证据。
- **check mode**：只审计 AI-slop，不修改文件，并应用 pass/fail gate。

核心判断标准是 **AI Slop Test**：“如果把这个界面展示给别人并说它是 AI 做的，对方会不会马上相信？”

## 前置条件

- （可选）`impeccable` Skill：可作为更强的 design engine。项目支持时可用 `npx impeccable skills install` 安装。安装后运行一次 `impeccable init` 写入 `PRODUCT.md` / `DESIGN.md`，之后可跳过 Design Context 问题。
- （可选）live URL（local dev server）：用于 Chrome DevTools MCP 的 before/after screenshots。
- （可选）`.impeccable.md` / `PRODUCT.md` / `DESIGN.md`：已有 Design Context 时跳过上下文收集。

## 使用场景

- “这个 dashboard 太通用，像 AI 做的。请更新它。”
- “发布前检查这个 screen 是否有 AI-slop 设计痕迹。”
- “重新设计 hero section，让它更有辨识度。”

## 用法

```text
Use $ywc-design-renew to renew src/components/hero with --url http://localhost:3000.
Use $ywc-design-renew --mode check --target src/app/dashboard --fail-on critical.
```

也可以用自然语言调用：

> “This screen looks AI-generated. Please renew the design.”

## 输入

- **必需**：`--target`（component / page / route）和 Design Context（audience / use-cases / brand tone）
- **可选**：`--url`（live screenshots）、`--mode check`、`--fail-on`、`--format html`

## 输出

- **renew**：更新后的 code，以及 renewal report（chosen direction、before→after 已解决的 slop findings、changed files、re-audit result、before/after screenshots）
- **check**：按 Critical / High / Medium / Low 排序的 slop audit report，以及 `--fail-on` gate verdict

## 相关 Skills

- `impeccable` — 安装时作为 delegated design engine（craft / polish / audit）
- `ywc-ui-ux-review` — renewal 后验证 usability / IA / WCAG 轴；本 Skill 只负责 aesthetic / slop 轴
- `ywc-review-learnings` — 累积项目确认过的 design preferences
