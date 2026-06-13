# ywc-review-learnings

Project별 Code Review 선호를 누적하여 Review 퀄리티를 시간이 지날수록 높이는 Skill입니다. CodeRabbit의 "learnings" 개념을 runtime 비의존(특정 bot 없이도 동작) 형태로 구현하여, `docs/review-learnings.md`라는 commit 가능한 Markdown 파일로 관리합니다. `ywc-impl-review`가 Review 직전에 이 파일을 불러와 적용합니다.

핵심은 각 learning이 *무엇을(what)* 뿐 아니라 **왜(why)** 까지 기록한다는 점입니다. Why가 있어야 유사하지만 동일하지 않은 상황에도 일반화되며, 단순 keyword match로 전락하지 않습니다.

## 지원 Mode

- **read** — Review 대상 파일 glob에 해당하는 learning을 불러와 Reviewer에 주입
- **update** — feedback / 완료된 review / PR bot comment에서 신규 learning 포착
- **list** — 현재 learning 목록 표시
- **curate** — stale하거나 모순되는 learning을 deprecate (hard-delete 금지)

## 사용 시나리오

- Review에서 나온 false positive를 "이건 우리 환경에선 괜찮아"라고 학습시켜 다음 review부터 재지적을 막고 싶을 때
- 반복되는 지적(예: ownership-scoped query의 owner-key 누락)을 미리 잡도록 규칙으로 누적하고 싶을 때
- CodeRabbit / Codex가 단 PR comment 중 받아들인 것을 internal review에 흡수하고 싶을 때
- Codex session이 Project별 review 선호를 자동으로 이해하도록 AGENTS.md 또는 CODEX.md에 `docs/review-learnings.md` 참조를 추가하고 싶을 때

## 사용 방법

```text
Use $ywc-review-learnings to update the project review learnings.
```

또는 자연어로 호출:

> "이건 false positive 야, 학습해둬"
> "이 경로에 적용되는 review learnings 불러와줘"
> "PR #128 의 CodeRabbit 코멘트를 review 학습으로 남겨줘"
> "review learnings 정리해줘"

## 입력

- (선택) `--mode read|update|list|curate` — Mode 강제 지정 (생략 시 자동 감지)
- (선택) `--target <glob|path...>` — Review 대상 경로 (read 시 적용 범위, update 시 귀속)
- (선택) `--source feedback|review|pr` — update 시 learning 출처 (기본 `feedback`)
- (선택) `--pr <번호>` — `--source pr` 와 함께 bot comment harvest 대상 PR
- (선택) `--output <경로>` — learning 파일 경로 (기본: `docs/review-learnings.md`)
- (선택) `--dry-run` — 쓰기 없이 CHANGESET만 표시

## 출력

- `docs/review-learnings.md` — `ID / Scope / Category / Polarity / Rule / Why / Provenance` Table
- update 시: 변경 내역을 명시하는 `Learnings added` 확인 block 출력
- 최초 파일 생성 시: AGENTS.md 또는 CODEX.md에 `docs/review-learnings.md`를 읽으라는 project instruction 추가를 권장하는 활성화 안내 출력

## 출력 예시

```markdown
# Review Learnings — ShopBot

<!-- updated: 2026-06-13 -->

## Learnings

| ID   | Scope        | Category | Polarity       | Rule | Why | Provenance |
|------|--------------|----------|----------------|------|-----|-----------|
| L001 | `**/*.sql`   | Security | DO             | ownership-scoped table 의 모든 query 는 owner-key 조건을 명시한다 | App-layer filtering 은 query 하나가 WHERE owner_id=? 를 빠뜨리는 순간 fail-open 한다 | PR#42, 2026-06-13 |
| L002 | `**/*.test.ts` | Test   | FALSE-POSITIVE | test setup 파일의 top-level await 를 missing-await bug 로 지적하지 않는다 | 해당 runner 가 top-level await 를 지원하므로 지적은 noise | dismissed PR#51, 2026-06-13 |
```

## 관련 Skill

- `ywc-impl-review` — Review 직전 read mode 로 이 Skill 을 호출하고, Review 후 update mode 로 학습을 누적
- `ywc-handle-pr-reviews` — dismiss 된 bot comment 를 `update --source pr` 로 흘려보낼 수 있음
- `ywc-ubiquitous-language` — 동일한 per-project 지식 파일 architecture (read/update, 사용자 확인 후 쓰기), 다른 도메인 (review 선호 vs 도메인 어휘)
- `ywc-receive-review` — Review feedback 에 *대응* 하는 discipline. 이 Skill 은 그 feedback 이 남긴 *지속적 교훈* 을 저장
