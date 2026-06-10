GRID_SIZE = 4

MAGIC_CONSTANT = 34

LINE_IDS = (
    "R1",
    "R2",
    "R3",
    "R4",
    "C1",
    "C2",
    "C3",
    "C4",
    "D1",
    "D2",
)

# 10선 = 행4 + 열4 + 대각2. 셀은 (row, col) 0-based.
LINE_CELLS: dict[str, list[tuple[int, int]]] = {
    "R1": [(0, c) for c in range(GRID_SIZE)],
    "R2": [(1, c) for c in range(GRID_SIZE)],
    "R3": [(2, c) for c in range(GRID_SIZE)],
    "R4": [(3, c) for c in range(GRID_SIZE)],
    "C1": [(r, 0) for r in range(GRID_SIZE)],
    "C2": [(r, 1) for r in range(GRID_SIZE)],
    "C3": [(r, 2) for r in range(GRID_SIZE)],
    "C4": [(r, 3) for r in range(GRID_SIZE)],
    "D1": [(i, i) for i in range(GRID_SIZE)],  # 주대각 ↘
    "D2": [(i, GRID_SIZE - 1 - i) for i in range(GRID_SIZE)],  # 부대각 ↙
}


def validate_lines(grid: list[list[int]]) -> dict:
    """10선×MAGIC_CONSTANT 검증.

    선행: 0 포함 → incomplete (합 계산 없음).
    failed_lines: fail 시 LINE_IDS 순서, 각 항목 {id, sum}.

    Args:
        grid: 4×4 list[list[int]], 값 0~16.

    Returns:
        {"status": "pass"|"fail"|"incomplete", "failed_lines": list[dict]}

    Raises:
        ValueError: grid가 4×4가 아닐 때.
    """
    if len(grid) != GRID_SIZE or any(len(row) != GRID_SIZE for row in grid):
        raise ValueError("grid must be 4x4")

    from entity.validation import validate_grid_lines

    return validate_grid_lines(grid, LINE_IDS, LINE_CELLS, MAGIC_CONSTANT)
