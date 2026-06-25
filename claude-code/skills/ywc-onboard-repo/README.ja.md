# ywc-onboard-repo

既存または初見の Repository に入る際、4-Phase (Reconnaissance → Architecture → Conventions → Generate) で Onboarding Guide と Starter CLAUDE.md を生成する Skill です。新規 Repository の scaffolding ではなく、`ywc-project-scaffold` の inverse direction として位置づきます。Reconnaissance は Glob + Grep のみで実施し、token cost を抑制します。

## Localized Versions

- [한국어 (entry)](./README.md)
- [English](./README.en.md)
- [한국어](./README.ko.md)

## 使うべき場面

- User が「onboard me」「このリポ初めて」「コードベースを案内して」と言及した場合
- 新規 Project に Claude Code を初期設定する場合 (Starter CLAUDE.md 生成)
- Subagent runner が implementation 委任の前に CLAUDE.md を必要とする場合

## 起動方法

```bash
/ywc-onboard-repo --scope apps/web/
```

または自然言語で:

> 「このリポを onboard して」
> 「既存の convention から CLAUDE.md を生成して」

## Iron Law

1. **Reconnaissance は Glob + Grep のみ** — Read は ambiguous signal が出た場合のみ
2. **Code から検証された convention が config から推定された convention より優先**
3. **既存 CLAUDE.md は in-place の enhancement のみ**、overwrite は禁止

## 入力

- (optional) `--scope <dir>` — monorepo の特定 workspace のみ reconnaissance
- (optional) `--guide-only` — Onboarding Guide のみ出力、CLAUDE.md は skip
- (optional) `--claude-md-only` — CLAUDE.md のみ生成、Guide は skip
- (optional) `--enhance` — 既存 CLAUDE.md がなくても enhancement path を強制

## 出力

- **Output A**: Onboarding Guide (Conversation に Markdown で出力) — Tech Stack, Architecture, Key Entry Points, Directory Map, Request Lifecycle, Conventions, Common Tasks, Where to Look, Detection Confidence
- **Output B**: Starter CLAUDE.md (repo root に write) — 既存 file があれば `## Detected Conventions (<YYYY-MM-DD>)` section のみ追記。既存の `AGENTS.md` (vendor-neutral 標準) / `.cursorrules` があれば一緒に Read して reconcile — 生成した CLAUDE.md がそれと矛盾しないようにする (AGENTS.md の emit は Codex variant の担当、意図的な divergence)

## 関連 Skill

- `ywc-project-scaffold` — inverse direction (新規 repo 作成)。同一 session 内で両方を呼ぶことは禁止
- `ywc-refactor-clean` — reconnaissance が dead-code accumulation を検出した場合の follow-up PR routing 先
- `ywc-impl-review` — 生成された Onboarding Guide が cold reviewer の anchor になる
- `ywc-plan` — Phase 2 の Request Lifecycle が plan Step 2 の architectural anchor
- `ywc-verify-done` — 最終 "Wrote CLAUDE.md" claim の vocabulary 規則を提供
