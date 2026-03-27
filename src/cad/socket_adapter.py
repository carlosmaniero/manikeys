from __future__ import annotations
import sys
import openscad as osc
from dataclasses import dataclass
from injector import inject, singleton
from context import injector
from models.parameters import Parameters
from openscad_ext.object import OSCObject


fn = 200


@singleton
@inject
@dataclass
class SocketAdapterCAD(OSCObject):
    parameters: Parameters

    @property
    def p(self):
        return self.parameters.socket_adapter

    def diode(self, border: float) -> osc.PyOpenSCAD:
        d = osc.union(
            osc.cylinder(
                h=self.p.diode_l + border,
                r=self.p.diode_r,
                center=True,
                fn=fn,
            ),
            osc.cylinder(
                h=self.p.diode_l * 100,
                r=self.p.diode_wire_r,
                center=True,
                fn=fn,
            ),
        )
        return osc.translate(d, [0, 0, (self.p.diode_l + border) / 2])

    def cherry_mx_hole(self) -> osc.PyOpenSCAD:
        error = 0.01
        hole_r = (1.5 + error) / 2
        hole_l = 500
        distance = 2

        position = [
            [[3.81, 2.54], [3.81 + distance, -1.08]],
            [[-2.54, 5.08], [-2.54 - distance, 1.08]],
        ]

        res = osc.cylinder(h=hole_l, r=2, center=True, fn=fn)

        for p in position:
            h_children = [
                osc.translate(
                    osc.cylinder(r=hole_r, h=1.1, center=True, fn=fn),
                    [point[0], point[1], 0.5 - 0.1],
                )
                for point in p
            ]
            res |= osc.hull(*h_children)

        for p in position:
            for point in p:
                res |= osc.translate(
                    osc.cylinder(h=hole_l, r=hole_r, center=True, fn=fn),
                    [point[0], point[1], 0],
                )

        return res

    def diode_wire_path(self) -> osc.PyOpenSCAD:
        c1 = osc.translate(
            osc.cylinder(h=100, r=self.p.diode_wire_r * 2, center=True, fn=fn),
            [self.p.diode_x, -self.p.cube_size / 2, 0],
        )
        c2 = osc.translate(
            osc.cylinder(h=100, r=self.p.diode_wire_r * 2, center=True, fn=fn),
            [self.p.diode_x, self.p.cube_size / 2, 0],
        )
        return c1 | c2

    def cap_socket(self) -> osc.PyOpenSCAD:
        c = osc.cube(
            [
                self.p.cap_socket_width,
                self.p.cube_size,
                self.p.cap_socket_height,
            ],
            center=True,
        )
        return osc.translate(c, [0, 0, self.p.cap_socket_height / 2 + 1])

    def led_placement(self) -> osc.PyOpenSCAD:
        pcb_radius = 5.05
        pcb_thickness = 3
        led_size = 5
        led_height = 2
        light_path = led_size - 2

        res = osc.cube([led_size, led_size, led_height], center=True)
        res |= osc.cube([light_path, light_path, 200], center=True)
        res |= osc.cylinder(r=pcb_radius, h=pcb_thickness, fn=fn)

        return osc.translate(res, [0, -pcb_radius, 4.5])

    def body(self) -> osc.PyOpenSCAD:
        c = osc.cube(
            [self.p.cube_size, self.p.cube_size, self.p.body_thickness],
            center=True,
        )
        return osc.translate(c, [0, 0, self.p.body_thickness / 2])

    def full_body(self) -> osc.PyOpenSCAD:
        return self.body() | self.cap_socket()

    def assemble(self) -> osc.PyOpenSCAD:
        obj = self.full_body()

        diode_cut = osc.translate(
            osc.rotate(
                self.diode(self.p.border + self.p.offset_fix), [90, 0, 0]
            ),
            [self.p.diode_x, 0, 2.5],
        )

        obj -= diode_cut
        obj -= self.cherry_mx_hole()
        obj -= self.diode_wire_path()
        obj -= self.led_placement()

        return osc.color(obj, "#333333")

    def socket(self) -> osc.PyOpenSCAD:
        size = self.p.cube_size + self.p.cap_socket_height * 2
        c = osc.cube([size, size, self.p.cap_socket_height], center=True)
        return osc.translate(
            c,
            [
                -size / 2,
                -size / 2,
                self.p.body_thickness - self.p.cap_socket_height / 2,
            ],
        )


if __name__ == "__main__":
    adapter = injector.get(SocketAdapterCAD)
    adapter.program(sys.argv)
