# Claude + Codex CLI 최적화 템플릿 (5인 이상 팀)

Claude Code와 Codex CLI 2개 도구로 협업하도록 구성된 프로젝트 템플릿입니다.
Claude Code가 오케스트레이터(요구사항 파악 · 계획 · 구현 · 웹 리서치)를 맡고,
Codex CLI는 `mcp__codex__codex` 도구로 호출되어 리뷰를 전담합니다.

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
