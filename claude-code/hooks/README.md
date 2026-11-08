# Claude Code Hooks

`scripts/install.sh --hooks` 로 설치하는 7개의 실전 검증 Hook 스크립트 모음.

## Hook 목록

| 파일 | Event | Matcher | 역할 |
| ------ | ------- | --------- | ------ |
| `block-dangerous-commands.py` | `PreToolUse` | `Bash` | 위험 Shell 명령 차단 (3단계) |
| `check-claude-md-freshness.sh` | `PreToolUse` | `Bash` | git push 전 CLAUDE.md 최신성 검사 |
| `cost-tracker.py` | `PostToolUse` + `Stop` | `*` / (없음) | tool 호출 로깅 및 세션 summary |
| `notify-permission.py` | `Notification` | (없음) | permission 대기 시 Slack 알림 |
| `permission_request.py` | `PermissionRequest` | (없음) | 읽기 전용 tool 및 안전한 Bash 자동 승인 |
| `protect-secrets.py` | `PreToolUse` | `Read\|Edit\|Write\|Bash\|Grep\|Glob` | 비밀 파일 접근 차단 |
| `session_start.py` | `SessionStart` | (없음) | 세션 시작 시 context 주입 |

## 설치

```bash
# 전체 global 설치 (~/.claude/hooks/)
bash scripts/install.sh --hooks

# 전체 local 설치 (./.claude/hooks/)
bash scripts/install.sh --hooks --local

# 선택 설치
bash scripts/install.sh --hooks block-dangerous-commands cost-tracker

# 설치 가능 목록
bash scripts/install.sh --list --hooks
```

**의존성**: `jq` (필수), `uv` (Python Hook 실행용, 필수)

---

## 각 Hook 상세

### block-dangerous-commands.py

`PreToolUse` / matcher: `Bash`

Bash 명령이 실행되기 전 위험도를 판단해 차단한다.

- **critical** — `rm -rf /`, `chmod 777 /` 등 즉시 차단
- **high** — `sudo`, `dd`, `mkfs` 등 확인 요청
- **strict** — 프로젝트 루트 밖 쓰기 시도 차단

다음 세 규칙은 명령을 `;`, `&&`, `||`, `|` 단위로 나누고 `shlex`로 토큰화한 뒤, 대상 명령의 argv만 검사한다. heredoc 본문과 따옴표 안의 문자열은 검사하지 않는다. 그래서 `grep -n`이나 commit 메시지 속 `--no-verify` 같은 문자열 때문에 차단되지 않는다.

| id | 결정 | 대상 |
| --- | --- | --- |
| `git-no-verify` | deny | `git commit`의 `--no-verify` 또는 `-n`(`-anm` 같은 묶음 포함), `git push --no-verify`. `git push -n`은 dry run이므로 허용 |
| `gh-merge-admin` | deny | `gh pr merge --admin` |
| `git-add-all` | ask | `git add -A` / `--all` / `.` |

토큰화에 실패하면(따옴표 짝이 맞지 않는 경우 등) 그냥 허용하지 않고, 정규식으로 명령 전체를 검사한다.

**한계**: 이 hook은 model의 실수를 막는 guardrail이지 sandbox가 아니다. 다음 경우는 잡지 않는다.

- ANSI-C escape로 쓴 flag(`$'\x2dn'`)
- shell alias / function, git alias(`git ci -n`)
- 스크립트 파일 안에서 실행되는 명령(`./commit.sh`)
- `core.hooksPath` 변경처럼 hook 자체를 끄는 설정

**의존성**: `uv`, Python 3.11+

---

### check-claude-md-freshness.sh

`PreToolUse` / matcher: `Bash`

`git push` 명령이 포함된 Bash 호출을 감지해 `CLAUDE.md` 최신성을 확인한다.
CLAUDE.md가 최근 커밋 이후 수정되지 않았다면 push를 차단하고 업데이트를 요청한다.

**의존성**: `bash`, `git`

---

### cost-tracker.py

**두 이벤트에 등록됨** — `PostToolUse` (matcher: `*`) + `Stop` (matcher: 없음)

- `PostToolUse`: 각 tool 호출의 입출력 토큰을 로그에 기록
- `Stop`: 세션 종료 시 누적 비용 summary 출력

> `install.sh`는 이 Hook을 **두 event에 각각 별도로** settings.json에 등록한다.
> registry의 `events` 배열 구조를 통해 이 예외적 동작을 명시한다.

**의존성**: `uv`, Python 3.11+

---

### notify-permission.py

`Notification` / matcher: (없음)

permission 요청 대기 시 Slack Webhook으로 알림을 전송한다.

**환경변수 설정 필요**:

```bash
export CCH_SLA_WEBHOOK="https://hooks.slack.com/services/..."
```

설정하지 않으면 알림 없이 조용히 종료된다 (오류 없음).

**의존성**: `uv`, Python 3.11+, Slack Incoming Webhook URL

---

### permission_request.py

`PermissionRequest` / matcher: (없음)

`Read`, `Glob`, `Grep`와 allowlist에 포함된 안전한 `Bash` 명령에 대한 permission 요청을 자동 승인한다.
`Write`, `Edit`, `MultiEdit`, `WebFetch` 등 쓰기 또는 외부 접근 가능성이 있는 tool은 여전히 사용자 확인을 요청한다.

**의존성**: `uv`, Python 3.11+

---

### protect-secrets.py

`PreToolUse` / matcher: `Read|Edit|Write|Bash|Grep|Glob`

`.env`, SSH private key, credentials 파일 등에 대한 접근과 유출을 차단한다.
파일 경로 패턴과 내용 패턴을 모두 검사한다.
`Grep`은 `path`와 `glob`을, `Glob`은 `path`와 `pattern`을 검사한다. `~/.ssh`, `~/.aws` 같은 비밀 디렉터리와 `**/.env*` 같은 비밀 파일명 패턴을 검색하면 차단한다. `Grep`의 `pattern`은 파일 내용을 찾는 정규식이므로 검사하지 않는다.
glob 패턴은 brace(`{a,b}`)를 펼쳐서 검사한다. 또 대표적인 비밀 파일명(`.env`, `id_rsa` 등)과 매칭되는지 확인하므로 `**/.[e]nv`나 `**/id_*`도 차단된다. 단, `*.json`처럼 `*`로 시작하는 확장자 필터는 리터럴 부분만 검사한다.
home이나 `/` 전체를 대상으로 하는 `Grep`은 `glob`이나 `type`이 없으면 차단한다(`broad-search`).

기존 설치에서 matcher가 `Read|Edit|Write|Bash`였다면 `install.sh --hooks protect-secrets`를 다시 실행한다. 기존 matcher 그룹에 있던 같은 명령은 제거되고 새 matcher로 옮겨진다.

## 테스트

```bash
python3 claude-code/hooks/test_hooks.py
```

stdin으로 JSON payload를 넣고 hook의 결정(deny / ask / 허용)을 검증한다. `scripts/validate.sh`가 실행한다.

**의존성**: `uv`, Python 3.11+

---

### session_start.py

`SessionStart` / matcher: (없음)

세션 시작 시 다음 context를 시스템 프롬프트에 자동 주입한다:

- `git status` / 최근 커밋 요약
- `CONTEXT.md` (존재하는 경우)
- `TODO.md` (존재하는 경우)
- 열린 GitHub Issues (gh CLI 인증된 경우)

**의존성**: `uv`, Python 3.11+, `git`, `gh` (선택)
