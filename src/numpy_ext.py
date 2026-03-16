from typing import Callable
import numpy as np
import numpy.typing as npt


def map_meshgrid(
    xrng: npt.NDArray[np.float64],
    yfn: Callable[[npt.NDArray[np.float64]], npt.NDArray[np.float64]],
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    y = yfn(xrng)
    x = np.broadcast_to(xrng[:, None], y.shape)

    return x, y
