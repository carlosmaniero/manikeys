from dataclasses import dataclass
import manifold3d
from components.wire_holder.model import WireHolderModel


@dataclass
class WireHolderBaseCAD:
    model: WireHolderModel

    def create_wire_holder(self, wires: int) -> manifold3d.Manifold:
        structure = manifold3d.Manifold.cube(
            self.model.housing_size(wires),
            center=True,
        )

        holes = []
        for col in range(wires):
            x = self.model.hole_x_position(col, wires)
            hole = manifold3d.Manifold.cylinder(
                height=self.model.hole_height,
                radius_low=self.model.hole_radius,
                circular_segments=100,
                center=True,
            ).translate([x, 0.0, 0.0])
            holes.append(hole)

        holes_manifold = manifold3d.Manifold.batch_boolean(
            holes, manifold3d.OpType.Add
        )
        return structure - holes_manifold
