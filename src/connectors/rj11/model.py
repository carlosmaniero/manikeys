from connectors.rj11.parameters import RJ11Parameters
from dataclasses import dataclass
from injector import inject, singleton


@singleton
@inject
@dataclass
class RJ11Model:
    rj11_parameters: RJ11Parameters

    @property
    def rj11(self) -> RJ11Parameters:
        return self.rj11_parameters

    @property
    def notch_start_y(self) -> float:
        return (
            self.rj11.length / 2
            - self.rj11.bottom_notch_start_y
            - self.rj11.bottom_notch_length / 2
        )

    @property
    def inner_width(self) -> float:
        return (
            self.rj11.width
            - self.rj11.inner_paddings[1]
            - self.rj11.inner_paddings[3]
        )

    @property
    def inner_height(self) -> float:
        return (
            self.rj11.height
            - self.rj11.inner_paddings[0]
            - self.rj11.inner_paddings[2]
        )

    @property
    def top_pocket_width(self) -> float:
        return self.rj11.width - 3.25 * 2

    @property
    def top_pocket_height(self) -> float:
        return self.rj11.height - 1

    @property
    def top_pocket_length(self) -> float:
        return 3

    @property
    def bottom_pocket_width(self) -> float:
        return self.rj11.width - 4 * 2

    @property
    def bottom_pocket_height(self) -> float:
        return self.rj11.height

    @property
    def bottom_pocket_length(self) -> float:
        return 1.5
