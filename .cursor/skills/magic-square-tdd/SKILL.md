---
name: magic-square-tdd
description: >-
  MagicSquare_00 ARRR·Dual-Track TDD (RED/GREEN/REFACTOR, C2C, pytest.fail,
  Golden Master). Use when Phase is red|green|refactor; when running Commands
  /red-test-plan, /red-skeleton, /green-minimal, /refactor-safe; or when the
  user mentions TDD, RED, GREEN, REFACTOR, Dual-Track, C2C, or pytest.fail.
disable-model-invocation: true
---

# magic-square-tdd

MagicSquare_00 **4×4 부분 마방진** TDD Skill. Command 본문과 충돌 시 **Command 우선**, 도메인·API는 SSOT 우선.

## SSOT

| 문서 | 경로 | 용도 |
|------|------|------|
| 규칙·API | `.cursorrules` | 도메인 · `validate_lines` 계약 · TDD 순서 |
| 요구사항 | `docs/PRD.md` | FR·Test ID (없으면 `Report/*.REPORT.md`) |
| 상수(픽스처) | `src/entity/constants.py` | `GRID_SIZE` · `BLANK` · `MAGIC_CONSTANT` |
| 검증 SSOT | `src/validate_lines.py` | `LINE_IDS` · `LINE_CELLS` |
| Approval | `tests/_approval.py` · `tests/golden/*.approved.txt` | Golden Master |

---

## 1. ARRR ↔ TDD 매핑

| ARRR | TDD | 단계 | Command | 산출 |
|------|-----|------|---------|------|
| **A — Ask** | **RED** | ③ | `/red-test-plan` | C2C·테스트 플랜 (파일 없음) |
| **A — Ask** | **RED** | ④ | `/red-skeleton` | `pytest.fail` 스켈레톤 (`tests/`만) |
| **A — Ask** | **RED** | ⑤ | `/tdd-red` | `assert` · FAIL 확인 |
| **R — Respond** | **GREEN** | — | `/green-minimal` | `src/` 최소 구현 · PASS |
| **R — Respond** | **GREEN** | — | `/golden-master` | `*.approved.txt` · matched |
| **R — Refine** | **REFACTOR** | ⑦ | `/refactor-smell` | 스멜 표 (수정 없음) |
| **R — Refine** | **REFACTOR** | ⑧ | `/refactor-safe` | Budget 내 리팩터 · PASS · golden |

**순서:** RED → GREEN → Golden → REFACTOR. 건너뛰기 금지.

---

## 2. Phase 선언 (응답 첫 줄)

| Phase | 형식 |
|-------|------|
| RED | `Phase: red \| Layer: entity \| Track: Logic` |
| GREEN | `Phase: green \| Layer: entity \| Track: Logic` |
| Golden | `Phase: green \| Layer: entity \| Track: Logic` |
| REFACTOR smell | `Phase: refactor \| Scope: src/ tests/ \| Track: Logic+UI` |
| REFACTOR safe | `Phase: refactor \| Layer: entity \| Track: Logic` |

- **Layer:** `entity` (기본) · `boundary` (Track A)
- **Track:** `Logic` (기본) · `UI`
- 대소문자·`|` 구분자 **그대로**

---

## 3. C2C Rule 1~3 요약

PRD FR 1건당 설계 3행 (RED ③ `/red-test-plan`):

| Rule | 내용 |
|------|------|
| **Rule1** | PRD FR 인용 (`docs/PRD.md` 또는 `.cursorrules`·Report) |
| **Rule2** | To-Do **1개** — 이번 RED에서 검증할 행위 한 가지 |
| **Rule3** | Test ID + **Given / When / Then** (격자·호출·`status`·`failed_lines`) |

---

## 4. RED 절대 금지

| 금지 | RED 단계 |
|------|----------|
| **`src/` 수정** | ③④⑤ · GREEN 전까지 |
| **`@pytest.mark.skip` · `pytest.skip()` · `xfail`** | 모든 RED |
| **assert 완화 · 기대값 변경 · 조건 삭제** | Red→Green 속임 |
| **Logic Track Domain Mock** | `validate_lines` 등 mock/stub 금지 |
| **E001~E005 emit·assert** | Entity RED (Boundary 전용) |
| **리터럴 `34`·`16`·`4`·줄 ID** | `entity.constants` · `LINE_IDS` import |
| **통과 더미** (`pass`·빈 테스트) | ④ 스켈레톤 |
| **③에서 tests/·src/ 파일 생성** | 설계만 |

**④ Then:** `pytest.fail("RED: {Test ID} — …")` **한 줄만** (assert 본문 금지).

---

## 5. GREEN

