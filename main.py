"""
Authors:
    Jakub Żurawski: https://github.com/s23047-jz/NAI/
    Mateusz Olstowski: https://github.com/Matieus/NAI/


Dataset from the previous task: Banknote Dataset
https://machinelearningmastery.com/standard-machine-learning-datasets/
---
"""

import os

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import fashion_mnist, cifar10
from matplotlib import pyplot as plt


HERE = os.getcwd()
DATA_DIR = os.path.join(HERE, 'data')
RESULTS_DIR = os.path.join(HERE, 'results')
LOGS_DIR = os.path.join(HERE, 'logs')


class NeuralNetwork:
    def __init__(
            self,
            n_of_neural_layers,
            n_of_neural_per_layer,
            dropout_rate=0.2,
            output_units=1,
            learning_rate=0.2,
            epochs=50,
            batch_size=64,
            shape=None,
            activation='relu',
            model_type='dense'
    ):
        self.n_of_neural_layers = n_of_neural_layers
        self.n_of_neural_per_layer = n_of_neural_per_layer
        self.dropout_rate = dropout_rate
        self.output_units = output_units
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size
        self.activation = activation
        self.shape = shape
        self.model_type = model_type
        self.tensorboard_callback = {}
        self.__create_logs_dir()

        self.models = {
            'dense': self.__create_dense_model,
            'conv': self.__create_conv_model
        }
        self.model = self.models[self.model_type]()

    def __create_logs_dir(self):
        """
        Creates logs directory
        """
        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)
            print('Created logs directory: {}'.format(LOGS_DIR))

    def __create_dense_model(self):
        """
        Creates model with dense layers
        """
        print("CREATING DENSE MODEL")
        model = models.Sequential()

        for _ in range(self.n_of_neural_layers):
            model.add(layers.Dense(self.n_of_neural_per_layer, activation=self.activation))
            model.add(layers.Dropout(self.dropout_rate))

        model.add(layers.Dense(self.output_units, activation='sigmoid'))
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate), loss='binary_crossentropy',
                      metrics=['accuracy'])

        self.tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=LOGS_DIR, histogram_freq=0)
        return model

    def __create_conv_model(self):
        """
        Creates model with dense Conv2D
        """
        print("CREATING CONV MODEL")
        model = models.Sequential()
        model.add(layers.Conv2D(
            self.n_of_neural_per_layer, (3, 3), 1, activation=self.activation, input_shape=self.shape, padding='same'
        ))
        model.add(layers.MaxPool2D())
        for _ in range(self.n_of_neural_layers):
            model.add(layers.Conv2D(self.n_of_neural_per_layer, (3, 3), 1, activation=self.activation))
            model.add(layers.MaxPool2D())

        # the number of filters creates a channel
        model.add(layers.Flatten())

        model.add(layers.Dense(self.shape[0], activation=self.activation))
        model.add(layers.Dense(self.output_units, activation='sigmoid'))
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate), loss='binary_crossentropy',
                      metrics=['accuracy'])

        # check how model will transform data
        model.summary()
        self.tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=LOGS_DIR, histogram_freq=0)
        return model

    def evaluate_model(
            self,
            x_train,
            y_train,
            x_test,
            y_test,
            save_config,
            get_evaluate_model,
            show_diagrams=True
    ):
        """
        Evaluate the model

        Parameters
        ----------
        x_train: dataframe / np.ndarray - X of training data
        y_train: array / np.array - Y of training data
        x_test: dataframe / np.ndarray - X of test data
        y_test: array / np.array - Y of test data
        save_config: bool - Should save current model configuration to excel file
        get_evaluate_model: bool - Should return model evaluation score
        get_evaluate_modelshow_diagrams: bool - Should show diagrams of model evaluation

        Returns
        -------
        loss: float - Model evaluation loss score if get_evaluate_model is True
        """
        history = self.model.fit(
            x_train,
            y_train,
            validation_data=(x_test, y_test),
            epochs=self.epochs,
            batch_size=self.batch_size,
            callbacks=[self.tensorboard_callback]
        )

        if save_config:
            self.__save_config(history.history['accuracy'][-1])
        if get_evaluate_model:
            loss, _ = self.model.evaluate(x_train, y_train)
            return loss
        if show_diagrams:
            fig = plt.figure()
            plt.plot(history.history['loss'], color='teal', label='loss')
            plt.plot(history.history['accuracy'], color='blue', label='accuracy')
            fig.suptitle('Loss', fontsize=20)
            plt.legend(loc='upper left')
            plt.show()

    def __save_config(self, accuracy):
        """
        Saves neural network configuration and score to the path

        Parameters
        ----------
        accuracy: float - The score of the model evaluate
        """

        config = {
            "n_of_neural_layers": self.n_of_neural_layers,
            "n_of_neural_per_layer": self.n_of_neural_per_layer,
            "dropout_rate": self.dropout_rate,
            "output_units": self.output_units,
            "learning_rate": self.learning_rate,
            "batch_size": self.batch_size,
            "epochs": self.epochs,
            "accuracy": accuracy
        }

        path = os.path.join(RESULTS_DIR, 'result.xlsx')
        if os.path.exists(path):
            df = pd.read_excel(path)
            df = df.append(pd.DataFrame([config]), ignore_index=True)
        else:
            os.makedirs(RESULTS_DIR, exist_ok=True)
            df = pd.DataFrame([config])

        df.to_excel(path, index=False)


