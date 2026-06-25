<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# Gen Testcase Skill（ywc-gen-testcase）

此 Claude Code Skill 接受 GitHub PR、已完成的任务目录或当前 git diff，生成**面向双受众的复选框驱动的 Markdown 测试表**：A 节面向开发者（合并前关卡），B 节面向 QA/浏览器（发布前关卡）。默认输出路径为项目的 `docs/test-case/` 目录。

后端工程师和 QA/PM/产品负责人可以各自独立并行签署自己的部分——因此合并决策和发布决策被清晰地分离。

## 使用方法

### 基本用法

从 PR URL 生成测试表：

```text
/ywc-gen-testcase https://github.com/acme/web-app/pull/250
```

在同一仓库中，PR 编号即可：

```text
/ywc-gen-testcase 250
```

### 基于任务的生成

```text
/ywc-gen-testcase 000001-010-db-create-users-table
```

### Git 范围生成

从任意提交范围生成。支持 SHA、标签、分支名和 `HEAD~N`。

```text
/ywc-gen-testcase v1.2..v1.3
/ywc-gen-testcase HEAD~5..HEAD
/ywc-gen-testcase main..feature-x
/ywc-gen-testcase --range abc1234..def5678
```

> 范围仅支持**双点 `A..B`** 形式。三点 `A...B` 被拒绝，因为其 merge-base 语义会静默地改变范围。
> 如果范围 HEAD 是开放/已合并 PR 的一部分（≥80% 提交重叠），Skill 会自动建议切换到 PR 模式——PR 正文/标签/验收标准能生成质量更好的场景。
> 如果提交消息质量较低（≥70% 的标题 ≤10 个字符），Skill 在继续前会发出警告。

### 基于 Diff 的生成

```text
/ywc-gen-testcase --from-diff
```

### 选项

| 选项 | 描述 | 示例 |
| --- | --- | --- |
| `--output-dir <path>` | 覆盖输出目录（默认：`docs/test-case/`） | `--output-dir ./qa/manual-tests` |
| `--lang <code>` | 测试表语言（`ja`、`ko`、`en`）。默认：自动检测 | `--lang ja` |
| `--filename <name>` | 文件名覆盖（不含 `.md`） | `--filename release-v2-smoke` |
| `--tasks-dir <path>` | 任务目录（默认：`tasks/`） | `--tasks-dir ./docs/tasks` |
| `--include-regression` | 添加回归测试节（B.3） | |
| `--audience <who>` | `dev` \| `qa` \| `both`。默认：`both`（单文件，A+B） | `--audience qa` |
| `--split` | 物理拆分为 `<slug>-dev.md` + `<slug>-qa.md` | |
| `--force-single` | 绕过 L 层级拆分建议；始终使用单文件 | |
| `--no-toc` | 禁止 M/L 层级的自动目录 | |
| `--from-diff` | 从 `git diff HEAD` 生成 | |
| `--range <spec>` | 明确的 git 范围（`A..B`）。等同于位置参数 | `--range v1.2..v1.3` |
| `--dry-run` | 仅显示生成计划（不写入文件） | |

> PR 标识符、任务规格、范围（`A..B`）和 `--from-diff` 互斥。`--split` 和 `--force-single` 互斥。如果传入不兼容的标志，Skill 会停止并询问您想要哪种模式。

## 双受众，双关卡

测试表的核心设计原则是按**"谁来运行，何时运行，使用哪些工具"**进行拆分。

| 节 | 受众 | 工具 | 关卡 |
| --- | --- | --- | --- |
| **A. 开发者验证** | 后端/DB/DevOps 工程师 | psql、gh CLI、curl、docker | **合并前**——合约、迁移、worker、容器 |
| **B. QA/浏览器验证** | QA、PM、产品负责人、设计师 | Chrome + DevTools、管理 UI、测试源 | **发布前**——终端用户体验及任何可在浏览器中观察到的效果 |

开发者和 QA 可以并行工作；每人只阅读自己的部分。

## 自动层级决策

布局根据场景数量自动选择，防止读者面对无法阅读的千行长文。

| 层级 | 场景数 | 布局 |
| --- | --- | --- |
| **S** | ≤ 20 | 单文件，A+B 节，无目录，无折叠 |
| **M** | 21–40 | 单文件，A+B 节，顶部自动目录，前提条件 + 边缘情况使用 `<details>` 折叠 |
| **L** | > 40 | 询问用户：带目录的单文件 / `--split` / 按阶段拆分，然后继续 |

大多数 PR 自然落在 S 或 M 层级；L 层级提示是大型发布的安全网。

## 执行周期

