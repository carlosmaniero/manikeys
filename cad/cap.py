import openscad as osc
from sphere_projection import SphereProjection
from data.parameters import parameters
from data.layout import layout

fn = 20


def outer():
    obj = osc.cube(
        [
            parameters.caps.size + parameters.caps.border * 2,
            parameters.caps.size + parameters.caps.border * 2,
            parameters.caps.outer.thickness,
        ],
        center=True,
    )

    obj += [0, 0, parameters.caps.thickness]
    obj -= [0, 0, parameters.caps.outer.thickness]
    obj = osc.color(obj, "blue")
    obj = obj.fillet(parameters.caps.border / 4, fn=fn)

    return obj


def cap():
    body = outer()

    obj = osc.cube(
        [
            parameters.caps.size,
            parameters.caps.size,
            parameters.caps.thickness + parameters.globals.diff_offset,
        ],
        center=True,
    )
    obj += [0, 0, parameters.caps.thickness / 2]
    obj = osc.color(obj, "red")

    return body - obj


def assembly_grid(projection: SphereProjection):
    length = parameters.caps.size + parameters.caps.gap

    grid = []
    initial_column_position = [0, 0, -projection.radius]

    for column in layout.grid():
        position = initial_column_position
        for index, key in enumerate(column):
            if index == 0:
                position = projection.move_constant_x(
                    position,
                    (key.offsetY - layout.columns[0].offsetY)
                    * parameters.caps.size,
                    direction=1,
                )

            rotation = projection.project_rotation(position)

            grid.append(
                cap().rotate(rotation) + position + [0, 0, projection.radius]
            )

            position = projection.move_constant_x(position, length, direction=1)

        initial_column_position = projection.move_constant_y(
            initial_column_position, length, direction=1
        )

    return osc.union(*grid)
