# 000062-040-docs-task-generator-preview-assets — Test Scenarios

1. preview-only → approved consume fixture를 run한다.
   - Expected Result: identical identity/digest succeeds; no re-decomposition occurs.
2. custom preview path, stale digest, missing spec and symlink escape fixtures를 run한다.
   - Expected Result: each returns `NEEDS_CONTEXT` before task artifacts are written.
3. wide-refactor batch boundary fixture를 run한다.
   - Expected Result: metadata is represented in preview, template and graph contract.
