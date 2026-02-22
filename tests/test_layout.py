from models.layout import LayoutColumn, Layout


def test_layout_all_keys():
    columns = [
        LayoutColumn(keys=2, offsetY=0),
        LayoutColumn(keys=1, offsetY=10),
    ]
    layout = Layout(columns=columns)

    keys = list(layout.all_keys())

    assert len(keys) == 3

    assert keys[0].col == 0
    assert keys[0].row == 0
    assert keys[0].offsetY == 0

    assert keys[1].col == 0
    assert keys[1].row == 1
    assert keys[1].offsetY == 0

    assert keys[2].col == 1
    assert keys[2].row == 0
    assert keys[2].offsetY == 10
