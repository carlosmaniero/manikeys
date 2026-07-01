from dataclasses import dataclass


@dataclass
class PogoPinParameters:
    body_length: float = 31.00
    body_width: float = 4.50
    body_height: float = 4.00
    flange_thickness: float = 1.00
    mounting_hole_diameter: float = 1.50
    mounting_hole_distance: float = 34.50
    pin_pitch: float = 2.54
    pin_count: int = 9
    magnet_distance: float = 27.00
    pin_height: float = 5.00
    pin_tip_diameter: float = 0.90
    solder_tail_diameter: float = 0.70
    solder_tail_length: float = 1.50
