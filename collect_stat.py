# #!/usr/bin/python
from scapy.all import *
from multiprocessing import Process, Queue
import csv
import time

class collect_stat():
    def __init__(self):
        self.con_data_DS = []
        self.counter = 0
        self.lock = None
        self.queue = None
    def run(self,q,lock):
        self.lock = lock

        while True: 
            time.sleep(1)
            popped = q.get()
            self.set_new_pkt(popped)
            

    def set_new_pkt(self,pkt):
        self.lock.acquire()
        with open('ssh_logs.csv', 'a') as csvfile:
            row = str(pkt[IP].src) + ',' + str(time.time()) + ',' + str(self.counter) + '\n'
            csvfile.write(row)
            self.counter += 1
        self.lock.release()