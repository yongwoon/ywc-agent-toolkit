<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-review-learnings

一个 Skill，用于累积每个项目的 code-review preferences，让 review 质量随着时间提升。它以 runtime-agnostic 的形式实现 CodeRabbit 的 “learnings” 概念（不需要 hosted bot），并把内容存储为可提交的 Markdown 文件 `docs/review-learnings.md`，供 `ywc-impl-review` 在 review 前读取。

关键点是每条 learning 不只记录“做什么”，还记录“为什么”。这个 why 让 learning 能泛化到相似但不完全相同的情况，而不是退化成脆弱的 keyword match。

## Modes

- **read** — 加载与 review-target globs 匹配的 learnings，并注入 reviewers
- **update** — 从用户反馈、已完成 review 或 PR bot comments 中捕获新 learnings
- **list** — 显示当前 learnings
- **curate** — 废弃过时或冲突的 learnings（绝不 hard-delete）

## 何时使用

- 教 reviewer 某个 false positive 在你的环境中可接受，让它下次不再重复提出
- 把 recurring findings（例如 ownership-scoped query 缺少 owner-key predicate）积累为更早捕获的 durable rules
- 把你接受的 CodeRabbit / Codex PR comments 吸收到内部 review 中
- 在 AGENTS.md 或 CODEX.md 中加入读取 `docs/review-learnings.md` 的指令，让每个 Codex session 共享项目 review preferences

## 用法

```text
Use $ywc-review-learnings to update the project review learnings.
```

或使用自然语言：

> “this is a false positive, remember it”
> “load the review learnings that apply to this path”
> “turn PR #128's CodeRabbit comments into review learnings”
> “clean up the review learnings”

## 输入

- （可选）`--mode read|update|list|curate` — 强制 mode（省略时自动检测）
- （可选）`--target <glob|path...>` — review-target paths
- （可选）`--source feedback|review|pr` — update mode 的 learning source（默认 `feedback`）
- （可选）`--pr <number>` — 使用 `--source pr` 时要收集 bot comments 的 PR
- （可选）`--output <path>` — learnings file path（默认 `docs/review-learnings.md`）
- （可选）`--dry-run` — 显示 CHANGESET 但不写入

## 输出

- `docs/review-learnings.md` — `ID / Scope / Category / Polarity / Rule / Why / Provenance` 表
- update 时：`Learnings added` confirmation block，准确说明变更
- 首次创建文件时：建议在 AGENTS.md 或 CODEX.md 中加入指令，让未来 Codex sessions 读取 `docs/review-learnings.md`

## Related skills

- `ywc-impl-review` — review 前以 read mode 调用，review 后以 update mode 调用
- `ywc-handle-pr-reviews` — dismissed bot comment 可流入 `update --source pr`
- `ywc-ubiquitous-language` — 同样是 per-project knowledge-file architecture，但内容域不同
- `ywc-receive-review` — 负责回应 review feedback 的纪律；本 Skill 存储由此产生的 durable lesson
