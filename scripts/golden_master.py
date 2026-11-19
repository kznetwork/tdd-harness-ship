"""골든 마스터(승인 테스트) 도구 — 사람이 승인한 동작 행을 파일에 모으고, 지금 코드의 동작과 비교한다.

승인 파일: tests/golden/approved.txt   한 줄 = 계약 | 입력 | 결과
"""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / "tests" / "golden" / "approved.txt"
HEADER = "# 골든 마스터 — 사람이 승인한 동작 행 (계약 | 입력 | 결과)\n"

# 계약마다 '관찰할 입력'. 승인할 때 이 중 이번 계약의 행만 제안한다.
GRID = [
    ("CT-1", 1),
    ("CT-1", 10_000),
    ("CT-1", 29_999),
    ("CT-2", 30_000),
    ("CT-2", 30_001),
    ("CT-2", 50_000),
    ("CT-2", 100_000),
    ("CT-3", 0),
    ("CT-3", -1),
    ("CT-3", -10_000),
    ("CT-4", 29_999.5),
    ("CT-4", None),
    ("CT-4", "10000"),
    ("CT-4", True),
]


def render(value: object) -> str:
    """지금 코드가 이 입력에 하는 일을 한 줄 문자열로 만든다. 예외도 동작이다."""
    from shipping import calculate_shipping_fee

    try:
        return repr(calculate_shipping_fee(value))
    except Exception as error:  # noqa: BLE001 — 어떤 예외든 동작으로 기록한다
        return f"{type(error).__name__}: {error}"


def row(contract: str, value: object) -> str:
    return f"{contract} | {value!r} | {render(value)}"


def load_approved() -> list[tuple[str, str, str]]:
    if not APPROVED.exists():
        return []
    rows = []
    for text in APPROVED.read_text(encoding="utf-8").splitlines():
        if text.strip() and not text.startswith("#"):
            contract, value, result = text.split(" | ", 2)
            rows.append((contract, value, result))
    return rows


def check_approved() -> list[str]:
    """승인한 행 중 지금 동작과 달라진 것을 설명하는 문장 목록 (비어 있으면 그대로)."""
    changed = []
    for contract, value, approved in load_approved():
        now = render(ast.literal_eval(value))
        if now != approved:
            changed.append(f"{contract} 입력 {value}: 승인 {approved!r} → 지금 {now!r}")
    return changed


def proposal(contract: str) -> list[str]:
    """이 계약의 행 중 아직 승인되지 않은 것(= 이번에 사람이 볼 것)."""
    approved = {(c, v) for c, v, _ in load_approved()}
    return [
        row(c, v) for c, v in GRID if c == contract and (c, repr(v)) not in approved
    ]


def approve(lines: list[str]) -> None:
    APPROVED.parent.mkdir(parents=True, exist_ok=True)
    text = APPROVED.read_text(encoding="utf-8") if APPROVED.exists() else HEADER
    APPROVED.write_text(
        text.rstrip("\n") + "\n" + "\n".join(lines) + "\n", encoding="utf-8"
    )
