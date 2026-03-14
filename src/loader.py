from __future__ import annotations
import subprocess
import openscad as osc
from pathlib import Path


def load_stl(path: str) -> osc.PyOpenSCAD:
    subprocess.run(["make", path], check=True)
    absolute_path = str(Path(path).resolve())
    return osc.osimport(absolute_path)
