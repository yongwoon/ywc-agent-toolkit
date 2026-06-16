<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-changelog-release-notes

一个用于从 git 历史记录、已合并的 PR 或 ywc-release-pr-list 输出中生成 CHANGELOG.md 条目和面向用户的发布说明的技能。
可生成技术性 CHANGELOG（Keep a Changelog 格式）和简明语言的面向用户发布摘要，作为独立文档输出。

## 核心概念：两种不同的输出

本技能生成**两种具有不同用途的文档**。

| | CHANGELOG.md | 发布说明 |
|---|---|---|
| 受众 | 开发者、维护者 | 最终用户、客户 |
| 包含内容 | 所有变更、CVE、PR 编号 | 仅用户可见的变更 |
| 语调 | 技术性、简洁 | 通俗语言、以利益为导向 |
| refactor/chore | 包含 | 省略 |

## 使用场景

### 情况 1：在标记新版本之前（最常见）

```
/ywc-changelog-release-notes --both --version 1.2.0
```

一次性生成面向开发者的 CHANGELOG.md 条目和面向用户的发布说明文档。
当需要为 GitHub Release 页面准备内容时使用此命令。

### 情况 2：仅更新 CHANGELOG.md

```
/ywc-changelog-release-notes --changelog
```

适用于没有外部用户的内部项目，仅需要面向开发者的变更历史时使用。
在创建 `git tag` 之前运行此命令。

### 情况 3：编写客户公告或 Slack 帖子

```
/ywc-changelog-release-notes --release
```

在编写面向用户的公告（如"v1.3.0 现已上线"）时使用。
技术细节会自动过滤，并从用户角度重新表述。

### 情况 4：修改文件前预览

```
/ywc-changelog-release-notes --dry-run
```

在实际修改文件之前，先查看将写入 `CHANGELOG.md` 的内容。
检查输出，如果内容正确则不带 `--dry-run` 重新运行。

### 情况 5：与 `ywc-release-pr-list` 配合使用

当已经准备好 PR 列表时，将其作为输入传递给本技能。

```
/ywc-release-pr-list > pr-list.md
/ywc-changelog-release-notes --both --pr-list pr-list.md --version 1.2.0
```

`ywc-release-pr-list` 以表格形式列出 PR；本技能将其**格式化**为可读、分类的 CHANGELOG 条目。

## 所有标志

```
/ywc-changelog-release-notes --changelog              # 仅生成 CHANGELOG.md 条目
/ywc-changelog-release-notes --release                # 仅生成面向用户的发布说明
/ywc-changelog-release-notes --both --version 1.2.0  # 生成两份文档
/ywc-changelog-release-notes --from v1.1.0 --to HEAD # 指定范围
/ywc-changelog-release-notes --dry-run               # 输出到 stdout，不修改文件
```

## 典型发布流程

```
1. ywc-release-pr-list          → 编译本次发布的 PR 列表
2. ywc-changelog-release-notes  → 生成 CHANGELOG + 发布说明
3. ywc-commit                   → 提交更新后的 CHANGELOG.md
4. ywc-create-pr                → 创建发布 PR
5. git tag -a v1.2.0 -m "..."   → 标记版本（技能会建议该命令）
```

## 相关技能

- `ywc-release-pr-list` — 生成用于 `--pr-list` 的 PR 列表
- `ywc-commit` — 提交更新后的 CHANGELOG.md
- `ywc-create-pr` — 创建发布 PR
- `ywc-incident-postmortem` — 驱动补丁版本发布的事故复盘
