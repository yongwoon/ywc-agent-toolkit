# 000062-030-refactor-task-generator-preview-core — Test Scenarios

1. `--preview-only` with valid spec fixture를 run한다.
   - Expected Result: canonical preview/revision/digest만 생성되고 task directory/graph는 없다.
2. symlink/traversal/mismatched identity fixture를 run한다.
   - Expected Result: `NEEDS_CONTEXT`, write 없음.
3. phase/batch/dependency 변경 fixture를 run한다.
   - Expected Result: digest가 달라져 fresh approval이 필요하다.
