"""Sanity — 지금까지 구현한 계약의 대표 입력을 실제로 한 번씩 불러 본다 (1초 이내).

python scripts/sanity.py --upto 3        # 우선순위 3 까지 구현했을 때
python scripts/sanity.py --readme        # + README.md 의 사용 예(doctest)까지
"""

from __future__ import annotations

import argparse
import doctest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from shipping import calculate_shipping_fee as fee  # noqa: E402

# (우선순위, 계약, 입력, 기대 — 값 또는 예외 종류)
CASES = [
    (1, "CT-1", 10_000, 3_000),
    (2, "CT-2", 30_000, 0),
    (3, "CT-3", 0, ValueError),
    (4, "CT-4", None, TypeError),
]


def call(value: object) -> object:
    try:
        return fee(value)
    except Exception as error:  # noqa: BLE001
        return type(error)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")   # Windows 콘솔(cp949)에서 ‘—’ 같은 글자 때문에 죽지 않게
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--upto", type=int, default=99, help="이 우선순위까지의 계약만 확인"
    )
    parser.add_argument(
        "--readme", action="store_true", help="README.md 의 사용 예도 실행"
    )
    args = parser.parse_args()

    failed = 0
    for priority, contract, value, expected in CASES:
        if priority > args.upto:
            continue
        got = call(value)
        ok = got == expected
        failed += not ok
        name = expected.__name__ if isinstance(expected, type) else expected
        shown = got.__name__ if isinstance(got, type) else got
        print(
            f"{'OK  ' if ok else 'FAIL'} {contract}  fee({value!r}) → {shown}  (기대 {name})"
        )

    if args.readme:
        result = doctest.testfile(
            str(ROOT / "README.md"),
            module_relative=False,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        )
        failed += result.failed
        print(
            f"{'OK  ' if not result.failed else 'FAIL'} README 사용 예 {result.attempted - result.failed}/{result.attempted} 통과"
        )

    print("sanity:", "통과" if not failed else f"실패 {failed}건")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
