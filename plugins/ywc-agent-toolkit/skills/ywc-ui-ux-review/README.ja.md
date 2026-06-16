# UI/UX Review - Hybrid Code & Live UI Auditor

静的 Code 分析と available browser tooling を用いた Live UI 探索を組み合わせ、Project を UI/UX 観点で点検し、優先度別 Markdown report を生成する Codex Skill です。

## 概要

「どこから UX を直すべきか」に evidence ベースで答える Skill です。すべての finding は権威ある heuristic(Nielsen 10 / WCAG 2.2 AA / Material 3 / Apple HIG / Internal Design System)に基づいて citation が付与されます。

### 主な機能

- Hybrid Review: 静的 Code 分析 + Live UI 探索
- 重点 Domain: Information Architecture, Visual Design
- Critical / High / Medium / Low の 4 段階出力
- すべての finding に location と heuristic citation を付与
- available browser tooling の accessibility tree snapshot により Token 効率を確保

## 使用方法

```text
http://localhost:3000 の dashboard を UI/UX review してください。
```

```text
Settings flow の usability と Information Architecture を audit してください。
```

自然言語 Trigger は [SKILL.md](./SKILL.md) に定義されています。

## Reference

- Domain checklist と heuristic citation は [`references/`](./references) にあります
- Report template は [`assets/`](./assets) にあります
- Workflow と Trigger は [SKILL.md](./SKILL.md) にあります

## Live UI Tooling

本 Skill は inspection 中心の作業に available browser tooling を優先使用します(accessibility tree snapshot、Lighthouse audit、computed style、screenshot 等)。Multi-step の interaction 自動化が必要な場合のみ Playwright MCP を補助的に使用します。

## Localized Versions

- [Korean (Primary)](./README.md)
- [English](./README.en.md)
- [Korean (Summary)](./README.ko.md)
