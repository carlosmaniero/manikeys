import math
from typing import List, Tuple, Optional

Vector3 = List[float]
Rotation = List[float]


class SphereProjection:
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

    def project_with_rotation(self, point: Vector3) -> Tuple[Vector3, Rotation]:
        projected_point = self.project(point)

        rot_x = math.degrees(
            math.atan2(projected_point[1] - self.position[1], self.radius)
        )
        rot_y = -math.degrees(
            math.atan2(projected_point[0] - self.position[0], self.radius)
        )

        return projected_point, [rot_x, rot_y, 0.0]
