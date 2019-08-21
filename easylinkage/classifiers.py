from recordlinkage.classifiers import FellegiSunter, SKLearnAdapter, Classifier
from easylinkage.utils.nb_sklearn import ECM
import pandas as pd
import numpy as np
import collections
import random
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer

class BaseECMClassifier(FellegiSunter, SKLearnAdapter, Classifier):

    def __init__(self,
                 init='jaro',
                 binarize=None,
                 max_iter=100,
                 atol=10e-5,
                 use_col_names=True,
                 *args, **kwargs):
        super(BaseECMClassifier, self).__init__(
            use_col_names=use_col_names
        )

        self.kernel = ECM(
            init=init,
            binarize=binarize,
            max_iter=max_iter,
            atol=atol, *args, **kwargs
        )

    def fit(self, X, *args, **kwargs):
        __doc__ = Classifier.__doc__  # noqa

        if isinstance(X, pd.DataFrame):
            self._column_labels = X.columns.tolist()

        Classifier.fit(self, X, *args, **kwargs)

    @property
    def algorithm(self):
        # Deprecated
        raise AttributeError(
            "This attribute is deprecated. Use 'classifier' instead.")


class ECMClassifier(BaseECMClassifier):
        
    @staticmethod
    def _numerically_correct(df):
        correction = np.identity(df.shape[1])
        n = df.index.levels[0][-1] + 1
        mindex = []
        for i in range(n, n + df.shape[1]):
            mindex += [(n, i)]
        mindex = pd.MultiIndex.from_tuples(mindex)
        df = pd.concat([df, pd.DataFrame(correction, columns=df.columns, index = mindex).astype(int)])
        return df
    
    @staticmethod
    def _drop_duplicated_columns(df):
        def get_dups(df):
            dup = set()
            for x in range(df.shape[1]):
                col = df.iloc[:, x]
                for y in range(x + 1, df.shape[1]):
                    otherCol = df.iloc[:, y]
                    if col.equals(otherCol):
                        dup.add(df.columns.values[y])
            return list(dup)
        return df.drop(columns = get_dups(df))

    def _fit_binarize(self, df, min_sim = 0.5):
        bincols = set([col for col in df if df[col].dropna().value_counts().index.isin([0,1]).all()])
        min_sim = np.max([min_sim, 0.5])
        self.fit_cuts = {}
        for col in df.columns:
            if col in bincols: continue
            N = len(df.index.levels[0])
            cutm = df[col].sort_values(ascending = False)[N]
            cutm = np.max([cutm, min_sim])
            interval = (1 - cutm) / 2
            cuth = cutm + interval
            cutl = cutm - interval
            cuts = sorted(set([cutl, cutm, cuth]))
            for i, cut in enumerate(cuts):
                newcol = col + ".%d" %i
                df[newcol] = 0
                df.loc[df[col] >= cut, [newcol]] = 1
                self.fit_cuts[(col, newcol)] = cut
            df.drop(col, axis = 1, inplace = True)
        df = df.astype(int)
        return df
                
    def _predict_binarize(self, df):
        cols = set()
        for c, cut in self.fit_cuts.items():
            col = c[0]
            cols.update([col])
            newcol = c[1]
            df[newcol] = 0
            df.loc[df[col] >= cut, [newcol]] = 1
        df.drop(list(cols), axis = 1, inplace = True)
        return df.astype(int)
        
    def _fit_preprocess(self, df):
        self.raw_fit_columns = df.columns
        # Impute with the mode
        X = np.array(df)
        self.imp = SimpleImputer(strategy = "most_frequent")
        self.imp.fit(X)
        X = self.imp.transform(X)
        # Scale from 0 to 1
        self.sc = MinMaxScaler()
        self.sc.fit(X)
        X = self.sc.transform(X)
        # New dataframe
        df = pd.DataFrame(X, columns = df.columns, index = df.index)
        # Binarize
        df = self._fit_binarize(df)
        # Remove constant columns
        df = df.loc[:, (df != df.iloc[0]).any()]
        # Remove duplicated columns
        df = self._drop_duplicated_columns(df)
        # Save columns to eventually predict
        self.fit_columns = df.columns
        # Numerically correct
        df = self._numerically_correct(df)
        return df
    
    def _predict_preprocess(self, df):
        # Impute with the mode
        X = np.array(df)
        X = self.imp.transform(X)
        # Scale from 0 to 1
        x = self.sc.transform(X)
        # New dataframe
        df = pd.DataFrame(X, columns = df.columns, index = df.index)
        # Binarize
        df = self._predict_binarize(df)
        # Get relevant columns
        df = df[self.fit_columns]
        return df
            
    def fit(self, comparison_vectors):
        dfc = comparison_vectors
        dfc = self._fit_preprocess(dfc)
        super().fit(dfc)
    
    def fit_predict(self, comparison_vectors):
        dfc = comparison_vectors
        self.fit(dfc)
        return self.predict(dfc)
    
    def predict(self, comparison_vectors):
        dfc = comparison_vectors
        dfc = self._predict_preprocess(dfc)
        return super().predict(dfc)
        
    def prob(self, comparison_vectors):
        dfc = comparison_vectors
        dfc = self._predict_preprocess(dfc)
        return super().prob(dfc)


class EnsembleECMClassifier(ECMClassifier):
     
    def __init__(self, ensemble_size = 10, init = "jaro", max_iter = 100, binarize = None, atol = 1e-4, use_col_names = True):
        ECMClassifier.__init__(self, init = init, max_iter = max_iter, binarize = binarize, atol = atol, use_col_names = use_col_names)
        self.ensemble_size = ensemble_size
        self.clfs = []
        self.fit_columns = []
        
    def _sample_features(self, df):
        def _get_feature_dict(df):
            features = collections.defaultdict(list)
            for c in df.columns:
                features[c.split("---")[0]] += [c]
            return features
        features = _get_feature_dict(df)
        ensemble = []
        for _ in range(0, self.ensemble_size):
            feats = []
            for k, v in features.items():
                feats += [random.choice(v)]
            ensemble += [feats]
        return ensemble
            
    def fit(self, comparison_vectors):
        dfc = comparison_vectors
        ensemble = self._sample_features(dfc)
        for cols in ensemble:
            clf = ECMClassifier()
            clf.fit(dfc[cols])
            self.clfs += [clf]
            self.fit_columns += [clf.raw_fit_columns]
            
    def fit_predict(self, comparison_vectors):
        dfc = comparison_vectors
        self.fit(dfc)
        return self.predict(dfc)
            
    def predict(self, comparison_vectors):
        dfc = comparison_vectors
        prd = []
        for cols, clf in zip(self.fit_columns, self.clfs):
            prd += [clf.predict(dfc[cols])]
        prd = pd.concat(prd, axis = 1)
        prd = prd.mode(axis = 1)
        return probas
         
    def prob(self, comparison_vectors):
        dfc = comparison_vectors
        prd = []
        for cols, clf in zip(self.fit_columns, self.clfs):
            prd += [clf.prob(dfc[cols])]
        prd = pd.concat(prd, axis = 1)
        prd = prd.median(axis = 1)
        return prd