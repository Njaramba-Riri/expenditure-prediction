from typing import Tuple, Annotated
from rich import print

import numpy as np

from sklearn.model_selection import train_test_split

def split_data(X: np.ndarray, y: np.ndarray, **kwargs) -> Tuple[
    Annotated[np.ndarray, "X_train"],
    Annotated[np.ndarray, "X_test"],
    Annotated[np.ndarray, "y_train"],
    Annotated[np.ndarray, "y_test"]
]:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=True, random_state=42)

    #print(f"X_train: {X_train.shape}\nX_test: {X_test.shape}\ny_train: {y_train.shape}\ny_test: {y_test.shape}")

    return X_train, X_test, y_train, y_test


