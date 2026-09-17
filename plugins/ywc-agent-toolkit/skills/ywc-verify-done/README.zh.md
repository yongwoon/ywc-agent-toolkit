# ywc-verify-done

在声明工作完成、测试通过或 bug 已修复之前充当验证 gate。

最终结论必须包含当前会话中新鲜执行的命令证据。

## 可选：Gate Ledger

仅在多个命令或已接受的 subagent artifact 组成同一个声明时追加使用。已安装 checker 的 `--status` 不启动 subprocess 且保持 bytes 不变；bare mode 只恢复没有精确 cached `PASS` 的 gate，`--reverify` 则 fresh 执行所有 runnable gate。`MANUAL` gate 会跳过。`CHECK` 是任意 shell，执行前必须检查；验证不存在时请使用 positive control。PR-ready 声明仍需独立的 600 秒 review poll、`--verify` head-SHA、CI 和 PR-health 证据。语法见 [gate-ledger.md](./references/gate-ledger.md)。
