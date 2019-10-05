import datetime
from threading import Thread
import pcapy
from impacket.ImpactDecoder import LinuxSLLDecoder, EthDecoder

class DecoderThread(Thread):
    def __init__(self, pcapObj=None, FilePath=None):
        datalink = pcapObj.datalink()
        self.FilePath = FilePath
        if pcapy.DLT_EN10MB == datalink:
            self.decoder = EthDecoder()
        elif pcapy.DLT_LINUX_SLL == datalink:
            self.decoder = LinuxSLLDecoder()
        else:
            raise Exception("Unsupported datalink type: " % datalink)

        self.pcap = pcapObj
        Thread.__init__(self)

    def run(self):
        self.pcap.loop(0, self.packetHandler)

    def display_hex(self, pkt):
        return pkt.get_data_as_string()


    def packetHandler(self, hdr, data):
        p = self.decoder.decode(data)
        ip = p.child()
        tcp = ip.child()
        try:
            src = (ip.get_ip_src(), tcp.get_th_sport())
        except AttributeError:
            print('Source Port not found')
        try:
            dst = (ip.get_ip_dst(), tcp.get_th_dport())
        except AttributeError:
            print('Destination Port not found')

        payload = self.display_hex(p)
        # with open(self.FilePath, 'a') as wf:
        #     wf.write()
        #     wf.close()

        try:
            sumBytePayload = sum(payload) / dst[1]
        except UnboundLocalError:
            sumBytePayload = sum(payload)

        protocol = tcp.protocol

        if protocol is None:
            return

        try:
            lenPayload = len(payload) / dst[1]
        except UnboundLocalError:
            lenPayload = len(payload)

        try:
            srcPort = src[1]
        except UnboundLocalError:
            srcPort = 0

        try:
            dstPort = dst[1]
        except UnboundLocalError:
            dstPort = 0

        #print(sumBytePayload, lenPayload)
        LOGS = str(protocol) + '|' + str(srcPort) + '|' + str(dstPort) + '|' + str(sumBytePayload) + '|' +\
        str(lenPayload)
        print(LOGS)

class intercept:
    def __init__(self, type=None, interface=None):
        self.interface = interface
        self.type = type
        self.fileName = None
        self.timeLog = None
        self.path = "logs/" + self.type + "/"
        self.net = None
        self.mask = None
        self.datalink = None

    def saveToLog(self):
        now = datetime.datetime.now()
        self.timeLog = str(now.day) + "-" + str(now.month) + "-" + str(now.year) + "_" + str(now.hour) + \
                       ":" + str(now.minute) + ".log"
        self.fileName = self.type + "-" + self.timeLog
        return self.path + self.fileName

    def start(self):
        absolutePathFile = self.saveToLog()
        cap = pcapy.open_live(self.interface, 65536, 0, 100)
        #cap.setfilter(r'ip proto \tcp')
        self.net = cap.getnet()
        self.mask = cap.getmask()
        self.datalink = cap.datalink()
        DecoderThread(cap, absolutePathFile).start()