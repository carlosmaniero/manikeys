from injector import Injector
from data.parameters import ParametersModule
from data.projection import ProjectionModule
from data.layout import LayoutModule

injector = Injector(
    [
        ParametersModule(),
        ProjectionModule(),
        LayoutModule(),
    ]
)
