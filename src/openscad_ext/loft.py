from dataclasses import dataclass, field
from typing import Callable
import openscad as osc
import traceback

SMALL_OFFSET = 1e-6


@dataclass
class Profile:
    upper: Callable[[float], float]
    lower: Callable[[float], float]
    span: tuple[float, float]
    segments: int | None = field(default=None)
    breakpoints: list[float] | None = field(default=None)


def profile_points(
    upper,
    lower,
    span: tuple[float, float],
    step: float = 1,
    breakpoints: list[float] | None = None,
):
    start, end = span

    pts = [p for p in (breakpoints or []) if start < p < end]
    left_pts = [p - SMALL_OFFSET for p in pts]
    right_pts = [p + SMALL_OFFSET for p in pts]
    milestones = sorted([start] + left_pts + pts + right_pts + [end])

    all_vs = []
    for segment_start, segment_end in zip(milestones, milestones[1:]):
        dist = segment_end - segment_start
        num_steps = max(1, int(round(dist / step)))
        actual_step = dist / num_steps

        for i in range(num_steps):
            all_vs.append(segment_start + i * actual_step)

    all_vs.append(end)

    ups = []
    downs = []
    for v in all_vs:
        try:
            ups.append([v, upper(v)])
            downs.append([v, lower(v)])
        except Exception:
            print(f"Error processing v = {v}")
            raise

    return ups, downs


def to_polygon(
    span, width_step, upper, lower, breakpoints: list[float] | None = None
):
    ups, downs = profile_points(upper, lower, span, width_step, breakpoints)
    downs_rev = downs[::-1]
    return ups + downs_rev


def callback_to_polygon_fn(callback: Callable[[float], Profile]):
    def polygon_fn(t):
        profile = callback(t)
        start, end = profile.span
        width = end - start

        resolution_count = (
            profile.segments
            if profile.segments is not None
            else max(1, int(width))
        )
        step = width / resolution_count if resolution_count > 0 else 1

        try:
            points = to_polygon(
                profile.span,
                step,
                profile.upper,
                profile.lower,
                breakpoints=profile.breakpoints,
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
    overlap_offset = SMALL_OFFSET

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
