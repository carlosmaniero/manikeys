from structure.body.parameters import BodyParameters
from injector import Module, provider, singleton
from models.projection import SphereProjection


class ProjectionModule(Module):
    @singleton
    @provider
    def provide_projection(
        self, body_parameters: BodyParameters
    ) -> SphereProjection:
        return SphereProjection(body_parameters.radius)
