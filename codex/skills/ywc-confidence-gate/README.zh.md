# ywc-confidence-gate

在启动非平凡实现或委派给 code generation / executor 之前，评估当前方案是否已经准备好。

它基于范围清晰度、架构一致性、证据质量、复用检查和 root cause 给出 PROCEED / REVIEW / STOP。

## Analyst contract

`Caller: ywc-confidence-gate` · `analysis_mode=confidence_root_cause`

明确提供 Caller 和 analysis_mode。缺失、未知或不匹配时返回 `NEEDS_CONTEXT`，不得推断。验证 Status → Summary → Finding counts → Analysis mode，并保留调用方原有 gate。

只返回一个原因候选及其支持和反对证据，不添加排序的替代假设或 5 Whys。拒绝也消耗一次 dispatch budget；评分和 band 决策由调用方保留。

Live runtime: `UNVERIFIED — instruction contract only`.
