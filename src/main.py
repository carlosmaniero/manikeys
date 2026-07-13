from __future__ import annotations
import sys
from typing import Iterator
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_many_stl_to_trimesh
from core.trimesh_ext.object import TrimeshObject
import trimesh


@singleton
@inject
@dataclass
class Keyboard(TrimeshObject):
    def assemble(self) -> Iterator[trimesh.Trimesh]:
        paths = [
            "build/assembly/cad/full_keyboard.stl",
            "build/assembly/base_plate/cad/base_plate.stl",
            "build/switches/socket/mount/cad/shell.stl",
            "build/switches/socket/cad/hot_swap_grid.stl",
            "build/switches/cad/keycap_grid.stl",
            "build/connectors/rj11/cad/rj11.stl",
            "build/connectors/rj11/cad/adapter_trimmed.stl",
        ]
        (
            body_part,
            bottom,
            socket_shell,
            sockets,
            switches,
            rj11,
            rj11_adapter,
        ) = load_many_stl_to_trimesh(paths)

        def hex_to_rgba(hex_str: str) -> list[int]:
            hex_str = hex_str.lstrip("#")
            return [int(hex_str[i : i + 2], 16) for i in (0, 2, 4)] + [255]

        body_part.visual.face_colors = hex_to_rgba("#ffb89b")
        bottom.visual.face_colors = hex_to_rgba("#c0b89b")
        socket_shell.visual.face_colors = hex_to_rgba("#c0b89b")
        sockets.visual.face_colors = hex_to_rgba("#c0b89b")
        switches.visual.face_colors = hex_to_rgba("#bec0b1")
        rj11.visual.face_colors = hex_to_rgba("#5a5a5a")
        rj11_adapter.visual.face_colors = hex_to_rgba("#c0b89b")

        yield body_part
        yield bottom
        yield socket_shell
        yield sockets
        yield switches
        yield rj11
        yield rj11_adapter


if __name__ == "__main__":
    keyboard = injector.get(Keyboard)
    keyboard.program(sys.argv)
