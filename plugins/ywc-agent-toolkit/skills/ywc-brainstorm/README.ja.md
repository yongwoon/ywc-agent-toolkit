# ywc-brainstorm

実装着手前に、ユーザーの rough idea を承認済み design に変換する Socratic dialogue skill です。

## 何をするか

次の Hard Gate を強制します:

> **NO IMPLEMENTATION SKILL, SPEC DRAFTING, OR CODE WRITING UNTIL A DESIGN IS PRESENTED AND THE USER HAS APPROVED IT.**

6 段階の dialogue workflow:

1. **Step 1 — Explore project context** — 影響範囲の `CLAUDE.md`、`docs/`、最近の commit を先に読み、古い前提を持ち込まない
2. **Step 2 — Detect "too big for one design"** — 複数の独立 subsystem が混在する場合は STOP し、decomposition を先に協議
3. **Step 3 — Ask clarifying questions one at a time** — What / Why / Out of Scope / Done When の 4 anchor を 1 メッセージ 1 質問で surface
4. **Step 4 — Propose 2–3 approaches with trade-offs** — 推奨案 1 + 代替案 1〜2、それぞれの trade-off を明示
5. **Step 5 — Present the design and get approval** — Section ごとに確認、最後に明示的な handoff 承認
6. **Step 6 — Handoff to `ywc-plan`** — 4 anchor と選択した approach を `ywc-plan` の入力として渡す

この skill は `ywc-code-gen`、`ywc-spec-writer`、`ywc-task-generator`、executor へ直接分岐しません — terminal state は常に `ywc-plan` の呼び出しです。

## いつ trigger されるか

- ユーザーが「アイディア」「構想」「ブレスト」「brainstorm」などを言及した時
- 意図が不明確で、実装方針が複数あり得る時
- 要求が複数の subsystem にまたがっていそうな時
- `ywc-plan` の Step 1 が clarification を委任してきた時

## 使わない場面

- 要求がすでに file path・acceptance criteria まで具体的 → `ywc-plan` を直接
- 既存 spec の quality validation → `ywc-spec-validate`
- Library / framework の選択 → `ywc-tech-research` を先に
- 実装中の質問 → `ywc-code-gen`

## 参考

詳細な workflow と Rationalization Defense は [SKILL.md](./SKILL.md) を参照してください。元の process discipline は `superpowers:brainstorming` を ywc の handoff (→ ywc-plan) に合わせて調整しています。

## Localized Versions

- [한국어 (default)](./README.md)
- [English](./README.en.md)
- [한국어 (full)](./README.ko.md)
