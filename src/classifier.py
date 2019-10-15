import os
import datetime
from sklearn.externals import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import random as rd
from sklearn.metrics import accuracy_score

DATA_PATH = 'data/'
MODEL_PATH = 'model/'
EPOCHS = 1
BATCH_SIZE = 60

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

    def MODEL_NB(self):
        return GaussianNB()


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

        self.data = pd.read_csv(DATA_PATH + self.type + '/' + self.data[1]).values.tolist()

        X = [x[1:] for x in self.data]
        y = [1 for y in self.data]

        n_features = len(X)

        for i in range(n_features):
            X.append([X[i][0], X[i][1], rd.randint(0, 999), rd.randint(0, 999), rd.randint(1, 99)])
            y.append(0)
            print(X[(len(X) - 1)])

        X_train, X_test, y_train, y_test = train_test_split(np.array(X, dtype=np.float64),
                                                            np.array(y, dtype=np.float64),
                                                            test_size=0.3,
                                                            random_state=0)


        self.nb = self.MODEL_NB()
        self.nb.fit(X=X, y=y)

        print("Predict model :", str(accuracy_score(y_test, self.nb.predict(X_test))) + "%")

        test = np.array([[1, 1, 80, 80, 0.18]], dtype=np.float64)

        print(test)

        pre = self.nb.predict(test)[0]
        print(pre)