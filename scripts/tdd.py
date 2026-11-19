#!/usr/bin/env python
"""TDD 하네스의 공통 도구와 next 명령."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "plan.md"
LOGS = ROOT / "logs" / "tdd"
ROW = re.compile(r"^\|\s*[☐☑⏸]\s*\|")


def run(cmd, text=None):
  argv = [sys.executable if part == "python" else part for part in cmd]
  env = {**os.environ, "PYTHONUTF8": "1"}
  result = subprocess.run(
    argv,
    cwd=ROOT,
    input=text,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
    env=env,
  )
  return result.returncode, (result.stdout + result.stderr).strip()


def git(*args, text=None):
  code, output = run(["git", "-c", "core.quotepath=false", *args], text=text)
  output = "\n".join(
    line for line in output.splitlines() if not line.startswith("warning:")
  )
  return code, output


def die(reason):
  print(f"[STOP] {reason}")
  raise SystemExit(1)


def read_plan():
  if not PLAN.exists():
    die("plan.md 가 없습니다. 작업 지시서가 없으면 구현하지 않고 멈춥니다.")
  rows = []
  for line in PLAN.read_text(encoding="utf-8").splitlines():
    if not ROW.match(line):
      continue
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    rows.append(
      {
        "state": cells[0],
        "p": cells[1],
        "tc": cells[2],
        "label": cells[3],
        "kind": cells[4],
        "title": cells[5],
        "input": cells[6],
        "expected": cells[7],
      }
    )
  return rows


def load(tc):
  guard_harness()
  path = LOGS / tc / "evidence.json"
  if not path.exists():
    die(f"{tc} 증거 파일이 없습니다. 먼저 `python scripts/tdd.py next` 를 실행하세요.")
  return json.loads(path.read_text(encoding="utf-8"))


def save(tc, evidence):
  path = LOGS / tc / "evidence.json"
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(
    json.dumps(evidence, ensure_ascii=False, indent=2),
    encoding="utf-8",
  )


def commit(subject, evidence, paths):
  code, output = git("add", "-A", "--", *paths)
  if code != 0:
    die("git add 실패:\n" + output)
  if not git("diff", "--cached", "--name-only")[1]:
    return None
  body = (
    f"Feature: {evidence['feature']}\n"
    f"Contract: {evidence['label']} ({evidence['kind']}, P{evidence['p']})\n"
    f"Evidence: logs/tdd/{evidence['tc']}/evidence.json"
  )
  code, output = git("commit", "-F", "-", text=f"{subject}\n\n{body}\n")
  if code != 0:
    die("커밋 실패:\n" + output)
  return git("rev-parse", "--short", "HEAD")[1]


def ensure_git_writable():
  probe = ROOT / ".git" / "tdd-write-probe"
  try:
    probe.write_text("probe", encoding="utf-8")
    probe.unlink()
  except OSError as error:
    die(
      f".git 에 쓸 수 없습니다 ({error.__class__.__name__}). 이 명령이 Codex 샌드박스 안에서 실행되고 있습니다.\n"
      "  → .codex/rules/tdd.rules (하네스 실행 허용 규칙)가 적용되지 않았습니다.\n"
      "  → codex 를 종료하고 같은 폴더에서 다시 시작해 '이 폴더를 신뢰' 하세요. 명령은 `python scripts/tdd.py …` 한 줄 그대로 실행해야 합니다."
    )


def guard_harness():
  ensure_git_writable()
  changed = git("status", "--porcelain", "--", "scripts", "AGENTS.md", ".codex")[1]
  if changed:
    die(
      "하네스 · 규칙 파일이 커밋된 상태와 다릅니다. 이 파일들은 루프 중에 고치지 않습니다:\n"
      + changed
    )


def cmd_next(_args):
  try:
    import hypothesis  # noqa: F401
    import pytest  # noqa: F401
  except ImportError as error:
    die(f"{error} — 가상환경(.venv)을 활성화한 터미널에서 codex 를 시작했는지 확인하세요.")

  ensure_git_writable()
  _, branch = git("branch", "--show-current")
  match = re.match(r"feature/(F-\d+)-", branch)
  if not match:
    die(
      f"현재 브랜치 '{branch}' 는 Feature 브랜치가 아닙니다. 예: git switch -c feature/F-01-shipping-fee"
    )

  dirty = git("status", "--porcelain")[1]
  if dirty:
    die(
      "커밋되지 않은 변경이 있습니다. 이전 루프를 report 로 끝내거나 정리한 뒤 다시 go 하세요:\n"
      + dirty
    )

  rows = read_plan()
  todos = [row for row in rows if row["state"] == "☐"]
  paused = [row for row in rows if row["state"] == "⏸"]
  if not todos:
    print(
      f"[끝] 미완료(☐) TC 가 없습니다. ⏸ 결정 대기 {len(paused)}건은 구현하지 않습니다. 새 TC 를 만들지 않고 멈춥니다."
    )
    return

  row = todos[0]
  base = git("rev-parse", "--short", "HEAD")[1]
  evidence = {
    "tc": row["tc"],
    "p": int(row["p"]),
    "label": row["label"],
    "kind": row["kind"],
    "title": row["title"],
    "feature": match.group(1),
    "branch": branch,
    "base": base,
    "started": datetime.now().isoformat(timespec="seconds"),
  }
  save(row["tc"], evidence)
  print(
    f"[NEXT] {row['tc']} · P{row['p']} · {row['label']} · {row['kind']} · {row['title']}"
  )
  print(f"  입력      : {row['input']}")
  print(f"  기대 결과 : {row['expected']}")
  print(
    f"  남은 ☐ {len(todos)}개 · ⏸ {len(paused)}개 · 브랜치 {branch} · 기준 커밋 {base}"
  )


def new_test_files():
  output = git(
    "status",
    "--porcelain",
    "--untracked-files=all",
    "--",
    "tests",
  )[1]
  return [
    line[3:].strip()
    for line in output.splitlines()
    if line[3:].strip().endswith(".py")
  ]


def pytest_summary(output):
  for line in reversed(output.splitlines()):
    if " in " in line and re.search(r"\b(passed|failed|error)", line):
      return line.strip("= ")
  return output.splitlines()[-1] if output else ""


def output_tail(output, count=14):
  return "\n".join(output.splitlines()[-count:])


def cmd_red(args):
  evidence = load(args.tc)
  files = new_test_files()
  if not files:
    die(
      "새로 만들거나 고친 테스트 파일(tests/*.py)이 없습니다. 먼저 RED 테스트를 작성하세요."
    )

  code, output = run(["python", "-m", "pytest", "-q", *files])
  if code in (2, 5) or "error during collection" in output.lower():
    die(
      f"RED 가 아닙니다 — 수집 오류이거나 실행된 테스트가 없습니다 (종료 코드 {code}). 먼저 해결하세요.\n"
      + output_tail(output)
    )

  status = "RED" if code == 1 else "NO-RED"
  evidence["red"] = {
    "status": status,
    "exit_code": code,
    "summary": pytest_summary(output),
  }
  evidence["red"]["commit"] = commit(
    f"test({args.tc}): {evidence['title']} [{status}]",
    evidence,
    ["tests"],
  )
  save(args.tc, evidence)
  print(
    f"[OK] {status} — 종료 코드 {code} · {evidence['red']['summary']} · 커밋 {evidence['red']['commit']}"
  )
  if status == "NO-RED":
    print(
      "[주의] 새 테스트가 처음부터 통과했습니다. Red 없이 통과한 사실을 보고하세요."
    )


def cmd_green(args):
  evidence = load(args.tc)
  if "red" not in evidence:
    die("RED 증거가 없습니다. red 단계를 먼저 하세요.")

  red_base = evidence["red"].get("commit") or evidence["base"]
  changed_tests = git("diff", "--name-only", red_base, "--", "tests")[1]
  if changed_tests:
    die(
      "RED 커밋 이후 tests/ 가 바뀌었습니다. 통과시키려고 테스트를 고치지 않습니다:\n"
      + changed_tests
    )

  code, output = run(
    ["python", "-m", "pytest", "-q", "-m", "not golden"]
  )
  if code != 0:
    die(
      f"단위 테스트 전체가 통과하지 않았습니다 (종료 코드 {code}).\n"
      + output_tail(output)
    )

  evidence["green"] = {
    "exit_code": code,
    "summary": pytest_summary(output),
  }
  evidence["green"]["commit"] = commit(
    f"feat({args.tc}): {evidence['title']} [GREEN]",
    evidence,
    ["."],
  )
  save(args.tc, evidence)
  commit_result = evidence["green"]["commit"] or "(구현 변경 없음)"
  print(
    f"[OK] GREEN — {evidence['green']['summary']} · 커밋 {commit_result}"
  )


def main():
  sys.stdout.reconfigure(encoding="utf-8")
  parser = argparse.ArgumentParser(description="TDD 하네스 게이트 스크립트")
  commands = parser.add_subparsers(dest="command", required=True)
  commands.add_parser("next")
  commands.add_parser("red").add_argument("tc")
  commands.add_parser("green").add_argument("tc")
  args = parser.parse_args()
  {
    "next": cmd_next,
    "red": cmd_red,
    "green": cmd_green,
  }[args.command](args)


if __name__ == "__main__":
  main()
