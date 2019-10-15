import os
import datetime
from sklearn.externals import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

DATA_PATH = 'data/'
MODEL_PATH = 'model/'

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

    def sort_list(self, X):
        y = []
        n = []
        while (len(y) < len(X)):
            s = np.random.randint(0, len(X))
            if s in y:
                continue
            print(X[s])
            n.append(X[s])
            y.append(s)
        return n


    def MODEL_KNN(self):
        return KNeighborsClassifier(n_neighbors=5)


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
        self.list_files = self.list_files()
        if len(self.list_files) == 0:
            print("Path \"" + DATA_PATH + self.type + "\" is empty")
            exit()

        self.data = self.get_data(self.list_files)
        print('Training {:.2f}MB of data...'.format(self.calc_bytes(self.data[0])))

        self.data = pd.read_csv(DATA_PATH + self.type + '/' + self.data[1]).values.tolist()

        ndata = [[n[1:], [1]] for n in self.data]

        n_features = len(ndata)

        for i in range(n_features):
            ndata.append([[ndata[i][0][0], ndata[i][0][1], np.random.randint(0, 999), np.random.randint(0, 999),
                           np.random.randint(1, 99)], [0]])
            print(ndata[(len(ndata) - 1)])

        ndata = self.sort_list(ndata)

        X = [n[0] for n in ndata]
        y = [n[1] for n in ndata]

        X_train, X_test, y_train, y_test = train_test_split(np.array(X, dtype=np.float64),
                                                            np.array(y, dtype=np.float64).ravel(),
                                                            test_size=0.3,
                                                            random_state=0)

        self.knn = self.MODEL_KNN()
        self.knn.fit(X=X_train, y=y_train)

        print("Predict model :", str(accuracy_score(y_test, self.knn.predict(X_test))) + "%")

        joblib.dump(self.knn, MODEL_PATH + 'model.pkl')
        print(f'Model successfully saved. -> {MODEL_PATH}model.pkl')