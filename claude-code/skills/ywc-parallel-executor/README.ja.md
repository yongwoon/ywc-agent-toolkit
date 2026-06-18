# ywc-parallel-executor (Parallel Executor)

task-generator が生成した Task を Agent が並列で実行する Skill です。dependency-graph.md を分析し、Wave ベースの並列実行 + Git Worktree 分離を行います。

## Test-first・Deep Module・Critical Module Review

worker payload に interface-first directive と test-first-where-feasible directive を注入します：behavior change task は実装の前に失敗する test を先に作成し(docs/config/mechanical は例外)、public surface を body より先に設計します(deep module)。Task の Ownership が critical path(auth, payment, crypto, PII, external input)に該当する場合、`--review` なしでも 4d で `/ywc-impl-review` と `/ywc-security-audit` を強制します。詳細は `../references/tdd-deep-module-gray-box.md` を参照してください。

## 使用方法

```text
/ywc-parallel-executor 000001-010-db-create-events           # 単一 Task
/ywc-parallel-executor 000001-010..000002-040                     # 範囲指定 (並列)
/ywc-parallel-executor --all                              # 全体実行
/ywc-parallel-executor 000001-010..000002-040 --review            # 並列 + 自動 Review
/ywc-parallel-executor 000001-010..000002-040 --local-merge       # PR なし Local merge
/ywc-parallel-executor 000001-010..000002-040 --draft             # Draft PR 作成 (後で人が merge)
/ywc-parallel-executor 000001-010..000002-040 --per-task-pr       # Task ごとに PR 作成・CI・review・merge
/ywc-parallel-executor 000026-010..000026-030 --aggregate-pr --group-name payments --pr-lang ko  # Group 単位の単一 PR
```

## Option

| Option | 説明 |
|--------|------|
| `--tasks-dir <path>` | Tasks directory パス (default: tasks/) |
| `--pr-lang <lang>` | 最終 PR (`--aggregate-pr`) の title/description 言語 (default: auto-detect) |
| `--review` | 各 Task 完了後 /ywc-impl-review を自動実行します (組み合わせ可能) |
| `--local-merge` | PR なし、base-branch へ直接 merge + push |
| `--draft` | 全体完了後に単一の Draft PR を作成します (open のまま人が merge) |
| `--per-task-pr` | Task ごとに PR 作成 → CI 待機 → bot review 対応 → merge まで実行 (sequential-executor の default と同じ full lifecycle) |
| `--aggregate-pr` | Invocation 全体 → branch 1個 + PR 1個。Task は引き続き並列 (Wave) で実行され単一の aggregate branch に蓄積され、最後に ready → CI → bot review → **merge** まで実行します (`--draft` の full-lifecycle 版) |
| `--group-name <name>` | aggregate branch 名 (`aggregate/<name>`) を指定し、同時実行する group を区別します。`--aggregate-pr` 専用、省略時は `aggregate/<base-branch>-<timestamp>` |

> Mode 未指定時のデフォルトはありません。`--local-merge` / `--draft` / `--per-task-pr` / `--aggregate-pr` のいずれかをユーザーが明示的に選択する必要があります。4種は相互排他です。

## Group 単位の実行 (`--aggregate-pr`)

多数の Task を **group にまとめて group ごとに PR 1個**で delivery し、必要なら **group 間で並列**に進めたい場合は `--aggregate-pr` を使用します。

**コア概念**: 1 invocation = 1 group = 1 PR。Group **内部**の Task は Wave ベースで並列実行され、各 Task の変更と `chore: mark ... as completed` marker commit が単一の aggregate branch に蓄積されます。全 Wave 完了後、その branch で単一の PR を開き ready → CI → bot review → merge-readiness gate → merge → base sync までを一度に実行します。marker commit は既に branch 上にあるため、merge 後の別途 Mark Complete はありません。

### 単一 Group

```text
/ywc-parallel-executor 000026-010..000026-030 --aggregate-pr --group-name payments --review --pr-lang ko
```

- `--review`: 各 Task の worktree branch が aggregate に合流する前に `/ywc-impl-review` で gate
- `--pr-lang ko`: PR title/description の言語を固定
- 実行前に `--dry-run` で Wave 計画 (Task 順序・依存・mode) を事前確認することを推奨します。

### Group 間の並列 (同時実行)

複数の group を同時に回すには **group ごとに 1 clone**(独立した `.git`)で分離する必要があります。`--aggregate-pr` は local `<base>` branch に直接累積(`git reset --hard origin/<base>` + per-task merge)するため、2 つの group が同じ `<base>` を同時に操作すると互いの累積を上書きします。**git worktree で分けても** working tree と untracked `.ywc-run-state.json` が分離されるだけで `.git` の refs(特に local `<base>` branch)は worktree 間で共有されるため、ref layer で依然として衝突します。worktree は分離境界になりません。

```bash
git clone <repo-url> ../grp-payments && \
  ( cd ../grp-payments && /ywc-parallel-executor 000026-010..000026-030 \
      --aggregate-pr --group-name payments --review --pr-lang ko ) &

git clone <repo-url> ../grp-search && \
  ( cd ../grp-search && /ywc-parallel-executor 000027-010..000027-040 \
      --aggregate-pr --group-name search --review --pr-lang ko ) &

wait
```

追加の clone なしで 1 つの repo で処理する場合は、group を **順次 back-to-back** で実行します (各 group 内部は引き続き並列):

```bash
/ywc-parallel-executor 000026-010..000026-030 --aggregate-pr --group-name payments --pr-lang ko
/ywc-parallel-executor 000027-010..000027-040 --aggregate-pr --group-name search   --pr-lang ko
```

詳細な手順・並行性の安全規則は [references/aggregate-pr.md](./references/aggregate-pr.md) を参照してください。

## 実行フロー

1. dependency-graph.md の Parse
2. Wave 計画の策定 (Topological Sort)
3. Wave 単位で実行: Worktree 作成 → Agent 並列実行 → 検証(Task Verify + 全体/影響範囲 regression suite + Ownership scope gate) → Merge → Worktree 削除

## Task → Agent 自動マッピング

| Category | Agent |
|----------|-------|
| db, api, domain, lib, worker | Backend Agent (sonnet) |
| ui | Frontend Agent (sonnet) |
| test | QA Agent (sonnet) |
| infra | DevOps Agent (sonnet) |
| refactor | Reviewer Agent (opus) |

Agent Hint で Override が可能です:
```markdown
## Parallel Execution Metadata
- Agent Hint: frontend
```

## sequential-executor との比較

| 状況 | 推奨ツール |
|------|-----------|
| 小規模作業 (1-3 Task) | sequential-executor |
| 順次依存性が強い作業 | sequential-executor |
| 大規模作業 (4+ Task) | /ywc-parallel-executor |
| 並列可能な Task が多い場合 | /ywc-parallel-executor |

## Triggering

この Skill の Trigger 条件は [SKILL.md](./SKILL.md) の `description` フィールドに定義されています。

## Localized Versions

- [English](./README.en.md)
- [Japanese](./README.ja.md)
- [Korean](./README.ko.md)
