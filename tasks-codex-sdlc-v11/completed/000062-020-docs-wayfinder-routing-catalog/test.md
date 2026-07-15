# 000062-020-docs-wayfinder-routing-catalog — Test Scenarios

1. ordinary planning prompt fixture를 evaluate한다.
   - Expected Result: `ywc-plan`/brainstorm route를 유지하고 Wayfinder를 불필요하게 호출하지 않는다.
2. multi-session unresolved-decision prompt fixture를 evaluate한다.
   - Expected Result: Wayfinder route와 local map handoff가 제시된다.
