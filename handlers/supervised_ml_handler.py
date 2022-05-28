import numpy as np

class SupervisedMlHandler:

    # create and return a one-hot encoded matrix of target indicies; random split at the moment
    def createTargetsForData(self, data : [], numberOfTargets:int = 3) -> np.ndarray:
        amountOfData = len(data)
        targets = np.zeros(shape = (amountOfData, numberOfTargets))
        for instanceIndex in range(amountOfData):
            classIndex = np.random.random_integers(0, numberOfTargets - 1)
            targets[instanceIndex, classIndex] = 1 # random class

        return targets