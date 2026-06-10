import pytest

from entity.blank_loc import blank_coords_row_major

GOLDEN_ID = "D-LOC-01"


def _format_d_loc_01_golden(coords: list[tuple[int, int]]) -> str:
    """int[6] 1-index: 두 빈칸 좌표 + status 0 + reserved 0. /golden-master 에서 잠금."""
    padded = coords + [(0, 0)] * (2 - len(coords))
    (r1, c1), (r2, c2) = padded[0], padded[1]
    return f"{r1 + 1} {c1 + 1} {r2 + 1} {c2 + 1} 0 0"


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given — grid_g1: 0 두 칸, row-major
    grid = grid_g1

    # When
    coords = blank_coords_row_major(grid)

    # Then — D-LOC-01
    assert coords == [(1, 1), (3, 2)]

    # Golden (D-LOC-01) — /golden-master 에서 assert_matches_golden 연결 예정
    # assert_matches_golden(_format_d_loc_01_golden(coords), GOLDEN_ID)


def test_d_loc_01_golden_master(grid_g1):
    # Given — grid_g1: 0 두 칸, row-major
    grid = grid_g1

    # When
    coords = blank_coords_row_major(grid)
    golden_text = _format_d_loc_01_golden(coords)

    # Then — D-LOC-01 Golden (FR-17)
    pytest.fail(f"RED: D-LOC-01 golden — assert_matches_golden matched int[6]: {golden_text}")
