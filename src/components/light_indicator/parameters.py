from dataclasses import dataclass


@dataclass
class LedParameters:
    pcb_radius: float = 5.0
    pcb_enty_radius: float = 7.0
    pcb_height: float = 4.0
    pcb_actual_height: float = 2.0
    led_size: float = 5.0
    led_height: float = 1.0

    @property
    def full_height(self) -> float:
        return self.pcb_height + self.led_height
