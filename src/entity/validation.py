from entity.constants import BLANK


def _line_sum(grid: list[list[int]], cells: list[tuple[int, int]]) -> int:
    return sum(grid[r][c] for r, c in cells)


def _failed_lines(
    grid: list[list[int]], line_ids: tuple[str, ...], line_cells: dict[str, list[tuple[int, int]]], magic_constant: int
) -> list[dict[str, int | str]]:
    failed: list[dict[str, int | str]] = []
    for line_id in line_ids:
        line_sum = _line_sum(grid, line_cells[line_id])
        if line_sum != magic_constant:
            failed.append({"id": line_id, "sum": line_sum})
    return failed


def validate_grid_lines(
    grid: list[list[int]],
    line_ids: tuple[str, ...],
    line_cells: dict[str, list[tuple[int, int]]],
    magic_constant: int,
) -> dict:
    for row in grid:
        for cell in row:
            if cell == BLANK:
                return {"status": "incomplete", "failed_lines": []}

    failed = _failed_lines(grid, line_ids, line_cells, magic_constant)
    if failed:
        return {"status": "fail", "failed_lines": failed}
    return {"status": "pass", "failed_lines": []}