| 규칙 | 내용 |
|------|------|
| **1커밋 = 1 RED 묶음** | 묶음 외 Test ID 선해결 금지 |
| **최소 구현** | 이번 묶음 PASS에 필요한 분기만 |
| **constants SSOT** | `34`·`16`·`4` → `entity/constants.py` 또는 `validate_lines` |
| **ECB** | Entity: boundary/control import 금지 · E001~E005 금지 |
| **tests/** | `pytest.fail`→`assert` 치환만 (이미 assert면 `src/`만) |
| **git commit** | 사용자 명시 요청 시만 |

---

## 6. REFACTOR

| 항목 | 규칙 |
|------|------|
| **전제** | `python -m pytest tests/ -v` 전부 PASS |
| **Change Budget** | 파일 ≤3 · 클래스 ≤1 · 메서드 ≤3 (1 smell = 1 `/refactor-safe`) |
| **불변** | 입출력 · 예외 · **int[6] 1-index** golden 포맷 |
| **golden** | `UPDATE_GOLDEN` 없이 matched; 수동 `.approved.txt` 편집 금지 |
| **금지** | 기능 추가 · 버그 수정 · assert 완화 |

**golden diff:** 비의도 → 롤백; 의도적(드묾) → ISS 문서 + `UPDATE_GOLDEN=1`.

---

## 7. Track A (UI) vs Track B (Logic)

| | **Track B — Logic** | **Track A — UI / Boundary** |
|---|---------------------|-------------------------------|
| **Layer** | `entity` | `boundary` (또는 `entity`+`Track: UI`) |
| **대상** | `validate_lines` · `blank_loc` · `solver` | 표시 · 입력 변환 · 에러 메시지 |
| **Mock** | Domain Mock **금지** | Boundary 입출력 격리 |
| **E001~E005** | emit **금지** | Boundary 시나리오에서만 |
| **golden** | int[6] 1-index (`2 2 4 3 0 0`) | `E001`~`E005` 문자열 (혼용 금지) |
| **Command** | 동일 체인 · `Layer`/`Track`만 치환 | `boundary`로 재사용 |

---

## 8. Command 체인

```
/red-test-plan
    → /red-skeleton
    → (/tdd-red)
    → /green-minimal
    → /golden-master
    → /refactor-smell
    → /refactor-safe
```

| Command | 파일 | 핵심 |
|---------|------|------|
| `red-test-plan` | `.cursor/commands/red-test-plan.md` | 4블록 표 · 파일 없음 |
| `red-skeleton` | `.cursor/commands/red-skeleton.md` | `pytest.fail` · `grid_g1` |
| `tdd-red` | `.cursor/commands/tdd-red.md` | AAA assert · FAIL |
| `green-minimal` | `.cursor/commands/green-minimal.md` | `src/` 최소 · PASS |
| `golden-master` | `.cursor/commands/golden-master.md` | `_approval.py` · golden |
| `refactor-smell` | `.cursor/commands/refactor-smell.md` | 스멜 표만 |
| `refactor-safe` | `.cursor/commands/refactor-safe.md` | smell 1건 · Budget |

완료 문구 예: `/red-skeleton 으로 넘길 준비됐다` (③).

---

## 9. pytest 명령 패턴

프로젝트 루트에서 실행 (`pyproject.toml` · `pythonpath = ["src"]`).

```bash
# RED — 단일
pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v

# RED/GREEN — 파일
pytest tests/test_validate_lines.py -v

# 전체 게이트 (REFACTOR·smell 전제)
python -m pytest tests/ -v

# Golden 기준 생성 (최초·ISS 후만)
UPDATE_GOLDEN=1 pytest tests/entity/test_d_sol_01.py::test_d_sol_01_step_a_success -v

# Golden matched (일상·완료)
python -m pytest tests/ -v
```

| 단계 | 기대 |
|------|------|
| RED ④ | FAILED — `pytest.fail: RED: …` |
| RED ⑤ | FAILED — `AssertionError` / 미구현 |
| GREEN | PASSED (묶음) |
| Golden | PASSED · golden 생성 후 matched |
| REFACTOR | PASSED · golden unchanged |

---

## 10. 완료 보고 형식

### RED ③ (`/red-test-plan`)

```
Phase: red | Layer: entity | Track: Logic
## 세션 주제 · 블록 1~4 (표)
/red-skeleton 으로 넘길 준비됐다
```

### RED ④ (`/red-skeleton`)

```
Phase: red | Layer: entity | Track: Logic
## Test ID · FAIL 한 줄 · 변경 파일 (tests/만)
```

### GREEN (`/green-minimal`)

```
Phase: green | Layer: entity | Track: Logic
## PASS Test ID · 변경 파일 · pytest · 회귀
```

### Golden (`/golden-master`)

```
Phase: green | Layer: entity | Track: Logic
## Test ID · golden 경로 · matched · diff 요약
```

### REFACTOR smell (`/refactor-smell`)

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
## pytest 게이트 · 스멜 표 · /refactor-safe 후보 1~3
P0 후보 중 1개를 골라 /refactor-safe 를 실행하세요.
```

### REFACTOR safe (`/refactor-safe`)

```
Phase: refactor | Layer: entity | Track: Logic
## 선택 스멜 · 변경 요약 · Change Budget · pytest · golden matched
```

---

## 도메인·API 요약

- **격자:** 4×4 · `0`=빈칸 · `1~16`
- **10선:** R1~R4 · C1~C4 · D1(↘) · D2(↙) — `LINE_IDS` 순서
- **`validate_lines(grid)`** → `{status: pass|fail|incomplete, failed_lines: [str]}`
- **incomplete 선행:** `0` 포함 → 합 계산 없음 · `failed_lines=[]`
- **응답 언어:** 한국어

---

## AAA · 픽스처

```python
# Given — grid; 상수는 SSOT import
# When  — result = validate_lines(grid)  (또는 entity 함수)
# Then  — assert 또는 pytest.fail (단계별)
```

| 픽스처 | 용도 |
|--------|------|
| `grid_g1` | 0 두 칸 · row-major (`tests/conftest.py`) |

---

## Golden int[6] (1-index)

```
{m1} {m2} {r1+1} {c1+1} {r2+1} {c2+1}   # 예: 6 15 2 2 4 3
```

Entity 성공: 상태 필드 `0`. Boundary: `E001`~`E005` 별도 포맷.

---

## 추가 리소스

- Command 상세: `.cursor/commands/*.md`
- 세션 맥락: `Report/*.REPORT.md`
