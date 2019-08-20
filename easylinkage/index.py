# -*- coding: utf-8 -*-

from recordlinkage import Index as BaseIndex
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import MiniBatchKMeans

class Index(BaseIndex):
        
    @staticmethod
    def _join(v):
        v = [x for x in v if str(x) != "nan"]
        return " ".join(v)

    def _ngram_vectorize(self, df, cols, n):
        dfm = df[cols].apply(self._join, axis=1)
        vectorizer = CountVectorizer(analyzer = "char", ngram_range = (1,n))
        vectorizer.fit(dfm)
        X = vectorizer.transform(dfm).toarray()
        return vectorizer, X

    @staticmethod
    def _clustering(X, k):
        kmeans = MiniBatchKMeans(n_clusters = k, random_state = 42)
        kmeans.fit(X)
        clusters = kmeans.predict(X)
        return kmeans, clusters

    def _partition_target(self, df, cols, n, k):
        vectorizer, X = self._ngram_vectorize(df, cols, n)
        kmeans, clusters = self._clustering(X, k)
        df["partition"] = clusters
        return df, vectorizer, kmeans
    
    def _partition_query(self, df, cols, vectorizer, kmeans):
        dfm = df[cols].apply(self._join, axis=1)
        X = vectorizer.transform(dfm).toarray()
        clusters = kmeans.predict(X)
        df["partition"] = clusters
        return df

    def _partition(self, dfq, dft, colsq, colst, ngrams, k):
        dft, vectorizer, kmeans = self._partition_target(dft, colst, ngrams, k)
        dfq = self._partition_query(dfq, colsq, vectorizer, kmeans)
        return dfq, dft
        
    def softblock(self, left_on, right_on, ngrams = 2, k = 5):
        assert not hasattr(self, "do_softblock"), "You can only softblock once... Try using lists on left_on and right_on arguments."
        if isinstance(left_on, str): left_on = [left_on]
        if isinstance(right_on, str): right_on = [right_on]
        self.ngrams = ngrams
        self.k = k
        self.softblock_left_on = left_on
        self.softblock_right_on = right_on
        self.block(left_on = "partition", right_on = "partition")
        self.do_softblock = True
    
    def index(self, x, x_link):
        x = x.copy()
        x_link = x_link.copy()
        if hasattr(self, "do_softblock"):
            x, x_link = self._partition(x, x_link,
                                        self.softblock_left_on, self.softblock_right_on,
                                        self.ngrams, self.k)
        return super().index(x, x_link)