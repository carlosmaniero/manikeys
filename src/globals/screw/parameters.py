from dataclasses import dataclass


@dataclass
class ScrewParameters:
    # m1
    m1_diameter: float = 0.95
    m1_5_diameter: float = 1.45
    
    # m2
    m2_diameter: float = 1.9
    m2_length: float = 8.0
    m2_head_diameter: float = 4.0
    m2_head_height: float = 2.0
    m2_5_diameter: float = 2.45
    
    # m3
    m3_diameter: float = 2.9
    
    # m4
    m4_diameter: float = 3.9

    # depths
    depth_short: float = 2.0
    depth_middle: float = 3.0
    depth_large: float = 4.0
