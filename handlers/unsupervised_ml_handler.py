from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE


class UnsupervisedMlHandler:

    def __init__(self):
        pass

    def count(self, data : []):
        pass
    #     count_vect = CountVectorizer()
    #     counts = count_vect.fit_transform(raw_documents= data)
    #     print(counts)
    #     return counts
    #
    # X_embedded = TSNE(n_components=3, learning_rate='auto',
    #                   init='random').fit_transform(X=[skill_counts, qualification_counts, jobs_counts])