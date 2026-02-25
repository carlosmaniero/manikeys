from injector import Module, provider, singleton
from models.parameters import Parameters
from models.projection import SphereProjection
from models.layout import Layout, LayoutColumn


class LayoutModule(Module):
    @singleton
    @provider
    def provide_layout(
        self, parameters: Parameters, projection: SphereProjection
    ) -> Layout:
        return Layout.from_spherical_projection(
            columns=[
                LayoutColumn(keys=3, offsetY=2),
                LayoutColumn(keys=4, offsetY=1),
                LayoutColumn(keys=5, offsetY=0),
                LayoutColumn(keys=5, offsetY=0.25),
                LayoutColumn(keys=5, offsetY=0.5),
                LayoutColumn(keys=5, offsetY=0.25),
                LayoutColumn(keys=5, offsetY=0),
            ],
            projection=projection,
            cap=parameters.caps,
        )
