from dataclasses import dataclass, field
from typing import Callable, cast
import numpy as np
from . import lerp


@dataclass
class Interpolator:
    start: float
    end: float
    base: np.ndarray | float
    algorithm: Callable[[np.ndarray, list[np.ndarray | float]], np.ndarray] = (
        field(default=lerp.cubic)
    )
    ratio: Callable[[list[np.ndarray], float, float], np.ndarray] = field(
        default=lerp.x_factor
    )

    def interpolate(
        self,
        coords: list[np.ndarray],
        target: np.ndarray | float,
    ) -> np.ndarray:
        t = self.ratio(coords, self.start, self.end)
        return self.algorithm(t, [self.base, target])


@dataclass
class InterpolationChain:
    interpolators: list[Interpolator] = field(default_factory=list)

    def interpolate(
        self,
        coords: list[np.ndarray],
        initial_target: np.ndarray | float,
    ) -> np.ndarray:
        result = cast(np.ndarray, initial_target)
        for interpolator in self.interpolators:
            result = interpolator.interpolate(coords, result)
        return result
