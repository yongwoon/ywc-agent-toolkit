# ywc-codex-toolkit-eval

이 Repository의 Codex `ywc-*` Skill과 Codex custom Agent 품질을 평가하는 로컬 관리 Skill입니다. `inventory_gate.py`로 구조 증거를 모으고, `score.py`로 mechanical axes를 채점한 뒤, 0-4 rubric 기반 judgment pass로 최종 grade와 개선 backlog를 만듭니다.

이 Skill은 배포 대상이 아닙니다. `.codex/skills/ywc-codex-toolkit-eval/` 아래에만 두고, `codex/skills/` 또는 `.codex-plugin/skills/`에 포함하지 않습니다.

## 사용 시나리오

- Codex Skill/Agent 전체 품질 평가를 정기적으로 실행할 때
- Codex bundle 변경 후 mechanical regression gate를 확인할 때
- 평가 결과를 `docs/skill-agent-eval/codex/` report와 scoreboard로 남길 때

## 사용 방법

```bash
$ywc-codex-toolkit-eval --target all
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/inventory_gate.py --json
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --mode mechanical --target codex/skills --format markdown
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/score.py --ci
```

## 출력

- `docs/skill-agent-eval/codex/` — Codex Skill/Agent 평가 report
- `docs/skill-agent-eval/codex/scoreboard.md` — rolling scoreboard
- `evals/history.mechanical.json` — reviewed mechanical baseline

## CI 경계

PR에서는 schema, lint, registry, fake-adapter 검사만 수행합니다.

```bash
python3 .codex/skills/ywc-codex-toolkit-eval/scripts/runner.py --adapter fake --suite mocked
```

Live 평가는 scheduled/manual 경로에만 있으며 명시적인 credential-provider
handoff와 API-egress policy가 모두 필요합니다. 둘 중 하나라도 없으면 조용히
성공하지 않고 `SKIPPED_UNAVAILABLE`(exit 3)을 보고합니다. Ablation은
manual-only이며 `INCONCLUSIVE=0`은 이 경로에서만 허용되고 retire 결정으로
사용되지 않습니다. 보고서는 gitignore된
`docs/skill-agent-eval/codex/runs/<run-id>/` 아래에 저장하며, 업로드 전
redaction 및 10 MB cap을 적용하고 실패 실행은 최대 7일만 보존합니다.

## 관련 Skill

- `ywc-skill-author` — Codex Skill 구조와 authoring rule의 출처
- `.claude/skills/ywc-toolkit-eval` — Claude Code Skill/Agent 평가용 별도 Skill
