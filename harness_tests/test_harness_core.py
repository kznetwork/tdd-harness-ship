"""하네스 인수 테스트 — docs/harness/하네스명세.md 의 next · red · green 을 실행 가능한 문장으로 옮긴 것.

각 테스트는 임시 폴더에 작은 git 저장소(Feature 브랜치 · plan.md · 스켈레톤)를 새로 만들고,
복사해 둔 scripts/tdd.py 를 진짜로 실행해 종료 코드 · 출력 · 커밋 이력을 확인한다.

실행: python -m pytest harness_tests -q          (일부만: -k test_next · -k test_red · -k test_green)
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
ENV = {
    **os.environ,
    "PYTHONUTF8": "1",
    "PYTHONIOENCODING": "utf-8",
    "GIT_AUTHOR_NAME": "tester",
    "GIT_AUTHOR_EMAIL": "t@example.com",
    "GIT_COMMITTER_NAME": "tester",
    "GIT_COMMITTER_EMAIL": "t@example.com",
}

PLAN = """# 테스트 계획

| 상태 | P | TC | 계약 | 유형 | 제목 | 입력 | 기대 결과 |
| :---: | :---: | --- | --- | --- | --- | --- | --- |
| ☑ | 1 | TC-0 | CT-0 | AC | 이미 끝난 일 | 1 | 1 |
| ☐ | 2 | TC-1 | CT-1 | AC | 기본 배송비 3,000원 | 10,000원 | 배송비 3,000원 |
| ☐ | 3 | TC-2 | CT-2 | E | 0원 이하는 오류 | 0 | ValueError |
| ⏸ | – | TC-3 | OQ-1 | OQ | 도서산간 | (미정) | 결정 대기 |
"""

STUB = '"""스켈레톤."""\n\n\ndef calculate_shipping_fee(order_amount):\n    return 0\n'
GOOD = '"""구현."""\n\n\ndef calculate_shipping_fee(order_amount):\n    return 3000\n'
TEST_FAIL = "from shipping import calculate_shipping_fee\n\n\ndef test_fee():\n    assert calculate_shipping_fee(10000) == 3000\n"
TEST_BROKEN = "import 없는_모듈\n\n\ndef test_x():\n    assert True\n"


def sh(cwd, *cmd):
    p = subprocess.run(list(cmd), cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
    out = chr(10).join(ln for ln in (p.stdout + p.stderr).strip().splitlines() if not ln.startswith("warning:"))  # 샌드박스의 git 경고는 뺀다
    return p.returncode, out


def git(cwd, *args):
    return sh(cwd, "git", "-c", "core.quotepath=false", *args)


def tdd(cwd, *args):
    return sh(cwd, sys.executable, "scripts/tdd.py", *args)


def _force_remove(func, path, _exc):
    os.chmod(path, stat.S_IWRITE)  # .git 안의 읽기 전용 파일(Windows)
    func(path)


@pytest.fixture
def repo():
    """Feature 브랜치 위에 plan.md · 스켈레톤 · 하네스가 커밋된 깨끗한 저장소.
    임시 폴더는 프로젝트의 logs/ 아래에 만든다 — Codex 샌드박스에서도 쓸 수 있는 곳이고 .gitignore 에 있다."""
    work = ROOT / "logs" / "harness_tests"
    work.mkdir(parents=True, exist_ok=True)
    tmp_path = Path(tempfile.mkdtemp(prefix="repo-", dir=work))
    yield _build(tmp_path)
    shutil.rmtree(tmp_path, onerror=_force_remove)


def _build(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "tests").mkdir()
    for name in ("tdd.py", "golden_master.py"):
        src = ROOT / "scripts" / name
        if src.exists():
            shutil.copy(src, tmp_path / "scripts" / name)
    shutil.copy(ROOT / "pytest.ini", tmp_path / "pytest.ini")
    shutil.copy(ROOT / "conftest.py", tmp_path / "conftest.py")
    (tmp_path / "plan.md").write_text(PLAN, encoding="utf-8")
    (tmp_path / "shipping.py").write_text(STUB, encoding="utf-8")
    (tmp_path / ".gitignore").write_text("logs/\n__pycache__/\n.pytest_cache/\n.hypothesis/\n", encoding="utf-8")
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "chore: start")
    git(tmp_path, "switch", "-q", "-c", "feature/F-01-shipping-fee")
    return tmp_path


def evidence(repo, tc="TC-1"):
    return json.loads((repo / "logs" / "tdd" / tc / "evidence.json").read_text(encoding="utf-8"))


def subjects(repo):
    return git(repo, "log", "--format=%s")[1].splitlines()


# ------------------------------------------------------------------ next
def test_next_refuses_main_branch(repo):
    git(repo, "switch", "-q", "main")
    rc, out = tdd(repo, "next")
    assert rc == 1 and "[STOP]" in out and "Feature 브랜치" in out


def test_next_refuses_uncommitted_changes(repo):
    (repo / "dirty.txt").write_text("x", encoding="utf-8")
    rc, out = tdd(repo, "next")
    assert rc == 1 and "[STOP]" in out and "커밋되지 않은 변경" in out


def test_next_picks_first_todo_and_writes_evidence(repo):
    rc, out = tdd(repo, "next")
    assert rc == 0, out
    assert "[NEXT] TC-1" in out and "기본 배송비 3,000원" in out
    ev = evidence(repo)
    assert ev["tc"] == "TC-1" and ev["feature"] == "F-01" and ev["p"] == 2
    assert git(repo, "status", "--porcelain")[1] == ""  # 파일을 고치지 않는다
    assert len(subjects(repo)) == 1  # 커밋도 만들지 않는다


def test_next_ends_when_nothing_left(repo):
    (repo / "plan.md").write_text(PLAN.replace("☐", "☑"), encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "docs: all done")
    rc, out = tdd(repo, "next")
    assert rc == 0 and "[끝]" in out


# ------------------------------------------------------------------ red
def test_red_requires_evidence_file(repo):
    rc, out = tdd(repo, "red", "TC-1")
    assert rc == 1 and "증거 파일이 없습니다" in out


def test_red_requires_a_new_test_file(repo):
    tdd(repo, "next")
    rc, out = tdd(repo, "red", "TC-1")
    assert rc == 1 and "새로 만들거나 고친 테스트 파일" in out


def test_red_rejects_collection_error(repo):
    tdd(repo, "next")
    (repo / "tests" / "test_broken.py").write_text(TEST_BROKEN, encoding="utf-8")
    rc, out = tdd(repo, "red", "TC-1")
    assert rc == 1 and "RED 가 아닙니다" in out
    assert len(subjects(repo)) == 1  # 커밋하지 않는다


def test_red_commits_a_failing_test(repo):
    tdd(repo, "next")
    (repo / "tests" / "test_fee.py").write_text(TEST_FAIL, encoding="utf-8")
    rc, out = tdd(repo, "red", "TC-1")
    assert rc == 0, out
    assert "[OK] RED" in out
    assert subjects(repo)[0] == "test(TC-1): 기본 배송비 3,000원 [RED]"
    ev = evidence(repo)
    assert ev["red"]["status"] == "RED" and ev["red"]["exit_code"] == 1 and ev["red"]["commit"]
    assert "tests/test_fee.py" in git(repo, "show", "--stat", "--format=", "HEAD")[1]


def test_red_marks_a_test_that_passes_at_once_as_no_red(repo):
    tdd(repo, "next")
    (repo / "shipping.py").write_text(GOOD, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "chore: impl first")
    (repo / "tests" / "test_fee.py").write_text(TEST_FAIL, encoding="utf-8")
    rc, out = tdd(repo, "red", "TC-1")
    assert rc == 0 and "NO-RED" in out
    assert subjects(repo)[0] == "test(TC-1): 기본 배송비 3,000원 [NO-RED]"


# ------------------------------------------------------------------ green
def test_green_requires_red_first(repo):
    tdd(repo, "next")
    rc, out = tdd(repo, "green", "TC-1")
    assert rc == 1 and "RED 증거가 없습니다" in out


def test_green_rejects_changed_tests(repo):
    tdd(repo, "next")
    (repo / "tests" / "test_fee.py").write_text(TEST_FAIL, encoding="utf-8")
    tdd(repo, "red", "TC-1")
    (repo / "tests" / "test_fee.py").write_text(TEST_FAIL.replace("3000", "0"), encoding="utf-8")  # 통과시키려고 테스트를 고쳤다
    rc, out = tdd(repo, "green", "TC-1")
    assert rc == 1 and "tests/ 가 바뀌었습니다" in out


def test_green_rejects_failing_tests(repo):
    tdd(repo, "next")
    (repo / "tests" / "test_fee.py").write_text(TEST_FAIL, encoding="utf-8")
    tdd(repo, "red", "TC-1")
    rc, out = tdd(repo, "green", "TC-1")  # 구현을 아직 안 했다
    assert rc == 1 and "단위 테스트 전체가 통과하지 않았습니다" in out


def test_green_commits_the_implementation(repo):
    tdd(repo, "next")
    (repo / "tests" / "test_fee.py").write_text(TEST_FAIL, encoding="utf-8")
    tdd(repo, "red", "TC-1")
    (repo / "shipping.py").write_text(GOOD, encoding="utf-8")
    rc, out = tdd(repo, "green", "TC-1")
    assert rc == 0, out
    assert "[OK] GREEN" in out
    assert subjects(repo)[0] == "feat(TC-1): 기본 배송비 3,000원 [GREEN]"
    assert evidence(repo)["green"]["exit_code"] == 0
    body = git(repo, "log", "-1", "--format=%B")[1]
    assert "Feature: F-01" in body and "Contract: CT-1" in body


# ------------------------------------------------------------------ 하네스를 고쳐서 통과시키려는 시도
def test_red_refuses_when_the_harness_itself_was_changed(repo):
    tdd(repo, "next")
    (repo / "tests" / "test_fee.py").write_text(TEST_FAIL, encoding="utf-8")
    with open(repo / "scripts" / "tdd.py", "a", encoding="utf-8") as f:
        f.write("\n# 규칙을 우회하려고 하네스를 고쳤다\n")
    rc, out = tdd(repo, "red", "TC-1")
    assert rc == 1 and "하네스" in out and "커밋된 상태와 다릅니다" in out
