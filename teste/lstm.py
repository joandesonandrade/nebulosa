# Código desenvolvido pelo Pedro Piassa
# Artigo http://www.uel.br/cce/dc/wp-content/uploads/PRELIMINAR-PEDRO-VITOR-PIASSA.pdf todos os direitos reservados.

import os
from math import *

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.utils import plot_model

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from matplotlib import pyplot

FILE_PATH = "folder/training_data/"
MODEL_PATH = "folder/model/lstm-{0}.model"
PLOT_PATH = "folder/lstm-{0}.model"

class DataType(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(f"Data type '{name}' not found")

    def __setattr__(self, name, value):
        raise AttributeError("Can't assign an attribute for a DataType")

    def __delattr__(self, name):
        if name in self:
            return self.pop(name, None)
        raise AttributeError(f"Data type '{name}' not found")

def prepare_data(data_type_folder, folders, files):
    data_dict = {}
    whole = None

    for folder in folders:
        single = None

        for file in files:
            full_path = FILE_PATH + data_type_folder + folder + "/" + file
            with open(full_path) as data_file:
                data_as_float = np.array([[line.rstrip("\r\n") for line in data_file]],
                                         dtype=np.float32)

                if single is None:
                    single = data_as_float
                else:
                    single = np.concatenate((single, data_as_float), axis=0)

        if whole is None:
            whole = single.T
        else:
            whole = np.concatenate((whole, single.T), axis=0)

    return whole

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True, drop_cols=None):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols = []
    names = []

    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [f'var{j+1}(t-{i})' for j in range(n_vars)] 

    for i in range(n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [f'var{j+1}(t)' for j in range(n_vars)]
        else:
            names += [f'var{j+1}(t+{i})' for j in range(n_vars)]

    agg = pd.concat(cols, axis=1)
    agg.columns = names

    if dropnan:
        agg.dropna(inplace=True)

    if drop_cols is not None:
        index_offset = n_in * n_vars
        drop_range = [j + index_offset + (n_vars * i) for i in range(n_out) for j in drop_cols]

        agg.drop(agg.columns[drop_range], axis=1, inplace=True)

    return agg

def training_data(files, data_type):
    data = []

    for _, v in files[data_type].items():
        data.append(v)

    return np.array(data, dtype=np.float32).T

def lstm_model(train_X, output_amount, activation):
    model = Sequential()
    model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2]),
                   activation=activation))
    model.add(Dense(output_amount))

    return model

def get_forecast(test_data, forecast_data, scaler, drop_cols):
    inv_forecast_data = np.empty(test_data.shape)
    j = 0

    for i in range(test_data.shape[1]):
        if i in drop_cols:
            inv_forecast_data[:, i] = test_data[:, i]
        else:
            inv_forecast_data[:, i] = forecast_data[:, j]
            j += 1
    inv_forecast_data = scaler.inverse_transform(inv_forecast_data)

    res = np.empty(forecast_data.shape)
    j = 0

    for i in range(test_data.shape[1]):
        if i not in drop_cols:
            res[:, j] = inv_forecast_data[:, i]
            j += 1

    return res

def plot_data(ip_data_forecast, port_data_forecast, name=None):
    ip_data_orig = values[:86400, 1]
    port_data_orig = values[:86400, 2]
    ip_data_ddos = ddos_vals[:, 1]
    port_data_ddos = ddos_vals[:, 2]

    fig, axs = plt.subplots(3, 2)
    plt.subplots_adjust(hspace=0.4)

    axs[0, 0].plot(ip_data_orig)
    axs[0, 0].set_title('IP orig')
        
    axs[0, 1].plot(port_data_orig) 
    axs[0, 1].set_title('PORT orig')

    axs[1, 0].plot(ip_data_forecast)
    axs[1, 0].set_title('IP forecast')

    axs[1, 1].plot(port_data_forecast)
    axs[1, 1].set_title('PORT forecast')
        
    axs[2, 0].plot(ip_data_ddos)
    axs[2, 0].set_title('IP DDoS')
    axs[2, 1].plot(port_data_ddos)
    axs[2, 1].set_title('PORT DDoS')

    tick_pos = [i * 3600 for i in range(25)]
    tick_label = [i for i in range(25)]

    for i in range(3):
        for j in range(2):
            pyplot.sca(axs[i, j])
            pyplot.xticks(tick_pos, tick_label)
    
    pyplot.legend()
    pyplot.show()

    if name is not None:
        fig.savefig(name + '.png')

