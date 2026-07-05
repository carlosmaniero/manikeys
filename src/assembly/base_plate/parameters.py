from dataclasses import dataclass


@dataclass
class BasePlateParameters:
    screw_height: float = 2.0
    cable_path_rows: int = 7
