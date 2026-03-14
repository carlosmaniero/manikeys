from typing import Callable
import numpy as np
import numpy.typing as npt


def map_meshgrid(
    xrange: npt.NDArray[np.float64],
    yfn: Callable[[float], npt.NDArray[np.float64]],
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """
    Creates a coordinate grid where Y is calculated for each X.
    """
    xrng = np.asanyarray(xrange)
    yrange = np.array([yfn(x) for x in xrng])
    x = np.broadcast_to(xrng[:, None], yrange.shape)
    y = yrange

    return x, y