class Data:
    def __init__(self):
        self.X_train = self.y_train = self.X_val = self.y_val = self.X_test = self.y_test = None
        self.shape = []
        self.__tensor_dataset()

    def __get_data(self):
        """
        Returns tensorflow datasets
        """
        return fashion_mnist.load_data()

    def __tensor_dataset(self):
        """
        Reads data from tensorflow datasets and converts it to training, validation and test sets
        """
        (train_images, train_labels), (test_images, test_labels) = self.__get_data()

        train_images = np.reshape(
            train_images, (train_images.shape[0], train_images.shape[1], train_images.shape[2], 1)
        )
        test_images = np.reshape(
            test_images, (test_images.shape[0], test_images.shape[1], test_images.shape[2], 1)
        )

        print(train_images.shape)

        self.shape = (train_images.shape[1], train_images.shape[2], 1)

        train_images = train_images / 255.0
        test_images = test_images / 255.0

        train_size = int(len(train_images)*.8)
        test_size = int(len(test_images)*.1)

        self.X_train, self.y_train = train_images[:train_size], train_labels[:train_size]
        self.X_val, self.y_val = train_images[:test_size], train_labels[:test_size]
        self.X_test, self.y_test = test_images[:test_size], test_labels[:test_size]

    def run(self):
        """
        Create neural network class and run evaluate_model method
        """
        nn = NeuralNetwork(
            2, 32, epochs=100, learning_rate=0.001, shape=self.shape, model_type='conv'
        )
        nn.evaluate_model(self.X_train, self.y_train, self.X_val, self.y_val, True, False)


class FashionMnist(Data):

    def __get_data(self):
        return fashion_mnist.load_data()


class CIFAR10(Data):

    def __get_data(self):
        return cifar10.load_data()


class Banknotes:
    def __init__(self):
        self.X_train = self.y_train = self.X_val = self.y_val = self.X_test = self.y_test = None
        self.__get_data()

    def __get_data(self):
        """
        Reads data from the path and converts it to training, validation and test sets
        """
        df = pd.read_csv(os.path.join(DATA_DIR, 'banknotes.csv'))
        X = df.drop('valid', axis=1)
        y = df['valid']

        max_value = X.max().max()
        print("The max values in X is {}".format(max_value))

        X = X / 18.0

        train_size = int(len(X) * .8)
        test_size = int(len(X) * .1)

        self.shape = (X.shape[1],)

        self.X_train, self.y_train = X[:train_size], y[:train_size]
        self.X_val, self.y_val = X[:test_size], y[:test_size]
        self.X_test, self.y_test = X[test_size:test_size+test_size], y[test_size:test_size+test_size]

    def run(self):
        """
        Create neural network class and run evaluate_model method
        """
        nn = NeuralNetwork(
            3, 50, epochs=100, learning_rate=0.001, batch_size=32, shape=self.shape
        )
        nn.evaluate_model(self.X_train, self.y_train, self.X_val, self.y_val, True, False)


def main():
    # f = FashionMnist()
    # f.run()

    c = CIFAR10()
    c.run()

    # b = Banknotes()
    # b.run()


if __name__ == '__main__':
    main()
