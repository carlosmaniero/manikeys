from __future__ import annotations
import manifold3d


def rounded_box(
    size: list[float],
    radius: float,
    circular_segments: int = 32,
    center: bool = True,
) -> manifold3d.Manifold:
    width, depth, height = size[0], size[1], size[2]
    cyl = manifold3d.Manifold.cylinder(
        height, radius, center=center, circular_segments=circular_segments
    )
    x_off = width / 2 - radius
    y_off = depth / 2 - radius
    x_off = max(0.0, x_off)
    y_off = max(0.0, y_off)
    c1 = cyl.translate([x_off, y_off, 0])
    c2 = cyl.translate([-x_off, y_off, 0])
    c3 = cyl.translate([x_off, -y_off, 0])
    c4 = cyl.translate([-x_off, -y_off, 0])
    return (c1 + c2 + c3 + c4).hull()


def capsule(
    size: list[float],
    circular_segments: int = 32,
    center: bool = True,
) -> manifold3d.Manifold:
    length, width, height = size[0], size[1], size[2]
    radius = width / 2
    cyl = manifold3d.Manifold.cylinder(
        height, radius, center=center, circular_segments=circular_segments
    )
    x_off = length / 2 - radius
    if x_off <= 0:
        return cyl
    return manifold3d.Manifold.hull(
        cyl.translate([-x_off, 0, 0]) + cyl.translate([x_off, 0, 0])
    )


def rounded_box_flat_bottom(
    size: list[float],
    radius: float,
    circular_segments: int = 32,
    center: bool = True,
) -> manifold3d.Manifold:
    width, depth, height = size[0], size[1], size[2]
    rbox = rounded_box(
        [width, depth, height],
        radius,
        circular_segments=circular_segments,
        center=center,
    )
    cube = manifold3d.Manifold.cube([width, depth, height / 2], center=center)
    if center:
        cube = cube.translate([0, 0, -height / 4])
    return rbox + cube


def half_rounded(
    size: list[float],
    circular_segments: int = 32,
    center: bool = True,
) -> manifold3d.Manifold:
    width, depth, height = size[0], size[1], size[2]
    radius = width / 2

    cyl = manifold3d.Manifold.cylinder(
        depth, radius, center=True, circular_segments=circular_segments
    ).rotate([90, 0, 0])

    top_box = manifold3d.Manifold.cube(
        [width, depth, radius], center=True
    ).translate([0, 0, radius / 2])
    semicyl = cyl ^ top_box

    flat_height = max(0.0, height - radius)

    if flat_height > 0:
        base_box = manifold3d.Manifold.cube(
            [width, depth, flat_height], center=True
        ).translate([0, 0, -flat_height / 2])
        result = base_box + semicyl
    else:
        result = semicyl
        if height != radius:
            result = result.scale([1, 1, height / radius])

    if center:
        result = result.translate([0, 0, (flat_height - radius) / 2])
    else:
        result = result.translate([0, 0, flat_height])

    return result
