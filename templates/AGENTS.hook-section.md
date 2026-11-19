
# 사이클 로그와 대화 기록 보관

- `.codex/hooks.json`(`python scripts/install_hooks.py` 로 만든다)의 훅이 `scripts/archive_session.py` 를 실행해 기록을 보관합니다 (UserPromptSubmit · PostToolUse · Stop · PreCompact · SessionStart · SessionEnd).
- 이벤트 로그: `logs/codex/<세션 ID 의 SHA-256 해시>/*.event.json` — 훅 입력 원문 · 보관 시각 · 보관 오류.
- Transcript: `docs/Prompt/NN.주제-날짜.md` — 세션마다 1개. 세션 중에는 같은 파일에 누적하고, 새 세션이면 번호(NN)가 올라갑니다.
- 사용자가 `/clear` 하면 새 세션이 시작됩니다. 마지막 응답이 끝날 때(Stop) 이미 Transcript 가 저장되어 있습니다. 루프마다 새 세션에서 시작하는 것을 기본으로 합니다.
- 사이클 보고서는 하네스가 `docs/reports/` 에 만들고 Git 에 커밋합니다. `logs/` 와 `docs/Prompt/` 는 Git 에서 제외하며 읽지 않습니다.
- 저장 오류가 표시되면 해당 루프의 기록 보관은 미완료입니다. 저장이 끝났다고 보고하지 않습니다.
- 훅은 응답이 끝난 뒤 실행되므로, 응답 안에서 저장이 끝났다고 미리 말하지 않습니다.
- 이 훅은 Codex 전용입니다. 설치 이전 대화의 소급 저장이나 강제 종료 시 저장을 보장하지 않습니다.
- 프롬프트에 비밀 값(키 · 토큰 · 개인정보)을 붙이지 않습니다. 기록에 남습니다.
