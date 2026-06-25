# Gen Testcase Skill (ywc-gen-testcase)

GitHub PR、実装済みの Task directory、または現在の git diff を入力として、**開発者向け Section A (pre-merge gate) と QA/Browser 向け Section B (pre-release gate) に分割された Checkbox 形式の Testsheet** を Markdown で生成する Claude Code Skill です。Default の出力先は project の `docs/test-case/` directory です。

Backend engineer と QA/PM/Product Owner がそれぞれ自分の section で独立・並列に Sign-off でき、Merge 判断と Release 判断を明確に分離します。

## 使い方

### 基本的な使い方

PR URL から生成:

```text
/ywc-gen-testcase https://github.com/acme/web-app/pull/250
```

同一 repository 内なら PR 番号のみで可能:

```text
/ywc-gen-testcase 250
```

### Task ベース生成

```text
/ywc-gen-testcase 000001-010-db-create-users-table
```

### Git Range ベース生成

任意の commit 範囲を指定できます。SHA / Tag / Branch / `HEAD~N` いずれも受け付けます。

```text
/ywc-gen-testcase v1.2..v1.3
/ywc-gen-testcase HEAD~5..HEAD
/ywc-gen-testcase main..feature-x
/ywc-gen-testcase --range abc1234..def5678
```

> Range は **two-dot `A..B`** のみサポート。Three-dot `A...B` は merge-base semantics で scope が暗黙に変わるため reject されます。
> Range HEAD が open/merged PR に含まれる場合 (80% 以上 commit 重複)、Skill が PR mode への切替を自動提案します — PR body / labels / Acceptance Criteria が scenario 品質を大幅に引き上げるためです。
> Commit message 品質が低い場合 (headline の 70% 以上が 10 文字以下) は警告して続行可否を確認します。

### Diff ベース生成

```text
/ywc-gen-testcase --from-diff
```

### Option

| Option | 説明 | 例 |
| --- | --- | --- |
| `--output-dir <path>` | 出力 directory を上書き (default: `docs/test-case/`) | `--output-dir ./qa/manual-tests` |
| `--lang <code>` | Testsheet の言語 (`ja`, `ko`, `en`)。default: auto-detect | `--lang ja` |
| `--filename <name>` | Filename override (`.md` 不要) | `--filename release-v2-smoke` |
| `--tasks-dir <path>` | Tasks directory パス (default: `tasks/`) | `--tasks-dir ./docs/tasks` |
| `--include-regression` | Regression section (B.3) を追加 | |
| `--audience <who>` | `dev` \| `qa` \| `both`。default: `both` (A+B 統合) | `--audience qa` |
| `--split` | `<slug>-dev.md` + `<slug>-qa.md` の 2 file に物理分割 | |
| `--force-single` | L tier でも split 提案せず単一 file を強制 | |
| `--no-toc` | M/L tier の auto-TOC を抑止 | |
| `--from-diff` | `git diff HEAD` を元に生成 | |
| `--range <spec>` | Git range を明示指定 (`A..B`)。positional と等価 | `--range v1.2..v1.3` |
| `--dry-run` | 生成計画のみ表示 (file は書き出さない) | |

> PR identifier・Task specifier・Range (`A..B`)・`--from-diff` は相互排他です。`--split` と `--force-single` も相互排他です。複数指定すると Skill は中断し、どの mode を意図したか確認します。

## 2 つの Audience、2 つの Gate

Testsheet の設計思想は「誰が・いつ・どの道具で検証するか」による **Section 分割** です。

| Section | 対象 | 使用道具 | Gate |
| --- | --- | --- | --- |
| **A. Developer Verification** | Backend / DB / DevOps engineer | psql, gh CLI, curl, docker | **Pre-merge** — contract, migration, worker, container |
| **B. QA / Browser Verification** | QA, PM, Product Owner, designer | Chrome + DevTools, 管理 UI, test origin | **Pre-release** — end-user 体感と browser observable effect |

Dev と QA が並列に進められ、各自自分の section のみを見れば済みます。

## Tier 自動判定

Scenario 数に応じて layout が自動決定され、読まれない 1000 行の壁を防ぎます。

| Tier | Scenario 数 | Layout |
| --- | --- | --- |
| **S** | ≤ 20 | 単一 file、A/B section、TOC / 折り畳みなし |
| **M** | 21–40 | 単一 file、A/B section、冒頭 auto-TOC + Prerequisites/Edge Cases は `<details>` で折り畳み |
| **L** | > 40 | user に 単一 file / `--split` / Phase 分割 のいずれかを確認してから生成 |

多くの PR は自然に S / M に収まり、L tier の確認 prompt は大型 release の安全装置として機能します。

## Execution Cycle

