from dataclasses import dataclass
from injector import inject, singleton
from components.wire_holder.parameters import WireHolderParameters


@singleton
@inject
@dataclass
class WireHolderModel:
    parameters: WireHolderParameters

    @property
    def hole_radius(self) -> float:
        return self.parameters.hole_diameter / 2

    def length(self, wires: int) -> float:
        inner_length = (
            wires * self.parameters.pitch
        ) + self.parameters.clearance
        return inner_length + (self.parameters.wall_thickness * 2)

    @property
    def width(self) -> float:
        return self.parameters.hole_diameter + (
            self.parameters.wall_thickness * 2
        )

    @property
    def height(self) -> float:
        return self.parameters.height

    @property
    def hole_height(self) -> float:
        return self.height + self.parameters.clearance

    def hole_x_position(self, col: int, wires: int) -> float:
        return (col - (wires - 1) / 2) * self.parameters.pitch

    def housing_size(self, wires: int) -> tuple[float, float, float]:
        return (self.length(wires), self.width, self.height)
