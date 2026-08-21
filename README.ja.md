# ywc-agent-toolkit

> このドキュメントは現在翻訳中です。全文は [English](README.md) を参照してください。
>
> 翻訳に貢献したい方は [Translation Issue](../../issues/new?template=translation.md) を作成してください。

---

Claude Code および Codex 向けの開発ワークフロー自動化スキル集です。計画立案、仕様書作成、タスク分解、コード生成、レビュー、リリースまでの全工程をカバーします。

[English](README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [Español](README.es.md)

> 📖 **[ドキュメント & ガイドブック](https://yongwoon.github.io/ywc-agent-toolkit-lp/ja/guidebook/)** — この README は概要です。前提条件、インストール、全 skill リファレンス、ステップバイステップのワークフロー解説はガイドブックにあります。

| 知りたいこと | ガイドブックのページ |
| ------------ | -------------------- |
| 5分で最初の機能をリリース | [03. クイックスタート](https://yongwoon.github.io/ywc-agent-toolkit-lp/ja/guidebook/03-quickstart/) |
| どの skill をどの順番で実行するか | [17. 全 Skill リファレンス](https://yongwoon.github.io/ywc-agent-toolkit-lp/ja/guidebook/14-skill-reference/) |
| 前提条件・インストール先・環境変数 | [18. 前提条件とインストール](https://yongwoon.github.io/ywc-agent-toolkit-lp/ja/guidebook/15-prerequisites-installation/) |
| 小規模変更 / 複数タスク / 自律ループ | [04](https://yongwoon.github.io/ywc-agent-toolkit-lp/ja/guidebook/04-general-cycle-small/) · [05](https://yongwoon.github.io/ywc-agent-toolkit-lp/ja/guidebook/05-general-cycle-medium-large/) · [06](https://yongwoon.github.io/ywc-agent-toolkit-lp/ja/guidebook/06-agentic-autonomous-loop/) |

## 対応ツール

| ツール      | Skills | Custom Agents | インストール先                            |
| ----------- | ------ | ------------- | ---------------------------------------- |
| Claude Code | 42     | 12            | `~/.claude/skills/`, `~/.claude/agents/` |
| Codex       | 52     | 8             | `~/.codex/skills/`, `~/.codex/agents/`   |

---

## クイックスタート

### Claude Code

プラグインマーケットプレイスからインストールします — clone も前提条件も不要です:

```bash
/plugin marketplace add yongwoon/ywc-agent-toolkit    # 1. ソースを登録
/plugin install ywc-agent-toolkit@ywc-agent-toolkit   # 2. プラグインをインストール
```

`marketplace add` はソースを登録するだけです。続けて `/plugin install` を実行するか、Plugin UI の **Marketplaces** タブからインストールしてください。インストール後は Claude Code を再起動すると skill が表示されます。

### Codex

```bash
codex plugin marketplace add yongwoon/ywc-agent-toolkit   # 1. ソースを登録
codex plugin add ywc-agent-toolkit@ywc-agent-toolkit      # 2. プラグインをインストール
```

すでにマーケットプレイスを追加済みの場合は、まず `codex plugin marketplace upgrade ywc-agent-toolkit` で Git スナップショットを更新してください。`codex` を実行して `/plugins` を開き、**YWC Agent Toolkit** タブからインストールすることもできます。

**Codex App** をお使いの場合は、サイドバーの **Plugins** を開き、**YWC Agent Toolkit** ソースを選択し、ソースが `yongwoon/ywc-agent-toolkit` であることを確認してから、プラグイン詳細画面でインストールしてください。

### skill を実行する

どちらのツールでも同じコマンドが使えます:

```bash
/ywc-onboard-repo           # 未知のコードベースを数分で把握
/ywc-plan                   # ラフなアイデアを plan または spec に
/ywc-debug-rootcause        # バグの根本原因を追跡
/ywc-impl-review            # spec / セキュリティ / 品質の観点でコードレビュー
/ywc-agentic                # goal ひとつで全 pipeline を自律実行
```

→ 前提条件、bash スクリプト fallback、インストール先、`CLAUDE_SKILLS_DIR` / `CLAUDE_AGENTS_DIR` / `CODEX_HOME` の上書きは [前提条件とインストール](https://yongwoon.github.io/ywc-agent-toolkit-lp/ja/guidebook/15-prerequisites-installation/) を参照してください。

### ガイドブックに含まれないインストールオプション

```bash
# 特定の skill のみインストール
bash scripts/install.sh --cc ywc-plan ywc-commit ywc-create-pr
bash scripts/install.sh --codex ywc-plan ywc-commit ywc-ui-ux-review

# 選択した agent のみ、または agent なしで skill のみ
bash scripts/install.sh --cc-agents ywc-backend-coder ywc-qa-engineer
bash scripts/install.sh --cc --skip-agents
```

### Codex の出力言語デフォルト

Codex 専用の `ywc-setup` は Codex `ywc-*` skill の artifact 言語デフォルトを設定します:

```bash
ywc-setup --scope project --lang ko
ywc-setup --scope user --lang ja
```

解決順序は explicit `--lang` > project `.codex/ywc.json` > project guidance（`AGENTS.md` / `CODEX.md` / `CLAUDE.md`）> user `~/.codex/ywc.json` > ユーザーへの確認です。Session default はサポートしていません。

---

## Skills

ほとんどの `ywc-*` skill は Claude Code と Codex の両方で利用できます。目的別に整理された全カタログは [全 Skill リファレンス](https://yongwoon.github.io/ywc-agent-toolkit-lp/ja/guidebook/14-skill-reference/) にあります。まずはここから:

| 目的 | Skills |
| ---- | ------ |
| アイデアを plan または spec に | [`ywc-plan`](claude-code/skills/ywc-plan/README.md) → [`ywc-spec-writer`](claude-code/skills/ywc-spec-writer/README.md) |
| 未知のコードベースを把握 | [`ywc-onboard-repo`](claude-code/skills/ywc-onboard-repo/README.md) |
| 依存関係に安全なタスクへ分解 | [`ywc-task-generator`](claude-code/skills/ywc-task-generator/README.md) |
| タスクを end-to-end で実装 | [`ywc-sequential-executor`](claude-code/skills/ywc-sequential-executor/README.md) / [`ywc-parallel-executor`](claude-code/skills/ywc-parallel-executor/README.md) |
| goal から全 pipeline を実行 | [`ywc-agentic`](claude-code/skills/ywc-agentic/README.md) |
| バグの根本原因を特定 | [`ywc-debug-rootcause`](claude-code/skills/ywc-debug-rootcause/README.md) |
| コード品質とセキュリティのレビュー | [`ywc-impl-review`](claude-code/skills/ywc-impl-review/README.md), [`ywc-security-audit`](claude-code/skills/ywc-security-audit/README.md) |
| PR 作成とレビューコメント対応 | [`ywc-create-pr`](claude-code/skills/ywc-create-pr/README.md) → [`ywc-handle-pr-reviews`](claude-code/skills/ywc-handle-pr-reviews/README.md) |
| QA テストシートの生成 | [`ywc-gen-testcase`](claude-code/skills/ywc-gen-testcase/README.md) |
| リリースノートの作成 | [`ywc-release-pr-list`](claude-code/skills/ywc-release-pr-list/README.md) + [`ywc-changelog-release-notes`](claude-code/skills/ywc-changelog-release-notes/README.md) |
| 新しい `ywc-*` skill の作成 | [`ywc-skill-author`](claude-code/skills/ywc-skill-author/README.md) |

すべての skill ディレクトリは [`claude-code/skills/`](claude-code/skills) と [`codex/skills/`](codex/skills) にあり、それぞれ独自の README を持っています。

**つながり:** `ywc-plan` → （Medium/Large）`ywc-spec-writer` → `ywc-spec-ready` → `ywc-task-generator` → `ywc-sequential-executor` / `ywc-parallel-executor` が各タスクを end-to-end で届けます。アドホックな変更は executor を経由せず `ywc-create-pr` → `ywc-handle-pr-reviews` で進めます。各経路のコマンドとフラグは [コア pipeline ガイド](https://yongwoon.github.io/ywc-agent-toolkit-lp/ja/guidebook/02-core-concepts/) を参照してください。

### HTML 出力モード

9つの Review / Report skill が `--format html` フラグに対応し、Markdown の代わりにブラウザですぐ開ける self-contained な HTML レポートを生成します。色分け、severity coding、タブ、インタラクティブなコントロールにより、受け取った人が実際に読んで行動できるようになります。

```bash
/ywc-impl-review --spec docs/spec.md --code src/ --format html
/ywc-gen-testcase 250 --format html   # localStorage サインオフ付きインタラクティブテストシート
```

> **⚠️ Token コスト** — HTML 出力は Markdown の 2〜4 倍の output token を消費します。デフォルトは `markdown` です。人がブラウザで読むレポートに限って有効化してください。

対応 skill と詳細: [`references/html-output.md`](claude-code/skills/references/html-output.md).

---

## Custom Agent

Claude Code には worker、reviewer、specialist dispatch 用の 12 個の custom agent が含まれます。`~/.claude/agents/` にインストールされ、詳細は [`claude-code/agents/README.md`](claude-code/agents/README.md) を参照してください。

Codex にはこれに対応する read-only の specialist agent が 7 個あり、`~/.codex/agents/`（`CODEX_HOME` で上書き可能）に agent ごとに 1 つの TOML ファイルとしてインストールされます:

| Agent | 用途 |
| ----- | ---- |
| [`ywc-architect`](claude-code/agents/ywc-architect.md) | アーキテクチャ判断とトレードオフの advisor |
| [`ywc-security-engineer`](claude-code/agents/ywc-security-engineer.md) | 静的セキュリティレビューと threat model の分類 |
| [`ywc-root-cause-analyst`](claude-code/agents/ywc-root-cause-analyst.md) | 根本原因および障害原因の分析 |
| [`ywc-performance-engineer`](claude-code/agents/ywc-performance-engineer.md) | パフォーマンスレビューとプロファイリング推奨 |
| [`ywc-typescript-reviewer`](claude-code/agents/ywc-typescript-reviewer.md) | TypeScript / JavaScript 言語別レビュー |
| [`ywc-python-reviewer`](claude-code/agents/ywc-python-reviewer.md) | Python 言語別レビュー |
| [`ywc-go-reviewer`](claude-code/agents/ywc-go-reviewer.md) | Go 言語別レビュー |

すべての Codex agent は read-only でファイルを編集しません。標準化された `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`、簡潔な finding、そして呼び出し側が適用または確認すべき場合の `Next action:` を返します。ソース TOML は [`codex/agents/`](codex/agents/) にあります。

---

## Claude Code Hooks

Claude Code の tool 呼び出し前後に実行される自動化 hook です。`~/.claude/hooks/`（グローバル）または `./.claude/hooks/`（プロジェクトローカル）にインストールされ、`settings.json` に自動登録されます。`jq` と `uv` が必要です。

```bash
bash scripts/install.sh --hooks                    # すべての hook をグローバルに
bash scripts/install.sh --hooks --local            # 現在のプロジェクトに
bash scripts/install.sh --hooks cost-tracker       # 特定の hook のみ
bash scripts/install.sh --list --hooks             # 利用可能な hook の一覧
```

| Hook                        | Event                  | 説明                                                                    |
| --------------------------- | ---------------------- | ----------------------------------------------------------------------- |
| `block-dangerous-commands`  | `PreToolUse`           | 危険な shell コマンドをブロック（critical/high/strict レベル）             |
| `check-claude-md-freshness` | `PreToolUse`           | `git push` 前に CLAUDE.md が最新か確認                                    |
| `cost-tracker`              | `PostToolUse` + `Stop` | tool 呼び出し統計を記録し、終了時にセッションサマリを出力                  |
| `notify-permission`         | `Notification`         | 権限待ちのときに Slack 通知を送信（`CCH_SLA_WEBHOOK` が必要）             |
| `permission-request`        | `PermissionRequest`    | 安全な tool（Read, Write, Edit）を自動承認                                |
| `protect-secrets`           | `PreToolUse`           | `.env`、SSH 鍵などのシークレットファイルへのアクセスをブロック            |
| `session-start`             | `SessionStart`         | セッション開始時に git status、`CONTEXT.md`、TODO、GitHub Issue を注入    |

hook ごとの使い方: [`claude-code/hooks/README.md`](claude-code/hooks/README.md).

---

## コントリビュート

コントリビュートを歓迎します。PR を提出する前に [CONTRIBUTING.md](CONTRIBUTING.md) をお読みください。

- **バグ報告・skill 改善**: issue または PR を作成してください
- **新しい skill**: [ywc-skill-author](claude-code/skills/ywc-skill-author/SKILL.md) のガイドラインに従ってください
- **翻訳**: [翻訳ガイド](CONTRIBUTING.md#translations) を参照してください
- **Codex パッケージ同期**: [Codex skill メンテナンス workflow](CONTRIBUTING.md#maintainer-workflow-for-codex-skills) を参照してください

## License

MIT
