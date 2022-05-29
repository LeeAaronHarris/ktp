import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer


class UnsupervisedMlHandler:

    def __init__(self):
        pass

    def countWordFrequency(self, data: []):
        # return n-grams
        count_vect = CountVectorizer()
        counts = count_vect.fit_transform(raw_documents=data)
        counts = counts.toarray()
        return counts

    def reduceDimensionality(self, data: np.ndarray, visualise: bool, title: str) -> np.ndarray:
        # transformedData = TSNE(n_components=2, learning_rate='auto',
        #               init='random').fit_transform(X=transformedData)
        # todo: grid search the number of components based on variance; not just 2
        pca = PCA(2).fit(data)
        amountOfPCVariance = pca.explained_variance_ratio_
        transformedData = pca.transform(data)
        if visualise:
            plt.scatter(transformedData[:, 0], transformedData[:, 1])
            plt.xlabel("PC 1 (" + str(amountOfPCVariance[0] * 100)[:5] + "%)")
            plt.ylabel("PC 2 (" + str(amountOfPCVariance[1] * 100)[:5] + "%)")
            plt.title(title)
            plt.show()

        return transformedData

    def getDataClusters(self, data: np.ndarray):
        cluster = KMeans(n_clusters=3).fit(data)  # sensitive to outliers
        predictedDistances = cluster.transform(data)
        predictions = cluster.predict(data)
        return predictions, predictedDistances

    def identifyGroupPercentage(self, data) -> np.ndarray:
        totalDistance = np.sum(data, axis=1, keepdims=True)
        percentages = 100 - (data / totalDistance) * 100
        totalPercentages = np.sum(percentages, axis=1, keepdims=True)
        normalisedPercentages = (percentages / totalPercentages) * 100
        return normalisedPercentages

    # identify which cluster contains the most uses of each word
    # inefficient - we have the counts already - and complex
    def identifyClusterClasses(self, resumes: [{}], clusterPredictions: np.ndarray, classNames: [str]) -> [str]:
        # split resumes according to cluster predictions
        splitResumes = self._splitResumesBasedOnClusterPredictions(resumes, clusterPredictions)

        frequencyOfEachWordInCluster = np.zeros(shape=(len(classNames), len(classNames)))

        for splitIndex, splitResume in enumerate(splitResumes):  # potentially uneven data distribution
            count_vect = CountVectorizer()
            wordFrequencies = count_vect.fit_transform(raw_documents=splitResume)
            wordsPresent = count_vect.get_feature_names_out()
            for indexOfClassWord, classWord in enumerate(classNames):
                locationOfClassword = self._getLocationOfWord(list=wordsPresent, wordToFind=classWord)
                if locationOfClassword is None: continue

                # count how many times the class word appears in the given resumes
                classWordCount = np.sum(wordFrequencies[:, locationOfClassword])
                # 1st example: how much testing appears in the resumes of each cluster
                frequencyOfEachWordInCluster[splitIndex, indexOfClassWord] = classWordCount
        return frequencyOfEachWordInCluster

    def _splitResumesBasedOnClusterPredictions(self, resumes, clusterPredictions) -> []:
        splitResumes = []
        for clusterNumber in range(np.max(clusterPredictions) + 1):
            indices = np.arange(0, len(resumes))[clusterPredictions == clusterNumber]
            splitResumes.append([resumes[index] for index in indices])
        return splitResumes

    def _getLocationOfWord(self, list: [], wordToFind: str) -> int:
        for index, word in enumerate(list):
            if wordToFind == word:
                return index
        return None

    def getClusterClasses(self, clusterFrequencies, classNames):
        # clusterRepresentations = np.argmax(clusterFrequencies, axis = 1) - ties

        clustersTaken = []
        clusterRepresentations = np.zeros(shape=(len(classNames)))
        for classNameIndex in range(len(classNames)):  # a name for each cluster
            frequencies = clusterFrequencies[classNameIndex, :]
            for clusterIndex in clustersTaken:
                frequencies[clusterIndex] = 1
            # remove unavailable indices]
            clusterRepresentations[classNameIndex] = np.argmax(frequencies)
            clustersTaken.append(np.argmax(frequencies))
        return clusterRepresentations