import numpy as np
from core.context import injector
from structure.body.models import BodyModel


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
