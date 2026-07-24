# CHANGELOG

이 프로젝트에서 진행한 작업을 날짜순으로 기록한다. 커밋 메시지의 "무엇을"보다
"왜 그렇게 결정했는지"를 남기는 데 초점을 둔다.

## 2026-07-24 (5인 이상 팀 템플릿으로 구성)

`Claude_Codex_최적화_템플릿_1~4인프로젝트`를 기반으로, 여러 명이 각자 자신의 Claude Code(+Codex CLI)
세션으로 같은 저장소를 동시에 작업하는 상황에 맞춰 아래 항목을 추가/변경했다.

- **`.claude/rules/team-collaboration.md` 신설**: 브랜치 전략(기능 브랜치 + PR, main/master 직접 커밋 금지),
  담당 범위 기반 충돌 방지, DESIGN.md 동기화, PR 리뷰, 핸드오프 규칙을 명문화했다. 1인 개발 템플릿에는
  없던, 팀 규모가 커지면서 필요해지는 조율 규칙이다.
- **`.claude/docs/OWNERSHIP.md` + `.github/CODEOWNERS` 신설**: 담당 모듈이 표로도(사람이 읽는 문서),
  자동으로도(GitHub PR 리뷰어 자동 지정) 드러나도록 두 파일을 짝지었다.
- **`.claude/docs/handoff/` 신설**: 세션 종료 시점에 작업이 끝나지 않았으면 다음 사람이 이어받을 수 있도록
  상태를 남기는 템플릿을 추가했다. 1인 프로젝트에서는 인수인계가 필요 없어 생략됐던 부분이다.
- **`.claude/hooks/check-branch-before-write.py` 추가**: 기존 5개 hook과 같은 "제안만 하고 차단하지 않는다"
  원칙을 유지하면서, main/master에서 직접 파일을 수정하려는 시점에 기능 브랜치 생성을 제안하도록 했다.
  `.claude/settings.json`의 `Edit|Write` PreToolUse matcher에 등록했다.
- **`.github/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/*` 추가**: 리뷰어가 여러 명일 때 PR/이슈
  형식이 사람마다 달라지는 것을 막기 위해 표준 템플릿을 넣었다.
- **CI에 `concurrency` 그룹 추가**: 팀원 여러 명이 같은 브랜치/PR에 연속으로 push하면 이전 CI 실행이 낭비되므로
  `cancel-in-progress: true`로 최신 커밋만 검사하도록 했다.
- **`settings.json` 권한 확장**: 브랜치 기반 워크플로에서 자주 쓰는 되돌리기 쉬운 명령
  (`git branch`, `git checkout -b`, `git fetch`, `git rev-parse`)을 허용 목록에 추가했다. `push`, `merge`,
  `rebase --onto` 등 상태를 바꾸는 명령은 여전히 매번 확인을 거치도록 제외했다.
- **CLAUDE.md / README.md / `.codex/AGENTS.md` / 관련 스킬 문서 갱신**: 규칙 6개→7개, hook 5개→6개로 늘어난
  내용을 반영하고, `/init` 스킬 체크리스트에 팀 오너십·브랜치 보호 설정 단계를 추가했다.
- 원본 템플릿의 `.claude/rules/`(언어·코딩 원칙·개발 환경·보안·테스트), `.claude/hooks/`의 기존 5개,
  `.claude/skills/`(13개), `.codex/`, CI/pre-commit/에디터 설정은 1인~4인 템플릿과 동일하게 유지했다 — 팀
  규모와 무관하게 유효한 규칙이기 때문이다.
