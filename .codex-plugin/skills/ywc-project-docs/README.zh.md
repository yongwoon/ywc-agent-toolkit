<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# project-docs

一个 Codex Skill，用于生成遵循项目 `docs/` 目录结构和规范的韩语或日语文档。

目标语言根据对话上下文自动选择。默认为**韩语**；当对话使用日语或明确要求日语时切换为日语。

## 使用方法

### 自动触发

以下自然语言短语可激活此 Skill：

```
"문서 작성해줘"       （韩语：写一个文档）
"문서 만들어줘"       （韩语：创建一个文档）
"document this"
"write a doc"
"add to docs/"
"ドキュメント作成して" （日语：创建文档）
"ドキュメントを書いて" （日语：写文档）
```

### 手动调用

```
/project-docs
```

## 此 Skill 的功能

1. **语言选择** — 检测对话语言并以韩语或日语生成内容
2. **目录路由** — 根据意图将文档放置在正确的 `docs/` 子目录中
3. **命名规范** — 应用小写 kebab-case，最少后缀
4. **文档结构** — 生成相关文档块、目录和编号章节
5. **交叉引用** — 在相关文档之间添加双向链接
6. **语言策略** — 正文使用所选语言；技术术语保留英文（不音译）
7. **阅读顺序** — 保留 `产品 → 架构 → 规范 → 计划` 的 LLM 消费顺序
8. **反模式** — 防止文件夹边界混合、重复存储和草稿/正式文档混淆

## 目录映射

### 主轴（核心文档）

| 请求类型 | 目标目录 |
|---|---|
| 产品目标、范围、PRD | `docs/product/` |
| 系统设计、技术决策 | `docs/architecture/` |
| 功能规则、实现标准 | `docs/specification/` |
| 实现顺序、里程碑 | `docs/plans/` |

### 次轴（运营、资产、草稿）

| 请求类型 | 目标目录 |
|---|---|
| 运营流程、设置指南 | `docs/manuals/` |
| 事故处理、已知问题 | `docs/troubleshooting/` |
| UI 原型、设计资产 | `docs/design/` |
| 辅助图片 | `docs/imgs/` |
| 未确认的想法、临时笔记 | `docs/todo/` |

## 示例

```
"제품 개요 문서 작성해줘"
→ docs/product/product-overview.md（韩语）

"인증 시스템 아키텍처 문서 작성해줘"
→ docs/architecture/authentication.md（韩语）

"認証システムのアーキテクチャドキュメントを書いて"
→ docs/architecture/authentication.md（日语）
```

## 本地化版本

- [韩语（主要）](./README.md)
- [日语](./README.ja.md)
- [韩语](./README.ko.md)
