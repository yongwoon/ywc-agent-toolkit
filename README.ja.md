# ywc-agent-toolkit

> この文書は現在翻訳中です。完全なドキュメントは [English](README.md) をご覧ください。
>
> 翻訳にご協力いただける方は [Translation Issue](../../issues/new?template=translation.md) を作成してください。

---

Claude Code および Codex 向けの開発ワークフロー自動化スキル集です。
計画立案・仕様書作成・タスク分解・コード生成・レビュー・リリースまでをカバーします。

現在、Claude Code skill 26 個と Codex skill 27 個を提供しています。

## インストール

### Claude Code プラグインマーケットプレイス（推奨）

```bash
# マーケットプレイスソースを追加（初回のみ）
/plugin marketplace add yongwoon/ywc-agent-toolkit
```

コマンド実行後、Plugin UI の **Marketplaces** タブから **ywc-agent-toolkit** をインストールしてください。
クローンや bash 不要で `~/.claude/skills/` に自動インストールされます。

### bash スクリプト

```bash
git clone https://github.com/yongwoon/ywc-agent-toolkit.git
cd ywc-agent-toolkit

# Claude Code
bash scripts/install.sh --cc

# Codex
bash scripts/install.sh --codex

# 両方
bash scripts/install.sh --all
```

詳細は [README.md](README.md) をご参照ください。

---

## Review Skill HTML 出力モード

8 つの Review / Report skill が opt-in の `--format html` flag をサポートします。Markdown の代わりに、ブラウザでそのまま開ける self-contained な HTML report を生成します。

**対応 Skill:** `ywc-impl-review`, `ywc-security-audit`, `ywc-spec-validate`, `ywc-tech-research`, `ywc-incident-postmortem`, `ywc-product-review`, `ywc-ui-ux-review`, `ywc-gen-testcase`

**導入の背景:** AI が生成した 100 行を超える Markdown ドキュメントは最後まで読まれない傾向があり、読まれない report は意思決定につながりません。HTML は色、severity coding、tab、インタラクティブな control（チェックボックス、`Copy as Markdown`）を加えることで、受け手が実際に読んで行動できるようにします。

```bash
/ywc-impl-review --spec docs/spec.md --code src/ --format html
/ywc-gen-testcase 250 --format html   # localStorage でサインオフ状態を保持するインタラクティブなテストシート
```

> **⚠️ Token コスト** — HTML 出力は Markdown と比べて output token を 2〜4 倍消費し、生成時間も長くなります。デフォルトは `markdown` です。人がブラウザで読む report に限って HTML を有効化してください。
