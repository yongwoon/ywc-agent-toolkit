# Handoff

Content write 전에 생성 handle의 identity, regular type, expected owner, mode `0600`을 검증합니다. 실패 시 content write와 chown을 하지 않습니다. 빈 파일·미완성 파일 정리는 생성 identity 증명과 expected owner 일치 검증이 모두 필요하며 write/close 후 검증도 유지합니다.

Expected owner는 파일을 exclusive 생성한 권한 있는 aggregator 프로세스의 effective UID/user입니다. 파일 owner를 그 identity와 비교하고, 확인 불가·불일치 시 `NEEDS_CONTEXT`를 반환합니다. Chown하거나 소유권이 불확실한 파일을 건드리지 않습니다.

현재 대화와 명시적으로 붙여 넣거나 첨부한 artifact로 간결한 임시 Markdown 인수인계 파일을 만듭니다. Session log를 검색하거나 언급된 경로·URL을 열지 않습니다. 기존 artifact는 경로만 참조하며 내용을 복사하지 않고 credentials, tokens, 개인정보와 무관한 비공개 자료를 제거합니다.

Goal, State, Decisions, Dead ends, Next step, References, Suggested skills 순서의 7개 section을 포함합니다. 빈 항목에는 `N/A — <reason>`을 쓰며 상태나 결정을 만들지 않습니다. Read-only agent는 inline evidence만 반환하고 권한 있는 aggregator만 파일을 씁니다. Owner/input/output/status가 맞지 않으면 `NEEDS_CONTEXT`를 반환합니다.

Canonical `${TMPDIR:-/tmp}` root와 검증된 stable directory handle을 사용합니다. 파일명은 `ywc-handoff-`, timestamp, 정규화한 `[a-z0-9-]` slug, 고유 suffix로 구성합니다. 양끝 hyphen을 제거하고 빈 slug는 `session`으로 바꾸며, 정규화 후 48자를 넘으면 거부합니다. 외부·탈출·검증 불가 경로에는 쓰지 않습니다. Exclusive/no-follow 생성과 생성 시점의 `0600` 권한을 요구하며 기존 파일·symlink를 덮어쓰지 않습니다. 이름 충돌만 총 5회까지 시도합니다. 권한·쓰기 실패는 성공으로 보고하지 않고 중단하며 이번 작업이 새로 생성했음을 입증한 파일만 정리합니다.

파일 identity, owner, 권한, 완성된 redacted 내용을 검증한 뒤에만 `DONE`과 경로를 보고합니다. 임시 파일은 자동 삭제되지 않습니다. 영구 저장소로 이동하려면 사용자가 destination을 명시적으로 승인해야 합니다.

사용: `Use $ywc-handoff to save a concise handoff for this session.`

`allow_implicit_invocation: false`는 explicit invocation 선호 metadata이며 runtime 강제를 보장하지 않습니다. Eval과 source fixture는 지침 계약만 검증합니다. 안전한 격리 실행이 없으면 실제 model/tool/filesystem 동작은 `UNVERIFIED`입니다.
