from __future__ import annotations
from dataclasses import dataclass
from injector import inject, singleton


@singleton
@inject
@dataclass
class Led:
    @property
    def pcb_radius(self) -> float:
        return 5

    @property
    def pcb_height(self) -> float:
        return 2

    @property
    def led_size(self) -> float:
        return 5

    @property
    def led_height(self) -> float:
        return 1

    @property
    def full_height(self) -> float:
        return self.pcb_height + self.led_height
