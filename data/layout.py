from models.layout import Layout, LayoutColumn
from data.parameters import parameters
from models.projection import SphereProjection

projection = SphereProjection(parameters.body.radius)

layout = Layout(
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
    parameters=parameters,
)
