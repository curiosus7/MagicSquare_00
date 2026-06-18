from validate_lines import GRID_SIZE, LINE_CELLS, LINE_IDS, MAGIC_CONSTANT, validate_lines


def test_incomplete_when_grid_has_zero():
    # Arrange — 0(빈칸) 1개 포함
    grid = [
        [0, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]

    # Act
    result = validate_lines(grid)

    # Assert — 선행: incomplete, failed_lines=[]
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []
