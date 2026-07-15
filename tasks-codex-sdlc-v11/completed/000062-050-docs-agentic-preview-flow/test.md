# 000062-050-docs-agentic-preview-flow — Test Scenarios

1. normal Medium Task Phase fixture를 run한다.
   - Expected Result: both calls use the same `--spec`; preview evidence is logged before approved consume.
2. stale/missing/mismatched preview and direct bypass fixtures를 run한다.
   - Expected Result: `NEEDS_CONTEXT`, task artifacts 없음.
