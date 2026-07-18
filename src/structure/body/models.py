from globals.wall.parameters import WallParameters
from structure.body.parameters import BodyParameters
from models.parameters import SwitchesParameters
from models.parameters import HandSupportParameters
from dataclasses import dataclass
import numpy as np
from injector import inject, singleton
from switches.model import Layout
from core.interpolation import lerp, Interpolator, InterpolationChain


@singleton
@inject
@dataclass
class NumPyCapsBottomSphere:
    layout: Layout
    wall_parameters: WallParameters
    body_parameters: BodyParameters
    switches_parameters: SwitchesParameters
    hand_support_parameters: HandSupportParameters

    @property
    def switch_offset(self) -> float:
        return (
            self.switches_parameters.size / 2
            + self.switches_parameters.border
            + self.wall_parameters.fillet
        )

    def start_x(self) -> float:
        return (
            self.layout.bounds.left[0]
            - self.switch_offset
            - self.wall_parameters.thickness
        )

    def end_x(self) -> float:
        return self.layout.bounds.right[0] + self.switch_offset

    def start_y(self) -> float:
        return (
            self.layout.bounds.top[1]
            - self.switch_offset
            - self.wall_parameters.thickness
        )

    def end_y(self) -> float:
        return (
            self.layout.bounds.bottom[1]
            + self.switch_offset
            + self.wall_parameters.thickness * 2
        )

    @property
    def highest(self) -> float:
        # TODO: calculate the actual highest point based the switch position and
        # rotation.
        return (
            self.layout.bounds.highest[2] + self.switches_parameters.border * 5
        )

    @property
    def highest_x(self) -> float:
        return self.layout.bounds.highest[0]

    @property
    def lowest(self) -> float:
        return self.layout.bounds.lowest[2]

    @property
    def lowest_x(self) -> float:
        return self.layout.bounds.lowest[0]

    def divider_x_main(self, offset: float) -> float:
        return self.highest_x + self.switches_parameters.size / 2 - offset

    def start_fixed_x(self, offset: float) -> float:
        return self.divider_x_main(offset) + self.switches_parameters.gap

    def z(self, x: np.ndarray, y: np.ndarray, offset: float) -> np.ndarray:
        radius = self.body_parameters.radius
        distance = np.sqrt(x**2 + y**2)
        start_fixed = self.divider_x_main(offset)

        interpolation = Interpolator(
            start=start_fixed,
            end=self.start_fixed_x(offset),
            base=radius - np.sqrt(radius**2 - distance**2) + offset,
            algorithm=lerp.reverse_cubic,
        )

        return interpolation.interpolate(
            [x, y],
            self.highest + offset,
        )


@singleton
@inject
@dataclass
class BodyLowBottom:
    wall_parameters: WallParameters
    body_parameters: BodyParameters
    switches_parameters: SwitchesParameters
    hand_support_parameters: HandSupportParameters

    def z(self, x: np.ndarray, _y: np.ndarray) -> np.ndarray:
        return np.full_like(
            x,
            self.body_parameters.bottom_z,
        )


@singleton
@inject
@dataclass
class BodyModel:
    sphere: NumPyCapsBottomSphere
    low_bottom: BodyLowBottom
    wall_parameters: WallParameters
    body_parameters: BodyParameters
    switches_parameters: SwitchesParameters
    hand_support_parameters: HandSupportParameters

    @property
    def effective_depth(self) -> float:
        return self.hand_support_parameters.depth

    @property
    def offset(self) -> float:
        return 0

    @property
    def divider_x_main(self) -> float:
        return self.sphere.divider_x_main(self.offset)

    @property
    def start_fixed_x(self) -> float:
        return self.sphere.start_fixed_x(self.offset)

    @property
    def hand_support_start_x(self) -> float:
        return self.start_x()

    @property
    def hand_support_end_x(self) -> float:
        return (
            self.end_x()
            - self.hand_support_parameters.offset_x
            - self.offset * 2
        )

    @property
    def divider_y(self) -> float:
        return self.sphere.start_y() - self.wall_parameters.thickness

    @property
    def highest(self) -> float:
        return self.sphere.highest + self.offset

    def hand_support_z(self, coords: list[np.ndarray]) -> np.ndarray:
        x_ratio = lerp.x_factor(
            coords,
            self.hand_support_start_x,
            self.hand_support_end_x,
        )

        curve = lerp.cubic(
            x_ratio,
            [
                self.sphere.lowest
                + self.offset
                + self.hand_support_parameters.offset_z,
                self.sphere.highest + self.offset,
            ],
        )

        reverse_curve = lerp.reverse_cubic(
            x_ratio,
            [
                self.sphere.lowest
                + self.offset
                + self.hand_support_parameters.offset_z,
                self.sphere.highest + self.offset,
            ],
        )

        return Interpolator(
            start=(self.hand_support_start_x + self.hand_support_end_x) / 2,
            end=self.hand_support_end_x,
            base=reverse_curve,
            ratio=lerp.x_factor,
            algorithm=lerp.reverse_cubic,
        ).interpolate(
            coords,
            curve,
        )

    def low_bottom_interpolations(
        self, coords: list[np.ndarray]
    ) -> InterpolationChain:
        x, y = coords
        base = self.low_bottom.z(x, y)

        return InterpolationChain(
            [
                # Y: from sphere to hand support
                Interpolator(
                    start=self.sphere.start_y() + self.offset,
                    end=self.sphere.start_y()
                    + self.wall_parameters.fillet
                    + self.offset,
                    base=self.hand_support_z(coords),
                    ratio=lerp.y_factor,
                ),
                Interpolator(
                    start=self.start_y(),
                    end=self.start_y() + self.hand_support_parameters.fillet,
                    base=base,
                    ratio=lerp.y_factor,
                ),
                Interpolator(
                    start=self.end_y(),
                    end=self.end_y() - self.wall_parameters.fillet,
                    base=base,
                    ratio=lerp.y_factor,
                ),
                Interpolator(
                    start=self.start_x(),
                    end=self.start_x() + self.wall_parameters.fillet,
                    base=base,
                ),
                Interpolator(
                    start=self.end_x(),
                    end=self.end_x() - self.wall_parameters.fillet,
                    base=base,
                ),
            ]
        )

    def z(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        z = self.sphere.z(x, y, self.offset)

        return self.low_bottom_interpolations([x, y]).interpolate([x, y], z)

    def start_x(self) -> float:
        return self.sphere.start_x() - self.offset

    def end_x(self) -> float:
        return self.start_x() + self.effective_width + self.offset * 2

    def start_y(self) -> float:
        return self.sphere.start_y() - self.effective_depth - self.offset

    def end_y(self) -> float:
        return self.sphere.end_y() + self.offset

    @property
    def width(self) -> float:
        return self.end_x() - self.start_x()

    @property
    def depth(self) -> float:
        return self.end_y() - self.start_y()

    @property
    def effective_width(self) -> float:
        return self.body_parameters.width

    @property
    def bottom_z(self) -> float:
        return self.body_parameters.bottom_z

    @property
    def connectors_bottom_offset(self) -> float:
        return self.body_parameters.connectors_bottom_offset

    @property
    def height(self) -> float:
        return self.highest - self.bottom_z


@singleton
@inject
@dataclass
class BodyInnerModel(BodyModel):
    @property
    def offset(self) -> float:
        return -self.wall_parameters.thickness
