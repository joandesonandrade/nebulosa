from src import intercept
import sys

def main():
    args = sys.argv

    howUse = "your command was invalid. How Use:\n"\
             "python3 nebulosa.py intercept normal|attack interface(wlp2s0)"

    it = None

    if len(args) > 1:
        try:
            args[1] = args[1]
            #Setting intercepting method
            if args[1] == 'intercept':
                args[2] = args[2]
                args[3] = args[3]
                if args[2] == 'normal':
                    it = intercept.intercept('normal', args[3])
                elif args[2] == 'attack':
                    it = intercept.intercept('attack', args[3])
                else:
                    print(howUse)
        except IndexError:
            print(howUse)

    if it is not None:
        it.start()
        print(f'Interception in Threading... Type={it.type} -> Log={it.fileName} | Net={it.net}')

if __name__ == '__main__':
    main()