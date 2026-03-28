from __future__ import annotations
import os
import subprocess
from typing import Sequence
import openscad as osc  # noqa: F401
from cad.object import Object


class OSCObject(Object["osc.PyOpenSCAD"]):
    def save(self, path: str):
        make_cmd = os.getenv("MAKE", "make")
        subprocess.run(
            [make_cmd, "build_with_pythonscad", f"FILE={path}"], check=True
        )

    def show(self):
        obj = self.assemble()
        obj.show()

    def program(self, argv: Sequence[str]):
        # UGLY HACK: if the first argument is empty, it means that it is inside
        # pythonscad
        if argv[0] == "":
            return self.show()

        parser = self._get_program_parser()
        args = parser.parse_args(argv[1:])

        if args.show:
            subprocess.run(["pythonscad", argv[0]], check=True)
            return

        super().program(argv)
