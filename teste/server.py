import socket
import pickle
import threading as th

host = ''
port = 4041

ids_jogadores = []
conections = []
clientes = []
threads = []
mensagens = []

def existeIDinServer(id):
    for j in ids_jogadores:
        return j == id
    return False

def broadCastMensagens(con):
    q = {"erro": 0, "mensagens": mensagens}
    con.send(pickle.dumps(q))

def lobbyClientServer(client, con):
    try:
        #conexão estabelecida
        print('Cliente conectado', client)
        dataJson = con.recv(1024)
        dataJson = pickle.loads(dataJson)
        if existeIDinServer(dataJson['id']):
            r = {"erro": 1, "msg": "ID já existe na sala", "code": 1}
            con.send(pickle.dumps(r))
            exit()

        print(f'{dataJson["id"]} entrou na sala.')
        conections.append(con)
        clientes.append(client)
        ids_jogadores.append(dataJson['id'])

        idClient = dataJson["id"]

        r = {"erro": 0, "status": 1}
        con.send(pickle.dumps(r))

        while True:
            try:
                broadCastMensagens(con)
                msg = con.recv(1024)
                if msg:
                    dataJson = pickle.loads(msg)
                    # if existeIDinServer(dataJson['id']) and dataJson['state'] == 3:
                    #     print('({0})> {1}'.format(idClient, dataJson["msg"]))
                    #     mensagens.append([idClient, dataJson['msg']])
                    print('({0})> {1}'.format(idClient, dataJson["msg"]))
                    mensagens.append([idClient, dataJson['msg']])
            except:
                con.close()
                print(f'{idClient} Cliente foi desconectado...')
                ids_jogadores.remove(idClient)
                clientes.remove(client)
                conections.remove(con)
                exit()
    except:
        print(f'Problema com o cliente {idClient}')
        exit()

print('Servidor iniciado...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (host, port)
s.bind(orig)
s.listen(1)

while True:
    con, client = s.accept()

    new_th = th.Thread(target=lobbyClientServer, args=(client, con, ))
    new_th.start()

    threads.append(new_th)
