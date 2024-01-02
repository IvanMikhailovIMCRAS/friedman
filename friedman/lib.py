from typing import Tuple

import numpy as np


def linearization(X: np.ndarray, Y: np.ndarray) -> Tuple[float, float, float]:
    if len(X) != len(Y):
        raise ValueError("linearization: X and Y have different dimension")
    N = len(X)
    denominator = X.dot(X) - X.mean() * X.sum()
    w = (X.dot(Y) - Y.mean() * X.sum()) / denominator
    b = (Y.mean() * X.dot(X) - X.mean() * X.dot(Y)) / denominator
    Yhat = w * X + b
    mse = (Yhat - Y).dot(Yhat - Y) / N
    return (w, b, mse)


def integral_transform(y: np.ndarray) -> np.ndarray:
    s = np.zeros(len(y), dtype=float)
    integral = 0.0
    for i in range(len(y)):
        integral += y[i]
        s[i] = integral
    return s


def bigest_negative_interval(x: np.ndarray) -> Tuple[int, int]:
    indexies = np.where(x < 0.0)[0]
    item = indexies[0]
    first = item
    intervals = []
    for i in indexies:
        if item != i:
            intervals.append([first, item - 1])
            item = i
            first = i
        item += 1
    intervals.append([first, indexies[-1]])
    numbers = [a[1] - a[0] for a in intervals]
    max_value = max(numbers)
    max_index = numbers.index(max_value)
    return tuple(intervals[max_index])
