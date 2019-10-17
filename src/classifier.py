import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import pickle

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
            # print(X[s])
            n.append(X[s])
            y.append(s)
        return n


    def MODEL_KNN(self, k):
        return KNeighborsClassifier(n_neighbors=k)


    def list_files(self):
        files = []
        for r, d, f in os.walk(DATA_PATH + self.type + '/'):
            for file in f:
                files.append(file)
        return files

    def decode_protocol(self, protocol):
        if protocol == 1:
            return "TCP"
        elif protocol == 2:
            return "UDP"
        else:
            return "Others"

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
        print('Size of {:.2f}MB of datas.'.format(self.calc_bytes(self.data[0])))

        self.data = pd.read_csv(DATA_PATH + self.type + '/' + self.data[1]).values.tolist()

        data_n_out = [x[2] for x in self.data if x[2] == 0]
        data_n_input = [x[2] for x in self.data if x[2] == 1]
        data_n_proto = [self.decode_protocol(x[1]) for x in self.data]
        data_n_src = [x[3] for x in self.data]
        data_n_dst = [x[4] for x in self.data]
        data_n_payload = [x[5] for x in self.data]

        print('=========== STATUS ===========')
        print("I/O: ")
        print('Out=', len(data_n_out), '| Input=', len(data_n_input))
        print('\nPROTOCOLS: ')
        print(pd.DataFrame({'protocol': data_n_proto})['protocol'].value_counts())
        print('\nSource Ports: ')
        print(pd.DataFrame({'src': data_n_src})['src'].value_counts())
        print('\nDestination Ports: ')
        print(pd.DataFrame({'dst': data_n_dst})['dst'].value_counts())
        print('\nMean of Payload: ')
        print(pd.DataFrame({'payload': data_n_payload})['payload'].mean())
        input('\nClick Enter to continue...')

        ndata = [[n[1:], [1]] for n in self.data]

        n_features = len(ndata)

        print('\nRandomly mixing data...')
        for i in range(n_features):
            n_dst = np.random.randint(0, 999)
            n_payload = np.random.randint(1, 99)
            if n_dst > 0:
                n_payload = n_payload / n_dst
            ndata.append([[ndata[i][0][0], ndata[i][0][1], np.random.randint(0, 999), n_dst, n_payload], [0]])
            # print(ndata[(len(ndata) - 1)])

        ndata = self.sort_list(ndata)

        X = [n[0] for n in ndata]
        y = [n[1] for n in ndata]

        X_train, X_test, y_train, y_test = train_test_split(np.array(X, dtype=np.float64),
                                                            np.array(y, dtype=np.float64).ravel(),
                                                            test_size=0.3,
                                                            random_state=0)

        print('Calculating the best n_neighbors...')
        k_test = 26
        k_result = []
        for i in range(1, k_test):
            self.knn = self.MODEL_KNN(i)
            self.knn.fit(X=X_train, y=y_train)
            k_result.append(accuracy_score(y_test, self.knn.predict(X_test)))

        k_index = 0
        k_best = k_result[k_index]

        for k in k_result:
            if k > k_best:
                k_best = k
                k_index = k_result.index(k)

        k_index = (k_index + 1)
        acc = k_best * 100
        print('Best Accuracy: {:.2f}%'.format(acc))
        print('n_neighbors:', k_index)

        self.knn = self.MODEL_KNN(k_index)
        self.knn.fit(X=X_train, y=y_train)

        print("Predict model: {:.2f}%".format(acc))

        if input('Do you want to save the model? (yes/no)> ') == 'yes':
            with open(MODEL_PATH + 'model.pkl', 'wb') as wf:
                pickle.dump(self.knn, wf)
                wf.close()
            print(f'Model successfully saved. -> {MODEL_PATH}model.pkl')