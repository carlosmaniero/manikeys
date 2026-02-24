from abc import ABC, abstractmethod
from typing import List, Tuple

Vector3 = List[float]
Rotation = List[float]


class Projection(ABC):
    @abstractmethod
    def project(self, point: Vector3) -> Vector3:
        """Projects a 3D point onto the surface."""
        pass

    @abstractmethod
    def project_with_rotation(self, point: Vector3) -> Tuple[Vector3, Rotation]:
        """Projects a 3D point and returns its position and surface-aligned rotation."""
        pass
