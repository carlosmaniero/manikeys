from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from core.context import injector
from core.loader import load_stl_to_manifold
from core.manifold_ext.object import ManifoldObject


@singleton
@inject
@dataclass
class IntersectionTestCAD(ManifoldObject):
    __test__ = False

    @property
    def shell_main(self) -> manifold3d.Manifold:
        path = "build/switches/socket/mount/cad/main.stl"
        full_keyboard_path = "build/assembly/cad/full_keyboard.stl"

        full_keyboard = (
            self.deps.stls[full_keyboard_path]
            if full_keyboard_path in self.deps.stls
            else load_stl_to_manifold(full_keyboard_path)
        )
        shell_main = (
            self.deps.stls[path]
            if path in self.deps.stls
            else load_stl_to_manifold(path)
        )

        return full_keyboard ^ shell_main

    @property
    def shell_hand(self) -> manifold3d.Manifold:
        path = "build/switches/socket/mount/cad/hand.stl"
        full_keyboard_path = "build/assembly/cad/full_keyboard.stl"

        full_keyboard = (
            self.deps.stls[full_keyboard_path]
            if full_keyboard_path in self.deps.stls
            else load_stl_to_manifold(full_keyboard_path)
        )
        shell_hand = (
            self.deps.stls[path]
            if path in self.deps.stls
            else load_stl_to_manifold(path)
        )

        return full_keyboard ^ shell_hand

    @property
    def hot_swap_v2_grid_shell(self) -> manifold3d.Manifold:
        hot_swap_path = "build/switches/socket/cad/hot_swap_v2_grid.stl"
        shell_path = "build/switches/socket/mount/cad/shell.stl"

        hot_swap_v2_grid = (
            self.deps.stls[hot_swap_path]
            if hot_swap_path in self.deps.stls
            else load_stl_to_manifold(hot_swap_path)
        )
        shell = (
            self.deps.stls[shell_path]
            if shell_path in self.deps.stls
            else load_stl_to_manifold(shell_path)
        )

        return hot_swap_v2_grid ^ shell

    @property
    def cable_matrix_grid_shell(self) -> manifold3d.Manifold:
        matrix_path = (
            "build/switches/cad/switch_hole_decorator_cable_matrix_grid.stl"
        )
        shell_path = "build/switches/socket/mount/cad/shell.stl"

        cable_matrix_grid = (
            self.deps.stls[matrix_path]
            if matrix_path in self.deps.stls
            else load_stl_to_manifold(matrix_path)
        )
        shell = (
            self.deps.stls[shell_path]
            if shell_path in self.deps.stls
            else load_stl_to_manifold(shell_path)
        )

        return cable_matrix_grid ^ shell

    @property
    def cable_matrix_grid_hot_swap_v2_grid(self) -> manifold3d.Manifold:
        matrix_path = (
            "build/switches/cad/switch_hole_decorator_cable_matrix_grid.stl"
        )
        hot_swap_path = "build/switches/socket/cad/hot_swap_v2_grid.stl"

        cable_matrix_grid = (
            self.deps.stls[matrix_path]
            if matrix_path in self.deps.stls
            else load_stl_to_manifold(matrix_path)
        )
        hot_swap_v2_grid = (
            self.deps.stls[hot_swap_path]
            if hot_swap_path in self.deps.stls
            else load_stl_to_manifold(hot_swap_path)
        )

        return cable_matrix_grid ^ hot_swap_v2_grid

    @property
    def base_plate_keyboard(self) -> manifold3d.Manifold:
        base_plate_path = "build/assembly/base_plate/cad/base_plate.stl"
        full_keyboard_path = "build/assembly/cad/full_keyboard.stl"

        base_plate = (
            self.deps.stls[base_plate_path]
            if base_plate_path in self.deps.stls
            else load_stl_to_manifold(base_plate_path)
        )
        full_keyboard = (
            self.deps.stls[full_keyboard_path]
            if full_keyboard_path in self.deps.stls
            else load_stl_to_manifold(full_keyboard_path)
        )

        return base_plate ^ full_keyboard

    @property
    def base_plate_shell(self) -> manifold3d.Manifold:
        base_plate_path = "build/assembly/base_plate/cad/base_plate.stl"
        shell_path = "build/switches/socket/mount/cad/shell.stl"

        base_plate = (
            self.deps.stls[base_plate_path]
            if base_plate_path in self.deps.stls
            else load_stl_to_manifold(base_plate_path)
        )
        shell = (
            self.deps.stls[shell_path]
            if shell_path in self.deps.stls
            else load_stl_to_manifold(shell_path)
        )

        return base_plate ^ shell

    def assemble(self) -> manifold3d.Manifold:
        result = (
            self.shell_main
            + self.shell_hand
            + self.hot_swap_v2_grid_shell
            + self.cable_matrix_grid_shell
            + self.cable_matrix_grid_hot_swap_v2_grid
            + self.base_plate_keyboard
            + self.base_plate_shell
        )
        if result.is_empty():
            return load_stl_to_manifold("dist/test_passed.stl")
        return result


if __name__ == "__main__":
    test_intersection = injector.get(IntersectionTestCAD)
    test_intersection.program(sys.argv)
