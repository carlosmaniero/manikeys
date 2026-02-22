class Key:
    def __init__(self, col: int, row: int, offsetY: int = 0):
        self.col = col
        self.row = row
        self.offsetY = offsetY

    def __repr__(self):
        return f"Key(col={self.col}, row={self.row}, offsetY={self.offsetY})"


class LayoutColumn:
    def __init__(self, keys: int, offsetY: int = 0):
        self.keys = keys
        self.offsetY = offsetY

    def __repr__(self):
        return f"LayoutColumn(keys={self.keys}, offsetY={self.offsetY})"


class Layout:
    def __init__(self, columns: list[LayoutColumn]):
        self.columns = columns

    def all_keys(self) -> list[Key]:
        for col_index, column in enumerate(self.columns):
            for row_index in range(column.keys):
                yield Key(col=col_index, row=row_index, offsetY=column.offsetY)

    def __repr__(self):
        return f"Layout(columns={self.columns})"
