from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.manifold_ext.object import ManifoldObject
from components.wire_holder.model import WireHolderModel
from components.wire_holder.cad.wire_holder_base import WireHolderBaseCAD


@singleton
@inject
@dataclass
class WireHolder7CAD(ManifoldObject):
    model: WireHolderModel

    def assemble(self) -> manifold3d.Manifold:
        base = WireHolderBaseCAD(self.model)
        return base.create_wire_holder(7)


if __name__ == "__main__":
    wire_holder_7 = injector.get(WireHolder7CAD)
    wire_holder_7.program(sys.argv)
