from entity.constants import BLANK, CELL_MAX, CELL_MIN


def solve_step_a(grid: list[list[int]]) -> tuple[bool, list[int]]:
    """Step A: 빈칸 2개·빠진 숫자 2개를 식별."""
    present = {cell for row in grid for cell in row if cell != BLANK}
    missing = sorted(
        n for n in range(CELL_MIN + 1, CELL_MAX + 1) if n not in present
    )
    blank_count = sum(1 for row in grid for cell in row if cell == BLANK)
    ok = blank_count == 2 and len(missing) == 2
    return ok, missing
