# Transcript Template — `Prompting/NN.Export-Transcript.md`

SSOT 예: `Prompting/05.Export-Transcript.md`.

---

```markdown
# MagicSquare_00 — 세션 NN Transcript
_Exported on YYYY-MM-DD from Cursor_
_Source uuid: {agent-transcript-uuid}_

---

**User**

(사용자 메시지 — 요약 또는 원문)

---

**Cursor**

(응답 요약 — `Phase: …` · 변경 파일 · pytest 결과)

```bash
(실제 실행한 pytest 명령·출력 — 세션에서 확인된 것만)
```

---

**User**

...

---

**Cursor**

**Phase: red | Layer: entity | Track: Logic**

(Command·스멜·Export 등 이번 턴 핵심)

---

*본 문서는 `Prompting/NN.Export-Transcript.md` — MagicSquare_00 세션 NN 대화 Export입니다.*
```

---

## 작성 규칙

| 규칙 | 내용 |
|------|------|
| **순서** | User → Cursor 교차, 시간순 |
| **Command** | `/red-test-plan` · `/export-session` 등 **실행된 것만** |
| **Phase** | Cursor 블록에 첫 줄 Phase 있으면 인용 |
| **pytest** | fenced `bash` — **채팅·터미널 실측만** |
| **_Source uuid** | Cursor agent transcript ID 알 수 있으면 기재; 없으면 `_Source uuid: —` |
| **코드 diff** | 핵심 변경만 짧게; 전체 파일 붙여넣기 지양 |

---

## 금지

- 대화에 없는 pytest **성공/실패 조작**
- `UPDATE_GOLDEN=1` 실행을 Transcript에 넣을 때 — **사용자·ISS 명시 없으면 기록하지 않음**
- `STEP*` · `cursor_*` 별도 파일 생성 (Export Command 범위 밖)
