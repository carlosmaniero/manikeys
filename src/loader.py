from __future__ import annotations
import openscad as osc
from pathlib import Path


def load_stl(path: str) -> osc.PyOpenSCAD:
    absolute_path = str(Path(path).resolve())

    if not Path(absolute_path).exists():
        raise FileNotFoundError(f"STL file not found: {absolute_path}")

    return osc.osimport(absolute_path)
