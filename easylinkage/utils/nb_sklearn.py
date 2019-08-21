# -*- coding: utf-8 -*-

import warnings

import numpy as np

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_array, check_X_y
from sklearn.exceptions import NotFittedError
from sklearn.preprocessing import LabelBinarizer, binarize

try:  # SciPy >= 0.19
    from scipy.special import logsumexp
except ImportError:
    from scipy.misc import logsumexp  # noqa
from scipy.sparse import issparse

from recordlinkage.types import is_string_like
from recordlinkage.algorithms.nb_sklearn import safe_sparse_dot
from recordlinkage.algorithms.nb_sklearn import ECM as BaseECM

class ECM(BaseECM):

    def fit(self, X):

        X = check_array(X, accept_sparse='csr')

        # count frequencies of elements in vector space
        # based on https://stackoverflow.com/a/33235665
        # faster than numpy.unique
        X_unique, X_freq = np.unique(X, axis=0, return_counts=True)
        X_freq = np.atleast_2d(X_freq)

        # Transform data with a label binarizer. Each column will get
        # transformed into a N columns (for each distinct value a column). For
        # a situation with 0 and 1 outcome values, the result given two
        # columns.
        X_unique_bin = self._fit_data(X_unique)
        _, n_features = X_unique_bin.shape

        # initialise parameters
        self.classes_ = np.array([0, 1])

        if is_string_like(self.init) and self.init == 'random':
            self.class_log_prior_, self.feature_log_prob_ = \
                self._init_parameters_random(X_unique_bin)
        elif is_string_like(self.init) and self.init == 'jaro':
            self.class_log_prior_, self.feature_log_prob_ = \
                self._init_parameters_jaro(X_unique_bin)
        else:
            raise ValueError("'{}' is not a valid value for "
                             "argument 'init'".format(self.init))

        iteration = 0
        stop_iteration = False

        self._log_class_log_prior = np.atleast_2d(self.class_log_prior_)
        self._log_feature_log_prob = np.atleast_3d(self.feature_log_prob_)

        while iteration < self.max_iter and not stop_iteration:

            # expectation step
            g = self.predict_proba(X_unique)
            g_freq = g * X_freq.T
            g_freq_sum = g_freq.sum(axis=0)

            # maximisation step
            class_log_prior_ = np.log(g_freq_sum + 1e-10) - np.log(X.shape[0] + 1e-10)  # p
            feature_log_prob_ = np.log(safe_sparse_dot(g_freq.T, X_unique_bin) + 1e-10)
            feature_log_prob_ -= np.log(np.atleast_2d(g_freq_sum).T + 1e-10)

            # Stop iterating when the class prior and feature probs are close
            # to the values in the to previous iteration (parameters starting
            # with 'self').
            class_log_prior_close = np.allclose(
                class_log_prior_, self.class_log_prior_, atol=self.atol)
            feature_log_prob_close = np.allclose(
                feature_log_prob_, self.feature_log_prob_, atol=self.atol)
            if (class_log_prior_close and feature_log_prob_close):
                stop_iteration = True
            if np.all(np.isnan(feature_log_prob_)):
                stop_iteration = True

            # Update the class prior and feature probs.
            self.class_log_prior_ = class_log_prior_
            self.feature_log_prob_ = feature_log_prob_

            # create logs
            self._log_class_log_prior = np.concatenate(
                [self._log_class_log_prior,
                 np.atleast_2d(self.class_log_prior_)]
            )
            self._log_feature_log_prob = np.concatenate(
                [self._log_feature_log_prob,
                 np.atleast_3d(self.feature_log_prob_)], axis=2
            )
            # Increment counter
            iteration += 1

        return self
