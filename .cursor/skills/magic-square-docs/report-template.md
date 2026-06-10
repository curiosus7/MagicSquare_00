# Report Template — `Report/NN.REPORT.md`

SSOT 예: `Report/05.REPORT.md`. `NN` = Step B에서 확정한 2자리 세션 번호.

---

```markdown
# MagicSquare_00 — 세션 NN 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_00 |
| 세션 | NN — (세션 주제 한 줄) |
| 보고서 생성일 | YYYY-MM-DD |
| 범위 | (예: ARRR Commands · entity TDD · Golden · REFACTOR) |
| ARRR 사이클 | (예: A(RED) → R(GREEN) → R(Refine) · repeat 여부) |

---

## 1. 요약

(3~5줄: 이번 세션 작업, pytest 최종 상태, 다음 단계)

---

## 2. 산출물

| 파일 | 설명 |
|------|------|
| `src/...` | |
| `tests/...` | |
| `.cursor/commands/...` | |
| `.cursor/skills/...` | |
| `tests/golden/....approved.txt` | *(해당 시)* |

---

## 3. TDD / 작업 기록

### STEP: RED

| 항목 | 내용 |
|------|------|
| Command | `/red-test-plan` · `/red-skeleton` · `/tdd-red` |
| Test ID | |
| 내용 | |
| pytest | `pytest ... -v` → **FAILED** — (실측 한 줄) |

### STEP: GREEN

| 항목 | 내용 |
|------|------|
| Command | `/green-minimal` |
| Test ID | |
| 내용 | `src/` 최소 구현 |
| pytest | `pytest ... -v` → **PASSED** — (실측) |

### STEP: Golden *(해당 시)*

| 항목 | 내용 |
|------|------|
| Command | `/golden-master` |
| Test ID | |
| golden | `tests/golden/{id}.approved.txt` |
| matched | yes / no (`UPDATE_GOLDEN` 없이) |

### STEP: REFACTOR *(해당 시)*

| 항목 | 내용 |
|------|------|
| Command | `/refactor-smell` · `/refactor-safe` |
| 스멜 | (유형 · 위치) |
| Budget | 파일 n · 메서드 n |
| pytest | `python -m pytest tests/ -v` → **PASSED** |
| golden | matched yes / no |

### STEP: repeat *(ARRR 1사이클 완료 보고 시)*

| 항목 | 내용 |
|------|------|
| Phase | `Phase: repeat` |
| 사이클 요약 | RED → GREEN → (Golden) → REFACTOR 완료 Test ID |
| 회귀 | `python -m pytest tests/ -v` → N passed |

### Phase 요약 표

| Phase | 내용 | pytest / 결과 |
|-------|------|----------------|
| RED | | FAILED — |
| GREEN | | PASSED — |
| Golden | | matched — |
| REFACTOR | | PASSED — |
| repeat | | (해당 시) |

**git status (세션 말미):** `(git status --short 출력 또는 해당 없음)`

---

## 4. 결정·규칙

- `.cursorrules` · API · SSOT 변경 (있을 때만)
- Command · Skill 추가 요약
- 10선 · incomplete · constants SSOT 한 줄씩

---

## 5. 다음 단계

- (다음 RED 묶음 · GREEN · `/refactor-smell` 등)

---

## 6. 관련 문서

| 문서 | 경로 |
|------|------|
| Transcript | `Prompting/NN.Export-Transcript.md` |
| 규칙 | `.cursorrules` |
| TDD Skill | `.cursor/skills/magic-square-tdd/SKILL.md` |
| Export Skill | `.cursor/skills/magic-square-docs/SKILL.md` |
| Export Command | `.cursor/commands/export-session.md` |
```

---

## Phase별 채움 규칙

| 세션 유형 | 채울 STEP |
|-----------|-----------|
| RED만 | RED |
| GREEN까지 | RED + GREEN |
| Golden 포함 | + Golden |
| REFACTOR 포함 | + REFACTOR |
| ARRR 1사이클 완료 | 위 전부 + **repeat** |

미진행 STEP은 표에서 `*(미진행)*` 또는 섹션 생략.
