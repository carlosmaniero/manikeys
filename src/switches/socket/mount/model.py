from dataclasses import dataclass
from injector import inject, singleton
from components.arduino_nano_case.model import ArduinoNanoCaseModel
from components.arduino_pro_micro_case.model import ArduinoProMicroCaseModel
from globals.wall.parameters import WallParameters
from structure.body.parameters import BodyParameters
from switches.socket.mount.parameters import PcbsPlacementParameters
from switches.socket.mount.models import (
    MountCavityModel,
    MountScrewCylinderModel,
)


@singleton
@inject
@dataclass
class PcbsPlacementModel:
    parameters: PcbsPlacementParameters
    mount_cavity_model: MountCavityModel
    screw_cylinder_model: MountScrewCylinderModel
    wall_parameters: WallParameters
    body_parameters: BodyParameters
    nano_model: ArduinoNanoCaseModel
    pro_model: ArduinoProMicroCaseModel

    @property
    def main_cavity_start_y(self) -> float:
        divider_size = (
            self.wall_parameters.thickness * 4
            + self.body_parameters.clearance * 2
        )
        return self.mount_cavity_model.divider_y + divider_size / 2

    @property
    def dimensions(self) -> tuple[float, float, float]:
        width = self.mount_cavity_model.width - self.parameters.clearance * 2
        depth = (
            self.mount_cavity_model.end_y()
            - self.main_cavity_start_y
            - self.parameters.clearance * 2
        )
        height = self.parameters.thickness
        return (width, depth, height)

    @property
    def coords(self) -> tuple[float, float, float]:
        x = self.mount_cavity_model.start_x() + self.parameters.clearance
        y = self.main_cavity_start_y + self.parameters.clearance
        z = self.screw_cylinder_model.z - self.parameters.thickness
        return (x, y, z)

    @property
    def cavity_mask_radius(self) -> float:
        return (
            self.screw_cylinder_model.cavity_radius + self.parameters.clearance
        )

    @property
    def cavity_mask_placements(self) -> list[tuple[float, float]]:
        placements = []
        for (
            x,
            y,
        ) in self.screw_cylinder_model.screw_placement_model.main_points:
            center_x = (
                x
                + self.screw_cylinder_model.screw_placement_model.standoff_size
                / 2
            )
            center_y = (
                y
                + self.screw_cylinder_model.screw_placement_model.standoff_size
                / 2
            )
            placements.append((center_x, center_y))
        return placements

    @property
    def inner_cut_dimensions(self) -> tuple[float, float, float]:
        width, depth, height = self.dimensions
        wall = self.parameters.wall_margin
        return (width - wall * 2, depth - wall * 2, height)

    @property
    def inner_cut_center(self) -> tuple[float, float, float]:
        x, y, z = self.coords
        width, depth, height = self.dimensions
        return (x + width / 2, y + depth / 2, z + height / 2)

    @property
    def cases_base_dimensions(self) -> tuple[float, float, float]:
        margin = self.parameters.wall_margin * 2
        width = (
            max(self.pro_model.dimensions[1], self.nano_model.dimensions[1])
            + margin
        )
        depth = (
            self.pro_model.dimensions[0]
            + self.nano_model.dimensions[0]
            + margin
        )
        height = self.parameters.thickness
        return (width, depth, height)

    @property
    def pro_case_coords(self) -> list[float]:
        pro_y_size = self.pro_model.dimensions[0]
        nano_y_size = self.nano_model.dimensions[0]
        arduinos_depth = pro_y_size + nano_y_size

        start_y = self.inner_cut_center[1] - arduinos_depth / 2

        x = self.inner_cut_center[0]
        y = start_y + nano_y_size + pro_y_size / 2
        z = (
            self.coords[2]
            - self.pro_model.dimensions[2] / 2
            - self.parameters.arduinos_offset_z
        )
        return [x, y, z]

    @property
    def nano_case_coords(self) -> list[float]:
        pro_y_size = self.pro_model.dimensions[0]
        nano_y_size = self.nano_model.dimensions[0]
        arduinos_depth = pro_y_size + nano_y_size

        start_y = self.inner_cut_center[1] - arduinos_depth / 2

        x = self.inner_cut_center[0]
        y = start_y + nano_y_size / 2
        z = (
            self.coords[2]
            - self.nano_model.dimensions[2] / 2
            - self.parameters.arduinos_offset_z
        )
        return [x, y, z]

    @property
    def cases_base_center(self) -> tuple[float, float, float]:
        return (
            self.inner_cut_center[0],
            self.inner_cut_center[1],
            self.coords[2]
            + self.parameters.thickness / 2
            - self.parameters.arduinos_offset_z,
        )

    @property
    def path_fillet_radius(self) -> float:
        return self.wall_parameters.fillet

    @property
    def connection_paths_control_points(self) -> list[list[list[float]]]:
        pcb_z = self.coords[2] + self.parameters.thickness / 2
        base_z = self.cases_base_center[2]
        center_x = self.inner_cut_center[0]
        center_y = self.inner_cut_center[1]

        pcb_left_x = center_x - self.inner_cut_dimensions[0] / 2
        pcb_right_x = center_x + self.inner_cut_dimensions[0] / 2
        pcb_front_y = center_y - self.inner_cut_dimensions[1] / 2
        pcb_back_y = center_y + self.inner_cut_dimensions[1] / 2

        half_thick = self.parameters.thickness / 2

        base_left_x = center_x - self.cases_base_dimensions[0] / 2 + half_thick
        base_right_x = center_x + self.cases_base_dimensions[0] / 2 - half_thick
        base_front_y = center_y - self.cases_base_dimensions[1] / 2 + half_thick
        base_back_y = center_y + self.cases_base_dimensions[1] / 2 - half_thick

        fillet_r = self.path_fillet_radius

        left_path = [
            [pcb_left_x, center_y, pcb_z, fillet_r],
            [base_left_x, center_y, pcb_z, fillet_r],
            [base_left_x, center_y, base_z, 0.0],
        ]

        right_path = [
            [pcb_right_x, center_y, pcb_z, fillet_r],
            [base_right_x, center_y, pcb_z, fillet_r],
            [base_right_x, center_y, base_z, 0.0],
        ]

        front_path = [
            [center_x, pcb_front_y, pcb_z, fillet_r],
            [center_x, base_front_y, pcb_z, fillet_r],
            [center_x, base_front_y, base_z, 0.0],
        ]

        back_path = [
            [center_x, pcb_back_y, pcb_z, fillet_r],
            [center_x, base_back_y, pcb_z, fillet_r],
            [center_x, base_back_y, base_z, 0.0],
        ]

        return [left_path, right_path, front_path, back_path]

    @property
    def fillet_radius(self) -> float:
        return self.wall_parameters.fillet
