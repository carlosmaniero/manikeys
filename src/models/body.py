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

    def z(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        radius = self.parameters.body.radius
        distance = np.sqrt(x**2 + y**2)

        return radius - np.sqrt(radius**2 - distance**2)


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

    def low_bottom_interpolations(self, base: np.ndarray | float):
        return InterpolationChain(
            [
                Interpolator(
                    start=self.caps_bottom_sphere.start_x(),
                    end=self.caps_bottom_sphere.start_x()
                    + self.parameters.body.fillet,
                    base=base,
                ),
                Interpolator(
                    start=self.caps_bottom_sphere.end_x(),
                    end=self.caps_bottom_sphere.end_x()
                    - self.parameters.body.fillet,
                    base=base,
                ),
                Interpolator(
                    start=self.caps_bottom_sphere.start_y(),
                    end=self.caps_bottom_sphere.start_y()
                    + self.parameters.body.fillet,
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
            ]
        )

    def z(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        z = self.caps_bottom_sphere.z(x, y)
        base_z = self.low_bottom.z(x, y)

        return self.low_bottom_interpolations(base_z).interpolate([x, y], z)

    def start_x(self) -> float:
        return self.caps_bottom_sphere.start_x()

    def end_x(self) -> float:
        return self.caps_bottom_sphere.end_x()

    def start_y(self) -> float:
        return self.caps_bottom_sphere.start_y()

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
