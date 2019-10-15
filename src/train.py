import os
import datetime
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, LSTM, Flatten, Dropout
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

DATA_PATH = 'data/'
MODEL_PATH = 'model/'
EPOCHS = 4
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

    def LSTM_MODEL(self, inputlstm):
        model = Sequential()
        model.add(LSTM(
            200,
            input_shape=inputlstm,
            return_sequences=True,
            activation='relu'))
        model.add(Flatten())
        model.add(Dense(5, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(5, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(5, activation='softmax'))
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

        ndata = [[n[1:], [1, 1, 1, 1, 1]] for n in self.data]

        n_features = len(ndata)

        for i in range(n_features):
            ndata.append([[ndata[i][0][0], ndata[i][0][1], np.random.randint(0, 999), np.random.randint(0, 999), np.random.randint(1, 99)], [0, 0, 0, 0, 0]])
            print(ndata[(len(ndata) - 1)])

        ndata = self.sort_list(ndata)

        X = [n[0] for n in ndata]
        y = [n[1] for n in ndata]

        X_train, X_test, y_train, y_test = train_test_split(np.array(X, dtype=np.float64),
                                                            np.array(y, dtype=np.float64),
                                                            test_size=0.3,
                                                            random_state=0)

        X_train = np.reshape(X_train, (-1, X_train.shape[1]))
        y_train = np.reshape(y_train, (-1, y_train.shape[1]))

        MinMax = MinMaxScaler(feature_range=(0, 1))

        X_train = MinMax.fit_transform(X_train)
        y_train = MinMax.fit_transform(y_train)

        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        inputlstm = (X_train.shape[1], X_train.shape[2])

        self.lstm = self.LSTM_MODEL(inputlstm)
        self.lstm = self.compile_model(self.lstm)
        history = self.lstm.fit(X_train,
                      y_train,
                      batch_size=BATCH_SIZE,
                      epochs=EPOCHS,
                      validation_data=(X_test, y_test))
        score, acc = self.lstm.evaluate(X_test, y_test, batch_size=BATCH_SIZE)
        print(f'acc={acc}%; score={score}')

        showGraph = input('Show Graph (yes/no)> ')

        if showGraph == 'yes':
            # Plot training & validation accuracy values
            plt.plot(history.history['acc'])
            plt.title('Model accuracy')
            plt.ylabel('Accuracy')
            plt.xlabel('Epoch')
            plt.legend(['Train', 'Test'], loc='upper left')
            plt.show()

            # Plot training & validation loss values
            plt.plot(history.history['loss'])
            plt.title('Model loss')
            plt.ylabel('Loss')
            plt.xlabel('Epoch')
            plt.legend(['Train', 'Test'], loc='upper left')
            plt.show()


        # pred = np.array([[1, 0, 21, 0, 0.140006623613181]])
        # pred = MinMax.fit_transform(pred)
        # pred = np.reshape(pred, (pred.shape[0], pred.shape[1], 1))
        #
        # predicted = self.lstm.predict(pred, BATCH_SIZE, verbose=True)
        # print(MinMax.inverse_transform(predicted))
        # print(self.lstm.evaluate(pred, predicted, batch_size=BATCH_SIZE))
        #
        # print(np.argmax(predicted))

        self.lstm.save(MODEL_PATH + 'model.h5')
        print(f'Model successfully saved. -> {MODEL_PATH}model.h5')