```text
Step 1: Input Resolution
  └─ PR: gh pr view / gh pr diff で metadata と diff を取得
  └─ Task: <tasks-dir>/<name>/ (完了済なら completed/ 優先) の task.md / README.md 読み込み
  └─ Diff: git diff HEAD + 直近 commit log 取得

Step 2: Audience and Surface Classification
  └─ Audience tag: A (Developer) / B (QA/Browser)
  └─ Surface: UI / Database / API / Background job / Configuration / Docs
  └─ Browser-observable effect があれば backend-only PR にも B section を入れる

Step 3: Scenario Generation
  └─ (audience, surface) 組ごとに 2〜5 scenario
  └─ 各 scenario に Goal / Preconditions / Steps / Expected / Checkbox
  └─ Source 優先順位: PR body / Task Acceptance Criteria > Commit message > Surface > Diff edge case

Step 4: Tier Decision
  └─ Scenario 数から S / M / L を判定
  └─ L tier は user に進行方法を確認してから生成

Step 5: Write the Testsheet
  └─ Single file (default) / split (--split / --audience)
  └─ M/L tier では TOC 挿入と Prerequisites/Edge Cases の折り畳み
  └─ 同じ path に file が存在する場合は `-v<N>` suffix (overwrite しない)

Step 6: Validate & Report
  └─ File 存在、Checkbox 数、Expected の具体性、TOC anchor を確認
  └─ Tier / Audience / Surface summary を報告
```

## Default Filename Rule

| Input | Single file (default) | `--split` |
| --- | --- | --- |
| PR | `pr-<number>-<slug>.md` | `pr-<number>-<slug>-dev.md` + `...-qa.md` |
| Task | `task-<phase>-<sequence>-<slug>.md` | `...-dev.md` + `...-qa.md` |
| Range | `range-<short-start>-<short-end>-<slug>.md` (両端が tag なら `range-v1.2-v1.3-<slug>.md`) | `...-dev.md` + `...-qa.md` |
| Diff | `<yyyymmdd-HHMM>-<branch-slug>.md` | `...-dev.md` + `...-qa.md` |

## Testsheet 構造 (single-file default)

```text
1. Summary
2. Prerequisites
   2.0 Common
   2.A Dev-only
   2.B QA-only
A. Developer Verification  [pre-merge gate]
   A.1 Database / Table
   A.2 API
   A.3 Background Jobs / Workers
   A.4 Configuration
   A.5 Dev Edge Cases
   A.6 Dev Sign-off
B. QA / Browser Verification  [pre-release gate]
   B.1 UI / Browser Scenarios
   B.2 User-visible Edge Cases
   B.3 Regression (--include-regression 指定時)
   B.4 QA Sign-off
Appendix (optional)
```

YAML front matter は `dev_tester` / `dev_status` / `qa_tester` / `qa_status` を独立管理します。

各 scenario には必ず **具体的な Expected result** を含めます。「動作すること」などの曖昧表現は禁止です。

## Length Management Guidelines

Bloat 防止の内蔵原則:

1. **Prerequisites は common + audience 別 suffix に分離** — 重複禁止
2. **20 行超の verification query / script は `scripts/qa/*.sql` 等に切り出し** path のみ参照
3. **Regression は既存 testsheet への link で短縮** (重複記述禁止)
4. **長い troubleshooting / payload sample は `## Appendix`** に移動し本文から link

この 4 原則で M tier testsheet の大半は ~800 行以内に収まります。

## Language Detection

`--lang` 未指定時の優先順位:

1. **CLAUDE.md / AGENTS.md** の言語 directive (`PR言語: 日本語`, `Documentation: Korean` 等)
2. **Recent testsheets** の主要言語
3. **Project `README.md`** の言語
4. **Fallback** — English

YAML front matter の key、section 番号、template 骨格は `--lang` に関わらず英語固定です (Tooling reference)。

## Error Handling

| 状況 | 動作 |
| --- | --- |
| Input 未指定 | 中断し PR / Task / `--from-diff` を要求 |
| 複数 input 指定 | 中断しどの mode を意図したか確認 |
| `--split` + `--force-single` 両方 | 中断しどちらを意図したか確認 |
| `gh` 未認証 (PR input) | `gh auth login` 案内後に中断 |
| PR 未発見 | PR 番号を報告して中断 |
| Task 未発見 | 類似名 task 一覧 (fuzzy match) 表示後中断 |
| Diff が空 | 「nothing to test」と報告して中断 |
| Output directory 書き込み不可 | 失敗 path を報告して中断 (silent fallback しない) |
| 同 path に file 存在 | `-v<N>` suffix 自動付与 |
| L tier で `--split`/`--force-single` 未指定 | 中断し user に進行方法を確認 |

## Integration

- **ywc-sequential-executor** — Testsheet 対象の PR/Task を生成 (upstream)
- **ywc-parallel-executor** — 並列実行 flow の PR を生成 (upstream)
- **ywc-merge-dependabot** — Release 前 smoke testsheet 用の dependency PR を生成 (upstream)

## Example Prompt

### PR URL から生成 (default: 単一 file A+B)

```text
/ywc-gen-testcase https://github.com/acme/web-app/pull/250
```

### 物理 split (dev/qa 2 file)

```text
/ywc-gen-testcase 250 --split --lang ja
```

### QA 専用 testsheet (QA チーム引き渡し用)

```text
/ywc-gen-testcase 250 --audience qa --lang ja
```

### 大型 PR でも単一 file を強制

```text
/ywc-gen-testcase 250 --force-single
```

### Task ベース + regression 付き

```text
/ywc-gen-testcase 000001-010-db-create-users-table --include-regression
```

### Git Range (tag 間)

```text
/ywc-gen-testcase v1.2..v1.3 --lang ja
```

### Pre-PR local range

```text
/ywc-gen-testcase HEAD~5..HEAD
```

### Dry-run

```text
/ywc-gen-testcase 250 --dry-run
```

## Triggering

この Skill の trigger 条件は [SKILL.md](./SKILL.md) の `description` field に定義されています。
