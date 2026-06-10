# MagicSquare_00 — Product Requirements Document (PRD)

| 항목 | 내용 |
|------|------|
| **프로젝트** | `MagicSquare_00` |
| **버전** | 1.2 |
| **작성일** | 2026-06-10 |
| **단계** | **세션 3~5** — Rule · Command · Skill · Test Loop · Entity(부분) |
| **SSOT 연계** | `.cursorrules` · 본 문서 · `src/validate_lines.py` · `src/entity/constants.py` · `Report/03.REPORT.md` |

---

## 1. 개요

### 1.1 한 줄 주제

4×4 부분 마방진에서 빈칸을 채운 직후, **행·열·대각선 10선**이 합 **34**인지 빠짐없이 판정하고, 틀린 줄(특히 **대각선**)을 바로 알 수 있게 **검증 Rule · Command · Test Loop**를 만든다.

### 1.2 Mom Test 근거

| 항목 | 내용 |
|------|------|
| **페르소나** | 4×4 **부분** 마방진 학습자. 빈칸 2개(0), 1~16, **10선** 각 합 **34**. ECB·실패 조건 과제 병행 |
| **진짜 문제** | 빈칸 2개를 채운 뒤 **10선 합 판정을 전부 하지 못하고**, **대각선 하나를 빼먹어** 같은 시도를 반복하며 **20분** 같은 시간을 잃는다 |
| **핵심 증거** | *"빈칸 2개 넣고 행·열·대각선 합 맞췄는데 **대각선 하나를 빼먹어서 20분 날렸다.**"* |
| **Mom Test 판정** | **부분 검증** — 증거 ① 확보, 종료 시점(③)은 Test Loop로 보완 |

### 1.3 성공 기준 (Mom Test 연결)

| # | 성공 기준 | Mom Test |
|---|-----------|----------|
| **SC-1** | **10선 합 34 검증**을 한 Command로 끝낼 수 있다 (행 4 + 열 4 + **대각 2** — 대각 누락 불가) | 증거 ① |
| **SC-2** | 합 ≠ 34 격자에 Test Loop가 **Red → Green**으로 **같은 실패를 재현**하고, 정답 격자는 Green | 증거 ① (20분 → 1초) |
| **SC-3** | 실패 시 **어느 줄**이 34가 아닌지 Output에 명시 (행·열만 맞고 **대각 틀린** 경우 포함) | 증거 ②·③ 보완 |

---

## 2. R-G-I-O

| | 내용 |
|---|---|
| **R — Role** | 4×4 부분 마방진 학습자. 빈칸 2개를 채운 뒤 **맞았는지 스스로 확인**해야 함 |
| **G — Goal** | **10선**(행 4 + 열 4 + 대각 2) 전부 합 34인지 판정하고, 틀리면 **어느 줄**인지 즉시 알기 |
| **I — Input** | 4×4 `list[list[int]]`. 값: **0**(빈칸) 또는 **1~16** |
| **O — Output** | **통과/실패/미완** + 실패 시 **틀린 줄 목록**과 **해당 합**. 10선 전부 검사 보장 |

### 2.1 과제 예시 격자 (빈칸 2개)

| | | | |
|---|---|---|---|
| 16 | 3 | 2 | 13 |
| 5 | 10 | 11 | **?** |
| 9 | 6 | **?** | 12 |
| 4 | 15 | 14 | 1 |

정답 채움: (1,3)=8, (2,2)=7 → `grid_complete` fixture (§8.1).

---

## 3. 범위

### 3.1 In Scope (세션 3~5)

| 영역 | 내용 | 상태 |
|------|------|------|
| **Rule** | 10선 각 합 = 34. 0 포함 시 `incomplete` | ✅ |
| **Command** | `validate_lines(grid)` — 10선 합·비교·결과 조립 | △ |
| **Skill** | pytest, fixture, ARRR Cursor Commands | ✅ |
| **Test Loop** | RED → GREEN → Golden → REFACTOR | △ |
| **Harness** | `src/validate_lines.py`, `src/entity/`, `tests/` | ✅ |
| **Entity** | D-LOC-01(빈칸 좌표), D-SOL-01(Step A) | ✅ |

### 3.2 Out of Scope (표면 문제)

| 제외 | 이유 |
|------|------|
| `Solver` / 빈칸 **자동 채우기** / 힌트 | 학습자 고통은 **맞는지 확인** |
| `GridUI` / `InputHandler` / ECB 전체 앱 | UI·입력은 표면 솔루션 |
| Entity 클래스(`MagicSquare`/`Cell`) 전면 모델링 | 단계적 도입 |
| 1~16 중복·범위 검증 일괄 처리 | **합 34 · 10선**에 집중 |
| UI Track (`Layer: boundary`, `Track: UI`) | 후속 세션 |

