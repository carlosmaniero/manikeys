from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from switches.socket.mount.models import MountCavityModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class FullKeyboardAssemblyCAD(ManifoldObject):
    model: MountCavityModel

    def assemble(self) -> manifold3d.Manifold:
        body = (
            self.deps.stls["build/structure/body/shape.stl"]
            - self.deps.stls[
                "build/structure/body/cad/body_cavity_sections.stl"
            ]
            - self.deps.stls[
                "build/assembly/base_plate/cad/masks/base_plate.stl"
            ]
            + self.deps.stls[
                "build/switches/cad/switch_hole_decorator_grid.stl"
            ]
            - self.deps.stls["build/switches/cad/switch_hole_grid.stl"]
            + self.deps.stls[
                "build/switches/cad/switch_decorator_thumb_grid.stl"
            ]
            - self.deps.stls["build/switches/cad/switch_thumb_hole.stl"]
            - self.deps.stls["build/connectors/pogo/cad/cable_path.stl"]
            - self.deps.stls["build/connectors/magnet/cad/snap.stl"]
            - self.deps.stls["build/connectors/rj45/cad/masks/body.stl"]
            + self.deps.stls["build/connectors/rj45/cad/placement.stl"]
            - self.deps.stls["build/connectors/usbc/cad/masks/usbc.stl"]
            + self.deps.stls["build/connectors/usbc/cad/adapter_trimmed.stl"]
            - self.deps.stls[
                "build/components/light_indicator/cad/masks/body.stl"
            ]
            + self.deps.stls[
                "build/components/light_indicator/cad/panel_frame.stl"
            ]
            - self.deps.stls["build/components/oled_096/cad/masks/body.stl"]
            + self.deps.stls["build/components/oled_096/cad/placement.stl"]
            + self.deps.stls["build/structure/body/screws/cad/placement.stl"]
            - self.deps.stls["build/structure/body/screws/cad/hole.stl"]
        )

        return body


if __name__ == "__main__":
    full_keyboard = injector.get(FullKeyboardAssemblyCAD)
    full_keyboard.program(sys.argv)
