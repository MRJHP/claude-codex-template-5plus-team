# 팀 협업 규칙 (5인 이상)

이 템플릿은 여러 명이 각자 자신의 Claude Code(+Codex CLI) 세션으로 같은 저장소를 동시에 작업하는
상황을 전제로 한다. 아래 규칙은 그 상황에서 충돌과 리뷰 병목을 줄이기 위한 것이다.

## 브랜치 전략

- `main`/`master`는 보호 브랜치다. 직접 커밋/푸시하지 않고 항상 PR을 통해 병합한다.
- 브랜치 이름: `feature/<짧은-설명>`, `fix/<이슈번호-설명>`, `chore/<설명>` 형식을 따른다.
- 작업을 시작하기 전 `git checkout -b <브랜치명>`으로 기능 브랜치를 만든다. 현재 `main`/`master`에서
  바로 파일을 수정하려 하면 `check-branch-before-write.py` hook이 알려준다 (강제 아님).
- PR을 열기 전 `git fetch && git rebase origin/main`(또는 팀이 합의한 병합 전략)으로 최신화해서
  충돌을 미리 해결한다.

## 담당 범위와 충돌 방지

- 작업 시작 전 [.claude/docs/OWNERSHIP.md](../docs/OWNERSHIP.md)에서 담당 영역을 확인한다.
- 담당 범위를 벗어난 파일을 광범위하게 수정해야 한다면, PR을 열기 전에 해당 담당자와 짧게 조율한다.
- 여러 모듈에 걸친 변경은 가능하면 모듈별로 PR을 나눈다 ([coding-principles.md](coding-principles.md)의
  "작게 커밋 가능한 단위" 원칙의 팀 버전).
- 같은 파일을 여러 명이 동시에 크게 수정 중이라는 것을 알게 되면, 먼저 조율하고 나서 진행한다.

## 설계 변경 동기화

- [.claude/docs/DESIGN.md](../docs/DESIGN.md)는 아키텍처 결정의 단일 진실 공급원(source of truth)이다.
- 다른 팀원의 작업에 영향을 줄 수 있는 아키텍처 변경(스키마, 공용 인터페이스, 외부 계약 등)은 구현 전에
  DESIGN.md에 ADR 항목을 먼저 추가해 팀이 비동기로 검토할 수 있게 한다.

## PR 리뷰

- `.github/CODEOWNERS`에 정의된 담당자의 승인이 최소 1건 필요하다.
- `.github/PULL_REQUEST_TEMPLATE.md`의 체크리스트(테스트/린트 통과, 관련 이슈, 브레이킹 체인지 여부)를 채운다.
- Codex 리뷰를 거친 변경이라면 PR 설명에 리뷰 여부와 핵심 피드백을 요약해 남긴다
  ([codex-delegation.md](codex-delegation.md) 참고). 사람 리뷰어가 같은 지적을 반복하지 않도록 돕는다.

## 핸드오프

- 세션을 마칠 때 작업이 아직 끝나지 않았다면 `.claude/docs/handoff/<날짜>-<이름>.md`
  (템플릿: [_template.md](../docs/handoff/_template.md))에 현재 상태·다음 단계·막힌 지점을 남긴다.
- 다른 사람이 이어받을 때는 CHANGELOG.md와 관련 handoff 노트를 먼저 확인한다.
