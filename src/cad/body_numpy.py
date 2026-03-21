from __future__ import annotations
import sys
import os
import numpy as np
from typing import Protocol
from typing import Callable
from injector import inject, singleton
from dataclasses import dataclass, field
import pyvista as pv
from models.body import BodyModel
from models.layout import Layout
from models.parameters import Parameters
from numpy_ext import map_meshgrid
from pyvista_ext import create_full_surface, VistaObject
from context import injector

SLICES = int(os.getenv("SLICES", 800))


class ZProtocol(Protocol):
    def z(self, x: np.ndarray, y: np.ndarray) -> np.ndarray: ...


@singleton
@inject
@dataclass
class NumPyCapsBottomSphere:
    layout: Layout
    parameters: Parameters

    @property
    def cap_offset(self):
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
    def cap_offset(self):
        return super().cap_offset - self.parameters.body.thickness

    def z(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        super_z = super().z(x, y)
        return super_z - self.parameters.body.thickness


def linear_interpolation(
    t: np.ndarray, a: np.ndarray | float, b: np.ndarray | float
) -> np.ndarray:
    return a + t * (b - a)


def cubic_interpolation(
    t: np.ndarray, a: np.ndarray | float, b: np.ndarray | float
) -> np.ndarray:
    v = np.sqrt(1.0 - (t - 1.0) * (t - 1.0))
    return (1.0 - v) * a + v * b


def from_to_x_ratio(
    x: np.ndarray, _y: np.ndarray, start: float, end: float
) -> np.ndarray:
    return np.clip((x - start) / (end - start), 0.0, 1.0)


def from_to_y_ratio(
    _x: np.ndarray, y: np.ndarray, start: float, end: float
) -> np.ndarray:
    return np.clip((y - start) / (end - start), 0.0, 1.0)


@dataclass
class Interpolator:
    start: float
    end: float
    algorithm: Callable[
        [np.ndarray, np.ndarray | float, np.ndarray | float], np.ndarray
    ] = field(default=cubic_interpolation)
    ratio: Callable[[np.ndarray, np.ndarray, float, float], np.ndarray] = field(
        default=from_to_x_ratio
    )

    def interpolate(
        self,
        x: np.ndarray,
        y: np.ndarray,
        a: np.ndarray | float,
        b: np.ndarray | float,
    ) -> np.ndarray:
        t = self.ratio(x, y, self.start, self.end)
        return self.algorithm(t, a, b)


@singleton
@inject
@dataclass
class BodyBottom:
    parameters: Parameters
    hole: HoleNumPyCapsBottomSphere

    def low_bottom_interpolations(self):
        return [
            Interpolator(
                start=self.hole.start_x(),
                end=self.hole.start_x() + self.parameters.body.fillet,
            ),
            Interpolator(
                start=self.hole.end_x(),
                end=self.hole.end_x() - self.parameters.body.fillet,
            ),
            Interpolator(
                start=self.hole.start_y(),
                end=self.hole.start_y() + self.parameters.body.fillet,
                ratio=from_to_y_ratio,
            ),
            Interpolator(
                start=self.hole.end_y(),
                end=self.hole.end_y() - self.parameters.body.fillet,
                ratio=from_to_y_ratio,
            ),
        ]

    def z(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        z = np.where(
            (x >= self.hole.start_x())
            & (x <= self.hole.end_x())
            & (y >= self.hole.start_y())
            & (y <= self.hole.end_y()),
            self.hole.z(x, y),
            -self.parameters.body.height,
        )

        for interpolator in self.low_bottom_interpolations():
            z = interpolator.interpolate(x, y, -self.parameters.body.height, z)

        return z


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
class NumPyBodyModel(BodyModel):
    caps_bottom_sphere: NumPyCapsBottomSphere
    low_bottom: BodyLowBottom
    parameters: Parameters

    def low_bottom_interpolations(self):
        return [
            Interpolator(
                start=self.caps_bottom_sphere.start_x(),
                end=self.caps_bottom_sphere.start_x()
                + self.parameters.body.fillet,
            ),
            Interpolator(
                start=self.caps_bottom_sphere.end_x(),
                end=self.caps_bottom_sphere.end_x()
                - self.parameters.body.fillet,
            ),
            Interpolator(
                start=self.caps_bottom_sphere.start_y(),
                end=self.caps_bottom_sphere.start_y()
                + self.parameters.body.fillet,
                ratio=from_to_y_ratio,
            ),
            Interpolator(
                start=self.caps_bottom_sphere.end_y(),
                end=self.caps_bottom_sphere.end_y()
                - self.parameters.body.fillet,
                ratio=from_to_y_ratio,
            ),
        ]

    def z(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        interpolations = self.low_bottom_interpolations()

        z = self.caps_bottom_sphere.z(x, y)
        base_z = self.low_bottom.z(x, y)

        for interpolator in interpolations:
            z = interpolator.interpolate(x, y, base_z, z)

        return z

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
class BodyCAD(VistaObject):
    model: NumPyBodyModel
    bottom: BodyBottom

    def assemble(self) -> pv.PolyData:
        xrange = np.linspace(
            self.model.start_x(),
            self.model.end_x(),
            SLICES,
            endpoint=True,
        )

        def yfn(x_arr):
            start_y = np.full_like(x_arr, self.model.start_y())
            end_y = np.full_like(x_arr, self.model.end_y())
            return np.linspace(start_y, end_y, SLICES, axis=-1)

        x, y = map_meshgrid(xrange, yfn)

        top_z = self.model.z(x, y)

        bottom_z = self.bottom.z(x, y)

        return create_full_surface(x, y, top_z, bottom_z)


if __name__ == "__main__":
    body = injector.get(BodyCAD)
    body.program(sys.argv)
