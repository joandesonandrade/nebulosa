from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
#from sklearn.externals import joblib
import pandas
import numpy


#Função que codifica os rótulos para uma sequência de números baseados na quantidade. Supondo que exista os rótulos A, B, C neste exemplo a funçao irá atribuir valor A=1; B=2; C=3...
le = preprocessing.LabelEncoder()

#Lendo os dados usando a biblioteca pandas.
dados = pandas.read_csv("dados/001.csv")

#Transformando os valores em números
clima_codificado = le.fit_transform(dados["clima"])
temperatura_codificado = le.fit_transform(dados["temperatura"])
jogou_codificado = le.fit_transform(dados["jogou"])


#Rótudo dos dados
y = numpy.array(jogou_codificado)

#Separando os dados para treinamento e teste, Treinamento=75% e Teste=25%
lista = list(zip(clima_codificado, temperatura_codificado))
X = numpy.asarray(lista)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

#Criando o modelo de Naive Bayes Gaussian
modelo = GaussianNB()

#Treinamendo o modelo usando os dados
modelo.fit(X=X_train, y=y_train)

#Testando a precisão do nosso modelo
print("Precisão de", str(accuracy_score(y_test, modelo.predict(X_test)))+"%")

#joblib.dump(modelo, "model.NB.pkl")