"""5교시 — templates/hooks.template.json 으로 .codex/hooks.json 을 만든다.

python scripts/install_hooks.py            .codex/hooks.json 만들기 (이미 있으면 그대로 두고 알린다)
python scripts/install_hooks.py --force    이미 있어도 다시 만든다
python scripts/install_hooks.py --check    만들지 않고 지금 설정이 맞는지만 확인한다

템플릿의 예시 경로(C:/DEV/tdd-harness/ship)를 이 폴더의 절대 경로로 바꿔 쓴다.
.codex 는 Codex 샌드박스에서 읽기 전용이라 AI 가 직접 쓰지 못한다 — 이 스크립트가 허용 규칙(.codex/rules/tdd.rules)으로 대신 쓴다.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "hooks.template.json"
TARGET = ROOT / ".codex" / "hooks.json"
EXAMPLE_ROOT = "C:/DEV/tdd-harness/ship"
EVENTS = {"UserPromptSubmit", "PostToolUse", "Stop", "PreCompact", "SessionStart", "SessionEnd"}


def build() -> dict:
    text = TEMPLATE.read_text(encoding="utf-8").replace(EXAMPLE_ROOT, ROOT.as_posix())
    return json.loads(text)


def problems(config: dict) -> list[str]:
    found = []
    events = set(config.get("hooks", {}))
    if events != EVENTS:
        found.append(f"이벤트가 다릅니다: 없는 것 {sorted(EVENTS - events)} · 모르는 것 {sorted(events - EVENTS)}")
    script = ROOT / "scripts" / "archive_session.py"
    if not script.exists():
        found.append(f"{script} 가 없습니다")
    for name, groups in config.get("hooks", {}).items():
        for group in groups:
            for handler in group.get("hooks", []):
                if ROOT.as_posix() not in handler.get("command", ""):
                    found.append(f"{name}: 명령의 경로가 이 폴더({ROOT.as_posix()})가 아닙니다")
    return found


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")   # Windows 콘솔(cp949)에서 ‘—’ 같은 글자 때문에 죽지 않게
    check = "--check" in sys.argv
    if check:
        if not TARGET.exists():
            print(f"[확인 실패] {TARGET.relative_to(ROOT).as_posix()} 가 없습니다. python scripts/install_hooks.py 를 실행하세요.")
            return 1
        found = problems(json.loads(TARGET.read_text(encoding="utf-8")))
        print("[확인 완료] 이벤트 6개 · 경로 일치" if not found else "[확인 실패]\n  " + "\n  ".join(found))
        return 1 if found else 0
    if TARGET.exists() and "--force" not in sys.argv:
        print(f"[그대로 둠] {TARGET.relative_to(ROOT).as_posix()} 가 이미 있습니다. 다시 만들려면 --force")
        return 0
    config = build()
    found = problems(config)
    if found:
        print("[실패] " + "; ".join(found))
        return 1
    TARGET.parent.mkdir(exist_ok=True)
    TARGET.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[완료] {TARGET.relative_to(ROOT).as_posix()} — 이벤트 {len(config['hooks'])}개, 스크립트 경로 {ROOT.as_posix()}/scripts/archive_session.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
