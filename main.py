# #!/usr/bin/python
from scapy.all import *
from difflib import SequenceMatcher
from decimal import Decimal 
from analyzer import anomaly_analyzer

from collect_stat import collect_stat
from Util import *

from multiprocessing import Process, Queue



statistics_collector = collect_stat()
anom_anlyzer = anomaly_analyzer()
#indication = ['SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.6','SSH-2.0-libssh_0.7.0','SSH-2.0-OpenSSH_7.6p1 Debian-4','hmac-sha2-256,hmac-sha2-512']
indication = ['SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.6','SSH-2.0-libssh_0.7.0','SSH-2.0-OpenSSH_7.6p1 Debian-4','hmac-sha2-256,hmac-sha2-512']

clean_csv()

q = Queue()
# We do multi processing so we need a lock
lock = Lock()
p1 = Process(target=statistics_collector.run, args=(q,lock,))
p2 = Process(target=anom_anlyzer.run,args=(lock,))
p2.start()
p1.start()


## In every handshake the are two messages we sniff 
## So we send one alert about every two messages.

counter = 0
def ssh_handshake_logic(pkt):
    global counter
    global q
    if counter == 0:
        counter = 1
    else:
        #checkTime(pkt)
        print 'Detect heand shake'
        q.put(pkt)
        counter = 0

def my_sniffer(pkt):
    if pkt[IP].src != '10.0.0.26' and  pkt[IP].dst != '10.0.0.26' : #My computer IP
        # pkt.show()
        try:
            info = pkt[Raw].load
        except:
            return

        #print(info)
        for i in indication:
            # Sometimes there are other noises in the packet data so that 80% match is OK.
            rat = SequenceMatcher(a=info,b=str(i)).ratio()
            if Decimal(rat) > Decimal(0.8):
                # print str(info[:-2]) 
                # print i         
                # print str(rat) 
                ssh_handshake_logic(pkt)

 
sniff(iface="enp0s3", prn=my_sniffer,filter="tcp and port 22",count=0)

