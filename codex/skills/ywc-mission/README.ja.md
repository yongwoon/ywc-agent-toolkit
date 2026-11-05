# Mission

プロジェクトの Mission、Success Criteria、Rejected Approaches、および任意の Non-goals/Constraints を `docs/mission.md` に保存し、Codex の次回セッションへ引き継ぐスキルです。

## 使い方

```text
Use $ywc-mission --mode read.
Use $ywc-mission --mode update --dry-run.
```

## オプション

この要約と異なる場合は `SKILL.md` を優先します。

| オプション | 値 | 既定値 | 説明 |
|---|---|---|---|
| `--mode` | `read\|update\|curate` | 自動判定 | 有効な anchor の読み取り、更新提案、古い項目の廃止。 |
| `--output` | `<path>` | `docs/mission.md` | Mission ファイルのパス。 |
| `--dry-run` | flag | off | CHANGESET を表示し、確認依頼や書き込みはしない。 |

## 状態と確認

- ファイルがない read は空の anchor を返します。任意セクションのない既存ファイルも有効です。
- update/curate は全体を読み、理由付き ADD/MODIFY/DEPRECATE CHANGESET を提示します。空でない正確な CHANGESET に対するユーザー確認後のみ永続化します。
- dry-run と空の変更は確認依頼、ファイル作成、更新日・変更履歴の更新を行いません。
- active Mission は一つです。SC は観測可能な Criterion と Rationale、RA は Reason が必要です。NG は Non-goal/Reason、CN は Constraint/Rationale が必要です。
- 任意セクションは最初の確定項目で作成し、active 項目がなくなれば除去します。廃止項目の原文・理由・出典・ID は履歴に残し、削除や ID 再利用はしません。
- anchor は active 項目のみ含めます。書き込み前に再読し、状態が変われば再確認します。反映済みの再試行は no-op、書き込み失敗は成功扱いにしません。
- 初回作成後は AGENTS.md/CODEX.md の有効化案内のみ提示し、これらのファイルを編集しません。リポジトリ走査からユーザー意図を捏造しません。

## 出力と根拠

read は compact Mission Anchor、update/curate は CHANGESET と確定結果を返します。永続形式は [mission-format.md](references/mission-format.md) を参照してください。

固定 upstream #348 (`29068f9f690fbf09e0ace8d562e4fb846b4d1339`) からの移植です。fixture と評価期待値はソース根拠であり、別途実行 trace がない live 動作は UNVERIFIED です。
