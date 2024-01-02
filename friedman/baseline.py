import numpy as np

from .lib import integral_transform


def baseline(
    y: np.ndarray, max_iter: int = 100, precision: float = 1e-16
) -> np.ndarray:
    size = len(y)
    precision *= size
    y0 = np.linspace(y[0], y[-1], size)
    s = np.zeros(size, dtype=float)
    w = np.zeros(size, dtype=float)
    for _ in range(max_iter):
        s = integral_transform(y0 - y)
        if np.sum((s - w) ** 2) < precision:
            break
        w = np.copy(s)
        s[:] = (s[:] - np.min(s)) / (np.max(s) - np.min(s))
        y0[:] = s[:] * (np.max(y0) - np.min(y0)) + np.min(y0)
    return y0