---

## 4. 도메인 규칙

| ID | 규칙 | 값 / SSOT |
|----|------|-----------|
| **DR-01** | 격자 크기 | 4×4 (`GRID_SIZE`) |
| **DR-02** | 셀 값 | **0**(빈칸) 또는 **1~16** |
| **DR-03** | 마법상수 | **34** (`MAGIC_CONSTANT`) — 리터럴 `34` 산재 금지 |
| **DR-04** | 검사 대상 **10선** | R1~R4, C1~C4, D1(주대각), D2(부대각) — **누락 금지** |
| **DR-05** | 빈칸(0) 존재 | 10선 판정 불가 → `incomplete`, `failed_lines=[]` |
| **DR-06** | 좌표 | row-major `grid[row][col]`, 0-index |

### 4.1 10선 ID 정의

| ID | 정의 |
|----|------|
| R1~R4 | 第 i 행 (i = 0..3) |
| C1~C4 | 第 j 열 (j = 0..3) |
| D1 | 주대각 `(0,0)(1,1)(2,2)(3,3)` |
| D2 | 부대각 `(0,3)(1,2)(2,1)(3,0)` |

상수 SSOT: `LINE_IDS` · `LINE_CELLS` in `src/validate_lines.py`

### 4.2 status 판정

| status | 조건 | failed_lines |
|--------|------|--------------|
| `pass` | 0 없음, 10선 모두 합 34 | `[]` |
| `fail` | 0 없음, 하나 이상 ≠ 34 | ≠34인 줄 목록 |
| `incomplete` | 0 하나 이상 | `[]` (합 계산 생략) |

---

## 5. 기능 요구 (FR)

### 5.1 Command — `validate_lines`

| ID | 요구 | 우선순위 | 연결 | 상태 |
|----|------|----------|------|------|
| **FR-01** | 4×4 격자를 입력받아 **10선** 각각의 합을 계산한다 | P0 | SC-1, DR-04 | △ |
| **FR-02** | 10선 **모두** 합이 34이면 `status: "pass"`, `failed_lines: []` | P0 | SC-1 | 🔲 T-G1 |
| **FR-03** | 0(빈칸)이 **하나라도** 있으면 `status: "incomplete"`, `failed_lines: []` | P0 | DR-05 | ✅ T-INC |
| **FR-04** | 0 없고 **하나 이상** 합 ≠ 34이면 `status: "fail"` | P0 | SC-3 | 🔲 T-G4 |
| **FR-05** | `fail` 시 `failed_lines`에 **줄 ID**(`id`)와 **실제 합**(`sum`)을 포함 | P0 | SC-3 | 🔲 *현재 `list[str]`만* |
| **FR-06** | **D1·D2 모두** 검사 — 대각 1개만 검사하는 구현 **금지** | P0 | Mom Test ① | 🔲 T-G4 |
| **FR-07** | 단일 진입점 `validate_lines(grid)` — Boundary·UI는 Control 호출만 | P0 | ECB | ✅ |

### 5.2 Test Loop

| ID | 요구 | 우선순위 | 연결 | 상태 |
|----|------|----------|------|------|
| **FR-08** | RED: 실패 테스트가 **먼저** 존재 (`tests/`만 수정) | P0 | SC-2 | ✅ |
| **FR-09** | GREEN: RED 통과 **최소** 구현 (`src/`만) | P0 | SC-2 | △ |
| **FR-10** | REFACTOR: GREEN 유지, **동작 변경 없음** | P1 | — | ✅ (validation 추출) |
| **FR-11** | 실패 메시지에 **줄 ID**(예: D2)와 **기대/실제 합** 명시 | P0 | FR-05 | 🔲 |
| **FR-12** | assert 완화·skip·xfail·테스트 삭제로 GREEN **금지** | P0 | TDD | ✅ 규칙 |

### 5.3 Golden Master (회귀)

| ID | 요구 | 우선순위 | 상태 |
|----|------|----------|------|
| **FR-13** | `grid_complete` 정답 격자 → `pass` 고정 (GM-G1) | P0 | 🔲 |
| **FR-14** | `grid_g4` 대각 오류 → `fail` + D2, sum=4 고정 (GM-G4) | P0 | 🔲 |
| **FR-15** | incomplete 격자 → `incomplete` 고정 (GM-INC) | P0 | △ T-INC ✅ |
| **FR-16** | D-SOL-01 Golden int[6] 1-index: `6 15 2 2 4 3` | P1 | ✅ |
| **FR-17** | D-LOC-01 Golden | P1 | 🔲 |

