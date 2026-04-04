from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_stl_to_manifold
from models.parameters import Parameters
from models.socket_placement import SocketPlacementInner
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class FullKeyboard(ManifoldObject):
    model: SocketPlacementInner
    parameters: Parameters

    def assemble(self) -> manifold3d.Manifold:
        body = load_stl_to_manifold("build/cad/body.stl")
        body = body - load_stl_to_manifold("build/cad/body_inner_sections.stl")
        body = body + load_stl_to_manifold("build/cad/body_screw_placement.stl")

        socket_shell = load_stl_to_manifold(
            "build/cad/socket_placement_shell.stl"
        )
        screw_mask = load_stl_to_manifold("build/cad/body_screw_mask.stl")

        body = body + (socket_shell - screw_mask)

        body = body + load_stl_to_manifold("build/cad/cap_grid.stl")
        body = body - load_stl_to_manifold("build/cad/cap_hole_grid.stl")
        body = body + load_stl_to_manifold("build/cad/cap_thumb.stl")
        body = body - load_stl_to_manifold("build/cad/cap_thumb_hole.stl")
        body = body - load_stl_to_manifold("build/cad/cable_path.stl")
        body = body - load_stl_to_manifold("build/cad/body_screw_hole.stl")
        body = body - load_stl_to_manifold("build/cad/logo.stl")

        return body


if __name__ == "__main__":
    full_keyboard = injector.get(FullKeyboard)
    full_keyboard.program(sys.argv)
