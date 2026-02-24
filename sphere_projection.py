import math
from typing import Optional, Tuple
from models.projection import Projection, Vector3, Rotation


class SphereProjection(Projection):
    def __init__(self, r: float, position: Optional[Vector3] = None):
        self.radius = float(r)
        if position is None:
            self.position = [0.0, 0.0, self.radius]
        else:
            self.position = position

    def project(self, point: Vector3) -> Vector3:
        normalized_radius = self.radius - point[2]

        vector = [
            point[0] - self.position[0],
            point[1] - self.position[1],
            0.0 - self.position[2],
        ]

        length = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)

        if length == 0:
            return self.position

        return [
            self.position[0] + vector[0] / length * normalized_radius,
            self.position[1] + vector[1] / length * normalized_radius,
            self.position[2] + vector[2] / length * normalized_radius,
        ]

    def project_rotation(self, point: Vector3) -> Rotation:
        rot_x = math.degrees(
            math.atan2(point[1] - self.position[1], self.radius)
        )
        rot_y = -math.degrees(
            math.atan2(point[0] - self.position[0], self.radius)
        )

        return [rot_x, rot_y, 0.0]

    def project_with_rotation(self, point: Vector3) -> Tuple[Vector3, Rotation]:
        projected_point = self.project(point)

        return projected_point, self.project_rotation(projected_point)

    def _move_arc(
        self,
        fixed_val: float,
        moving_val: float,
        z_val: float,
        length: float,
        direction: int,
    ) -> Tuple[float, float]:
        radius_effective_sq = self.radius**2 - fixed_val**2

        if radius_effective_sq <= 0:
            return moving_val, z_val

        r_eff = math.sqrt(radius_effective_sq)

        current_angle = math.atan2(z_val, moving_val)
        delta_theta = length / r_eff

        new_angle = current_angle + (delta_theta * direction)

        new_moving = r_eff * math.cos(new_angle)
        new_z = r_eff * math.sin(new_angle)

        return new_moving, new_z

    def move_constant_x(
        self, initial_point: Vector3, length: float, direction: int = 1
    ) -> Vector3:
        x, y, z = initial_point
        new_y, new_z = self._move_arc(x, y, z, length, direction)
        return [x, new_y, new_z]

    def move_constant_y(
        self, initial_point: Vector3, length: float, direction: int = 1
    ) -> Vector3:
        x, y, z = initial_point
        new_x, new_z = self._move_arc(y, x, z, length, direction)
        return [new_x, y, new_z]