### 5.4 Entity (세션 5~)

| ID | 요구 | 상태 |
|----|------|------|
| **FR-D-LOC-01** | `blank_coords_row_major(grid_g1)` → `[(1,1), (3,2)]` | ✅ |
| **FR-D-SOL-01** | `solve_step_a(grid_g1)` → `ok=True`, `missing=[6, 15]` | ✅ |

---

## 6. API 계약

### 6.1 시그니처 (목표)

```python
validate_lines(grid: list[list[int]]) -> ValidationResult
```

### 6.2 타입 (목표 — FR-05)

```python
class FailedLine(TypedDict):
    id: str   # R1~R4 | C1~C4 | D1 | D2
    sum: int  # 해당 줄 실제 합

class ValidationResult(TypedDict):
    status: Literal["pass", "fail", "incomplete"]
    failed_lines: list[FailedLine]
```

### 6.3 현재 구현 (세션 5)

```python
# src/validate_lines.py → entity.validation.validate_grid_lines
validate_lines(grid) -> dict
# {
#   "status": "pass" | "fail" | "incomplete",
#   "failed_lines": list[str]   # fail 시 줄 ID만 (sum 미포함 — FR-05 갭)
# }
```

**예외:** `grid`가 4×4가 아니면 `ValueError("grid must be 4x4")`

### 6.4 Entity API

| 함수 | 모듈 | 반환 |
|------|------|------|
| `blank_coords_row_major(grid)` | `entity.blank_loc` | `list[tuple[int,int]]` |
| `solve_step_a(grid)` | `entity.solver` | `(ok: bool, missing: list[int])` |
| `validate_grid_lines(...)` | `entity.validation` | 내부 10선 검증 |

### 6.5 구현 상태

| 파일 | 상태 |
|------|------|
| `src/validate_lines.py` | `LINE_IDS` · `LINE_CELLS` SSOT · Command 진입점 |
| `src/entity/constants.py` | `GRID_SIZE` · `BLANK` · `MAGIC_CONSTANT` |
| `src/entity/validation.py` | `_line_sum` · `_failed_line_ids` · incomplete/pass/fail |
| `src/entity/blank_loc.py` | D-LOC-01 ✅ |
| `src/entity/solver.py` | D-SOL-01 ✅ |
| `tests/test_validate_lines.py` | T-INC ✅ · T-G1/T-G4 🔲 |

---

## 7. ECB (8계층)

| 계층 | 역할 | 위치 | 세션 3~5 |
|------|------|------|----------|
| **Entity** | 상수, 빈칸·솔버, 검증 로직 | `src/entity/` | ✅ |
| **Rule** | 10선=34, 0→incomplete | PRD · `.cursorrules` | ✅ |
| **Control** | `validate_lines` | `src/validate_lines.py` | ✅ |
| **Command** | 단일 진입점 | Control | ✅ |
| **Boundary** | pytest Act/Assert | `tests/` | ✅ |
| **Skill** | pytest, fixture, ARRR Commands | `tests/conftest.py` · `.cursor/` | ✅ |
| **Test Loop** | RED→GREEN→Golden→REFACTOR | `tests/` + `src/` | △ |
| **Solver/UI** | — | — | ❌ 후속 |

### 7.1 ECB Emit 코드 (Logic Track 금지)

| 코드 | 의미 | Logic Track |
|------|------|-------------|
| E001 | GridUI render / 화면 갱신 | emit 금지 |
| E002 | InputHandler / 셀 입력 | emit 금지 |
| E003 | Solver / 자동 채우기 | emit 금지 |
| E004 | ECB 다이어그램·메타 산출 | emit 금지 |
| E005 | 파일 I/O·외부 API | emit 금지 |

### 7.2 Mock 규칙

| Track | Layer | Domain Mock | 비고 |
|-------|-------|-------------|------|
| Logic | entity | **금지** | fixture/인라인 격자 사용 |
| Logic | boundary | **금지** | Control 호출만 |
| UI | boundary | *(후속)* | — |

Boundary 테스트에 **합 계산·10선 나열 로직**을 넣지 않는다 (Control 침범).

---

## 8. 테스트 요구

### 8.1 Fixture (`tests/conftest.py`)

