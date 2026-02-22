from collections import namedtuple
import openscad as osc


def get_global_parameters():
    return namedtuple("PARAMETERS", ["diff_offset"])(
        diff_offset=osc.add_parameter(
            "diff_offset",
            0.5,
            description="(set zero for final render) adds an extra offset to the difference operation to prevent rendering issues",
        )
    )
