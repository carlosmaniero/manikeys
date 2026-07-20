from __future__ import annotations
import math
import numpy as np
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


def rotate_vector(
    vector: np.ndarray, axis: np.ndarray, angle: float
) -> np.ndarray:
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (
        vector * cos_a
        + np.cross(axis, vector) * sin_a
        + axis * np.dot(axis, vector) * (1.0 - cos_a)
    )


def generate_path_points(
    control_points: list[list[float]], num_arc_points: int = 16
) -> list[np.ndarray]:
    points = []
    n = len(control_points)

    arcs = {}
    for i in range(1, n - 1):
        cp = control_points[i]
        if len(cp) < 4 or cp[3] <= 0:
            continue

        p_prev = np.array(control_points[i - 1][:3], dtype=np.float32)
        p_curr = np.array(cp[:3], dtype=np.float32)
        p_next = np.array(control_points[i + 1][:3], dtype=np.float32)
        r = cp[3]

        v1 = p_prev - p_curr
        v2 = p_next - p_curr
        len_v1 = np.linalg.norm(v1)
        len_v2 = np.linalg.norm(v2)

        if len_v1 < 1e-6 or len_v2 < 1e-6:
            continue

        v1 = v1 / len_v1
        v2 = v2 / len_v2

        cos_theta = np.clip(np.dot(v1, v2), -1.0, 1.0)
        theta = np.arccos(cos_theta)

        if theta < 1e-4 or theta > np.pi - 1e-4:
            continue

        d = r / np.tan(theta / 2.0)
        d = min(d, len_v1 / 2.0, len_v2 / 2.0)
        r_actual = d * np.tan(theta / 2.0)

        t1 = p_curr + d * v1
        t2 = p_curr + d * v2

        bisector = v1 + v2
        len_bisector = np.linalg.norm(bisector)
        if len_bisector < 1e-6:
            continue
        bisector = bisector / len_bisector
        h = r_actual / np.sin(theta / 2.0)
        c = p_curr + h * bisector

        u1 = (t1 - c) / r_actual
        u2 = (t2 - c) / r_actual

        e1 = u1
        e2 = u2 - np.dot(u2, e1) * e1
        len_e2 = np.linalg.norm(e2)
        if len_e2 > 1e-6:
            e2 = e2 / len_e2
        else:
            e2 = np.zeros(3, dtype=np.float32)

        alpha = np.arccos(np.clip(np.dot(u1, u2), -1.0, 1.0))

        arc_pts = []
        for j in range(num_arc_points + 1):
            phi = alpha * (j / num_arc_points)
            pt = c + r_actual * (np.cos(phi) * e1 + np.sin(phi) * e2)
            arc_pts.append(pt)

        arcs[i] = (t1, t2, arc_pts)

    points.append(np.array(control_points[0][:3], dtype=np.float32))
    for i in range(1, n - 1):
        if i in arcs:
            t1, t2, arc_pts = arcs[i]
            points.extend(arc_pts)
        else:
            points.append(np.array(control_points[i][:3], dtype=np.float32))
    points.append(np.array(control_points[-1][:3], dtype=np.float32))

    unique_points = [points[0]]
    for pt in points[1:]:
        if np.linalg.norm(pt - unique_points[-1]) > 1e-6:
            unique_points.append(pt)
    return unique_points


def path_extrude(
    cross_section: manifold3d.CrossSection, control_points: list[list[float]]
) -> manifold3d.Manifold:
    path = generate_path_points(control_points)
    m = len(path) - 1
    if m < 1:
        raise ValueError("Path must contain at least 2 points.")

    polys = cross_section.to_polygons()
    if not polys:
        raise ValueError("CrossSection is empty.")
    poly = polys[0]
    K = len(poly)

    tangents = []
    for j in range(m + 1):
        if j == 0:
            t = path[1] - path[0]
        elif j == m:
            t = path[m] - path[m - 1]
        else:
            t = path[j + 1] - path[j - 1]
        len_t = np.linalg.norm(t)
        tangents.append(
            t / len_t if len_t > 1e-6 else np.array([0, 0, 1], dtype=np.float32)
        )

    normals = []
    binormals = []

    t0 = tangents[0]
    if abs(t0[0]) < 0.9:
        n0 = np.cross(t0, np.array([1, 0, 0], dtype=np.float32))
    else:
        n0 = np.cross(t0, np.array([0, 1, 0], dtype=np.float32))
    n0 = n0 / np.linalg.norm(n0)
    b0 = np.cross(t0, n0)

    normals.append(n0)
    binormals.append(b0)

    for j in range(1, m + 1):
        t_prev = tangents[j - 1]
        t_curr = tangents[j]
        n_prev = normals[j - 1]

        axis = np.cross(t_prev, t_curr)
        len_axis = np.linalg.norm(axis)
        if len_axis < 1e-6:
            n_curr = n_prev
        else:
            axis = axis / len_axis
            angle = np.arccos(np.clip(np.dot(t_prev, t_curr), -1.0, 1.0))
            n_curr = rotate_vector(n_prev, axis, angle)
            n_curr = n_curr / np.linalg.norm(n_curr)

        b_curr = np.cross(t_curr, n_curr)
        normals.append(n_curr)
        binormals.append(b_curr)

    vertices = []
    for j in range(m + 1):
        center = path[j]
        n = normals[j]
        b = binormals[j]
        for k in range(K):
            pt2d = poly[k]
            pt3d = center + pt2d[0] * n + pt2d[1] * b
            vertices.append(pt3d)

    vertices = np.array(vertices, dtype=np.float32)

    triangles = []
    for j in range(m):
        for k in range(K):
            k_next = (k + 1) % K
            a = j * K + k
            b = j * K + k_next
            c = (j + 1) * K + k_next
            d = (j + 1) * K + k

            triangles.append([a, b, c])
            triangles.append([a, c, d])

    for k in range(1, K - 1):
        triangles.append([0, k + 1, k])

    offset = m * K
    for k in range(1, K - 1):
        triangles.append([offset, offset + k, offset + k + 1])

    triangles = np.array(triangles, dtype=np.uint32)

    mesh = manifold3d.Mesh(vert_properties=vertices, tri_verts=triangles)
    return manifold3d.Manifold(mesh)
