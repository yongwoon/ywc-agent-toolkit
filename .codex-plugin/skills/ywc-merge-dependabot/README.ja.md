# Merge Dependabot Skill (Codex)

## 概要

Dependabot が作成した Pull Request を安全にまとめて Merge する Skill です。
Claude Code と Codex CLI の両方で利用できます。

## 主な機能

- 全 Dependabot PR、または Security 関連 PR のみを Merge
- Dockerfile `FROM` 変更、Major Version Upgrade、CI Status の pre-merge check
- Merge conflict の解決試行と CI 再実行待ち
- Default では PR 番号の昇順で sequential 処理
- **Parallel-auto mode**: lockfile ecosystem ごとに lane を作り、各 lane で active auto-merge PR を 1 件だけ維持して、大量 PR の wall-clock 時間を短縮
- 最終 Summary Report の出力

## 使用方法

### Claude Code

```text
/ywc-merge-dependabot                          # 全 PR を sequential 処理
/ywc-merge-dependabot security                 # Security PR のみ sequential 処理
/ywc-merge-dependabot parallel-auto            # 全 PR を ecosystem-lane auto-merge
/ywc-merge-dependabot security parallel-auto   # Security PR のみ ecosystem-lane auto-merge
```

### Codex CLI

```text
Use $ywc-merge-dependabot to merge all open Dependabot pull requests.
Use $ywc-merge-dependabot security to merge only security-related Dependabot PRs.
Use $ywc-merge-dependabot parallel-auto to merge a large batch via ecosystem-lane auto-merge scheduling.
Use $ywc-merge-dependabot security parallel-auto to combine the security scope with the parallel-auto execution flag.
```

## 前提条件

- GitHub CLI (`gh`) の install と authentication が完了していること
- 対象 repository への Merge 権限があること
- `parallel-auto` の場合: repository の "Allow auto-merge" が有効であること。無効な場合は sequential mode に fallback します。

## Mode

この Skill は 2 つの直交 flag をサポートします。

**Scope flag** — 対象 PR:

| Token | Scope |
| --- | --- |
| `security` | Security 関連 Dependabot PR のみ |
| _(なし)_ | すべての Dependabot PR |

**Execution flag** — 処理方式:

| Token | Execution | 使用時点 |
| --- | --- | --- |
| `parallel-auto` | Ecosystem lane + lane ごとに active auto-merge PR 1 件 | 複数 ecosystem にまたがる PR が 5 件以上ある場合 |
| _(なし)_ | PR 番号昇順の sequential 処理 | 少量 batch または strict branch protection 環境 |

## Skip 条件

| 条件 | 理由 |
| --- | --- |
| Dockerfile `FROM` 変更 | Container base image 変更は手動 review が必要 |
| Major Version Upgrade | Breaking change risk |
| CI 未通過 | Build/Test 失敗状態での Merge 防止 |

## Result Format

```text
Mode: parallel-auto (security)
Ecosystem groups processed: npm (3), github-actions (2), python (2)

- Merged    (npm)            : #123 Bump axios from 1.6.0 to 1.7.2
- Skipped   (Dockerfile)     : #127 Bump node from 18 to 20
- Skipped   (Major version)  : #130 Bump webpack from 4.x to 5.x
- Failed    (lane stalled)   : #132 Bump express from 4.18.0 to 4.19.2 - CONFLICTING after 30 min
```

Sequential mode でも `Mode` line は出力し、`Ecosystem groups` header と PR line の ecosystem annotation は省略します。

## ファイル構成

```text
ywc-merge-dependabot/
├── README.md
├── README.en.md / README.ja.md / README.ko.md
├── SKILL.md
├── agents/
│   └── openai.yaml
└── scripts/
    └── group-by-ecosystem.py
```

## 関連 Skill

- [ywc-create-pr](../ywc-create-pr/SKILL.md) — PR 作成
- [ywc-handle-pr-reviews](../ywc-handle-pr-reviews/SKILL.md) — PR review comment 対応
- [ywc-release-pr-list](../ywc-release-pr-list/SKILL.md) — Release PR list 生成
