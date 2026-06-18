# Sequential Executor Skill (ywc-sequential-executor)

ywc-task-generator Skill で生成された Task を実行する Claude Code Skill です。Branch 作成から実装、Commit、PR 作成、CI 確認、Merge、Local sync まで、開発 Lifecycle 全体を自動化します。

## Test-first・Deep Module・Critical Module Review

behavior change は test-first です：bugfix は fix の前に失敗する regression test を、新規動作は実装の前に失敗する test を先に作成します(docs/config/mechanical task は例外)。Public contract 変更時は interface を body より先に作成します(deep module)。Task の Ownership が critical path(auth, payment, crypto, PII, external input)に該当する場合、`--review` なしでも `/ywc-impl-review` と `/ywc-security-audit` を強制します。詳細は `../references/tdd-deep-module-gray-box.md` を参照してください。

単一 Task の実行に加え、連続した Task range を指定して繰り返し実行することもサポートしています。

## 使い方

### 基本的な使い方

単一 Task を実行します:

```text
/ywc-sequential-executor 000001-010-db-create-users-table
```

Phase+Sequence prefix でも指定できます:

```text
/ywc-sequential-executor 000001-010
```

### Range 実行

連続した Task を順次繰り返し実行します:

```text
/ywc-sequential-executor 000001-010..000002-030
```

### 次の Task を自動検出

Task を指定しない場合、dependency graph を分析して実行可能な次の Task を自動選択します:

```text
/ywc-sequential-executor
```

### Option

| Option | 説明 | 例 |
|--------|------|----|
| `--pr-lang <lang>` | PR title/description の言語指定 | `--pr-lang ja` |
| `--tasks-dir <path>` | Tasks directory のパス (default: `tasks/`) | `--tasks-dir ./docs/tasks` |
| `--skip-ci-wait` | CI 待機と auto-merge を skip (PR 作成のみ) | |
| `--draft` | Draft PR を作成、merge skip | |
| `--local-merge` | PR を作成せず、ローカルで base branch へ merge して push (Step 4 の verification は通常通り実行) | |
| `--aggregate-pr` | range 全体を work branch 1個 + PR 1個で delivery (各 Task を `work/<name>` に順次 local-merge → work→base PR 1個) | |
| `--group-name <name>` | work branch 名(`work/<name>`)を指定。`--aggregate-pr` 専用、省略時は `work/<base>-<timestamp>` | `--group-name project-health` |
| `--base-branch <branch>` | Base branch 指定 (default: auto-detect) | `--base-branch develop` |
| `--dry-run` | 実行計画のみ表示 (Task 順序、dependency、mode)。実際には実行しない | |
| `--worktree` | range 全体を **隔離された git worktree 1個** の中で実行し、main checkout を空けておきます。run-level 隔離 — Task は依然として順次実行。独立 flag で 4 種 delivery mode・`--review` と組み合わせ可能。詳細は [references/worktree-run.md](./references/worktree-run.md) | `--worktree` |

> `--local-merge`, `--draft`, `--skip-ci-wait`, `--aggregate-pr` は相互排他です。複数指定した場合 Skill は中断し、どの mode を意図したか確認します。
> `--local-merge` は **リモート CI を経由しない** ため、Step 4 のローカル verification (lint/typecheck/test) だけが merge の安全装置となります。重要な変更には推奨しません。
> `--worktree` は上記の mutual-exclusion 集団と **独立** です (5 番目のメンバーではない)。worktree の中で Docker stack を起動すると host の既存 dev stack と host port が衝突する可能性があります (host-isolation follow-up の管轄)。Task は順次実行されるため *並列* の衝突は発生しません。

### Group 単位の実行 (`--aggregate-pr`)

複数の Task を **1 つの work branch に順次蓄積し、group ごとに PR 1個** で delivery したい場合は `--aggregate-pr` を使用します。range 全体が次の流れで一度に処理されます:

1. `work/<name>` branch を base から 1 回作成
2. range の各 Task を **work branch を基準に順次実行** (各 Task は work branch へ local-merge → 次の Task は更新された work branch から分岐)
3. 最後の Task 終了後、**work → base PR 1個** を作成 → ready → CI → bot review → merge → base sync
4. 完了報告

real base (main) は最後の PR merge まで **変更されません**。parallel の worktree/wave なしで順次のみ動作するため、シンプルで安全です。

```text
/ywc-sequential-executor 000024-010..000025-030 --aggregate-pr --group-name project-health --review --pr-lang ko
```

- `--review`: 各 Task が work branch に合流する前に `/ywc-impl-review` で gate
- `--pr-lang ko`: 最終 PR の title/description 言語を固定
- 実行前に `--dry-run` で Task 順序・作成される work branch を事前確認できます。

詳細な手順は [references/aggregate-pr.md](./references/aggregate-pr.md) を参照してください。

