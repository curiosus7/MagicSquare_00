import pytest


@pytest.fixture
def grid_g1():
    """4×4, 0 두 칸, row-major 1~16 (빈칸: (1,1), (3,2))."""
    return [
        [1, 2, 3, 4],
        [5, 0, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 0, 16],
    ]


@pytest.fixture
def grid_complete():
    """과제 정답 격자 — 0 없음, 10선 합 34 (T-G1 / GM-G1)."""
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]


@pytest.fixture
def grid_g4():
    """Mom Test 대각 — 행·열·D1=34, D2만 sum=4 (T-G4 / GM-G4)."""
    return [
        [1, 16, 16, 1],
        [16, 1, 1, 16],
        [16, 1, 16, 1],
        [1, 16, 1, 16],
    ]


@pytest.fixture
def grid_incomplete():
    """0 포함 — incomplete (T-INC / GM-INC)."""
    return [
        [0, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]
