from collections import namedtuple
import openscad as osc
from parameter import get_global_parameters
from models.layout import Key

fn = 200

global_parameters = get_global_parameters()

_cap_size = osc.add_parameter("cap_size", 14)
_cap_thickness = osc.add_parameter("cap_thickness", 5)
_cap_border = osc.add_parameter("cap_border", 2.5)
_cap_outer_thickness = osc.add_parameter("cap_outer_thickness", 1.5)


parameters = namedtuple("CAP", ["size", "thickness", "border", "outer"])(
    size=_cap_size,
    thickness=_cap_thickness,
    border=_cap_border,
    outer=namedtuple("OUTER", ["thickness"])(thickness=_cap_outer_thickness),
)


def outer():
    obj = osc.cube(
        [
            parameters.size + parameters.border * 2,
            parameters.size + parameters.border * 2,
            parameters.outer.thickness,
        ],
        center=True,
    )

    obj += [0, 0, parameters.thickness]
    obj -= [0, 0, parameters.outer.thickness]
    obj = osc.color(obj, "blue")
    obj = obj.fillet(parameters.border / 4, fn=fn)

    return obj


def cap(key: Key = Key(col=0, row=0, offsetY=0)):
    body = outer()

    obj = osc.cube(
        [
            parameters.size,
            parameters.size,
            parameters.thickness + global_parameters.diff_offset,
        ],
        center=True,
    )
    obj += [0, 0, parameters.thickness / 2]
    obj = osc.color(obj, "red")

    return body - obj
