# ywc-design-renew

平凡な、あるいは「LLM が作ったような(AI slop)」Frontend 画面を distinctive な
デザインへ renew し、同時に AI-slop tell を点検する Claude Code Skill です。
`impeccable` skill が install されていれば design engine として委譲し、無ければ
自前の内蔵 ruleset で動作するため、どの project / runtime でも機能します。

## 概要

LLM が生成した画面は同一 template で学習されているため、cyan-on-dark palette、
gradient text、border-left stripe、Inter font、均一な card grid といった予測可能な
視覚的 cliché に収束します。この Skill はその「AI slop」signal を検出(check)し、
除去(renew)します。

- **renew mode (default)**: 既存画面を受け取り bold な aesthetic direction へ改善し、
  before/after の evidence を残します。
- **check mode**: 編集せず AI-slop 点検のみ行い、pass/fail gate を適用します。

判定の軸は **AI Slop Test** です — 「この画面を見せて『AI が作った』と言ったら、
即座に信じるか?」

## 事前準備

- (任意) `impeccable` skill — あれば強力な design engine として委譲、無ければ自前
  ruleset に fallback。**install (いずれか)**: Claude Code で
  `/plugin marketplace add pbakaus/impeccable`、または `npx impeccable skills install`。
  install 後に `/impeccable init` を 1 回実行すると project の Design Context が設定され、
  下記の `PRODUCT.md` / `DESIGN.md` が生成されて再質問が省略されます。
- (任意) Live URL (local dev server) — before/after screenshot 用の Chrome DevTools
  MCP 探索に使用。
- (任意) `.impeccable.md` / `PRODUCT.md` / `DESIGN.md` — Design Context が既にあれば
  再質問を省略。

## 利用シナリオ

- 「この dashboard のデザインが平凡で、LLM が作ったみたい。renew して。」
- 「release 前に、この画面に AI-slop の signal が無いか点検して。」
- 「Hero section を distinctive に再デザインして。」

## 使い方

```bash
/ywc-design-renew --target src/components/hero --url http://localhost:3000
/ywc-design-renew --mode check --target src/app/dashboard --fail-on critical
```

または自然言語で呼び出し:

> 「この画面、AI が作ったように見える。デザインを renew して。」

## 入力

- **必須**: `--target` (component / page / route) と Design Context
  (audience / use-cases / brand tone)
- **任意**: `--url` (live screenshot)、`--mode check`、`--fail-on`、`--format html`

## 出力

- **renew**: renew した code と renewal report (選択した direction、解消した slop
  finding の before→after、変更 file、再検証結果、before/after screenshot)
- **check**: 優先度(Critical / High / Medium / Low)別 slop audit report と
  `--fail-on` gate の判定

## 関連 Skill

- `impeccable` — install 時に design engine として委譲 (craft / polish / audit)
- `ywc-ui-ux-review` — renew 後の usability / IA / WCAG 軸を検証 (この Skill は
  美観 / slop 軸のみ担当)
- `ywc-review-learnings` — renew 中に確定したデザイン選好を project 単位で蓄積
