from __future__ import annotations
import subprocess
from typing import Sequence
import openscad as osc  # noqa: F401
from cad.object import Object


class OSCObject(Object["osc.PyOpenSCAD"]):
    def save(self, path: str):
        subprocess.run(
            ["make", "build_with_pythonscad", f"FILE={path}"], check=True
        )

    def show(self):
        obj = self.assemble()
        obj.show()

    def program(self, argv: Sequence[str]):
        # UGLY HACK: if the first argument is empty, it means that it is inside
        # pythonscad
        if argv[0] == "":
            return self.show()
        super().program(argv)
