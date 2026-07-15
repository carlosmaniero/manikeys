import numpy as np
from core.context import injector
from structure.body.models import BodyModel, BodyInnerModel


def test_body_model_properties():
    body_model = injector.get(BodyModel)
    assert body_model is not None

    assert body_model.start_x() < body_model.end_x()
    assert body_model.start_y() < body_model.end_y()
    assert body_model.width == body_model.end_x() - body_model.start_x()
    assert body_model.depth == body_model.end_y() - body_model.start_y()
    assert body_model.bottom_z == -body_model.body_parameters.height


def test_body_model_z():
    body_model = injector.get(BodyModel)
    x = np.array([0.0, 10.0])
    y = np.array([0.0, -10.0])
    z = body_model.z(x, y)
    assert isinstance(z, np.ndarray)
    assert len(z) == 2


def test_body_wall_thickness_uniform():
    body_model = injector.get(BodyModel)
    inner_model = injector.get(BodyInnerModel)
    x_min = (
        max(body_model.start_x(), inner_model.start_x())
        + body_model.wall_parameters.fillet
    )
    x_max = min(body_model.divider_x_main, inner_model.divider_x_main)
    y_min = body_model.sphere.start_y() + body_model.wall_parameters.fillet
    y_max = (
        min(body_model.end_y(), inner_model.end_y())
        - body_model.wall_parameters.fillet
    )
    x_coords = np.random.uniform(x_min, x_max, 100)
    y_coords = np.random.uniform(y_min, y_max, 100)
    z_outer = body_model.z(x_coords, y_coords)
    z_inner = inner_model.z(x_coords, y_coords)
    diffs = z_outer - z_inner
    np.testing.assert_allclose(diffs, 3.0, rtol=1e-5)
