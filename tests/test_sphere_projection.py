import math
from models.projection import SphereProjection


def test_move_constant_x():
    proj = SphereProjection(100.0)
    p1 = [10.0, 20.0, 30.0]
    res = proj.move_constant_x(p1, 5.0, 1)

    x, y, z = p1
    radius = 100.0
    r_eff = math.sqrt(radius**2 - x**2)
    angle = math.atan2(z, y)
    new_angle = angle + (5.0 / r_eff)
    exp_y = r_eff * math.cos(new_angle)
    exp_z = r_eff * math.sin(new_angle)

    assert math.isclose(res[0], x)
    assert math.isclose(res[1], exp_y)
    assert math.isclose(res[2], exp_z)


def test_move_constant_y():
    proj = SphereProjection(100.0)
    p1 = [10.0, 20.0, 30.0]
    res = proj.move_constant_y(p1, 5.0, 1)

    x, y, z = p1
    radius = 100.0
    r_eff = math.sqrt(radius**2 - y**2)
    angle = math.atan2(z, x)
    new_angle = angle + (5.0 / r_eff)
    exp_x = r_eff * math.cos(new_angle)
    exp_z = r_eff * math.sin(new_angle)

    assert math.isclose(res[0], exp_x)
    assert math.isclose(res[1], y)
    assert math.isclose(res[2], exp_z)


def test_move_constant_limit():
    proj = SphereProjection(10.0)
    p1 = [10.0, 0.0, 0.0]
    res = proj.move_constant_x(p1, 5.0, 1)
    assert res == p1

    p2 = [0.0, 10.0, 0.0]
    res2 = proj.move_constant_y(p2, 5.0, 1)
    assert res2 == p2
