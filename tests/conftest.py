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
