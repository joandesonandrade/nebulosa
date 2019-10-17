import pickle
import numpy as np

MODEL_PATH = 'model/'

class predict:

    def __init__(self, X):
        with open(MODEL_PATH + 'model.pkl', 'rb') as rb:
            self.model = pickle.load(rb)
            rb.close()
        self.X = X

    def get_result(self):
        X = np.array([self.X])
        return self.model.predict(X)