import os
import datetime
from sklearn.externals import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Flatten
from sklearn.preprocessing import MinMaxScaler
from matplotlib.pyplot import plot
from sklearn.neural_network import MLPClassifier

DATA_PATH = 'data/'
MODEL_PATH = 'model/'
EPOCHS = 4
BATCH_SIZE = 64

class trainer:
    def __init__(self, type):
        try:
            if int(type) == 1:
                type = 'normal'
            elif int(type) == 2:
                type = 'attack'
            else:
                type = 'normal'
                print('Type was set to normal default.')
        except ValueError:
            raise ('Invalid type [ Select number 1 to normal or 2 to attack ]')

        self.type = type

    def calc_bytes(self, data):
        return len(data) / 1024 / 1024

    def salveModelTo(self):
        now = datetime.datetime.now()
        self.timeLog = str(now.day) + "-" + str(now.month) + "-" + str(now.year) + "_" + str(now.hour) + \
                       ":" + str(now.minute) + ".nebulosa"
        self.fileName = self.type + "-" + self.timeLog
        return MODEL_PATH + self.fileName

    def LSTM_MODEL(self, inputlstm):
        model = Sequential()
        model.add(LSTM(
            300,
            input_shape=inputlstm,
            return_sequences=True,
            activation='relu'))
        model.add(Flatten())
        model.add(Dense(6, activation='linear'))
        return model

    def compile_model(self, model):
        model.compile(loss='binary_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        return model

    def list_files(self):
        files = []
        for r, d, f in os.walk(DATA_PATH + self.type + '/'):
            for file in f:
                files.append(file)
        return files

    def get_data(self, list):
        data = None
        msg = 'SELECT YOUR DATASET\n\n'
        j = 0
        for file in list:
            msg += str(j) + ' -> ' + file + '\n'
            j += 1
        print(msg)
        while (data is None):
            s = input('dataset> ')
            try:
                with open(DATA_PATH + self.type + '/' + str(list[int(s)])) as rf:
                    data = rf.read()
                    rf.close()
            except IndexError:
                print('Index invalid, select a number valid.')

        return data, list[int(s)]

    def compile(self):
        self.model_path = self.salveModelTo()
        self.list_files = self.list_files()
        if len(self.list_files) == 0:
            print("Path \"" + DATA_PATH + self.type + "\" is empty")
            exit()

        self.data = self.get_data(self.list_files)
        print('Training {:.2f}MB of data...'.format(self.calc_bytes(self.data[0])))

        self.data = pd.read_csv(DATA_PATH + self.type + '/' + self.data[1])


        X = self.data[0:549]
        y = self.data[1:550]


        X_train, X_test, y_train, y_test = train_test_split(np.array(X),
                                                            np.array(y),
                                                            test_size=0.3,
                                                            random_state=0)

        # X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
        # y_train = np.reshape(y_train, (y_train.shape[0], 1, y_train.shape[1]))

        X_train = np.reshape(X_train, (-1, X_train.shape[1]))
        #X_test = np.reshape(X_test, (-1, X_test.shape[1]))
        y_train = np.reshape(y_train, (-1, y_train.shape[1]))
        #y_test = np.reshape(y_test, (-1, y_test.shape[1]))

        MinMax = MinMaxScaler()

        X_train = MinMax.fit_transform(X_train)
        #y_train = MinMaxScaler.fit_transform(y_train)

        X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
        X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

        inputlstm = (X_train.shape[1], X_train.shape[2])

        self.lstm = self.LSTM_MODEL(inputlstm)
        self.lstm = self.compile_model(self.lstm)
        self.lstm.fit(X_train,
                      y_train,
                      batch_size=BATCH_SIZE,
                      epochs=EPOCHS)
        score, acc = self.lstm.evaluate(X_test, y_test, batch_size=BATCH_SIZE)
        print(f'{acc}%')