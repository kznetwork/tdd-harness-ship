#!/usr/bin/env python
"""TDD 하네스 — go 루프의 단계마다 증거를 남기고 커밋을 만드는 게이트 스크립트 (표준 라이브러리만 사용).

python scripts/tdd.py next                      첫 ☐ TC 를 고른다
python scripts/tdd.py red TC-1                  RED 확인 + 커밋
python scripts/tdd.py green TC-1                GREEN 확인 + 커밋
python scripts/tdd.py golden TC-1 [--approve]   골든 마스터 제안 / 승인 + 커밋
python scripts/tdd.py smell TC-1                코드 스멜 분석 문서 검증 + 지표
python scripts/tdd.py plan-check TC-5           (마지막 루프) 리팩터링 계획서 검증 + 커밋
python scripts/tdd.py refactor TC-5 R-1         (마지막 루프) 리팩터링 한 건 확인 + 커밋
python scripts/tdd.py regress TC-1              회귀(전체 테스트) + Sanity
python scripts/tdd.py probe TC-5                (Red 없이 통과했을 때) 변이 탐침
python scripts/tdd.py report TC-1 --note "요약"  보고서 생성 + plan.md ☑ + 커밋
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
import golden_master as gm  # noqa: E402

PLAN = ROOT / "plan.md"
LOGS = ROOT / "logs" / "tdd"
UNIT = ["python", "-m", "pytest", "-q", "-m", "not golden"]
FULL = ["python", "-m", "pytest", "-q"]
ROW = re.compile(r"^\|\s*[☐☑⏸]\s*\|")


# ------------------------------------------------------------------ 바탕 도구
def run(cmd, text=None, cwd=ROOT):
    """명령을 실행해 (종료 코드, 출력) 을 돌려준다. 'python' 은 지금 쓰는 인터프리터로 바꾼다."""
    argv = [sys.executable if a == "python" else a for a in cmd]
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    p = subprocess.run(
        argv,
        cwd=cwd,
        input=text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    return p.returncode, (p.stdout + p.stderr).strip()


def shown(cmd):
    return " ".join(f'"{a}"' if " " in a else a for a in cmd)


def git(*args, text=None):
    """git 을 실행한다. 샌드박스에서 나오는 'warning: …' 줄(예: 전역 ignore 파일을 못 읽음)은 결과에서 뺀다."""
    code, out = run(["git", "-c", "core.quotepath=false", *args], text=text)
    out = "\n".join(line for line in out.splitlines() if not line.startswith("warning:"))
    return code, out


def head():
    return git("rev-parse", "--short", "HEAD")[1]


def die(message):
    print(f"[STOP] {message}")
    sys.exit(1)


def tail(out, n=14):
    return "\n".join(out.splitlines()[-n:])


def summary(out):
    for line in reversed(out.splitlines()):
        if " in " in line and re.search(r"\b(passed|failed|error)", line):
            return line.strip("= ")
    return out.splitlines()[-1] if out else ""


# ------------------------------------------------------------------ plan.md · 증거 파일
def read_plan():
    if not PLAN.exists():
        die("plan.md 가 없습니다. 작업 지시서가 없으면 구현하지 않고 멈춥니다.")
    rows = []
    for line in PLAN.read_text(encoding="utf-8").splitlines():
        if ROW.match(line):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            rows.append(
                dict(
                    state=c[0],
                    p=c[1],
                    tc=c[2],
                    label=c[3],
                    kind=c[4],
                    title=c[5],
                    inp=c[6],
                    expect=c[7],
                )
            )
    return rows


def ensure_git_writable():
    """.git 에 쓸 수 있는지 확인한다. 못 쓰면 커밋이 조용히 건너뛰어지므로 여기서 멈춘다."""
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
    """하네스(scripts/) · 규칙(AGENTS.md) · 훅 설정(.codex/)이 커밋된 상태 그대로인지 확인한다.
    AI 가 루프 중에 하네스나 규칙을 고쳐 통과시키는 것을 막는다."""
    ensure_git_writable()
    changed = git("status", "--porcelain", "--", "scripts", "AGENTS.md", ".codex")[1]
    if changed:
        die("하네스 · 규칙 파일이 커밋된 상태와 다릅니다. 이 파일들은 루프 중에 고치지 않습니다:\n" + changed)


def load(tc):
    guard_harness()
    f = LOGS / tc / "evidence.json"
    if not f.exists():
        die(
            f"{tc} 증거 파일이 없습니다. 먼저 `python scripts/tdd.py next` 를 실행하세요."
        )
    return json.loads(f.read_text(encoding="utf-8"))


def save(tc, ev):
    f = LOGS / tc / "evidence.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(ev, ensure_ascii=False, indent=2), encoding="utf-8")


def commit(subject, ev, pathspec, extra=""):
    """pathspec 을 add 하고 규칙 서식으로 커밋한다. 바뀐 것이 없으면 None."""
    rc, out = git("add", "-A", "--", *pathspec)
    if rc != 0:
        die("git add 실패:\n" + out)
    if not git("diff", "--cached", "--name-only")[1]:
        return None
    body = f"Feature: {ev['feature']}\nContract: {ev['label']} ({ev['kind']}, P{ev['p']})\n{extra}".rstrip()
    rc, out = git("commit", "-q", "-F", "-", text=f"{subject}\n\n{body}\n")
    if rc != 0:
        die("커밋 실패:\n" + out)
    return head()


# ------------------------------------------------------------------ next
def cmd_next(_):
    try:
        import hypothesis  # noqa: F401
        import pytest  # noqa: F401
    except ImportError as error:
        die(f"{error} — 가상환경(.venv)을 활성화한 터미널에서 codex 를 시작했는지 확인하세요.")
    ensure_git_writable()
    rc, branch = git("branch", "--show-current")
    m = re.match(r"feature/(F-\d+)-", branch)
    if not m:
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
    todo = [r for r in rows if r["state"] == "☐"]
    paused = [r for r in rows if r["state"] == "⏸"]
    if not todo:
        print(
            f"[끝] 미완료(☐) TC 가 없습니다. ⏸ 결정 대기 {len(paused)}건은 구현하지 않습니다. 새 TC 를 만들지 않고 멈춥니다."
        )
        return
    r = todo[0]
    last = len(todo) == 1
    ev = dict(
        tc=r["tc"],
        p=int(r["p"]),
        label=r["label"],
        contract=r["label"].split("·")[0],
        kind=r["kind"],
        title=r["title"],
        feature=m.group(1),
        branch=branch,
        last_loop=last,
        base=head(),
        started=datetime.now().isoformat(timespec="seconds"),
    )
    save(r["tc"], ev)
    print(f"[NEXT] {r['tc']} · P{r['p']} · {r['label']} · {r['kind']} · {r['title']}")
    print(f"  입력      : {r['inp']}")
    print(f"  기대 결과 : {r['expect']}")
    print(
        f"  RED 방식  : '{r['kind'].split('·')[0]}' 유형 — AGENTS.md '유형별 RED' 표를 따른다"
    )
    print(
        f"  마지막 루프: {'예 → 스멜 분석 뒤 리팩터링 계획서 작성 · 리팩터링 · README 예시까지 Sanity' if last else '아니오 → 이번에는 스멜 분석만 하고 코드는 고치지 않는다'}"
    )
    print(
        f"  남은 ☐ {len(todo)}개 · ⏸ {len(paused)}개 · 브랜치 {branch} · 기준 커밋 {ev['base']}"
    )


# ------------------------------------------------------------------ red · green
def new_test_files():
    out = git("status", "--porcelain", "--untracked-files=all", "--", "tests")[1]
    files = [ln[3:].strip() for ln in out.splitlines()]
    return [f for f in files if f.endswith(".py") and "test_golden_master" not in f]


def cmd_red(a):
    ev = load(a.tc)
    files = new_test_files()
    if not files:
        die(
            "새로 만들거나 고친 테스트 파일(tests/*.py)이 없습니다. 먼저 RED 테스트를 작성하세요."
        )
    numstat = git("diff", "--numstat", "HEAD", "--", "tests")[1]
    deleted = sum(
        int(x.split()[1]) for x in numstat.splitlines() if x.split()[1].isdigit()
    )
    if deleted:
        die(
            f"기존 테스트에서 {deleted}줄이 지워졌습니다. 통과한 테스트는 수정하거나 삭제하지 않습니다."
        )
    cmd = UNIT + files
    rc, out = run(cmd)
    if rc in (2, 5) or "error during collection" in out.lower():
        die(
            f"RED 가 아닙니다 — 수집 오류이거나 실행된 테스트가 없습니다 (종료 코드 {rc}). 먼저 해결하세요.\n"
            + tail(out)
        )
    status = "RED" if rc == 1 else "NO-RED"
    reasons = []
    for line in re.findall(r"^E\s+(.+)$", out, re.M):
        if line.startswith(("Failing test case", "Falsifying", ")")):
            continue
        line = re.sub(r"\s+#.*$", "", line).rstrip(",")
        line = (
            f"반례 {line}" if re.fullmatch(r"\w+=.+", line) else line
        )  # Hypothesis 가 찾아 준 입력
        if line not in reasons:
            reasons.append(line)
    reasons = reasons[:6]
    ev["red"] = dict(
        status=status,
        command=shown(cmd),
        exit_code=rc,
        summary=summary(out),
        files=files,
        failed=re.findall(r"^FAILED (\S+)", out, re.M),
        reasons=reasons,
    )
    tag = "RED" if status == "RED" else "NO-RED"
    ev["red"]["commit"] = commit(
        f"test({a.tc}): {ev['title']} [{tag}]",
        ev,
        ["tests"],
        f"Evidence: {shown(cmd)} -> exit {rc}, {ev['red']['summary']}",
    )
    save(a.tc, ev)
    print(
        f"[OK] {status} — 종료 코드 {rc} · {ev['red']['summary']} · 커밋 {ev['red']['commit']}"
    )
    for r in reasons:
        print("   이유:", r)
    if status == "NO-RED":
        print(
            "[주의] 새 테스트가 처음부터 통과했습니다. 'Red 없이 통과' 로 보고하고, probe 로 이 테스트가 구현을 감시하는지 확인하세요."
        )


def cmd_green(a):
    ev = load(a.tc)
    if "red" not in ev:
        die("RED 증거가 없습니다. red 단계를 먼저 하세요.")
    changed = git(
        "diff", "--name-only", ev["red"]["commit"] or ev["base"], "--", "tests"
    )[1]
    if changed:
        die(
            "RED 커밋 이후 tests/ 가 바뀌었습니다. 통과시키려고 테스트를 고치지 않습니다:\n"
            + changed
        )
    rc, out = run(UNIT)
    if rc != 0:
        die(f"단위 테스트 전체가 통과하지 않았습니다 (종료 코드 {rc}).\n" + tail(out))
    ev["green"] = dict(command=shown(UNIT), exit_code=0, summary=summary(out))
    ev["green"]["commit"] = commit(
        f"feat({a.tc}): {ev['title']} [GREEN]",
        ev,
        ["."],
        f"Evidence: {shown(UNIT)} -> exit 0, {ev['green']['summary']}",
    )
    save(a.tc, ev)
    print(
        f"[OK] GREEN — {ev['green']['summary']} · 커밋 {ev['green']['commit'] or '(구현 변경 없음)'}"
    )


# ------------------------------------------------------------------ 골든 마스터 승인
def cmd_golden(a):
    ev = load(a.tc)
    if "green" not in ev:
        die("GREEN 증거가 없습니다. green 단계를 먼저 하세요.")
    drift = gm.check_approved()
    if drift:
        die(
            "이미 승인한 동작이 바뀌었습니다 (회귀). 구현을 되돌리세요:\n  "
            + "\n  ".join(drift)
        )
    rows = gm.proposal(ev["contract"])
    if not rows:
        rc, out = run(FULL + ["-m", "golden"])
        ev["golden"] = dict(status="새 행 없음", rows=0, summary=summary(out))
        save(a.tc, ev)
        print(
            f"[OK] {ev['contract']} 는 새로 승인할 행이 없습니다. 기존 승인 행은 그대로입니다 ({ev['golden']['summary']})."
        )
        return
    print(
        f"[제안] {ev['contract']} 동작 {len(rows)}행 — 계약표와 비교해 읽어 보세요 (계약 | 입력 | 결과)"
    )
    for r in rows:
        print("   ", r)
    if not a.approve:
        ev["golden"] = dict(status="승인 대기", rows=len(rows), proposal=rows)
        save(a.tc, ev)
        print(
            "[승인 대기] 사용자의 '승인' 답을 받은 뒤에만 --approve 로 다시 실행합니다. 지금은 멈춥니다."
        )
        sys.exit(3)
    gm.approve(rows)
    rc, out = run(FULL + ["-m", "golden"])
    if rc != 0:
        die("승인한 행이 골든 테스트를 통과하지 못했습니다.\n" + tail(out))
    ev["golden"] = dict(
        status="승인", rows=len(rows), proposal=rows, summary=summary(out)
    )
    ev["golden"]["commit"] = commit(
        f"test(golden): {ev['contract']} 동작 {len(rows)}행 승인 [APPROVED]",
        ev,
        ["tests/golden"],
    )
    save(a.tc, ev)
    print(
        f"[OK] 승인 {len(rows)}행 · {ev['golden']['summary']} · 커밋 {ev['golden']['commit']}"
    )


# ------------------------------------------------------------------ 코드 스멜 분석
def code_metrics():
    src = (ROOT / "shipping.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    functions, magic = [], []
    for f in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
        branches = sum(
            isinstance(n, (ast.If, ast.IfExp, ast.BoolOp, ast.For, ast.While))
            for n in ast.walk(f)
        )
        functions.append(
            dict(
                name=f.name,
                lines=f.end_lineno - f.lineno + 1,
                params=len(f.args.args),
                complexity=1 + branches,
            )
        )
        for n in ast.walk(f):
            if (
                isinstance(n, ast.Constant)
                and isinstance(n.value, (int, float))
                and not isinstance(n.value, bool)
                and n.value not in (0, 1)
            ):
                magic.append(dict(value=n.value, line=n.lineno))
    consts = [
        t.id
        for n in tree.body
        if isinstance(n, ast.Assign)
        for t in n.targets
        if isinstance(t, ast.Name)
    ]
    return dict(
        lines=len(src.splitlines()),
        functions=functions,
        magic_numbers=magic,
        constants=consts,
    )


def cmd_smell(a):
    ev = load(a.tc)
    if "green" not in ev:
        die("GREEN 증거가 없습니다.")
    dirty = [
        ln
        for ln in git("status", "--porcelain")[1].splitlines()
        if not ln[3:].startswith("docs/")
    ]
    if dirty:
        die(
            "스멜 분석 단계에서는 docs/ 밖의 파일을 바꾸지 않습니다 (리팩터링은 마지막 루프의 계획서 뒤에):\n"
            + "\n".join(dirty)
        )
    doc = ROOT / "docs" / "refactor" / "smells" / f"{a.tc}.md"
    if not doc.exists():
        die(
            f"{doc.relative_to(ROOT).as_posix()} 가 없습니다. AGENTS.md 의 '코드 스멜 분석 서식'대로 작성하세요."
        )
    text = doc.read_text(encoding="utf-8")
    missing = [
        k
        for k in ("## 코드 스멜", "```mermaid", "classDiagram", "- 판정:")
        if k not in text
    ]
    if missing:
        die(f"{doc.name} 에 서식 항목이 빠졌습니다: {missing}")
    m = code_metrics()
    ev["smell"] = dict(doc=doc.relative_to(ROOT).as_posix(), metrics=m)
    save(a.tc, ev)
    print(f"[OK] 스멜 분석 문서 {ev['smell']['doc']}")
    for f in m["functions"]:
        print(
            f"   함수 {f['name']}: {f['lines']}줄 · 매개변수 {f['params']} · 복잡도 {f['complexity']}"
        )
    print(
        f"   매직 넘버: {[(x['value'], str(x['line']) + '행') for x in m['magic_numbers']] or '없음'} · 모듈 상수: {m['constants'] or '없음'}"
    )


# ------------------------------------------------------------------ 리팩터링 계획서 · 리팩터링 (마지막 루프)
def read_refactor_plan():
    doc = ROOT / "docs" / "refactor" / "refactor-plan.md"
    if not doc.exists():
        die(
            "docs/refactor/refactor-plan.md 가 없습니다. AGENTS.md 의 '리팩터링 계획서 서식'대로 작성하세요."
        )
    text = doc.read_text(encoding="utf-8")
    items = []
    for m in re.finditer(
        r"^### (R-\d+) (.+?)\n(.*?)(?=^#{2,3} |\Z)", text, re.S | re.M
    ):
        need = [
            k
            for k in ("- 기법:", "- 대상:", "- 안전망:", "- 위험:")
            if k not in m.group(3)
        ]
        if need:
            die(f"{m.group(1)} 에 항목이 빠졌습니다: {need}")
        technique = re.search(r"- 기법: (.+)", m.group(3)).group(1).strip()
        items.append(dict(id=m.group(1), title=m.group(2).strip(), technique=technique))
    if not items:
        die("계획서에 '### R-1 제목' 형식의 항목이 없습니다.")
    if "## 보류" not in text:
        die("'## 보류' 구역이 없습니다 (하지 않기로 한 것과 그 이유).")
    return items


def cmd_plan_check(a):
    ev = load(a.tc)
    if not ev["last_loop"]:
        die(
            "마지막 루프가 아닙니다. 리팩터링 계획서와 리팩터링은 마지막 루프에서만 합니다 (이번에는 스멜 분석만)."
        )
    if "smell" not in ev:
        die("스멜 분석(smell)을 먼저 끝내세요.")
    items = read_refactor_plan()
    ids = f"{items[0]['id']}~{items[-1]['id']}" if len(items) > 1 else items[0]["id"]
    ev["plan"] = dict(
        items=items,
        commit=commit(
            f"docs(refactor): 리팩터링 계획서 {ids} [PLAN]", ev, ["docs/refactor"]
        ),
    )
    ev["refactors"] = []
    save(a.tc, ev)
    print(
        f"[OK] 리팩터링 계획서 {len(items)}건: "
        + " · ".join(f"{i['id']} {i['title']}" for i in items)
    )


def cmd_refactor(a):
    ev = load(a.tc)
    items = ev.get("plan", {}).get("items") or die(
        "plan-check 를 먼저 통과해야 합니다."
    )
    done = [r["id"] for r in ev["refactors"]]
    item = next((i for i in items if i["id"] == a.rid), None) or die(
        f"{a.rid} 가 계획서에 없습니다."
    )
    expected = (
        next(i["id"] for i in items if i["id"] not in done)
        if len(done) < len(items)
        else None
    )
    if a.rid != expected:
        die(f"계획서 순서대로 진행합니다. 다음은 {expected} 입니다.")
    touched = [
        ln
        for ln in git("status", "--porcelain")[1].splitlines()
        if ln[3:].startswith("tests/")
    ]
    if touched:
        die(
            "리팩터링은 구조 변경입니다 — tests/ 를 바꾸지 않습니다:\n"
            + "\n".join(touched)
        )
    rc, out = run(FULL)
    if rc != 0:
        die(
            f"리팩터링 뒤 전체 테스트(골든 포함)가 실패했습니다 (종료 코드 {rc}). 되돌리거나 고치세요.\n"
            + tail(out)
        )
    h = commit(
        f"refactor({a.rid}): {item['title']} [REFACTOR]",
        ev,
        ["."],
        f"Technique: {item['technique']}\nEvidence: {shown(FULL)} -> exit 0, {summary(out)}",
    )
    ev["refactors"].append(
        dict(
            id=a.rid,
            title=item["title"],
            technique=item["technique"],
            summary=summary(out),
            commit=h,
        )
    )
    save(a.tc, ev)
    print(f"[OK] {a.rid} {item['title']} — {summary(out)} · 커밋 {h}")


# ------------------------------------------------------------------ 회귀 · Sanity
def cmd_regress(a):
    ev = load(a.tc)
    ids = {
        ln
        for ln in run(["python", "-m", "pytest", "--collect-only", "-q"])[
            1
        ].splitlines()
        if "::" in ln
    }
    base = LOGS / "baseline_ids.txt"
    before = (
        set(base.read_text(encoding="utf-8").splitlines()) if base.exists() else set()
    )
    if before - ids:
        die(
            "이전 루프에 있던 테스트가 사라졌습니다:\n  "
            + "\n  ".join(sorted(before - ids))
        )
    rc, out = run(FULL)
    if rc != 0:
        die(f"회귀 테스트 실패 (종료 코드 {rc}).\n" + tail(out))
    sanity = ["python", "scripts/sanity.py", "--upto", str(ev["p"])] + (
        ["--readme"] if ev["last_loop"] else []
    )
    rc2, out2 = run(sanity)
    if rc2 != 0:
        die("Sanity 실패:\n" + out2)
    base.parent.mkdir(parents=True, exist_ok=True)
    base.write_text("\n".join(sorted(ids)), encoding="utf-8")
    ev["regress"] = dict(
        command=shown(FULL),
        summary=summary(out),
        tests=len(ids),
        new_tests=len(ids - before),
        sanity_command=shown(sanity),
        sanity=out2.splitlines()[-1],
    )
    save(a.tc, ev)
    print(
        f"[OK] 회귀 {ev['regress']['summary']} (테스트 {len(ids)}개, 이번에 +{len(ids - before)}) · {out2.splitlines()[-1]}"
    )
    print(out2)


# ------------------------------------------------------------------ 변이 탐침 (Red 없이 통과한 테스트가 진짜 감시하는지)
def mutants(src):
    swap = {">=": ">", ">": ">=", "<=": "<", "<": "<=", "==": "!=", "!=": "=="}
    lines = src.splitlines(keepends=True)
    for t in tokenize.generate_tokens(io.StringIO(src).readline):
        if t.type == tokenize.OP and t.string in swap:
            new = swap[t.string]
        elif t.type == tokenize.NUMBER and re.fullmatch(r"[\d_]+", t.string):
            new = str(int(t.string.replace("_", "")) + 1)
        else:
            continue
        (row, c0), (_, c1) = t.start, t.end
        changed = lines[:]
        changed[row - 1] = lines[row - 1][:c0] + new + lines[row - 1][c1:]
        yield f"{row}행 {t.string} → {new}", "".join(changed)


def cmd_probe(a):
    ev = load(a.tc)
    files = ev["red"]["files"]
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name in ("tests", "scripts"):
            shutil.copytree(
                ROOT / name, tmp / name, ignore=shutil.ignore_patterns("__pycache__")
            )
        for name in ("conftest.py", "pytest.ini"):
            shutil.copy(ROOT / name, tmp / name)
        for label, text in mutants((ROOT / "shipping.py").read_text(encoding="utf-8")):
            (tmp / "shipping.py").write_text(text, encoding="utf-8")
            if run(UNIT + ["-x", *files], cwd=tmp)[0] != 0:
                results.append((label, "새 테스트가 잡음"))
            elif run(UNIT + ["-x"], cwd=tmp)[0] != 0:
                results.append((label, "다른 테스트가 잡음"))
            else:
                results.append((label, "살아남음"))
    for label, verdict in results:
        print(f"   {label:<16} {verdict}")
    survived = sum(v == "살아남음" for _, v in results)
    ev["probe"] = dict(
        total=len(results),
        by_new=sum(v == "새 테스트가 잡음" for _, v in results),
        by_other=sum(v == "다른 테스트가 잡음" for _, v in results),
        survived=survived,
    )
    save(a.tc, ev)
    p = ev["probe"]
    print(
        f"[{'경고' if survived else 'OK'}] 변이 {p['total']}개 — 새 테스트 {p['by_new']} · 다른 테스트 {p['by_other']} · 살아남음 {survived}"
    )


# ------------------------------------------------------------------ 보고서
def cmd_report(a):
    ev = load(a.tc)
    need = ["red", "green", "golden", "smell", "regress"]
    need += ["probe"] if ev.get("red", {}).get("status") == "NO-RED" else []
    need += ["plan"] if ev["last_loop"] else []
    missing = [k for k in need if k not in ev]
    if missing:
        die(f"아직 끝나지 않은 단계가 있어 보고서를 만들지 않습니다: {missing}")
    if ev["golden"]["status"] == "승인 대기":
        die("골든 마스터 승인이 끝나지 않았습니다.")
    if ev["last_loop"] and not ev["refactors"]:
        die("계획서의 리팩터링을 하나도 적용하지 않았습니다 (refactor 단계).")
    red, green, gold, smell, reg = (
        ev["red"],
        ev["green"],
        ev["golden"],
        ev["smell"],
        ev["regress"],
    )
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = ROOT / "docs" / "reports" / f"{stamp}_{a.tc}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    log = git("log", "--reverse", "--format=- `%h` %s", f"{ev['base']}..HEAD")[1]
    m = smell["metrics"]
    lines = [
        f"# 사이클 보고서 — {a.tc} · {ev['title']}",
        "",
        f"- 브랜치 `{ev['branch']}` · 계약 {ev['label']} ({ev['kind']}, P{ev['p']}) · 마지막 루프: {'예' if ev['last_loop'] else '아니오'}",
        f"- 요약(AI): {a.note or '(없음)'}",
        "",
        "## 1. RED",
        f"- 판정: {'의도한 실패 확인' if red['status'] == 'RED' else '**Red 없이 통과** (처음부터 통과 — 변이 탐침으로 감시력 확인)'}",
        f"- 명령: `{red['command']}` · 종료 코드 {red['exit_code']} · {red['summary']}",
        f"- 실패한 테스트: {', '.join(red['failed']) or '없음'}",
    ]
    lines += [f"- 실패 이유: {r}" for r in red["reasons"]] + [
        f"- 커밋: `{red['commit']}`",
        "",
        "## 2. GREEN",
        f"- 명령: `{green['command']}` · 종료 코드 0 · {green['summary']}",
        f"- 커밋: `{green['commit'] or '구현 변경 없음'}`",
        "",
        "## 3. 승인 (골든 마스터)",
        f"- 상태: {gold['status']} · 행 {gold['rows']}개 · 커밋 `{gold.get('commit') or '-'}`",
    ]
    lines += [f"  - `{r}`" for r in gold.get("proposal", [])]
    lines += [
        "",
        "## 4. 코드 스멜 분석",
        f"- 문서: `{smell['doc']}`",
        f"- 지표: 함수 {', '.join(f['name'] + '(' + str(f['lines']) + '줄·복잡도' + str(f['complexity']) + ')' for f in m['functions'])}"
        f" · 매직 넘버 {len(m['magic_numbers'])}개 · 모듈 상수 {len(m['constants'])}개",
        "",
        "## 5. 리팩터링",
    ]
    if ev["last_loop"]:
        lines += [
            f"- 계획서: `docs/refactor/refactor-plan.md` (커밋 `{ev['plan']['commit']}`)"
        ]
        lines += [
            f"- {r['id']} {r['title']} — {r['technique']} · {r['summary']} · 커밋 `{r['commit']}`"
            for r in ev["refactors"]
        ]
    else:
        lines += ["- 이번 루프는 분석만 했다 (계획서와 리팩터링은 마지막 루프에서)."]
    if "probe" in ev:
        p = ev["probe"]
        lines += [
            "",
            "## 변이 탐침",
            f"- 변이 {p['total']}개 중 새 테스트가 {p['by_new']}개, 다른 테스트가 {p['by_other']}개를 잡았고 살아남은 것은 {p['survived']}개",
        ]
    lines += [
        "",
        "## 6. 회귀 · Sanity",
        f"- 회귀: `{reg['command']}` · {reg['summary']} (테스트 {reg['tests']}개)",
        f"- Sanity: `{reg['sanity_command']}` · {reg['sanity']}",
        "",
        "## 7. 이번 루프의 커밋 (보고서 커밋 제외)",
        log or "- (없음)",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    plan = PLAN.read_text(encoding="utf-8")
    plan = re.sub(
        rf"^\|\s*☐(\s*\|[^\n]*?\|\s*{re.escape(a.tc)}\s*\|)",
        r"| ☑\1",
        plan,
        count=1,
        flags=re.M,
    )
    PLAN.write_text(plan, encoding="utf-8")
    ev["report"] = path.relative_to(ROOT).as_posix()
    ev["report_commit"] = commit(
        f"docs({a.tc}): 사이클 보고서 · 스멜 분석 [REPORT]", ev, ["docs", "plan.md"]
    )
    save(a.tc, ev)
    print(f"[OK] 보고서 {ev['report']} · plan.md {a.tc} ☑ · 커밋 {ev['report_commit']}")
    print(
        "[다음] git push 로 올리고, 사람이 /clear 한 뒤 go 를 보냅니다 (Stop · SessionEnd 훅이 Transcript 를 보관)."
    )


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="TDD 하네스 게이트 스크립트")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("next")
    for name in ("red", "green", "smell", "regress", "probe", "plan-check"):
        sub.add_parser(name).add_argument("tc")
    g = sub.add_parser("golden")
    g.add_argument("tc")
    g.add_argument("--approve", action="store_true")
    r = sub.add_parser("refactor")
    r.add_argument("tc")
    r.add_argument("rid")
    rp = sub.add_parser("report")
    rp.add_argument("tc")
    rp.add_argument("--note", default="")
    a = parser.parse_args()
    {
        "next": cmd_next,
        "red": cmd_red,
        "green": cmd_green,
        "golden": cmd_golden,
        "smell": cmd_smell,
        "plan-check": cmd_plan_check,
        "refactor": cmd_refactor,
        "regress": cmd_regress,
        "probe": cmd_probe,
        "report": cmd_report,
    }[a.cmd](a)


if __name__ == "__main__":
    main()
