#!/usr/bin/env python3
"""PreToolUse hook (matcher: Edit|Write).

main/master 브랜치에서 직접 파일을 수정하려는 경우 기능 브랜치 생성을 '제안'한다.
5인 이상 팀에서는 여러 명이 동시에 작업하므로 보호 브랜치 직접 수정을 피하는 게 좋다.
절대 차단하지 않는다 (permissionDecision은 항상 allow).
"""

import json
import subprocess
import sys

from _hooklog import log_event

PROTECTED_BRANCHES = ("main", "master")


def current_branch() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=3,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip()


def main() -> None:
    sys.stdin.read()  # 다른 hook과 동일한 stdin 프로토콜을 소비만 하고 내용은 쓰지 않는다.

    branch = current_branch()
    if branch not in PROTECTED_BRANCHES:
        log_event("check-branch-before-write", "PreToolUse", triggered=False, detail=branch)
        sys.exit(0)

    log_event("check-branch-before-write", "PreToolUse", triggered=True, detail=branch)
    reason = (
        f"[check-branch-before-write] 현재 '{branch}' 브랜치에서 직접 작업 중입니다. "
        "5인 이상 팀에서는 main/master에 직접 커밋하지 않고 기능 브랜치를 만드는 것을 권장합니다 "
        "(예: git checkout -b feature/설명). 강제 아님, .claude/rules/team-collaboration.md 참고."
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
