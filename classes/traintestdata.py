from numpy import ndarray
from typing import Any
import numpy as np
from sklearn.model_selection import train_test_split  # type: ignore


class TrainTestData:
    def __init__(
        self,
        X_train: ndarray[Any, Any],
        X_test: ndarray[Any, Any],
        y_train: ndarray[Any, Any],
        y_test: ndarray[Any, Any],
    ):
        self.X_train = X_train
        self.X_test = X_test

        self.y_train = y_train
        self.y_test = y_test


def banknote_data(*, test_size: float = 0.25) -> TrainTestData:
    banknote = np.genfromtxt(
        r"banknote/data/banknote.txt",
        delimiter=",",
        dtype=str,
    )

    banknote_X = banknote[:, :-1].astype(float)
    banknote_y = banknote[:, -1]

    data = TrainTestData(
        *train_test_split(banknote_X, banknote_y, test_size=test_size),
    )
    return data
