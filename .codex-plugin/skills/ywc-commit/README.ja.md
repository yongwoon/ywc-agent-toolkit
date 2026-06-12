# Commit Skill (ywc-commit)

現在の session で行った変更を安全に Git commit（および任意で push）する Codex Skill です。

## 概要

この Skill は以下を自動で処理します:

- Session に関連する file のみを選別して stage
- 論理的に異なる変更を別々の commit に分離
- Project の既存 commit style（type/scope/message）を `git log` から学習して一貫したメッセージを作成
- Commit 結果のサマリーを報告

## 使い方

自然言語または slash command で要求します:

```text
/ywc-commit
```

```text
commit and push
```

```text
authentication 関連の file のみ commit して
```

韓国語の表現（`커밋 해줘`、`커밋푸쉬 ㄱㄱ`、`지금까지 한 작업 커밋`）も認識されます。

## 主要ルール

| ルール | 内容 |
| --- | --- |
| Session 関連 file のみ stage | この会話で作成・修正・議論した file のみ対象 |
| 論理単位で commit を分割 | 1 commit = 1 目的 |
| Push は明示的要求時のみ | "push"、"푸쉬"、"올려줘" などを含む場合のみ実行 |
| `--no-verify` 禁止 | Hook 失敗時は原因を修正または報告 |
| `git add .` 禁止 | 常に file path を明示して stage |
| main/master への直接 commit 前に確認 | ほぼ必ずミスなので先に確認 |
| 秘密値・成果物を除外 | `.env*`、`dist/`、`build/` は意図的でなければ除外 |
| Tool 固有の co-author trailer はデフォルトで追加しない | Repository 慣例またはユーザーの明示要求がある場合のみ含める |

## Workflow

```text
Step 1: 現在状態の把握
  └─ git status、git diff、git log（style 学習）、branch 確認

Step 2: 変更 file の分類
  └─ IN（session 関連）/ UNKNOWN（出所不明）/ OUT（無関係）
  └─ UNKNOWN/OUT があれば分類一覧をユーザーに提示して承認を得る

Step 3: 論理単位で commit を分割
  └─ 性格の異なる変更は別 commit として計画
  └─ 必要に応じて git add -p で hunk 単位 stage
  └─ 計画（file + メッセージ草案）をユーザーに提示して承認

Step 4: Commit メッセージ作成
  └─ git log から project style を学習して同じ形式を適用
  └─ Co-author trailer は repository 慣例またはユーザー要求がある場合のみ含める

Step 5: Stage & Commit
  └─ 明示 path で stage → diff 確認 → heredoc で commit

Step 6: 結果確認
  └─ git log、git status で漏れ・残余変更を確認

Step 7: Push（要求された場合のみ）
  └─ 通常 push、upstream がなければ -u flag を使用
  └─ Force-push は明示的要求時のみ
```

## Commit メッセージ形式

Project の既存 `git log` style に合わせます。一般的な形式:

```text
<type>(<scope>): <summary>

<body — 必要な場合のみ>
```

**type 例**（この repository で使われているものだけを使用）:
`feat`、`fix`、`refactor`、`perf`、`chore`、`docs`、`test`

**scope**: `git log` から観察した pattern を使用（package 名、module 名など）。複数の領域にまたがる場合は省略。

`Co-Authored-By` trailer はデフォルトでは追加しません。最近の commit 履歴で AI co-author trailer が一貫して使われている場合、またはユーザーが明示的に要求した場合のみ、repository の慣例に従います。Repository 慣例がなく、ユーザーが co-author trailer を要求した場合は `Co-Authored-By: Claude <noreply@anthropic.com>` を使用します。

## 報告形式

Commit 完了後に以下の形式で報告します:

```text
✅ N 件の commit 作成 [+ push 有無]
  1. <hash> <type>(<scope>): <summary>
  2. <hash> <type>(<scope>): <summary>
除外した file: <あれば列挙、なければ省略>
```

## Error Handling

| Situation | Behavior |
| --- | --- |
| UNKNOWN file 発見 | 分類一覧をユーザーに提示し承認後に進む |
| Hook 失敗 | `--no-verify` 使用禁止、原因を報告して停止 |
| main/master への直接 commit | まずユーザーに確認 |
| Non-fast-forward push が拒否された | 状況を説明してオプションを提示、force-push は明示要求時のみ |
| 秘密値・成果物 file 発見 | ユーザーに通知して除外 |

## Integration

この Skill は以下の Skill と連動します:

- **ywc-create-pr** — PR 作成前の commit step（Step 3）で内部的に使用
- **ywc-sequential-executor** — Task 実行中の commit step で参照可能

## Example Prompt

```text
/ywc-commit
commit and push
authentication 関連の file のみ commit して
```
