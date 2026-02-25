from injector import Module, provider, singleton
from models.parameters import Parameters
from models.projection import SphereProjection


class ProjectionModule(Module):
    @singleton
    @provider
    def provide_projection(self, parameters: Parameters) -> SphereProjection:
        return SphereProjection(parameters.body.radius)
