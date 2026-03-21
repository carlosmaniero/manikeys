from dataclasses import dataclass
import math
import numpy as np
from injector import inject, singleton
from .layout import Layout
from .parameters import Parameters
from openscad_ext.interpolation import smooth_interpolate_from_to
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


@dataclass
class BodyThumbSection:
    layout: Layout
    parameters: Parameters

    @property
    def width(self) -> float:
        return (self.parameters.caps.size * 1.5 + self.parameters.caps.gap) * 2

    def z(self, x: float, y: float, reference_z: float) -> float:
        if x < 0:
            return smooth_interpolate_from_to(
                reference_z,
                self.highest_cap_z() - 10,
                x,
                -self.parameters.body.fillet,
                0,
            )
        if x > self.width:
            return smooth_interpolate_from_to(
                self.highest_cap_z() - 10,
                reference_z,
                x,
                self.width,
                self.width + self.parameters.body.fillet,
                reversed=True,
            )
        return self.highest_cap_z() - 10

    def highest_cap_z(self) -> float:
        return (
            self.layout.positioning.highest[2] + self.parameters.caps.size / 2
        )


@dataclass
class LegacyBodyModel:
    layout: Layout
    parameters: Parameters
    thumb_section: BodyThumbSection

    def _is_thumb_section(self, x: float) -> bool:
        return (
            self.end_x() - self.fillet * 3
            > x
            > self.thumb_section.width + self.fillet
        )

    def top_z_with_thumb(self, x: float, y: float) -> float:
        sphere_z = self.sphere_lower_z(x, y)

        if y == self.start_y():
            return self.min_z

        if y >= self.last_cap_y():
            return smooth_interpolate_from_to(
                sphere_z,
                self.highest_cap_z(),
                y,
                self.last_cap_y(),
                self.last_cap_y() + self.fillet,
                reversed=True,
            )

        reference = self.first_cap_y() - self.fillet * 2

        if y < reference:
            delta_y = 2 - y / reference
            z = self.highest_cap_z() * delta_y

            if self._is_thumb_section(x):
                relative_x = x - self.thumb_section.width - self.fillet * 2
                return self.thumb_section.z(relative_x, y, z)

            return z

        if y < self.first_cap_y():
            return smooth_interpolate_from_to(
                self.highest_cap_z(),
                sphere_z,
                y,
                self.first_cap_y() - self.fillet,
                self.first_cap_y(),
            )

        return sphere_z

    @property
    def min_z(self) -> float:
        return -self.parameters.body.height

    @property
    def fillet(self) -> float:
        return self.parameters.body.fillet

    @property
    def fillet_end_y(self) -> float:
        return self.end_y() - self.fillet

    @property
    def fillet_start_x(self) -> float:
        return self.start_x() + self.fillet

    def top_z(self, x: float, y: float) -> float:
        """ "
        this is the most important function of this model.

        This represent the top z coordinate through the coordinates x and y.
        """
        z = self.top_z_with_thumb(x, y)

        zy_smothed = smooth_interpolate_from_to(
            z,
            self.min_z,
            y,
            self.fillet_end_y,
            self.end_y(),
            reversed=True,
        )

        if x <= self.fillet_start_x:
            return smooth_interpolate_from_to(
                self.min_z,
                zy_smothed,
                x,
                self.start_x(),
                self.fillet_start_x,
            )

        if x > self.end_x() - self.fillet * 2:
            return smooth_interpolate_from_to(
                zy_smothed,
                self.min_z,
                x,
                self.end_x() - self.fillet * 2,
                self.end_x(),
                reversed=True,
            )

        return zy_smothed

    def highest_cap_z(self) -> float:
        return (
            self.layout.positioning.highest[2] + self.parameters.caps.size / 2
        )

    def start_x(self) -> float:
        return -self.parameters.caps.size - self.parameters.caps.gap

    def end_x(self) -> float:
        return 180 + self.start_x()

    def start_y(self) -> float:
        return (
            self.first_cap_y()
            - (self.parameters.caps.size + self.parameters.caps.gap) * 2
        )

    def end_y(self) -> float:
        return 180 + self.start_y()

    def last_cap_y(self) -> float:
        return (
            self.layout.positioning.bottom[1]
            + self.parameters.caps.size / 2
            + self.parameters.caps.gap
        )

    def first_cap_y(self) -> float:
        return (
            self.layout.positioning.top[1]
            - self.parameters.caps.size / 2
            - self.parameters.caps.gap * 2
        )

    def sphere_lower_z(self, x: float, y: float) -> float:
        radius = self.parameters.body.radius
        distance = math.sqrt(x**2 + y**2)
        highest = self.highest_cap_z()

        if distance >= radius:
            return min(radius, highest)
        else:
            result = radius - math.sqrt(radius**2 - distance**2)
            return min(result, highest)


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
class BodyModel(LegacyBodyModel):
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
