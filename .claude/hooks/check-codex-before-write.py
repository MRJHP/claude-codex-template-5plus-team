#!/usr/bin/env python3
"""PreToolUse hook (matcher: Edit|Write).

편집하려는 파일이 위험도가 높아 보이면 Codex 상담을 '제안'한다. 절대 차단하지 않는다.

제안은 `hookSpecificOutput.additionalContext`로만 전달한다. `permissionDecision`은 출력하지
않는다 — PreToolUse에서 `allow`를 내면 사용자 승인 없이 도구가 실행되는 권한 우회가 되고,
`permissionDecisionReason`은 Claude에게 전달되지도 않는다(2026-09-19 실험, Claude Code 2.1.278).
"""

import json
import sys

from _hooklog import log_event
from _risk_keywords import RISK_PATH_KEYWORDS


def is_risky(file_path: str, content: str) -> bool:
    path_lower = file_path.lower()
    if any(k in path_lower for k in RISK_PATH_KEYWORDS):
        return True
    return len(content) > 4000  # 한 번에 너무 큰 변경


def main() -> None:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        data = {}

    tool_input = data.get("tool_input", {}) or {}
    file_path = str(tool_input.get("file_path", ""))
    content = str(tool_input.get("content", "") or tool_input.get("new_string", ""))

    if not file_path or not is_risky(file_path, content):
        log_event("check-codex-before-write", "PreToolUse", triggered=False, detail=file_path)
        sys.exit(0)

    log_event("check-codex-before-write", "PreToolUse", triggered=True, detail=file_path)
    suggestion = (
        f"[check-codex-before-write] '{file_path}'은(는) 민감하거나 규모가 큰 변경으로 보입니다. "
        "구현 전에 MCP 도구 mcp__codex__codex를 호출해 Codex에게 접근 방식을 상담해볼 것을 "
        "제안합니다 (강제 아님, .claude/rules/codex-delegation.md 기준 참고)."
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": suggestion,
                }
            }
        )
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
