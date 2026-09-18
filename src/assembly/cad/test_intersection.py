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

    def assemble(self) -> manifold3d.Manifold:
        result = self.shell_main + self.shell_hand + self.hot_swap_v2_grid_shell
        if result.is_empty():
            return load_stl_to_manifold("dist/test_passed.stl")
        return result


if __name__ == "__main__":
    test_intersection = injector.get(IntersectionTestCAD)
    test_intersection.program(sys.argv)
