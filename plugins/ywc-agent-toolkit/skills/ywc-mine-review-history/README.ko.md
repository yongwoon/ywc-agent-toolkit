# Mine Review History

Merge된 PR의 Bot Review Comment를 제한된 범위에서 일괄 조사하고, 서로 다른 PR에 반복된 결함 Class를 확인 게이트가 있는 review-learning 후보로 제시하는 Codex Skill입니다. `--limit` 또는 `--since`가 필수이며, 근거가 불완전하면 보수적으로 제외합니다.

프로젝트 학습 파일은 직접 쓰지 않고 `$ywc-review-learnings --mode update --source mining`에 위임합니다. 공유 Catalog는 Maintainer 제안만 출력합니다.

자세한 내용은 [SKILL.md](./SKILL.md)를 참고하세요.
