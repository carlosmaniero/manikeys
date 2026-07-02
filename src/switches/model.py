from models.parameters import SwitchesParameters
from dataclasses import dataclass
from typing import List, Protocol
from models.projection import SphereProjection
from dataclasses import field


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


class SwitchDimensions(Protocol):
    size: float
    gap: float


@dataclass
class LayoutBounds:
    left: list[float] = field(default_factory=lambda: [float("inf"), 0, 0])
    right: list[float] = field(default_factory=lambda: [float("-inf"), 0, 0])
    top: list[float] = field(default_factory=lambda: [0, float("inf"), 0])
    bottom: list[float] = field(default_factory=lambda: [0, float("-inf"), 0])
    highest: list[float] = field(default_factory=lambda: [0, 0, float("-inf")])
    lowest: list[float] = field(default_factory=lambda: [0, 0, float("inf")])

    def update(self, position: List[float]):
        if position[0] < self.left[0]:
            self.left = position

        if position[0] > self.right[0]:
            self.right = position

        if position[1] > self.bottom[1]:
            self.bottom = position

        if position[1] < self.top[1]:
            self.top = position

        if position[2] > self.highest[2]:
            self.highest = position

        if position[2] < self.lowest[2]:
            self.lowest = position

    def width(self) -> float:
        return self.right[0] - self.left[0]

    def depth(self) -> float:
        return self.bottom[1] - self.top[1]


@dataclass
class Layout:
    columns: List[LayoutColumn]
    grid: List[List[Key]]
    bounds: LayoutBounds

    @classmethod
    def from_spherical_projection(
        cls,
        columns: List[LayoutColumn],
        projection: SphereProjection,
        switch: SwitchDimensions,
    ) -> "Layout":
        length = switch.size + switch.gap
        initial_column_position = [0, 0, -projection.radius]

        grid = []
        bounds = LayoutBounds()

        for col_index, column in enumerate(columns):
            keys_in_col = []
            position = initial_column_position

            for row_index in range(column.keys):
                if row_index == 0:
                    position = projection.move_constant_x(
                        position,
                        (column.offsetY - columns[0].offsetY) * switch.size,
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

                bounds.update(key.position)

                keys_in_col.append(key)

                position = projection.move_constant_x(
                    position, length, direction=1
                )

            grid.append(keys_in_col)

            initial_column_position = projection.move_constant_y(
                initial_column_position, length, direction=1
            )

        return cls(columns=columns, grid=grid, bounds=bounds)

    def get_main_cluster_corners(
        self, switches_parameters: SwitchesParameters
    ) -> List[List[float]]:
        top_left = [
            self.bounds.left[0]
            - switches_parameters.size
            - switches_parameters.gap,
            self.bounds.top[1]
            - switches_parameters.size
            - switches_parameters.gap,
        ]
        top_right = [
            self.bounds.right[0]
            + switches_parameters.size
            + switches_parameters.gap,
            self.bounds.top[1]
            - switches_parameters.size
            - switches_parameters.gap,
        ]
        bottom_left = [
            self.bounds.left[0]
            - switches_parameters.size
            - switches_parameters.gap,
            self.bounds.bottom[1]
            + switches_parameters.size
            + switches_parameters.gap,
        ]
        bottom_right = [
            self.bounds.right[0]
            + switches_parameters.size
            + switches_parameters.gap,
            self.bounds.bottom[1]
            + switches_parameters.size
            + switches_parameters.gap,
        ]

        top_first_key = list(self.grid[0][0].position)
        top_first_key[0] = top_left[0]
        top_first_key[1] -= switches_parameters.size + switches_parameters.gap

        top_third_key = list(self.grid[3][0].position)
        top_third_key[0] -= switches_parameters.size + switches_parameters.gap
        top_third_key[1] = top_left[1]

        return [
            top_third_key,
            top_first_key,
            bottom_left,
            bottom_right,
            top_right,
        ]
