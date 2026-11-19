"""pytest 공통 설정 — Hypothesis 를 수업에서 매번 같은 결과가 나오도록 고정한다."""

from hypothesis import settings

settings.register_profile("class", max_examples=200, derandomize=True, deadline=None)
settings.load_profile("class")
