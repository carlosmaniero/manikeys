from models.layout import Layout, LayoutColumn

layout = Layout(
    columns=[
        LayoutColumn(keys=5, offsetY=0),
        LayoutColumn(keys=5, offsetY=0),
        LayoutColumn(keys=5, offsetY=0.25),
        LayoutColumn(keys=5, offsetY=0.5),
        LayoutColumn(keys=5, offsetY=0.25),
        LayoutColumn(keys=4, offsetY=0),
        LayoutColumn(keys=3, offsetY=0),
    ]
)
