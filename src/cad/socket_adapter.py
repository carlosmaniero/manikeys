from __future__ import annotations
import sys
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.parameters import Parameters
from manifold_ext.object import ManifoldObject


fn = 200


@singleton
@inject
@dataclass
class SocketAdapterCAD(ManifoldObject):
    parameters: Parameters

    @property
    def p(self):
        return self.parameters.socket_adapter

    def diode(self, border: float) -> manifold3d.Manifold:
        d1 = manifold3d.Manifold.cylinder(
            height=self.p.diode_l + border,
            radius_low=self.p.diode_r,
            center=True,
            circular_segments=fn,
        )
        d2 = manifold3d.Manifold.cylinder(
            height=self.p.diode_l * 100,
            radius_low=self.p.diode_wire_r,
            center=True,
            circular_segments=fn,
        )
        d = d1 + d2
        return d.translate([0, 0, (self.p.diode_l + border) / 2])

    def cherry_mx_hole(self) -> manifold3d.Manifold:
        error = 0.01
        hole_r = (1.5 + error) / 2
        hole_l = 500
        distance = 2

        position = [
            [[3.81, 2.54], [3.81 + distance, -1.08]],
            [[-2.54, 5.08], [-2.54 - distance, 1.08]],
        ]

        res = manifold3d.Manifold.cylinder(
            height=hole_l, radius_low=2.0, center=True, circular_segments=fn
        )

        for p in position:
            h_children = [
                manifold3d.Manifold.cylinder(
                    radius_low=hole_r,
                    height=1.1,
                    center=True,
                    circular_segments=fn,
                ).translate([point[0], point[1], 0.5 - 0.1])
                for point in p
            ]
            # OpenSCAD hull of children
            combined = manifold3d.Manifold.batch_boolean(
                h_children, manifold3d.OpType.Add
            )
            res += combined.hull()

        for p in position:
            for point in p:
                res += manifold3d.Manifold.cylinder(
                    height=hole_l,
                    radius_low=hole_r,
                    center=True,
                    circular_segments=fn,
                ).translate([point[0], point[1], 0])

        return res

    def diode_wire_path(self) -> manifold3d.Manifold:
        c1 = manifold3d.Manifold.cylinder(
            height=100,
            radius_low=self.p.diode_wire_r * 2,
            center=True,
            circular_segments=fn,
        ).translate([self.p.diode_x, -self.p.cube_size / 2, 0])
        c2 = manifold3d.Manifold.cylinder(
            height=100,
            radius_low=self.p.diode_wire_r * 2,
            center=True,
            circular_segments=fn,
        ).translate([self.p.diode_x, self.p.cube_size / 2, 0])
        return c1 + c2

    def cap_socket(self) -> manifold3d.Manifold:
        c = manifold3d.Manifold.cube(
            [
                self.p.cap_socket_width,
                self.p.cube_size,
                self.p.cap_socket_height,
            ],
            center=True,
        )
        return c.translate([0, 0, self.p.cap_socket_height / 2 + 1])

    def led_placement(self) -> manifold3d.Manifold:
        pcb_radius = 5.05
        pcb_thickness = 3
        led_size = 5
        led_height = 2
        light_path = led_size - 2

        res = manifold3d.Manifold.cube(
            [led_size, led_size, led_height], center=True
        )
        res += manifold3d.Manifold.cube(
            [light_path, light_path, 200], center=True
        )
        res += manifold3d.Manifold.cylinder(
            radius_low=pcb_radius, height=pcb_thickness, circular_segments=fn
        )

        return res.translate([0, -pcb_radius, 4.5])

    def body(self) -> manifold3d.Manifold:
        c = manifold3d.Manifold.cube(
            [self.p.cube_size, self.p.cube_size, self.p.body_thickness],
            center=True,
        )
        return c.translate([0, 0, self.p.body_thickness / 2])

    def full_body(self) -> manifold3d.Manifold:
        return self.body() + self.cap_socket()

    def assemble(self) -> manifold3d.Manifold:
        obj = self.full_body()

        diode_cut = (
            self.diode(self.p.border + self.p.offset_fix)
            .rotate([90, 0, 0])
            .translate([self.p.diode_x, 0, 2.5])
        )

        obj -= diode_cut
        obj -= self.cherry_mx_hole()
        obj -= self.diode_wire_path()
        obj -= self.led_placement()

        return obj

    def socket(self) -> manifold3d.Manifold:
        size = self.p.cube_size + self.p.cap_socket_height * 2
        c = manifold3d.Manifold.cube(
            [size, size, self.p.cap_socket_height], center=True
        )
        return c.translate(
            [
                -size / 2,
                -size / 2,
                self.p.body_thickness - self.p.cap_socket_height / 2,
            ]
        )


if __name__ == "__main__":
    adapter = injector.get(SocketAdapterCAD)
    adapter.program(sys.argv)
