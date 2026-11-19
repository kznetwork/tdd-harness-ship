# 실습 프롬프트 · 명령 · 파일 — ship (배송비 계산기 · 심화 과정)

교안(176쪽)의 **슬라이드 번호 순서**대로, 그 쪽에서 쓰는 프롬프트 · 명령 · 파일 내용을 그대로 모았다. 이 파일은 교안을 빌드할 때 슬라이드마다 자동으로 기록한 것이라 번호가 어긋나지 않는다. AI 응답 문구는 실행마다 다르며, 판단 기준은 언제나 `pytest` 결과와 하네스(`scripts/tdd.py`) 출력이다.

## 어디에서 실습하나 (작업 폴더)

| 항목 | 내용 |
|---|---|
| 작업 폴더 | `C:\DEV\tdd-harness\ship` |
| 만드는 법 | 강사가 나눠 준 `starter\ship` 을 `C:\DEV\tdd-harness\` 아래로 **폴더째 복사**한다 (슬라이드 가상환경 쪽의 명령) |
| 여는 법 | VS Code → 파일 → 폴더 열기 → `C:\DEV\tdd-harness\ship` · 터미널 ① · ② 와 `codex` 도 이 폴더에서 실행 |
| 처음 한 번 | `python -m venv .venv` → `.venv\Scripts\Activate.ps1` → `python -m pip install -r requirements-dev.txt` → `python -m pytest -q` (1 passed) |
| Codex | 반드시 `(.venv)` 가 켜진 터미널 ① 에서 `codex` 를 시작하고, 처음 물으면 이 폴더를 ‘신뢰’ 한다 |
| 막히면 | `solution\ship` (끝 상태) 또는 `solution\checkpoints\c02 ~ c09` (단계별 상태)와 비교 |

## 쓰는 법

- 이 파일을 VS Code 에서 열어 두고, **슬라이드 번호가 같은 항목**의 블록을 복사해 붙여 넣는다.
- **▶ 프롬프트** = Codex 에 붙여 넣는다 (터미널 ①, `.venv` 를 켠 상태). **⌨ 명령** = 터미널 ② (PowerShell) 에서 실행. **📄 파일** = 직접 만들어야 할 때 파일 내용 (대부분은 프롬프트나 `Copy-Item` 으로 만든다).
- 명령 블록의 `#` 뒤는 설명이다. 줄 앞의 `>` 와 `(.venv)` 는 프롬프트 표시이므로 붙이지 않는다 (이 파일에는 이미 뺐다).
- `<내계정>` · `<짝의 GitHub ID>` · `<복사한 토큰>` 처럼 꺾쇠가 있는 곳만 내 값으로 바꾼다.
- go 루프에서 사람이 입력하는 말은 `go` · `승인` · `/clear` 세 가지뿐이다.
- 토큰은 비밀번호와 같다. 채팅 · 프롬프트 · AGENTS.md 에 붙이지 않는다.

## 찾아보기

