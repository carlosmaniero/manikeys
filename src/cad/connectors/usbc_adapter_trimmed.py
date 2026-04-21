from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from loader import load_many_stl_to_manifold
from models.usbc import USBCModel
from manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class USBCAdapterTrimmedCAD(ManifoldObject):
    model: USBCModel

    def assemble(self) -> manifold3d.Manifold:
        print("Loading STL files...")
        paths = [
            "build/cad/connectors/usbc_adapter.stl",
            "build/cad/body.stl",
        ]
        adapter, body = load_many_stl_to_manifold(paths)
        return adapter ^ body


if __name__ == "__main__":
    adapter_trimmed = injector.get(USBCAdapterTrimmedCAD)
    adapter_trimmed.program(sys.argv)
