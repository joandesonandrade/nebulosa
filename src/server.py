import socket
import pickle
import threading as th

host = ''
port = 30

threads = []

LOGS_PATH = 'logs/'

def broadCast(con, data):
    q = {
            "success": 1,
            "data": data
        }
    con.send(pickle.dumps(q))

def lobbyClientServer(client, con):
    print('Client connected', client)
    try:
        while True:
            try:
                with open(LOGS_PATH + 'logs.csv', 'rt') as rt:
                    ndata = [x for x in rt.read().replace(',', '').split('\n') if x is not '']
                    rt.close()

                data = []
                for i, x in enumerate(ndata):
                    if i > (len(ndata) - 50):  # offset
                        data.append(x)

                msg = con.recv(1024)
                if msg:
                    broadCast(con, data)
            except:
                print('Client desconnected', client)
                exit()
    except:
        print('Client desconnected', client)
        exit()


def start():
    print('Server is working...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (host, port)
    s.bind(orig)
    s.listen(1)

    while True:
        con, client = s.accept()

        new_th = th.Thread(target=lobbyClientServer, args=(client, con, ))
        new_th.start()

        threads.append(new_th)
