from entity.blank_loc import blank_coords_row_major
from entity.solver import solve_step_a
from tests._approval import assert_matches_golden

GOLDEN_ID = "D-SOL-01"


def _format_d_sol_01_golden(
    missing: list[int], coords: list[tuple[int, int]]
) -> str:
    """int[6] 1-index: missing 두 값 + 빈칸 좌표 (row-major)."""
    m1, m2 = missing[0], missing[1]
    (r1, c1), (r2, c2) = coords[0], coords[1]
    return f"{m1} {m2} {r1 + 1} {c1 + 1} {r2 + 1} {c2 + 1}"


def test_d_sol_01_step_a_success(grid_g1):
    # Given — grid_g1
    grid = grid_g1

    # When
    ok, missing = solve_step_a(grid)
    coords = blank_coords_row_major(grid)

    # Then — D-SOL-01 (Golden 잠금 완료)
    assert ok is True
    assert missing == [6, 15]
    assert_matches_golden(_format_d_sol_01_golden(missing, coords), GOLDEN_ID)
