# ywc-changelog-release-notes

Git History、Merged PR、または`ywc-release-pr-list`の出力を基に、
CHANGELOG.mdエントリとUser向けRelease Notesを生成するSkillです。
Keep a Changelog形式の技術文書と、非技術User向けのPlain Language要約を
それぞれ別ドキュメントとして作成します。

## 核心概念: 2種類の出力物

このSkillは**目的が異なる2つの文書**を生成します。

| | CHANGELOG.md | Release Notes |
|---|---|---|
| 対象読者 | 開発者、メンテナー | 最終User、顧客 |
| 含む内容 | 全変更、CVE、PR番号 | User可視の変更のみ |
| 文体 | 技術的、簡潔 | Plain Language、恩恵中心 |
| refactor/chore | 含む | 除外 |

## 実際の使用シナリオ

### Case 1: 新バージョンのTag付け前（最も一般的）

```
/ywc-changelog-release-notes --both --version 1.2.0
```

開発者向けCHANGELOG.mdとUser向けRelease Notesを一度に生成します。
GitHub Release pageに掲載する内容が必要な場合に使用します。

### Case 2: CHANGELOG.mdのみ更新する場合

```
/ywc-changelog-release-notes --changelog
```

外部Userがいない内部チーム運営プロジェクトなど、開発者向け変更履歴のみ必要な場合に使用します。
`git tag`を打つ前に実行します。

### Case 3: 顧客向けアナウンスやSlack投稿の作成

```
/ywc-changelog-release-notes --release
```

「v1.3.0がリリースされました」のようなUser向けアナウンスを作成する際に使用します。
技術的な内容は自動的に除外され、User視点の文章に変換されます。

### Case 4: ファイル変更前に内容を確認する場合

```
/ywc-changelog-release-notes --dry-run
```

実際に`CHANGELOG.md`を変更する前に、どのような内容が入るかを確認する際に使用します。
内容を確認し、問題なければ`--dry-run`なしで再実行します。

### Case 5: `ywc-release-pr-list`と連携する場合

PRリストを事前に整理している場合、その結果をこのSkillのInputとして活用できます。

```
/ywc-release-pr-list > pr-list.md
/ywc-changelog-release-notes --both --pr-list pr-list.md --version 1.2.0
```

`ywc-release-pr-list`はPRをテーブルで一覧化し、このSkillはそれを読みやすいCHANGELOGエントリに**フォーマット**します。

## 使用方法（全Flag）

```
/ywc-changelog-release-notes --changelog              # CHANGELOG.mdエントリのみ生成
/ywc-changelog-release-notes --release                # User向けRelease Notesのみ生成
/ywc-changelog-release-notes --both --version 1.2.0  # 両ドキュメントを生成
/ywc-changelog-release-notes --from v1.1.0 --to HEAD # 特定の範囲を指定
/ywc-changelog-release-notes --dry-run               # ファイル変更なし、出力のみ
```

## 典型的なRelease フロー

```
1. ywc-release-pr-list          → 今回のReleaseに含まれるPRリストを整理
2. ywc-changelog-release-notes  → CHANGELOG + Release Notes を生成
3. ywc-commit                   → 更新したCHANGELOG.mdをCommit
4. ywc-create-pr                → Release PRを作成
5. git tag -a v1.2.0 -m "..."   → Tagを打つ（SkillがCommandを提案）
```

## 関連Skill

- `ywc-release-pr-list` — `--pr-list`へのInputとなるPRリスト生成
- `ywc-commit` — 更新したCHANGELOG.mdのCommit
- `ywc-create-pr` — Release PRの作成
- `ywc-incident-postmortem` — Patch Releaseの原因となったインシデントの振り返り
