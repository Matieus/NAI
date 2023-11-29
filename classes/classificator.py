from classes.traintestdata import TrainTestData
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report  # type: ignore
from sklearn import svm
from typing import Any


class Classificator:
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

        self.dc_classifier = DecisionTreeClassifier(
            random_state=random_state,
            max_depth=max_depth,
        )
        self.dc_classifier.fit(
            self.data.X_train,
            self.data.y_train,
        )

        self.y_test_dc_pred: np.ndarray[Any, Any] = self.dc_classifier.predict(
            self.data.X_test
        )

        self.svm_classifier = svm.SVC()
        self.svm_classifier.fit(self.data.X_train, self.data.y_train)

        self.y_test_svm_pred: np.ndarray[Any, Any] = self.svm_classifier.predict(
            self.data.X_test
        )

    def tranning(self):
        print(
            f"{self.name} | Decision Tree | Training Report",
            classification_report(
                self.data.y_train,
                self.dc_classifier.predict(self.data.X_train),
            ),  # type: ignore
            sep="\n",
        )

    def testing(self):
        print(
            f"{self.name} | Decision Tree | Testing Report",
            classification_report(
                self.data.y_test, self.y_test_dc_pred
            ),  # type: ignore
            sep="\n",
        )

    def svm_tranning(self):
        print(
            f"{self.name} | SVM | Training Report",
            classification_report(
                self.data.y_train,
                self.svm_classifier.predict(self.data.X_train),
            ),  # type: ignore
            sep="\n",
        )

    def svm_testing(self):
        print(
            f"{self.name} | SVM | Testing Report",
            classification_report(
                self.data.y_test, self.y_test_svm_pred
            ),  # type: ignore
            sep="\n",
        )
