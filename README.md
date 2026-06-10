# MagicSquare_00

4×4 부분 마방진에서 빈칸을 채운 직후, **행·열·대각선 10선**이 합 **34**인지 빠짐없이 판정하고, 틀린 줄(특히 **대각선**)을 바로 알 수 있게 **검증 Rule · Command · Test Loop**를 만든다.

Mom Test 근거: *"빈칸 2개 넣고 행·열·대각선 합 맞췄는데 **대각선 하나를 빼먹어서 20분 날렸다.**"*

상세 요구사항: [docs/PRD.md](docs/PRD.md) v1.2 (SSOT)

---

## 도메인

| ID | 규칙 |
|----|------|
| DR-01 | 격자 4×4 |
| DR-02 | 셀 값 `0`(빈칸) 또는 `1~16` |
| DR-03 | 마법상수 `34` (`MAGIC_CONSTANT`) |
| DR-04 | 검증 10선 — R1~R4 · C1~C4 · D1(주↘) · D2(부↙), **누락 금지** |
| DR-05 | `0` 포함 → `incomplete`, 합 계산 생략 |
| DR-06 | 좌표 row-major, 0-index |

---

## 빠른 시작

**요구:** Python 3 · pytest

```bash
pytest
# 또는
python -m pytest tests/ -v
```

**현재:** `3 passed` — T-INC · D-LOC-01 · D-SOL-01

---

## API

### `validate_lines` (Command)

```python
from validate_lines import validate_lines

result = validate_lines([
    [0, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
])
# 현재: {"status": "incomplete", "failed_lines": []}
```

| `status` | 조건 | `failed_lines` |
|----------|------|----------------|
| `incomplete` | `0` 포함 — 합 계산 생략 | `[]` |
| `pass` | 0 없음, 10선 합 모두 34 | `[]` |
| `fail` | 0 없음, 하나 이상 ≠ 34 | 틀린 줄 목록 |

**목표 (FR-05):** `failed_lines: list[{id, sum}]` — 현재는 **줄 ID만** (`list[str]`)

### Entity

| 함수 | 모듈 | 용도 |
|------|------|------|
| `blank_coords_row_major(grid)` | `entity.blank_loc` | 빈칸 좌표 (D-LOC-01) |
| `solve_step_a(grid)` | `entity.solver` | Step A — 빈칸·빠진 숫자 (D-SOL-01) |

---

## Fixture

| Fixture | 설명 | 상태 |
|---------|------|------|
| `grid_g1` | 부분 격자 — 0 두 칸 `(1,1)`, `(3,2)` (Entity) | ✅ |
| `grid_complete` | 정답 완성 격자 (10선=34) — T-G1 | 🔲 예정 |
| `grid_g4` | D2만 sum=4 — Mom Test 대각 시나리오 (T-G4) | 🔲 예정 |

---

## 테스트 플랜 (PRD §8.2)

PRD [§8.2 Test ID · Golden ID](docs/PRD.md) 기준. 각 테스트는 **Arrange → Act → Assert** (AAA) 순서.

| Test ID | 테스트 함수 | Fixture | FR | 파일 | 상태 |
|---------|-------------|---------|-----|------|------|
| **T-G1** | `test_g1_all_lines_pass` | `grid_complete` | FR-02 | `tests/test_validate_lines.py` | 🔲 |
| **T-G4** | `test_g4_fails_with_wrong_anti_diagonal` | `grid_g4` | FR-04, FR-05, FR-06 | `tests/test_validate_lines.py` | 🔲 |
| **T-INC** | `test_incomplete_when_grid_has_zero` | 인라인 / `grid_incomplete` | FR-03 | `tests/test_validate_lines.py` | ✅ |
| **D-LOC-01** | `test_d_loc_01_blank_coords_row_major` | `grid_g1` | DR-06 | `tests/entity/test_d_loc_01.py` | ✅ |
| **D-SOL-01** | `test_d_sol_01_step_a_success` | `grid_g1` | FR-D-SOL-01 | `tests/entity/test_d_sol_01.py` | ✅ |

### T-G1 — `test_g1_all_lines_pass` 🔲

**FR-02:** 10선 **모두** 합이 34이면 `status: "pass"`, `failed_lines: []`