```text
步骤 1：输入解析
  └─ PR：通过 gh pr view / gh pr diff 获取元数据和 diff
  └─ 任务：从 <tasks-dir>/<name>/ 加载 task.md / README.md（优先 completed/）
  └─ Diff：捕获 git diff HEAD + 最近提交日志

步骤 2：受众和界面分类
  └─ 受众标签：A（开发者）或 B（QA/浏览器）
  └─ 界面：UI / 数据库 / API / 后台任务 / 配置 / 文档
  └─ 可在浏览器中观察的效果：即使是纯后端 PR，在适当时也添加 B 节

步骤 3：场景生成
  └─ 每（受众，界面）对 2–5 个场景
  └─ 每个场景：目标 / 前提条件 / 步骤 / 预期结果 / 复选框
  └─ 来源优先级：PR 正文或任务验收标准 > 提交 > 界面 > diff 边缘情况

步骤 4：层级决策
  └─ 计算场景数并决定 S / M / L
  └─ L 层级在写入前询问用户如何继续

步骤 5：写入测试表
  └─ 单文件（默认）或拆分（--split / --audience）
  └─ M/L 层级插入目录并将前提条件/边缘情况包装在 <details> 中
  └─ 如果目标已存在，追加 -v<N>（绝不覆盖）

步骤 6：验证并报告
  └─ 文件存在、复选框数量、具体预期结果、目录锚点
  └─ 报告层级/受众/界面摘要
```

## 默认文件名规则

| 输入 | 单文件（默认） | `--split` |
| --- | --- | --- |
| PR | `pr-<number>-<slug>.md` | `pr-<number>-<slug>-dev.md` + `...-qa.md` |
| 任务 | `task-<phase>-<sequence>-<slug>.md` | `...-dev.md` + `...-qa.md` |
| 范围 | `range-<short-start>-<short-end>-<slug>.md`（两端点均为标签时使用标签名，如 `range-v1.2-v1.3-<slug>.md`） | `...-dev.md` + `...-qa.md` |
| Diff | `<yyyymmdd-HHMM>-<branch-slug>.md` | `...-dev.md` + `...-qa.md` |

## 测试表结构（默认单文件）

```text
1. 摘要
2. 前提条件
   2.0 公共
   2.A 仅开发者
   2.B 仅 QA
A. 开发者验证  [合并前关卡]
   A.1 数据库/表
   A.2 API
   A.3 后台任务/Worker
   A.4 配置
   A.5 开发者边缘情况
   A.6 开发者签署
B. QA/浏览器验证  [发布前关卡]
   B.1 UI/浏览器场景
   B.2 用户可见的边缘情况
   B.3 回归（使用 --include-regression）
   B.4 QA 签署
附录（可选）
```

YAML front matter 携带 `dev_tester` / `dev_status` / `qa_tester` / `qa_status` 作为独立关卡。

每个场景必须包含**具体的预期结果**。禁止使用"检查是否正常工作"等模糊措辞。

## 长度管理指南

内置原则以防止内容膨胀：

1. **前提条件：公共前缀 + 受众后缀**——无重复
2. **超过 20 行的验证材料**提取到 `scripts/qa/*.sql`（或类似位置）；仅引用路径
3. **通过引用进行回归**——链接到之前的测试表而非重复
4. **长篇故障排除/载荷示例 → `## 附录`**，从相关场景链接

一致应用后，大多数 M 层级测试表保持在约 800 行以内。

## 语言检测

未指定 `--lang` 时的优先级：

1. **CLAUDE.md / AGENTS.md** — 如 `PR言語: 日本語`、`Documentation: Korean` 等指令
2. `docs/test-case/` 中**最近的测试表**
3. **项目 `README.md`** 语言
4. **回退** — 英语

无论 `--lang` 如何，YAML front matter 键、节编号和模板脚手架始终使用英语。

## 错误处理

| 情况 | 行为 |
| --- | --- |
| 未提供输入 | 停止；询问 PR / 任务 / `--from-diff` |
| 提供了多个输入 | 停止；询问哪种模式 |
| `--split` + `--force-single` 均设置 | 停止；询问意图 |
| `gh` 未认证（PR 输入） | 要求用户运行 `gh auth login`；停止 |
| PR 未找到 | 报告 PR 编号；停止 |
| 任务未找到 | 列出相似任务（模糊匹配）；停止 |
| 空 diff（diff 输入） | 报告"无需测试"；停止 |
| 输出目录不可写 | 报告失败路径；停止（无静默回退） |
| 目标文件已存在 | 追加 `-v<N>` 后缀 |
| 检测到 L 层级且未设置 `--split`/`--force-single` | 停止并询问用户如何继续 |

## 集成

位于面向实现的 `ywc` skills 的下游：

- **ywc-sequential-executor** — 生成待测试的 PR/任务（上游）
- **ywc-parallel-executor** — 同上，用于并行执行（上游）
- **ywc-merge-dependabot** — 需要冒烟测试表的已合并依赖升级（上游）

## 示例提示

### 从 PR URL 生成（默认：单文件 A+B）

```text
/ywc-gen-testcase https://github.com/acme/web-app/pull/250
```

### 物理拆分为两个文件

```text
/ywc-gen-testcase 250 --split --lang ja
```

### 仅 QA 测试表（交给 QA 团队）

```text
/ywc-gen-testcase 250 --audience qa --lang ja
```

### 即使是大型 PR 也强制单文件

```text
/ywc-gen-testcase 250 --force-single
```

### 带回归节的任务测试表

```text
/ywc-gen-testcase 000001-010-db-create-users-table --include-regression
```

### Git 范围（两个标签之间）

```text
/ywc-gen-testcase v1.2..v1.3 --lang ja
```

### 合并前本地范围

```text
/ywc-gen-testcase HEAD~5..HEAD
```

### 预演

```text
/ywc-gen-testcase 250 --dry-run
```

## 触发条件

此 Skill 的触发条件在 [SKILL.md](./SKILL.md) 的 `description` 字段中定义。
