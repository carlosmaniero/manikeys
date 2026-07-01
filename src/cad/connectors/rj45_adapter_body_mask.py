import sys
from manifold3d import Manifold as M
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from models.rj45 import RJ45PlacementModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class RJ45AdapterBodyMaskCAD(ManifoldObject):
    model: RJ45PlacementModel

    @property
    def housing(self) -> M:
        return M.cube(
            self.model.rj45_model.housing,
            center=True,
        ).translate(self.model.rj45_model.housing_coords)

    def assemble(self) -> M:
        mask = self.housing.translate(self.model.translation_coords)
        return mask


if __name__ == "__main__":
    mask_cad = injector.get(RJ45AdapterBodyMaskCAD)
    mask_cad.program(sys.argv)