| 단계 | 내용 |
|------|------|
| **Given** | `grid_complete` fixture — 과제 정답 4×4 (0 없음, 10선=34) |
| **When** | `result = validate_lines(grid_complete)` |
| **Then** | `result["status"] == "pass"` |
| | `result["failed_lines"] == []` |

**Fixture `grid_complete`:**

```
[16,  3,  2, 13]
[ 5, 10, 11,  8]
[ 9,  6,  7, 12]
[ 4, 15, 14,  1]
```

**Golden:** GM-G1 — `pass`, `failed_lines: []`

**TDD:** RED → `conftest.py`에 `grid_complete` 추가 → assert 본문 → GREEN(10선 합·pass 판정)

---

### T-G4 — `test_g4_fails_with_wrong_anti_diagonal` 🔲

**FR-04:** 0 없고 하나 이상 합 ≠ 34 → `fail` · **FR-05:** `failed_lines`에 `id`·`sum` · **FR-06:** D1·D2 **모두** 검사

| 단계 | 내용 |
|------|------|
| **Given** | `grid_g4` — 행·열·D1=34, **D2(부대각)만 sum=4** (Mom Test 대각 시나리오) |
| **When** | `result = validate_lines(grid_g4)` |
| **Then** | `result["status"] == "fail"` |
| | `failed_lines`에 D2 포함, `sum == 4` |
| | R1~R4, C1~C4, D1은 `failed_lines`에 **없음** (D2만 틀림) |

**Fixture `grid_g4`:**

```
[ 1, 16, 16,  1]
[16,  1,  1, 16]
[16,  1, 16,  1]
[ 1, 16,  1, 16]
```

→ D2(부↙) 셀 `(0,3)+(1,2)+(2,1)+(3,0)` = **4** (≠34)

**Golden:** GM-G4 — `fail`, D2, `sum=4`

**TDD:** RED → `grid_g4` fixture → assert(D2·sum) → GREEN(D2 검사 + FR-05 TypedDict)

---

### T-INC — `test_incomplete_when_grid_has_zero` ✅

**FR-03:** 0(빈칸)이 **하나라도** 있으면 `status: "incomplete"`, `failed_lines: []` — **합 계산 생략**

| 단계 | 내용 |
|------|------|
| **Given** | 인라인 4×4 — `(0,0)`에 `0` 1개, 나머지 1~16 |
| **When** | `result = validate_lines(grid)` |
| **Then** | `result["status"] == "incomplete"` |
| | `result["failed_lines"] == []` |

**Golden:** GM-INC — `incomplete`, `failed_lines: []` (🔲 Golden 잠금 예정)

---

### D-LOC-01 — `test_d_loc_01_blank_coords_row_major` ✅

**DR-06:** 좌표 row-major, 0-index

| 단계 | 내용 |
|------|------|
| **Given** | `grid_g1` — 0 두 칸 `(1,1)`, `(3,2)` |
| **When** | `coords = blank_coords_row_major(grid_g1)` |
| **Then** | `coords == [(1, 1), (3, 2)]` |

**Fixture `grid_g1`:**

```
[ 1,  2,  3,  4]
[ 5,  0,  7,  8]
[ 9, 10, 11, 12]
[13, 14,  0, 16]
```

---

### D-SOL-01 — `test_d_sol_01_step_a_success` ✅

**FR-D-SOL-01:** `solve_step_a(grid_g1)` → `ok=True`, `missing=[6, 15]`

| 단계 | 내용 |
|------|------|
| **Given** | `grid_g1` |
| **When** | `ok, missing = solve_step_a(grid)` · `coords = blank_coords_row_major(grid)` |
| **Then** | `ok is True` |
| | `missing == [6, 15]` |
| | Golden **D-SOL-01**: `6 15 2 2 4 3` (missing 두 값 + 빈칸 좌표 1-index) |

---

### 실행 · 상수

```bash
python -m pytest tests/ -v
# 개별: pytest tests/test_validate_lines.py::test_g1_all_lines_pass -v
```

상수 **34 / 16 / 4** — `entity.constants` · `validate_lines` import 우선 (리터럴 남발 금지).

---

## 프로젝트 구조

