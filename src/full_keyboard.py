from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_many_stl_to_manifold
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
        paths = [
            "build/cad/body.stl",
            "build/cad/body_inner_sections.stl",
            "build/cad/body_screw_placement.stl",
            "build/cad/cap_grid.stl",
            "build/cad/cap_hole_grid.stl",
            "build/cad/cap_thumb.stl",
            "build/cad/cap_thumb_hole.stl",
            "build/cad/cable_path.stl",
            "build/cad/body_screw_hole.stl",
            "build/cad/connectors/rj45_adapter_body_mask.stl",
            "build/cad/connectors/rj45_adapter_front_placement.stl",
            "build/cad/connectors/usbc_mask.stl",
            "build/cad/connectors/usbc_adapter_trimmed.stl",
            "build/cad/magnet_snap.stl",
            "build/cad/components/light_indicator/body_mask.stl",
            "build/cad/components/light_indicator/panel_frame.stl",
            "build/cad/components/oled_096_placement_body_mask.stl",
            "build/cad/components/oled_096_placement.stl",
        ]

        manifolds = load_many_stl_to_manifold(paths)

        (
            body,
            body_inner_sections,
            body_screw_placement,
            cap_grid,
            cap_hole_grid,
            cap_thumb,
            cap_thumb_hole,
            cable_path,
            body_screw_hole,
            rj45_mask,
            rj45_adapter_placement,
            usbc_mask,
            usbc_adapter,
            magnet_snap,
            light_indicator_body_mask,
            light_indicator_panel_frame,
            oled_placement_body_mask,
            oled_placement,
        ) = manifolds

        body = body - body_inner_sections
        body = body + cap_grid
        body = body - cap_hole_grid
        body = body + cap_thumb
        body = body - cap_thumb_hole
        body = body - cable_path
        body = body - magnet_snap

        body = body - rj45_mask
        body = body + rj45_adapter_placement

        body = body - usbc_mask
        body = body + usbc_adapter

        body = body - light_indicator_body_mask
        body = body + light_indicator_panel_frame

        body = body - oled_placement_body_mask
        body = body + oled_placement

        body = body + body_screw_placement
        body = body - body_screw_hole

        return body


if __name__ == "__main__":
    full_keyboard = injector.get(FullKeyboard)
    full_keyboard.program(sys.argv)
