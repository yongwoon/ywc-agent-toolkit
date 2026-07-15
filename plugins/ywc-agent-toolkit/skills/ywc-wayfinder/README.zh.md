# ywc-wayfinder

这是一个用于大型或高不确定性变更的 discovery Skill，适合跨多个 session 维护本地、可恢复的探索路线。它只允许一个 active ticket，并负责决定下一步 routing，而不是直接实现代码。

## 使用场景

- 在 ordinary planning 之前仍有太多 unresolved decision
- 需要跨多个 session 持续 discovery
- 需要 repo 内可审阅的本地 handoff，而不是外部 tracker write

## 核心约定

- canonical map path: `docs/ywc-plans/<slug>-wayfinder.md`
- 只允许一个 active ticket
- terminal resolved 返回 `DONE`，且不做最终写入
- terminal deferred / blocked 返回 `NEEDS_CONTEXT`，且不做最终写入
