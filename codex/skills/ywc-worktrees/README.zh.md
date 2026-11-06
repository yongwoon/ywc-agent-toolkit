# ywc-worktrees

用于管理隔离工作区的 git worktree 创建、审计、路径解析和清理。

它可以独立使用，也可以作为 executor 或 finish-branch 的 delegated helper。

## 现有分支与 PR worktree

`create` 只接受 `--base-branch` 或 `--existing-branch <H>` 之一。现有分支只使用精确的 local/origin ref，并区分不存在、传输失败、已 checkout、dirty 和 locked 状态后停止。
