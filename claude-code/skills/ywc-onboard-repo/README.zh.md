# ywc-onboard-repo

一个 4 阶段（Reconnaissance → Architecture → Conventions → Generate）skill，用于进入既有或陌生的 repository。它向 conversation 输出 Onboarding Guide，并在 repo root 写入 Starter CLAUDE.md，对任何既有 CLAUDE.md 进行原地增强。它**不是** scaffolder — `ywc-project-scaffold` 是相反方向。Reconnaissance 仅使用 Glob + Grep 以控制 token 成本。

## 本地化版本

- [한국어 (entry)](./README.md)
- [English](./README.en.md)
- [日本語](./README.ja.md)
- [Español](./README.es.md)

## 何时使用

- 用户说 "onboard me"、"带我了解这个 repo"、"帮我理解这个 codebase"
- 首次在项目中配置 Claude Code（生成 Starter CLAUDE.md）
- subagent runner 在委派实现前需要一个 CLAUDE.md

## 如何调用

```bash
/ywc-onboard-repo --scope apps/web/
```

或使用自然语言：

> "onboard me to this repo"
> "根据既有约定生成 CLAUDE.md"

## 铁律

1. **Reconnaissance 仅使用 Glob + Grep** — Read 仅保留给后续阶段暴露的歧义信号
2. **从源代码验证的约定优先于从 config 推断的约定**
3. **既有 CLAUDE.md 原地增强** — 绝不覆盖

## 输入

- （可选）`--scope <dir>` — 将 reconnaissance 限定到某个 workspace（在 monorepo 中有用）
- （可选）`--guide-only` — 仅输出 Onboarding Guide，跳过 CLAUDE.md
- （可选）`--claude-md-only` — 仅写入 CLAUDE.md，跳过 Guide
- （可选）`--enhance` — 即使尚无 CLAUDE.md 也强制走增强路径

## 输出

- **Output A**: Onboarding Guide（打印的 Markdown）— Tech Stack, Architecture, Key Entry Points, Directory Map, Request Lifecycle, Conventions, Common Tasks, Where to Look, Detection Confidence
- **Output B**: Starter CLAUDE.md（写入 repo root）— 若已存在 CLAUDE.md，仅追加 `## Detected Conventions (<YYYY-MM-DD>)` 部分。若存在 `AGENTS.md`（vendor-neutral 标准）/ `.cursorrules`，会一并 Read 并 reconcile，使生成的 CLAUDE.md 不与其矛盾（emit AGENTS.md 是 Codex variant 的职责 — 有意的 divergence）

## 相关 Skills

- `ywc-project-scaffold` — 相反方向（创建新 repo）；切勿在一个 session 中同时调用两者
- `ywc-refactor-clean` — 当 reconnaissance 揭示大量 dead-code 累积时的 downstream
- `ywc-impl-review` — 生成的 Onboarding Guide 为冷启动 reviewer 提供锚点
- `ywc-plan` — 第 2 阶段的 Request Lifecycle 是 plan Step 2 消费的架构锚点
- `ywc-verify-done` — 最终 "Wrote CLAUDE.md" 声明的词汇规则
