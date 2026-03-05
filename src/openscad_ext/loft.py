from dataclasses import dataclass, field
from typing import Callable
import openscad as osc
import traceback


@dataclass
class Profile:
    upper: Callable[[float], float]
    lower: Callable[[float], float]
    span: tuple[float, float]
    segments: int | None = field(default=None)


def profile_points(upper, lower, span: tuple[float, float], step: float = 1):
    start, end = span
    v = start
    ups = []
    downs = []

    while v <= end:
        try:
            ups.append([v, upper(v)])
            downs.append([v, lower(v)])
        except Exception:
            print("Error processing v =", v)
            raise

        if v == end:
            break

        v += step

        if v > end:
            v = end

    return ups, downs


def to_polygon(span, width_step, upper, lower):
    ups, downs = profile_points(upper, lower, span, width_step)
    downs_rev = downs[::-1]
    return ups + downs_rev


def callback_to_polygon_fn(callback: Callable[[float], Profile]):
    def polygon_fn(t):
        profile = callback(t)
        start, end = profile.span
        width = end - start
        step = (
            profile.segments
            if profile.segments is not None
            else max(1, int(width))
        )

        try:
            points = to_polygon(
                profile.span,
                width / step if step > 0 else 1,
                profile.upper,
                profile.lower,
            )

            return points
        except Exception as e:
            print(f"Error processing t = {t}: {e}")
            traceback.print_exc()
            raise

    return polygon_fn


def loft(
    callback: Callable[[float], Profile],
    span: tuple[float, float],
    slices: int | None = None,
    fn: int = 100,
):
    start, end = span
    height = end - start

    if slices is None:
        slices = int(height)

    def internal_callback(t_relative):
        return callback(t_relative + start)

    return osc.linear_extrude(
        callback_to_polygon_fn(internal_callback),
        height=height,
        fn=fn,
        slices=slices,
    ).translate([0, 0, start])
