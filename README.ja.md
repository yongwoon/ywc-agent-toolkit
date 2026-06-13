# ywc-agent-toolkit

> この文書は現在翻訳中です。完全なドキュメントは [English](README.md) をご覧ください。
>
> 翻訳にご協力いただける方は [Translation Issue](../../issues/new?template=translation.md) を作成してください。

---

Claude Code および Codex 向けの開発ワークフロー自動化スキル集です。
計画立案・仕様書作成・タスク分解・コード生成・レビュー・リリースまでをカバーします。

現在、Claude Code skill 36 個、Codex skill 37 個、Claude Code agent 12 個、Codex custom agent 7 個を提供しています。

## 前提条件

プラグインマーケットプレイスおよび Codex プラグインのインストールには **前提条件なし** — ツールがすべて自動処理します。

**bash スクリプト fallback** を使用する場合、`install.sh` を実行する前に以下が必要です:

| ツール | 必要な理由 | インストール |
| ------ | ---------- | ------------ |
| `git` | リポジトリのクローン | ほとんどのシステムにプリインストール済み |
| `bash ≥ 3.2` | `install.sh` の実行 | macOS / Linux にプリインストール済み |
| `jq` | フック登録 | `brew install jq` / `apt-get install jq` |

**スキルランタイム**（インストール時には不要）:

| ツール | 使用スキル | インストール |
| ------ | ---------- | ------------ |
| `python3 ≥ 3.9` | `ywc-parallel-executor`, `ywc-finish-branch`, `ywc-merge-dependabot` | macOS 12.3+ にプリインストール済み; `brew install python3` |
| `gh` CLI | Git & Release スキルの大部分 | `brew install gh` / [cli.github.com](https://cli.github.com) |

---

## インストール

### Claude Code プラグインマーケットプレイス（推奨）

```bash
# マーケットプレイスソースを追加（初回のみ）
/plugin marketplace add yongwoon/ywc-agent-toolkit
```

コマンド実行後、Plugin UI の **Marketplaces** タブから **ywc-agent-toolkit** をインストールしてください。
クローンや bash 不要で `~/.claude/skills/` に自動インストールされます。

### Codex CLI プラグインディレクトリ

このリポジトリには、Codex プラグイン配布用のパッケージングメタデータが [`.codex-plugin/`](.codex-plugin/) に含まれています。プラグインローカルの skill は `.codex-plugin/skills/` にミラーされ、`bash scripts/validate.sh` で鮮度が検証されます。これは Codex CLI/App でのプラグインインストールに備えるもので、公式 Codex マーケットプレイスに既に掲載されていることを意味しません。

このリポジトリを含む Codex プラグインマーケットプレイスまたはソースが利用可能になったら:

```text
# Shell
codex

# 対話型 Codex セッション内で
/plugins
```

対話型 Codex セッション内でプラグインディレクトリを開き、`yongwoon/ywc-agent-toolkit` の **ywc-agent-toolkit** を検索して、**Install plugin** を選択してください。

### Codex App Plugins サイドバー

Codex App では、サイドバーの **Plugins** を開き、**ywc-agent-toolkit** を検索または参照し、プラグインソースが `yongwoon/ywc-agent-toolkit` であることを確認してから、プラグイン詳細画面でインストールしてください。

このリポジトリが利用可能な Codex プラグインソースに表示されるまでは、下の bash fallback を使用してください。

### bash スクリプト fallback

```bash
YWC_REF=<release-tag-or-reviewed-commit>
git clone --branch "$YWC_REF" --depth 1 https://github.com/yongwoon/ywc-agent-toolkit.git
cd ywc-agent-toolkit
git remote get-url origin
git rev-parse --verify HEAD

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

9 つの Review / Report skill が opt-in の `--format html` flag をサポートします。Markdown の代わりに、ブラウザでそのまま開ける self-contained な HTML report を生成します。

**対応 Skill:** `ywc-impl-review`, `ywc-security-audit`, `ywc-spec-validate`, `ywc-tech-research`, `ywc-incident-postmortem`, `ywc-product-review`, `ywc-ui-ux-review`, `ywc-gen-testcase`, `ywc-design-renew`

**導入の背景:** AI が生成した 100 行を超える Markdown ドキュメントは最後まで読まれない傾向があり、読まれない report は意思決定につながりません。HTML は色、severity coding、tab、インタラクティブな control（チェックボックス、`Copy as Markdown`）を加えることで、受け手が実際に読んで行動できるようにします。

```bash
/ywc-impl-review --spec docs/spec.md --code src/ --format html
/ywc-gen-testcase 250 --format html   # localStorage でサインオフ状態を保持するインタラクティブなテストシート
```

> **⚠️ Token コスト** — HTML 出力は Markdown と比べて output token を 2〜4 倍消費し、生成時間も長くなります。デフォルトは `markdown` です。人がブラウザで読む report に限って HTML を有効化してください。

---

## Custom Agent

Claude Code には worker / reviewer / specialist dispatch 用の **12 個**の custom agent が含まれています。`~/.claude/agents/` にインストールされます。詳細は [`claude-code/agents/README.md`](claude-code/agents/README.md) をご参照ください。

Codex には `ywc-*` skill を補完する **7 個**の read-only specialist agent が含まれます。`~/.codex/agents/` にインストールされます。

| Agent | 用途 | Sandbox |
|-------|------|---------|
| `ywc-architect` | アーキテクチャ決定・トレードオフ advisor | `read-only` |
| `ywc-security-engineer` | 静的セキュリティレビューと threat model 分類 | `read-only` |
| `ywc-root-cause-analyst` | 根本原因・障害原因の分析 | `read-only` |
| `ywc-performance-engineer` | パフォーマンスレビューとプロファイリング推奨 | `read-only` |
| `ywc-typescript-reviewer` | TypeScript / JavaScript 言語特化レビュー | `read-only` |
| `ywc-python-reviewer` | Python 言語特化レビュー | `read-only` |
| `ywc-go-reviewer` | Go 言語特化レビュー | `read-only` |

詳細は [README.md](README.md) をご参照ください。
