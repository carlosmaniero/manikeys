from dataclasses import dataclass


@dataclass
class ArduinoNanoCaseParameters:
    pcb_width: float = 17.78
    pcb_length: float = 43.18

    screw_height: float = 2.0
    screw_distance: float = 1.27
