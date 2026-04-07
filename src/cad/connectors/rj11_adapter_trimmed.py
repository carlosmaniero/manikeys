from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_many_stl_to_manifold
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class RJ11AdapterTrimmedCAD(ManifoldObject):
    def assemble(self) -> manifold3d.Manifold:
        print("Loading STL files...")
        paths = [
            "build/cad/connectors/rj11_adapter.stl",
            "build/cad/body.stl",
        ]
        adapter, body = load_many_stl_to_manifold(paths)
        return adapter ^ body


if __name__ == "__main__":
    adapter_trimmed = injector.get(RJ11AdapterTrimmedCAD)
    adapter_trimmed.program(sys.argv)
