from dataclasses import dataclass
from injector import inject, singleton
from structure.body.models import BodyInnerModel


@singleton
@inject
@dataclass
class MountModel(BodyInnerModel):
    @property
    def offset(self) -> float:
        # TODO: it also should have an error margin
        return super().offset - self.body_parameters.clearance


@singleton
@inject
@dataclass
class MountCavityModel(MountModel):
    @property
    def offset(self) -> float:
        return super().offset - self.wall_parameters.thickness
