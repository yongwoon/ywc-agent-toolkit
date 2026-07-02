<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-spec-ready

本文介绍 Codex `ywc-spec-ready` workflow。权威的触发条件、anti-triggers、执行步骤和输出格式定义在 [SKILL.md](./SKILL.md)。

## 本地化版本

- [한국어](./README.md)
- [English](./README.en.md)
- [日本語](./README.ja.md)
- [한국어 full](./README.ko.md)
- [Español](./README.es.md)

## 何时使用

- natural-language goal 必须先变成 validated spec，再进入 task generation。
- 现有 spec 必须在 `ywc-task-generator` 前达到 `ywc-spec-validate` 的 `DONE`。
- `DONE_WITH_CONCERNS` 需要在严格上限内通过重复 `ywc-plan --update-spec` loop 处理。

## 用法

```bash
$ywc-spec-ready "Design payment failure recovery UX"
$ywc-spec-ready --spec docs/ywc-plans/example.md --max-iterations 4
$ywc-spec-ready --spec docs/ywc-plans/example.md --dry-run
```

成功时，本 Skill 打印 `ywc-task-generator <spec-path>` 并停止。它不会直接生成 tasks 或实现 code。

## 输出

本 Skill 遵循 [SKILL.md](./SKILL.md) 中定义的 report、loop log 和 status format。
