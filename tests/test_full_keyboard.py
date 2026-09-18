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
