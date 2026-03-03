from dataclasses import dataclass, field
from typing import Callable
import openscad as osc
import traceback


@dataclass
class Slice:
    upper: Callable[[float], float]
    lower: Callable[[float], float]
    x_range: tuple[float, float]
    slices: int | None = field(default=None)


def slicer_points(upper, lower, x_range: tuple[float, float], step: float = 1):
    x_start, x_end = x_range
    x = x_start
    ups = []
    downs = []

    while x <= x_end:
        try:
            ups.append([x, upper(x)])
            downs.append([x, lower(x)])
        except Exception:
            print("Error processing x =", x)
            raise

        if x == x_end:
            break

        x += step

        if x > x_end:
            x = x_end

    return ups, downs


def extrude_z(x_range, width_step, upper, lower):
    ups, downs = slicer_points(upper, lower, x_range, width_step)
    downs_rev = downs[::-1]
    return ups + downs_rev


def callback_to_extrude_z_fn(callback: Callable[[float], Slice]):
    def slide_fn(z):
        slice = callback(z)
        x_start, x_end = slice.x_range
        width = x_end - x_start
        step = slice.slices if slice.slices is not None else max(1, int(width))

        try:
            points = extrude_z(
                slice.x_range,
                width / step if step > 0 else 1,
                slice.upper,
                slice.lower,
            )

            return points
        except Exception as e:
            print(f"Error processing z = {z}: {e}")
            traceback.print_exc()
            raise

    return slide_fn


def slicer(
    callback: Callable[[float], Slice],
    height: float,
    slices: int | None = None,
    fn: int = 100,
):
    if slices is None:
        slices = int(height)

    return osc.linear_extrude(
        callback_to_extrude_z_fn(callback),
        height=height,
        fn=fn,
        slices=slices,
    )
