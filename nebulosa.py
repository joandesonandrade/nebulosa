import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--intercept", help="--intercept | Intercept traffic", action="store_true")
    parser.add_argument("--preprocessing", help="--preprocessing | Processing data files", action="store_true")
    parser.add_argument("--train", help="--train | Training the model", action="store_true")
    parser.add_argument("--predict", help="--predict | Get predict the model", action="store_true")
    args = parser.parse_args()

    it = None
    pre = None
    tr = None

    if args.intercept:
        from src import intercept
        type = input("Enter the intercept type number [ 1- normal / 2- attack]> ")
        interface = input("Your interface [wlan0/eth0]> ")

        if type is not None and interface is not None:
            it = intercept.intercept(type=type, interface=interface)

    if args.preprocessing:
        from src import preprocessing
        type = input("Enter the intercept type number [ 1- normal / 2- attack]> ")
        pre = preprocessing.processing(type=type)

    if args.train:
        #from src import train
        from src import classifier
        type = input("Enter the intercept type number [ 1- normal / 2- attack]> ")
        #tr = train.trainer(type=type)
        tr = classifier.trainer(type=type)

    if args.predict:
        from src import predict_model
        from random import randint

        pm = predict_model.predict([1, 0, 0, 80, 0.091917591])
        r = pm.get_result()
        print(r[0])
        exit()

        for i in range(50):
            pm = predict_model.predict([randint(1, 3), randint(0, 1), randint(0, 999), randint(0, 999), randint(0, 999)])
            r = pm.get_result()
            if int(r[0]) == 1:
                print('Tráfego normal', pm.X)
            else:
                print('Tráfego anormal', pm.X)

    if tr is not None:
        print(f'Training model... Type={tr.type}')
        tr.compile()

    if pre is not None:
        print('Processing data files...')
        pre.compile()

    if it is not None:
        it.start()
        print(f'Interception in Threading... Type={it.type} -> Log={it.fileName} | Net={it.net}')

if __name__ == '__main__':
    main()