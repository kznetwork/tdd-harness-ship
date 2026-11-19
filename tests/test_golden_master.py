"""골든 마스터 — 사람이 승인한 동작 행이 지금도 그대로인지 확인한다."""

import pytest

from golden_master import check_approved


@pytest.mark.golden
def test_approved_behavior_is_unchanged() -> None:
    changed = check_approved()
    assert not changed, "승인한 동작이 바뀌었습니다:\n" + "\n".join(changed)
