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
    breakpoints: list[float] | None = None,
):
    start, end = span
    total_height = end - start

    points = sorted([p for p in (breakpoints or []) if start < p < end])
    all_points = [start] + points + [end]

    results = []
    overlap_offset = 0.0000001

    for segment_start, segment_end in zip(all_points, all_points[1:]):
        adjusted_end = segment_end

        if segment_end != end:
            # TODO: Because of this offset the union of segments contains a
            # very thin gap.
            # This can be solved by extruding the last segment of each part and
            # extrudind it until the overlap that way the union will be
            # seamless, but for now this is good enough.
            adjusted_end -= overlap_offset

        height = adjusted_end - segment_start

        if height <= 0:
            continue

        if slices is not None:
            current_slices = max(1, int(slices * (height / total_height)))
        else:
            current_slices = max(1, int(height))

        def internal_callback(t_relative, start_at=segment_start):
            return callback(t_relative + start_at)

        extrusion = osc.linear_extrude(
            callback_to_polygon_fn(internal_callback),
            height=height,
            fn=fn,
            slices=current_slices,
        ).translate([0, 0, segment_start])

        results.append(extrusion)

    if not results:
        return osc.union()

    return osc.union(*results) if len(results) > 1 else results[0]
