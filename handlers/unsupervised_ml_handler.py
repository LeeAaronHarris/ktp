import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA


class UnsupervisedMlHandler:

    def __init__(self):
        pass

    def countWordFrequency(self, data : []):
        #return n-grams
        count_vect = CountVectorizer()
        counts = count_vect.fit_transform(raw_documents= data)
        counts = counts.toarray()
        return counts

    def reduceDimensionality(self, data : np.ndarray) -> np.ndarray:
        # transformedData = TSNE(n_components=2, learning_rate='auto',
        #               init='random').fit_transform(X=transformedData)
        # todo: grid search the number of components based on variance; not just 2
        pca = PCA(2).fit(data)
        #amountOfPCVariance = pca.explained_variance_ratio_
        transformedData = pca.transform(data)
        return transformedData