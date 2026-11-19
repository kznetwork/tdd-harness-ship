"""Codex CLI 훅 — 실행 기록(이벤트 로그)과 대화 기록(Transcript)을 파일로 보관한다.

  logs/codex/<세션 ID 의 SHA-256>/<uuid>.event.json   훅 입력 전문 · 보관 시각 · 오류   (기계 원본)
  docs/Prompt/NN.주제-날짜.md                          대화 전체를 읽기 쉽게 정리한 Markdown (세션마다 1개)

훅 입력(stdin JSON)의 공통 필드: session_id · transcript_path · cwd · hook_event_name
  UserPromptSubmit: prompt   Stop: last_assistant_message   PostToolUse: tool_name · tool_input · tool_response
  SessionStart: source (startup · resume · clear · compact · fork)   SessionEnd: reason
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
SAVE_EVENTS = {"Stop", "PreCompact", "SessionEnd"}  # Transcript 를 저장하는 이벤트
LOG_EVENTS = {"UserPromptSubmit", "PostToolUse", "SessionStart"}  # 이벤트 로그만 남기는 이벤트
KNOWN_EVENTS = SAVE_EVENTS | LOG_EVENTS
TRIVIAL = {"go", "yes", "no", "y", "n", "ok", "승인", "계속"}
CONTEXT = re.compile(r"<(environment_context|user_instructions|INSTRUCTIONS)>[\s\S]*?</\1>")


def clean(text: str) -> str:
    return CONTEXT.sub("", text).strip()


def read_turns(path: str | None) -> list[tuple[str, str]]:
    """Codex 가 남긴 롤아웃(JSONL)에서 사용자 · 어시스턴트 메시지를 (역할, 글) 목록으로 읽는다."""
    turns: list[tuple[str, str]] = []
    if not path or not Path(path).exists():
        return turns
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        try:
            data = json.loads(line)
        except ValueError:
            continue
        payload = data.get("payload") if isinstance(data, dict) else None
        if data.get("type") != "response_item" or not isinstance(payload, dict) or payload.get("type") != "message":
            continue
        role = payload.get("role")
        parts = [c.get("text", "") for c in payload.get("content", []) if isinstance(c, dict)]
        text = clean("".join(parts))
        # 규칙 파일(AGENTS.md)과 환경 정보는 Codex 가 사용자 메시지로 넣어 준다 — 대화가 아니므로 뺀다.
        if not text or text.startswith(("# AGENTS.md", "<")):
            continue
        if role == "user":
            turns.append(("User", text))
        elif role == "assistant":
            turns.append(("Assistant", text))
    return turns


def pick_topic(turns: list[tuple[str, str]]) -> str:
    """첫 의미 있는 사용자 말에서 주제어를 만든다. 'go' 뿐이면 응답에 나온 TC 번호를 쓴다."""
    for role, text in turns:
        if role == "User" and text.lower() not in TRIVIAL:
            words = re.findall(r"[가-힣a-zA-Z0-9]+", text)
            if words:
                return "_".join(words[:4])[:30]
    tcs = re.findall(r"TC-\d+", " ".join(t for r, t in turns if r == "Assistant"))
    return f"{tcs[0]}_루프" if tcs else "대화세션"


def markdown_path(session_dir: Path, topic: str) -> Path:
    """세션에 정해 둔 docs/Prompt 파일 경로. 새 세션이면 번호(NN)를 하나 올려 새로 정한다."""
    remembered = session_dir / "transcript_md_path.txt"
    if remembered.exists():
        return ROOT / remembered.read_text(encoding="utf-8").strip()
    folder = ROOT / "docs" / "Prompt"
    folder.mkdir(parents=True, exist_ok=True)
    numbers = [int(m.group(1)) for f in folder.glob("*.md") if (m := re.match(r"(\d+)\.", f.name))]
    safe = re.sub(r'[\\/*?:"<>|\s]+', "_", topic).strip("._") or "대화세션"
    path = folder / f"{max(numbers, default=0) + 1:02d}.{safe}-{datetime.now():%Y%m%d}.md"
    remembered.write_text(path.relative_to(ROOT).as_posix(), encoding="utf-8")
    return path


def render(turns: list[tuple[str, str]], payload: dict, title: str) -> str:
    out = [
        f"# {title}\n",
        f"- **Session ID**: `{payload['session_id']}`",
        f"- **기록 시각**: {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S} UTC\n",
    ]
    n = 0
    for role, text in turns:
        if role == "User":
            n += 1
            out.append(f"---\n\n## Turn {n}\n\n### 👤 User\n\n{text}\n")
        else:
            out.append(f"### 🤖 Assistant\n\n{text}\n")
    return "\n".join(out)


def end_note(payload: dict) -> str:
    return f"\n---\n\n> 세션 종료 (reason: {payload.get('reason', '알 수 없음')}) — 이 파일이 마지막 저장본이다.\n"


def archive(payload: dict) -> tuple[Path, str | None]:
    event = payload["hook_event_name"]
    if event not in KNOWN_EVENTS:  # 다른 도구의 이벤트 이름(예: Gemini 의 AfterAgent)이 들어오면 조용히 넘기지 않는다
        raise ValueError(f"알 수 없는 훅 이벤트 '{event}' — Codex 이벤트는 {' · '.join(sorted(KNOWN_EVENTS))} 입니다")
    key = sha256(payload["session_id"].encode("utf-8")).hexdigest()  # 세션 ID 를 경로에 그대로 쓰지 않는다
    session_dir = ROOT / "logs" / "codex" / key
    session_dir.mkdir(parents=True, exist_ok=True)
    record_id = uuid4().hex  # 호출마다 새 파일 — 덮어쓰지 않는다
    snapshot = md_rel = error = None
    if event == "UserPromptSubmit":  # 이 입력이 Transcript 파일을 못 읽을 때의 대체 자료가 된다
        (session_dir / "last_prompt.txt").write_text(payload.get("prompt", ""), encoding="utf-8")
    if event in SAVE_EVENTS:
        source = payload.get("transcript_path")
        try:
            if source and Path(source).exists():
                (session_dir / f"{record_id}.transcript.jsonl").write_bytes(Path(source).read_bytes())
                snapshot = f"{record_id}.transcript.jsonl"
            turns = read_turns(source)
            if not turns:  # 대화 파일을 못 읽으면 직전 프롬프트와 마지막 응답으로 대신한다
                last = session_dir / "last_prompt.txt"
                prompt = last.read_text(encoding="utf-8") if last.exists() else ""
                turns = [("User", clean(prompt)), ("Assistant", payload.get("last_assistant_message") or "")]
                turns = [t for t in turns if t[1]]
            path = markdown_path(session_dir, pick_topic(turns))
            ending = event == "SessionEnd"
            if ending and not turns and path.exists():  # 새 내용이 없으면 이미 저장한 대화는 두고, 끝났다는 표시만 더한다
                text = path.read_text(encoding="utf-8")
            else:
                text = render(turns, payload, path.stem)
            path.write_text(text + (end_note(payload) if ending else ""), encoding="utf-8")
            md_rel = path.relative_to(ROOT).as_posix()
        except (OSError, KeyError) as exc:
            error = str(exc)
    record = {
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "event": payload,
        "transcript_snapshot": snapshot,
        "transcript_md": md_rel,
        "archive_error": error,
    }
    record_path = session_dir / f"{record_id}.event.json"
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return record_path, md_rel if not error else f"ERROR:{error}"


def main() -> int:
    # stdout 은 Codex 와 약속한 JSON 만, 사람이 읽을 오류는 stderr 로 보낸다.
    try:
        payload = json.load(sys.stdin)
        record_path, md = archive(payload)
        if md and md.startswith("ERROR:"):
            raise OSError(f"Transcript 저장 실패: {md[6:]}; 로그: {record_path}")
    except (OSError, ValueError, KeyError, TypeError) as error:
        message = f"세션 보관 오류: {error}"
        print(message, file=sys.stderr)
        print(json.dumps({"systemMessage": message}, ensure_ascii=False))
        return 1  # 실패를 성공으로 숨기지 않는다
    out = {}
    if payload["hook_event_name"] in SAVE_EVENTS:
        out["systemMessage"] = f"세션 로그 및 Transcript 저장: {record_path}" + (f" (Transcript: {md})" if md else "")
    print(json.dumps(out, ensure_ascii=False))
    if "--echo" in sys.argv:  # 손으로 실행해 볼 때: 무엇을 저장했는지 사람이 읽을 한 줄을 stderr 로 보여 준다
        saved = f" · Transcript {md}" if md else ""
        print(f"[기록] {payload['hook_event_name']} → {record_path.relative_to(ROOT).as_posix()}{saved}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
