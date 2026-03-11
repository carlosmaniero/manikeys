from context import injector
from cad.cap import CapCAD
from cad.body import BodyCAD
import openscad as osc
import os
from pathlib import Path


def to_absolute_path(filename: str) -> str:
    relative_path = Path(filename)
    absolute_path = relative_path.resolve()
    return str(absolute_path)


def _file_exists(filename: str) -> bool:
    return os.path.isfile(to_absolute_path(filename))


def load_or_build(obj):
    if _file_exists(obj.filename):
        print(f"Loading {to_absolute_path(obj.filename)}")
        return osc.osimport(to_absolute_path(obj.filename))
    print(f"Building {obj.filename} from scratch")
    obj.export()
    return osc.osimport(to_absolute_path(obj.filename))


def main():
    return load_or_build(injector.get(BodyCAD))


if __name__ == "__main__":
    cap_cad = injector.get(CapCAD)
    body = main()
    body |= cap_cad.assembly_grid()
    body -= cap_cad.cap_body_mask_hole()
    body.show()
