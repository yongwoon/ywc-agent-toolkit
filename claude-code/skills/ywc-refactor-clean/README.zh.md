<!-- AUTO-GENERATED: This file was translated by Claude AI from README.en.md.
     Community review and corrections are welcome.
     Source: README.en.md | Language: Chinese (Simplified) -->

# ywc-refactor-clean

由检测工具（knip / depcheck / ts-prune / vulture / deadcode / cargo-udeps）支持的死代码移除 Skill。检测结果被分类为 SAFE / CAUTION / DANGER 三个层级，逐项删除，并在每次删除前后运行范围受限的 Test，最后以遵循 `ywc-verify-done` evidence-block 格式的 Verification Report 收尾。行为变更（例如需要语义协调的重复合并）明确超出范围，会路由到 `ywc-tdd-ritual` + `ywc-code-gen`。

## 本地化版本

- [한국어 (entry)](./README.md)
- [日本語](./README.ja.md)
- [한국어](./README.ko.md)

## 何时使用

- 用户说 "remove dead code"、"run knip"、"clean unused imports"
- 在一个 sprint 之后，作为每月定期的卫生清理，在其独立的 branch 上进行
- 当 `ywc-onboard-repo` 检测到在刚进入的 repo 中死代码堆积妨碍架构理解时

## 如何调用

```bash
/ywc-refactor-clean --scope src/ --tier safe
```

或使用自然语言：

> "clean up the dead code"
> "run knip and remove the safe findings"

## 铁律

**没有三个见证者绝不删除**：(1) 检测工具标记它，(2) grep 找不到任何引用，(3) 每个批次后 Test 保持通过。

## 输入

- （可选）`--scope <dir>` — 将检测 + 删除限制在某个路径（默认：repo root）
- （可选）`--tier safe | safe+caution | all` — 在指定层级后停止（默认：`safe`）
- （可选）`--dry-run` — 生成报告而不改动文件
- （可选）`--skip-verify-done` — 仅当上游调用方自行处理 verify-done 时有效

## 输出

- 逐项的 commit 系列（`chore(cleanup): remove unused <symbol> (knip)`）
- 最终的 Verification Report（Output Format — 嵌入 `ywc-verify-done` 的 evidence block）
- 未删除的 DANGER 层级项列表（建议放入独立的 PR）

## 相关 Skill

- `ywc-verify-done` — 强制的 Step 7 handoff；提供 PASS / FAIL evidence-block 格式
- `ywc-tdd-ritual` — 当合并需要行为协调时的升级目标
- `ywc-code-gen` — 涉及行为变更的清理属于这里，而非本 Skill
- `ywc-confidence-gate` — 通过 5 维度评分标准处理边界 CAUTION ↔ DANGER 分类
- `ywc-onboard-repo` — 进入新 repository 后的上游调用方
