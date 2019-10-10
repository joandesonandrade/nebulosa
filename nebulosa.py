from src import intercept
from 
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--intercept", help="--intercept | Intercept traffic", action="store_true")
    args = parser.parse_args()

    it = None

    if args.intercept:
        type = input("Enter the intercept type number [ 1- normal / 2- attack]> ")
        interface = input("Your interface [wlan0/eth0]> ")

        if type is not None and interface is not None:
            it = intercept.intercept(type=type, interface=interface)

    if it is not None:
        it.start()
        print(f'Interception in Threading... Type={it.type} -> Log={it.fileName} | Net={it.net}')

if __name__ == '__main__':
    main()