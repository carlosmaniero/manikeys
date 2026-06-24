from unittest.mock import Mock
from models.components.oled_096 import Oled096Model
from models.parameters import Oled096Parameters


class Oled096ParametersStub(Oled096Parameters):
    def __init__(self, clearance: float = 0.5):
        self._clearance = clearance

    @property
    def pcb(self) -> list[float]:
        return [20, 30, 1]

    @property
    def panel(self) -> list[float]:
        return [10, 15, 1.5]

    @property
    def clearance(self) -> float:
        return self._clearance

    @property
    def screw_hole_offset(self) -> float:
        return 2.0

    @property
    def screw_hole_depth(self) -> float:
        return 1.0

    @property
    def cable_clearance(self) -> list[float]:
        return [10.0, 2.0]


def create_mock_parameters(
    thickness: float = 5.0, clearance: float = 0.5, oled096=None
) -> Mock:
    mock_params = Mock()
    mock_params.oled096 = oled096 or Oled096ParametersStub(clearance=clearance)
    mock_params.body.thickness = thickness
    return mock_params


def test_oled_096_body():
    mock_params = create_mock_parameters()
    model = Oled096Model(global_parameters=mock_params)

    assert model.pcb_pocket == [20.5, 30.5, 6.5]
    assert model.body == [40.5, 50.5, 8.0]
    assert model.pcb_pocket_coords == [0.0, 0.0, -0.75]
    assert model.panel_pocket == [10.5, 15.5, 2.0]
    assert model.panel_pocket_coords == [0.0, 0.0, 3.25]
    assert model.screw_holes_translation == [-20.25, 0.0, 0.0]
    assert model.cable_clearance == [10.0, 2.0, 6.5]
    assert model.cable_clearance_coords == [0.0, 16.25, -0.75]
    assert model.lid_pocket == [40.5, 15.0, 5.0]
    assert model.lid_pocket_coords == [0.0, 0.0, -1.5]


def test_oled_096_screw_holes():
    mock_params = create_mock_parameters(clearance=0)
    model = Oled096Model(global_parameters=mock_params)

    assert model.screw_holes == [
        [2.0, 0, 1.75],
        [38.0, 0, 1.75],
    ]


def test_oled_096_cable_clearance():
    mock_params = create_mock_parameters(clearance=0)
    model = Oled096Model(global_parameters=mock_params)

    assert model.cable_clearance == [10.0, 2.0, 6.0]
    assert model.cable_clearance_coords == [0.0, 16.0, -0.75]
