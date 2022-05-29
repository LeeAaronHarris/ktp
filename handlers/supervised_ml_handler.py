import numpy as np
import pandas as pd


class SupervisedMlHandler:

    # create and return a one-hot encoded matrix of target indicies; random split at the moment
    def createTargetsForData(self, data: [], numberOfTargets: int = 3) -> np.ndarray:
        amountOfData = len(data)
        targets = np.zeros(shape=(amountOfData, numberOfTargets))
        for instanceIndex in range(amountOfData):
            classIndex = np.random.random_integers(0, numberOfTargets - 1)
            targets[instanceIndex, classIndex] = 1  # random class

        return targets

    def assignScoreToEachResume(self, data: np.ndarray, classNames: [str]) -> pd.DataFrame:
        # scale data to percentages
        data = (data / np.sum(data, axis=1, keepdims=True)) * 100
        data = np.round(data, decimals=2)

        indices = ["resume" + str(index + 1) for index in range(len(data))]
        frame = pd.DataFrame(data, index=indices, columns=classNames)
        return frame  # todo
