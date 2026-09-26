> **보관(archive) 상태 (2026-08-20)**: 이 템플릿을 실제로 쓰는 5인 이상 팀 프로젝트가 아직 없어
> 보관 중입니다(2026-08-20 `_templates/_archive/`로 이동, 2026-09-26 사용자 요청으로 중간 폴더를 없애고
> `_templates/` 바로 아래로 옮김 — 위치만 바뀌었고 보관 상태는 그대로). 다른 템플릿(예:
> `claude-codex-optimized-template-under-4-members`)에 적용하는 규칙 확산 작업 대상에서 제외되며,
> 실사용이 필요해지면 그때 최신 상태로 다시 점검한 뒤 실사용으로 복귀시킵니다.
>
> **복귀 전 반드시 확인할 것 (2026-09-20, 2026-09-26 갱신)**: 2026-09-26 Codex 연동을 기준 템플릿
> (`claude-codex-optimized-template-under-4-members`)과 같은 방식으로 최신화했다(`npx` 0.153.4 고정
> MCP 서버, read-only 강제 훅, MCP 응답 파싱 보강, 훅 회귀 테스트). 보관 상태는 그대로다. 실사용으로
> 복귀할 때는 그 사이 기준 템플릿에 생긴 다른 변경을 다시 점검한다.

# Claude + Codex CLI 최적화 템플릿 (5인 이상 팀)

Claude Code와 Codex CLI 2개 도구로 협업하도록 구성된 프로젝트 템플릿입니다.
Claude Code가 오케스트레이터(요구사항 파악 · 계획 · 구현 · 웹 리서치)를 맡고,
Codex CLI는 MCP 도구 `mcp__codex__codex`로 호출되어 리뷰를 전담합니다.

5인 이상 팀이 각자 자신의 Claude Code 세션으로 같은 저장소를 동시에 작업하는 상황을 전제로,
브랜치 전략 · 코드 오너십(CODEOWNERS) · PR 리뷰 게이트를 추가했습니다.

자세한 협업 구조, 규칙, 스킬, 품질 게이트는 [CLAUDE.md](CLAUDE.md)를 참고하세요.
작업 이력은 [CHANGELOG.md](CHANGELOG.md)에 날짜순으로 기록됩니다.

## 시작하기 (개인 환경)

```bash
uv sync                       # 의존성 설치
uv run pre-commit install     # 커밋 전 ruff/mypy 자동 실행 활성화
```

새 프로젝트로 초기화하려면 Claude Code에서 `/init` 스킬을 사용하세요.

**Codex 연동**: `.mcp.json`에 Codex가 프로젝트 MCP 서버로 등록되어 있다
(`npx -y @openai/codex@0.153.4 mcp-server`). `codex mcp-server`는 Codex CLI 0.154.0에서 삭제됐기
때문에 마지막 지원 버전을 npx로 고정한 것이다. 전역 Codex CLI 설치는 필요 없고, 저장소를 클론한
팀원은 Node.js(npx)와 Codex 로그인만 있으면 된다. 인증은 팀원 각자 자기 계정으로 개별 진행한다
(`.mcp.json`에는 인증 정보가 전혀 없고, 로그인 상태는 각자의 `~/.codex/auth.json`에 저장되어 저장소와
무관함):

```bash
npx -y @openai/codex@0.153.4 login   # 최초 1회, 팀원 각자 자기 계정으로 로그인
```

Codex 호출 경로는 MCP `codex` 도구 하나뿐이다. Bash로 Codex CLI를 직접 실행하는 등의 다른 호출
방식은 쓰지 않는다.

- Claude Code가 이 저장소의 MCP 서버를 처음 인식하면 신뢰 여부를 묻는다. 승인 후 `claude mcp list`에
  `codex: ✓ Connected`가 보이면 준비 완료다.
- `.mcp.json`의 `command`는 Windows용 `cmd /c npx ...` 형태다. macOS/Linux에서는 `command`를
  `npx`, `args`를 `["-y", "@openai/codex@0.153.4", "mcp-server"]`로 바꾼다.
- 호출은 항상 `sandbox: read-only`·`approval-policy: never`이며 `.claude/hooks/codex-disable-plugins.py`가
  이를 강제한다. 세부 호출 규칙은 [codex-delegation.md](.claude/rules/codex-delegation.md) 참고.
- 알려진 한계: npm에서 `0.153.4`가 내려가면(unpublish) 서버가 뜨지 않는다.

## 팀 세팅 (한 번만)

1. `.claude/docs/OWNERSHIP.md`와 `.github/CODEOWNERS`에 실제 팀원/GitHub 핸들을 채웁니다.
2. GitHub 저장소 설정 → Branches에서 `main`/`master`에 브랜치 보호 규칙을 추가하고,
   "Require a pull request before merging", "Require review from Code Owners",
   "Require status checks to pass"(CI job `check`)를 켭니다.
3. 팀원 각자 로컬에서 `uv sync && uv run pre-commit install`을 실행합니다.

## 작업 흐름 (팀원별)

```bash
git checkout -b feature/짧은-설명   # main/master에서 직접 작업하지 않음
# Claude Code + Codex로 구현 ...
git fetch && git rebase origin/main # PR 전 최신화
git push -u origin feature/짧은-설명
# GitHub에서 PR 생성 → PULL_REQUEST_TEMPLATE.md 체크리스트 작성 → CODEOWNERS 리뷰 대기
```

자세한 원칙은 [.claude/rules/team-collaboration.md](.claude/rules/team-collaboration.md)를 참고하세요.
