from dataclasses import dataclass
from injector import inject, singleton
from .parameters import Parameters, PogoPinParameters
from .body import BodyModel


@singleton
@inject
@dataclass
class PogoPinModel:
    parameters: Parameters
    body_model: BodyModel

    @property
    def pogo_pin(self) -> PogoPinParameters:
        return self.parameters.pogo_pin

    @property
    def body_length(self) -> float:
        return self.pogo_pin.body_length

    @property
    def body_width(self) -> float:
        return self.pogo_pin.body_width

    @property
    def body_height(self) -> float:
        return self.pogo_pin.body_height

    @property
    def flange_thickness(self) -> float:
        return self.pogo_pin.flange_thickness

    @property
    def mounting_hole_diameter(self) -> float:
        return self.pogo_pin.mounting_hole_diameter

    @property
    def mounting_hole_distance(self) -> float:
        return self.pogo_pin.mounting_hole_distance

    @property
    def pin_pitch(self) -> float:
        return self.pogo_pin.pin_pitch

    @property
    def pin_count(self) -> int:
        return self.pogo_pin.pin_count

    @property
    def magnet_distance(self) -> float:
        return self.pogo_pin.magnet_distance

    @property
    def pin_height(self) -> float:
        return self.pogo_pin.pin_height

    @property
    def pin_tip_diameter(self) -> float:
        return self.pogo_pin.pin_tip_diameter

    @property
    def solder_tail_diameter(self) -> float:
        return self.pogo_pin.solder_tail_diameter

    @property
    def solder_tail_length(self) -> float:
        return self.pogo_pin.solder_tail_length

    @property
    def flange_full_length(self) -> float:
        return self.mounting_hole_distance + self.mounting_hole_diameter + 1.0

    @property
    def flange_z_offset(self) -> float:
        return self.body_height / 2 - 2.0 - self.flange_thickness / 2

    @property
    def pins_start_x(self) -> float:
        return -(self.pin_count - 1) * self.pin_pitch / 2

    @property
    def thickness(self) -> float:
        return self.parameters.body.thickness

    @property
    def adapter_width(self) -> float:
        return self.flange_full_length + self.thickness * 2

    @property
    def adapter_length(self) -> float:
        return self.body_width + self.thickness * 2

    @property
    def adapter_height(self) -> float:
        return self.thickness

    @property
    def adapter_z_center(self) -> float:
        return self.body_height / 2 - self.adapter_height / 2

    @property
    def adapter_screw_hole_diameter(self) -> float:
        return 1.2
