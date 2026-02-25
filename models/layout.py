from dataclasses import dataclass
from typing import List, Protocol
from .projection import SphereProjection


@dataclass
class Key:
    col: int
    row: int
    position: List[float]
    rotation: List[float]
    offsetY: float = 0


@dataclass
class LayoutColumn:
    keys: int
    offsetY: float = 0


class CapSize(Protocol):
    size: float
    gap: float


@dataclass
class Layout:
    columns: List[LayoutColumn]
    grid: List[List[Key]]

    @classmethod
    def from_spherical_projection(
        cls,
        columns: List[LayoutColumn],
        projection: SphereProjection,
        cap: CapSize,
    ) -> "Layout":
        length = cap.size + cap.gap
        initial_column_position = [0, 0, -projection.radius]

        grid = []

        for col_index, column in enumerate(columns):
            keys_in_col = []
            position = initial_column_position

            for row_index in range(column.keys):
                if row_index == 0:
                    position = projection.move_constant_x(
                        position,
                        (column.offsetY - columns[0].offsetY) * cap.size,
                        direction=1,
                    )

                rotation = projection.project_rotation(position)

                key = Key(
                    col=col_index,
                    row=row_index,
                    position=[
                        position[0],
                        position[1],
                        position[2] + projection.radius,
                    ],
                    rotation=rotation,
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

        return cls(columns=columns, grid=grid)
