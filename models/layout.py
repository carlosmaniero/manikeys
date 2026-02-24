from typing import Optional


class Key:
    def __init__(
        self, col: int, row: int, position: list[float], offsetY: float = 0
    ):
        self.col = col
        self.row = row
        self.offsetY = offsetY
        self.position: list[float] = position

    def __repr__(self):
        return f"Key(col={self.col}, row={self.row}, offsetY={self.offsetY}, position={self.position})"


class LayoutColumn:
    def __init__(self, keys: int, offsetY: float = 0):
        self.keys = keys
        self.offsetY = offsetY

    def __repr__(self):
        return f"LayoutColumn(keys={self.keys}, offsetY={self.offsetY})"


class Layout:
    def __init__(self, columns: list[LayoutColumn], projection, parameters):
        self.columns = columns
        self._grid = self._compute_grid(projection, parameters)

    def _compute_grid(self, projection, parameters):
        length = parameters.caps.size + parameters.caps.gap
        initial_column_position = [0, 0, -projection.radius]

        grid = []

        for col_index, column in enumerate(self.columns):
            keys_in_col = []
            position = initial_column_position

            for row_index in range(column.keys):
                if row_index == 0:
                    position = projection.move_constant_x(
                        position,
                        (column.offsetY - self.columns[0].offsetY)
                        * parameters.caps.size,
                        direction=1,
                    )

                key = Key(
                    col=col_index,
                    row=row_index,
                    position=position,
                    offsetY=column.offsetY,
                )

                keys_in_col.append(key)

                position = projection.move_constant_x(
                    position, length, direction=1
                )

            grid.append(keys_in_col)

            initial_column_position = projection.move_constant_y(
                initial_column_position, length, direction=1
            )

        return grid

    def grid(self):
        return self._grid

    def __repr__(self):
        return f"Layout(columns={self.columns})"
