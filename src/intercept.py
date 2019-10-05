import datetime
from threading import Thread
import pcapy
from impacket.ImpactDecoder import LinuxSLLDecoder, EthDecoder
import netifaces as ni

class DecoderThread(Thread):
    def __init__(self, pcapObj=None, FilePath=None, Interface=None):
        datalink = pcapObj.datalink()
        self.FilePath = FilePath
        self.Interface = Interface
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
        payload = self.display_hex(p)

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
            lenPayload = len(payload) / dstPort
        else:
            sumBytePayload = sum(payload)
            lenPayload = len(payload)

        protocol = tcp.protocol
        io = 1#input

        if protocol is None:#ARP
            return

        #protocol 17 = UDP

        if protocol == 1:#ICMP
            if tcp.get_icmp_num_addrs() > 0:
                io = 0#output

        if protocol == 6:#TCP
            myAddr = ni.ifaddresses(self.Interface)[ni.AF_INET][0]['addr']
            if myAddr != ip.get_ip_dst():
                io = 0#output

        #Protocol|I/O|SrcPort|DstPort|SumPayload|LenPayload
        LOGS = str(protocol) + '|' + str(io) + '|' + str(srcPort) + '|' + str(dstPort) + '|' + str(sumBytePayload) + '|' +\
        str(lenPayload) + '\n'
        with open(self.FilePath, 'a') as wf:
            wf.write(LOGS)
            wf.close()

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
        DecoderThread(cap, absolutePathFile, self.interface).start()