import numpy as np


def linear(t: np.ndarray, values: list[np.ndarray | float]) -> np.ndarray:
    a, b = values
    return a + t * (b - a)


def cubic(t: np.ndarray, values: list[np.ndarray | float]) -> np.ndarray:
    a, b = values
    v = np.sqrt(1.0 - (t - 1.0) * (t - 1.0))
    return (1.0 - v) * a + v * b


def x_factor(coords: list[np.ndarray], start: float, end: float) -> np.ndarray:
    x = coords[0]
    return np.clip((x - start) / (end - start), 0.0, 1.0)


def y_factor(coords: list[np.ndarray], start: float, end: float) -> np.ndarray:
    y = coords[1]
    return np.clip((y - start) / (end - start), 0.0, 1.0)
