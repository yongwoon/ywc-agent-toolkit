<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-review-learnings

一个按项目积累 code-review 偏好的 Skill，使 review 质量随时间不断提升。它以运行时无关的形式（无需托管 bot）实现了 CodeRabbit 的 "learnings" 概念，存储为可提交的 Markdown 文件 `docs/review-learnings.md`，供 `ywc-impl-review` 在 review 前加载。

其关键特性在于：每条 learning 不仅记录*该做什么*，还记录**为什么**。这个 why 正是让一条 learning 能够推广到相似但不完全相同的情况，而不是退化为脆弱的 keyword 匹配。

## 模式

- **read** — 加载 scope 与 review 目标 glob 匹配的 learnings，并注入到 reviewer 中
- **update** — 从用户反馈、已完成的 review 或抓取的 PR bot 评论中捕获新的 learnings
- **list** — 显示当前的 learnings
- **curate** — 弃用陈旧或矛盾的 learnings（绝不硬删除）

## 何时使用

- 教会 reviewer 某个 false positive 在你的环境中是可接受的，使其下次 review 时不再重复提出
- 将反复出现的 findings（例如 ownership-scoped 查询上缺失 owner-key 谓词）积累为更早捕获的持久规则
- 吸收你接受的 CodeRabbit / Codex PR 评论到内部 review 中
- 将 `@docs/review-learnings.md` 添加到 CLAUDE.md，使每个 LLM session 共享项目的 review 偏好

## 使用方法

```bash
/ywc-review-learnings
```

或使用自然语言：

> "this is a false positive, remember it"
> "load the review learnings that apply to this path"
> "turn PR #128's CodeRabbit comments into review learnings"
> "clean up the review learnings"

## 输入

- （可选）`--mode read|update|list|curate` — 强制指定模式（省略时自动检测）
- （可选）`--target <glob|path...>` — review 目标路径
- （可选）`--source feedback|review|pr|debug|incident` — update 模式的 learning 来源（默认 `feedback`；`debug`/`incident` 捕获 root-cause / 事故预防项）
- （可选）`--pr <number>` — 通过 `--source pr` 抓取 bot 评论的 PR
- （可选）`--output <path>` — learnings 文件路径（默认 `docs/review-learnings.md`）
- （可选）`--dry-run` — 显示 CHANGESET 而不写入

## 输出

- `docs/review-learnings.md` — 一个 `ID / Scope / Category / Polarity / Rule / Why / Provenance` 的表格
- update 时：一个 `Learnings added` 确认块，准确说明发生了哪些变更
- 首次创建文件时：一个激活提示，建议你将 `@docs/review-learnings.md` 添加到 CLAUDE.md（正是这个引用使得每次未来的 review 和 LLM session 自动加载这些 learnings）

## 输出示例

```markdown
# Review Learnings — ShopBot

<!-- updated: 2026-06-13 -->

## Learnings

| ID   | Scope          | Category | Polarity       | Rule | Why | Provenance |
|------|----------------|----------|----------------|------|-----|-----------|
| L001 | `**/*.sql`     | Security | DO             | Every query on an ownership-scoped table includes the owner-key predicate | App-layer filtering fails open the moment one query forgets WHERE owner_id=? | PR#42, 2026-06-13 |
| L002 | `**/*.test.ts` | Test     | FALSE-POSITIVE | Do not flag top-level await in test setup files | The runner supports it; flagging it is noise | dismissed PR#51, 2026-06-13 |
```

## 相关 Skill

- `ywc-impl-review` — 在 review 前以 read 模式、review 后以 update 模式调用本 Skill
- `ywc-handle-pr-reviews` — 一条被驳回的 bot 评论可以馈送到 `update --source pr`
- `ywc-ubiquitous-language` — 相同的按项目 knowledge-file 架构，不同的内容领域
- `ywc-receive-review` — 用于*回应* review 反馈的纪律；本 Skill *存储*它产生的持久经验
