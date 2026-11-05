# ywc-debug-rootcause

用于系统化调查 bug、测试失败、build 失败或异常行为。

在确认 root cause 和可复现证据之前，避免只修补表面症状。

## Analyst contract

`Caller: ywc-debug-rootcause` · `analysis_mode=debug_hypotheses`

明确提供 Caller 和 analysis_mode。缺失、未知或不匹配时返回 `NEEDS_CONTEXT`，不得推断。验证 Status → Summary → Finding counts → Analysis mode，并保留调用方原有 gate。

先记录最小 feedback loop 的失败及 catches/misses，排列 3–5 个可证伪假设，每次只改变一个变量。无法自动复现时记录手动证据和限制，不伪造 RED。三次修复失败后停止。仅当有效 debug 响应同时包含分别有证据支持的 `Fix #4 signal: fix harder` 和 `Next fix worth attempting: <one concrete minimal change>` 时，允许最后一次第四次尝试；失败后不得第五次尝试。

Live runtime: `UNVERIFIED — instruction contract only`.
