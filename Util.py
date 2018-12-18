from time import sleep
from datetime import datetime
from scapy.all import *

def checkTime(pkt):
    now = datetime.now()
    if not (8 < int(now.hour) < 16) :
        print 'Alert ' + pkt[IP].src + ' try to connect outside the permitted working hours'





def clean_csv():
    with open("ssh_logs.csv","r") as input:
        with open("ssh_logs.csv","wb") as output: 
            for line in input:
                pass
    with open('ssh_logs.csv', 'a') as csvfile:
        row = 'IP,timestamp,counter\n' 
        csvfile.write(row)         
        csvfile.write('1.1.1.1,7,0\n')
        csvfile.write('9.9.9.9,7,0')