def sketch_data(data, title):
    print('[*] ' + title.upper())
    if type(data) == pd.DataFrame:
        print(data.head())
    else:
        print(data)
    print(data.shape)
    print("--------------------------------------------------------------------------------\n\n")

if __name__ == "__main__":
    no_attack_data_folders = ['021218', '031218', '051218', '071218', '091218', '121218']
    ddos_first_data_folders = ['071218']
    ddos_sec_data_folders = ['071218']
    data_files = ['bytes1.txt', 'EntropiaDstIP1.txt', 'EntropiaDstPort1.txt', 'EntropiaScrIP1.txt', 'EntropiaSrcPort1.txt', 'packets1.txt']
    prediction_data = ['EntropiaDstIP1.txt', 'EntropiaDstPort1.txt']

    data_type = DataType(NO_ATTACK='without-attack/',
                         DDOS_PORTSCAN='ddos-portscan/',
                         PORTSCAN_DDOS='portscan-ddos/')

    values = prepare_data(data_type.NO_ATTACK,
                          no_attack_data_folders,
                          data_files)
    sketch_data(values, "raw traffic data, without attack, taken from the data files")

    ddos_vals = prepare_data(data_type.DDOS_PORTSCAN,
                             ddos_first_data_folders,
                             data_files)
    sketch_data(ddos_vals, "raw traffic data containing a ddos attack, taken from the data files")

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)

    lag_input = 1
    lag_output = 1
    n_features = 6
    drop_cols = [j for i, j in zip(data_files, range(len(data_files))) if i not in prediction_data] # Takes only the columns that are represented by the prediction_data variable

    scaled_data = series_to_supervised(scaled,
                                       n_in=lag_input,
                                       n_out=lag_output,
                                       drop_cols=drop_cols)
    sketch_data(scaled_data, "timeseries converted to a supervised learning problem")
    
    scaled_values = scaled_data.values

    testing_len = 86400 # size of the testing set
    training_len = scaled_values.shape[0] - testing_len # size of the training set

    n_obs = n_features * lag_input # number of observed variables
    layer_out = (n_features - len(drop_cols)) * lag_output # output variables

    train = scaled_values[:training_len, :]
    test = scaled_values[training_len:, :]
    sketch_data(train, "training data")
    sketch_data(test, "testing data")

    train_X = train[:, :n_obs]
    train_y = train[:, -layer_out:]
    test_X = test[:, :n_obs]
    test_y = test[:, -layer_out:]
#    print(train_X.shape, len(train_X), train_y.shape)

    train_X = train_X.reshape((train_X.shape[0], lag_input, n_features))
    test_X = test_X.reshape((test_X.shape[0], lag_input, n_features))
#    print(train_X.shape, test_X.shape)

    activation = tf.nn.softmax
    epochs = 4
    batch_size = 60

    model_name = f'activation={activation.__name__}-epochs={epochs}-batch_size={batch_size}'
    model_fullpath = MODEL_PATH.format(model_name)
    plot_fullpath = PLOT_PATH.format(model_name)

    if not os.path.isfile(model_fullpath):
        model = lstm_model(train_X=train_X, output_amount=layer_out,
                           activation=activation)

        print(model.summary())
        plot_model(model, to_file='./model_lstm.png', show_shapes=True,
                   show_layer_names=True)

        model.compile(loss='mae', optimizer='adam', metrics=['accuracy', 'mse'])

        history = model.fit(train_X,
                            train_y,
                            epochs=epochs,
                            batch_size=batch_size,
                            validation_data=(test_X, test_y),
                            verbose=1,
                            shuffle=False)

        model.save(model_fullpath)
    else:
        model = tf.keras.models.load_model(model_fullpath)

    yhat = model.predict(test_X)
    sketch_data(yhat, "model prediction data")

    test_X = test_X.reshape((test_X.shape[0], lag_input*n_features))
    sketch_data(test_X, "reshaped testing data")

    res = get_forecast(test_X, yhat, scaler, drop_cols) # Here is the predicted traffic
    sketch_data(res, "Predicted traffic data")

    plot_data(ip_data_forecast=res[:, 0], port_data_forecast=res[:, 1],
              name=plot_fullpath)
