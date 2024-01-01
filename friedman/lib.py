import numpy as np


def integral_transform(y: np.ndarray) -> np.ndarray:
    s = np.zeros(len(y), dtype=float)
    integral = 0.0
    for i in range(len(y)):
        integral += y[i]
        s[i] = integral
    return s
