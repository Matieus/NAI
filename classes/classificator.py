from classes.traintestdata import TrainTestData
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report  # type: ignore
from sklearn import svm
from typing import Any


class Classificator:
    """Class that performs classification using SVM and a decision tree

    Parameters:
    data (TrainTestData): data for classification
    name (str): name of Classificator for the report
    random_state (int): Controls the randomness of the estimator
    max_depth (int): The maximum depth of the tree.

    """

    def __init__(
        self,
        *,
        data: TrainTestData,
        name: str = "Unknown",
        random_state: int = 0,
        max_depth: int = 100,
    ) -> None:
        self.name = name
        self.data = data

        """Starts creating decission tree"""
        self.dc_classifier = DecisionTreeClassifier(
            random_state=random_state,
            max_depth=max_depth,
        )

        """Build a decision tree classifier from the training set (X, y)."""
        self.dc_classifier.fit(
            self.data.X_train,
            self.data.y_train,
        )

        """Predict class or regression value for X."""
        self.y_test_dc_pred: np.ndarray[Any, Any] = self.dc_classifier.predict(
            self.data.X_test
        )

        self.svm_classifier = svm.SVC()

        """Fit the SVM model according to the given training data."""
        self.svm_classifier.fit(self.data.X_train, self.data.y_train)

        """Perform classification on samples in X."""
        self.y_test_svm_pred: np.ndarray[Any, Any] = self.svm_classifier.predict(
            self.data.X_test
        )

    def traning(self):
        """Printing report showing the main classification metrics
        for tranning decision tree"""
        print(
            f"{self.name} | Decision Tree | Training Report",
            classification_report(
                self.data.y_train,
                self.dc_classifier.predict(self.data.X_train),
            ),  # type: ignore
            sep="\n",
        )

    def testing(self):
        """Printing report showing the main classification metrics
        for testing a decision tree
        """
        print(
            f"{self.name} | Decision Tree | Testing Report",
            classification_report(
                self.data.y_test, self.y_test_dc_pred
            ),  # type: ignore
            sep="\n",
        )

    def svm_traning(self):
        """Printing report showing the main classification metrics
        for tranning SVM"""
        print(
            f"{self.name} | SVM | Training Report",
            classification_report(
                self.data.y_train,
                self.svm_classifier.predict(self.data.X_train),
            ),  # type: ignore
            sep="\n",
        )

    def svm_testing(self):
        """Printing report showing the main classification metrics
        for testing SVM"""
        print(
            f"{self.name} | SVM | Testing Report",
            classification_report(
                self.data.y_test, self.y_test_svm_pred
            ),  # type: ignore
            sep="\n",
        )
