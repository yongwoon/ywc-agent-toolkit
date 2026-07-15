# 000062-010-docs-wayfinder-core — Test Scenarios

1. New destination map fixture를 실행한다.
   - Expected Result: canonical map fields와 하나의 active ticket이 생성된다.
2. invalid ticket resume fixture를 실행한다.
   - Expected Result: `NEEDS_CONTEXT`, map write 없음.
3. all-resolved 및 deferred terminal fixture를 실행한다.
   - Expected Result: 각각 `DONE` 및 `NEEDS_CONTEXT`, write 없음.
