from unittest.mock import Mock
from models.components.oled_096 import Oled096Model, Oled096PlacementModel
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
    mock_params.wall.thickness = thickness
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
    assert model.lid_pocket == [40.5, 15.5, 5.0]
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


def test_oled_096_placement_position():
    mock_params = create_mock_parameters()
    mock_params.caps.size = 14.0
    mock_params.caps.full_offset = 20.0
    mock_params.wall.thickness = 3.0

    mock_body_model = Mock()
    mock_body_model.highest = 350.0
    mock_body_model.sphere.highest = 350.0
    mock_body_model.bottom_z = -10.0
    mock_body_model.hand_support_end_x = 100.0
    mock_body_model.divider_y = 200.0

    mock_cap_thumb = Mock()
    mock_cap_thumb.body_model = mock_body_model
    mock_cap_thumb.get_positions.return_value = [
        [100.0, 200.0, 300.0],
        [100.0, 180.0, 300.0],
        [100.0, 160.0, 300.0],
    ]

    oled_model = Oled096Model(global_parameters=mock_params)
    model = Oled096PlacementModel(
        global_parameters=mock_params, oled=oled_model, cap_thumb=mock_cap_thumb
    )

    assert model.placement_position == [129.0, 177.0, 347.0]
    assert model.mask_size == [32.5, 36.5, 360.0]
    assert model.mask_coords == [129.0, 174.0, 170.0]
    assert model.shell_mask_size == [35.5, 45.5, 9.0]
    assert model.shell_mask_coords == [129.0, 177.0, 347.0]