| 슬라이드 | 제목 | 프롬프트 | 명령 | 파일 |
|---:|---|---:|---:|---:|
| 9 | 실습 폴더 복사와 가상환경 만들기 — 복사 · 설치 · 첫 실행 |  | 1 |  |
| 10 | 설치 확인 — 가상환경 위에서 도구 버전을 본다 |  | 1 |  |
| 11 | VS Code 작업 화면 — 터미널 두 개로 나눠 쓴다 |  | 1 |  |
| 17 | GitHub MCP — Codex 가 저장소 · 이슈 · PR 을 만들게 하는 연결 |  | 1 |  |
| 18 | GitHub MCP 연결이 되는지 읽기 전용으로 확인한다 | 1 |  |  |
| 19 | GitHub 저장소 만들기(프롬프트) → 내 PC 의 저장소와 연결(터미널 ②) | 1 | 1 |  |
| 20 | Feature 브랜치(터미널 ②)와 이슈(프롬프트)를 만든다 | 1 | 1 |  |
| 27 | ① 맘 테스트 질문 8개를 AI 에게 만들게 한다 (읽기 전용) | 1 |  |  |
| 28 | ② 인터뷰를 진행하고 ③ 노트로 저장한다 | 1 |  |  |
| 31 | ④ 노트에서 우선순위가 있는 계약표를 만든다 | 1 |  |  |
| 33 | ⑤ 경계를 짝으로 점검하고 커밋한다 |  | 1 |  |
| 37 | ① PRD.md 를 계약표에서 만든다 | 1 |  |  |
| 39 | ② README.md — 사용 예는 doctest 형식으로 | 1 |  |  |
| 43 | ③ plan.md — 계약표를 작업 지시서로 | 1 |  |  |
| 46 | ④ 문서를 커밋하고 push 한다 |  | 1 |  |
| 50 | Codex 샌드박스는 .git 에 쓰지 못한다 — 그래서 하네스 명령만 규칙으로 허용한다 |  | 1 |  |
| 55 | ① ADR(아키텍처 결정 기록)을 프롬프트로 쓰게 한다 | 1 |  |  |
| 60 | ① 인수 테스트를 먼저 돌려 본다 — 하네스가 없어 모두 실패 (RED) |  | 1 |  |
| 61 | ② Codex 에게 공통 도구와 next 를 만들게 한다 | 1 |  |  |
| 62 | ③ red 를 더한다 — 이미 통과한 next 는 그대로 두고 | 1 |  |  |
| 63 | ④ green 을 더하고, 인수 테스트 14개를 모두 통과시킨다 (GREEN) | 1 | 1 |  |
| 64 | ⑤ 핵심 3개를 커밋하고, 나머지 7개는 제공본으로 이어 간다 | 1 | 1 |  |
| 65 | ⑥ 제공본 하네스를 처음 실행해 본다 — --help 와 next |  | 1 |  |
| 67 | ① 하네스 허용 규칙을 직접 만든다 — .codex/rules/tdd.rules |  | 2 | 1 |
| 77 | ② AGENTS.md 를 프롬프트로 만든다 — 빈칸 세 곳만 채우게 한다 | 1 | 1 |  |
| 78 | ③ Codex 가 AGENTS.md 를 읽는지 — debug prompt-input 으로 확인 | 1 | 1 |  |
| 79 | ④ 폴더 신뢰와 허용 규칙 — 승인 창 없이 하네스가 도는지 확인한다 | 1 | 1 |  |
| 80 | ⑤ ADR · AGENTS.md · 허용 규칙을 커밋하고 push 한다 |  | 1 |  |
| 87 | ① Codex 없이 훅을 손으로 실행해 본다 — 저장과 오류 알림 |  | 1 |  |
| 89 | ③ 훅 설치를 프롬프트로 시키고, Codex 를 재시작해 신뢰를 승인한다 | 1 | 1 |  |
| 93 | 일부러 틀린 입력 — 실패를 숨기지 않는지 확인한다 |  | 1 |  |
| 106 | 해 보기 — 하네스의 거절 두 가지와 Sanity 를 직접 본다 |  | 1 |  |
| 107 | 루프 ① (TC-1) — go 와 NEXT, 그리고 AI 가 쓴 RED 테스트 | 1 |  |  |
| 108 | 루프 ① — RED: 실패를 눈으로 확인하고 커밋한다 |  | 2 |  |
| 109 | 루프 ① — GREEN: 가짜 구현으로 통과시키고 커밋한다 |  | 2 |  |
| 110 | 루프 ① — 승인: 새 동작 행을 사람이 읽고 ‘승인’ 한다 | 1 | 2 |  |
| 111 | 루프 ① — 스멜 분석: 문서와 Mermaid 만 남긴다 |  | 1 |  |
| 112 | 루프 ① — 회귀 · Sanity, 보고서, push 로 마무리 |  | 3 |  |
| 113 | 루프 사이 의식 — 확인 · push · /clear · 새 go (함께) |  | 1 |  |
| 114 | 루프 ② (TC-2) — go: 경계 네 점과 구간 속성, 일부만 RED | 1 |  |  |
| 115 | 루프 ② — GREEN 은 조건 한 줄, 승인은 새 4행만 |  | 3 |  |
| 118 | 루프 ③ (TC-3) — go: 0 이하는 ValueError | 1 |  |  |
| 119 | 루프 ③ — GREEN: 가드 한 줄, 승인은 새 3행 |  | 3 |  |
| 120 | 일부러 규칙을 어겨 본다 — 하네스가 막는 순간 |  | 3 |  |
| 122 | 루프 ④ (TC-4) 전에 — 우연히 통과하는 테스트를 먼저 본다 |  | 1 |  |
| 124 | 루프 ④ — GREEN: 정수 검사를 먼저, 승인은 bool 까지 4행 |  | 3 |  |
| 127 | 루프 ⑤ (TC-5) — 마지막 루프의 시작, Red 없이 통과 | 1 |  |  |
| 128 | Red 없이 통과한 테스트를 믿는 법 — 변이 탐침 (probe) |  | 2 |  |
| 129 | 스멜 분석 — 쌓인 문서를 합쳐 정리한다 |  | 1 |  |
| 130 | 리팩터링 계획서 — 쌓인 스멜을 순서 · 안전망 · 위험이 있는 항목으로 |  | 1 |  |
| 131 | R-1 — 매직 넘버를 이름 있는 상수로 |  | 2 |  |
| 132 | R-2 — 입력 검증을 함수로 분리 (Extract Function) |  | 2 |  |
| 133 | 회귀 · Sanity — README 사용 예까지 실행 |  | 1 |  |
| 134 | 마지막 보고서와 plan.md 의 최종 상태 |  | 1 |  |
| 135 | 최종 상태 — 코드는 작아졌고, 테스트와 기록은 늘었다 |  | 1 |  |
| 136 | Pull Request 를 열고 짝을 리뷰어로 지정한다 — 머지는 리뷰 뒤 | 1 | 1 |  |
| 140 | 리뷰 코멘트를 쓰고 Approve 한다 — Codex 는 읽기 전용 1차 점검만 | 1 |  |  |

## 슬라이드 9 — 실습 폴더 복사와 가상환경 만들기 — 복사 · 설치 · 첫 실행

**⌨ 명령 — PowerShell**

