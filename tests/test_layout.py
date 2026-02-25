import math
from models.layout import LayoutColumn, Layout
from models.projection import SphereProjection
from data.parameters import parameters


def assert_pos_equal(pos1, pos2):
    assert len(pos1) == len(pos2)
    for a, b in zip(pos1, pos2):
        assert math.isclose(a, b, abs_tol=1e-12)


def test_layout_grid():
    columns = [
        LayoutColumn(keys=2, offsetY=10),
        LayoutColumn(keys=1, offsetY=0),
    ]
    radius = 100.0
    projection = SphereProjection(radius)

    layout = Layout.from_spherical_projection(
        columns=columns, projection=projection, cap=parameters.caps
    )

    grid = list(layout.grid)

    assert len(grid) == 2

    # First column
    col0 = list(grid[0])
    assert len(col0) == 2

    # Key(0,0) - should be at initial position [0, 0, -radius] + [0, 0, radius] = [0, 0, 0]
    assert col0[0].col == 0
    assert col0[0].row == 0
    assert col0[0].offsetY == 10
    assert_pos_equal(col0[0].position, [0, 0, 0])
    assert_pos_equal(
        col0[0].rotation, projection.project_rotation([0, 0, -radius])
    )

    # Key(0,1) - should be moved by length (size + gap) in X
    length = parameters.caps.size + parameters.caps.gap
    raw_pos_0_1 = projection.move_constant_x([0, 0, -radius], length, 1)
    expected_pos_0_1 = [raw_pos_0_1[0], raw_pos_0_1[1], raw_pos_0_1[2] + radius]
    assert_pos_equal(col0[1].position, expected_pos_0_1)
    assert_pos_equal(col0[1].rotation, projection.project_rotation(raw_pos_0_1))

    # Second column
    col1 = list(grid[1])
    assert len(col1) == 1
    assert col1[0].col == 1
    assert col1[0].row == 0
    assert col1[0].offsetY == 0

    # Key(1,0) - started at move_constant_y([0,0,-radius], length)
    # Then move_constant_x by (0 - 10) * size
    initial_col_1 = projection.move_constant_y([0, 0, -radius], length, 1)
    raw_pos_1_0 = projection.move_constant_x(
        initial_col_1, (0 - 10) * parameters.caps.size, 1
    )
    expected_pos_1_0 = [raw_pos_1_0[0], raw_pos_1_0[1], raw_pos_1_0[2] + radius]
    assert_pos_equal(col1[0].position, expected_pos_1_0)
    assert_pos_equal(col1[0].rotation, projection.project_rotation(raw_pos_1_0))
