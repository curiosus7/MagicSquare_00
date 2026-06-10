from entity.constants import BLANK, GRID_SIZE


def blank_coords_row_major(grid: list[list[int]]) -> list[tuple[int, int]]:
    """격자에서 빈칸(BLANK) 좌표를 row-major 순으로 반환."""
    coords: list[tuple[int, int]] = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == BLANK:
                coords.append((r, c))
    return coords
