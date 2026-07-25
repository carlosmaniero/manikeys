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
class RJ11AdapterTrimmedCAD(ManifoldObject):
    def assemble(self) -> manifold3d.Manifold:
        adapter = self.deps.stls["build/connectors/rj11/cad/adapter.stl"]
        body = self.deps.stls["build/structure/body/shape.stl"]
        return adapter ^ body


if __name__ == "__main__":
    adapter_trimmed = injector.get(RJ11AdapterTrimmedCAD)
    adapter_trimmed.program(sys.argv)
