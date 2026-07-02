from dataclasses import dataclass, field


@dataclass
class Oled096Parameters:
    display_height: float = 1.5
    pcb: list[float] = field(default_factory=lambda: [24.7, 27.0, 1.5])
    panel: list[float] = field(default_factory=lambda: [24.74, 16.9, 1.5])
    clearance: float = 0.5
    screw_hole_offset: float = 2.0
    flat_cable_clearance: float = 0.25
    flat_cable_width: float = 9.0
    cable_clearance: list[float] = field(default_factory=lambda: [10.0, 2.0])