```
MagicSquare_00/
├── docs/PRD.md              # 요구사항 SSOT (v1.2)
├── .cursorrules             # 도메인 · API · TDD
├── src/
│   ├── validate_lines.py    # Command · LINE_IDS SSOT
│   └── entity/
│       ├── constants.py
│       ├── blank_loc.py
│       ├── solver.py
│       └── validation.py
├── tests/
│   ├── conftest.py
│   ├── test_validate_lines.py
│   ├── entity/
│   ├── golden/
│   └── _approval.py
├── .cursor/commands/        # ARRR Commands
├── .cursor/skills/
├── Report/
└── Prompting/
```

---

## TDD (ARRR)

```
RED → GREEN → Golden → REFACTOR
```

| Phase | 규칙 |
|-------|------|
| RED | `tests/`만 · FAIL 확인 |
| GREEN | `src/` 최소 구현 |
| REFACTOR | GREEN 유지 · 구조 정리 |

Commands: `/red-test-plan` · `/red-skeleton` · `/tdd-red` · `/green-minimal` · `/golden-master` · `/refactor-smell` · `/refactor-safe` · `/export-session`

---

## 구현 현황

| Test ID | 내용 | 상태 |
|---------|------|------|
| T-INC | `0` 포함 → `incomplete` | ✅ |
| T-G1 | `grid_complete` → `pass` | 🔲 |
| T-G4 | `grid_g4` → `fail`, D2 (대각) | 🔲 |
| D-LOC-01 | 빈칸 좌표 row-major | ✅ |
| D-SOL-01 | Step A + Golden | ✅ |

| Golden | 기대 | 상태 |
|--------|------|------|
| GM-G1 | pass | 🔲 |
| GM-G4 | fail, D2 sum=4 | 🔲 |
| D-SOL-01 | `6 15 2 2 4 3` | ✅ |

**다음:** `grid_complete`/`grid_g4` fixture · T-G1/T-G4 RED · FR-05 (`failed_lines` sum)

---

## 수용 기준 (요약)

| # | 기준 | 상태 |
|---|------|------|
| AC-1 | `grid_complete` → pass | 🔲 |
| AC-2 | `grid_g4` → fail, D2 sum=4 | 🔲 |
| AC-3 | incomplete → `incomplete` | ✅ |
| AC-4 | pytest 전체 passed + Golden | △ 3 passed |
| AC-5 | Boundary에 합 계산 없음 | ✅ |
| AC-6 | Solver·UI·ECB 전체 미착수 | ✅ |

---

## 세션 문서

| NN | 주제 | Report | Transcript |
|----|------|--------|------------|
| 03 | Mom Test + 세션 3 워크북 | [03.REPORT.md](Report/03.REPORT.md) | [03.Export-Transcript.md](Prompting/03.Export-Transcript.md) |
| 04 | Harness · TDD RED | [04.REPORT.md](Report/04.REPORT.md) | [04.Export-Transcript.md](Prompting/04.Export-Transcript.md) |
| 05 | ARRR · entity TDD · Golden | [05.REPORT.md](Report/05.REPORT.md) | [05.Export-Transcript.md](Prompting/05.Export-Transcript.md) |
| 06 | PRD §8.2 테스트 플랜 · README | [06.REPORT.md](Report/06.REPORT.md) | [06.Export-Transcript.md](Prompting/06.Export-Transcript.md) |
| 07 | T-G1/T-G4 RED·GREEN · D-LOC-01 Golden · PR #3 | [07.REPORT.md](Report/07.REPORT.md) | [07.Export-Transcript.md](Prompting/07.Export-Transcript.md) |

---

## 관련 문서

| 문서 | 경로 |
|------|------|
| PRD v1.2 | [docs/PRD.md](docs/PRD.md) |
| Mom Test | [Report/STEP1_MomTest_인터뷰보고서.md](Report/STEP1_MomTest_인터뷰보고서.md) |
| TDD Skill | [.cursor/skills/magic-square-tdd/SKILL.md](.cursor/skills/magic-square-tdd/SKILL.md) |
| Docs Skill | [.cursor/skills/magic-square-docs/SKILL.md](.cursor/skills/magic-square-docs/SKILL.md) |

---

## 범위 밖

솔버 자동 채우기 · Grid UI · BCE 전체 · 1~16 중복·범위 검증 — [docs/PRD.md §3.2](docs/PRD.md)
