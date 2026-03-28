from dataclasses import dataclass
import numpy as np
from injector import inject, singleton
from .layout import Layout
from .parameters import Parameters
from interpolation import lerp, Interpolator, InterpolationChain


@singleton
@inject
@dataclass
class NumPyCapsBottomSphere:
    layout: Layout
    parameters: Parameters

    @property
    def cap_offset(self) -> float:
        return (
            self.parameters.caps.size / 2
            + self.parameters.caps.border
            + self.parameters.body.fillet
        )

    def start_x(self) -> float:
        return self.layout.positioning.left[0] - self.cap_offset

    def start_y(self) -> float:
        return self.layout.positioning.top[1] - self.cap_offset

    def end_x(self) -> float:
        return self.layout.positioning.right[0] + self.cap_offset

    def end_y(self) -> float:
        return self.layout.positioning.bottom[1] + self.cap_offset

    @property
    def highest(self) -> float:
        # TODO: calculate the actual highest point based the cap position and
        # rotation.
        return (
            self.layout.positioning.highest[2] + self.parameters.caps.border * 5
        )

    @property
    def highest_x(self) -> float:
        return self.layout.positioning.highest[0]

    def outer_start_y(self) -> float:
        return self.start_y()

    @property
    def lowest(self) -> float:
        return self.layout.positioning.lowest[2]

    @property
    def lowest_x(self) -> float:
        return self.layout.positioning.lowest[0]

    def z(self, x: np.ndarray, y: np.ndarray, offset) -> np.ndarray:
        radius = self.parameters.body.radius - offset
        distance = np.sqrt(x**2 + y**2)
        start_fixed = self.highest_x + self.parameters.caps.size / 2

        interpolation = Interpolator(
            start=start_fixed,
            end=start_fixed + self.parameters.caps.gap,
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
    parameters: Parameters

    def z(self, x: np.ndarray, _y: np.ndarray) -> np.ndarray:
        return np.full_like(x, -self.parameters.body.height)


@singleton
@inject
@dataclass
class BodyModel:
    sphere: NumPyCapsBottomSphere
    low_bottom: BodyLowBottom
    parameters: Parameters

    @property
    def effective_depth(self) -> float:
        return self.parameters.hand_support.depth

    @property
    def offset(self) -> float:
        return 0

    def low_bottom_interpolations(
        self, coords: list[np.ndarray]
    ) -> InterpolationChain:
        x, y = coords
        base = self.low_bottom.z(x, y)

        y_ratio = lerp.x_factor(
            coords,
            self.sphere.start_x() + self.offset,
            self.sphere.highest_x - self.offset,
        )

        lowest_to_heighest = np.minimum(
            lerp.reverse_cubic(
                y_ratio,
                [
                    self.sphere.lowest
                    + self.offset
                    + self.parameters.hand_support.offset_z,
                    self.sphere.highest
                    + self.offset
                    + self.parameters.hand_support.offset_z
                    + self.parameters.body.fillet,
                ],
            ),
            self.sphere.highest + self.offset,
        )

        return InterpolationChain(
            [
                Interpolator(
                    start=self.sphere.outer_start_y(),
                    end=self.sphere.start_y() + self.parameters.body.fillet,
                    base=lowest_to_heighest,
                    ratio=lerp.y_factor,
                ),
                Interpolator(
                    start=self.start_y(),
                    end=self.start_y() + self.parameters.hand_support.fillet,
                    base=base,
                    ratio=lerp.y_factor,
                ),
                Interpolator(
                    start=self.end_y(),
                    end=self.end_y() - self.parameters.body.fillet,
                    base=base,
                    ratio=lerp.y_factor,
                ),
                Interpolator(
                    start=self.start_x(),
                    end=self.start_x() + self.parameters.body.fillet,
                    base=base,
                ),
                Interpolator(
                    start=self.end_x(),
                    end=self.end_x() - self.parameters.body.fillet,
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
        return self.parameters.body.width


@singleton
@inject
@dataclass
class BodyInnerModel(BodyModel):
    @property
    def offset(self) -> float:
        return -self.parameters.body.thickness
