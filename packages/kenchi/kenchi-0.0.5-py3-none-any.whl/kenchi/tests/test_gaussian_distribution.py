from unittest import TestCase

import numpy as np
from sklearn.model_selection import ParameterGrid

from kenchi import GaussianDetector


class GaussianDetectorTest(TestCase):
    def test_score(self):
        train_size = 1000
        test_size  = 100
        n_outliers = 10
        n_features = 10

        rnd        = np.random.RandomState(0)

        X_train    = rnd.normal(size=(train_size, n_features))

        X_test     = np.concatenate(
            (
                rnd.normal(size=(test_size - n_outliers, n_features)),
                rnd.uniform(-10.0, 10.0, size=(n_outliers, n_features))
            )
        )
        y_test     = np.concatenate(
            (
                np.zeros(test_size - n_outliers, dtype=np.int32),
                np.ones(n_outliers, dtype=np.int32),
            )
        )

        param_grid = {
            'assume_independent':    [False, True],
            'fpr':                   [0.1],
            'threshold':             [None, 3.0],
            'use_method_of_moments': [True]
        }

        for params in ParameterGrid(param_grid):
            det    = GaussianDetector().set_params(**params)

            self.assertIsInstance(det.fit(X_train), GaussianDetector)
            self.assertGreater(det.score(X_test, y_test), 0.0)