> 注意: 中断された run の `.ywc-run-state.json` が残っていると、次の実行がその state で resume され、新しい range が無視されることがあります。新しい range を意図する場合は先に `.ywc-run-state.json` を削除してください。

## Execution Cycle

各 Task に対して以下の Step を順番に実行します。**Range mode では Task ごとに全 Cycle (Step 1 → Step 8) を繰り返します。各 Task は独立した feature branch を使用します。**

### Range Mode の Task 別 Branch Lifecycle

**Normal mode (PR flow):**

```text
Task ごとに: base branch checkout → pull → feature branch 作成 → 実装 → PR → CI → merge → 繰り返し
```

**`--local-merge` mode:**

```text
Task ごとに: base branch checkout → pull → feature branch 作成 → 実装 → local merge → push → 繰り返し
```

**`--draft` / `--skip-ci-wait` mode:**

```text
Task ごとに: 前の feature branch から分岐 (chain branching) → 実装 → draft PR → 繰り返し
```

### Step 詳細

```text
Step 1: Dependency Validation & Spec Loading
  └─ Depends On の全 Task が tasks/completed/ にあるか確認
  └─ README.md の Spec Reference (Primary Sources / Summary / Out of Scope) をロード
  └─ 外部 URL は .claude/settings.local.json の taskExecutor.externalSpecUrls policy に従う

Step 2: Branch Creation (毎 Task 実行 — range でもスキップしない)
  └─ (normal/local-merge) git checkout <base> && git pull && git checkout -b feature/<task-name>
  └─ (range+draft/skip-ci-wait) 前の feature branch から分岐 (chain branching)

Step 3: Implementation
  └─ task.md の Implementation Steps に従い実装、適切な単位で Commit

Step 4: Task Verification
  └─ Task Verify command および lint/typecheck/test 実行

Step 5: PR Creation
  └─ create-pr Skill を呼び出し (security check, CI pre-push validation 含む)
  └─ (--local-merge) skip — PR は作成しない

Step 6: CI Verification & Merge
  └─ gh pr checks --watch → gh pr merge --delete-branch
  └─ (--local-merge) git checkout base → git merge --no-ff feature/<task> → git push → git branch -d

Step 7: Local Sync
  └─ git checkout <base-branch> && git pull origin <base-branch>

Step 8: Mark Complete
  └─ mv tasks/<task-name> tasks/completed/<task-name> → commit
  └─ --local-merge range: 毎 Task 即時 push
  └─ Normal PR range: push は最後の Task 完了後に 1 回だけ実行

Step 9: Next Task (Range mode)
  └─ 残りの Task があれば Step 1 に戻り全 Cycle 繰り返し (Step 2 含む)
```

## PR Language

`--pr-lang` を指定しない場合、以下の優先順位で言語を検出します:

1. **CLAUDE.md** — 言語指定の確認 (例: `Git commits: Japanese`)
2. **AGENTS.md** — 言語設定の確認
3. **最近の PR 履歴** — 主に使われている言語を検出
4. **Fallback** — English

## Error Handling

| 状況 | 動作 |
|------|------|
| CI 失敗 | 最大 2 回 fix を試み、その後 user に通知 |
| Merge conflict | 中断し、user に手動解決を依頼 |
| CI timeout (30 分超過) | 状態を報告し、user に待機継続か確認 |
| Dependency 未充足 | 未完了 dependency のリストを出力して中断 |
| Task 未発見 | 利用可能な Task 一覧を表示 |

## Integration

この Skill は以下の Skill と連携します:

- **ywc-task-generator** — Task 生成 (upstream)
- **create-pr** — PR 作成 (Step 5 で呼び出し)

## Example Prompt

### 単一 Task 実行 (Japanese PR)

```text
/ywc-sequential-executor 000001-010-db-create-users-table --pr-lang ja
```

### 全 Range 実行

```text
/ywc-sequential-executor 000001-010..000003-020 --pr-lang ja
```

### Draft PR のみ作成 (merge しない)

```text
/ywc-sequential-executor 000001-010..000002-030 --draft --pr-lang ko
```

### Flag 競合時の動作

`--local-merge`, `--draft`, `--skip-ci-wait` を同時に指定すると、Skill は実行を中断し、どの mode を意図したか確認します。この 3 つは異なる終了状態を作るためです (前者は PR なし + merge 済、後者 2 つは PR あり + merge なし)。

```text
/ywc-sequential-executor 000001-010 --local-merge --draft
# → 中断。「--local-merge と --draft は相互排他です。どの mode にしますか?」
```

### PR なしでローカル merge のみ実行

個人 project や hotfix など、PR workflow が不要な場合に使います:

```text
/ywc-sequential-executor 000001-010-db-create-users-table --local-merge
```

Step 4 の lint/typecheck/test は同じく実行され、通過すれば `git merge --no-ff` で base branch にマージされ push されます。

## Triggering

この Skill の Trigger 条件は [SKILL.md](./SKILL.md) の `description` フィールドに定義されています。
