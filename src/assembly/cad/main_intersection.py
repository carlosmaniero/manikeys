from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class MainIntersectionCAD(ManifoldObject):
    def assemble(self) -> manifold3d.Manifold:
        full_keyboard = self.deps.stls["build/assembly/cad/full_keyboard.stl"]
        shell_main = self.deps.stls["build/switches/socket/mount/cad/main.stl"]

        return full_keyboard ^ shell_main


if __name__ == "__main__":
    main_intersection = injector.get(MainIntersectionCAD)
    main_intersection.program(sys.argv)
