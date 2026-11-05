# ywc-tdd-ritual

在实现功能、bug fix 或行为变更前，执行 RED -> GREEN -> REFACTOR 的 TDD 流程。

它要求先看到测试失败，再实现生产代码，避免事后补测试。

## 编写反馈契约

记录现有 public test seam 的 catches/misses，完成一个行为的 RED/GREEN/REFACTOR 后再开始下一个。没有合适 seam 时保留复现证据并提出必要的接口决策。
