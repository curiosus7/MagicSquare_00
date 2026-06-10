from entity.blank_loc import blank_coords_row_major


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given — grid_g1: 0 두 칸, row-major
    grid = grid_g1

    # When
    coords = blank_coords_row_major(grid)

    # Then
    assert coords == [(1, 1), (3, 2)]
