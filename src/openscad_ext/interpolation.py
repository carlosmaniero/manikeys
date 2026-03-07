import math


def smooth_step(t: float) -> float:
    """
    Circular interpolation (Ease-out) factor.
    Returns a value between 0 and 1.
    """
    t = max(0.0, min(1.0, abs(t)))
    # Circular ease-out: sqrt(1 - (t - 1)^2)
    return math.sqrt(1.0 - (t - 1.0) * (t - 1.0))


def smooth_interpolate(a: float, b: float, t: float) -> float:
    """
    Smoothly interpolates between values a and b based on factor t [0, 1].
    """
    v = smooth_step(t)
    return (1.0 - v) * a + v * b


def smooth_interpolate_from_to(
    a: float, b: float, x: float, from_x: float, to_x: float
) -> float:
    """
    Smoothly interpolates between values a and b based on x in range [from_x, to_x].
    """
    if from_x == to_x:
        return a
    t = (x - from_x) / (to_x - from_x)
    return smooth_interpolate(a, b, t)


def smooth_transition(f, h, t):
    v = smooth_step(t)

    def combined_func(x):
        return (1 - v) * f(x) + v * h(x)

    return combined_func


def smooth_transition_from_to(f, h, from_x, to_x):
    return lambda x: smooth_transition(f, h, (x - from_x) / (to_x - from_x))(x)
