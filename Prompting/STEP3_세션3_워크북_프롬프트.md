# STEP 3 — 세션 3 워크북 프롬프트

## 사용법

STEP 1 Mom Test가 완료된 뒤, 아래 프롬프트를 보낸다.  
Mom Test 결과를 바탕으로 **세션 3 워크북**(R-G-I-O · 성공 기준 · 8계층 범위)이 채워진다.

**선행 조건:** `Report/STEP1_MomTest_인터뷰보고서.md` 또는 동등한 Mom Test 정리본

---

## 프롬프트 (복사용)

```
Mom Test 결과:
- 페르소나: [4×4 부분 마방진 학습자 — 수업 실습 + ECB·실패 조건 병행]
- 진짜 문제 (한 문장): [검증 항목 누락 → 20분 낭비]
- Mom Test 증거 3줄: [빈칸 2개 / 대각선 빼먹음 / 20분]

MagicSquare_00 세션 3 워크북을 채워줘:
1) 주제 한 문장 (Mom Test 기반, 솔루션 최소화)
2) R-G-I-O (Role/Goal/Input/Output)
3) 성공 기준 3개 (Mom Test 증거와 연결)
4) 표면 문제 — 이번 프로젝트에서 하지 않을 것
8계층 중 이번 세션에서 만드는 것만: Rule, Command, (Skill), Test Loop
```

---

## 출력 항목

| # | 항목 | 기준 |
|---|------|------|
| 1 | **주제 (1문장)** | 솔루션 단어(앱·솔버·UI) 없음. **판정·확인 비용** 중심 |
| 2 | **R-G-I-O** | Role=학습자, Goal=10선×34 즉시 판정, Input=4×4 grid, Output=validate_lines 결과 |
| 3 | **성공 기준 3개** | 각각 Mom Test 증거 3줄과 1:1 연결 |
| 4 | **표면 문제 (하지 않을 것)** | 솔버·ECB 도구·UI·BCE 전체 등 배제 목록 |
| 5 | **8계층 (세션 3만)** | Rule · Command · (Skill) · Test Loop — Entity/Boundary/Solver는 후속 |

---

## 세션 3 핵심 Command

```
validate_lines(grid) → ValidationResult
  - ok: bool
  - status: "pass" | "fail" | "incomplete"
  - lines[]: fail 시 { id, sum, expected: 34 }
```

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [Report/03.REPORT.md](../Report/03.REPORT.md) | 세션 3 워크북 보고서 (전체) |
| [Report/STEP1_MomTest_인터뷰보고서.md](../Report/STEP1_MomTest_인터뷰보고서.md) | Mom Test 원본 |
| [STEP3_보고서_보내기.md](./STEP3_보고서_보내기.md) | 보고서 저장 요청 |

---

*MagicSquare_00 — STEP 3*
