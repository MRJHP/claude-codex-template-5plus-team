# CHANGELOG

이 프로젝트에서 진행한 작업을 날짜순으로 기록한다. 커밋 메시지의 "무엇을"보다
"왜 그렇게 결정했는지"를 남기는 데 초점을 둔다.

## 2026-07-28

- **Windows 한글 경로에서 pre-commit hook 인코딩 깨지는 문제 발견 및 해결법 기록**: 저장소 경로에
  `박주형`처럼 한글(비 ASCII)이 포함된 상태에서 `uv run pre-commit install`을 실행하면, `.git/hooks/pre-commit`
  스크립트에 그 경로를 UTF-8이 아닌 시스템 로케일(CP949)로 잘못 인코딩해서 쓰는 경우가 있었다. Git Bash는
  hook 스크립트를 UTF-8로 해석하므로 `INSTALL_PYTHON` 경로가 실제 `.venv` 경로와 어긋나
  `` `pre-commit` not found. Did you forget to activate your virtualenv? `` 에러로 `git commit`이 실패했다.
  `PYTHONUTF8=1 uv run pre-commit install --overwrite`로 hook을 재설치하면 해결된다. 자매 저장소
  (`claude-codex-optimized-template-under-4-members`)에서 먼저 발견해 동일하게 반영했다.
  [dev-environment.md](.claude/rules/dev-environment.md) 참고.
- **`/init`으로 템플릿 예제를 실제 패키지명으로 교체**: `src/project/__init__.py`,
  `tests/test_project.py`를 `src/my_project/`, `tests/test_my_project.py`로 바꾸고 `pyproject.toml`의
  프로젝트명을 갱신했다. 구체적인 실제 기능은 아직 정해지지 않아 `greet` 예제는 그대로 두었다. 이 저장소의
  `team-collaboration.md` 규칙에 따라 `chore/init-and-precommit-fix` 기능 브랜치 + PR로 반영했다.

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

## 2026-07-24 (CODEOWNERS 변경사항 push 및 병합)

로컬에만 있던 CODEOWNERS 기본 오너 임시 지정 커밋을 GitHub에 반영했다.

- `master`가 보호 브랜치라 직접 push가 거부되어(`GH006`), `chore/push-codeowners-update` 기능
  브랜치로 push 후 PR(#2)을 생성했다 — team-collaboration.md의 브랜치 전략을 그대로 따른 사례다.
- CODEOWNERS 기본 오너가 PR 작성자 본인(`@MRJHP`)과 같아 리뷰어로 자신을 지정할 수 없었다(GitHub
  정책상 작성자는 자기 PR을 리뷰할 수 없음). 아직 팀원이 CODEOWNERS에 실제로 채워지지 않은 초기
  상태라 리뷰어 없이 CI 통과만 확인하고 병합했다 — 팀원이 합류하면 CODEOWNERS를 실제 핸들로
  갱신해 이 문제가 재발하지 않도록 해야 한다.
- 병합 후 로컬/원격 기능 브랜치를 정리했다.

## 2026-07-24 (`uv run` 트램폴린 오류 원인 파악 및 개발 환경 점검)

`uv run pytest`가 `error: uv trampoline failed to canonicalize script path`로 실패하는 문제를
조사하고 해결했다.

- **원인**: 이 프로젝트 폴더가 원래 `Claude_Codex_최적화_템플릿_...` 이름의 폴더였다가
  `claude-codex-template-5plus-team`으로 이름이 바뀌면서 만들어졌는데, `.venv`가 그 옛 폴더에서
  생성된 채로 그대로 옮겨졌다. uv가 만드는 `pytest.exe`/`ruff.exe`/`mypy.exe` 등 CLI 트램폴린
  실행파일은 생성 시점의 venv 절대경로를 내부에 하드코딩해두는데, 폴더 이름이 바뀌면서 그 경로가
  더 이상 존재하지 않아 발생한 오류였다 (`python.exe -m pytest`처럼 트램폴린을 거치지 않는 호출은
  문제없이 동작했다).
- **조치**: `.venv` 삭제 후 `uv sync`로 현재 경로 기준으로 재생성. 이후 `uv run pytest`,
  `uv run ruff check`, `uv run ruff format --check`, `uv run mypy` 모두 정상 통과 확인했다.
- **추가로 발견한 문제**: `.git/hooks/pre-commit`가 설치돼 있지 않았다 — `.git/hooks`는 git이 추적하지
  않는 로컬 디렉터리라 폴더 이동 과정에서 유실된 것으로 보인다. `uv run pre-commit install`로
  재설치해 `git commit` 시 자동 실행되도록 복구했다.
- **Codex 연동 확인**: `mcp__codex__codex` 도구로 테스트 세션을 호출해 정상 응답과 `threadId` 발급을
  확인했다 — 폴더 이름 변경이 Codex MCP 연동에는 영향을 주지 않았다.
- 교훈: 프로젝트 폴더를 옮기거나 이름을 바꿀 때는 `.venv`를 반드시 재생성해야 한다
  (`.git/hooks`도 함께 재설치 필요). [dev-environment.md](../.claude/rules/dev-environment.md)의
  커밋 전 체크리스트를 실행하기 전에 이 단계를 먼저 거쳐야 한다.
