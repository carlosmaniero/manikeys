from injector import Module, provider, singleton
from models.body import LegacyBodyModel, BodyThumbSection
from models.layout import Layout
from models.parameters import Parameters


class BodyModule(Module):
    @singleton
    @provider
    def provide_thumb_section(
        self, layout: Layout, parameters: Parameters
    ) -> BodyThumbSection:
        return BodyThumbSection(layout=layout, parameters=parameters)

    @singleton
    @provider
    def provide_body_model(
        self,
        layout: Layout,
        parameters: Parameters,
        thumb_section: BodyThumbSection,
    ) -> LegacyBodyModel:
        return LegacyBodyModel(
            layout=layout, parameters=parameters, thumb_section=thumb_section
        )
