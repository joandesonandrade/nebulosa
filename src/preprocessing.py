import os
import datetime
import threading as th
import pandas as pd
import numpy as np

LOGS_PATH = 'logs/'
DATA_PATH = 'data/'


class processing:

    def encode_protocol(self, protocol):
        #tcp=1;udp=2;others=3
        if protocol == '6':
            return 1
        elif protocol == '17':
            return 2
        else:
            return 3

    def encode_port(self, port):
        #ports longer than 3 digits are irrelevant
        if len(port) > 3:
            return 0
        else:
            return int(port)

    def ThreadProcessing(self, data=None):
        lines = data.split("\n")
        columns = ['protocol', 'io', 'srcport', 'dstport', 'payload']
        data = []
        for line in lines:
            # Protocol|I/O|SrcPort|DstPort|SumPayload|LenPayload
            d = line.split("|")
            if len(d) > 4:
                data.append([d[0], d[1], d[2], d[3], d[4]])

        #normalize data
        protocol_ = np.array([self.encode_protocol(x[0]) for x in data], dtype=np.int32)
        io_ = np.array([x[1] for x in data], dtype=np.int32)
        src_ = np.array([self.encode_port(x[2]) for x in data], dtype=np.int32)
        dst_ = np.array([self.encode_port(x[3]) for x in data], dtype=np.int32)
        payload_ = np.array([x[4] for x in data])
        normal = np.array(pd.DataFrame({
            'A': protocol_,
            'B': io_,
            'C': src_,
            'D': dst_,
            'E': payload_
        }))
        #
        df = pd.DataFrame(normal, columns=columns)
        df.to_csv(DATA_PATH + self.type + '/' + self.fileName)
        self.finish = True
        print(f'Successful, Type={self.type} -> CSV={self.fileName}')

    def __init__(self, type=None):
        try:
            if int(type) == 1:
                type = 'normal'
            elif int(type) == 2:
                type = 'attack'
            else:
                type = 'normal'
                print('Type was set to normal default.')
        except ValueError:
            raise ('Invalid type [ Select number 1 to normal or 2 to attack ]')

        self.finish = False
        self.type = type
        self.fileName = None

    def saveToCSV(self):
        now = datetime.datetime.now()
        self.timeLog = str(now.day) + "-" + str(now.month) + "-" + str(now.year) + "_" + str(now.hour) + \
                       ":" + str(now.minute) + ".csv"
        self.fileName = self.type + "-" + self.timeLog
        return DATA_PATH + self.fileName

    def list_files(self):
        files = []
        for r, d, f in os.walk(LOGS_PATH + self.type + '/'):
            for file in f:
                files.append(file)
        return files

    def processing_data(self):
        data = ''
        for file in self.list_files:
            with open(LOGS_PATH + self.type + '/' + file, 'rt') as rf:
                data += rf.read()
                rf.close()
        thData = th.Thread(target=self.ThreadProcessing, args=(data,))
        thData.start()
        return thData

    def compile(self):
        self.absolutePathFile = self.saveToCSV()
        self.list_files = self.list_files()
        if len(self.list_files) == 0:
            print("Path \"" + LOGS_PATH + self.type + "\" is empty")
            exit()
        self.processing_data()
        while (self.finish == False):
            continue