```powershell
New-Item -ItemType Directory -Force C:\DEV\tdd-harness | Out-Null
Copy-Item -Recurse "<강사 배포 폴더>\starter\ship" C:\DEV\tdd-harness\ship
cd C:\DEV\tdd-harness\ship
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## 슬라이드 10 — 설치 확인 — 가상환경 위에서 도구 버전을 본다

**⌨ 명령 — 터미널**

```powershell
python --version
python -m pytest --version
python -m pip show hypothesis
git --version
codex --version
codex login status          # 로그인 확인 (처음이면 codex 를 실행해 로그인)
```

## 슬라이드 11 — VS Code 작업 화면 — 터미널 두 개로 나눠 쓴다

**⌨ 명령 — 터미널 ①**

```powershell
cd C:\DEV\tdd-harness\ship
code .                      # VS Code 로 폴더 열기
  (Ctrl+Shift+`  새 터미널)
.venv\Scripts\Activate.ps1
codex                      # 터미널 ① 에서만
```

## 슬라이드 17 — GitHub MCP — Codex 가 저장소 · 이슈 · PR 을 만들게 하는 연결

**⌨ 명령 — PowerShell — 터미널 ①**

```powershell
# 터미널 ① (가상환경을 켠 상태) — 토큰 값은 이 창에서만 유효
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "<복사한 토큰>"
# 한 번만: GitHub MCP 서버 등록 (설정에 이름만 저장)
codex mcp add github --url https://api.githubcopilot.com/mcp/ --bearer-token-env-var GITHUB_PERSONAL_ACCESS_TOKEN
# 등록 확인
codex mcp list
```

## 슬라이드 18 — GitHub MCP 연결이 되는지 읽기 전용으로 확인한다

**▶ 프롬프트 — 프롬프트 · MCP 연결 확인 (터미널 ①)**

```text
GitHub MCP 로 내 GitHub 로그인 ID 만 알려줘.
아무것도 만들거나 바꾸지 마.
```

## 슬라이드 19 — GitHub 저장소 만들기(프롬프트) → 내 PC 의 저장소와 연결(터미널 ②)

**▶ 프롬프트 — 프롬프트 ① · 저장소 만들기 (터미널 ①)**

```text
GitHub MCP 로 내 계정에 비공개(private) 저장소 tdd-harness-ship 을 만들어줘.
- README · .gitignore · 라이선스는 추가하지 마 (내 PC 에 이미 있다).
- 만든 뒤 HTTPS 주소만 알려줘. 다른 저장소는 건드리지 마.
```

**⌨ 명령 — PowerShell — 터미널 ② (ship 폴더)**

```powershell
git config user.name "이순신"
git config user.email "me@example.com"
git init -b main
git add .
git commit -m "chore: starter skeleton"
git remote add origin https://github.com/<내계정>/tdd-harness-ship.git
git push -u origin main
```

## 슬라이드 20 — Feature 브랜치(터미널 ②)와 이슈(프롬프트)를 만든다

**⌨ 명령 — PowerShell — 터미널 ②**

```powershell
git switch -c feature/F-01-shipping-fee
git push -u origin feature/F-01-shipping-fee
git branch -vv
```

**▶ 프롬프트 — 프롬프트 ② · 이슈 만들기 (터미널 ①)**

```text
GitHub MCP 로 저장소 tdd-harness-ship 에 이슈를 하나 만들어줘.
제목: F-01 배송비 계산 · 라벨: feature
본문:
운영자로서, 결제 금액에 맞는 배송비를 자동으로 얻고 싶다.
Theme T-1 · Epic E-1 · 브랜치 feature/F-01-shipping-fee
- [ ] TC-1 기본 배송비 3,000원
- [ ] TC-2 30,000원 이상 무료
- [ ] TC-3 0원 이하는 ValueError
- [ ] TC-4 정수가 아니면 TypeError
- [ ] TC-5 배송비 불변식
만든 뒤 이슈 번호와 주소만 알려줘.
```

## 슬라이드 27 — ① 맘 테스트 질문 8개를 AI 에게 만들게 한다 (읽기 전용)

**▶ 프롬프트 — 프롬프트 — 맘 테스트 질문 (읽기 전용)**

```text
역할: 맘 테스트(The Mom Test) 원칙을 따르는 요구사항 인터뷰어.
@docs/요구사항.md 의 세 줄을 읽고, 온라인 쇼핑몰 운영자에게 물어볼 질문 8개를 만들어줘. 파일은 수정하지 마.
규칙: ① 과거의 구체적인 사례를 묻는다 (“마지막으로 …”, “지난번에 …”).
      ② “~하면 좋을까요?” “~하시겠어요?” 같은 미래 가정 · 의견 질문은 쓰지 않는다.
      ③ 우리 기능을 소개하거나 해결책을 제안하지 않는다.
각 질문 옆에 ‘이 질문으로 알아내려는 것’ 을 한 줄로 적어줘.
```

## 슬라이드 28 — ② 인터뷰를 진행하고 ③ 노트로 저장한다

**▶ 프롬프트 — 프롬프트 — 인터뷰 진행 · 노트 저장**

```text
좋아. 이제 네가 인터뷰어, 내가 소나무마켓 운영자 역할이다.
한 번에 질문 하나씩만 하고 내 답을 기다려줘. 답이 모호하면 꼬리 질문은 한 번만 해.
8개를 다 묻고 나면 아래 서식으로 docs/interview/인터뷰노트.md 를 만들어줘.
  1) 겪은 일(사실): # | 질문 | 답 요약 | 읽어 낸 것
  2) 요구사항 3줄에 없던 것
  3) 결정할 수 없었던 것(OQ)
내 답에 없는 내용은 지어내지 마.
```

## 슬라이드 31 — ④ 노트에서 우선순위가 있는 계약표를 만든다

**▶ 프롬프트 — 프롬프트 — 계약표 + 우선순위**

```text
역할: 요구사항 분석가. @docs/요구사항.md 와 @docs/interview/인터뷰노트.md 를 근거로 docs/계약표.md 를 만들어줘.
열: P(우선순위) | 계약 ID | 유형(AC·E·INV·OQ) | 규칙 | 사전조건 | 사후조건 | 오류 | 근거(인터뷰 Q 번호)
우선순위: ① 정상 경로 ② 사고 이력이 있는 경계 ③ 입력 방어 ④ 전체를 감시하는 불변식은 맨 뒤 (P 가 가장 큰 계약이 마지막 루프다).
오류 메시지는 내가 정한다: 0 이하 → ValueError("주문 금액은 0보다 커야 합니다."), 정수 아님(bool 포함) → TypeError("주문 금액은 정수여야 합니다.").
새 규칙은 지어내지 말고, 인터뷰에서 정해지지 않은 것은 OQ 로 남기고 P 에 ⏸ 를 적어줘.
```

## 슬라이드 33 — ⑤ 경계를 짝으로 점검하고 커밋한다

**⌨ 명령 — PowerShell**

```powershell
git add docs\interview
git commit -m "docs(F-01): 맘 테스트 인터뷰 노트"
git add docs\계약표.md
git commit -m "docs(F-01): 계약표 (우선순위 P1~P5)"
git log --oneline -n 2
```

## 슬라이드 37 — ① PRD.md 를 계약표에서 만든다

**▶ 프롬프트 — 프롬프트 — PRD.md**

```text
역할: 제품 기획자. @docs/요구사항.md @docs/interview/인터뷰노트.md @docs/계약표.md 를 근거로 프로젝트 루트에 PRD.md 를 만들어줘.
구성: 맨 위 표(Theme · Epic · Feature · 브랜치 · 근거) / 1 배경과 문제 / 2 목표와 비목표 / 3 기능 요구사항(계약표와 1:1, 수용 기준 예) / 4 비기능 요구사항 / 5 가정 · 결정 · 미해결 / 6 추적.
Theme 은 ‘T-1 주문 · 결제 경험 개선’, Epic 은 ‘E-1 배송비 정책 자동화’, Feature 는 ‘F-01 배송비 계산’, 브랜치는 feature/F-01-shipping-fee 로 적어줘.
인터뷰에 없는 사실은 지어내지 말고, 근거는 Q 번호로 적어줘. 길이는 한 화면 반(60줄 안팎).
```

## 슬라이드 39 — ② README.md — 사용 예는 doctest 형식으로

**▶ 프롬프트 — 프롬프트 — README.md (doctest 사용 예 · 릴리스 정보 · To-Do)**

```text
@PRD.md @docs/계약표.md 를 근거로 프로젝트 루트에 README.md 를 만들어줘.
구성: 한 줄 소개 / 설치와 실행(venv · pip install -r requirements-dev.txt · python -m pytest -q) / 사용 예 / 규칙 표 / 범위 밖 / 릴리스 정보 / To-Do / 개발 방법.
‘사용 예’ 는 반드시 파이썬 doctest 형식(>>> 와 기대 출력)으로, 다음 다섯 개만 적어줘:
  10_000 → 3000 · 29_999 → 3000 · 30_000 → 0 · 0 → ValueError · 29_999.5 → TypeError
예외는 ‘Traceback (most recent call last):’ / ‘    ...’ / ‘오류종류: 메시지’ 세 줄 형식으로 쓰고, 코드 블록 안 마지막 예시 뒤에 빈 줄을 하나 둬줘 (doctest 가 거기서 끝난다).
‘릴리스 정보’: 버전은 SemVer 라는 한 줄 설명 + 표(버전 | 날짜 | 포함한 Feature | 변경 요약). 0.1.0(예정 · F-01 배송비 계산)과 0.2.0(계획 · F-02 도서산간)의 두 행만.
‘To-Do’: 체크박스 목록. 만든 F-01 은 [x], 계약표의 OQ 와 PRD 의 미해결 항목은 [ ] 로 적어줘.
```

## 슬라이드 43 — ③ plan.md — 계약표를 작업 지시서로

**▶ 프롬프트 — 프롬프트 — plan.md**

```text
@docs/계약표.md 와 @PRD.md 로 프로젝트 루트에 plan.md 를 만들어줘.
맨 위 ‘지침’ 구역: (1) AGENTS.md 의 go 루프를 따르고 go 한 번에 첫 ☐ TC 하나만 처리한다 (2) 상태는 ☐ 미완료 · ☑ 완료 · ⏸ 결정 대기(건너뜀)이고 ☑ 는 하네스가 표시한다 (3) P 는 구현 순서이며 가장 큰 P 의 TC 가 마지막 루프다.
‘테스트 목록’ 표 열: 상태 | P | TC | 계약 | 유형 | 제목 | 입력 | 기대 결과
계약마다 TC 하나(INV-1 · 2 는 하나로 묶는다), P 순서대로, 상태는 ☐. OQ 는 상태 ⏸, P 는 – 로 둔다. 표 칸 안에 세로선(|)을 쓰지 마.
```

## 슬라이드 46 — ④ 문서를 커밋하고 push 한다

**⌨ 명령 — PowerShell**

```powershell
git add PRD.md README.md
git commit -m "docs(F-01): PRD.md · README.md"
git add plan.md
git commit -m "docs(F-01): plan.md 테스트 목록"
git push
git log --oneline --reverse main..HEAD
```

## 슬라이드 50 — Codex 샌드박스는 .git 에 쓰지 못한다 — 그래서 하네스 명령만 규칙으로 허용한다

**⌨ 명령 — PowerShell (실제 실행)**

```powershell
codex sandbox -c sandbox_mode="workspace-write" powershell.exe -NoProfile -Command "'ok' | Set-Content probe.txt; Get-Content probe.txt; git add -A; git commit -qm probe"
```

## 슬라이드 55 — ① ADR(아키텍처 결정 기록)을 프롬프트로 쓰게 한다

**▶ 프롬프트 — 프롬프트 · ADR 쓰기 (터미널 ①)**

```text
docs/adr/0001-하네스-스켈레톤.md 를 만들어줘 (docs/adr 폴더가 없으면 만들어).
ADR 형식: 제목 · 상태(채택) · 배경 · 선택지(A 지침만 · B 파이썬 게이트 스크립트 + AGENTS.md · C /goal) · 결정(B) · 결과(좋은 점 · 감수할 점) · 다시 볼 때.
근거로 쓸 사실은 이것만이야: ① 규칙 문장만으로는 ‘Red 를 봤다’ 는 거짓 보고를 막지 못한다 ② Codex 샌드박스는 .git 에 쓰지 못해 하네스 명령만 허용 규칙(.codex/rules/tdd.rules)으로 샌드박스 밖에서 실행한다 ③ /goal 은 끝났는지를 모델이 판정해 승인 대기와 맞지 않는다.
10줄 이내로 쓰고 다른 파일은 건드리지 마.
```

## 슬라이드 60 — ① 인수 테스트를 먼저 돌려 본다 — 하네스가 없어 모두 실패 (RED)

**⌨ 명령 — PowerShell — 터미널 ② (ship 폴더)**

```powershell
code docs\harness\하네스명세.md      # 훑어 읽는다 (2 ~ 4절이 만들 것)
dir scripts
python -m pytest harness_tests -q
```

## 슬라이드 61 — ② Codex 에게 공통 도구와 next 를 만들게 한다

**▶ 프롬프트 — 프롬프트 ② · 공통 도구 + next (터미널 ①)**

```text
docs/harness/하네스명세.md 를 읽고 scripts/tdd.py 를 만들어줘.
- 이번에는 1절 ‘공통 도구’ 와 2절 next 만 구현해 (red · green 은 아직 만들지 마).
- 표준 라이브러리만 쓰고, 명세에 적힌 [STOP] 메시지 문구를 그대로 써.
- 다 만든 뒤 python -m pytest harness_tests -q -k test_next 를 실행해서 결과를 그대로 알려줘. 실패하면 tdd.py 만 고쳐서 다시 실행해. harness_tests/ 는 고치지 마.
```

## 슬라이드 62 — ③ red 를 더한다 — 이미 통과한 next 는 그대로 두고

**▶ 프롬프트 — 프롬프트 ③ · red (터미널 ①)**

```text
docs/harness/하네스명세.md 의 3절 red 를 scripts/tdd.py 에 추가해줘.
- 이미 만든 공통 도구와 next 는 바꾸지 마.
- 다 만든 뒤 python -m pytest harness_tests -q -k "test_next or test_red" 를 실행해서 결과를 그대로 알려줘. 실패하면 tdd.py 만 고쳐서 다시 실행해. harness_tests/ 는 고치지 마.
```

## 슬라이드 63 — ④ green 을 더하고, 인수 테스트 14개를 모두 통과시킨다 (GREEN)

**▶ 프롬프트 — 프롬프트 ④ · green (터미널 ①)**

```text
docs/harness/하네스명세.md 의 4절 green 을 scripts/tdd.py 에 추가해줘.
- 이미 만든 공통 도구 · next · red 는 바꾸지 마.
- 다 만든 뒤 python -m pytest harness_tests -q 전체를 실행해서 결과를 그대로 알려줘. 실패하면 tdd.py 만 고쳐서 다시 실행해. harness_tests/ 는 고치지 마.
```

**⌨ 명령 — PowerShell — 터미널 ②**

```powershell
python -m pytest harness_tests -q      # 터미널 ② 에서 한 번 더 — 내 눈으로
```

## 슬라이드 64 — ⑤ 핵심 3개를 커밋하고, 나머지 7개는 제공본으로 이어 간다

**⌨ 명령 — PowerShell — 터미널 ② (ship 폴더)**

```powershell
git add scripts docs\harness harness_tests
git commit -m "feat(F-01): 하네스 핵심 — next · red · green"
Copy-Item templates\harness\tdd.full.py scripts\tdd.py -Force
python -m pytest harness_tests -q
python scripts/tdd.py --help
git add scripts
git commit -m "feat(F-01): 하네스 나머지 7개 명령(제공본)"
git push
```

**▶ 프롬프트 — 프롬프트 · 과제 — 다음 명령도 같은 방식으로**

```text
(과제 — 시간이 있을 때) docs/harness/하네스명세.md 5절의 golden 을 만들고 싶어.
먼저 이 명령의 명세를 같은 형식(확인 · 거절하는 말 · 통과하면)으로 5절 뒤에 써 주고, 그에 맞는 인수 테스트를 harness_tests/ 에 추가해 RED 를 보여줘. 구현은 그다음에 하자.
```

## 슬라이드 65 — ⑥ 제공본 하네스를 처음 실행해 본다 — --help 와 next

**⌨ 명령 — PowerShell — 터미널 ② (ship 폴더)**

```powershell
python scripts/tdd.py --help
python scripts/tdd.py next
dir logs\tdd\TC-1
```

## 슬라이드 67 — ① 하네스 허용 규칙을 직접 만든다 — .codex/rules/tdd.rules

**📄 파일 — .codex\rules\tdd.rules — 이 내용을 그대로 붙여 넣는다**

```text
# 하네스 실행 허용 규칙 (Codex 실행 정책 — 프로젝트를 '신뢰'해야 읽힌다)
#
# Codex 샌드박스는 .git 에 쓰지 못한다. 그래서 커밋을 만드는 하네스 명령은
# 샌드박스 밖에서 실행해야 한다. 아래 규칙은 '이 명령으로 시작하는 것만' 물어보지 않고 실행한다.
# 그 밖의 명령(git commit 직접 실행 등)은 평소처럼 샌드박스 안에서 실행되거나 승인을 묻는다.

prefix_rule(
    pattern = ["python", "scripts/tdd.py"],
    decision = "allow",
    justification = "TDD 하네스: 증거를 남기고 단계마다 커밋을 만든다",
    match = ["python scripts/tdd.py next", "python scripts/tdd.py red TC-1", "python scripts/tdd.py golden TC-2 --approve"],
    not_match = ["python scripts/other.py", "python -m pytest -q"],
)

prefix_rule(
    pattern = ["python", "scripts/install_hooks.py"],
    decision = "allow",
    justification = "5교시: templates/hooks.template.json 으로 .codex/hooks.json 을 만든다 (.codex 는 샌드박스에서 읽기 전용)",
    match = ["python scripts/install_hooks.py", "python scripts/install_hooks.py --check"],
)
```

**⌨ 명령 — PowerShell — 터미널 ②**

```powershell
New-Item -ItemType Directory -Force .codex\rules | Out-Null
code .codex\rules\tdd.rules        # 왼쪽 내용 붙여 넣기 → 저장
codex execpolicy check --rules .codex/rules/tdd.rules -- python scripts/tdd.py red TC-1
codex execpolicy check --rules .codex/rules/tdd.rules -- git commit -m x
```

**⌨ 명령 — PowerShell — 대안**

```powershell
# 직접 만들기 싫을 때(대안) — 같은 내용을 복사
New-Item -ItemType Directory -Force .codex\rules | Out-Null
Copy-Item templates\harness\tdd.rules .codex\rules\tdd.rules
```

## 슬라이드 77 — ② AGENTS.md 를 프롬프트로 만든다 — 빈칸 세 곳만 채우게 한다

**▶ 프롬프트 — 프롬프트 · AGENTS.md 만들기 (터미널 ①)**

```text
templates/AGENTS.template.md 를 읽고 프로젝트 루트에 AGENTS.md 를 만들어줘.
- 템플릿의 내용은 한 글자도 바꾸지 말고 <<채우기 ①②③>> 세 곳만 채워줘.
  ① 브랜치 이름 규칙: feature/F-<번호>-<영문-슬러그> (예: feature/F-01-shipping-fee)
  ② 마지막 루프가 아닐 때 하지 않는 일: 코드를 고치는 리팩터링을 하지 않고 스멜 분석 문서만 남깁니다
  ③ 단위 테스트 전체 명령: python -m pytest -q -m "not golden"
- 다 채운 뒤 ‘<<채우기’ 가 몇 곳 남았는지 알려줘. 다른 파일은 건드리지 마.
```

**⌨ 명령 — PowerShell — 터미널 ②**

```powershell
Copy-Item templates\AGENTS.template.md AGENTS.md
code AGENTS.md          # <<채우기 ①②③>> 세 곳을 오른쪽 표대로 고친다
Select-String -Path AGENTS.md -Pattern "<<채우기"
```

## 슬라이드 78 — ③ Codex 가 AGENTS.md 를 읽는지 — debug prompt-input 으로 확인

**⌨ 명령 — PowerShell (실제 구조)**

```powershell
codex debug prompt-input "go" | Select-String "project-doc" -Context 0,3
```

**▶ 프롬프트 — 프롬프트 — 이해 확인 (읽기 전용)**

```text
파일은 수정하지 마. go 를 받으면 어떤 순서로 무엇을 할지 9단계로 요약해줘.
각 단계에서 실행할 하네스 명령, 마지막 루프에서만 달라지는 점, 사람이 해야 하는 일(승인 · push · /clear)도 적어줘.
그리고 커밋은 누가 어떻게 만드는지도 한 줄로 말해줘.
```

## 슬라이드 79 — ④ 폴더 신뢰와 허용 규칙 — 승인 창 없이 하네스가 도는지 확인한다

**▶ 프롬프트 — 프롬프트 · 하네스 첫 호출 (터미널 ①)**

```text
python scripts/tdd.py next 를 실행해줘.
결과만 그대로 보여주고 파일은 고치지 마.
```

**⌨ 명령 — Codex 안에서 (성공하면 이렇게 — 승인 창이 없다)**

```powershell
codex                    # ship 폴더 · (.venv) 를 켠 터미널 ①
```

## 슬라이드 80 — ⑤ ADR · AGENTS.md · 허용 규칙을 커밋하고 push 한다

**⌨ 명령 — PowerShell**

```powershell
git add docs\adr AGENTS.md
git commit -m "docs(F-01): ADR-0001 하네스 스켈레톤 · AGENTS.md"
git push
git log --oneline -n 3
```

## 슬라이드 87 — ① Codex 없이 훅을 손으로 실행해 본다 — 저장과 오류 알림

**⌨ 명령 — PowerShell — 터미널 ② (ship 폴더)**

```powershell
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new()   # 이 창에서만 한글 깨짐 방지
'{"session_id":"demo-session-0001","hook_event_name":"UserPromptSubmit","transcript_path":null,"cwd":".","prompt":"go"}' | python -X utf8 scripts\archive_session.py --echo
'{"session_id":"demo-session-0001","hook_event_name":"Stop","transcript_path":null,"cwd":".","last_assistant_message":"TC-1 완료: RED → GREEN. 보고서: docs/reports/demo.md"}' | python -X utf8 scripts\archive_session.py --echo
'{"session_id":"demo-session-0001","hook_event_name":"SessionEnd","transcript_path":null,"cwd":".","reason":"other"}' | python -X utf8 scripts\archive_session.py --echo
```

## 슬라이드 89 — ③ 훅 설치를 프롬프트로 시키고, Codex 를 재시작해 신뢰를 승인한다

**▶ 프롬프트 — 프롬프트 · 훅 설치 (터미널 ①)**

```text
훅 설치를 해줘. 순서대로 하고 단계마다 결과를 알려줘.
1) python scripts/install_hooks.py 를 실행해 .codex/hooks.json 을 만든다.
2) python scripts/install_hooks.py --check 로 확인한다.
3) templates/AGENTS.hook-section.md 의 내용을 AGENTS.md 맨 아래에 그대로 덧붙인다 (다른 부분은 바꾸지 않는다).
.codex 폴더와 scripts/ 는 직접 고치지 마. 다른 파일은 건드리지 마.
```

**⌨ 명령 — PowerShell — 터미널 ②**

```powershell
# 직접 하고 싶을 때(대안) — 터미널 ②
python scripts/install_hooks.py
python scripts/install_hooks.py --check
Get-Content templates\AGENTS.hook-section.md | Add-Content AGENTS.md -Encoding utf8
Select-String -Path AGENTS.md -Pattern "사이클 로그와 대화 기록 보관"
```

## 슬라이드 93 — 일부러 틀린 입력 — 실패를 숨기지 않는지 확인한다

**⌨ 명령 — PowerShell (실제 실행)**

```powershell
'{}' | python -X utf8 scripts\archive_session.py --echo
'{"session_id":"demo-session-0001","hook_event_name":"AfterAgent","prompt":"go"}' | python -X utf8 scripts\archive_session.py --echo
```

## 슬라이드 106 — 해 보기 — 하네스의 거절 두 가지와 Sanity 를 직접 본다

**⌨ 명령 — PowerShell — 터미널 ② (실제 실행)**

```powershell
python scripts/tdd.py red TC-1          # next 없이 red
python scripts/tdd.py next
python scripts/tdd.py red TC-1          # 테스트를 쓰기 전에 red
python -m pytest -q -m golden
python scripts/sanity.py --upto 1
```

## 슬라이드 107 — 루프 ① (TC-1) — go 와 NEXT, 그리고 AI 가 쓴 RED 테스트

**▶ 프롬프트 — 프롬프트**

```text
go
```

## 슬라이드 108 — 루프 ① — RED: 실패를 눈으로 확인하고 커밋한다

**⌨ 명령 — 하네스 red (실제)**

```powershell
python scripts/tdd.py red TC-1
```

**⌨ 명령 — git log**

```powershell
git log --oneline -n 1
```

## 슬라이드 109 — 루프 ① — GREEN: 가짜 구현으로 통과시키고 커밋한다

**⌨ 명령 — pytest (실제)**

```powershell
python -m pytest -q -m "not golden"
```

**⌨ 명령 — 하네스 green (실제)**

```powershell
python scripts/tdd.py green TC-1
```

## 슬라이드 110 — 루프 ① — 승인: 새 동작 행을 사람이 읽고 ‘승인’ 한다

**⌨ 명령 — 하네스 golden — 제안 (실제, 종료 코드 3)**

```powershell
python scripts/tdd.py golden TC-1
```

**▶ 프롬프트 — 프롬프트 — 사람의 답**

```text
승인
```

**⌨ 명령 — 하네스 golden --approve (실제)**

```powershell
python scripts/tdd.py golden TC-1 --approve
```

## 슬라이드 111 — 루프 ① — 스멜 분석: 문서와 Mermaid 만 남긴다

**⌨ 명령 — 하네스 smell (실제)**

```powershell
python scripts/tdd.py smell TC-1
```

## 슬라이드 112 — 루프 ① — 회귀 · Sanity, 보고서, push 로 마무리

**⌨ 명령 — regress (실제)**

```powershell
python scripts/tdd.py regress TC-1
```

**⌨ 명령 — report (실제)**

```powershell
python scripts/tdd.py report TC-1 --note "…"
```

**⌨ 명령 — git push (사람)**

```powershell
git push
```

## 슬라이드 113 — 루프 사이 의식 — 확인 · push · /clear · 새 go (함께)

**⌨ 명령 — PowerShell · Codex**

```powershell
git log --oneline -n 4
git push
/clear                 # Codex 안에서 — 새 세션 (Stop 훅이 이미 Transcript 저장)
dir docs\Prompt
```

## 슬라이드 114 — 루프 ② (TC-2) — go: 경계 네 점과 구간 속성, 일부만 RED

**▶ 프롬프트 — 프롬프트**

```text
go
```

## 슬라이드 115 — 루프 ② — GREEN 은 조건 한 줄, 승인은 새 4행만

**⌨ 명령 — green (실제)**

```powershell
python scripts/tdd.py green TC-2
```

**⌨ 명령 — golden 제안 (실제)**

```powershell
python scripts/tdd.py golden TC-2
```

**⌨ 명령 — 승인 뒤 (실제)**

```powershell
승인
python scripts/tdd.py golden TC-2 --approve
```

## 슬라이드 118 — 루프 ③ (TC-3) — go: 0 이하는 ValueError

**▶ 프롬프트 — 프롬프트**

```text
go
```

## 슬라이드 119 — 루프 ③ — GREEN: 가드 한 줄, 승인은 새 3행

**⌨ 명령 — green (실제)**

```powershell
python scripts/tdd.py green TC-3
```

**⌨ 명령 — golden 제안 (실제)**

```powershell
python scripts/tdd.py golden TC-3
```

**⌨ 명령 — 승인 뒤 (실제)**

```powershell
승인
python scripts/tdd.py golden TC-3 --approve
```

## 슬라이드 120 — 일부러 규칙을 어겨 본다 — 하네스가 막는 순간

**⌨ 명령 — PowerShell**

```powershell
(Get-Content tests\test_ct3_non_positive.py) -replace 'match="0보다"','match=""' | Set-Content tests\test_ct3_non_positive.py -Encoding utf8
python scripts/tdd.py green TC-3
git checkout -- tests\test_ct3_non_positive.py
```

**⌨ 명령 — PowerShell**

```powershell
python scripts/tdd.py report TC-3 --note "x"
```

**⌨ 명령 — PowerShell**

```powershell
python scripts/tdd.py next
python scripts/tdd.py red TC-3
```

## 슬라이드 122 — 루프 ④ (TC-4) 전에 — 우연히 통과하는 테스트를 먼저 본다

**⌨ 명령 — 구현 전에도 통과 (실제 실행)**

```powershell
python -m pytest -q tests/test_accident.py
```

## 슬라이드 124 — 루프 ④ — GREEN: 정수 검사를 먼저, 승인은 bool 까지 4행

**⌨ 명령 — green (실제)**

```powershell
python scripts/tdd.py green TC-4
```

**⌨ 명령 — golden 제안 (실제)**

```powershell
python scripts/tdd.py golden TC-4
```

**⌨ 명령 — 승인 뒤 (실제)**

```powershell
승인
python scripts/tdd.py golden TC-4 --approve
```

## 슬라이드 127 — 루프 ⑤ (TC-5) — 마지막 루프의 시작, Red 없이 통과

**▶ 프롬프트 — 프롬프트**

```text
go
```

## 슬라이드 128 — Red 없이 통과한 테스트를 믿는 법 — 변이 탐침 (probe)

**⌨ 명령 — probe (실제)**

```powershell
python scripts/tdd.py probe TC-5
```

**⌨ 명령 — green · golden (실제)**

```powershell
python scripts/tdd.py green TC-5
python scripts/tdd.py golden TC-5
```

## 슬라이드 129 — 스멜 분석 — 쌓인 문서를 합쳐 정리한다

**⌨ 명령 — smell (실제)**

```powershell
python scripts/tdd.py smell TC-5
```

## 슬라이드 130 — 리팩터링 계획서 — 쌓인 스멜을 순서 · 안전망 · 위험이 있는 항목으로

**⌨ 명령 — plan-check (실제)**

```powershell
python scripts/tdd.py plan-check TC-5
```

## 슬라이드 131 — R-1 — 매직 넘버를 이름 있는 상수로

**⌨ 명령 — refactor R-1 (실제)**

```powershell
python scripts/tdd.py refactor TC-5 R-1
```

**⌨ 명령 — git show --stat (실제)**

```powershell
git show --stat
```

## 슬라이드 132 — R-2 — 입력 검증을 함수로 분리 (Extract Function)

**⌨ 명령 — refactor R-2 (실제)**

```powershell
python scripts/tdd.py refactor TC-5 R-2
```

**⌨ 명령 — git log (실제)**

```powershell
git log --oneline -n 3
```

## 슬라이드 133 — 회귀 · Sanity — README 사용 예까지 실행

**⌨ 명령 — regress (실제)**

```powershell
python scripts/tdd.py regress TC-5
```

## 슬라이드 134 — 마지막 보고서와 plan.md 의 최종 상태

**⌨ 명령 — report (실제)**

```powershell
python scripts/tdd.py report TC-5 --note "…"
```

## 슬라이드 135 — 최종 상태 — 코드는 작아졌고, 테스트와 기록은 늘었다

**⌨ 명령 — 최종 확인 (실제)**

```powershell
python -m pytest -q
python scripts/sanity.py --upto 5 --readme
git log --oneline main..HEAD | Measure-Object -Line
```

## 슬라이드 136 — Pull Request 를 열고 짝을 리뷰어로 지정한다 — 머지는 리뷰 뒤

**▶ 프롬프트 — 프롬프트 · PR 열기 (터미널 ①)**

```text
GitHub MCP 로 저장소 tdd-harness-ship 에 Pull Request 를 만들어줘.
base: main · head: feature/F-01-shipping-fee · 제목: F-01 배송비 계산
본문:
Closes #1
## 요약
결제 금액에 맞는 배송비를 계산한다 (CT-1 ~ 4, INV-1 · 2). 도서산간(OQ-1)은 다음 릴리스.
## 증거
- 사이클 보고서 5개: docs/reports/
- 테스트 19개 통과 · 골든 14행 · README 예시 6/6
- 리팩터링 R-1 · R-2 (계획서: docs/refactor/refactor-plan.md)
리뷰어로 <짝의 GitHub ID> 를 요청해줘. 머지는 하지 마. 만든 뒤 PR 번호와 주소만 알려줘.
```

**⌨ 명령 — PowerShell · 웹**

```powershell
# 터미널 ② — PR 을 열기 전에
git status                # 깨끗한가
git push                  # 마지막 커밋까지 올리기
git log --oneline -n 3
# GitHub 웹 (한 번)
저장소 → Settings → Collaborators
→ Add people → 짝의 GitHub ID
```

## 슬라이드 140 — 리뷰 코멘트를 쓰고 Approve 한다 — Codex 는 읽기 전용 1차 점검만

**▶ 프롬프트 — 프롬프트 · 1차 점검 (선택, 터미널 ①)**

```text
읽기 전용으로 점검해줘. 파일은 고치지 마.
main 과 현재 브랜치의 차이(git diff main...HEAD)와 docs/reports/ 를 보고 아래만 알려줘.
1) RED 이후 tests/ 가 바뀐 커밋이 있는가
2) 보고서의 passed 수와 git log 가 맞지 않는 곳
3) 구조 변경(refactor)과 동작 변경이 한 커밋에 섞인 곳
근거로 커밋 해시를 같이 적어줘.
```
