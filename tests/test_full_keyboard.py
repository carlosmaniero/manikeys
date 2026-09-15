from core.loader import load_stl_to_manifold


def test_full_keyboard_and_shell_main_intersection_is_empty():
    full_keyboard = load_stl_to_manifold("build/assembly/cad/full_keyboard.stl")
    shell_main = load_stl_to_manifold(
        "build/switches/socket/mount/cad/main.stl"
    )

    intersection = full_keyboard ^ shell_main
    assert intersection.is_empty() or abs(intersection.volume()) < 1e-4


def test_full_keyboard_and_shell_hand_intersection_is_empty():
    full_keyboard = load_stl_to_manifold("build/assembly/cad/full_keyboard.stl")
    shell_hand = load_stl_to_manifold(
        "build/switches/socket/mount/cad/hand.stl"
    )

    intersection = full_keyboard ^ shell_hand
    assert intersection.is_empty() or abs(intersection.volume()) < 1e-4
