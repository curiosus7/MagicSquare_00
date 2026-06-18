# Phase Checklist — magic-square-docs Export

`/export-session` 또는 Export 요청 시 **Step A~F** 순서로 체크. 추측·임의 실행 금지.

---

## Step A — 입력 수집

| # | 항목 | 수집 방법 | 기록 위치 |
|---|------|-----------|-----------|
| A1 | **git status** | `git status --short` (있을 때) | Report §3·Transcript |
| A2 | **pytest** | `python -m pytest tests/ -v` — **실제 출력만** | Report §3 · Phase 표 |
| A3 | **Phase** | 채팅·Command 응답 첫 줄 (`Phase: red\|green\|refactor\|repeat`) | Report §3 |
| A4 | **Test ID** | D-LOC-01 · D-SOL-01 · T3 등 채팅·플랜 근거 | Report §3 · 산출물 |
| A5 | **Command** | `/red-test-plan` · `/green-minimal` 등 실행 목록 | Transcript · Report §2 |
| A6 | **golden matched** | golden 연결 시 `UPDATE_GOLDEN` 없이 PASS 여부 | Report §3 GREEN/Golden 행 |
| A7 | **세션 주제** | 1문장 — PRD·Report·채팅 | Report 헤더 |

### Step A 금지

- 채팅·터미널에 **없는** pytest 결과 기재
- **`UPDATE_GOLDEN=1` 임의 실행**
- **`git commit` 임의 실행**

### Step A 완료 조건

- [ ] pytest 명령·결과가 **이번 세션에서 확인된 것**만 있음
- [ ] Phase·Test ID·Command가 대화와 일치
- [ ] git status 실행했거나 repo 없음을 명시

---

## Step B — 세션 번호 NN

| 규칙 | 내용 |
|------|------|
| 스캔 | `Report/NN.REPORT.md` · `Prompting/NN.Export-Transcript.md` 의 **NN 최대값** |
| 계산 | **NN = max + 1** (2자리: `05`, `06`, …) |
| 사용자 지정 | `05` 등 명시 시 그 번호 사용 |
| SSOT 예 | `Report/05.REPORT.md` · `Prompting/05.Export-Transcript.md` |

### Step B 완료 조건

- [ ] NN 확정·Report·Transcript **동일 NN**

---

## Step C — Report 작성

- 템플릿: [report-template.md](report-template.md)
- Phase별 **STEP** 블록: RED · GREEN · REFACTOR · **repeat** (ARRR 1사이클 완료 시)
- 경로: `Report/NN.REPORT.md`

### Step C 완료 조건

- [ ] `NN.REPORT.md` 형식 (`NN.XXX`)
- [ ] §3 TDD 표에 실제 Phase·pytest만
- [ ] §6 Transcript 링크

---

## Step D — Transcript 작성

- 템플릿: [transcript-template.md](transcript-template.md)
- **User / Cursor** 시간순
- 헤더: `_Exported on YYYY-MM-DD from Cursor_`
- 메타: `_Source uuid: {agent-transcript-uuid}` (알 수 있을 때)
- 경로: `Prompting/NN.Export-Transcript.md`

### Step D 완료 조건

- [ ] Command 이름·Phase·pytest fenced block (실측만)
- [ ] 추측 대화 없음

---

## Step E — README 문서 표 갱신

`README.md`가 **루트에 있을 때만**:

| 열 | 내용 |
|----|------|
| 세션 | NN |
| Report | `Report/NN.REPORT.md` |
| Transcript | `Prompting/NN.Export-Transcript.md` |
| 주제 | 1문장 |

`README.md` 없으면 Step E **생략** — Step F 보고에 `README 없음 — 생략` 명시.

### Step E 완료 조건

- [ ] README 있으면 표 1행 추가·갱신
- [ ] 없으면 생략 기록

---

## Step F — 완료 보고

```
## Export 완료

| 종류 | 경로 |
|------|------|
| Report | Report/NN.REPORT.md |
| Transcript | Prompting/NN.Export-Transcript.md |

## 세션 NN 요약
- (한 줄)

## 다음
- (한 줄)
```

### Step F 완료 조건

- [ ] 경로 **2개** 명시
- [ ] git commit 하지 않음 (명시 요청 전)
