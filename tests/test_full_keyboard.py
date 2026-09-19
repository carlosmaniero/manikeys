from core.context import injector
from assembly.cad.test_intersection import IntersectionTestCAD


def test_full_keyboard_and_shell_main_intersection_is_empty():
    intersection_cad = injector.get(IntersectionTestCAD)
    intersection = intersection_cad.shell_main
    assert intersection.is_empty()


def test_full_keyboard_and_shell_hand_intersection_is_empty():
    intersection_cad = injector.get(IntersectionTestCAD)
    intersection = intersection_cad.shell_hand
    assert intersection.is_empty()


def test_hot_swap_v2_grid_and_shell_intersection_is_empty():
    intersection_cad = injector.get(IntersectionTestCAD)
    intersection = intersection_cad.hot_swap_v2_grid_shell
    assert intersection.is_empty()


def test_cable_matrix_grid_and_shell_intersection_is_empty():
    intersection_cad = injector.get(IntersectionTestCAD)
    intersection = intersection_cad.cable_matrix_grid_shell
    assert intersection.is_empty()


def test_cable_matrix_grid_and_hot_swap_v2_grid_intersection_is_empty():
    intersection_cad = injector.get(IntersectionTestCAD)
    intersection = intersection_cad.cable_matrix_grid_hot_swap_v2_grid
    assert intersection.is_empty()


def test_base_plate_and_keyboard_intersection_is_empty():
    intersection_cad = injector.get(IntersectionTestCAD)
    intersection = intersection_cad.base_plate_keyboard
    assert intersection.is_empty()


def test_base_plate_and_shell_intersection_is_empty():
    intersection_cad = injector.get(IntersectionTestCAD)
    intersection = intersection_cad.base_plate_shell
    assert intersection.is_empty()
