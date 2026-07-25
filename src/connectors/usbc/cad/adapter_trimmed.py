from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_many_stl_to_manifold
from connectors.usbc.model import USBCModel
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class USBCAdapterTrimmedCAD(ManifoldObject):
    model: USBCModel

    def assemble(self) -> manifold3d.Manifold:
        adapter = self.deps.stls["build/connectors/usbc/cad/adapter.stl"]
        body = self.deps.stls["build/structure/body/shape.stl"]
        return adapter ^ body


if __name__ == "__main__":
    adapter_trimmed = injector.get(USBCAdapterTrimmedCAD)
    adapter_trimmed.program(sys.argv)
