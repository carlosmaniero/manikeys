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
        return (
            self.layout.positioning.highest[2] + self.parameters.caps.border * 5
        )

    @property
    def highest_x(self) -> float:
        return self.layout.positioning.highest[0]

    @property
    def lowest(self) -> float:
        return self.layout.positioning.lowest[2]

    @property
    def lowest_x(self) -> float:
        return self.layout.positioning.lowest[0]

    def z(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        radius = self.parameters.body.radius
        distance = np.sqrt(x**2 + y**2)
        start_fixed = self.highest_x + self.parameters.caps.size / 2

        interpolation = Interpolator(
            start=start_fixed,
            end=start_fixed + self.parameters.caps.gap,
            base=radius - np.sqrt(radius**2 - distance**2),
            algorithm=lerp.reverse_cubic,
        )

        return interpolation.interpolate(
            [x, y],
            self.highest,
        )


@singleton
@inject
@dataclass
class HoleNumPyCapsBottomSphere(NumPyCapsBottomSphere):
    layout: Layout
    parameters: Parameters

    @property
    def cap_offset(self) -> float:
        return super().cap_offset - self.parameters.body.thickness

    def z(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        super_z = super().z(x, y)
        return super_z - self.parameters.body.thickness


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
    caps_bottom_sphere: NumPyCapsBottomSphere
    low_bottom: BodyLowBottom
    parameters: Parameters

    def low_bottom_interpolations(
        self, coords: list[np.ndarray]
    ) -> InterpolationChain:
        x, y = coords
        base = self.low_bottom.z(x, y)

        y_ratio = lerp.x_factor(
            coords,
            self.caps_bottom_sphere.start_x(),
            self.caps_bottom_sphere.highest_x,
        )

        lowest_to_heighest = np.minimum(
            lerp.reverse_cubic(
                y_ratio,
                [
                    self.caps_bottom_sphere.lowest + 10,
                    self.caps_bottom_sphere.highest
                    + 10
                    + self.parameters.body.fillet,
                ],
            ),
            self.caps_bottom_sphere.highest,
        )

        return InterpolationChain(
            [
                Interpolator(
                    start=self.caps_bottom_sphere.start_y(),
                    end=self.caps_bottom_sphere.start_y()
                    + self.parameters.body.fillet,
                    base=lowest_to_heighest,
                    ratio=lerp.y_factor,
                ),
                Interpolator(
                    start=self.start_y(),
                    end=self.start_y() + 50,
                    base=base,
                    ratio=lerp.y_factor,
                ),
                Interpolator(
                    start=self.caps_bottom_sphere.end_y(),
                    end=self.caps_bottom_sphere.end_y()
                    - self.parameters.body.fillet,
                    base=base,
                    ratio=lerp.y_factor,
                ),
                Interpolator(
                    start=self.caps_bottom_sphere.start_x(),
                    end=self.caps_bottom_sphere.start_x()
                    + self.parameters.body.fillet,
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
        z = self.caps_bottom_sphere.z(x, y)

        return self.low_bottom_interpolations([x, y]).interpolate([x, y], z)

    def start_x(self) -> float:
        return self.caps_bottom_sphere.start_x()

    def end_x(self) -> float:
        return self.start_x() + 180

    def start_y(self) -> float:
        return self.caps_bottom_sphere.start_y() - 110

    def end_y(self) -> float:
        return self.caps_bottom_sphere.end_y()


@singleton
@inject
@dataclass
class BodyInnerModel:
    parameters: Parameters
    hole: HoleNumPyCapsBottomSphere

    def low_bottom_interpolations(self):
        base = -self.parameters.body.height
        return InterpolationChain(
            [
                Interpolator(
                    start=self.hole.start_x(),
                    end=self.hole.start_x() + self.parameters.body.fillet,
                    base=base,
                ),
                Interpolator(
                    start=self.hole.end_x(),
                    end=self.hole.end_x() - self.parameters.body.fillet,
                    base=base,
                ),
                Interpolator(
                    start=self.hole.start_y(),
                    end=self.hole.start_y() + self.parameters.body.fillet,
                    base=base,
                    ratio=lerp.y_factor,
                ),
                Interpolator(
                    start=self.hole.end_y(),
                    end=self.hole.end_y() - self.parameters.body.fillet,
                    base=base,
                    ratio=lerp.y_factor,
                ),
            ]
        )

    def z(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        z = np.where(
            (x >= self.hole.start_x())
            & (x <= self.hole.end_x())
            & (y >= self.hole.start_y())
            & (y <= self.hole.end_y()),
            self.hole.z(x, y),
            -self.parameters.body.height,
        )

        return self.low_bottom_interpolations().interpolate([x, y], z)

    def start_x(self) -> float:
        return self.hole.start_x()

    def end_x(self) -> float:
        return self.hole.end_x()

    def start_y(self) -> float:
        return self.hole.start_y()

    def end_y(self) -> float:
        return self.hole.end_y()
