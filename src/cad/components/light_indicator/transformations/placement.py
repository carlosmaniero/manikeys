from __future__ import annotations
import manifold3d
from dataclasses import dataclass
from injector import inject, singleton
from models.components.light_indicator.main_body import MainBodyModel
from models.body import BodyModel
from models.parameters import Parameters


@singleton
@inject
@dataclass
class LightIndicatorPlacement:
    parameters: Parameters
    indicator_model: MainBodyModel
    body_model: BodyModel

    def position_on_the_body(
        self, body: manifold3d.Manifold
    ) -> manifold3d.Manifold:
        r = self.indicator_model.body_depth / 2
        height = self.indicator_model.margin_thickness * 2

        return (
            body.translate(
                [
                    (self.indicator_model.left_edge) / 2 - r * 2,
                    0,
                    0,
                ]
            )
            .rotate([0, 0, 90])
            .translate(
                [
                    self.body_model.start_fixed_x + 12,
                    self.body_model.end_y()
                    - self.parameters.body.fillet
                    - self.parameters.body.thickness,
                    self.body_model.highest - height / 2,
                ]
            )
        )
