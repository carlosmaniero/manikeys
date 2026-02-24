from models.layout import LayoutColumn, Layout


def test_layout_grid():
    columns = [
        LayoutColumn(keys=2, offsetY=10),
        LayoutColumn(keys=1, offsetY=0),
    ]
    layout = Layout(columns=columns)

    grid = list(layout.grid())

    assert len(grid) == 2

    # First column
    col0 = list(grid[0])
    assert len(col0) == 2
    assert col0[0].col == 0
    assert col0[0].row == 0
    assert col0[0].offsetY == 10
    assert col0[1].col == 0
    assert col0[1].row == 1
    assert col0[1].offsetY == 10

    # Second column
    col1 = list(grid[1])
    assert len(col1) == 1
    assert col1[0].col == 1
    assert col1[0].row == 0
    assert col1[0].offsetY == 0
