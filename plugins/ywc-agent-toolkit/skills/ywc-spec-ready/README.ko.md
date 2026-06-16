# ywc-spec-ready

이 문서는 Codex `ywc-spec-ready` workflow 안내입니다. 정확한 trigger, anti-trigger, 실행 절차, output format은 [SKILL.md](./SKILL.md)를 기준으로 합니다.

## Localized Versions

- [한국어](./README.md)
- [English](./README.en.md)
- [日本語](./README.ja.md)

## 사용 시나리오

- 자연어 goal을 spec으로 만들고 validation loop까지 마쳐야 할 때
- 기존 spec을 `ywc-task-generator` 전에 `DONE` 상태까지 검증해야 할 때
- `DONE_WITH_CONCERNS`를 `ywc-plan --update-spec`로 반복 수렴시켜야 할 때

## 사용 방법

```bash
$ywc-spec-ready "결제 실패 복구 UX를 설계해줘"
$ywc-spec-ready --spec docs/ywc-plans/example.md --max-iterations 4
$ywc-spec-ready --spec docs/ywc-plans/example.md --dry-run
```

성공 시 이 Skill은 `ywc-task-generator <spec-path>`를 출력하고 멈춥니다. 직접 task 생성이나 implementation은 수행하지 않습니다.

## 출력

이 Skill은 [SKILL.md](./SKILL.md)에 정의된 report, loop log, status format을 따릅니다.
