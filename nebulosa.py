import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--intercept", help="--intercept | Intercept traffic", action="store_true")
    parser.add_argument("--preprocessing", help="--preprocessing | Processing data files", action="store_true")
    parser.add_argument("--train", help="--train | Training the model", action="store_true")
    parser.add_argument("--predict", help="--predict | Get predict the model", action="store_true")
    parser.add_argument("--listen", help="--listen | Listen traffic flow", action="store_true")
    parser.add_argument("--server", help="--server | Init the server", action="store_true")
    parser.add_argument("--api", help="--api | Init the API", action="store_true")
    args = parser.parse_args()

    if args.intercept:
        from src import intercept
        type = input("Enter the intercept type number [ 1- normal / 2- attack]> ")
        interface = input("Your interface [wlan0/eth0]> ")

        if type is not None and interface is not None:
            it = intercept.intercept(type=type, interface=interface)
            it.start()
            print(f'Interception in Threading... Type={it.type} -> Log={it.fileName} | Net={it.net}')

    if args.preprocessing:
        from src import preprocessing
        type = input("Enter the intercept type number [ 1- normal / 2- attack]> ")
        if type is not None:
            pre = preprocessing.processing(type=type)
            print('Processing data files...')
            pre.compile()

    if args.train:
        #from src import train
        from src import classifier
        type = input("Enter the intercept type number [ 1- normal / 2- attack]> ")
        if type is not None:
            #tr = train.trainer(type=type)
            tr = classifier.trainer(type=type)
            print(f'Training model... Type={tr.type}')
            tr.compile()

    if args.predict:
        from src import predict_model
        from random import randint

        print('Testing data random...')
        for i in range(50):
            mydstport = randint(0, 999)
            mypayload = randint(0, 999)
            if mydstport > 0:
                mypayload = mypayload / mydstport
            pm = predict_model.predict([randint(1, 3), randint(0, 1), randint(0, 999), mydstport, mypayload])
            r = pm.get_result()
            if int(r[0]) == 1:
                print('normal', pm.X)
            else:
                print('anormalies', pm.X)

    if args.listen:
        from src import listen
        interface = input("Your interface [wlan0/eth0]> ")
        if interface is not None:
            lt = listen.listen(interface)
            lt.start()

    if args.server:
        from src import server
        server.start()

    if args.api:
        from src import api
        api.start()



if __name__ == '__main__':
    main()