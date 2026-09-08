# Mine Review History

여러 Merge 완료 PR의 Bot Review Comment를 제한된 범위에서 조사해 반복 결함 Class와 확인 기반 학습 변경안을 제시하는 Codex Skill입니다.

`--limit` 또는 `--since`가 필요하며, 반복 횟수는 서로 다른 PR 기준입니다. 해소/후속 수정 또는 명시적 사람의 기각 근거가 없는 Comment는 보수적으로 제외합니다. 확인 전에는 어떤 파일도 쓰지 않으며, 로컬 학습 저장은 `$ywc-review-learnings --mode update --source mining`에 위임하고 공유 Catalog는 Maintainer 제안만 출력합니다.

```text
$ywc-mine-review-history --limit 50
$ywc-mine-review-history --since 2026-01-01 --min-recurrence 4
```

자세한 계약은 [SKILL.md](./SKILL.md)를 참고하세요.