| Fixture | 설명 | 기대 | 상태 |
|---------|------|------|------|
| `grid_g1` | **부분** 격자 — 0 두 칸 `(1,1)`, `(3,2)` (Entity용) | D-LOC/D-SOL | ✅ |
| `grid_complete` | 과제 **정답** 격자 (10선 합 34) | `pass` | 🔲 추가 예정 |
| `grid_g4` | 행·열·D1=34, **D2만 sum=4** (Mom Test 대각) | `fail`, D2 | 🔲 추가 예정 |
| `grid_incomplete` | 0 포함 | `incomplete` | △ 인라인 사용 |

**`grid_complete` (T-G1 / GM-G1):**

```
[16,  3,  2, 13]
[ 5, 10, 11,  8]
[ 9,  6,  7, 12]
[ 4, 15, 14,  1]
```

**`grid_g4` (T-G4 / GM-G4 — Mom Test 대각 시나리오):**

```
[ 1, 16, 16,  1]
[16,  1,  1, 16]
[16,  1, 16,  1]
[ 1, 16,  1, 16]
```

→ D2(부대각) 합 = **4** (≠34).

**`grid_g1` (Entity — 부분 격자):**

```
[ 1,  2,  3,  4]
[ 5,  0,  7,  8]
[ 9, 10, 11, 12]
[13, 14,  0, 16]
```

### 8.2 Test ID · Golden ID

| Test ID | 테스트 함수 | Fixture | FR | 상태 |
|---------|-------------|---------|-----|------|
| **T-G1** | `test_g1_all_lines_pass` | `grid_complete` | FR-02 | 🔲 |
| **T-G4** | `test_g4_fails_with_wrong_anti_diagonal` | `grid_g4` | FR-04, FR-05, FR-06 | 🔲 |
| **T-INC** | `test_incomplete_when_grid_has_zero` | 인라인 / `grid_incomplete` | FR-03 | ✅ |
| **D-LOC-01** | `test_d_loc_01_blank_coords_row_major` | `grid_g1` | DR-06 | ✅ |
| **D-SOL-01** | `test_d_sol_01_step_a_success` | `grid_g1` | FR-D-SOL-01 | ✅ |

| Golden ID | Fixture | Expected | 상태 |
|-----------|---------|----------|------|
| GM-G1 | `grid_complete` | pass, `failed_lines: []` | 🔲 |
| GM-G4 | `grid_g4` | fail, D2, sum=4 | 🔲 |
| GM-INC | incomplete | incomplete, `failed_lines: []` | 🔲 |
| D-SOL-01 | `grid_g1` | `6 15 2 2 4 3` | ✅ |

### 8.3 AAA · pytest

- **Arrange** → fixture / 4×4 격자
- **Act** → `result = validate_lines(grid)`
- **Assert** → `status`, `failed_lines` 구체 값

```bash
python -m pytest tests/ -v
```

상수 **34 / 16 / 4** — `entity.constants` · `validate_lines` import 우선 (리터럴 남발 금지).

---

## 9. ARRR · TDD 워크플로

### 9.1 Phase 선언

| Phase | 선언 예 |
|-------|---------|
| RED 설계 | `Phase: red \| Layer: entity \| Track: Logic` |
| RED assert | `Phase: RED` |
| GREEN | `Phase: green \| Layer: entity \| Track: Logic` |
| Golden | `Phase: green \| Layer: entity \| Track: Logic` |
| REFACTOR | `Phase: refactor \| Layer: entity \| Track: Logic` |

### 9.2 Command 파이프라인

```
/red-test-plan → /red-skeleton → /tdd-red → /green-minimal
  → /golden-master → /refactor-smell → /refactor-safe → /export-session
```

| Command | ARRR | 산출 |
|---------|------|------|
| `/red-test-plan` | Ask ③ | C2C·Track B·테스트 플랜 |
| `/red-skeleton` | Ask ④ | `pytest.fail` 스켈레톤 |
| `/tdd-red` | RED | assert 본문 |
| `/green-minimal` | Review ① | `src/` 최소 구현 |
| `/golden-master` | Review ② | GM 잠금 |
| `/refactor-smell` | Refactor ① | Smell 표 |
| `/refactor-safe` | Refactor ② | safe refactor |
| `/export-session` | Release | Report + Transcript |

### 9.3 TDD 규칙

1. **RED → GREEN → REFACTOR** 고정. 한 사이클·한 관심사.
2. RED: `tests/`만. GREEN: `src/`만. REFACTOR: GREEN 유지.
3. 금지: assert 완화, skip, xfail, 테스트 삭제로 GREEN.

