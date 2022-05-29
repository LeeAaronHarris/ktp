import matplotlib.pyplot as plt
import numpy as np


class DataVisualiser:

    def __init__(self):
        pass

    def visualiseData(self, data : np.ndarray):
        plt.scatter(data[:, 0], data[:, 1])
        plt.xlabel("PC 1")
        plt.ylabel("PC 2")
        plt.show()