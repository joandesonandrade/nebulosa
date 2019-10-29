import pickle
import numpy as np
from keras.models import load_model

MODEL_PATH = 'model/'

#called with import lib
with open(MODEL_PATH + 'model.pkl', 'rb') as rb:
    model_knn = pickle.load(rb)
    rb.close()
model_lstm = load_model(MODEL_PATH + 'model.h5')

class predict:

    def __init__(self, X, buffer):
        self.X = X
        self.buffer = buffer

    def get_result(self):
        lstm_result = 0
        self.X = np.array([self.X])
        if len(self.buffer) > 5:
            self.buffer = np.array(self.buffer)
            self.buffer = np.reshape(self.buffer, (self.buffer.shape[0], self.buffer.shape[1], 1))
            lstm_result = np.argmax(model_lstm.predict(self.buffer, 60, verbose=True))
        knn_result = model_knn.predict(self.X)[0]
        return knn_result, lstm_result