### 9.4 C2C Rule (RED ③)

| Rule | 내용 |
|------|------|
| **Rule1** | PRD FR 문장 인용 |
| **Rule2** | To-Do 1개 |
| **Rule3** | Test ID + Given / When / Then |

### 9.5 Refactor Smell ID

| ID | 이름 |
|----|------|
| S01 | Duplicated 10-line sum |
| S02 | Magic number |
| S03 | Long method |
| S04 | Boundary logic leak |
| S05 | Dead stub |
| S06 | Misplaced constant |
| S07 | failed_lines order |

---

## 10. 프로젝트 구조

```
MagicSquare_00/
├── docs/
│   └── PRD.md                 # 본 문서 (SSOT)
├── src/
│   ├── validate_lines.py      # Control/Command · LINE_IDS SSOT
│   └── entity/
│       ├── constants.py
│       ├── blank_loc.py
│       ├── solver.py
│       └── validation.py
├── tests/
│   ├── conftest.py            # Skill — fixture
│   ├── test_validate_lines.py # Boundary
│   ├── entity/
│   ├── golden/
│   └── _approval.py
├── pyproject.toml
├── .cursorrules
├── .cursor/commands/          # ARRR Commands
├── .cursor/skills/
├── Report/
└── Prompting/
```

---

## 11. 수용 기준 (Acceptance)

세션 **완료** 조건:

| # | 기준 | 검증 | 상태 |
|---|------|------|------|
| **AC-1** | `validate_lines(grid_complete)["status"] == "pass"` | T-G1 / GM-G1 | 🔲 |
| **AC-2** | G4 → fail, `"D2" in failed_ids`, D2 sum == 4 | T-G4 / GM-G4 | 🔲 |
| **AC-3** | incomplete 격자 → `status == "incomplete"` | T-INC / GM-INC | ✅ |
| **AC-4** | pytest 전체 **passed** (Golden Master) | `/golden-master` | △ 3 passed |
| **AC-5** | Boundary에 합 계산 로직 없음 | 코드 리뷰 / FR-07 | ✅ |
| **AC-6** | Solver·GridUI·ECB 전체 미착수 | 범위 §3.2 | ✅ |

---

## 12. 구현 현황 (세션 5)

| 구분 | 내용 |
|------|------|
| **pytest** | `python -m pytest tests/ -v` → **3 passed** |
| **완료** | T-INC · D-LOC-01 · D-SOL-01 + Golden |
| **REFACTOR** | `validation.py` — S01 (`_line_sum`, `_failed_line_ids`) |
| **갭** | FR-05 (`failed_lines` sum) · T-G1 · T-G4 · fixture `grid_complete`/`grid_g4` |

---

## 13. 로드맵

### 13.1 단기

1. `grid_complete` · `grid_g4` fixture 추가
2. **T-G1 · T-G4 RED** → GREEN → GM-G1 · GM-G4
3. **FR-05** — `FailedLine` TypedDict 반영
4. D-LOC-01 Golden

### 13.2 중기

- 1~16 중복·범위 검증
- Entity Step B 솔버 확장

### 13.3 장기

- Boundary · Control · Grid UI · BCE 전체

---

## 14. 참조 문서

| 문서 | 용도 |
|------|------|
| [Report/STEP1_MomTest_인터뷰보고서.md](../Report/STEP1_MomTest_인터뷰보고서.md) | Mom Test 원본 |
| [Report/03.REPORT.md](../Report/03.REPORT.md) | 세션 3 워크북 · R-G-I-O |
| [Report/04.REPORT.md](../Report/04.REPORT.md) · [05.REPORT.md](../Report/05.REPORT.md) | Harness · ARRR |
| `.cursorrules` | AI·TDD·도메인 |
| `.cursor/skills/magic-square-tdd/SKILL.md` | Test ID·ARRR |
| [MagicSquare_xx PRD](https://github.com/kznetwork/MagicSquare_xx/blob/main/docs/PRD.md) | 참고 구조 |

---

## 15. 변경 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-06-10 | 초안 — Mom Test · R-G-I-O · FR·Test ID · 세션 5 현황 |
| 1.1 | 2026-06-10 | MagicSquare_1004 PRD 구조 반영 |
| 1.2 | 2026-06-10 | MagicSquare_xx PRD 반영 — FR-01~17 · ECB · fixture · GM · AC · 구현 갭 명시 |

---

*MagicSquare_00 — docs/PRD.md v1.2 — SSOT for FR-* · ECB · Test Loop*
