from validate_lines import GRID_SIZE, LINE_CELLS, LINE_IDS, MAGIC_CONSTANT, validate_lines
from tests._approval import assert_matches_golden


def _format_validation_golden(result: dict) -> str:
    """Boundary Golden 직렬화 (GM-G1 / GM-G4 / GM-INC). /golden-master 에서 잠금."""
    status = result["status"]
    if status in ("pass", "incomplete"):
        return status
    parts = [status]
    for line in result["failed_lines"]:
        if isinstance(line, dict):
            parts.append(f"{line['id']} {line['sum']}")
        else:
            parts.append(str(line))
    return " ".join(parts)


def test_g1_all_lines_pass(grid_complete):
    # Given — grid_complete: 과제 정답 4×4 (0 없음, 10선=34)
    grid = grid_complete

    # Act
    result = validate_lines(grid)

    # Assert — T-G1: 10선 모두 MAGIC_CONSTANT
    assert result["status"] == "pass"
    assert result["failed_lines"] == []
    assert_matches_golden(_format_validation_golden(result), "GM-G1")


def test_g4_fails_with_wrong_anti_diagonal(grid_g4):
    # Given — grid_g4: 행·열·D1=MAGIC_CONSTANT, D2(부대각)만 sum=4 (PRD §8.1)
    grid = grid_g4
    d2 = LINE_IDS[-1]
    d2_wrong_sum = 4

    # Act
    result = validate_lines(grid)

    # Assert — T-G4: D2만 틀림, failed_lines에 id·sum (FR-05)
    assert result["status"] == "fail"
    assert result["failed_lines"] == [{"id": d2, "sum": d2_wrong_sum}]
    assert_matches_golden(_format_validation_golden(result), "GM-G4")


def test_incomplete_when_grid_has_zero(grid_incomplete):
    # Given — 0(빈칸) 1개 포함
    grid = grid_incomplete

    # When
    result = validate_lines(grid)

    # Assert — T-INC: incomplete, failed_lines=[]
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []

    assert_matches_golden(_format_validation_golden(result), "GM-INC")
