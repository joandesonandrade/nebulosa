import random
import socket
import pickle

host = '127.0.0.1'
port = 4041

def gerarIdGame():
    return random.randint(10,999)

id_jogador = gerarIdGame()

print('Conectando com o servidor...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (host, port)
s.connect(dest)

dataJson = {"id": id_jogador, "state": 1}
s.send(pickle.dumps(dataJson))
dataJson = s.recv(1024)
dataJson = pickle.loads(dataJson)

if(dataJson['erro'] == 0 and dataJson['status'] == 1):
    print('Conexão estabelecida com o servidor...')
    while True:
        dataJson = s.recv(1024)
        if dataJson:
            dataJson = pickle.loads(dataJson)
            if dataJson['erro'] == 0:
                for mensagem in dataJson['mensagens']:
                    print('({0})> {1}'.format(mensagem[0], mensagem[1]))

        msg = input('> ')
        s.send(pickle.dumps({"id": id_jogador, "state": 3, "msg": msg}))
