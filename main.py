"""
Authors:
    Jakub Żurawski: https://github.com/s23047-jz/NAI/
    Mateusz Olstowski: https://github.com/Matieus/NAI/


5. Banknote Dataset
https://machinelearningmastery.com/standard-machine-learning-datasets/

The Banknote Dataset involves predicting whether a given banknote is authentic
given a number of measures taken from a photograph.

It is a binary (2-class) classification problem. The number of observations
for each class is not balanced. There are 1,372 observations with 4 input
variables and 1 output variable. The variable names are as follows:

Variance of Wavelet Transformed image (continuous).
Skewness of Wavelet Transformed image (continuous).
Kurtosis of Wavelet Transformed image (continuous).
Entropy of image (continuous).
Class (0 for authentic, 1 for inauthentic).
The baseline performance of predicting the most prevalent class
is a classification accuracy of approximately 50%.

A sample of the first 5 rows is listed below.

3.6216,8.6661,-2.8073,-0.44699,0
4.5459,8.1674,-2.4586,-1.4621,0
3.866,-2.6383,1.9242,0.10645,0
3.4566,9.5228,-4.0112,-3.5944,0
0.32924,-4.4552,4.5718,-0.9888,0
4.3684,9.6718,-3.9606,-3.1625,0

---

Letter Recognition
https://archive.ics.uci.edu/dataset/59/letter+recognition

Database of character image features; try to identify the letter

The objective is to identify each of a large number of black-and-white
rectangular pixel displays as one of the 26 capital letters
in the English alphabet.  The character images were based on
20 different fonts and each letter within these 20 fonts was randomly
distorted to produce a file of 20,000 unique stimuli.
Each stimulus was converted into 16 primitive numerical attributes
(statistical moments and edge counts) which were then scaled
to fit into a range of integer values from 0 through 15.
We typically train on the first 16000 items and then
use the resulting model to predict the letter category
for the remaining 4000.  See the article cited above for more details.
"""


from classes.classificator import Classificator
from classes.traintestdata import banknote_data, letters_data


def main():
    bnk = Classificator(
        name="Banknote Recognition",
        data=banknote_data(),
        max_depth=3,
    )
    bnk.testing()
    bnk.svm_testing()

    ltr = Classificator(
        name="Letters Recognition",
        data=letters_data(),
    )
    ltr.testing()
    ltr.svm_testing()


if __name__ == "__main__":
    main()
