import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import itertools
import os

import warnings
warnings.filterwarnings("always")


def run(fold):
    train = pd.read_csv("Datasets/train.csv")
    test = pd.read_csv("Datasets/test.csv")

    train.head(2)


if __name__ == '__main__':
    run()