"""모든 hook이 공유하는 실행 로그 유틸리티.

각 hook은 자기 판단(제안할지 말지)을 내린 뒤 이 함수로 결과를 한 줄만 기록한다.
로그는 차단/실패를 유발하면 안 되므로 쓰기 실패는 조용히 무시한다.

`agent`/`status`는 agent-visualizer(하네스 이벤트를 실시간 시각화하는 별도 도구)가
소비하는 필드다. 이 파일은 그 도구를 몰라도 되지만, 필드 이름은 계약으로 유지한다.
"""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "hooks.jsonl"


def read_hook_input() -> dict[str, Any]:
    """훅 stdin(JSON)을 dict로 읽는다. 비었거나 깨졌거나 최상위가 객체가 아니면 빈 dict."""
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def as_dict(value: object) -> dict[str, Any]:
    """중첩 필드(tool_input 등)가 객체가 아니면 빈 dict — `.get()` 호출이 훅을 죽이지 않게 한다."""
    return value if isinstance(value, dict) else {}


def log_event(
    hook_name: str,
    event: str,
    triggered: bool,
    detail: str = "",
    agent: str = "claude",
    status: str = "",
    usage: dict[str, Any] | None = None,
) -> None:
    entry = {
        "ts": datetime.now(UTC).isoformat(timespec="seconds"),
        "hook": hook_name,
        "event": event,
        "triggered": triggered,
        "detail": detail,
        "agent": agent,
        "status": status or ("flag" if triggered else "working"),
        "usage": usage,
    }
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass
