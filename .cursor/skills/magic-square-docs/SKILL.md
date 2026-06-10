---
name: magic-square-docs
description: >-
  MagicSquare_00 Report and Transcript export (Report/NN.REPORT.md,
  Prompting/NN.Export-Transcript.md). Use for Report Export, Transcript,
  /export-session, Phase repeat, ARRR cycle completion reports, or session N
  report requests.
disable-model-invocation: true
---

# magic-square-docs

세션 **Report** + **Prompting Transcript** Export Skill.

> **Export 요청 시 magic-square-docs Skill 로드 후 checklist 수행**

`/export-session` Command와 함께 사용. Command 트리거·파일명 규칙은 [`.cursor/commands/export-session.md`](../../commands/export-session.md) 우선.

## SSOT 형식

| 종류 | 경로 예 |
|------|---------|
| Report | `Report/05.REPORT.md` |
| Transcript | `Prompting/05.Export-Transcript.md` |

기존 예: `Report/04.REPORT.md` · `Prompting/04.Export-Transcript.md`

---

## 워크플로 (Step A → F)

상세 체크: [phase-checklist.md](phase-checklist.md)

### Step A — 입력 수집

| 입력 | 명령·출처 |
|------|-----------|
| git status | `git status --short` |
| pytest | `python -m pytest tests/ -v` |
| Phase | 채팅 `Phase: red\|green\|refactor\|repeat` |
| Test ID | D-LOC-01 · D-SOL-01 · T3 … |
| Command | `/red-test-plan` · `/green-minimal` · `/export-session` … |

**실측만 기록.** 채팅·터미널에 없는 pytest 결과 금지.

### Step B — NN = max(Report, Prompting) + 1

```
Report/NN.REPORT.md
Prompting/NN.Export-Transcript.md
```

- `Report/`·`Prompting/`에서 `NN.REPORT.md` · `NN.Export-Transcript.md` 패턴 스캔
- **NN = 최대 NN + 1** (사용자 지정 NN 있으면 그대로)

### Step C — Report

- 템플릿: [report-template.md](report-template.md)
- Phase별 **STEP:** RED · GREEN · REFACTOR · **repeat**
- ARRR 1사이클 완료 시 `STEP: repeat` + Phase 요약 표

### Step D — Transcript

- 템플릿: [transcript-template.md](transcript-template.md)
- `_Exported on YYYY-MM-DD from Cursor_`
- `_Source uuid: {uuid}` (agent transcript ID, 없으면 `—`)
- User / Cursor 시간순

### Step E — README 문서 표 갱신

루트 `README.md` **있을 때만** 세션 문서 표에 1행 추가:

```markdown
| NN | 주제 한 줄 | Report/NN.REPORT.md | Prompting/NN.Export-Transcript.md |
```

없으면 생략 · Step F에 `README 없음` 명시.

### Step F — 완료 보고

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

---

## `/export-session` 연동

| 항목 | 내용 |
|------|------|
| 트리거 | `Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘.` 또는 `/export-session` |
| Skill 로드 | **Export 요청 시 magic-square-docs Skill 로드 후 checklist 수행** |
| 필수 출력 | Report + Transcript **둘 다** |
| 파일명 | `NN.REPORT.md` · `NN.Export-Transcript.md` only |

TDD Phase·pytest·Command 상세는 [magic-square-tdd](../magic-square-tdd/SKILL.md)와 교차 참조.

---

## Phase: repeat (ARRR 1사이클 완료)

`Phase: repeat` 보고 시 Report §3에 **STEP: repeat** 추가:

| 필드 | 내용 |
|------|------|
| 완료 Test ID | 이번 사이클 ID |
| 경로 | RED ③→④→⑤ → GREEN → Golden → REFACTOR ⑦→⑧ |
| 회귀 | `python -m pytest tests/ -v` → 전부 PASSED (실측) |

---

## Report §3 STEP 요약

| STEP | Phase | 대표 Command |
|------|-------|--------------|
| RED | `Phase: red` | `/red-test-plan` · `/red-skeleton` · `/tdd-red` |
| GREEN | `Phase: green` | `/green-minimal` |
| Golden | `Phase: green` | `/golden-master` |
| REFACTOR | `Phase: refactor` | `/refactor-smell` · `/refactor-safe` |
| repeat | `Phase: repeat` | (사이클 완료 요약) |

---

## 금지

| 금지 | 이유 |
|------|------|
| **git commit / push 임의** | `.cursorrules` — 명시 요청 시만 |
| **`UPDATE_GOLDEN=1` 임의** | golden 갱신은 ISS·명시 후만 |
| **채팅에 없는 pytest 결과** | Export 신뢰성 |
| **Report 또는 Transcript 하나만** | Export Command 위반 |
| **`NN.*` 외 파일명** | 저장 규칙 |
| **`STEP*`·`cursor_*` Prompting 생성** | Export 범위 밖 |
| **대화 없는 내용 추측** | Transcript·Report 오염 |

---

## 빠른 참조

| 리소스 | 경로 |
|--------|------|
| Checklist | [phase-checklist.md](phase-checklist.md) |
| Report 템플릿 | [report-template.md](report-template.md) |
| Transcript 템플릿 | [transcript-template.md](transcript-template.md) |
| Export Command | `.cursor/commands/export-session.md` |
| TDD Skill | `.cursor/skills/magic-square-tdd/SKILL.md` |
| 규칙 | `.cursorrules` |

---

## Agent 실행 순서 (요약)

1. [phase-checklist.md](phase-checklist.md) Step A — 수집
2. Step B — NN 확정
3. [report-template.md](report-template.md) → `Report/NN.REPORT.md`
4. [transcript-template.md](transcript-template.md) → `Prompting/NN.Export-Transcript.md`
5. README 표 (있을 때)
6. Step F 완료 보고

응답 언어: **한국어**.
