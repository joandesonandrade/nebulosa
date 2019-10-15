from sklearn.externals import joblib
import numpy as np

MODEL_PATH = 'model/'

class predict:

    def __init__(self, X):
        self.model = joblib.load(MODEL_PATH + 'model.pkl')
        self.X = X

    def get_result(self):
        X = np.array([self.X])
        return self.model.predict(X)