from threading import Thread
import pcapy
from impacket.ImpactDecoder import LinuxSLLDecoder, EthDecoder
import netifaces as ni
from src import predict_model

MODEL_PATH = 'model/'
LOGS_PATH = 'logs/'
FAIL = '\033[91m'
ENDC = '\033[0m'


class ModelPredict:
    def __init__(self, protocol, io, srcPort, dstPort, sumBytePayload, srcIP, dstIP, buffer):
        self.protocol = protocol
        self.io = io
        self.srcPort = srcPort
        self.dstPort = dstPort
        self.srcIP = srcIP
        self.dstIP = dstIP
        self.sumBytePayload = sumBytePayload
        self.buffer_traffic = buffer
        self.predict()

    def predict(self):
        data = [self.protocol, self.io, self.srcPort, self.dstPort, self.sumBytePayload]
        result = predict_model.predict(X=data, buffer=self.buffer_traffic)
        result_knn, result_lstm = result.get_result()
        print('lstm:', result_lstm, 'knn:', result_knn)
        if result_knn == 1 and result_lstm > 0:
            result = 0
        else:
            result = 1

        with open(LOGS_PATH + 'logs.csv', 'a') as wt:
            wt.write(str(result) + ',' + str(self.srcIP) + ',' + str(self.dstIP) + '\n')
            wt.close()


class DecoderThread(Thread):
    def __init__(self, pcapObj=None, Interface=None):
        datalink = pcapObj.datalink()
        self.Interface = Interface
        if pcapy.DLT_EN10MB == datalink:
            self.decoder = EthDecoder()
        elif pcapy.DLT_LINUX_SLL == datalink:
            self.decoder = LinuxSLLDecoder()
        else:
            raise Exception("Unsupported datalink type: " % datalink)

        self.pcap = pcapObj
        self.buffer_traffic = []
        Thread.__init__(self)

    def run(self):
        self.pcap.loop(0, self.packetHandler)

    def display_hex(self, pkt):
        return pkt.get_data_as_string()

    def encode_protocol(self, protocol):
        # tcp=1;udp=2;others=3
        if protocol == 6:
            return 1
        elif protocol == 17:
            return 2
        else:
            return 3

    def encode_port(self, port):
        # ports longer than 3 digits are irrelevant
        if len(str(port)) > 3:
            return 0
        else:
            return int(port)

    def packetHandler(self, hdr, data):
        p = self.decoder.decode(data)
        ip = p.child()
        tcp = ip.child()
        payload = self.display_hex(p)

        myAddr = ni.ifaddresses(self.Interface)[ni.AF_INET][0]['addr']

        try:
            srcIP = ip.get_ip_src()
            if myAddr == srcIP:
                srcIP = 0
        except AttributeError:
            srcIP = 0

        try:
            dstIP = ip.get_ip_dst()
            if myAddr == dstIP:
                dstIP = 0
        except AttributeError:
            dstIP = 0

        try:
            srcPort = tcp.get_th_sport()
        except AttributeError:
            srcPort = 0

        try:
            dstPort = tcp.get_th_dport()
        except AttributeError:
            dstPort = 0

        if dstPort > 0:
            sumBytePayload = sum(payload) / dstPort
        else:
            sumBytePayload = sum(payload)

        try:
            protocol = tcp.protocol
        except AttributeError:
            return

        io = 1  # input

        if protocol is None:  # ARP
            return

        # protocol 17 = UDP

        if protocol == 1:  # ICMP
            if tcp.get_icmp_num_addrs() > 0:
                io = 0  # output

        if protocol == 6:  # TCP
            myAddr = ni.ifaddresses(self.Interface)[ni.AF_INET][0]['addr']
            if myAddr != ip.get_ip_dst():
                io = 0  # output

        protocol = self.encode_protocol(protocol)
        srcPort = self.encode_port(srcPort)
        dstPort = self.encode_port(dstPort)

        if len(self.buffer_traffic) > 10:
            self.buffer_traffic = []

        self.buffer_traffic.append([protocol, io, srcPort, dstPort, sumBytePayload])

        self.model = Thread(target=ModelPredict, args=(protocol,
                                                       io,
                                                       srcPort,
                                                       dstPort,
                                                       sumBytePayload,
                                                       srcIP,
                                                       dstIP,
                                                       self.buffer_traffic))
        self.model.start()


class listen:
    def __init__(self, interface=None):
        self.interface = interface

    def start(self):
        cap = pcapy.open_live(self.interface, 65536, 0, 100)
        print('Nebusola is working...')
        DecoderThread(cap, self.interface).start()
