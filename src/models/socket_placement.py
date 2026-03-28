from dataclasses import dataclass
from injector import inject, singleton
from .body import BodyInnerModel


@singleton
@inject
@dataclass
class SocketPlacement(BodyInnerModel):
    @property
    def offset(self) -> float:
        # TODO: it also should have an error margin
        return super().offset - self.parameters.body.clearance


@singleton
@inject
@dataclass
class SocketPlacementInner(SocketPlacement):
    @property
    def offset(self) -> float:
        return super().offset - self.parameters.body.thickness
