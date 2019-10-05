from sklearn import preprocessing
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

#Abrindo o dados como Dataframe
dados = pd.read_csv('dados/001.csv')

#Iniciando o método para binanizar as classe sim=1; não=0
pre = preprocessing.LabelBinarizer()

#Binazirando a classe jogou, e atribuíndo a uma matriz n-dimencional
y_binary = pre.fit_transform(dados['jogou'])
y = np.array(y_binary).ravel()

lista_clima = [x for x in dados['clima']]
lista_temperatura = [x for x in dados['temperatura']]
lista_jogou = [x for x in dados['jogou']]

pre = preprocessing.LabelEncoder()

clima_encoding = pre.fit_transform(lista_clima)
temperatura_encoding = pre.fit_transform(lista_temperatura)
jogou_encoding = pre.fit_transform(lista_jogou)

lista = list(zip(clima_encoding, temperatura_encoding, jogou_encoding))

X = np.array(lista, dtype=np.int32)

#colunas = ['A', 'B', 'C']

# print(pd.DataFrame(X, columns=colunas, dtype=np.int32))
# print(pd.DataFrame(y, columns=['Classe'], dtype=np.int32))
#
# xX = []
# for i, x in enumerate(X):
#     xX.append([list(x), y[i][0]])
#
# dX = [(x[0][0] + x[0][1] + x[0][2]) for x in xX]
# dY = [x[1] for x in xX]
#
# print('Soma dos rótulos:', dX)
# print('Classe:', dY)
#
# fig, ax = plt.subplots()
# ax.plot(dX)
# ax.plot(dY)
# plt.show()


from sklearn import model_selection
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

#Dividido os dados, onde o treinamento ficará com 75% e teste 25%, eu sempre uso este padrão :)
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.25, random_state=0)

#Gerando o modelo, vou deixar os parâmetros padrão
knn = KNeighborsClassifier()

#Treinando o modelo
knn.fit(X=X_train, y=y_train)

#Avaliando a pontuação do modelo, usando os dados de teste
pontuacao = str(accuracy_score(y_test, knn.predict(X_test)) * 100)
print("Precisão: "+pontuacao+"%")
